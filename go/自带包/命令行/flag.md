# flag

Package flag 实现命令行标志解析。

flag包允许使用以下格式

```
-flag
--flag   // double dashes are also permitted
-flag=x
-flag x  // non-boolean flags only
```

## 1 变量

```go
var ErrHelp = errors.New("flag: help requested")
```

ErrHelp 是调用 -help 或 -h 标志但未定义此类标志时返回的错误。

```go
var Usage = func() {
	fmt.Fprintf(CommandLine.Output(), "Usage of %s:\n", os.Args[0])
	PrintDefaults()
}
```

默认的帮助信息生成函数，可被覆盖。

## 2 定义命令行参数

**类型函数​**​：根据参数类型选择对应函数，返回对应类型的指针。

```go
port := flag.Int("port", 8080, "端口号")          // 整数类型
debug := flag.Bool("debug", false, "启用调试模式") // 布尔类型
name := flag.String("name", "guest", "用户名")     // 字符串类型

// 调用`flag.Parse()`解析`os.Args`中的参数，必须在所有参数定义后调用。
flag.Parse()


// 通过解引用指针获取已解析的值：
fmt.Printf("Port: %d\n", *port)
fmt.Printf("Debug: %t\n", *debug)
fmt.Printf("Name: %s\n", *name)

// 可以将标志值绑定一个变量p
IntVar(p *int, name string, value int, usage string)
```

| ​**​类型​**​             | ​**​定义函数​**​      | ​**​示例命令行参数​**​ | ​**​默认值处理​**​                    |
| ---------------------- | ----------------- | --------------- | -------------------------------- |
| 整数 (`int`)             | `flag.Int()`      | `--port=8080`   | 缺省使用默认值，类型错误报错。                  |
| 布尔 (`bool`)            | `flag.Bool()`     | `--debug`（无需等号） | `--debug`设置为`true`，无参数默认`false`。 |
| 字符串 (`string`)         | `flag.String()`   | `--name=John`   | 缺省使用默认值。                         |
| 浮点数 (`float64`)        | `flag.Float64()`  | `--ratio=0.8`   | 缺省使用默认值，类型错误报错。                  |
| 持续时间 (`time.Duration`) | `flag.Duration()` | `--timeout=5s`  | 支持`300ms`、`1h`等格式。               |
| 自定义类型                  | `flag.Var()`      | 根据自定义解析逻辑定      | 需实现`flag.Value`接口。               |
| **布尔参数特殊处理​**​：        |                   |                 |                                  |

* 不需要显式赋值，存在即为`true`。\
  示例：`./app --debug` → `debug=true`\
  若需显式禁用，使用`--debug=false`。

## 3 Arg(i int) string

* Arg 返回第 i 个命令行参数。Arg（0） 是处理完标志后剩下的第一个参数。如果请求的元素不存在，则 Arg 返回空字符串。

```go
  
func main() {  
    p := flag.Int("num", 100, "数字测试")  
  
    flag.Parse()  
    fmt.Println(*p)  
    fmt.Println(flag.Arg(0))   // 必须在Parse之后使用
    fmt.Println(flag.Args())   // 返回列表
    fmt.Println(flag.NArg())   // NArg 是处理标志后剩余的参数数。
    fmt.Println(flag.NFlag())  // 返回已设置的命令行标志数量。
}

```

## 4 \*\* `Parse()`​\*\*​

* ​**​作用​**​：解析命令行参数（`os.Args[1:]`）。
* ​**​使用时机​**​：在所有 `flag` 定义后调用。
*   ​**​示例​**​：

    ```go
    flag.Parse() // 必须调用以触发参数解析
    ```

## 5 ​**​ `Parsed() bool`​**​

* ​**​作用​**​：检查是否已解析命令行参数。
* ​**​场景​**​：验证参数解析状态。
*   ​**​示例​**​：

    ```go
    if !flag.Parsed() {
        flag.Parse()
    }
    ```

## 6 **`Visit(fn func(*Flag))`​**​

* ​**​作用​**​：遍历所有已设置的命令行标志。
* ​**​场景​**​：生成自定义帮助信息或校验输入。
*   ​**​示例​**​：

    ```go
    flag.Visit(func(f *flag.Flag) {
        fmt.Printf("Flag: %s, Value: %v\n", f.Name, f.Value)
    })

    flag.VisitAll(func(f *flag.Flag) {  // 遍历所有定义的标志（无论是否设置）。
    fmt.Printf("%s: %s\n", f.Name, f.Usage) 
    ```

})\
\`\`\`

## 7 **`Set(name, value string) error`​**​

* ​**​作用​**​：动态设置某个标志的值。
* ​**​场景​**​：覆盖默认值或在测试中模拟输入。
*   ​**​示例​**​：

    ```go
    flag.Set("port", "9090") // 强制设置 --port=9090
    ```

## 8 FlagSet

`flag` 包中，`FlagSet` 类型用于创建 ​**​独立的命令行参数集合​**​，支持子命令、多组参数隔离和定制化解析。

### 8.1 定义FlagSet

```go
// 语法
func NewFlagSet(name string, errorHandling ErrorHandling) *FlagSet

// 示例：创建子命令 "server" 的参数集
serverCmd := flag.NewFlagSet("server", flag.ExitOnError)
```

* ​**​参数说明​**​：
  * `name`：FlagSet 名称（用于帮助信息）。
  * `errorHandling`：错误处理模式，可选：
    * `flag.ContinueOnError`：解析错误后继续执行，返回错误。
    * `flag.ExitOnError`：遇到错误时调用 `os.Exit(2)`（默认行为）。
    * `flag.PanicOnError`：解析错误时触发 `panic`。

### 8.2 定义标志

定义标志方法与全局flag包类似。

手动指定要解析的参数列表（如 `os.Args` 的子切片）：

```go
// 假设命令行输入：./app server --port=9090 --debug
serverCmd.Parse(os.Args[2:]) // 解析从第三个参数开始的部分
```
