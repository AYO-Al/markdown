`bufio`包提供了带缓冲的I/O操作，通过减少系统调用次数来提升读写效率。
# 1 常量

```go
const (
	// MaxScanTokenSize is the maximum size used to buffer a token
	// unless the user provides an explicit buffer with [Scanner.Buffer].
	// The actual maximum token size may be smaller as the buffer
	// may need to include, for instance, a newline.
	MaxScanTokenSize = 64 * 1024
)
```

`bufio` 包中的 `MaxScanTokenSize` 常量定义了在用户未显式指定缓冲区时，`Scanner` 类型用于缓冲单个 token 的默认最大容量（64KB）。

- **核心作用**

1. ​**​默认缓冲区限制​**​：
    
    - 当使用 `bufio.NewScanner` 创建扫描器且未调用 `Buffer` 方法时，`Scanner` 内部使用 `MaxScanTokenSize`（64KB）作为缓冲区容量的上限。
    - ​**​Token​**​：指通过 `Split` 函数（如 `ScanLines`）分割出的数据块（如一行文本、一个单词）。
2. ​**​隐式分割限制​**​：
    
    - 若某次扫描的 token ​**​超过缓冲区容量​**​，`Scanner` 会返回 `bufio.ErrTooLong` 错误。
    - ​**​实际容量更小​**​：因缓冲区需预留空间存储分隔符（如换行符 `\n`），实际可存储的 token 数据略小于 64KB。
# 2 函数

## 2.1 ScanBytes：按字节分割​​

- **​功能​**​：将每个字节作为独立的token返回。  
- **​适用场景​**​：需要逐字节处理二进制数据或字符流。  
- **​行为​**​：

    - 每次返回一个字节（`len(token) == 1`）。
    - 不会返回空token（除非输入数据本身为空）。

​**​示例​**​：

```go
scanner := bufio.NewScanner(strings.NewReader("Hello")) scanner.Split(bufio.ScanBytes) 
for scanner.Scan() { 
    fmt.Printf("%q ", scanner.Bytes()) // 输出 'H' 'e' 'l' 'l' 'o' 
    }
```
## 2.2 ​ScanLines：按行分割​​

- **​功能​**​：返回每行文本（去除行尾的`\r\n`或`\n`）。  
- **​适用场景​**​：处理文本文件、日志或网络协议中的行数据。  
- **​行为​**​：

    - 支持`\r\n`（Windows）和`\n`（Unix）换行符。
    - 允许空行（返回空字符串`""`）。
    - 文件末尾的非空行即使无换行符也会返回。

​**​示例​**​：

```go
input := "Line1\nLine2\r\nLine3" 
scanner := bufio.NewScanner(strings.NewReader(input)) scanner.Split(bufio.ScanLines) 
for scanner.Scan() { 
    fmt.Println(scanner.Text()) // 输出 Line1, Line2, Line3 
    }
```
## 2.3 ​ScanRunes：按UTF-8字符分割​​

- **​功能​**​：将每个UTF-8编码的字符（rune）作为token返回。  
- **​适用场景​**​：处理多语言文本或需要逐个字符分析的场景。  
- **​行为​**​：

    - 错误的UTF-8编码会被替换为`U+FFFD`（Unicode替换字符）。
    - 等效于遍历字符串的`for range`循环。

​**​示例​**​：

```go
scanner := bufio.NewScanner(strings.NewReader("Go语言")) scanner.Split(bufio.ScanRunes) 
for scanner.Scan() {
    fmt.Printf("%q ", scanner.Text()) // 输出 'G' 'o' '语' '言' 
    }
```

---

## 2.4 ​ScanWords：按单词分割​​

- **​功能​**​：返回被空格分隔的单词（去除前后空格）。  
- **​适用场景​**​：解析空格分隔的数据（如CSV的简化版、文本统计）。  
- **​行为​**​：

    - 使用`unicode.IsSpace`判断空格（包括`\t`、`\n`、`\v`等）。
    - 不会返回空字符串。

​**​示例​**​：

