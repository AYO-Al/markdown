Go 标准库中的 `strings` 包是处理文本数据的核心工具，提供高效且功能丰富的字符串操作函数。
# 1 函数
## 1.1 字符串基础操作
### 1.1.1 func Clone(s string) string

​**​作用​**​：创建字符串副本（避免内存共享）  
​**​注意​**​：Go 1.18+ 引入，用于避免大字符串内存泄漏  
​**​示例​**​：

```go
s1 := "Hello, 世界"
s2 := strings.Clone(s1)
fmt.Println(s2) // Hello, 世界
```
### 1.1.2 func Compare(a, b string) int

​**​作用​**​：按字典序比较字符串  
​**​返回值​**​：

- `0`：相等
- `-1`：a < b
- `1`：a > b

​**​注意​**​：通常直接使用 `==`、`<`、`>` 运算符  
​**​示例​**​：

```go
fmt.Println(strings.Compare("apple", "banana")) // -1
fmt.Println(strings.Compare("", ""))            // 0
```
## 1.2 包含性检查
### 1.2.1 func Contains(s, substr string) bool

​**​作用​**​：检查是否包含子串  
​**​注意​**​：空子串始终返回 `true`  
​**​示例​**​：

```go
fmt.Println(strings.Contains("Golang", "go")) // false（大小写敏感）
fmt.Println(strings.Contains("", ""))         // true
```
### 1.2.2 func ContainsAny(s, chars string) bool

​**​作用​**​：检查是否包含 chars 中的任意字符  
​**​注意​**​：chars 为空时返回 `false`  
​**​示例​**​：

```go
fmt.Println(strings.ContainsAny("team", "aeiou")) // true（含 'e'）
fmt.Println(strings.ContainsAny("fail", "xyz"))  // false
```
### 1.2.3 func ContainsFunc(s string, f func(rune) bool) bool

​**​作用​**​：检查是否包含满足条件的字符（Go 1.23+）  
​**​注意​**​：空字符串始终返回 `false`  
​**​示例​**​：

```go
hasDigit := func(r rune) bool { return unicode.IsDigit(r) }
fmt.Println(strings.ContainsFunc("a1b", hasDigit)) // true
fmt.Println(strings.ContainsFunc("abc", hasDigit)) // false
```
### 1.2.4 func ContainsRune(s string, r rune) bool

​**​作用​**​：检查是否包含特定 Unicode 字符

```go
fmt.Println(strings.ContainsRune("日本語", '語')) // true
fmt.Println(strings.ContainsRune("", 'a'))      // false
```
## 1.3 计数与分割
### 1.3.1 func Count(s, substr string) int

​**​作用​**​：计算子串出现次数  
​**​注意​**​：空子串返回 `len(s)+1`  
​**​示例​**​：

```go
fmt.Println(strings.Count("cheese", "e")) // 3
fmt.Println(strings.Count("five", ""))   // 5
```
### 1.3.2 func Cut(s, sep string) (before, after string, found bool)

​**​作用​**​：在第一个分隔符处切割字符串  
​**​注意​**​：未找到分隔符时返回 `s, "", false`  
​**​示例​**​：

```go
before, after, found := strings.Cut("name=John", "=")
fmt.Printf("%q, %q, %v\n", before, after, found) // "name", "John", true

before, after, found = strings.Cut("no_separator", "=")
fmt.Printf("%q, %q, %v\n", before, after, found) // "no_separator", "", false
```
### 1.3.3 func CutPrefix(s, prefix string) (after string, found bool)

​**​作用​**​：移除前缀（如存在）
​**​示例​**​：

```go
after, found := strings.CutPrefix("Golang is fun", "Golang")
fmt.Printf("%q, %v\n", after, found) // " is fun", true

after, found = strings.CutPrefix("Hello", "Hi")
fmt.Printf("%q, %v\n", after, found) // "Hello", false
```
### 1.3.4 func CutSuffix(s, suffix string) (before string, found bool)

