`regexp` 包为 Go 语言提供了强大的正则表达式处理能力。通过编译正则表达式并使用 `Regexp` 对象，你可以轻松地进行字符串匹配、查找、替换和分割等操作。

需要注意的是：
- **性能**：编译正则表达式是一个相对昂贵的操作，建议在初始化时编译正则表达式并复用 `Regexp` 对象。

- **并发安全**：`Regexp` 对象是并发安全的，可以在多个 goroutine 中共享使用。
# 常用函数

`Regexp`包中常用函数有Match和MatchString，这两个函数逻辑都差不多，都是在字符串中查找对应正则，返回是否查找成功。

```go
package function

import (
	"fmt"
	"regexp"
)

func Check_type(v interface{}, p string) interface{} {
	switch t := v.(type) {
	case []byte:
		v, ok := v.([]byte)
		if ok {
			return match_byte_find(p, v)
		}
	case string:
		v, ok := v.(string)
		if ok {
			return match_string_find(p, v)
		}
	default:
		fmt.Println(t)
	}
	return false
}

func match_byte_find(p string, v []byte) bool {
	ok, err := regexp.Match(p, v)
	if err != nil {
		fmt.Println(err)
		return ok
	}
	return ok
}

func match_string_find(p string, v string) bool {
	ok, err := regexp.MatchString(p, v)
	if err != nil {
		fmt.Println(err)
	}
	return ok
}

```

# Regexp对象

Regexp是编译后的正则表达式的表示。

Regexp包提供了四个函数来创建Regexp对象。regexp.Compile，regexp.MustCompile，regexp.CompilePOSIX，regexp.MustCompilePOSIX。

```go
func Compile(expr string) (*Regexp, error)

func CompilePOSIX(expr string) (*Regexp, error)

func MustCompile(str string) *Regexp

func MustCompilePOSIX(str string) *Regexp

```

这四个函数都接受一个正则表达式字符串，`Compile`这两个函数如果匹配不到则返回error，`MustCompile`这两个函数则直接引发恐慌。

`POSIX`这两个函数，使用 POSIX 兼容的正则表达式语法，使用最长匹配优先策略，可能稍慢一些。而其他两个函数使用 Perl 兼容的正则表达式语法，通常更快，使用贪婪匹配。
## 匹配

`Regexp`对象也提供了Match和MatchString方法用来判断字符串是否匹配正则表达式。
## 查找

```go
// `FindString` 方法用于查找第一个匹配的字符串。
func (re *Regexp) Find(b []byte) []byte

// `FindAllString` 方法用于查找所有匹配的字符串，并返回一个字符串切片。可以指定返回的最大匹配数，-1 表示返回所有匹配项。
func (re *Regexp) FindAll(b []byte, n int) [][]byte

// `FindStringIndex` 方法用于查找第一个匹配的字符串，并返回其在原字符串中的起始和结束位置。
func (re *Regexp) FindStringIndex(s string) (loc []int)

// `FindAllStringIndex` 方法用于查找所有匹配的字符串，并返回它们在原字符串中的起始和结束位置。可以指定返回的最大匹配数，-1 表示返回所有匹配项。
func (re *Regexp) FindAllStringIndex(s string, n int) [][]int

// `FindStringSubmatch` 方法用于查找第一个匹配的字符串，并返回匹配的子字符串切片。
func (re *Regexp) FindStringSubmatch(s string) []string

// `FindAllStringSubmatch` 方法用于查找所有匹配的字符串，并返回匹配的子字符串切片。可以指定返回的最大匹配数，-1 表示返回所有匹配项。
func (re *Regexp) FindAllStringSubmatch(s string, n int) [][]string

```
## 替换

```go
// `ReplaceAllString` 方法用于替换所有匹配的字符串。
// 能使用$1使用捕获组
// 还能使用?P<name>给捕获组命名
func (re *Regexp) ReplaceAllString(src, repl string) string

func main() {
	re := regexp.MustCompile(`a(x*)b`)
	fmt.Println(re.ReplaceAllString("-ab-axxb-", "T"))
	fmt.Println(re.ReplaceAllString("-ab-axxb-", "$1"))
	fmt.Println(re.ReplaceAllString("-ab-axxb-", "$1W"))
	fmt.Println(re.ReplaceAllString("-ab-axxb-", "${1}W"))

	re2 := regexp.MustCompile(`a(?P<1W>x*)b`)
	fmt.Printf("%s\n", re2.ReplaceAllString("-ab-axxb-", "$1W"))
	fmt.Println(re.ReplaceAllString("-ab-axxb-", "${1}W"))

}
/*
-T-T-
--xx-
---
-W-xxW-
--xx-
-W-xxW-
*/

// `ReplaceAllStringFunc` 方法用于替换所有匹配的字符串，并允许你通过一个自定义函数来决定如何替换每个匹配项。这个方法非常灵活，因为你可以在替换过程中执行复杂的逻辑。
func (re *Regexp) ReplaceAllStringFunc(src string, repl func(string) string) string
```
## 分割

```go
// `Split` 方法用于根据正则表达式分割字符串，并返回一个字符串切片。可以指定返回的最大分割数，-1 表示返回所有分割项。
func (re *Regexp) Split(s string, n int) []string
```