```go
input := "  Hello  世界\t!\n" 
scanner := bufio.NewScanner(strings.NewReader(input)) scanner.Split(bufio.ScanWords) 
for scanner.Scan() { 
    fmt.Println(scanner.Text()) // 输出 "Hello", "世界", "!" 
    }
```

## 2.5 函数​对比与选择指南​​

| ​**​函数​**​  | ​**​分割单位​**​ | ​**​空token​**​ | ​**​典型场景​**​ |
| ----------- | ------------ | -------------- | ------------ |
| `ScanBytes` | 单个字节         | 无              | 二进制处理、字符级分析  |
| `ScanLines` | 文本行          | 允许             | 日志处理、配置文件读取  |
| `ScanRunes` | UTF-8字符      | 无              | 多语言文本处理、字形分析 |
| `ScanWords` | 单词           | 无              | 文本统计、简单数据解析  |
# 3 类型
## 3.1 Reader

`bufio.Reader` 为 `io.Reader` 提供了缓冲功能，减少直接访问底层数据源的次数，从而提升读取效率。

### 3.1.1 初始化​​

- ​**​`NewReader(rd io.Reader) *Reader`​**​  
    创建默认缓冲区大小（4096字节）的 `Reader`。
- ​**​`NewReaderSize(rd io.Reader, size int) *Reader`​**​  
    自定义缓冲区大小，适用于需要优化内存或处理大块数据的场景。

```go
file, _ := os.Open("data.txt") 
reader := bufio.NewReader(file) // 默认4KB缓冲 
largeReader := bufio.NewReaderSize(file, 64 * 1024) // 64KB缓冲
```
### 3.1.2 基础读取​​

- ​**​`Read(p []byte) (n int, err error)`​**​  
    读取数据到 `p`，可能未填满 `p`。需检查 `n` 和 `err`。  
    ​**​适用场景​**​：通用数据读取，需手动处理部分读取情况。  
    ​**​注意​**​：需配合 `io.ReadFull` 确保读取完整数据。

```go
buf := make([]byte, 1024) 
n, err := reader.Read(buf) 
if err != nil && err != io.EOF {
    log.Fatal(err) 
    }
```
### 3.1.3 按分隔符读取​​

- ​**​`ReadBytes(delim byte) ([]byte, error)`​**​  
    读取直到遇到 `delim`，返回包含分隔符的数据。  
    ​**​适用场景​**​：按行（`\n`）或自定义分隔符（如 `,`）解析数据。

```go
data, err := reader.ReadBytes('\n') 
if err != nil {
    // 处理错误 } 
fmt.Println("Line:", string(data))
```

- ​**​`ReadString(delim byte) (string, error)`​**​  
    功能同 `ReadBytes`，但返回字符串，避免额外转换。

```go
line, err := reader.ReadString('\n')
```
### 3.1.4 **行读取​**​

- ​**​`ReadLine() (line []byte, isPrefix bool, err error)`​**​  
    低级行读取方法，不包含行尾符。`isPrefix` 表示行被截断。  
    ​**​注意​**​：推荐使用 `ReadBytes('\n')` 或 `Scanner` 简化处理。

```go
for {     
    line, isPrefix, err := reader.ReadLine()     
    if err == io.EOF { 
            break     
            }     
    if isPrefix {         // 处理超长行（需多次读取）     }     
    fmt.Println("Line:", string(line)) }
```
### 3.1.5 **字符与字节处理​**​

- ​**​`ReadByte() (byte, error)`​**​  
    读取单个字节，适用于二进制解析。

```go
b, err := reader.ReadByte() 
if err != nil {     
// 处理错误 
} 
fmt.Printf("Byte: %c\n", b)
```

- ​**​`ReadRune() (r rune, size int, err error)`​**​  
    读取UTF-8字符，自动处理编码错误（返回 `U+FFFD`）。

```go
r, size, err := reader.ReadRune() 
if err != nil {     
// 处理错误 
} 
fmt.Printf("Rune: %c (Size: %d)\n", r, size)
```
### 3.1.6 **缓冲区操作​**​