​**​作用​**​：移除后缀（如存在）
**示例​**​：

```go
before, found := strings.CutSuffix("backup.tar.gz", ".gz")
fmt.Printf("%q, %v\n", before, found) // "backup.tar", true

before, found = strings.CutSuffix("data.json", ".xml")
fmt.Printf("%q, %v\n", before, found) // "data.json", false
```
## 1.4 大小写处理

### 1.4.1 func EqualFold(s, t string) bool

​**​作用​**​：不区分大小写比较字符串  
​**​注意​**​：支持 Unicode 大小写折叠  
​**​示例​**​：

```go
fmt.Println(strings.EqualFold("Go", "go"))    // true
fmt.Println(strings.EqualFold("ß", "ss"))    // true（德语）
```
### 1.4.2 func ToLower(s string) string

​**​作用​**​：转换为小写  
​**​注意​**​：使用 Unicode 规则  
​**​示例​**​：

```go
fmt.Println(strings.ToLower("GOPHER")) // "gopher"
```
### 1.4.3 func ToUpper(s string) string

​**​作用​**​：转换为大写  
​**​示例​**​：

```go
fmt.Println(strings.ToUpper("gopher")) // "GOPHER"
```
## 1.5 分割与连接
### 1.5.1 func Fields(s string) \[\]string

**作用​**​：按空白分割字符串  
​**​注意​**​：连续空白视为单分隔符  
​**​示例​**​：

```go
fmt.Printf("%q\n", strings.Fields("  a b  c ")) // ["a", "b", "c"]
```
### 1.5.2 func FieldsFunc(s string, f func(rune) bool) \[\]string

​**​作用​**​：按自定义函数分割  
​**​示例​**​：

```go
splitOnDigit := func(r rune) bool { return unicode.IsDigit(r) }
fmt.Printf("%q\n", strings.FieldsFunc("a1b2c3", splitOnDigit)) // ["a", "b", "c"]
```
### 1.5.3 func Join(elems \[\]string, sep string) string

​**​作用​**​：连接字符串切片  
​**​注意​**​：空切片返回空字符串  
​**​示例​**​：

```go
fmt.Println(strings.Join([]string{"a", "b"}, "-")) // "a-b"
fmt.Println(strings.Join([]string{}, ","))         // ""
```
### 1.5.4 func Split(s, sep string) \[\]string

​**​作用​**​：按分隔符分割字符串  
​**​注意​**​：空分隔符按字符分割  
​**​示例​**​：

```go
fmt.Printf("%q\n", strings.Split("a,b,c", ",")) // ["a", "b", "c"]
fmt.Printf("%q\n", strings.Split("abc", ""))    // ["a", "b", "c"]
```
### 1.5.5 func SplitAfterN(s, sep string, n int) \[\]string

​**​作用​**​：分割并保留分隔符  
​**​参数​**​：`n` - 控制返回子串数量  
​**​注意​**​：`n < 0` 时无限制  
​**​示例​**​：

```go
fmt.Printf("%q\n", strings.SplitAfterN("a,b,c", ",", 2)) // ["a,", "b,c"]
```
## 1.6 索引查找
### 1.6.1 func Index(s, substr string) int

​**​作用​**​：查找子串首次出现位置  
​**​返回值​**​：未找到返回 `-1`  
​**​示例​**​：

```go
fmt.Println(strings.Index("chicken", "ken")) // 4
fmt.Println(strings.Index("chicken", "egg")) // -1
```
### 1.6.2 func LastIndex(s, substr string) int

​**​作用​**​：查找子串最后一次出现位置  
​**​示例​**​：

```go
fmt.Println(strings.LastIndex("go gopher", "go")) // 3
```
### 1.6.3 func IndexByte(s string, c byte) int

​**​作用​**​：查找字节首次出现位置  
​**​注意​**​：仅处理单字节  
​**​示例​**​：

