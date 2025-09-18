
`encoding/json`为官方自带JSON处理包。提供了对JSON数据的编码和解码功能，可以方便地将Go数据结构转换为JSON格式（称为序列化或编码），以及将JSON数据转换为Go数据结构（称为反序列化或解码）。

# 1 序列化

- 将 Go 结构体、map 或基本类型序列化为 JSON 字节切片。
-  **`json.Marshal(v interface{}) ([]byte, error)`**

**注意事项​**​：

- 只有公开字段可序列化
- 字段可通过标签定制
- 循环引用会报错
- 默认开启HTML转义

```go
// 结构体和JSON映射  
type Conf struct {  
    Addr     string `json:"addr,omitempty"`  
    Port     string `json:"port"`  
    User     string `json:"user"`  
    Password string `json:"password"`  
}  
  
func main() {  
    conf := Conf{  
    Addr:     "1",  
    Port:     "1",  
    User:     "1",  
    Password: "1",  
}
  
    data, _ := json.Marshal(conf)  
    // 格式化json  
    data_dent, _ := json.MarshalIndent(conf, "", " ")  
    fmt.Println(string(data))  
    fmt.Println(string(data_dent))
    }
```

- 设置输出格式
- func MarshalIndent(v any, prefix, indent string) (\[\]byte, error)

```go
b, err := json.MarshalIndent(data, "<prefix>", "<indent>")


/*
Output:

{
<prefix><indent>"a": 1,
<prefix><indent>"b": 2
<prefix>}
*/
```

- 压缩JSON数据：移除不必要的空格
- `json.Compact(dst *bytes.Buffer, src []byte) error`
**参数​**​：

- `dst`：压缩后数据存储的缓冲区
- `src`：待压缩的JSON数据

​**​返回值​**​：

- `error`：语法错误时返回`SyntaxError`

​**​注意事项​**​：

- 会移除所有JSON无效空格和换行符
- 对无效JSON会报错
- 不检查JSON内容有效性

```go
  
type test struct {  
    Content interface{} `json:"content"`  
}  
  
func main() {  
    t := test{Content: "123"}  
    src, _ := json.MarshalIndent(t, "\t", "\t")  
    b := &bytes.Buffer{}  
    json.Compact(b, src)  
    fmt.Println(b)  
}

// {"content":"123"}
```

- HTML转义JSON特殊字符
- `json.HTMLEscape(dst *bytes.Buffer, src []byte)`
 
**参数​**​：

- `dst`：转义后数据存储的缓冲区
- `src`：原始JSON数据

​**​注意事项​**​：

- 转义字符：`<`→`\u003c`，`>`→`\u003e`，`&`→`\u0026`
- 常用来防止XSS攻击
- 不改变JSON结构

```go
func main() {
	src := []byte(`{
	"script": "<script>alert('XSS')</script>"
}`)

	dst := &bytes.Buffer{}
	json.HTMLEscape(dst, src)

	fmt.Println("转义结果:", dst.String())
}

/* 输出：
转义结果: {
	"script": "\u003cscript\u003ealert('XSS')\u003c/script\u003e"
}
*/
```

- 格式化JSON（添加缩进）
- `json.Indent(dst *bytes.Buffer, src []byte, prefix, indent string) error`

**参数​**​：

- `dst`：格式化后数据存储的缓冲区
- `src`：原始JSON数据
- `prefix`：每行前缀
- `indent`：缩进字符串

​**​返回值​**​：

- `error`：语法错误时返回`SyntaxError`

​**​注意事项​**​：

- 对无效JSON会报错
- 缩进建议使用空格而非制表符
- 会规范化JSON结构

```go
func main() {
	src := []byte(`{"name":"Bob","age":30,"skills":["Java","C++"]}`)

	dst := &bytes.Buffer{}
	err := json.Indent(dst, src, "", "  ") // 使用2空格缩进
	
	if err == nil {
		fmt.Println("格式化JSON:\n" + dst.String())
	}
}

/* 输出：
格式化JSON:
{
  "name": "Bob",
  "age": 30,
  "skills": [
    "Java",
    "C++"
  ]
}
*/
```

# 2 反序列化

- 将 JSON 数据解析到 Go 结构体或 map 中。
- **`json.Unmarshal(data []byte, v interface{}) error`**
    - v必须是指针类型
**注意事项​**​：

- 必须传入结构体指针
- JSON字段与结构体标签匹配（区分大小写）
- 多余字段被忽略
- 缺失字段保留零值

```go
// 结构体和JSON映射  
type Conf struct {  
    Addr     string `json:"addr,omitempty"`  
    Port     string `json:"port"`  
    User     string `json:"user"`  
    Password string `json:"password"`  
}  

// 需要和结构体绑定
conf := Conf{}

f, _ := os.Open("./conf.json")  
b, _ := io.ReadAll(f)  
json.Unmarshal(b, &conf)  
fmt.Println(conf)  
  
// 反序列未知结构的JSON  
var data map[string]interface{}  
  
json.Unmarshal(b, &data)  
```
# 3 流式处理

- 创建编码器，将数据直接写入 `io.Writer`（如 HTTP 响应或文件）。
    - **`json.NewEncoder(w io.Writer) *json.Encoder`**
-  将 Go 数据结构（如结构体、切片、映射等）​**序列化为 JSON 格式**，并直接写入关联的 `io.Writer`（如文件、HTTP 响应、网络连接等）。
    - func (enc \*Encoder) Encode(v any) error
    - 将 `v` 编码为 JSON 并写入 `enc` 关联的 `io.Writer`