- ​**​`Peek(n int) ([]byte, error)`​**​  
    预读 `n` 字节不移动指针，用于协议头解析等场景。  
    ​**​注意​**​：调用后无法使用 `UnreadByte/Rune` 直到下次读取。

```go
header, err := reader.Peek(4) 
if bytes.HasPrefix(header, []byte("HTTP")) { 
// 处理HTTP响应 
}
```

- ​**​`UnreadByte() error`​**​  
    回退最后一个读取的字节，仅限前操作为读操作。

```go
b, _ := reader.ReadByte() 
if b != 'A' {
    reader.UnreadByte() // 撤销读取 
    }
```

- ​**​`UnreadRune() error`​**​  
    回退最后一个读取的rune，仅限前操作为 `ReadRune`。
### 3.1.7 ​跳过与清空​​

- ​**​`Discard(n int) (int, error)`​**​  
    跳过 `n` 字节，用于忽略无用数据段。

```go
// 跳过文件头 
discarded, err := reader.Discard(128) 
if err != nil {
    // 处理无法跳过的错误 
    }
```

- ​**​`Reset(r io.Reader)`​**​  
    重置Reader，切换底层数据源并清空缓冲。  
    ​**​适用场景​**​：复用Reader实例处理多个流。

```go
reader.Reset(newSource) // 重置后读取新数据源
```
### 3.1.8 **高效数据转移​**​

- ​**​`WriteTo(w io.Writer) (n int64, err error)`​**​  
    将数据直接写入 `w`，利用底层 `WriteTo` 优化（如文件复制）。

```go
written, err := reader.WriteTo(os.Stdout)
fmt.Printf("Copied %d bytes\n", written)
```

当调用 `bufio.Reader` 的 `WriteTo` 方法时，其内部逻辑如下：

1. ​**​检查底层 `io.Reader` 是否实现了 `io.WriterTo`​**​：
    
    - 如果 ​**​是​**​，直接调用底层对象的 `WriteTo` 方法，绕过 `bufio.Reader` 的缓冲区。
    - 如果 ​**​否​**​，使用 `bufio.Reader` 的缓冲机制，多次调用底层 `Read` 方法读取数据并写入 `w`。
2. ​**​性能优化目的​**​：
    
    - 避免双重缓冲（底层和 `bufio` 的缓冲同时存在），减少内存复制。
    - 利用底层可能存在的更高效写入实现（如零拷贝技术）。
### 3.1.9 ​状态查询​​

- ​**​`Buffered() int`​**​  
    返回缓冲区可读字节数，用于预判数据是否足够。

```go
if reader.Buffered() >= 4 {  
    data, _ := reader.Peek(4) 
    }
```

- ​**​`Size() int`​**​  
    获取缓冲区大小，用于调试或动态调整。

```go
fmt.Println("Buffer size:", reader.Size())
```


### 3.1.10 ​**​使用场景对比​**​

| ​**​方法​**​             | ​**​适用场景​**​  | ​**​注意事项​**​      |
| ---------------------- | ------------- | ----------------- |
| `Read`                 | 通用数据读取        | 需处理部分读取和错误        |
| `ReadBytes/ReadString` | 按分隔符读取完整数据块   | 内存占用可能较高          |
| `ReadLine`             | 需要处理超长行的低级操作  | 推荐使用 `Scanner` 替代 |
| `Peek`                 | 协议头检测或数据预判    | 避免后续Unread操作      |
| `Discard`              | 跳过无用数据段       | 确保跳过的字节数有效        |
| `WriteTo`              | 高效数据转移（如文件复制） | 优先利用底层优化          |
## 3.2 Writer

`bufio.Writer` 为 `io.Writer` 提供缓冲功能，通过减少系统调用次数提升写入效率。

### 3.2.1 **初始化​**​

- ​**​`NewWriter(w io.Writer) *Writer`​**​  
    创建默认缓冲区大小（4096字节）的 `Writer`。
- ​**​`NewWriterSize(w io.Writer, size int) *Writer`​**​  
    自定义缓冲区大小，适用于大文件写入或高频小数据场景。