```go
fmt.Println(strings.IndexByte("golang", 'a')) // 3
```
### 1.6.4 func IndexRune(s string, r rune) int

​**​作用​**​：查找 Unicode 字符位置  
​**​示例​**​：

```go
fmt.Println(strings.IndexRune("日本語", '本')) // 3（UTF-8位置）
```
### 1.6.5 func IndexFunc(s string, f func(rune) bool) int

​**​作用​**​：查找满足条件的字符位置  
​**​示例​**​：

```go
isDigit := func(r rune) bool { return unicode.IsDigit(r) }
fmt.Println(strings.IndexFunc("abc123", isDigit)) // 3
```
## 1.7 修剪操作
### 1.7.1 func Trim(s, cutset string) string

​**​作用​**​：移除两端指定字符集  
​**​注意​**​：按字符集移除，非子串  
​**​示例​**​：

```go
fmt.Printf("%q\n", strings.Trim("¡¡Hello!¡", "!¡")) // "Hello"
```
### 1.7.2 func TrimSpace(s string) string

​**​作用​**​：移除两端空白  
​**​注意​**​：包括空格、制表符、换行符  
​**​示例​**​：

```go
fmt.Printf("%q\n", strings.TrimSpace(" \t\n Hello \n\t ")) // "Hello"
```
### 1.7.3 func TrimPrefix(s, prefix string) string

​**​作用​**​：移除指定前缀  
​**​注意​**​：无前缀时返回原字符串  
​**​示例​**​：

```go
fmt.Println(strings.TrimPrefix("test.example", "test.")) // "example"
fmt.Println(strings.TrimPrefix("example", "test."))      // "example"
```
### 1.7.4 func TrimSuffix(s, suffix string) string

​**​作用​**​：移除指定后缀  
​**​示例​**​：

```go
fmt.Println(strings.TrimSuffix("backup.tar.gz", ".gz")) // "backup.tar"
```
### 1.7.5 func TrimFunc(s string, f func(rune) bool) string

​**​作用​**​：按自定义函数修剪两端  
​**​示例​**​：

```go
notLetter := func(r rune) bool { return !unicode.IsLetter(r) }
fmt.Println(strings.TrimFunc("123abc456", notLetter)) // "abc"
```
## 1.8 映射与替换
### 1.8.1 func Map(mapping func(rune) rune, s string) string

​**​作用​**​：对每个字符应用映射函数  
​**​注意​**​：返回 `rune(-1)` 会删除字符  
​**​示例​**​：

```go
rot13 := func(r rune) rune {
    switch {
    case r >= 'A' && r <= 'Z':
        return 'A' + (r-'A'+13)%26
    case r >= 'a' && r <= 'z':
        return 'a' + (r-'a'+13)%26
    }
    return r
}
fmt.Println(strings.Map(rot13, "Hello")) // "Uryyb"
```
### 1.8.2 func Replace(s, old, new string, n int) string

​**​作用​**​：替换子串  
​**​参数​**​：`n` - 替换次数（`n<0` 表示全部替换）  
​**​注意​**​：`old` 为空时在字符间插入 `new`  
​**​示例​**​：

```go
fmt.Println(strings.Replace("oink oink oink", "k", "ky", 2)) // "oinky oinky oink"
fmt.Println(strings.Replace("abc", "", "-", -1))             // "-a-b-c-"
```
### 1.8.3 func ReplaceAll(s, old, new string) string

​**​作用​**​：替换所有子串  
​**​示例​**​：

```go
fmt.Println(strings.ReplaceAll("banana", "a", "o")) // "bonono"
```
### 1.8.4 func ToValidUTF8(s, replacement string) string

​**​作用​**​：替换无效 UTF-8 序列  
​**​注意​**​：用于清理损坏的 UTF-8 数据  
​**​示例​**​：