- 创建解码器，从 `io.Reader`（如 HTTP 请求体或文件）读取并解析 JSON。
    - **`json.NewDecoder(r io.Reader) *json.Decoder`**
- `Decoder`类型的`Decode`方法用于从输入流中解析JSON数据并将其解码到指定的Go变量中。
    - func (dec \*Decoder) Decode(v any) error
    - `dec` 是一个指向`json.Decoder`的指针，该解码器关联了一个输入流（如文件、网络连接等）。
    - `v` 是目标变量的指针，用于存储解码后的数据。

```go
package main

import (
    "encoding/json"
    "net/http"
)

type User struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

func handleUser(w http.ResponseWriter, r *http.Request) {
    // 1. 创建解码器，绑定请求体（r.Body 是 io.Reader）
    decoder := json.NewDecoder(r.Body)
    defer r.Body.Close()

    // 2. 解码 JSON 数据到结构体
    var user User
    if err := decoder.Decode(&user); err != nil {
        http.Error(w, "Bad Request", http.StatusBadRequest)
        return
    }

    // 3. 处理业务逻辑（示例：返回欢迎消息）
    response := map[string]string{
        "message": "Hello, " + user.Name,
    }

    // 4. 设置响应头
    w.Header().Set("Content-Type", "application/json")

    // 5. 创建编码器，将响应写入 http.ResponseWriter（io.Writer）
    encoder := json.NewEncoder(w)
    if err := encoder.Encode(response); err != nil {
        http.Error(w, "Internal Server Error", http.StatusInternalServerError)
    }
}

func main() {
    http.HandleFunc("/user", handleUser)
    http.ListenAndServe(":8080", nil)
}
```

## 3.1 json.Decoder类型

用于从输入流（io.Reader）中解码JSON对象。适用于流式读取或处理大型JSON数据。
### 3.1.1 json.NewDecoder(r io.Reader) \*Decoder

**功能​**​：创建从输入流读取JSON的解码器  
​**​参数​**​：

- `r`：数据源（如`os.File`、`http.Request.Body`等）

​**​返回值​**​：

- `*Decoder`：JSON解码器指针

​**​注意事项​**​：

- 适用于流式JSON处理
- 比`Unmarshal`更节省内存
- 解码器会缓存数据，不要直接操作源Reader

```go
package main

import (
	"encoding/json"
	"fmt"
	"strings"
)

func main() {
	// 模拟来自网络的JSON流
	jsonStream := `{"name":"Alice"} {"name":"Bob"}`

	// 创建解码器
	decoder := json.NewDecoder(strings.NewReader(jsonStream))

	for {
		var user struct{ Name string }
		if err := decoder.Decode(&user); err != nil {
			fmt.Println("解码结束:", err) // io.EOF 表示流结束
			break
		}
		fmt.Printf("解码结果: %+v\n", user)
	}
}

/* 输出：
解码结果: {Name:Alice}
解码结果: {Name:Bob}
解码结束: EOF
*/

```
### 3.1.2 (dec \*Decoder) Buffered() io.Reader

**功能​**​：返回解码器缓冲区未读内容  
​**​返回值​**​：

- `io.Reader`：包含缓存数据的读取器

​**​注意事项​**​：

- 用于跨协议数据传输后读取剩余数据
- 需在`Decode()`后调用
- 读取后缓冲区会被清空

```go
func main() {
	jsonStream := `{"name":"Alice"}EXTRA DATA`
	decoder := json.NewDecoder(strings.NewReader(jsonStream))

	var user struct{ Name string }
	if err := decoder.Decode(&user); err != nil {
		fmt.Println("错误:", err)
		return
	}

	// 获取缓冲区剩余数据
	remaining := decoder.Buffered()
	extra, _ := io.ReadAll(remaining)
	
	fmt.Println("用户数据:", user.Name)
	fmt.Println("剩余数据:", string(extra))
}

/* 输出：
用户数据: Alice
剩余数据: EXTRA DATA
*/
```
### 3.1.3 (dec \*Decoder) Decode(v any) error

**功能​**​：解析当前JSON值到结构体  
​**​参数​**​：

- `v`：目标结构体指针

​**​返回值​**​：

- `error`：可能的错误：
    - `json.SyntaxError`：语法错误
    - `json.UnmarshalTypeError`：类型不匹配
    - `io.ErrUnexpectedEOF`：意外结束
    - 调用`DisallowUnknownFields`后出现未知字段

​**​注意事项​**​：

- 每次调用读取一个JSON值
- 流结束时返回`io.EOF`
- 需确保目标变量可修改（传递指针）

```go
func main() {
	jsonStream := `{"name":123} {"age":"should_be_number"}`
	decoder := json.NewDecoder(strings.NewReader(jsonStream))

	// 第一次尝试解码
	var user1 struct{ Name string }
	if err := decoder.Decode(&user1); err != nil {
		fmt.Printf("错误1: %T %v\n", err, err)
	}

	// 第二次尝试解码
	var user2 struct{ Age int }
	if err := decoder.Decode(&user2); err != nil {
		fmt.Printf("错误2: %T %v\n", err, err)
	}
}

/* 输出：
错误1: *json.UnmarshalTypeError json: cannot unmarshal number into Go struct field .Name of type string
错误2: *json.UnmarshalTypeError json: cannot unmarshal string into Go struct field .Age of type int
*/
```
### 3.1.4 (dec \*Decoder) DisallowUnknownFields()

