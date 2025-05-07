Go语言中的`io`包为I/O操作提供了基础接口和工具，旨在抽象不同底层实现的细节，使代码能够以统一的方式处理多种I/O类型（如文件、内存缓冲区、网络连接等）。

 > ​​核心接口​​

1. ​**​`Reader`接口​**​：
    
    - ​**​定义​**​：`Read(p []byte) (n int, err error)`
    - ​**​作用​**​：从数据源读取数据到字节切片`p`中，返回读取的字节数`n`和可能的错误（如`io.EOF`表示数据结束）。
    - ​**​常见实现​**​：`os.File`（文件）、`bytes.Buffer`（内存缓冲区）、`net.Conn`（网络连接）。
2. ​**​`Writer`接口​**​：
    
    - ​**​定义​**​：`Write(p []byte) (n int, err error)`
    - ​**​作用​**​：将字节切片`p`写入目标，返回实际写入的字节数`n`和错误。
    - ​**​常见实现​**​：同`Reader`的实现类型。
3. ​**​`Closer`接口​**​：
    
    - ​**​定义​**​：`Close() error`
    - ​**​作用​**​：关闭资源（如文件、网络连接），释放相关系统资源。
4. ​**​组合接口​**​：
    
    - `ReadWriter`：组合了`Reader`和`Writer`。
    - `ReadCloser`/`WriteCloser`：组合了`Closer`接口，用于读写后关闭资源。
    - `Seeker`：提供`Seek(offset int64, whence int) (int64, error)`方法，用于调整读写位置（如随机访问文件）。
# 1 常量

```go
const (
	SeekStart   = 0 // seek relative to the origin of the file
	SeekCurrent = 1 // seek relative to the current offset
	SeekEnd     = 2 // seek relative to the end
)
```
# 2 变量

## 2.1 EOF (End Of File)​​

- ​**​定义​**​：
    
    ```go
    var EOF = errors.New("EOF")
    ```
    
- ​**​用途​**​：  
    当 `Reader` 读取到输入流的末尾时返回此错误。​**​它表示正常的数据结束​**​，而不是一个真正的错误。
- ​**​关键特性​**​：
    - 必须直接返回 `EOF` 自身（而不是用 `fmt.Errorf` 包装），因为调用方通常用 `==` 直接比较错误：
        
        ```go
        if err == io.EOF {
            // 处理正常结束
        }
        ```
        
    - 仅在数据​**​预期结束​**​时返回。例如，读取文件到末尾。
- ​**​示例场景​**​：
    
    ```go
    data := make([]byte, 100)
    n, err := reader.Read(data)
    if err == io.EOF {
        fmt.Println("数据读取完毕")
    }
    ```

## 2.2 ​ErrUnexpectedEOF​

- ​**​定义​**​：
    
    ```go
    var ErrUnexpectedEOF = errors.New("unexpected EOF")
    ```
    
- ​**​用途​**​：  
    当在读取​**​固定大小的数据块或结构化数据​**​时，未达到预期长度就遇到了 `EOF`。这表示数据可能被意外截断。
- ​**​常见场景​**​：
    - 读取协议头（如固定长度的二进制头部）。
    - 解码结构化数据（如 JSON/XML 片段不完整）。
- ​**​示例​**​：
    
    ```go
    buf := make([]byte, 1024)
    if _, err := io.ReadFull(reader, buf); err != nil {
        if err == io.ErrUnexpectedEOF {
            fmt.Println("数据不完整")
        }
    }
    ```

## 2.3 ​ErrClosedPipe​

- ​**​定义​**​：
    
    ```go
    var ErrClosedPipe = errors.New("io: read/write on closed pipe")
    ```
    
- ​**​用途​**​：  
    当对已关闭的 `Pipe`（管道）执行读/写操作时返回此错误。管道通常用于连接并发代码（如 `io.Pipe()`）。
- ​**​典型场景​**​：
    
    ```go
    pr, pw := io.Pipe()
    pw.Close() // 显式关闭写入端
    
    _, err := pw.Write([]byte("data"))
    if err == io.ErrClosedPipe {
        fmt.Println("管道已关闭")
    }
    ```

## 2.4 ​ErrShortBuffer​

- ​**​定义​**​：
    
    ```go
    var ErrShortBuffer = errors.New("short buffer")
    ```
    
- ​**​用途​**​：  
    当 `Reader` 需要读取的数据长度超过了提供的缓冲区容量时返回此错误。
- ​**​常见于​**​：
    - `io.ReadFull`：尝试填充整个缓冲区，但输入流提前结束。
