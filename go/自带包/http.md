Go语言内置的net/http包十分的优秀，提供了HTTP客户端和服务端的实现。

# 1 常用函数

## 1.1 ListenAndServe

- 函数签名
```go
func ListenAndServe(addr string, handler Handler) error
```

- 启动一个 HTTP 服务器，监听指定地址。
    - 监听一个TCP网络地址，使用Handler来处理连接上的请求
- 连接配置保持为TCP keep-alives
    - 自动为每个接受的连接启用 ​**TCP keep-alive** 机制，防止长时间空闲连接占用资源。
    - Keep-alive 间隔由操作系统决定（通常约 1-2 小时）。
- 处理请求
    - 对每个新连接，启动一个 goroutine 处理请求。
    - 使用传入的 `handler` 处理 HTTP 请求。若 `handler` 为 `nil`，默认使用 `http.DefaultServeMux`（全局多路复用器）。
- 错误返回
    - 一般返回非空error

```go
  
func index(w http.ResponseWriter, r *http.Request) {  
    fmt.Fprintln(w, "Hello World")  
}  
  
func main() {  
    http.HandleFunc("/", index)  
    err := http.ListenAndServe(":8080", nil)  
    fmt.Println(err)  
}
```
## 1.2 ListenAndServeTLS

- 函数签名
```go
func ListenAndServeTLS(addr, certFile, keyFile string, handler http.Handler) error
```

- ​**参数**：
    - `addr`：监听的 TCP 地址，格式为 `"host:port"`（如 `":443"`）。
    - `certFile`：服务器证书文件路径（通常为 `.pem` 或 `.crt` 文件）。
    - `keyFile`：服务器私钥文件路径（通常为 `.key` 文件）。
    - `handler`：HTTP 请求处理器，若为 `nil`，使用 `http.DefaultServeMux`。
- ​**返回值**：始终返回非 `nil` 错误（如证书无效、权限不足等）。

- ​**启用 HTTPS 加密通信**
    - 使用 ​**TLS（Transport Layer Security）​** 协议加密客户端与服务端之间的数据传输。
    - 默认支持 TLS 1.2 及以上版本（取决于 Go 版本），确保通信安全性。

- **证书与私钥要求**
    - ​**证书（`certFile`）​**：验证服务器身份，需包含完整的证书链（见下文）。
    - ​**私钥（`keyFile`）​**：用于解密客户端发送的加密数据，需严格保密。

- ​**证书链拼接规则**
    - ​**证书链格式**：若证书由 CA 签发，`certFile` 应为 ​**服务器证书 + 中间证书 + 根证书** 的拼接（按顺序）。
    - ​**示例**：
        ```pem
        -----BEGIN CERTIFICATE-----
        （服务器证书内容）
        -----END CERTIFICATE-----
        -----BEGIN CERTIFICATE-----
        （中间证书内容）
        -----END CERTIFICATE-----
        -----BEGIN CERTIFICATE-----
        （根证书内容）
        -----END CERTIFICATE-----
        ```

- ​**验证逻辑**：客户端通过证书链逐级验证信任关系，若中间证书缺失，会导致某些客户端（如浏览器）提示证书错误。
```go
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Secure HTTPS!"))
})

err := http.ListenAndServeTLS(
    ":443", 
    "server.pem", // 证书文件
    "server.key", // 私钥文件
    nil,          // 使用 DefaultServeMux
)
if err != nil {
    log.Fatal("HTTPS 服务启动失败:", err)
}
```

## 1.3 HandleFunc

`http.HandleFunc` 是 Go 语言 `net/http` 包中的一个核心函数，用于向默认的 HTTP 请求多路复用器（`DefaultServeMux`）注册处理函数。当用户访问特定路径时，注册的处理函数会被调用。

- 函数签名
```go
func HandleFunc(pattern string, handler func(http.ResponseWriter, *http.Request))
```

- ​**参数**：
    - `pattern`：URL 路径模式（如 `"/hello"` 或 `"/user/"`）。
    - `handler`：处理函数，需满足 `func(http.ResponseWriter, *http.Request)` 签名。

- **基于 `DefaultServeMux`**
    - `DefaultServeMux` 是全局默认的 HTTP 请求多路复用器。
    - 当调用 `http.ListenAndServe(addr, nil)` 时，若 `handler` 参数为 `nil`，则使用 `DefaultServeMux`。

- **子树路径匹配**  
    - 以斜杠 `/` 结尾的模式表示一个子树路径，匹配该路径及其子路径