**功能​**​：开启未知字段错误检查  
​**​注意事项​**​：

- 调用后遇到JSON中存在但目标结构没有的字段会报错
- 适用于严格模式解析
- 需在`Decode()`前调用

```go
func main() {
	jsonStream := `{"name":"Alice","email":"alice@example.com"}`
	decoder := json.NewDecoder(strings.NewReader(jsonStream))
	decoder.DisallowUnknownFields() // 开启严格模式

	var user struct {
		Name string `json:"name"`
	}
	
	err := decoder.Decode(&user)
	fmt.Println("错误:", err)
}

/* 输出：
错误: json: unknown field "email"
*/
```
### 3.1.5 (dec \*Decoder) InputOffset() int64

**功能​**​：返回当前解码位置的字节偏移量  
​**​返回值​**​：

- `int64`：自流开始的字节偏移量

​**​注意事项​**​：

- 用于错误定位
- 在`Decode()`或`Token()`之后调用
- 包含所有已读字节（包括空白）

```go
func main() {
	jsonStream := `  {"name": "Bob"}`
	decoder := json.NewDecoder(strings.NewReader(jsonStream))
	
	// 读取第一个token：{
	_, _ = decoder.Token()
	
	fmt.Println("当前位置:", decoder.InputOffset()) // 1个空格+{
}

/* 输出：
当前位置: 3
*/
```
### 3.1.6 (dec \*Decoder) More() bool

​**​功能​**​：检查是否还有更多元素（在数组/对象内）  
​**​返回值​**​：

- `bool`：存在更多元素时返回`true`

​**​注意事项​**​：

- 用于遍历数组或对象
- 在读取`[`或`{`后使用
- 在`[`/`]`或`{`/`}`之间返回`true`

```go
func main() {
	jsonStream := `["Go", "Python", "Rust"]`
	decoder := json.NewDecoder(strings.NewReader(jsonStream))

	// 读取开始标记 [
	decoder.Token()

	for decoder.More() {
		var lang string
		decoder.Decode(&lang)
		fmt.Println("语言:", lang)
	}

	// 读取结束标记 ]
	decoder.Token()
}

/* 输出：
语言: Go
语言: Python
语言: Rust
*/
```
### 3.1.7 (dec \*Decoder) Token() (Token, error)

**功能​**​：读取下一个JSON Token  
​**​返回值​**​：

- `Token`：可以是：
    - `json.Delim`：分隔符 `[`, `]`, `{`, `}`
    - `string`, `float64`, `bool`, `nil`
- `error`：解析错误或`io.EOF`

​**​注意事项​**​：

- 用于底层JSON解析
- Token需在正确的结构上下文中使用
- 数字默认返回`float64`，除非使用`UseNumber()`

```go
func main() {
	jsonStream := `{"name": "Charlie", "active": true}`
	decoder := json.NewDecoder(strings.NewReader(jsonStream))

	for {
		token, err := decoder.Token()
		if err != nil {
			break
		}

		switch t := token.(type) {
		case json.Delim:
			fmt.Printf("分隔符: %q\n", t)
		case string:
			fmt.Printf("字段名/值: %q\n", t)
		case bool:
			fmt.Printf("布尔值: %v\n", t)
		default:
			fmt.Printf("其他类型: %T\n", token)
		}
	}
}

/* 输出：
分隔符: '{'
字段名/值: "name"
字段名/值: "Charlie"
字段名/值: "active"
布尔值: true
分隔符: '}'
*/
```
### 3.1.8 (dec \*Decoder) UseNumber()

​**​功能​**​：将数字作为`json.Number`类型解析  
​**​注意事项​**​：

- 防止大整数丢失精度
- 需在首次`Token()`或`Decode()`前调用
- `json.Number`可转为`int64`/`float64`/`string`

```go
func main() {
	jsonStream := `{"id": 12345678901234567890}`
	decoder := json.NewDecoder(strings.NewReader(jsonStream))
	decoder.UseNumber() // 启用数字保护

	var data struct {
		ID json.Number `json:"id"`
	}

	decoder.Decode(&data)

	// 尝试转为int64（会失败）
	_, intErr := data.ID.Int64()
	
	// 转为字符串保持原始值
	str := data.ID.String()
	
	fmt.Println("整型转换错误:", intErr)
	fmt.Println("字符串表示:", str)
}

/* 输出：
整型转换错误: strconv.ParseInt: parsing "12345678901234567890": value out of range
字符串表示: 12345678901234567890
*/
```
## 3.2 json.Encoder类型

`json.Encoder` 是 Go 标准库中用于流式 JSON 编码的核心类型，特别适合将 Go 数据结构序列化为 JSON 并写入各种输出流。相比 `json.Marshal`，它更高效处理大型数据结构和连续输出。

### 3.2.1 func NewEncoder(w io.Writer) \*Encoder

​**​功能​**​：创建 JSON 编码器  
​**​参数​**​：

- `w io.Writer`：JSON 数据目标（文件、网络连接等）  
    ​**​返回值​**​：
- `*Encoder`：初始化好的编码器指针  
    ​**​注意事项​**​：
- 创建后应立即使用
- 编码器会缓存数据，写入完成后可能需要调用 `Flush()`（取决于底层 `Writer`）

