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


# 2.基础语法
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
import ( "fmt" ) 

// 常量声明 
const greeting = "Hello, World!" 

// 自定义类型和方法 
type greeter struct { 
	name string 
	} 
	
func (g greeter) greet() { 
	fmt.Println(greeting, g.name) 
	} 
	
// 主函数 
func main() 
{ 
	// 变量声明和赋值 
	var g = greeter{name: "Go"} 
	// 方法调用 
	g.greet() 
}
```
- 包声明：