```go
invalid := "Hello\x80World"
fmt.Println(strings.ToValidUTF8(invalid, "�")) // "Hello�World"
```
## 1.9 重复与迭代
### 1.9.1 func Repeat(s string, count int) string

​**​作用​**​：重复字符串  
​**​注意​**​：`count<0` 会 panic  
​**​示例​**​：

```go
fmt.Println(strings.Repeat("na", 3)) // "nanana"
```
### 1.9.2 func Lines(s string) iter.Seq\[string\]

​**​作用​**​：迭代字符串行（Go 1.22+）  
​**​注意​**​：使用 `range` 迭代  
​**​示例​**​：

```go
for line := range strings.Lines("line1\nline2\n") {
    fmt.Println(line)
}
// 输出:
// line1
// line2
```
### 1.9.3 func Fields(s string) \[\]string

**作用​**​：按空白字符分割字符串  
​**​返回值​**​：字符串切片  
​**​分割规则​**​：

1. 使用 `unicode.IsSpace` 定义的空白字符：
    - 空格 `' '`
    - 制表符 `'\t'`
    - 换行符 `'\n'`
    - 回车符 `'\r'`
    - 换页符 `'\f'`
    - 垂直制表符 `'\v'`
2. 连续空白视为单分隔符
3. 忽略开头和结尾的空白

```go
package main

import (
	"fmt"
	"strings"
)

func main() {
	s := "  Go is\tawesome\nand  powerful!  "
	fields := strings.Fields(s)
	fmt.Printf("%q\n", fields)
	// 输出: ["Go" "is" "awesome" "and" "powerful!"]
}
```
### 1.9.4 func FieldsFunc(s string, f func(rune) bool) \[\]string

​**​作用​**​：按自定义函数分割字符串  
​**​参数​**​：

- `f func(rune) bool`：分割判断函数
    - 返回 `true`：当前字符是分隔符
    - 返回 `false`：当前字符是内容

​**​返回值​**​：字符串切片  
​**​分割规则​**​：

1. 连续满足 `f` 的字符视为单分隔符
2. 忽略开头和结尾的分隔符

```go
package main

import (
	"fmt"
	"strings"
	"unicode"
)

func main() {
	// 按非字母字符分割
	splitNonAlpha := func(r rune) bool {
		return !unicode.IsLetter(r)
	}
	
	s := "Go1.20, released in 2023!"
	fields := strings.FieldsFunc(s, splitNonAlpha)
	fmt.Printf("%q\n", fields)
	// 输出: ["Go" "released" "in"]
}
```
### 1.9.5 func FieldsSeq(s string) iter.Seq\[string\]

​**​作用​**​：迭代按空白分割的字段  
​**​示例​**​：

```go
for field := range strings.FieldsSeq("a b c") {
    fmt.Println(field)
}
// 输出:
// a
// b
// c
```
### 1.9.6 func FieldsFuncSeq(s string, f func(rune) bool) iter.Seq\[string\] (Go 1.22+)

​**​作用​**​：按自定义函数分割字符串并返回迭代器  
​**​返回值​**​：`iter.Seq[string]`（可遍历的字符串序列）  
​**​特点​**​：

- 惰性求值：按需生成结果
- 内存高效：适合大文本处理
- 流式处理：可中途停止

```go
package main

import (
	"fmt"
	"strings"
	"unicode"
)

func main() {
	// 按数字分割
	splitOnDigit := func(r rune) bool {
		return unicode.IsDigit(r)
	}
	
	s := "a1b22c333d"
	seq := strings.FieldsFuncSeq(s, splitOnDigit)
	
	// 遍历迭代器
	for v := range seq {
		fmt.Println(v)
	}
	// 输出:
	// a
	// b
	// c
	// d
}
```


# 2 类型
## 2.1 Builder

用于​**​高效构建字符串​**​的核心类型，特别适合需要大量字符串拼接的场景。

**核心优势​**​：