- ​**​示例​**​：
    
    ```go
    buf := make([]byte, 5)
    if _, err := io.ReadFull(reader, buf); err != nil {
        if err == io.ErrShortBuffer {
            fmt.Println("缓冲区太小")
        }
    }
    ```

## 2.5 ​ErrShortWrite​

- ​**​定义​**​：
    
    ```go
    var ErrShortWrite = errors.New("short write")
    ```
    
- ​**​用途​**​：  
    当 `Writer` 实际写入的字节数少于请求的字节数，但未返回明确的错误时触发。这通常表示底层 I/O 资源异常（如磁盘满）。
- ​**​关键点​**​：
    - 与 `ErrShortBuffer` 不同，此错误发生在写入端。
- ​**​处理建议​**​：
    - 可能需要重试写入剩余的数据。
- ​**​示例​**​：
    
    ```go
    data := []byte("hello")
    n, err := writer.Write(data)
    if err == io.ErrShortWrite {
        fmt.Printf("仅写入 %d 字节\n", n)
    }
    ```


## 2.6 ​ErrNoProgress​

- ​**​定义​**​：
    
    ```go
    var ErrNoProgress = errors.New("multiple Read calls return no data or error")
    ```
    
- ​**​用途​**​：  
    当连续多次调用 `Reader.Read` 均未返回数据或错误时触发。通常表示 `Reader` 的实现存在缺陷（如死循环）。
- ​**​典型场景​**​：
    - 自定义的 `Reader` 未正确处理读取逻辑。
- ​**​示例​**​：
    
    ```go
    type BrokenReader struct{}
    
    func (r *BrokenReader) Read(p []byte) (n int, err error) {
        // 错误实现：永远返回 0, nil
        return 0, nil
    }
    
    func main() {
        buf := make([]byte, 10)
        _, err := io.ReadAtLeast(&BrokenReader{}, buf, 1)
        if err == io.ErrNoProgress {
            fmt.Println("Reader 实现异常")
        }
    }
    ```

> 错误处理最佳实践​​

1. ​**​区分 `EOF` 和 `ErrUnexpectedEOF`​**​：
    - 使用 `io.ReadFull` 或类似方法读取固定长度数据时，优先检查 `ErrUnexpectedEOF`。
2. ​**​避免包装 `EOF`​**​：
    
    ```go
    // 正确
    return 0, io.EOF
    
    // 错误（会导致 == 判断失败）
    return 0, fmt.Errorf("read failed: %w", io.EOF)
    ```
# 3 函数
## 3.1 func Copy(dst Writer, src Reader) (written int64, err error)​

- ​**​作用​**​：  
    将数据从 `src` 读取并写入 `dst`，直到 `src` 返回 `io.EOF` 或发生错误。内部自动管理缓冲区，默认使用 32KB 的临时缓冲区。
- ​**​返回值​**​：  
    成功复制的字节数 `written` 和遇到的第一个错误（如 `io.EOF`）。
    成功的复制返回 err == nil，而不是 err == EOF。由于 Copy 被定义为从 src 读取到 EOF，因此它不会将 Read 中的 EOF 视为要报告的错误。
- ​**​适用场景​**​：
    - 文件拷贝（如从 `os.File` 复制到另一个文件）。
    - 网络数据传输（如将 `net.Conn` 内容写入 `bytes.Buffer`）。
- ​**​示例​**​：
    
    ```go
    src, _ := os.Open("input.txt")
    dst, _ := os.Create("output.txt")
    written, err := io.Copy(dst, src) // 复制文件
    ```

## 3.2 ​func CopyBuffer(dst Writer, src Reader, buf \[\]byte) (written int64, err error)

- ​**​作用​**​：  
    与 `Copy` 功能相同，但允许自定义缓冲区 `buf`。若 `buf` 为 `nil`，函数会自行创建默认大小为1的缓冲区。
- ​**​适用场景​**​：
    - 需要复用或控制缓冲区大小的场景（如高频调用时减少内存分配）。
- ​**​示例​**​：
    
    ```go
    buf := make([]byte, 64 * 1024) // 64KB 缓冲区
    written, err := io.CopyBuffer(dst, src, buf)
    ```

## 3.3 ​func CopyN(dst Writer, src Reader, n int64) (written int64, err error)​

- ​**​作用​**​：  
    从 `src` 复制​**​精确的 `n` 字节​**​到 `dst`。若 `src` 提前返回 `io.EOF`，会触发 `io.ErrUnexpectedEOF`。
- ​**​适用场景​**​：
    - 复制固定长度的数据（如读取协议头或分块传输）。