```go
func main() {
    // 创建目标 writer（内存缓冲区）
    buf := new(bytes.Buffer)
    
    // 创建编码器
    enc := json.NewEncoder(buf)
    fmt.Printf("编码器创建: %T\n", enc)
}
/* 输出:
编码器创建: *json.Encoder
*/
```
### 3.2.2 func (enc \*Encoder) Encode(v any) error

​**​功能​**​：将 Go 值编码为 JSON 并写入  
​**​参数​**​：

- `v any`：需要序列化的 Go 值  
    ​**​返回值​**​：
- `error`：可能的错误：
    - `json.UnsupportedTypeError`：不支持的类型
    - `json.UnsupportedValueError`：不支持的值
    - `json.MarshalerError`：自定义 `MarshalJSON` 方法错误
    - `io` 包相关错误（写入失败）

​**​注意事项​**​：

- 每次调用写入一个完整的 JSON 值
- 默认会添加换行符（可用 `SetIndent` 控制）
- 对通道、函数等不支持类型返回错误

```go
func main() {
    type Product struct {
        ID    int
        Name  string
        Price float64
    }
    
    buf := new(bytes.Buffer)
    enc := json.NewEncoder(buf)
    
    // 成功编码
    p1 := Product{101, "Laptop", 1299.99}
    if err := enc.Encode(p1); err != nil {
        fmt.Println("错误:", err)
    }
    
    // 尝试编码通道（不支持类型）
    ch := make(chan int)
    if err := enc.Encode(ch); err != nil {
        fmt.Printf("错误类型: %T\n值: %v\n", err, err)
    }
    
    fmt.Println("输出结果:")
    fmt.Println(buf.String())
}
/* 输出:
错误类型: *json.UnsupportedTypeError
值: json: unsupported type: chan int

输出结果:
{"ID":101,"Name":"Laptop","Price":1299.99}
*/
```
### 3.2.3 func (enc \*Encoder) SetEscapeHTML(on bool)

​**​功能​**​：控制是否转义 HTML 字符  
​**​参数​**​：

- `on bool`：`true` 开启转义（默认），`false` 关闭  
    ​**​注意事项​**​：
- 转义字符：`<`, `>`, `&` → `\u003c`, `\u003e`, `\u0026`
- 防止 JSON 被错误解释为 HTML
- 在输出 HTML 内联 JSON 时建议开启

```go
func main() {
    data := map[string]string{
        "html": "<div>Hello</div>",
        "script": "<script>alert('test')</script>",
    }
    
    buf := new(bytes.Buffer)
    enc := json.NewEncoder(buf)
    
    // 默认转义
    fmt.Println("--- 默认开启转义 ---")
    enc.Encode(data)
    fmt.Println(buf.String())
    
    buf.Reset()
    fmt.Println("\n--- 关闭转义 ---")
    enc.SetEscapeHTML(false) // 关闭转义
    enc.Encode(data)
    fmt.Println(buf.String())
}
/* 输出:
--- 默认开启转义 ---
{"html":"\u003cdiv\u003eHello\u003c/div\u003e","script":"\u003cscript\u003ealert('test')\u003c/script\u003e"}

--- 关闭转义 ---
{"html":"<div>Hello</div>","script":"<script>alert('test')</script>"}
*/
```
### 3.2.4 func (enc \*Encoder) SetIndent(prefix, indent string)

​**​功能​**​：设置 JSON 输出缩进格式  
​**​参数​**​：

- `prefix string`：每行前缀
- `indent string`：每级缩进字符串  
    ​**​注意事项​**​：
- 通常在首次 `Encode()` 前调用
- 会显著增加输出大小
- 使用空格而非制表符确保跨平台一致性

```go
func main() {
    type Employee struct {
        ID        int
        Name      string
        Positions []string
    }
    
    emp := Employee{
        ID:   2023,
        Name: "Alice Smith",
        Positions: []string{"Developer", "Team Lead"},
    }
    
    buf := new(bytes.Buffer)
    enc := json.NewEncoder(buf)
    
    // 无缩进
    fmt.Println("--- 无缩进 ---")
    enc.Encode(emp)
    fmt.Println(buf.String())
    
    buf.Reset()
    fmt.Println("\n--- 带缩进 ---")
    enc.SetIndent("", "  ") // 2空格缩进
    enc.Encode(emp)
    fmt.Println(buf.String())
    
    buf.Reset()
    fmt.Println("\n--- 带前缀和缩进 ---")
    enc.SetIndent(">>", "  ")
    enc.Encode(emp)
    fmt.Println(buf.String())
}
/* 输出:
--- 无缩进 ---
{"ID":2023,"Name":"Alice Smith","Positions":["Developer","Team Lead"]}

--- 带缩进 ---
{
  "ID": 2023,
  "Name": "Alice Smith",
  "Positions": [
    "Developer",
    "Team Lead"
  ]
}

--- 带前缀和缩进 ---
>>{
>>  "ID": 2023,
>>  "Name": "Alice Smith",
>>  "Positions": [
>>    "Developer",
>>    "Team Lead"
>>  ]
>>}
*/
```
# 4 判断字节切片是否为有效JSON

- **`json.Valid(data []byte) bool`**

```go
isValid := json.Valid([]byte(`{"name": "Alice"}`)) // true
```
# 5 结构体标签