- ​**​零值可用​**​：无需初始化即可使用
- ​**​内存高效​**​：自动管理内存分配
- ​**​并发不安全​**​：非线程安全，需自行加锁
### 2.1.1 Cap() int - 获取底层容量

**功能​**​：返回底层字节切片的容量  
​**​返回值​**​：当前分配的字节容量  
​**​注意​**​：容量可能大于实际内容长度

```go
b := strings.Builder{}
fmt.Println("初始容量:", b.Cap()) // 0

b.Grow(100)
fmt.Println("扩容后容量:", b.Cap()) // >=100 (实际可能更大)
```
### 2.1.2 Grow(n int) - 预分配内存

**功能​**​：预分配至少 `n` 字节的内存空间  
​**​参数​**​：`n` - 需要预分配的字节数  
​**​注意​**​：

- 若 `n < 0` 会触发 panic
- 实际分配可能大于 `n`（Go 内存管理策略）

```go
b := strings.Builder{}
b.Grow(1024) // 预分配1KB内存
fmt.Println("预分配后容量:", b.Cap()) // 1024 或更大
```
### 2.1.3 Len() int - 获取内容长度

**功能​**​：返回当前存储的字节数（非字符数）  
​**​返回值​**​：已写入的字节长度

```go
b := strings.Builder{}
b.WriteString("你好")
fmt.Println("字节长度:", b.Len()) // 6 (UTF-8编码)
fmt.Println("字符长度:", utf8.RuneCountInString(b.String())) // 2
```
### 2.1.4 Reset() - 清空内容

**功能​**​：清空内容并尝试释放内存  
​**​注意​**​：重置后仍可重用

```go
b := strings.Builder{}
b.WriteString("临时内容")
b.Reset()
fmt.Println("重置后内容:", b.String()) // 空字符串
fmt.Println("重置后长度:", b.Len()) // 0
```
### 2.1.5 String() string - 获取最终字符串

**功能​**​：返回构建的字符串  
​**​注意​**​：

- 后续修改不会影响已返回的字符串
- 内部使用 `unsafe` 转换，高效无拷贝

```go
b := strings.Builder{}
b.WriteString("Hello")
s1 := b.String()
b.WriteString(" World")
s2 := b.String()

fmt.Println(s1) // "Hello"
fmt.Println(s2) // "Hello World"
```
### 2.1.6 Write(p \[\]byte) (int, error)

**功能​**​：写入字节切片  
​**​参数​**​：`p` - 要写入的字节切片  
​**​返回值​**​：

- `int`：成功写入的字节数（总是 `len(p)`）
- `error`：总是 `nil`（为兼容 `io.Writer` 接口）

```go
b := strings.Builder{}
data := []byte{72, 101, 108, 108, 111} // "Hello"
n, err := b.Write(data)

fmt.Println("写入字节数:", n) // 5
fmt.Println("错误:", err)   // nil
fmt.Println("内容:", b.String()) // "Hello"
```
### 2.1.7 WriteByte(c byte) error

**功能​**​：写入单个字节  
​**​参数​**​：`c` - 要写入的字节  
​**​返回值​**​：`error` 总是 `nil`

```go
b := strings.Builder{}
b.WriteByte('G')
b.WriteByte('o')
fmt.Println(b.String()) // "Go"
```
### 2.1.8 WriteRune(r rune) (int, error)

**功能​**​：写入 Unicode 字符（rune）  
​**​参数​**​：`r` - Unicode 字符  
​**​返回值​**​：

- `int`：写入的字节数
- `error`：总是 `nil`

```go
b := strings.Builder{}
size, _ := b.WriteRune('世')
fmt.Println("写入字节:", size) // 3 (UTF-8编码)
size, _ = b.WriteRune('界')
fmt.Println("内容:", b.String()) // "世界"
```
### 2.1.9 WriteString(s string) (int, error)

**功能​**​：高效写入字符串  
​**​参数​**​：`s` - 要写入的字符串  
​**​返回值​**​：