```go
   http.HandleFunc("/images/", func(w http.ResponseWriter, r *http.Request) {
    // 匹配 /images/、/images/1.jpg、/images/2023/summer.jpg 等
})
```

- ​**精确匹配**  
    - 不以斜杠结尾的模式需完全匹配路径：
    ```go
    http.HandleFunc("/about", func(w http.ResponseWriter, r *http.Request) {
        // 仅匹配 /about，不匹配 /about/ 或 /about-us
    })
    ```
## 1.4 Handle

用于向默认的多路复用器（`DefaultServeMux`）注册路由的核心函数。与 `http.HandleFunc` 不同，它接受一个实现了 `http.Handler` 接口的对象，而非直接的处理函数。

- 函数签名
```go
func Handle(pattern string, handler http.Handler)
```

- ​**参数**：
    - `pattern`：URL 路径模式（如 `"/api"` 或 `"/static/"`）。
    - `handler`：必须实现 `http.Handler` 接口的对象（需定义 `ServeHTTP` 方法）。

- **注册 `http.Handler` 对象**  
    将自定义的处理器对象绑定到指定路径模式，允许更复杂的请求处理逻辑（例如状态管理、中间件链等）。
    
- **基于 `DefaultServeMux`**
    - 与 `http.HandleFunc` 一样，依赖全局的 `DefaultServeMux`。
    - 通过 `http.ListenAndServe(addr, nil)` 自动启用。

```go
// 定义处理器类型
type LoggingHandler struct {
    // 可维护状态（如日志记录器、数据库连接等）
    Logger *log.Logger
}

// 实现 ServeHTTP 方法
func (h *LoggingHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    h.Logger.Printf("Request: %s %s", r.Method, r.URL.Path)
    fmt.Fprintf(w, "Logged request to %s", r.URL.Path)
}

// 注册处理器
logger := log.New(os.Stdout, "INFO: ", log.LstdFlags)
http.Handle("/log", &LoggingHandler{Logger: logger})

// 启动服务
http.ListenAndServe(":8080", nil)
```
#### 1.4.1.1 **http.HandleFunc 与 http.Handle 的区别**

- ​**`http.HandleFunc`**：直接接受处理函数。

    ```go
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) { ... })
    ```

- ​**`http.Handle`**：接受实现了 `http.Handler` 接口的对象。

    ```go
    type MyHandler struct{}
    func (h *MyHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) { ... }
    
    http.Handle("/", &MyHandler{})
    ```
    
- ​**等价性**：  
    `http.HandleFunc` 是 `http.Handle` 的语法糖，以下代码等效：

    ```go
    http.Handle("/", http.HandlerFunc(handler))
    ```
# 2 常用类型
## 2.1 Handler

`net/http` 包中，​`http.Handler` 是一个 ​**接口类型**，定义了 HTTP 请求处理器的核心行为。任何实现了该接口的类型都可以处理 HTTP 请求，是构建 Web 服务的核心抽象。
```go
type Handler interface {
    ServeHTTP(http.ResponseWriter, *http.Request)
}
```

- 实现该接口的类型必须定义 `ServeHTTP` 方法，用于处理 HTTP 请求并返回响应。
    -  `http.ResponseWriter`：用于写入响应头和响应体。
    - `*http.Request`：包含客户端请求的所有信息。

任何需要处理 HTTP 请求的自定义逻辑都需要实现该接口。常见的实现方式包括：

1. ​**自定义结构体**：用于复杂逻辑或需要维护状态的场景。
2. ​**函数适配器**：将普通函数转换为 `Handler` 接口。
3. ​**中间件**：通过包装现有的 `Handler` 添加额外功能。

### 2.1.1 http提供的Handler实现
#### 2.1.1.1 FileServer(root FileSystem)

- 作用：用于托管静态文件。
    - 托管前端静态资源（HTML、CSS、JavaScript）。
    - 提供下载文件服务。
```go
fs := http.FileServer(http.Dir("./static"))
http.Handle("/static/", http.StripPrefix("/static/", fs))
```
#### 2.1.1.2 TimeoutHandler(h http.Handler, dt time.Duration, msg string)

- 作用：为处理器添加超时控制。
    - 防止长时间阻塞的操作耗尽服务器资源。
    - 对第三方 API 调用设置超时。