| 标签选项                | 说明                 |
| ------------------- | ------------------ |
| `json:"-"`          | 忽略该字段              |
| `json:"name"`       | 指定 JSON 字段名        |
| `json:",omitempty"` | 字段为空值时忽略           |
| `json:",inline"`    | 嵌套结构体的字段平铺到父级 JSON |
# 6 分隔符
## 6.1 json.Delim类型

```go
type Delim rune
```

该类型用于表示JSON的分隔符，即方括号`[`、`]`和花括号`{`、`}`。其底层是一个 `rune` 类型值。在 `json.Decoder` 的 `Token()` 方法中，当遇到 JSON 结构分隔符时会返回该类型值。
### 6.1.1 func (d Delim) String() string

**功能​**​：将 JSON 分隔符转换为可读的字符串表示  
​**​接收器​**​：

- `d Delim`：要转换的 JSON 分隔符

​**​返回值​**​：

- `string`：分隔符的字符串表示
    - `{` → `"{"`
    - `}` → `"}"`
    - `[` → `"["`
    - `]` → `"]"`

**注意事项​**​：

- 提供人眼可读的分隔符表示
- 输出包含引号，便于在日志或调试信息中识别
- 与直接类型转换相比更易读

```go
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"strings"
)

func main() {
	// 创建包含各种 JSON 结构的示例数据
	const jsonData = `{
		"user": {
			"id": 101,
			"name": "Alice",
			"tags": ["admin", "dev"],
			"projects": [
				{"name": "ProjectA", "status": "active"},
				{"name": "ProjectB", "status": "pending"}
			]
		}
	}`

	// 创建 JSON 解码器
	dec := json.NewDecoder(strings.NewReader(jsonData))
	
	// 跟踪当前解析深度
	depth := 0
	
	fmt.Println("开始解析 JSON 数据结构:")
	fmt.Println("------------------------")
	
	// 循环处理所有 token
	for {
		token, err := dec.Token()
		if err == io.EOF {
			break
		}
		if err != nil {
			panic(err)
		}
		
		// 检查是否为分隔符
		if delim, isDelim := token.(json.Delim); isDelim {
			// 根据分隔符类型更新深度并打印信息
			switch delim {
			case '{', '[':
				depth++
				printIndented(depth, fmt.Sprintf("开始对象/数组: %s", delim.String()))
			case '}', ']':
				printIndented(depth, fmt.Sprintf("结束对象/数组: %s", delim.String()))
				depth--
			}
			continue
		}
		
		// 对于非分隔符 tokens
		printIndented(depth, fmt.Sprintf("值: %v (%T)", token, token))
	}
	
	fmt.Println("------------------------")
	fmt.Println("JSON 解析完成")
}

// 辅助函数：缩进打印
func printIndented(depth int, msg string) {
	indent := strings.Repeat("  ", depth)
	fmt.Printf("%s%d> %s\n", indent, depth, msg)
}
```
# 7 特殊处理

## 7.1 json.Number 类型

`json.Number` 是一个表示 JSON 数字的字符串类型，用于避免大整数或高精度小数在解码时的精度损失。

### 7.1.1 func (n Number) Float64() (float64, error)

​**​功能​**​：将 JSON 数字转换为 `float64`  
​**​返回值​**​：

- `float64`：转换后的浮点数
- `error`：可能的错误：
    - `strconv.ErrSyntax`：无法解析为数字
    - `strconv.ErrRange`：超出 `float64` 范围

### 7.1.2 func (n Number) Int64() (int64, error)

​**​功能​**​：将 JSON 数字转换为 `int64`  
​**​返回值​**​：

- `int64`：转换后的整数
- `error`：可能的错误：
    - `strconv.ErrSyntax`：非整数格式
    - `strconv.ErrRange`：超出 `int64` 范围

### 7.1.3 func (n Number) String() string

​**​功能​**​：返回 JSON 数字的原始字符串表示  
​**​返回值​**​：

- `string`：原始 JSON 数字（未解析）

## 7.2 使用场景：

- 处理可能超出 `int64` 范围的大整数
- 避免高精度小数的浮点转换误差
- 需要数字原始格式的场景

```go
package main

import (
	"encoding/json"
	"fmt"
	"log"
)

func main() {
	// JSON 包含大整数和高精度小数
	jsonStr := `[
		{"id": 12345678901234567890, "pi": 3.14159265358979323846},
		{"id": "98765432109876543210", "pi": 9.8765432109876543210}
	]`
	
	// 使用 json.Number 解码
	var data []struct {
		ID json.Number `json:"id"`
		Pi json.Number `json:"pi"`
	}
	
	if err := json.Unmarshal([]byte(jsonStr), &data); err != nil {
		log.Fatal(err)
	}
	
	for i, item := range data {
		fmt.Printf("\n项目 %d:\n", i+1)
		
		// 获取原始字符串表示
		fmt.Printf("  原始ID: %s\n", item.ID.String())
		fmt.Printf("  原始Pi: %s\n", item.Pi.String())
		
		// 尝试转换为 int64
		idInt, err := item.ID.Int64()
		if err != nil {
			fmt.Printf("  ID转为int64错误: %v\n", err)
		} else {
			fmt.Printf("  ID为int64: %d\n", idInt)
		}
		
		// 尝试转换为 float64
		piFloat, err := item.Pi.Float64()
		if err != nil {
			fmt.Printf("  Pi转为float64错误: %v\n", err)
		} else {
			fmt.Printf("  Pi为float64: %.10f\n", piFloat)
		}
		
		// 直接转换为字符串进行计算
		idStr := item.ID.String()
		fmt.Printf("  ID最后两位: %s\n", idStr[len(idStr)-2:])
	}
}

/*
项目 1:
  原始ID: 12345678901234567890
  原始Pi: 3.14159265358979323846
  ID转为int64错误: strconv.ParseInt: parsing "12345678901234567890": value out of range
  Pi为float64: 3.1415926536
  ID最后两位: 90

项目 2:
  原始ID: 98765432109876543210
  原始Pi: 9.8765432109876543210
  ID转为int64错误: strconv.ParseInt: parsing "98765432109876543210": value out of range
  Pi为float64: 9.8765432110
  ID最后两位: 10
*/
```
### 7.2.1 json.RawMessage 类型