- `int`：写入的字节数（`len(s)`）
- `error`：总是 `nil`

```go
b := strings.Builder{}
n, _ := b.WriteString("高效")
fmt.Println("写入字节:", n) // 6 (中文字符)
```
## 2.2 Reader

用于​**​高效读取字符串内容​**​的核心类型，实现了多个 I/O 接口，提供类似文件操作的读取能力。

```go
type Reader struct {
    s        string    // 原始字符串
    i        int64     // 当前读取位置
    prevRune int       // 前一个rune位置（用于UnreadRune）
}
```

**核心优势​**​：

- ​**​高效读取​**​：零内存分配
- ​**​随机访问​**​：支持 `ReadAt` 和 `Seek`
- ​**​接口丰富​**​：实现 `io.Reader`、`io.Seeker` 等接口
### 2.2.1 func NewReader(s string) \*Reader

**作用​**​：创建字符串读取器  
​**​参数​**​：`s` - 要读取的字符串  
​**​返回值​**​：指向新创建 Reader 的指针

```go
// 创建包含中文的Reader
r := strings.NewReader("Hello, 世界")
fmt.Printf("创建Reader: %#v\n", r) 
// 输出: &strings.Reader{s:"Hello, 世界", i:0, prevRune:-1}
```
### 2.2.2 func (r \*Reader) Len() int

​**​作用​**​：获取未读取字节数  
​**​返回值​**​：剩余未读取字节数

```go
r := strings.NewReader("Golang")
fmt.Println("初始长度:", r.Len()) // 6
r.Read(make([]byte, 3))
fmt.Println("读取后长度:", r.Len()) // 3
```
### 2.2.3 func (r \*Reader) Size() int64

​**​作用​**​：获取原始字符串总字节数  
​**​返回值​**​：字符串总字节数（与 `Len()` 不同）

```go
r := strings.NewReader("你好")
fmt.Println("总字节数:", r.Size()) // 6 (UTF-8编码)
fmt.Println("未读字节数:", r.Len()) // 6
```
### 2.2.4 func (r \*Reader) Read(b \[\]byte) (n int, err error)

​**​作用​**​：读取数据到字节切片  
​**​参数​**​：`b` - 目标字节切片  
​**​返回值​**​：

- `n`：实际读取字节数
- `err`：`io.EOF`（已读完）或 `nil`

```go
r := strings.NewReader("Reader Demo")
buf := make([]byte, 5)

// 第一次读取
n, err := r.Read(buf)
fmt.Printf("读取 %d 字节: %q, 错误: %v\n", n, buf[:n], err)
// 输出: 读取 5 字节: "Reade", 错误: <nil>

// 第二次读取
n, err = r.Read(buf)
fmt.Printf("读取 %d 字节: %q, 错误: %v\n", n, buf[:n], err)
// 输出: 读取 5 字节: "r Dem", 错误: <nil>

// 第三次读取
n, err = r.Read(buf)
fmt.Printf("读取 %d 字节: %q, 错误: %v\n", n, buf[:n], err)
// 输出: 读取 1 字节: "o", 错误: EOF
```
### 2.2.5 func (r \*Reader) ReadByte() (byte, error)

​**​作用​**​：读取单个字节  
​**​返回值​**​：

- `byte`：读取的字节
- `error`：`io.EOF`（已读完）或 `nil`

```go
r := strings.NewReader("ABC")
b, err := r.ReadByte()
fmt.Printf("字节: %c, 错误: %v\n", b, err) // A, <nil>
b, err = r.ReadByte()
fmt.Printf("字节: %c, 错误: %v\n", b, err) // B, <nil>
b, err = r.ReadByte()
fmt.Printf("字节: %c, 错误: %v\n", b, err) // C, <nil>
b, err = r.ReadByte()
fmt.Printf("字节: %d, 错误: %v\n", b, err) // 0, EOF
```
### 2.2.6 func (r \*Reader) ReadRune() (ch rune, size int, err error)