- ​**​示例​**​：
    
    ```go
    // 复制前 100 字节
    written, err := io.CopyN(dst, src, 100)
    if errors.Is(err, io.ErrUnexpectedEOF) {
        fmt.Println("数据不足 100 字节")
    }
    ```

## 3.4 func Pipe() (\*PipeReader, \*PipeWriter)​

- ​**​作用​**​：  
    创建一对关联的 `PipeReader` 和 `PipeWriter`，形成一个内存管道。写入 `PipeWriter` 的数据可直接被 `PipeReader` 读取。
- ​**​特性​**​：
    - ​**​阻塞性​**​：写入操作会阻塞，直到另一端读取数据（反之亦然）。
    - ​**​错误处理​**​：关闭一端后，另一端的读写会返回 `io.ErrClosedPipe`。
- ​**​适用场景​**​：
    - 连接需要分离读写逻辑的代码（如加密/解密流水线）。
    - 多 goroutine 间数据传递。
- ​**​示例​**​：
    
    ```go
    pr, pw := io.Pipe()
    go func() {
        defer pw.Close()
        pw.Write([]byte("通过管道传输的数据"))
    }()
    data, _ := io.ReadAll(pr) // 读取数据
    ```

## 3.5 ​func ReadAll(r Reader) (\[\]byte, error)

- ​**​作用​**​：  
    读取 `r` 的所有数据直到 `io.EOF`，返回完整字节切片。
- ​**​注意​**​：
    - ​**​内存风险​**​：大文件可能导致内存耗尽，建议改用流式处理（如 `io.Copy`）。
    - ReadAll 从 r 读取，直到出现错误或 EOF，并返回它读取的数据。成功的调用返回 err == nil，而不是 err == EOF。由于 ReadAll 定义为从 src 读取到 EOF，因此它不会将 Read 中的 EOF 视为要报告的错误。
- ​**​适用场景​**​：
    - 读取小型配置文件或 HTTP 响应体。
- ​**​示例​**​：
    
    ```go
    data, err := io.ReadAll(resp.Body) // 读取 HTTP 响应
    ```

## 3.6 ​func ReadAtLeast(r Reader, buf \[\]byte, min int) (n int, err error)​

- ​**​作用​**​：  
    从 `r` 读取至少 `min` 字节到 `buf`。若实际读取的字节数 `< min`，返回 `io.ErrUnexpectedEOF`（若 `r` 提前结束）或 `io.ErrShortBuffer`（若 `buf` 太小）。
- ​**​适用场景​**​：
    - 读取必须满足最小长度的数据（如二进制协议解析）。
- ​**​示例​**​：
    
    ```go
    buf := make([]byte, 10)
    n, err := io.ReadAtLeast(reader, buf, 5) // 至少读取 5 字节
    ```


## 3.7 ​func ReadFull(r Reader, buf \[\]byte) (n int, err error)​

- ​**​作用​**​：  
    等价于 `ReadAtLeast(r, buf, len(buf))`，即必须填满整个 `buf`。
- ​**​错误​**​：
    - 若未填满且 `r` 结束，返回 `io.ErrUnexpectedEOF`。
- ​**​适用场景​**​：
    - 读取固定长度的数据块（如读取 4 字节的整数）。
- ​**​示例​**​：
    
    ```go
    buf := make([]byte, 4)
    n, err := io.ReadFull(reader, buf) // 必须读取 4 字节
    ```

## 3.8 func WriteString(w Writer, s string) (n int, err error)​

- ​**​作用​**​：  
    将字符串 `s` 写入 `w`。若 `w` 实现了 `io.StringWriter` 接口（如 `bytes.Buffer`），会直接调用其 `WriteString` 方法以优化性能。
- ​**​优化点​**​：
    - 避免将字符串转换为 `[]byte` 的额外内存分配。
- ​**​适用场景​**​：
    - 高效写入字符串内容（如日志输出）。
- ​**​示例​**​：
    
    ```go
    var buf bytes.Buffer
    n, _ := io.WriteString(&buf, "Hello, World!") // 写入字符串
    ```

> ​总结与选择建议​​

|函数|核心用途|关键特性|
|---|---|---|
|`Copy`|流式复制|自动管理缓冲区，适合大文件或网络流|
|`CopyBuffer`|自定义缓冲区复制|控制内存复用|
|`CopyN`|复制固定长度|精确控制复制量|
|`Pipe`|内存管道通信|阻塞式读写，适用并发场景|
|`ReadAll`|读取全部数据|简单但需注意内存风险|
|`ReadAtLeast`|读取最小字节|确保最低数据量|
|`ReadFull`|填满缓冲区|严格数据完整性|
|`WriteString`|高效写入字符串|避免类型转换开销|