`json.RawMessage` 是原始的、未解码的 JSON 字节片段，允许延迟解码或传递原始 JSON。
### 7.2.2 func (m RawMessage) MarshalJSON() (\[\]byte, error)

​**​功能​**​：将 `RawMessage` 作为 JSON 数据直接返回  
​**​返回值​**​：

- `[]byte`：原始消息字节
- `error`：永不返回错误

### 7.2.3 func (m \*RawMessage) UnmarshalJSON(data \[\]byte) error

​**​功能​**​：将原始 JSON 数据存储到 `RawMessage` 中  
​**​参数​**​：

- `data []byte`：要存储的原始 JSON  
    ​**​返回值​**​：
- `error`：永不返回错误

# 8 使用场景：

- 解组时保留部分 JSON 用于后续处理
- 构建需要合并多个 JSON 的结构
- 实现灵活的 JSON 处理管道

```go
package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	// 包含动态内容的 JSON
	jsonStr := `{
		"id": 101,
		"meta": {
			"source": "api-v3",
			"timestamp": "2023-05-15T10:30:00Z",
			"signature": "abc123"
		},
		"data": {
			"type": "user",
			"attributes": {
				"name": "Alice",
				"roles": ["admin", "editor"]
			}
		}
	}`
	
	// 只解析元数据，数据保留原始格式
	type Response struct {
		ID    int             `json:"id"`
		Meta  json.RawMessage `json:"meta"`
		Data  json.RawMessage `json:"data"`
	}
	
	var resp Response
	if err := json.Unmarshal([]byte(jsonStr), &resp); err != nil {
		fmt.Println("解析错误:", err)
		return
	}
	
	fmt.Printf("响应 ID: %d\n", resp.ID)
	
	// 处理元数据
	type Metadata struct {
		Source    string `json:"source"`
		Timestamp string `json:"timestamp"`
	}
	
	var meta Metadata
	if err := json.Unmarshal(resp.Meta, &meta); err != nil {
		fmt.Println("元数据解析错误:", err)
	} else {
		fmt.Printf("元数据: Source=%s, Timestamp=%s\n", meta.Source, meta.Timestamp)
	}
	
	// 根据类型动态处理数据
	typeHeader := struct {
		Type string `json:"type"`
	}{}
	
	if err := json.Unmarshal(resp.Data, &typeHeader); err == nil {
		switch typeHeader.Type {
		case "user":
			fmt.Println("\n处理用户数据:")
			var userData struct {
				Attributes struct {
					Name  string   `json:"name"`
					Roles []string `json:"roles"`
				} `json:"attributes"`
			}
			if err := json.Unmarshal(resp.Data, &userData); err == nil {
				fmt.Printf("用户名: %s\n角色: %v\n", userData.Attributes.Name, userData.Attributes.Roles)
			}
		case "product":
			fmt.Println("\n处理产品数据")
		default:
			fmt.Println("\n未知数据类型:", typeHeader.Type)
		}
	}
	
	// 输出原始数据
	fmt.Printf("\n原始数据字段:\n%s\n", resp.Data)
	
	// 重新序列化整个响应
	resp.ID = 102 // 修改ID
	newJSON, _ := json.MarshalIndent(resp, "", "  ")
	fmt.Printf("\n修改后的响应:\n%s\n", newJSON)
}

/*
响应 ID: 101
元数据: Source=api-v3, Timestamp=2023-05-15T10:30:00Z

处理用户数据:
用户名: Alice
角色: [admin editor]

原始数据字段:
{
			"type": "user",
			"attributes": {
				"name": "Alice",
				"roles": ["admin", "editor"]
			}
		}

修改后的响应:
{
  "id": 102,
  "meta": {
    "source": "api-v3",
    "timestamp": "2023-05-15T10:30:00Z",
    "signature": "abc123"
  },
  "data": {
    "type": "user",
    "attributes": {
      "name": "Alice",
      "roles": [
        "admin",
        "editor"
      ]
    }
  }
}
*/
```
# 9 json.Token 类型

`json.Token` 是一个表示 JSON 解析过程中令牌的空接口，具体类型包括：

- `json.Delim`：分隔符 `{`, `}`, `[`, `]`
- `string`：字符串值
- `float64`：数字值
- `bool`：布尔值
- `nil`：null 值

**使用场景**：

- 实现自定义的 JSON 解析器
- 提取特定部分而不解析整个结构
- 处理非结构化 JSON 数据