```go
slowHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    time.Sleep(10 * time.Second)
    w.Write([]byte("Done"))
})
timeoutHandler := http.TimeoutHandler(slowHandler, 5*time.Second, "Request timed out")
http.Handle("/slow", timeoutHandler)
```
#### 2.1.1.3 NotFoundHandler()

- 作用：返回一个固定响应 `404 Not Found` 的处理器。
```go
mux.Handle("/missing", http.NotFoundHandler())
```
#### 2.1.1.4 http.StripPrefix(prefix string, h http.Handler)

- 作用：移除请求路径的前缀后，再将请求转发给 `h`。
    - 托管静态文件时，去除 URL 前缀。
```go
fs := http.FileServer(http.Dir("./static"))
mux.Handle("/static/", http.StripPrefix("/static", fs))
```
#### 2.1.1.5 RedirectHandler(url string, code int)

- 作用：返回一个重定向到指定 URL 的处理器。
```go
mux.Handle("/old", http.RedirectHandler("/new", http.StatusMovedPermanently))
```
### 2.1.2 自定义Handler接口

```go
// 定义处理器类型
type HelloHandler struct {
    Greeting string
}

// 实现 ServeHTTP 方法
func (h *HelloHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "%s, World!", h.Greeting)
}

// 使用处理器
func main() {
    handler := &HelloHandler{Greeting: "Hello"}
    http.Handle("/hello", handler) // 注册到路由
    http.ListenAndServe(":8080", nil)
}
// 也能使用HandlerFunc转换为Handler接口
handler := http.HandlerFunc(helloFunc)
```
## 2.2 Dir类型

http.Dir 是 Go 语言 net/http 包中用于表示文件系统目录的类型，主要用于提供静态文件服务。它实现了 **http.FileSystem** 接口，允许通过 HTTP 访问指定目录下的文件。

```go
type Dir string
```
- ​**本质**：是 `string` 类型的别名，表示文件系统的绝对或相对路径（如 `"./static"`）。
- ​**实现接口**：`http.FileSystem`（需实现 `Open` 方法）。

### 2.2.1 Open(name string) (http.File, error)

```go
package main

import "net/http"

func main() {
    // 创建文件服务器，根目录为 "./public"
    fs := http.FileServer(http.Dir("./public"))
    http.Handle("/static/", http.StripPrefix("/static/", fs))
    http.ListenAndServe(":8080", nil)
}
```
- ​**作用**：根据 `name` 路径打开文件，返回 `http.File` 对象。
- ​**逻辑**：
    1. ​**路径拼接**：将 `http.Dir` 表示的目录与请求路径 `name` 合并。
    2. ​**安全检查**：清理路径中的 `..`，防止访问根目录外的文件。
    3. ​**返回文件**：若文件存在且可读，返回文件句柄；否则返回错误（如 `os.ErrNotExist`）。

## 2.3 FileSystem类型

http.FileSystem 是 Go 语言 net/http 包中用于抽象文件系统访问的接口类型，允许通过 HTTP 协议提供文件服务。它不限于物理磁盘文件，可以支持内存文件、嵌入式资源或云存储（如 S3）等。
```go
type FileSystem interface {
    Open(name string) (File, error)
}
```
## 2.4 Header类型

`http.Header` 是 Go 语言 `net/http` 包中用于操作 HTTP 头部信息的类型。它是一个键值对集合，键为字符串，值为字符串切片（`[]string`），支持多值头部（如 `Accept-Encoding: gzip, deflate`）。
```go
type Header map[[string]
```
### 2.4.1 Get(key string) string

- 作用：获取键对应的第一个值。
```go
contentType := header.Get("Content-Type") // 返回 "application/json"
```
### 2.4.2 Set(key, value string)

- 作用：设置键的值，覆盖所有现有值。
```go
// 强制设置单值头部（如 `Authorization`）。
header.Set("Authorization", "Bearer abc123")
```
### 2.4.3 Add(key, value string)

- 作用：为键追加一个值，保留现有值。
```go
// 添加多值头部（如 `Accept-Language`）。
header.Add("Accept-Language", "en-US")
header.Add("Accept-Language", "zh-CN") // 最终值：["en-US", "zh-CN"]
```
### 2.4.4 Del(key string)

- 作用：删除键及其所有值。
```go
// 移除敏感或冗余头部（如 `X-Secret-Token`）。
header.Del("X-Debug-Info")
```
### 2.4.5 Values(key string) \[\]string