​**​作用​**​：读取单个 Unicode 字符  
​**​返回值​**​：

- `ch`：Unicode 字符
- `size`：字符占用的字节数
- `err`：`io.EOF` 或 `nil`

```go
r := strings.NewReader("语言")
ch, size, err := r.ReadRune()
fmt.Printf("字符: %c, 大小: %d, 错误: %v\n", ch, size, err) // 语, 3, <nil>
ch, size, err = r.ReadRune()
fmt.Printf("字符: %c, 大小: %d, 错误: %v\n", ch, size, err) // 言, 3, <nil>
ch, size, err = r.ReadRune()
fmt.Printf("字符: %d, 大小: %d, 错误: %v\n", ch, size, err) // 0, 0, EOF
```
### 2.2.7 func (r \*Reader) ReadAt(b \[\]byte, off int64) (n int, err error)

**作用​**​：从指定位置读取（不改变当前读取位置）  
​**​参数​**​：

- `b`：目标字节切片
- `off`：读取起始位置（字节偏移）  
    ​**​返回值​**​：
- `n`：实际读取字节数
- `err`：`io.EOF`（读取到结尾）或 `nil`

```go
r := strings.NewReader("RandomAccess")
buf := make([]byte, 5)

// 从位置7读取
n, err := r.ReadAt(buf, 7)
fmt.Printf("从位置7读取 %d 字节: %q, 错误: %v\n", n, buf[:n], err)
// 输出: 从位置7读取 5 字节: "Acces", 错误: <nil>

// 验证当前读取位置未变
fmt.Println("当前位置:", r.Size()-int64(r.Len())) // 0
```
### 2.2.8 func (r \*Reader) Seek(offset int64, whence int) (int64, error)

​**​作用​**​：移动读取位置  
​**​参数​**​：

- `offset`：偏移量
- `whence`：基准位置（`io.SeekStart`/`io.SeekCurrent`/`io.SeekEnd`）  
    ​**​返回值​**​：
- `int64`：新位置
- `error`：位置无效时返回错误

```go
r := strings.NewReader("SeekExample")

// 移动到开头
pos, err := r.Seek(0, io.SeekStart)
fmt.Println("位置:", pos, "错误:", err) // 0, <nil>

// 向前移动5字节
pos, err = r.Seek(5, io.SeekCurrent)
fmt.Println("位置:", pos, "错误:", err) // 5, <nil>

// 读取验证
b, _ := r.ReadByte()
fmt.Printf("当前字符: %c\n", b) // E

// 移动到结尾
pos, err = r.Seek(-3, io.SeekEnd)
fmt.Println("位置:", pos, "错误:", err) // 8, <nil>

// 读取结尾字符
b, _ = r.ReadByte()
fmt.Printf("结尾字符: %c\n", b) // e
```
### 2.2.9 func (r \*Reader) UnreadByte() error

**作用​**​：回退一个字节  
​**​返回值​**​：

- `error`：无前次读取时返回错误

```go
r := strings.NewReader("AB")
b, _ := r.ReadByte()
fmt.Printf("读取: %c\n", b) // A

// 回退
err := r.UnreadByte()
fmt.Println("回退错误:", err) // <nil>

// 再次读取
b, _ = r.ReadByte()
fmt.Printf("再次读取: %c\n", b) // A
```
### 2.2.10 func (r \*Reader) UnreadRune() error

​**​作用​**​：回退一个 Unicode 字符  
​**​返回值​**​：

- `error`：无前次读取或前次非 ReadRune 时返回错误

```go
r := strings.NewReader("语言")
ch, _, _ := r.ReadRune()
fmt.Printf("读取: %c\n", ch) // 语

// 回退
err := r.UnreadRune()
fmt.Println("回退错误:", err) // <nil>

// 再次读取
ch, _, _ = r.ReadRune()
fmt.Printf("再次读取: %c\n", ch) // 语
```
### 2.2.11 func (r \*Reader) WriteTo(w io.Writer) (n int64, err error)