```go
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"strings"
)

func main() {
	// 示例 JSON 数据
	jsonData := `{
		"name": "Advanced JSON Processor",
		"version": 2.1,
		"stable": true,
		"features": [
			"stream_processing",
			{"name": "custom_parsing", "enabled": true},
			null,
			"error_handling"
		],
		"config": null
	}`

	// 创建解码器
	dec := json.NewDecoder(strings.NewReader(jsonData))
	
	// 用于统计的计数器
	var (
		depth            int
		objectCount      int
		arrayCount       int
		stringCount      int
		numberCount      int
		boolCount        int
		nullCount        int
		maxDepth         int
		currentObjectKey string
	)
	
	fmt.Println("开始解析 JSON 结构...")
	fmt.Println("-------------------------------")
	
	for {
		// 获取下一个令牌
		token, err := dec.Token()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal("解析错误:", err)
		}
		
		// 更新最大深度
		if depth > maxDepth {
			maxDepth = depth
		}
		
		// 处理分隔符
		if delim, ok := token.(json.Delim); ok {
			switch delim {
			case '{':
				objectCount++
				depth++
				fmt.Printf("%s开始对象 (depth %d)\n", indent(depth), depth)
			case '}':
				depth--
				fmt.Printf("%s结束对象\n", indent(depth+1))
			case '[':
				arrayCount++
				depth++
				fmt.Printf("%s开始数组 (depth %d)\n", indent(depth), depth)
			case ']':
				depth--
				fmt.Printf("%s结束数组\n", indent(depth+1))
			}
			continue
		}
		
		// 处理值类型
		switch v := token.(type) {
		case string:
			// 在对象中，字符串可能是键也可能是值
			if depth > 0 && dec.InputOffset() > 0 {
				if currentObjectKey == "" {
					// 当前字符串是一个键
					currentObjectKey = v
					fmt.Printf("%s键: %s\n", indent(depth+1), v)
				} else {
					// 当前字符串是一个值
					stringCount++
					fmt.Printf("%s值: %q (类型: string)\n", indent(depth+1), v)
					currentObjectKey = ""
				}
			} else {
				stringCount++
				fmt.Printf("%s字符串: %q (类型: string)\n", indent(depth), v)
			}
			
		case float64:
			numberCount++
			fmt.Printf("%s数字: %v (类型: float64)\n", indent(depth+1), v)
			
		case bool:
			boolCount++
			fmt.Printf("%s布尔: %v (类型: bool)\n", indent(depth+1), v)
			
		case nil:
			nullCount++
			fmt.Printf("%snull 值\n", indent(depth+1))
		}
	}
	
	fmt.Println("-------------------------------")
	fmt.Println("JSON 结构统计:")
	fmt.Printf("最大深度: %d\n", maxDepth)
	fmt.Printf("对象数: %d\n", objectCount)
	fmt.Printf("数组数: %d\n", arrayCount)
	fmt.Printf("字符串数: %d\n", stringCount)
	fmt.Printf("数字数: %d\n", numberCount)
	fmt.Printf("布尔值数: %d\n", boolCount)
	fmt.Printf("null 值数: %d\n", nullCount)
}

// 辅助函数：生成缩进
func indent(depth int) string {
	return strings.Repeat("  ", depth)
}

/*
开始解析 JSON 结构...
-------------------------------
  开始对象 (depth 1)
    键: name
    值: "Advanced JSON Processor" (类型: string)
    键: version
    数字: 2.1 (类型: float64)
    键: stable
    布尔: true (类型: bool)
    键: features
    开始数组 (depth 2)
      字符串: "stream_processing" (类型: string)
      开始对象 (depth 3)
        键: name
        值: "custom_parsing" (类型: string)
        键: enabled
        布尔: true (类型: bool)
      结束对象
      null 值
      字符串: "error_handling" (类型: string)
    结束数组
    键: config
    null 值
  结束对象
-------------------------------
JSON 结构统计:
最大深度: 3
对象数: 2
数组数: 1
字符串数: 4
数字数: 1
布尔值数: 2
null 值数: 2
*/
```
# 10 自定义序列化/反序列化

在 Go 的 `encoding/json` 包中，`Marshaler` 和 `Unmarshaler` 接口提供了强大的扩展机制，允许开发者完全控制自定义类型的 JSON 序列化和反序列化行为。

## 10.1 json.Marshaler 接口

```go
type Marshaler interface {
    MarshalJSON() ([]byte, error)
}
```

**功能​**​：允许类型自定义其 JSON 编码表示  
​**​注意事项​**​：

- 实现此接口后，`json.Marshal/Encode` 会优先调用此方法
- 返回的 `[]byte` 必须是有效 JSON
- 错误处理需明确具体错误类型
- 优先级高于 `TextMarshaler`
## 10.2 json.Unmarshaler 接口

```go
type Unmarshaler interface {
    UnmarshalJSON([]byte) error
}
```

**功能​**​：允许类型自定义其 JSON 解码行为  
​**​注意事项​**​：

- 实现此接口后，`json.Unmarshal/Decode` 会优先调用此方法
- 传入的是原始 JSON 字节切片
- 需要完全处理解码逻辑（包括嵌套结构）
- 优先级高于 `TextUnmarshaler`
- 使用的是必定是指针类型接受者