- 作用：获取键对应的所有值。
```go
// 处理多值头部（如 `Cache-Control`）。
langs := header.Values("Accept-Language") // 返回 ["en-US", "zh-CN"]
```
### 2.4.6 Write(w io.Writer) error

- 作用：将头部按 HTTP 格式写入 `io.Writer`
```go
// 手动构建 HTTP 响应或请求。
var buf bytes.Buffer
header.Write(&buf) // 生成 "Content-Type: application/json\r\n..."
```
## 2.5 Request

`http.Request` 是 Go 语言 `net/http` 包中表示 HTTP 请求的核心结构体，它封装了客户端请求的所有信息，包括方法、URL、头、体等。
```go
type Request struct {
        Method string

        URL *url.URL

        Header Header

        Body io.ReadCloser

        GetBody func() (io.ReadCloser, error)

        ContentLength int64

        TransferEncoding []string

        Close bool

        Host string

        Form url.Values

        PostForm url.Values

        MultipartForm *multipart.Form

        Trailer Header

        RemoteAddr string

        RequestURI string

        TLS *tls.ConnectionState

        Cancel <-chan struct{}

        Response *Response

        Pattern string

        ctx context.Context

}

```

- 属性
    - Method：HTTP 请求方法（如 `GET`、`POST`、`PUT` 等）。
    - URL：解析后的请求 URL 信息，包含路径、查询参数等。
        - `Path`：请求路径（如 `/api/data`）。
        - `RawQuery`：原始查询字符串（如 `?name=foo&id=123`）。
        - `Query()`：解析后的查询参数（返回 `url.Values` 类型）。
    - Header：HTTP 请求头信息。
    ```go
    contentType := r.Header.Get("Content-Type")
    ```
    - Body：请求体数据流（如 POST 表单或 JSON 数据）。
        - 读取后需关闭：`defer r.Body.Close()`。
        - 不可重复读取，多次使用需缓存（如 `ioutil.ReadAll`）。
    - Form和PostForm
        - `Form`：合并 URL 查询参数和 POST 表单数据（需先调用 `ParseForm`）。
        - `PostForm`：仅包含 POST/PUT 表单数据（需先调用 `ParseForm`）。
    - MultipartForm：解析后的多部分表单数据（如文件上传）。
    - Cookies()：返回请求中的 Cookie 列表。
    ```go
     cookie, err := r.Cookie("session_id")   
    ```
    - Context()：获取请求的上下文（用于传递元数据或超时控制）。
### 2.5.1 ParseForm() error

- 作用：解析 URL 查询参数和 `application/x-www-form-urlencoded` 类型的请求体。
- 调用关系：在访问 `r.Form` 或 `r.PostForm` 前必须调用。
```go
if err := r.ParseForm(); err != nil {
    http.Error(w, "Bad Request", http.StatusBadRequest)
    return
}
name := r.Form.Get("name")
```
### 2.5.2 FormValue(key string) string

- 作用：获取 URL 查询参数或 POST 表单中指定键的值（自动调用 `ParseForm`）。
- 注意：若键存在多个值，返回第一个值。
### 2.5.3 PostFormValue(key string) string

- 作用：仅获取 POST 表单中指定键的值（自动调用 `ParseForm`）。
### 2.5.4 ParseMultipartForm(maxMemory int64) error

- 作用：解析 `multipart/form-data` 类型的请求体（如文件上传）。
- 参数：`maxMemory` 指定内存缓存大小（超出部分写入临时文件）。
```go
if err := r.ParseMultipartForm(10 << 20); err != nil { // 10MB
    http.Error(w, "Bad Request", http.StatusBadRequest)
    return
}
fileHeader := r.MultipartForm.File["avatar"][0]
```
### 2.5.5 Cookie(name string) (\*Cookie, error)

- 作用：获取指定名称的 Cookie。
### 2.5.6 WithContext(ctx context.Context) \*Request

- 作用：创建绑定新上下文的新请求（常用于中间件传递数据或超时控制）。
```go
ctx := context.WithValue(r.Context(), "userID", 123)
newReq := r.WithContext(ctx)
```
## 2.6 ResponseWriter

`http.ResponseWriter` 是 Go 语言 `net/http` 包中用于构建 HTTP 响应的核心接口，它定义了服务端向客户端发送响应的基本操作。

```go
type ResponseWriter interface {
        Header() Header // 获取响应头（用于设置头信息）

        Write([]byte) (int, error) // 写入响应体数据

        WriteHeader(statusCode int) // 设置 HTTP 状态码
}
```