```go
file, _ := os.Create("output.log") 
defer file.Close()  // 默认4KB缓冲 
writer := bufio.NewWriter(file)  // 自定义64KB缓冲 
largeWriter := bufio.NewWriterSize(file, 64 * 1024)
```
### 3.2.2 **写入数据​**​

- ​**​`Write(p []byte) (int, error)`​**​  
    将数据写入缓冲区。若缓冲区空间不足，自动刷新后继续写入。  
    ​**​注意​**​：返回的写入字节数可能小于 `len(p)`，需检查错误。

```go
data := []byte("Hello, World!") 
n, err := writer.Write(data) 
if err != nil {
    log.Fatal("写入失败:", err) 
    }
```

- ​**​`WriteString(s string) (int, error)`​**​  
    直接写入字符串，避免转换为 `[]byte`。

```go
str := "Hello, Go!" 
n, err := writer.WriteString(str)
```

- ​**​`WriteByte(c byte) error`​**​  
    写入单个字节，适用于二进制数据。

```go
err := writer.WriteByte('\n') // 写入换行符
```

- ​**​`WriteRune(r rune) (int, error)`​**​  
    写入UTF-8字符，自动处理编码。

```go
size, err := writer.WriteRune('🚀') // 写入Unicode字符
```
### 3.2.3 缓冲区管理​​

- ​**​`Flush() error`​**​  
    强制将缓冲区数据写入底层 `Writer`，​**​必须在写入结束后调用​**​。

```go
err := writer.Flush() // 确保数据持久化
```

- ​**​`Available() int`​**​  
    返回缓冲区剩余空间，用于预判写入是否触发刷新。

```go
if writer.Available() < len(data) { 
// 手动刷新或处理 
}
```

- ​**​`AvailableBuffer() []byte`（Go 1.18+）​**​  
    返回一个可直接追加数据的空切片，需立即通过 `Write` 提交。

```go
buf := writer.AvailableBuffer() 
buf = append(buf, "Debug: "...) 
buf = append(buf, logData...) 
_, err := writer.Write(buf)
```
### 3.2.4 高效数据复制​​

- ​**​`ReadFrom(r io.Reader) (int64, error)`​**​  
    从 `Reader` 读取数据并写入缓冲区，优先调用底层 `ReadFrom` 实现优化性能。

```go
file, _ := os.Open("source.txt") 
n, err := writer.ReadFrom(file) // 高效复制文件内容
```
### 3.2.5 状态查询与重置​​

- ​**​`Buffered() int`​**​  
    返回当前缓冲区中待刷新的字节数。

```go
if writer.Buffered() > 4096 {
writer.Flush() // 缓冲区接近满载时手动刷新 
}
```

- ​**​`Reset(w io.Writer)`​**​  
    重置 `Writer`，切换底层目标并清空缓冲区。

```go
newFile, _ := os.Create("new.log") 
writer.Reset(newFile) // 复用Writer处理新文件
```
### 3.2.6 注意事项​​

1. ​**​错误处理​**​：一旦写入出错，后续操作均返回相同错误，需及时终止并处理。
2. ​**​缓冲区刷新​**​：程序退出或关键操作后必须调用 `Flush`，避免数据丢失。
3. ​**​并发安全​**​：`bufio.Writer` 非并发安全，需外部同步（如 `sync.Mutex`）。
4. ​**​性能权衡​**​：
    - ​**​缓冲区大小​**​：默认4KB适用于多数场景，大文件可调至64KB~1MB。
    - ​**​自动刷新​**​：缓冲区满时自动触发，但需手动控制关键点刷新。
## 3.3 ReadWriter

```go
type ReadWriter struct {
	*Reader
	*Writer
}
```

ReadWriter 存储指向 Reader 和 Writer 的指针。它实现了 io.ReadWriter 。

## 3.4 Scanner

`bufio.Scanner` 是 Go 标准库中用于高效逐块读取数据的工具，尤其适合处理结构化文本（如按行分割的日志、单词或自定义格式）。

- ​**​按标记（Token）分割输入流​**​：支持按行、单词、字符或自定义规则分割。
- ​**​自动缓冲管理​**​：减少系统调用，提升读取效率。
- ​**​轻量级 API​**​：简化逐块读取逻辑，避免手动处理缓冲区和边界条件。
### 3.4.1 初始化与基础操作​