```go
package main

import (
	"encoding/json"
	"fmt"
	"time"
)

// 自定义时间类型
type CustomTime struct {
	time.Time
}

// 实现 Marshaler 接口
func (ct CustomTime) MarshalJSON() ([]byte, error) {
	// 使用自定义时间格式
	formatted := ct.Format("2006-01-02 15:04:05")
	return json.Marshal(formatted) // 序列化为JSON字符串
}

// 实现 Unmarshaler 接口
func (ct *CustomTime) UnmarshalJSON(data []byte) error {
	var timeStr string
	if err := json.Unmarshal(data, &timeStr); err != nil {
		return err
	}
	
	// 使用当前时间作为默认值（对空时间特殊处理）
	if timeStr == "" {
		ct.Time = time.Now()
		return nil
	}
	
	// 解析自定义时间格式
	t, err := time.Parse("2006-01-02 15:04:05", timeStr)
	if err != nil {
		return fmt.Errorf("无效的时间格式: %w", err)
	}
	
	ct.Time = t
	return nil
}

func main() {
	// 测试数据
	type Event struct {
		Name string     `json:"name"`
		Time CustomTime `json:"time"`
	}
	
	// 序列化测试
	now := CustomTime{time.Date(2023, 5, 15, 14, 30, 0, 0, time.UTC)}
	event := Event{"Conference Call", now}
	
	jsonData, _ := json.Marshal(event)
	fmt.Println("序列化结果:", string(jsonData))
	
	// 反序列化测试（含错误时间格式）
	jsonStr := `{"name":"Team Meeting","time":"invalid_time"}`
	var newEvent Event
	err := json.Unmarshal([]byte(jsonStr), &newEvent)
	
	if err != nil {
		fmt.Printf("\n反序列化错误: %T %v\n", err, err)
	} else {
		fmt.Printf("\n解析成功: %s at %s\n", 
			newEvent.Name, 
			newEvent.Time.Format(time.RFC1123))
	}
	
	// 测试空时间处理
	emptyTimeJSON := `{"name":"Test","time":""}`
	var emptyEvent Event
	if err := json.Unmarshal([]byte(emptyTimeJSON), &emptyEvent); err == nil {
		fmt.Printf("\n空时间处理: %s (现在时间)\n", emptyEvent.Time.Format(time.Kitchen))
	}
}

/*
序列化结果: {"name":"Conference Call","time":"2023-05-15 14:30:00"}

反序列化错误: *fmt.wrapError 无效的时间格式: parsing time "invalid_time" as "2006-01-02 15:04:05": cannot parse "invalid_time" as "2006"

空时间处理: 06:04PM (现在时间) // 实际输出取决于运行时间
*/
```
# 11 接口反序列化

- 问题：当想从json文件中反序列化到带有接口类型字段的结构体时，会出现不知道该字段接口底层具体的数据类型
- 解决：核心思路就是创建一个具有具体类型的 `temp` 结构体，反序列化到该结构体后再赋值给原结构体

```go
package main  
  
import (  
    "encoding/json"  
    "fmt"    "io"    "os")  
  
type Value interface {  
    Len() int  
}  
  
type Test struct {  
    Key     string `json:"key"`  
    Content Value  `json:"value"`  
}  
  
type ByteView struct {  
    b []byte `json:"b"`  
}  
  
func (b ByteView) Len() int {  
    return len(b.b)  
}  
  
func (b ByteView) MarshalJSON() ([]byte, error) {  
    return json.Marshal(struct {  
       B string `json:"b"`  
    }{B: string(b.b)})  
}  
  
func (b *ByteView) UnmarshalJSON(data []byte) error {  
    b.b = data  
    return nil  
}  
  
func (b ByteView) String() string {  
    return string(b.b)  
}  
  
func (t *Test) UnmarshalJSON(data []byte) error {  
    var temp struct {  
       Key     string   `json:"key"`  
       Content ByteView `json:"value"`  
    }  
  
    if err := json.Unmarshal(data, &temp); err != nil {  
       return err  
    }  
  
    t.Key = temp.Key  
    t.Content = temp.Content  
  
    return nil  
}  
  
func main() {  
    //t := Test{  
    // Key: "s",    // Content:   ByteView{b: []byte("hello")},    //}    //    //t1 := Test{}    //    //f, _ := os.OpenFile("t.json", os.O_RDWR|os.O_CREATE, os.ModePerm)    //defer f.Close()    //    //jb, _ := json.MarshalIndent(t, "", "\t")    //fmt.Println(string(jb))    //    //json.Unmarshal(jb, &t)    //fmt.Printf("%#v\n", t) // 直接反序列化不会出问题  
    //  
    //enc := json.NewEncoder(f)    //enc.SetIndent("", "\t")    //enc.Encode(t)    //    //f.Seek(0, io.SeekStart)    //    //dec := json.NewDecoder(f)    //dec.Decode(&t1)    //fmt.Printf("%+v\n", t1) // 从文件中反序列化会出现不知道接口具体类型的问题  
  
    f, _ := os.OpenFile("t.json", os.O_RDWR, os.ModePerm)  
    defer f.Close()  
  
    t := Test{  
       Key:     "t",  
       Content: ByteView{b: []byte("helo")},  
    }  
  
    enc := json.NewEncoder(f)  
    enc.Encode(t)  
  
    var td Test  
    f.Seek(0, io.SeekStart)  
    dec := json.NewDecoder(f)  
    err := dec.Decode(&td)  
    if err != nil {  
       fmt.Println(err) // json: cannot unmarshal string into Go struct field .value of type main.ByteView  
    }  
  
    fmt.Printf("td :: %+v", td) // td :: {Key:t Content:{"b":"helo"}}  
}
```