- Header() http.Header：返回响应头的 `Header` 对象（`map[string][]string`），用于设置头信息。
    - 必须在调用 `WriteHeader` 或 `Write` ​**之前** 设置头信息，否则可能不生效。
    - 头信息键名自动转换为 ​**首字母大写**​（如 `content-type` → `Content-Type`）。
```go
w.Header().Set("Content-Type", "application/json")
w.Header().Add("Cache-Control", "max-age=3600")
```

- Write(\[\]byte) (int, error)：向响应体写入数据（如 HTML、JSON、二进制流等）。
    - 如果未调用 `WriteHeader`，第一次调用 `Write` 时会自动触发 `WriteHeader(http.StatusOK)`。
    - 支持多次调用，数据会 ​**追加** 到响应体中。

- WriteHeader(statusCode int)： 显式设置 HTTP 状态码（如 `200`、`404` 等）。
    - 只能调用一次，重复调用会触发日志警告：`http: superfluous response.WriteHeader call`。
    - 必须在 `Write` ​**之前** 调用，否则状态码可能被默认设为 `200`。
```go
w.WriteHeader(http.StatusNotFound)
```
## 2.7 ServeMux

`http.ServeMux` 是 Go 语言 `net/http` 包中用于管理 HTTP 请求路由的核心类型，它是一个 ​**HTTP 请求多路复用器**​（即路由管理器），负责将不同路径的请求分发到对应的处理器。

```go
type ServeMux struct {  
    mu       sync.RWMutex  
    tree     routingNode   
    index    routingIndex  
    patterns []*pattern  
    mux121   serveMux121   
}
```

- mu：读写锁，用于保护路由表（`tree`、`index` 等字段）的并发安全。
    - 写操作​（如注册路由 `Handle`/`HandleFunc`）会获取写锁（`Lock`），阻塞其他读写。
    - ​读操作​（如处理请求 `ServeHTTP`）会获取读锁（`RLock`），允许多个读并行。
- tree：表示路由的 ​**前缀树（Trie 树）​** 结构，用于高效匹配 URL 路径。
- index：路由索引，用于加速特定场景下的查找（如按主机名分类或路径前缀）。
- patterns：存储所有已注册的路由模式（如 `/api`、`/user/{id}`）。
- mux121：旧版路由复用器（如 Go 1.21 之前的实现），通过 `GODEBUG=httpmuxgo121=1` 启用，用于兼容性测试或回退。

### 2.7.1 NewServeMux() \*ServeMux

- 作用：创建一个新的ServeMux对象
### 2.7.2 Handle(pattern string, handler http.Handler)

- 作用：将 `handler` 注册到指定的路径模式 `pattern`。
    - `pattern`：URL 路径匹配模式（如 `"/api"` 或 `"/static/"`）。
    - `handler`：实现了 `http.Handler` 接口的对象。
```go
mux := http.NewServeMux()
mux.Handle("/", &HomeHandler{}) // 自定义处理器
```
### 2.7.3 HandleFunc(pattern string, handler func(http.ResponseWriter, \*http.Request))

- 作用：将函数 `handler` 转换为 `http.Handler` 并注册到 `pattern`。
```go
mux := http.NewServeMux()
mux.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Hello, ServeMux!"))
})
```
### 2.7.4 Handler(r \*http.Request) (handler http.Handler, pattern string)

- 作用：根据请求 `r` 查找匹配的处理器和路径模式。
    - 一般用于中间件或自定义路由逻辑，较少直接调用。
```go
handler, pattern := mux.Handler(r)
log.Printf("Request to %s handled by %T", pattern, handler)
```
### 2.7.5 ServeHTTP(w http.ResponseWriter, r \*http.Request)

- 作用：实现 `http.Handler` 接口，处理请求并调用匹配的处理器。
    - 用户通常不直接调用此方法，由 `http.Server` 自动触发。
## 2.8 路径匹配

ServeMux 的路径匹配遵循以下优先级规则，且区分大小写：

1. ​**最长路径优先**：  
    例如，注册了 `/` 和 `/api`，请求 `/api` 会匹配后者。
2. ​**子树路径匹配**：  
    以 `/` 结尾的模式（如 `/images/`）会匹配该路径及其子路径（如 `/images/1.jpg`）。
3. ​**精确匹配**：  
    不以 `/` 结尾的模式（如 `/about`）仅匹配完全相同的路径（不匹配 `/about/`）。
