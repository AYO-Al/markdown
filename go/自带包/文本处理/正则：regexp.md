`regexp` 包为 Go 语言提供了强大的正则表达式处理能力。通过编译正则表达式并使用 `Regexp` 对象，你可以轻松地进行字符串匹配、查找、替换和分割等操作。基于 [RE2 引擎](https://github.com/google/re2/wiki/Syntax)。

需要注意的是：
- **性能**：编译正则表达式是一个相对昂贵的操作，建议在初始化时编译正则表达式并复用 `Regexp` 对象。

- **并发安全**：`Regexp` 对象是并发安全的，可以在多个 goroutine 中共享使用。

**方法命名规则**​​：

∙Find(All)?(String)?(Submatch)?(Index)?：组合后缀决定返回格式。

    ∙All：返回所有非重叠匹配（n参数控制返回数量，-1返回全部）。

    ∙String：输入/输出为字符串（否则为 []byte）。

    ∙Submatch：包含捕获组（索引 0为完整匹配，1为第一组，依此类推）。

    ∙Index：返回字节索引位置（如 [start, end]）。
# 常用函数

## func Match(pattern string, b \[\]byte) (matched bool, err error)

​**​作用​**​: 检查字节切片是否包含与正则表达式匹配的子序列

**参数说明**

- `pattern string`: 正则表达式字符串
    
- `b []byte`: 要匹配的字节切片

**返回值**

- `matched bool`: 如果匹配成功返回 true，否则 false
    
- `err error`: 正则表达式解析错误或语法错误
    
**错误情况**

- 正则表达式语法错误（如未闭合的括号、无效的转义序列等）
    
- 编译正则表达式失败时返回 error
    
**注意事项**

1. 每次调用都会编译正则表达式，频繁使用时建议使用 `Compile`
    
2. 匹配是部分匹配（除非正则中包含 ^ 和 $）
    
3. 使用 RE2 语法，不支持 Perl 扩展
    
4. 适用于处理二进制数据或字节流

```go
matched, err := regexp.Match(`h`, []byte("hello")) // tre,nil
```

## func MatchReader(pattern string, r io.RuneReader) (matched bool, err error)

​**​作用​**​：从 `io.RuneReader`接口读取数据并检查是否匹配正则表达式。

**参数说明**：

- `pattern`：正则表达式字符串。
    
- `r`：实现 `io.RuneReader`接口的数据源（如文件流、网络流）。
    

**返回值**：

同 `Match`函数。

**注意事项**：

1. ​**​适用场景​**​：适合流式数据或大文本，避免一次性加载内存
    
2. ​**​性能与限制​**​：同 `Match`，每次调用编译正则表达式。

```go
    pattern := "云长"
    r := bytes.NewReader([]byte("关羽关云长")) // 创建 RuneReader
    matched, err := regexp.MatchReader(pattern, r) // true,nil
```
## func MatchString(pattern string, s string) (matched bool, err error)

同`Match`。
## func QuoteMeta(s string) string

​**​作用​**​：转义字符串 `s`中的所有正则元字符（如 `.`、`*`、`?`），使其成为字面字符串。

**参数说明**：

- `s`：待转义的字符串（如 `"file.txt"`）。    

**返回值**：

- 转义后的字符串（如 `"file\.txt"`）。
    
**注意事项**：

1.  ​**​关键用途​**​：当用户输入需作为正则字面量时，必须转义以避免语法错误。

2. ​**​转义范围​**​：包括 `\.+*?()|[]{}^$`等元字符

```go
s := "file.txt*"  
fmt.Println(regexp.QuoteMeta(s)) // file\.txt
```
# 类型
## Regexp

`Regexp`类型代表一个编译后的正则表达式，它是线程安全的，可以在多个 goroutine 中并发使用。所有正则表达式操作都通过 `Regexp`类型的方法进行。
### 编译函数

#### func Compile(expr string) (\*Regexp, error)

​**​作用​**​: 编译正则表达式并返回 Regexp 对象

**参数说明**

- `expr string`: 正则表达式字符串
    
**返回值**

-  `*Regexp`: 编译后的正则表达式对象
    
- `error`: 编译错误（正则表达式语法错误）
    
**错误情况**

-  正则表达式语法错误（如未闭合的括号、无效的转义序列等）
    
**注意事项**

1.  如果正则表达式编译失败，返回错误
    
2. 相比 `MustCompile`，更适合处理可能失败的正则表达式
    
3. 编译后的 Regexp 对象可以重复使用，提高性能

```go
package main

import (
    "fmt"
    "regexp"
)

func main() {
    // 编译一个简单的正则表达式
    re, err := regexp.Compile(`go(\d+)`)
    if err != nil {
        fmt.Println("编译错误:", err)
        return
    }
    
    // 使用编译后的正则表达式
    match := re.FindString("golang go123 go456")
    fmt.Println("找到匹配:", match)
    
    // 尝试编译无效的正则表达式
    _, err = regexp.Compile(`go(`) // 缺少闭合括号
    if err != nil {
        fmt.Println("预期错误:", err)
    }
}

/**
找到匹配: go123
预期错误: error parsing regexp: missing closing ): `go(`
*/
```
#### func CompilePOSIX(expr string) (\*Regexp, error)

​**​作用​**​: 使用 POSIX ERE 语法编译正则表达式

**参数说明**

- `expr string`: POSIX ERE 语法的正则表达式
    
**返回值**

-  `*Regexp`: 编译后的正则表达式对象
    
- `error`: 编译错误
    
**注意事项**

1.  使用 POSIX ERE (Extended Regular Expression) 语法
    
2. 匹配语义与标准正则表达式略有不同（最长左匹配）
    
3. 性能可能略低于标准正则表达式

```go
package main

import (
    "fmt"
    "regexp"
)

func main() {
    // 使用 POSIX 语法编译正则表达式
    re, err := regexp.CompilePOSIX(`(go|golang)`)
    if err != nil {
        fmt.Println("编译错误:", err)
        return
    }
    
    // 使用编译后的正则表达式
    matches := re.FindAllString("golang is better than go", -1)
    fmt.Println("所有匹配:", matches)
    
    // 比较 POSIX 和标准正则表达式的差异
    stdRe, _ := regexp.Compile(`(go|golang)`)
    posixRe, _ := regexp.CompilePOSIX(`(go|golang)`)
    
    stdMatch := stdRe.FindString("golang")
    posixMatch := posixRe.FindString("golang")
    
    fmt.Printf("标准匹配: %s, POSIX匹配: %s\n", stdMatch, posixMatch)
}

/**
所有匹配: [golang go]
标准匹配: go, POSIX匹配: golang
*/
```
#### func MustCompile(str string) \*Regexp

​**​作用​**​: 编译正则表达式，如果失败则 panic

**参数说明**

-  `str string`: 正则表达式字符串
    
**返回值**
- `*Regexp`: 编译后的正则表达式对象
    
**注意事项**

1.     如果正则表达式无效，会引发 panic
    
2. 适合在程序初始化时使用已知正确的正则表达式
    
3. 比 `Compile`更简洁，但不够安全
#### func MustCompilePOSIX(str string) \*Regexp

结合了 `CompilePOSIX`和 `MustCompile`的特性.
### 匹配方法

#### func (re \*Regexp) Match(b \[\]byte) bool

​**​作用​**​: 检查字节切片是否匹配正则表达式

#### 参数说明

-  `b []byte`: 要检查的字节切片
    
**返回值**

-     `bool`: 如果匹配返回 true，否则 false

```go
package main

import (
    "fmt"
    "regexp"
)

func main() {
    re := regexp.MustCompile(`^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$`)
    
    // 检查字节切片是否匹配电子邮件格式
    email := []byte("user@example.com")
    isValid := re.Match(email)
    fmt.Printf("%s 是有效的电子邮件: %v\n", string(email), isValid)
    
    // 检查无效电子邮件
    invalidEmail := []byte("invalid.email")
    isValid = re.Match(invalidEmail)
    fmt.Printf("%s 是有效的电子邮件: %v\n", string(invalidEmail), isValid)
}

/**
user@example.com 是有效的电子邮件: true
invalid.email 是有效的电子邮件: false
*/
```
#### func (re \*Regexp) MatchReader(r io.RuneReader) bool

​**​作用​**​: 从 RuneReader 读取数据并检查是否匹配

**参数说明**

- `r io.RuneReader`: 实现 io.RuneReader 接口的数据源
    
**返回值**

-  `bool`: 如果匹配返回 true，否则 false

#### func (re \*Regexp) MatchString(s string) bool
### 查找方法
#### func (re \*Regexp) Find(b \[\]byte) \[\]byte

**作用​**​: 在字节切片中查找第一个匹配项

**参数说明**

-  `b []byte`: 要搜索的字节切片
    
**返回值**

-    `[]byte`: 第一个匹配项的字节切片，如果没有匹配返回 nil

```go
re, err := regexp.Compile(`(go|golang)`)  
if err == nil {  
    fmt.Println(string(re.Find([]byte("hello golang"))))  // go
} else {  
    fmt.Println(err)  
} 
```
#### func (re \*Regexp) FindAll(b \[\]byte, n int) \[\]\[\]byte

​**​作用​**​: 在字节切片中查找所有匹配项

**参数说明**

-  `b []byte`: 要搜索的字节切片
    
- `n int`: 最多返回的匹配数量，-1 表示返回所有匹配
    
**返回值**

-  `[][]byte`: 所有匹配项的字节切片数组

```go
  
    re, err := regexp.Compile(`(go|golang)`)  
    b := re.FindAll([]byte("hello go golang "), -1)  
    if err == nil {  
       for i := 0; i < len(b); i++ {  
          fmt.Println(string(b[i]))  // go go
       }  
    } else {  
       fmt.Println(err)  
    }
```
#### func (re \*Regexp) FindString(s string) string

​**​作用​**​: 在字符串中查找第一个匹配项

**参数说明**

-  `s string`: 要搜索的字符串
    
**返回值**

-  `string`: 第一个匹配项的字符串，如果没有匹配返回空字符串
### 替换方法

#### func (re \*Regexp) ReplaceAll(src, repl \[\]byte) \[\]byte

​**​作用​**​: 替换所有匹配项（字节切片版本）

**参数说明**

-  `src []byte`: 源字节切片
    
- `repl []byte`: 替换内容
    
**返回值**

-  `[]byte`: 替换后的字节切片
    
**注意事项**

1. 在替换字符串中可以使用 `$1`, `$2`等引用捕获组
    
2. 使用 `$0`引用整个匹配项

```go
package main

import (
    "fmt"
    "regexp"
)

func main() {
    re := regexp.MustCompile(`(\d+)-(\d+)-(\d+)`) // 匹配日期格式 YYYY-MM-DD
    
    // 替换日期格式
    src := []byte("日期: 2023-04-15, 另一个日期: 2022-12-25")
    repl := []byte("$2/$3/$1") // 改为 MM/DD/YYYY 格式
    result := re.ReplaceAll(src, repl)
    fmt.Printf("替换结果: %s\n", string(result))
    
    // 使用 $0 引用整个匹配
    repl2 := []byte("[$0]") // 给日期加上方括号
    result2 := re.ReplaceAll(src, repl2)
    fmt.Printf("加括号结果: %s\n", string(result2))
}

/**
替换结果: 日期: 04/15/2023, 另一个日期: 12/25/2022
加括号结果: 日期: [2023-04-15], 另一个日期: [2022-12-25]
*/
```
#### func (re \*Regexp) ReplaceAllString(src, repl string) string

​**​作用​**​: 替换所有匹配项（字符串版本）

**参数说明**

-  `src string`: 源字符串
    
- `repl string`: 替换内容
    
**返回值**

-  `string`: 替换后的字符串

```go
package main

import (
    "fmt"
    "regexp"
)

func main() {
    re := regexp.MustCompile(`(\w+)=(\w+)`) // 匹配键值对
    
    // 替换键值对格式
    src := "name=John age=30 city=NewYork"
    repl := "$1: $2" // 改为 key: value 格式
    result := re.ReplaceAllString(src, repl)
    fmt.Printf("替换结果: %s\n", result)
    
    // 使用命名捕获组（需要先定义）
    re2 := regexp.MustCompile(`(?P<key>\w+)=(?P<value>\w+)`)
    repl2 := "${key}: ${value}" // 使用命名引用
    result2 := re2.ReplaceAllString(src, repl2)
    fmt.Printf("命名替换结果: %s\n", result2)
}

/**
替换结果: name: John age: 30 city: NewYork
命名替换结果: name: John age: 30 city: NewYork
*/
```
### 其他重要方法

#### func (re \*Regexp) Split(s string, n int) \[\]string

​**​作用​**​: 使用正则表达式分割字符串

**参数说明**

-  `s string`: 要分割的字符串
    
- `n int`: 最多分割的次数，-1 表示不限制
    
**返回值**

- `[]string`: 分割后的字符串数组

```go
package main

import (
    "fmt"
    "regexp"
)

func main() {
    re := regexp.MustCompile(`\s*,\s*`) // 匹配逗号及周围的可选空格
    
    // 分割字符串
    text := "apple, banana,  cherry, date"
    parts := re.Split(text, -1)
    fmt.Printf("分割结果: %v\n", parts)
    
    // 限制分割次数
    limitedParts := re.Split(text, 2)
    fmt.Printf("限制分割次数: %v\n", limitedParts)
    
    // 使用复杂正则分割
    re2 := regexp.MustCompile(`[,;]\s*`) // 匹配逗号或分号及后续空格
    text2 := "apple; banana, cherry; date"
    parts2 := re2.Split(text2, -1)
    fmt.Printf("多分隔符分割: %v\n", parts2)
}

/**
分割结果: [apple banana cherry date]
限制分割次数: [apple banana,  cherry, date]
多分隔符分割: [apple banana cherry date]
*/
```
#### func (re \*Regexp) SubexpNames() \[\]string

​**​作用​**​: 返回捕获组的名称

SubexpNames返回此正则表达式中的括号子表达式的名称。第一个子表达式的名称是names\[1\]，因此如果m是一个匹配切片，则m\[i\]的名称是SubexpNames()\[i\]。由于整个正则表达式不能命名，names\[0\]始终是空字符串。该切片不应被修改。

**返回值**

-  `[]string`: 捕获组名称的数组，未命名组为空字符串

```go
package main

import (
    "fmt"
    "regexp"
)

func main() {
    // 包含命名和未命名捕获组的正则表达式
    re := regexp.MustCompile(`(?P<year>\d+)-(?P<month>\d+)-(\d+)`) // 最后一个组未命名
    
    // 获取捕获组名称
    names := re.SubexpNames()
    fmt.Printf("捕获组名称: %v\n", names)
    
    // 使用捕获组名称
    text := "2023-04-15"
    match := re.FindStringSubmatch(text) // [2023-04-15 2023 04 15]
    for i, name := range names {
        if name != "" {
            fmt.Printf("%s: %s\n", name, match[i])
        } else if i > 0 {
            fmt.Printf("未命名组%d: %s\n", i, match[i])
        }
    }
}

/**
捕获组名称: [ year month ]
年: 2023
月: 04
未命名组2: 15
*/
```
#### func (re \*Regexp) NumSubexp() int

​**​作用​**​: 返回捕获组的数量

#### 返回值

- `int`: 捕获组的数量