- ​**​`NewScanner(r io.Reader) *Scanner`​**​  
    创建 `Scanner` 实例，默认分割函数为 `ScanLines`（按行分割）。
    
```go
file, _ := os.Open("data.txt") 
scanner := bufio.NewScanner(file)
```
    
- ​**​`Scan() bool`​**​  
    推进扫描器到下一个标记。返回 `true` 表示成功获取标记，`false` 表示结束（EOF 或错误）。
    
```go
for scanner.Scan() {
    fmt.Println(scanner.Text()) // 逐行处理 
    } 
if err := scanner.Err(); err != nil {
    log.Fatal("扫描错误:", err) 
    }
```
### 3.4.2 获取标记内容​​

- ​**​`Text() string`​**​  
    返回当前标记的字符串（自动复制数据，安全但可能增加内存分配）。
    
```go
line := scanner.Text()
```
    
- ​**​`Bytes() []byte`​**​  
    返回当前标记的字节切片（直接引用内部缓冲区，需立即使用或复制）。
    
```
data := scanner.Bytes() 
copyBuf := make([]byte, len(data)) 
copy(copyBuf, data)
```
### 3.4.3 分割函数与缓冲控制​​

- ​**​`Split(split SplitFunc)`​**​  
    设置自定义分割函数，支持以下内置函数：
    
    - `ScanLines`：按行分割（默认）。
    - `ScanWords`：按空格分割单词。
    - `ScanRunes`：按 UTF-8 字符分割。
    - `ScanBytes`：按字节分割。
    
```go
// 按单词分割 
scanner.Split(bufio.ScanWords)
```
    
- ​**​`Buffer(buf []byte, max int)`​**​  
    设置初始缓冲区和最大容量，避免因大标记导致错误。
    
```
// 处理最大 1MB 的标记 
buf := make([]byte, 4096) 
scanner.Buffer(buf, 1<<20) // 初始 4KB，最大 1MB`
```
### 3.4.4 错误处理​

- ​**​`Err() error`​**​  
    返回扫描过程中首个非 `EOF` 错误。
    
```go
if scanner.Scan() {
    // 正常处理 
    } else if err := scanner.Err(); err != nil {  
       // 处理错误（如缓冲区不足、I/O 错误） 
       }
```
### 3.4.5 底层逻辑与性能优化​​

> ​**​3.1 缓冲机制​**​

- ​**​内部缓冲区​**​：`Scanner` 维护一个动态缓冲区，按需从底层 `Reader` 读取数据。
- ​**​填充策略​**​：当缓冲区无法容纳下一个标记时，自动扩容（受 `Buffer` 方法约束）或触发错误。

> ​**​3.2 分割函数（`SplitFunc`）​**​

- ​**​函数签名​**​：
    
```go
type SplitFunc func(data []byte, atEOF bool) (advance int, token []byte, err error)
```
    
- `data`：当前缓冲区未处理的数据。
- `atEOF`：是否已读到输入流的末尾。
- `advance`：本次处理消耗的字节数。
- `token`：提取的标记（可为 `nil`）。
- `err`：错误（如 `ErrFinalToken` 表示结束扫描）。

- ​**​自定义示例​**​（按分号分割）：
    
```go
func splitBySemicolon(data []byte, atEOF bool) (int, []byte, error) { 
    if i := bytes.IndexByte(data, ';'); i >= 0 { 
            return i + 1, data[0:i], nil // 返回分号前的内容    
             }     
    if atEOF {
             return len(data), data, nil // 处理末尾数据     
             }     
    return 0, nil, nil // 请求更多数据 
    }  
    scanner.Split(splitBySemicolon)
```
    

>  ​**​3.3 错误与恢复​**​

- ​**​不可恢复性​**​：一旦遇到错误（如 `ErrTooLong` 或 I/O 错误），扫描终止。
- ​**​缓冲区限制​**​：默认最大标记大小为 `bufio.MaxScanTokenSize`（64KB），超出需显式设置 `Buffer`。