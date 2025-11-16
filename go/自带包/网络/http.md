Go语言内置的net/http包十分的优秀，提供了HTTP客户端和服务端的实现。
# 变量

```go
var NoBody = noBody{}
```

NoBody 是一个 [io.ReadCloser](https://pkg.go.dev/io#ReadCloser)，没有字节。Read 始终返回 EOF，Close 始终返回 nil。它可以在传出客户端请求中使用，以显式表示请求具有零字节。但是，另一种方法是简单地将 [Request.Body] 设置为 nil。

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

## 1.5 func MaxBytesReader(w ResponseWriter, r io.ReadCloser, n int64) io.ReadCloser

- 作用：主要用于限制HTTP请求体（Request Body）的最大大小，防止客户端（无论是意外还是恶意）发送过大的请求，从而保护服务器资源免于被耗尽
    -  **`w http.ResponseWriter`​**​：服务器的响应写入器。当请求体过大时，函数内部可能会利用它来确保连接被正确关闭或处理。
    
    - ​**​`r io.ReadCloser`​**​：通常传入原始的请求体 `r.Body`。它必须实现 `io.ReadCloser`接口（即同时包含 `Read`和 `Close`方法）。
    
    - ​**​`n int64`​**​：允许读取的请求体的最大字节数。
- 当从被包装的 `r.Body`中读取的数据量超过设定的 `n`时：

    1. 后续的读取操作会​**​立即返回一个错误​**​。
    
    2. 常见的错误信息是 `"http: request body too large"`。
    
    3. 你需要在后续读取请求体的代码中（例如 `io.ReadAll(r.Body)`或 `json.NewDecoder(r.Body).Decode(...)`）检查并处理这个错误，通常向客户端返回 `http.StatusRequestEntityTooLarge`(413) 状态码

    4. 当 `http.MaxBytesReader`检测到读取的数据量超过设置的限制时，它不会立即向客户端发送响应，而是会​**​在后续读取请求体（`r.Body`）时返回一个特定的错误​**​。
    

调用后，它返回一个包装过的 `io.ReadCloser`，你应该用其​**​替换原始的 `r.Body`**。

```go
http.HandleFunc("/upload", func(w http.ResponseWriter, r *http.Request) {
    // 限制请求体最大为 1MB
    r.Body = http.MaxBytesReader(w, r.Body, 1 * 1024 * 1024) // 1MB

    // 尝试读取整个请求体
    body, err := io.ReadAll(r.Body)
    if err != nil {
        // 检查是否是请求体过大的错误
        if strings.Contains(err.Error(), "http: request body too large") {
            http.Error(w, "请求体过大", http.StatusRequestEntityTooLarge)
            return
        }
        // 处理其他读取错误
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    // ... 处理 body
})
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
## 2.2 HandlerFunc

`HandlerFunc` 是​**​接口型函数模式最经典的实现​**​。它完美展示了如何通过函数类型实现接口，极大简化 HTTP 处理器的编写。

**设计精妙之处**：

1. ​**​类型转换即实现​**​：任何 `func(ResponseWriter, *Request)` 函数都可转为 `Handler`
2. ​**​零成本抽象​**​：没有额外内存分配
3. ​**​闭包友好​**​：天然支持状态捕获

```go
// 1. 定义函数类型
type HandlerFunc func(ResponseWriter, *Request)

// 2. 实现接口方法
func (f HandlerFunc) ServeHTTP(w ResponseWriter, r *Request) {
    f(w, r) // 关键：直接调用函数本身
}

```

```go
// 1. 直接定义处理函数
welcome := func(w ResponseWriter, r *Request) {
    fmt.Fprintf(w, "Welcome! %s", r.URL.Query().Get("name"))
}

// 2. 注册路由（函数秒变处理器）
http.Handle("/welcome", http.HandlerFunc(welcome))

// 更简洁的写法（无需中间变量）
http.Handle("/hello", http.HandlerFunc(func(w ResponseWriter, r *Request) {
    fmt.Fprint(w, "Hello World!")
}))
```
## 2.3 Dir类型

http.Dir 是 Go 语言 net/http 包中用于表示文件系统目录的类型，主要用于提供静态文件服务。它实现了 **http.FileSystem** 接口，允许通过 HTTP 访问指定目录下的文件。

```go
type Dir string
```
- ​**本质**：是 `string` 类型的别名，表示文件系统的绝对或相对路径（如 `"./static"`）。
- ​**实现接口**：`http.FileSystem`（需实现 `Open` 方法）。

### 2.3.1 Open(name string) (http.File, error)

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

## 2.4 FileSystem类型

http.FileSystem 是 Go 语言 net/http 包中用于抽象文件系统访问的接口类型，允许通过 HTTP 协议提供文件服务。它不限于物理磁盘文件，可以支持内存文件、嵌入式资源或云存储（如 S3）等。
```go
type FileSystem interface {
    Open(name string) (File, error)
}
```
## 2.5 Header类型

`http.Header` 是 Go 语言 `net/http` 包中用于操作 HTTP 头部信息的类型。它是一个键值对集合，键为字符串，值为字符串切片（`[]string`），支持多值头部（如 `Accept-Encoding: gzip, deflate`）。
```go
type Header map[[string]
```
### 2.5.1 Get(key string) string

- 作用：获取键对应的第一个值。
```go
contentType := header.Get("Content-Type") // 返回 "application/json"
```
### 2.5.2 Set(key, value string)

- 作用：设置键的值，覆盖所有现有值。
```go
// 强制设置单值头部（如 `Authorization`）。
header.Set("Authorization", "Bearer abc123")
```
### 2.5.3 Add(key, value string)

- 作用：为键追加一个值，保留现有值。
```go
// 添加多值头部（如 `Accept-Language`）。
header.Add("Accept-Language", "en-US")
header.Add("Accept-Language", "zh-CN") // 最终值：["en-US", "zh-CN"]
```
### 2.5.4 Del(key string)

- 作用：删除键及其所有值。
```go
// 移除敏感或冗余头部（如 `X-Secret-Token`）。
header.Del("X-Debug-Info")
```
### 2.5.5 Values(key string) \[\]string

- 作用：获取键对应的所有值。
```go
// 处理多值头部（如 `Cache-Control`）。
langs := header.Values("Accept-Language") // 返回 ["en-US", "zh-CN"]
```
### 2.5.6 Write(w io.Writer) error

- 作用：将头部按 HTTP 格式写入 `io.Writer`
```go
// 手动构建 HTTP 响应或请求。
var buf bytes.Buffer
header.Write(&buf) // 生成 "Content-Type: application/json\r\n..."
```
## 2.6 Request

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
### 2.6.1 ParseForm() error

- 作用：解析 URL 查询参数和 `application/x-www-form-urlencoded` 类型的请求体。
- 调用关系：在访问 `r.Form` 或 `r.PostForm` 前必须调用。
```go
if err := r.ParseForm(); err != nil {
    http.Error(w, "Bad Request", http.StatusBadRequest)
    return
}
name := r.Form.Get("name")
```
### 2.6.2 FormValue(key string) string

- 作用：获取 URL 查询参数或 POST 表单中指定键的值（自动调用 `ParseForm`）。
- 注意：若键存在多个值，返回第一个值。
### 2.6.3 func (r \*Request) FormFile(key string) (multipart.File, \*multipart.FileHeader, error)

- 作用：返回表单键提供的第一个文件，如有必要，FormFile 会调用 Request.ParseMultipartForm （默认的内存大小限制是 32MB）和 Request.ParseForm
- 接收一个字符串参数 `key`，这个 `key`对应于HTML表单中文件上传输入框（`<input type="file">`）的 `name`属性值
- ​multipart.File：一个实现了`io.Reader`接口的对象，用于读取文件内容
- \*multipart.FileHeader:包含文件的元数据，如文件名、大小和MIME信息
- error:表示操作过程中是否发生错误

### 2.6.4 PostFormValue(key string) string

- 作用：仅获取 POST 表单中指定键的值（自动调用 `ParseForm`）。
### 2.6.5 ParseMultipartForm(maxMemory int64) error

- 作用：解析 `multipart/form-data` 类型的请求体（如文件上传）。
- 参数：`maxMemory` 指定内存缓存大小（超出部分写入临时文件）。
- 调用此方法后，解析得到的所有表单数据（包括普通字段和上传的文件信息）会存储在 `http.Request`对象的 `MultipartForm`字段中，此后你可以通过该字段或其它辅助方法来访问数据
```go
if err := r.ParseMultipartForm(10 << 20); err != nil { // 10MB
    http.Error(w, "Bad Request", http.StatusBadRequest)
    return
}
fileHeader := r.MultipartForm.File["avatar"][0]
```
### 2.6.6 Cookie(name string) (\*Cookie, error)

- 作用：获取指定名称的 Cookie。
### 2.6.7 WithContext(ctx context.Context) \*Request

- 作用：创建绑定新上下文的新请求（常用于中间件传递数据或超时控制）。
```go
ctx := context.WithValue(r.Context(), "userID", 123)
newReq := r.WithContext(ctx)
```
## 2.7 ResponseWriter

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
## 2.8 ServeMux

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

### 2.8.1 NewServeMux() \*ServeMux

- 作用：创建一个新的ServeMux对象
### 2.8.2 Handle(pattern string, handler http.Handler)

- 作用：将 `handler` 注册到指定的路径模式 `pattern`。
    - `pattern`：URL 路径匹配模式（如 `"/api"` 或 `"/static/"`）。
    - `handler`：实现了 `http.Handler` 接口的对象。
```go
mux := http.NewServeMux()
mux.Handle("/", &HomeHandler{}) // 自定义处理器
```
### 2.8.3 HandleFunc(pattern string, handler func(http.ResponseWriter, \*http.Request))

- 作用：将函数 `handler` 转换为 `http.Handler` 并注册到 `pattern`。
```go
mux := http.NewServeMux()
mux.HandleFunc("/hello", func(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Hello, ServeMux!"))
})
```
### 2.8.4 Handler(r \*http.Request) (handler http.Handler, pattern string)

- 作用：根据请求 `r` 查找匹配的处理器和路径模式。
    - 一般用于中间件或自定义路由逻辑，较少直接调用。
```go
handler, pattern := mux.Handler(r)
log.Printf("Request to %s handled by %T", pattern, handler)
```
### 2.8.5 ServeHTTP(w http.ResponseWriter, r \*http.Request)

- 作用：实现 `http.Handler` 接口，处理请求并调用匹配的处理器。
    - 用户通常不直接调用此方法，由 `http.Server` 自动触发。
## 2.9 路径匹配

ServeMux 的路径匹配遵循以下优先级规则，且区分大小写：

1. ​**最长路径优先**：  
    例如，注册了 `/` 和 `/api`，请求 `/api` 会匹配后者。
2. ​**子树路径匹配**：  
    以 `/` 结尾的模式（如 `/images/`）会匹配该路径及其子路径（如 `/images/1.jpg`）。
3. ​**精确匹配**：  
    不以 `/` 结尾的模式（如 `/about`）仅匹配完全相同的路径（不匹配 `/about/`）。
## 2.10 Client

`http.Client`是Go语言`net/http`包中用于发送HTTP请求并接收HTTP响应的核心结构体。

```go
type Client struct {
	// Transport specifies the mechanism by which individual
	// HTTP requests are made.
	// If nil, DefaultTransport is used.
	Transport RoundTripper

	// CheckRedirect specifies the policy for handling redirects.
	// If CheckRedirect is not nil, the client calls it before
	// following an HTTP redirect. The arguments req and via are
	// the upcoming request and the requests made already, oldest
	// first. If CheckRedirect returns an error, the Client's Get
	// method returns both the previous Response (with its Body
	// closed) and CheckRedirect's error (wrapped in a url.Error)
	// instead of issuing the Request req.
	// As a special case, if CheckRedirect returns ErrUseLastResponse,
	// then the most recent response is returned with its body
	// unclosed, along with a nil error.
	//
	// If CheckRedirect is nil, the Client uses its default policy,
	// which is to stop after 10 consecutive requests.
	CheckRedirect func(req *Request, via []*Request) error

	// Jar specifies the cookie jar.
	//
	// The Jar is used to insert relevant cookies into every
	// outbound Request and is updated with the cookie values
	// of every inbound Response. The Jar is consulted for every
	// redirect that the Client follows.
	//
	// If Jar is nil, cookies are only sent if they are explicitly
	// set on the Request.
	Jar CookieJar

	// Timeout specifies a time limit for requests made by this
	// Client. The timeout includes connection time, any
	// redirects, and reading the response body. The timer remains
	// running after Get, Head, Post, or Do return and will
	// interrupt reading of the Response.Body.
	//
	// A Timeout of zero means no timeout.
	//
	// The Client cancels requests to the underlying Transport
	// as if the Request's Context ended.
	//
	// For compatibility, the Client will also use the deprecated
	// CancelRequest method on Transport if found. New
	// RoundTripper implementations should use the Request's Context
	// for cancellation instead of implementing CancelRequest.
	Timeout time.Duration
}
```

| 字段名                     | 类型                                         | 功能说明                                                  | 默认值                        | 注意事项与示例                                                                                                                                                                                                                                                                                                                                                               |
| ----------------------- | ------------------------------------------ | ----------------------------------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ​**​`Transport`​**​     | `RoundTripper`接口                           | 指定HTTP事务（请求-响应）的完整运行机制，是客户端最核心的组件，负责连接管理、协议细节等底层传输逻辑。 | `http.DefaultTransport`    | 1. ​**​连接池​**​：默认的 `DefaultTransport`会维护连接池以复用连接，提升性能。关键配置包括 `MaxIdleConns`（总最大空闲连接数，默认100）和 `MaxIdleConnsPerHost`（每主机最大空闲连接数，​**​默认2​**​，此值过小可能导致高并发时频繁建连）<br><br>。  <br>2. ​**​自定义​**​：可实现自定义的 `RoundTripper`以控制代理、TLS、压缩等底层细节<br><br>。  <br>3. ​**​超时​**​：`Transport`本身可设置更细粒度的超时（如 `DialContext.Timeout`, `TLSHandshakeTimeout`），这与 `Client.Timeout`是互补的<br><br>。 |
| ​**​`CheckRedirect`​**​ | `func(req *Request, via []*Request) error` | 定义处理HTTP重定向的策略。当收到3xx响应时，客户端在跟随重定向前会调用此函数。            | 默认策略：在10次连续重定向后停止<br><br>。 | 1. ​**​控制逻辑​**​：可通过此函数限制重定向次数、记录重定向路径或根据特定条件（如URL）中止重定向<br><br>。  <br>2. ​**​特殊错误​**​：若函数返回 `http.ErrUseLastResponse`，则客户端返回最近一个响应且不关闭其Body，并返回 `nil`错误<br><br>。  <br>示例：`func(req *http.Request, via []*http.Request) error { if len(via) >= 5 { return fmt.Errorf("stopped after %d redirects", len(via)) } return nil }`                                           |
| ​**​`Jar`​**​           | `CookieJar`接口                              | 管理Cookie的容器。自动存储响应中的Cookie，并在后续出站请求中自动添加相关的Cookie。    | `nil`                      | 1. ​**​默认行为​**​：如果为 `nil`，则只有在请求上显式设置的Cookie才会被发送，响应中的Cookie会被忽略<br><br>。  <br>2. ​**​使用​**​：通常使用 `cookiejar.New(nil)`创建Jar实例<br><br>。该Jar是内存型的，程序重启后Cookie会丢失。如需持久化，需自行实现。                                                                                                                                                                                           |
| ​**​`Timeout`​**​       | `time.Duration`                            | 设置客户端每次请求从开始到结束（包括重定向、读取响应体）的​**​总时间限制​**​。           |                            |                                                                                                                                                                                                                                                                                                                                                                       |
1. **复用Client实例​**​：`http.Client`是并发安全的，其底层的 `Transport`维护了连接池。​**​强烈建议在应用程序中复用同一个Client实例​**​（或极少数几个配置不同的实例），而不是为每个请求都创建新的Client。这可以避免不必要的连接建立与销毁开销，并有效利用连接池。
    
2. ​**​资源清理​**​：使用 `Client`发送请求后，​**​必须关闭响应体（`resp.Body.Close()`）​**​，通常使用 `defer`语句确保执行。这是为了将连接返回到连接池以供复用，否则可能导致资源（如文件描述符）泄漏。
    
3. ​**​默认客户端​**​：包级别的便捷函数（如 `http.Get`, `http.Post`）使用默认的 `http.DefaultClient`。它是一个没有设置超时的基本客户端，在生产环境中直接使用需谨慎，最好根据需求创建具有适当配置（尤其是 `Timeout`）的自定义Client。
### 2.10.1 Get

- **定义​**​: `func (c *Client) Get(url string) (resp *Response, err error)`
    
- ​**​用途​**​: 向指定URL发起​**​GET​**​请求。适用于简单的数据获取。

```go
// 使用默认客户端
resp, err := http.Get("https://api.example.com/data")
if err != nil {
    // 处理网络错误或协议错误
    log.Fatal(err)
}
defer resp.Body.Close() // 必须关闭响应体

body, _ := io.ReadAll(resp.Body)
fmt.Printf("Status: %s, Body: %s\n", resp.Status, string(body))
```

- **注意​**​: 非2xx状态码（如404、500）​**​不会​**​被该方法认为是错误，你需要检查 `resp.StatusCode`。
### 2.10.2 Post 和 PostForm​

- **定义​**​:
    
    - `func (c *Client) Post(url, contentType string, body io.Reader) (resp *Response, err error)`
        
    - `func (c *Client) PostForm(url string, data url.Values) (resp *Response, err error)`
        
    
- ​**​用途​**​: ​**​Post​**​用于发送自定义内容类型（如JSON）的数据。​**​PostForm​**​专用于发送表单数据（`application/x-www-form-urlencoded`）。

```go
// 使用 Post 发送 JSON
jsonData := `{"title": "Post Example"}`
resp, err := http.Post("https://api.example.com/posts", "application/json", strings.NewReader(jsonData))
// ... 错误处理和资源清理

// 使用 PostForm 提交表单
formData := url.Values{}
formData.Add("username", "admin")
formData.Add("password", "secret")
resp, err := http.PostForm("https://api.example.com/login", formData)
// ... 错误处理和资源清理
```
### 2.10.3 DO

- **定义​**​: `func (c *Client) Do(req *Request) (*Response, error)`
    
- ​**​用途​**​: 这是最基础、最强大的方法。`Get`, `Post`等方法内部都调用了`Do`。当需要设置自定义请求头、使用特定上下文（Context）或更精细地控制请求时，必须使用`Do`方法。

```go
// 1. 创建请求对象
req, err := http.NewRequestWithContext(context.Background(), "GET", "https://api.example.com/data", nil)
if err != nil {
    log.Fatal(err)
}
// 2. 设置自定义请求头
req.Header.Add("Authorization", "Bearer your-token")
req.Header.Add("User-Agent", "MyApp/1.0")

// 3. 使用配置好的客户端发送请求
client := &http.Client{Timeout: 10 * time.Second}
resp, err := client.Do(req)
if err != nil {
    // 处理错误，可能是网络错误、超时等
    log.Fatal(err)
}
defer resp.Body.Close() // 至关重要！

// ... 处理响应
```

​**​关键提醒​**​:

- 如果返回的 `err`为 `nil`，​**​必须​**​在读取完响应体后调用 `resp.Body.Close()`来释放网络连接，使其能被连接池复用。通常使用 `defer`来确保执行。
    
- 错误可能由客户端策略（如重定向检查失败）或HTTP协议问题（如网络连接失败）引起。非2xx状态码​**​不会​**​导致错误
### 2.10.4 CloseIdleConnections

- **定义​**​: `func (c *Client) CloseIdleConnections()`
    
- ​**​用途​**​: 关闭客户端传输层中所有处于空闲（keep-alive）状态的连接。它不会中断正在使用的连接。通常在应用程序退出或明确知道一段时间内不会有新请求时调用，有助于释放系统资源

```go
​client := &http.Client{Timeout: 30 * time.Second}
// ... 使用client进行一系列请求
// 程序退出前或合适时机
client.CloseIdleConnections()
```
### 2.10.5 注意事项

1. ​**​资源管理：务必关闭响应体​**​

    这是最重要也是最容易出错的一点。只要`client.Do`, `Get`, `Post`等函数返回的`err`为`nil`，你就​**​必须​**​在处理完响应后关闭`resp.Body`。使用`defer`是确保这一操作得以执行的最佳方式。

```go
resp, err := http.Get("...")
if err != nil {
    return err
}
defer resp.Body.Close() // 使用defer，无论后续逻辑如何，都会执行关闭
// ... 读取resp.Body
```

2. **​错误处理：区分网络错误与HTTP错误​**

    - **网络/协议错误​**​：会在`err`中体现，如超时、DNS解析失败、连接被拒绝等。
    
    - ​**​HTTP错误​**​：指4xx, 5xx等状态码。这些​**​不会​**​使`err`不为nil，你需要手动检查`resp.StatusCode`。

```go
resp, err := http.Get("...")
if err != nil {
    // 处理网络或协议错误
    log.Fatal("Request failed:", err)
}
defer resp.Body.Close()

if resp.StatusCode != http.StatusOK {
    // 处理HTTP层面的错误（如404 Not Found, 500 Internal Server Error）
    log.Fatalf("HTTP error: %s", resp.Status)
}
// ... 正常处理响应体
```

3. **性能优化：复用Client实例​**​

- `http.Client`是并发安全的，其内部通过 `Transport`机制管理连接池。​**​绝对不要​**​为每个HTTP请求都创建一个新的`Client`。应该在程序生命周期内复用同一个（或少量几个配置不同的）Client实例，这样可以极大提升性能，避免频繁建立和断开TCP连接

- 确保连接能被复用的正确操作包括两个步骤：​**​将响应体读取完毕​**​和​**​关闭响应体​**​。

    1. ​**​读取完毕​**​：这是为了将连接中的残留数据清空，为下一个请求准备好一个“干净”的连接。如果你不关心响应内容，也需要将其读取并丢弃。
    
    2. ​**​关闭响应体​**​：这是最关键的一步，它会通知底层的 `Transport`：“这个连接我已经用完了，请把它收回到连接池里。”

```go
// 好的做法：在全局范围初始化一个客户端
var myClient = &http.Client{
    Timeout: 15 * time.Second,
}

func makeRequest() {
    resp, err := myClient.Get("...")
    // ...
}
```

4. **配置超时​**​

    永远不要使用无限期等待的默认客户端（`http.DefaultClient`没有设置超时）。为你的客户端设置合理的超时时间，防止请求无限期挂起，这对生产环境的稳定性至关重要。

```go
client := &http.Client{
    Timeout: 15 * time.Second, // 总超时时间，包括连接、重定向、读取响应体
}
```

| 方法                        | 最佳使用场景                                        | 灵活性        | 是否自动处理重定向/Cookie | 响应体是否必须关闭 |
| ------------------------- | --------------------------------------------- | ---------- | ---------------- | --------- |
| ​**​`Get`​**​             | 快速发起简单的GET请求                                  | 低          | 是                | ​**​是​**​ |
| ​**​`Post`/`PostForm`​**​ | 快速发起简单的POST请求（JSON或表单）                        | 低          | 是                | ​**​是​**​ |
| ​**​`Do`​**​              | ​**​需要高度自定义​**​的请求（如设置Header、Context、使用非标准方法） | ​**​极高​**​ | 遵循客户端配置          | ​**​是​**  |
`http.Client`的高性能很大程度上得益于其底层的连接池机制，由`Transport`类型管理

。了解几个关键配置有助于优化高频请求场景：

- ​**​MaxIdleConnsPerHost​**​：默认值为​**​2​**​。这表示对同一个目标主机，最多只保持2个空闲连接。在高并发场景下，此值设置过小可能导致需要频繁创建新连接。可以根据需要适当调大。
    
- ​**​DisableKeepAlives​**​：默认为`false`，即启用长连接（连接复用）。除非有特殊理由，否则不应禁用。
    
- ​**​IdleConnTimeout​**​：空闲连接在连接池中保留的最长时间，超时后连接将被关闭。