​**​作用​**​：将剩余内容写入 io.Writer  
​**​参数​**​：`w` - 目标写入器  
​**​返回值​**​：

- `n`：写入的字节数
- `err`：写入错误

```go
r := strings.NewReader("WriteTo Example")
buf := new(bytes.Buffer)

// 写入缓冲区
n, err := r.WriteTo(buf)
fmt.Printf("写入 %d 字节, 错误: %v\n", n, err)
fmt.Println("内容:", buf.String()) // WriteTo Example

// 验证已读完
fmt.Println("剩余长度:", r.Len()) // 0
```
### 2.2.12 func (r \*Reader) Reset(s string)

​**​作用​**​：重置读取器（复用内存）  
​**​参数​**​：`s` - 新字符串

```go
r := strings.NewReader("First")
r.Read(make([]byte, 3))

r.Reset("Second")
fmt.Println("重置后长度:", r.Len()) // 6
```
## 2.3 Replacer

用于​**​高效执行字符串替换​**​的核心类型，特别适合需要同时进行多组替换的场景。

**核心优势​**​：

- ​**​高效替换​**​：使用 Trie 树或哈希表优化查找
- ​**​多组替换​**​：支持一次性定义多组替换规则
- ​**​线程安全​**​：替换操作可并发执行
### 2.3.1 func NewReplacer(oldnew ...string) \*Replacer

​**​作用​**​：创建替换器实例  
​**​参数​**​：`oldnew` - 替换规则对（必须是偶数个字符串）  
​**​返回值​**​：`*Replacer` 指针  
​**​注意事项​**​：

- 参数必须是 `old1, new1, old2, new2, ...` 格式
- 规则按添加顺序应用（非同时替换）
- 长规则优先于短规则

```go
// 创建替换器：将 "go" 替换为 "Golang"，"php" 替换为 "PHP"
r := strings.NewReplacer("go", "Golang", "php", "PHP")

// 错误示例（参数数量必须为偶数）
// r := strings.NewReplacer("go", "Golang", "php") // panic: odd argument count
```
### 2.3.2 func (r \*Replacer) Replace(s string) string

​**​作用​**​：执行字符串替换  
​**​参数​**​：`s` - 原始字符串  
​**​返回值​**​：替换后的新字符串

```go
r := strings.NewReplacer(
    "apple", "orange",
    "banana", "grape",
    "fruit", "food",
)

input := "I have an apple, a banana, and some fruit."
output := r.Replace(input)

fmt.Println(output)
// 输出: I have an orange, a grape, and some food.
```

```go
// 规则应用顺序
r := strings.NewReplacer("ab", "J", "a", "AA")  
test := "abja"  
fmt.Println(r.Replace(test)) // JjAA
// 解释: 长规则优先，先匹配"ab"->"J"，剩余"a"->"AA"
```
### 2.3.3 func (r \*Replacer) WriteString(w io.Writer, s string) (n int, err error)

​**​作用​**​：将替换结果写入 io.Writer  
​**​参数​**​：

- `w` - 目标写入器（需实现 io.Writer）
- `s` - 原始字符串  
    ​**​返回值​**​：
- `n` - 写入的字节数
- `err` - 写入错误

```go
// 创建替换器
r := strings.NewReplacer("\r\n", "\n", "\r", "\n") // 标准化换行符

// 创建缓冲区
buf := new(bytes.Buffer)

// 写入替换内容
text := "Line1\r\nLine2\rLine3"
n, err := r.WriteString(buf, text)

fmt.Printf("写入 %d 字节, 错误: %v\n", n, err)
fmt.Println("标准化内容:", buf.String())
// 输出:
// 写入 18 字节, 错误: <nil>
// 标准化内容: Line1\nLine2\nLine3
```
