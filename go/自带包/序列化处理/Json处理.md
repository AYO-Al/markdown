
`encoding/json`为官方自带JSON处理包。

## 1.1 序列化

- 将 Go 结构体、map 或基本类型序列化为 JSON 字节切片。
-  **`json.Marshal(v interface{}) ([]byte, error)`**

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
## 1.2 反序列化

- 将 JSON 数据解析到 Go 结构体或 map 中。
- **`json.Unmarshal(data []byte, v interface{}) error`**
    - v必须是指针类型

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
## 1.3 流式处理

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

## 1.4 判断字节切片是否为有效JSON

- **`json.Valid(data []byte) bool`**

```go
isValid := json.Valid([]byte(`{"name": "Alice"}`)) // true
```
## 1.5 结构体标签

| 标签选项                | 说明                 |
| ------------------- | ------------------ |
| `json:"-"`          | 忽略该字段              |
| `json:"name"`       | 指定 JSON 字段名        |
| `json:",omitempty"` | 字段为零值时忽略           |
| `json:",inline"`    | 嵌套结构体的字段平铺到父级 JSON |
