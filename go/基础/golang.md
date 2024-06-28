# 1.go简介
Go 是一个开源的编程语言，它能让构造简单、可靠且高效的软件变得容易。

Go是从2007年末由Robert Griesemer, Rob Pike, Ken Thompson主持开发，后来还加入了Ian Lance Taylor, Russ Cox等人，并最终于2009年11月开源，在2012年早些时候发布了Go 1稳定版本。现在Go的开发已经是完全开放的，并且拥有一个活跃的社区。

Go 语言被设计成一门应用于搭载 Web 服务器，存储集群或类似用途的巨型中央服务器的系统编程语言。

对于高性能分布式系统领域而言，Go 语言无疑比大多数其它语言有着更高的开发效率。它提供了海量并行的支持，这对于游戏服务端的开发而言是再好不过了。

go语言具有以下特色：
- 简洁、快速、安全
- 并行、有趣、开源
- 内存管理、数组安全、编译迅速

你可以尝试编写第一个go程序，记住go程序文件以`.go`结尾
```go
package main
  
import "fmt"

func main() {
        fmt.Println("Hello,World!")
}
```
可以使用`go run`直接运行程序，也可以使用`go build`编译为二进制文件再执行。


# 2.语言结构
一般来说，go语言由以下几个部分组成：
- 包声明
- 引入包
- 函数
- 变量
- 语句/表达式
- 注释

比如说下面这段程序
```go
// 包声明 
package main 

// 导入包 
import ( 
	"fmt" 
	"math"
) 

// 常量声明 
const greeting = "Hello, World!" 

// 自定义类型和方法 
type greeter struct { 
	name string 
	} 
	
func (g greeter) greet() { 
	fmt.Println(greeting, g.name) 
	} 

func add(a int, b int) int {
	return a + b 
}

// 主函数 
func main() 
{ 
	// 变量声明和赋值 
	var s int = 42
	var g = greeter{name: "Go"} 
	// 方法调用 
	g.greet() 
}
```
- `包声明`：第一行是包声明，必须在源文件非注释的第一行指明这个文件属于哪个包，如:`package main`指明这是一个可独立执行的程序，每个Go应用程序都应该包含一个名为main的包。
- `导入包`：`import`告诉Go编译器这个程序需要使用哪些包。导入的包必须使用，否则报错。
- `常量声明`：使用`const`声明常量，常量在声明时必须赋值，且值不能更改。
- `类型声明`：`使用type`来声明一个类型。
- `方法声明`：方法是带有接收者参数的函数。在这个例子中，`greet`方法的接收者是`greeter`类型的变量`g`。
- `函数声明`：函数可以定义参数和类型，还能使用`return`返回值。
- `主函数`：_func main()_ 是程序开始执行的函数。main 函数是每一个可执行程序所必须包含的，一般来说都是在启动后第一个执行的函数（如果有 init() 函数则会先执行该函数）。
- `变量声明`：使用`var`声明一个变量，可以在函数外声明全局变量，也可以在函数内声明局部变量。也可以使用`s := 123`声明一个短变量，并由Go编译器自动推算变量类型。定义的变量必须使用，否则报错，可以使用`_ = 123`避免。
- `注释`：/\*...\*/是块注释，//是单行注释
- 当标识符（包括常量、变量、类型、函数名、结构字段等等）以一个大写字母开头，如：Group1，那么使用这种形式的标识符的对象就可以被外部包的代码所使用（客户端程序需要先导入这个包），这被称为导出（像面向对象语言中的 public）；标识符如果以小写字母开头，则对包外是不可见的，但是他们在整个包的内部是可见并且可用的（像面向对象语言中的 protected ）。
**注意：导入包的包名要使用双引号；函数的左`{`不能单独在一行；Go中一行代表一个语句结束，如果想将多个语句写在一行则必须使用`;`人为区分，但并不建议。**

# 3.基础语法
**标识符**
标识符一般用来命名变量、类型等程序实体。一个标识符由数字、字母和下划线构成，但不能由数字开头。

以下是无效的标识符：
- 1ab（数字开头）
- case（不能使用关键字）
- a+b（不能使用运算）

**字符串连接**
Go语言中的字符串连接可以通过`+`实现。
```go
package main
import "fmt"
func main() {
	fmt.Println("Google" + "Runoob")
}

# 结果：GoogleRunoob
```

**格式化字符串**
Go 语言中使用 fmt.Sprintf 或 fmt.Printf 格式化字符串并赋值给新串：
- **Sprintf** 根据格式化参数生成格式化的字符串并返回该字符串。
- **Printf** 根据格式化参数生成格式化的字符串并写入标准输出。
- 

**Sprintf示例**
```go
package main

import (
"fmt"
)

func main() {
        var a = 123
        var enddata = "2023-12-23"
        var url = "Code=%d&endDate=%s"
        var target = fmt.Sprintf(url,a,enddata)
        fmt.Println(target)
}

# Code=123&endDate=2023-12-23
```

```go
package main

import (
"fmt"
)

func main() {
        var a = 123
        var enddata = "2023-12-23"
        var url = "Code=%d&endDate=%s"
        fmt.Printf(url,a,enddata)
}

# Code=123&endDate=2023-12-23
```
**Sprintf输出后会自动换行，Printf不会。**








