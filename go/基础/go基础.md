# go简介
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
  
import (
   . "fmt" // 在使用时不需要写包名
   f "fmt" // 在使用时可以使用别名
   _ "fmt" // 不使用该包的函数，而是调用init函数
)

func main() {
        fmt.Println("Hello,World!")
}
```
可以使用`go run`直接运行程序，也可以使用`go build`编译为二进制文件再执行。

也可以在包路径下使用`go mod init 包名`，然后使用`go mod tidy`更新依赖，使用`go install`安装可执行文件。
# go安装配置

先在Go官网上https://go.dev/dl/下载对应的压缩包，然后把压缩包解压到指定目录。接来下设置Go环境变量：

 - GOROOT：Go语言安装根目录的路径，也就是GO语言的安装路径。一般是自动设置的，只有在安装了多版本或者go的安装路径不在默认位置需要指定GOROOT。
 
- GOPATH：若干工作区目录的路径。
    - scr：里面每一个子目录都是一个包，包里面是源码。
    - pkg：编译后生成的包的位置。
    - bin：生成的可执行文件位置。

- GOBIN：`GOBIN` 指定了 `go install` 命令安装可执行文件的目录。如果未设置 `GOBIN`，则默认安装到 `GOPATH/bin` 目录。

- PATH：环境变量路径。

注意把export语句写到`profile`/`.bashrc`文件中，否则只对当前会话有效。
# go执行原理及相关命令

## 命令源码文件

声明自己属于 main 代码包、包含无参数声明和结果声明的 main 函数。

命令源码文件被安装以后，GOPATH 如果只有一个工作区，那么相应的可执行文件会被存放当前工作区的 bin 文件夹下；如果有多个工作区，就会安装到 GOBIN 指向的目录下。

命令源码文件是 Go 程序的入口。

同一个代码包中最好也不要放多个命令源码文件。多个命令源码文件虽然可以分开单独 go run 运行起来，但是无法通过 go build 和 go install。
## 库源码文件

库源码文件就是不具备命令源码文件上述两个特征的源码文件。存在于某个代码包中的普通的源码文件。

库源码文件被安装后，相应的归档文件（.a 文件）会被存放到当前工作区的 pkg 的平台相关目录下。
## 测试源码文件

名称以 _test.go 为后缀的代码文件，并且必须包含 Test 或者 Benchmark 名称前缀的函数：

```
func TestXXX( t *testing.T) {

}
```

名称以 Test 为名称前缀的函数，只能接受 *testing.T 的参数，这种测试函数是功能测试函数。

```
func BenchmarkXXX( b *testing.B) {

}
```

名称以 Benchmark 为名称前缀的函数，只能接受 *testing.B 的参数，这种测试函数是性能测试函数。
## Go常用命令

我们可以打开终端输入：go help即可看到Go的这些命令以及简介。

```
	bug         start a bug report
	build       compile packages and dependencies
	clean       remove object files and cached files
	doc         show documentation for package or symbol
	env         print Go environment information
	fix         update packages to use new APIs
	fmt         gofmt (reformat) package sources
	generate    generate Go files by processing source
	get         download and install packages and dependencies
	install     compile and install packages and dependencies
	list        list packages or modules
	mod         module maintenance
	run         compile and run Go program
	test        test packages
	tool        run specified go tool
	version     print Go version
	vet         report likely mistakes in packages
```

其中和编译相关的有build、get、install、run这4个。接下来就依次看看这四个的作用。

且各个命令通用的命令标记，以下这些命令都可适用的：

| 名称    | 说明                                                                                                  |
| ----- | --------------------------------------------------------------------------------------------------- |
| -a    | 用于强制重新编译所有涉及的 Go 语言代码包（包括 Go 语言标准库中的代码包），即使它们已经是最新的了。该标记可以让我们有机会通过改动底层的代码包做一些实验。                    |
| -n    | 使命令仅打印其执行过程中用到的所有命令，而不去真正执行它们。如果不只想查看或者验证命令的执行过程，而不想改变任何东西，使用它正好合适。                                 |
| -race | 用于检测并报告指定 Go 语言程序中存在的数据竞争问题。当用 Go 语言编写并发程序的时候，这是很重要的检测手段之一。                                         |
| -v    | 用于打印命令执行过程中涉及的代码包。这一定包括我们指定的目标代码包，并且有时还会包括该代码包直接或间接依赖的那些代码包。这会让你知道哪些代码包被执行过了。                       |
| -work | 用于打印命令执行时生成和使用的临时工作目录的名字，且命令执行完成后不删除它。这个目录下的文件可能会对你有用，也可以从侧面了解命令的执行过程。如果不添加此标记，那么临时工作目录会在命令执行完毕前删除。 |
| -x    | 使命令打印其执行过程中用到的所有命令，并同时执行它们。                                                                         |
## run 

专门用来运行命令源码文件的命令，**注意，这个命令不是用来运行所有 Go 的源码文件的！**

go run 命令只能接受一个命令源码文件以及若干个库源码文件（必须同属于 main 包）作为文件参数，且**不能接受测试源码文件**。它在执行时会检查源码文件的类型。如果参数中有多个或者没有命令源码文件，那么 go run 命令就只会打印错误提示信息并退出，而不会继续执行。

想知道`go run`命令具体做了什么事情，可以使用`-n`选项查看。

`go run`命令在第二次执行的时候，如果发现导入的代码包没有发生变化，那么`go run`不会再次编译这个导入的代码包，而是直接静态链接过来。

## build

`go build`命令主要是用于测试编译，在包的编译过程中，若有必要，会同时编译与之相关的包。

- 如果是普通包，执行这个命令不会产生任何文件。

- 如果是main包，当只执行该命令后，会在当前目录下生成一个可执行文件。

- 如果某个文件夹下有多个文件，而你只想编译其中一个文件，可以在命令之后加上文件名。

- 也可以指定编译输出的文件名，只需要加上-o选项即可。否则默认使用package包名或者是第一个源文件名。
## install

`go install`命令是用来编译并安装代码包或源码文件的。

`go install`命令实际上做了两步操作：一是生成结果文件(可执行文件或.a包)，二是会把编译好的文件移动到指定的目录中。

可执行文件：一般是go install带main函数的go文件产生的，有函数入口，所以可以直接运行。

.a应用包：一般是go install不包含main函数的go文件产生的，没有函数入口，只能被调用。
## get

`go get`命令是用来从远程仓库上下载并安装代码包。**注意：go get命令会把当前的代码包下载到$GOPATH中的第一个工作区的src目录中，并安装。**

`go get`有一个智能下载的功能，在使用它检出货更新代码包之后，它会寻找与本地已安装Go语言的版本号相对应的标签或分支。

常用选项如下

| 命令        | 说明                                                                                   |
| --------- | ------------------------------------------------------------------------------------ |
| -d        | 让命令程序只执行下载动作，而不执行安装动作                                                                |
| -f        | 仅在使用-u选项时才有效。该标记会让命令程序忽略掉对已下载代码包的导入路径的检查。如果下载并安装的代码包所属的项目是你从别人那里fork过来的，那么这么做就尤为重要了。 |
| -fix      | 让命令程序在下载代码包后先执行修正动作，而后再进行编译和安装。                                                      |
| -insecure | 允许命令程序使用非安全的scheme去下载指定的代码包。                                                         |
| -t        | 让命令程序同时下载并安装指定的代码包中的测试源码文件中依赖的代码包。                                                   |
| -u        | 让命令利用网络来更新已有代码包及其依赖包。默认情况下，该命令只会从网络上下载本地不存在的代码包，而不会更新已有的代码包。                         |
| -x        | 打印输出命令所执行的操作。                                                                        |
## 其他命令

| 命令         | 说明                                                                                      |
| ---------- | --------------------------------------------------------------------------------------- |
| go clean   | 移除当前源码包里面编译生成的文件                                                                        |
| go fmt     | 格式化所有写好的代码文件，-w选项修改文件                                                                   |
| go test    | 自动读取源码目录下名为*_test.go文件，生成并且允许测试用的可执行文件。                                                 |
| go doc     | 查看对应包的使用文档，`go doc builtin`；查看对应函数的，`go doc fmt Printf`；查看对应代码，`go doc -src fmt Printf` |
| go fix     | 用来修复以前老版本的代码到新版本                                                                        |
| go version | 查看go当前版本                                                                                |
| go env     | 查看当前go的环境变量                                                                             |
| go list    | 列出当前全部安装的package                                                                        |
# 编码规范

本规范旨在为日常Go项目开发提供一个代码的规范指导，方便团队形成一个统一的代码风格，提高代码的可读性，规范性和统一性。本规范将从命名规范，注释规范，代码风格和 Go 语言提供的常用的工具这几个方面做一个说明。该规范参考了 go 语言官方代码的风格制定。

##  命名规范

命名是代码规范中很重要的一部分，统一的命名规则有利于提高的代码的可读性，好的命名仅仅通过命名就可以获取到足够多的信息。

Go在命名时以字母a到Z或a到Z或下划线开头，后面跟着零或更多的字母、下划线和数字(0到9)。Go不允许在命名时中使用@、$和%等标点符号。Go是一种区分大小写的编程语言。因此，Manpower和manpower是两个不同的命名。

> 1. 当命名（包括常量、变量、类型、函数名、结构字段等等）以一个大写字母开头，如：Group1，那么使用这种形式的标识符的对象就**可以被外部包的代码所使用**（客户端程序需要先导入这个包），这被称为导出（像面向对象语言中的 public）； > 2. **命名如果以小写字母开头，则对包外是不可见的，但是他们在整个包的内部是可见并且可用的**（像面向对象语言中的 private ）

### 包命名：package

保持package的名字和目录保持一致，尽量采取有意义的包名，简短，有意义，尽量和标准库不要冲突。包名应该为**小写**单词，不要使用下划线或者混合大小写。

```
package demo

package main
```

### 文件命名

尽量采取有意义的文件名，简短，有意义，应该为**小写**单词，使用**下划线**分隔各个单词。

```
my_test.go
```

### 结构体命名

- 采用驼峰命名法，首字母根据访问控制大写或者小写
    
- struct 申明和初始化格式采用多行，例如下面：
    

```
// 多行申明
type User struct{
    Username  string
    Email     string
}

// 多行初始化
u := User{
    Username: "astaxie",
    Email:    "astaxie@gmail.com",
}

```

### 接口命名

- 命名规则基本和上面的结构体类型
- 单个函数的结构名以 “er” 作为后缀，例如 Reader , Writer 。

```
type Reader interface {
        Read(p []byte) (n int, err error)
}

```

### 变量命名

- 和结构体类似，变量名称一般遵循驼峰法，首字母根据访问控制原则大写或者小写，但遇到特有名词时，需要遵循以下规则：
    - 如果变量为私有，且特有名词为首个单词，则使用小写，如 apiClient
    - 其它情况都应当使用该名词原有的写法，如 APIClient、repoID、UserID
    - 错误示例：UrlArray，应该写成 urlArray 或者 URLArray
- 若变量类型为 bool 类型，则名称应以 Has, Is, Can 或 Allow 开头

```
var isExist bool
var hasConflict bool
var canManage bool
var allowGitHook bool
```

### 常量命名

常量均需使用全部大写字母组成，并使用下划线分词

```
const APP_VER = "1.0"
```

如果是枚举类型的常量，需要先创建相应类型：

```
type Scheme string

const (
    HTTP  Scheme = "http"
    HTTPS Scheme = "https"
)

```

### 关键字

下面的列表显示了Go中的保留字。这些保留字不能用作常量或变量或任何其他标识符名称。

![guanjianzi](http://7xtcwd.com1.z0.glb.clouddn.com/guanjianzi.jpg)

## 注释

Go提供C风格的`/* */`块注释和C ++风格的`//`行注释。行注释是常态；块注释主要显示为包注释，但在表达式中很有用或禁用大量代码。

- 单行注释是最常见的注释形式，你可以在任何地方使用以 // 开头的单行注释
- 多行注释也叫块注释，均已以 /* 开头，并以 */ 结尾，且不可以嵌套使用，多行注释一般用于包的文档描述或注释成块的代码片段

go 语言自带的 godoc 工具可以根据注释生成文档，生成可以自动生成对应的网站（ [golang.org](http://golang.org/) 就是使用 godoc 工具直接生成的），注释的质量决定了生成的文档的质量。每个包都应该有一个包注释，在package子句之前有一个块注释。对于多文件包，包注释只需要存在于一个文件中，任何一个都可以。包评论应该介绍包，并提供与整个包相关的信息。它将首先出现在`godoc`页面上，并应设置下面的详细文档。

详细的如何写注释可以 参考：<[http://golang.org/doc/effective_go.html#commentary](http://golang.org/doc/effective_go.html#commentary)>

### 包注释

每个包都应该有一个包注释，一个位于package子句之前的块注释或行注释。包如果有多个go文件，只需要出现在一个go文件中（一般是和包同名的文件）即可。 包注释应该包含下面基本信息(请严格按照这个顺序，简介，创建人，创建时间）：

- 包的基本简介（包名，简介）
- 创建者，格式： 创建人： rtx 名
- 创建时间，格式：创建时间： yyyyMMdd

例如 util 包的注释示例如下

```
// util 包， 该包包含了项目共用的一些常量，封装了项目中一些共用函数。
// 创建人： hanru
// 创建时间： 20190419
```

### 结构（接口）注释

每个自定义的结构体或者接口都应该有注释说明，该注释对结构进行简要介绍，放在结构体定义的前一行，格式为： 结构体名， 结构体说明。同时结构体内的每个成员变量都要有说明，该说明放在成员变量的后面（注意对齐），实例如下：

```
// User ， 用户对象，定义了用户的基础信息
type User struct{
    Username  string // 用户名
    Email     string // 邮箱
}
```

### 函数（方法）注释

每个函数，或者方法（结构体或者接口下的函数称为方法）都应该有注释说明，函数的注释应该包括三个方面（严格按照此顺序撰写）：

- 简要说明，格式说明：以函数名开头，“，”分隔说明部分
- 参数列表：每行一个参数，参数名开头，“，”分隔说明部分
- 返回值： 每行一个返回值

示例如下：

```
// NewtAttrModel ， 属性数据层操作类的工厂方法
// 参数：
//      ctx ： 上下文信息
// 返回值：
//      属性操作类指针
func NewAttrModel(ctx *common.Context) *AttrModel {
}
```

### 代码逻辑注释

对于一些关键位置的代码逻辑，或者局部较为复杂的逻辑，需要有相应的逻辑说明，方便其他开发者阅读该段代码，实例如下：

```
// 从 Redis 中批量读取属性，对于没
```
# 代码风格
## 语句的结尾

Go语言中是不需要使用结尾符的，默认一行就是一条数据；但如果打算将多个语句写在一行，则必须使用分号
## 括号和空格

括号和空格方面，go会强制左大括号不换行，否则会报错；所有的运算符和操作数之间要留空格。

# 变量的使用

##  什么是变量

变量是为存储特定类型的值而提供给内存位置的名称。在go中声明变量有多种语法。

所以变量的本质就是一小块内存，用于存储数据，在程序运行过程中数值可以改变

## 声明变量

var名称类型是声明单个变量的语法。

> 以字母或下划线开头，由一个或多个字母、数字、下划线组成

声明一个变量

第一种，指定变量类型，声明后若不赋值，使用默认值

```
var name type
name = value
```

第二种，根据值自行判定变量类型(类型推断Type inference)

如果一个变量有一个初始值，Go将自动能够使用初始值来推断该变量的类型。因此，如果变量具有初始值，则可以省略变量声明中的类型。

```
var name = value
```

第三种，省略var, 注意 :=左侧的变量不应该是已经声明过的(多个变量同时声明时，至少保证一个是新变量)，否则会导致编译错误(简短声明).且简短声明不能声明全局变量。

```
name := value

// 例如
var a int = 10
var b = 10
c : = 10
```

> 这种方式它只能被用在函数体内，而不可以用于全局变量的声明与赋值

示例代码：

```
package main
var a = "Hello"
var b string = "World"
var c bool

func main(){
    println(a, b, c)
}
```

运行结果：

```
Hello World false
```

### 多变量声明

第一种，以逗号分隔，声明与赋值分开，若不赋值，存在默认值

```
var name1, name2, name3 type
name1, name2, name3 = v1, v2, v3
```

第二种，直接赋值，下面的变量类型可以是不同的类型

```
var name1, name2, name3 = v1, v2, v3
```

第三种，集合类型

```
var (
    name1 type1
    name2 type2
)
```

## 注意事项

如果在相同的代码块中，我们不可以再次对于相同名称的变量使用初始化声明，例如：a := 20 就是不被允许的，编译器会提示错误 no new variables on left side of :=，但是 a = 20 是可以的，因为这是给相同的变量赋予一个新的值。

如果你在定义变量 a 之前使用它，则会得到编译错误 undefined: a。如果你声明了一个局部变量却没有在相同的代码块中使用它，同样会得到编译错误，例如下面这个例子当中的变量 a：

```
func main() {
   var a string = "abc"
   fmt.Println("hello, world")
}
```

尝试编译这段代码将得到错误 a declared and not used

此外，单纯地给 a 赋值也是不够的，这个值必须被使用，所以使用

在同一个作用域中，已存在同名的变量，则之后的声明初始化，则退化为赋值操作。但这个前提是，最少要有一个新的变量被定义，且在同一作用域，例如，下面的y就是新定义的变量

```
package main

import (
	"fmt"
)

func main() {
	x := 140
	fmt.Println(&x)
	x, y := 200, "abc"
	fmt.Println(&x, x)
	fmt.Print(y)
}
```

运行结果：

```
0xc04200a2b0
0xc04200a2b0 200
abc
```
# 常量

常量是一个简单值的标识符，在程序运行时，不会被修改的量。**常量不被引用也不会报错**。

常量中的数据类型只可以是布尔型、数字型（整数型、浮点型和复数）和字符串型。

**常量必须赋值才能使用，没有默认值。**

常量的定义格式：
```go
const identifier [type] = value
```

你可以省略类型说明符 [type]，因为编译器可以根据变量的值来推断其类型。

- 显式类型定义： `const b string = "abc"`  
    
- 隐式类型定义： `const b = "abc"`

多个相同类型的声明可以简写为：

```go
const c_name1, c_name2 = value1, value2
```

以下实例演示了常量的应用：

```go
package main  
  
import "fmt"  
  
func main() {  
   const LENGTH int = 10  
   const WIDTH int = 5    
   var area int  
   const a, b, c = 1, false, "str" //多重赋值  
  
   area = LENGTH * WIDTH  
   fmt.Printf("面积为 : %d", area)  
   println()  
   println(a, b, c)    
}  
```

以上实例运行结果为：

```go
面积为 : 50
1 false str
```

常量还可以用作枚举，在枚举中，**如果一个常量没有赋值，默认值和上一个非空常量值一样**：

```go
const (
    Unknown = 0
    Female = 1
    Male = 2
)

const (
    a = 1
    b = 2
    c = 3
)
```

数字 0、1 和 2 分别代表未知性别、女性和男性。

常量可以用len(), cap(), unsafe.Sizeof()函数计算表达式的值。常量表达式中，函数必须是内置函数，否则编译不过

```go
package main  
  
import "unsafe"  
const (  
    a = "abc"  
    b = len(a)  
    c = unsafe.Sizeof(a)  
)  
  
func main(){  
    println(a, b, c)  
}  
```
以上实例运行结果为：

```go
abc 3 16
```
## iota

iota，特殊常量，可以认为是一个可以被编译器修改的常量。是一个无类型的整数常量，通常用于生成一组相关的整数常量。

iota 在 const关键字出现时将被重置为 0(const 内部的第一行之前)，const 中每新增一行常量声明将使 iota 计数一次(iota 可理解为 const 语句块中的行索引)。

iota 可以被用作枚举值：

```go
const (   // 在一个新的const关键字中会被重置为0
    a = iota
    b = iota
    c = iota
)
```

第一个 iota 等于 0，每当 iota 在新的一行被使用时，它的值都会自动加 1；所以 a=0, b=1, c=2 可以简写为如下形式：

```go
const (
    a = iota
    b
    c
)
```

### iota 用法

```go
package main  
  
import "fmt"  
  
func main() {  
    const (  
            a = iota   //0  
            b          //1  
            c          //2  
            d = "ha"   //独立值，iota += 1  
            e          //"ha"   iota += 1  
            f = 100    //iota +=1  
            g          //100  iota +=1  
            h = iota   //7,恢复计数  
            i          //8  
    )  
    fmt.Println(a,b,c,d,e,f,g,h,i)  
}  
```

以上实例运行结果为：

```go
0 1 2 ha ha 100 100 7 8
```


```go
package main  
  
import "fmt"  
const (  
    i=1<<iota  
    j=3<<iota  
    k  
    l  
)  
  
func main() {  
    fmt.Println("i=",i)  
    fmt.Println("j=",j)  
    fmt.Println("k=",k)  
    fmt.Println("l=",l)  
}  

以上实例运行结果为：

i= 1
j= 6
k= 12
l= 24
```

iota 表示从 0 开始自动加 1，所以 i=1<<0, j=3<<1（**<<** 表示左移的意思），即：i=1, j=6，这没问题，关键在 k 和 l，从输出结果看 k=3<<2，l=3<<3。

简单表述:

- **i=1**：左移 0 位，不变仍为 1。
- **j=3**：左移 1 位，变为二进制 **110**，即 6。
- **k=3**：左移 2 位，变为二进制 **1100**，即 12。
- **l=3**：左移 3 位，变为二进制 **11000**，即 24。
# 数据类型

在 Go 编程语言中，数据类型用于声明函数和变量。

数据类型的出现是为了把数据分成所需内存大小不同的数据，编程的时候需要用大数据的时候才需要申请大内存，就可以充分利用内存。

Go 语言按类别有以下几种数据类型：

| 序号  | 类型和描述                                                                                                                                                                       |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **布尔型**  <br>布尔型的值只可以是常量 true 或者 false。一个简单的例子：var b bool = true。                                                                                                           |
| 2   | **数字类型**  <br>整型 int 和浮点型 float32、float64，Go 语言支持整型和浮点型数字，并且支持复数，其中位的运算采用补码。                                                                                                |
| 3   | **字符串类型:**  <br>字符串就是一串固定长度的字符连接起来的字符序列。Go 的字符串是由单个字节连接起来的。Go 语言的字符串的字节使用 UTF-8 编码标识 Unicode 文本。**请注意单引号：字符，双引号：字符串和\`\`：原始字符串字面量**                                         |
| 4   | **派生类型:**  <br>包括：<br><br>- (a) 指针类型（Pointer）<br>- (b) 数组类型<br>- (c) 结构化类型(struct)<br>- (d) Channel 类型<br>- (e) 函数类型<br>- (f) 切片类型<br>- (g) 接口类型（interface）<br>- (h) Map 类型 |


## 数字类型

Go 也有基于架构的类型，例如：int、uint 和 uintptr。

|序号|类型和描述|
|---|---|
|1|**uint8**  <br>无符号 8 位整型 (0 到 255)|
|2|**uint16**  <br>无符号 16 位整型 (0 到 65535)|
|3|**uint32**  <br>无符号 32 位整型 (0 到 4294967295)|
|4|**uint64**  <br>无符号 64 位整型 (0 到 18446744073709551615)|
|5|**int8**  <br>有符号 8 位整型 (-128 到 127)|
|6|**int16**  <br>有符号 16 位整型 (-32768 到 32767)|
|7|**int32**  <br>有符号 32 位整型 (-2147483648 到 2147483647)|
|8|**int64**  <br>有符号 64 位整型 (-9223372036854775808 到 9223372036854775807)|

### 浮点型

|序号|类型和描述|
|---|---|
|1|**float32**  <br>IEEE-754 32位浮点型数|
|2|**float64**  <br>IEEE-754 64位浮点型数|
|3|**complex64**  <br>32 位实数和虚数|
|4|**complex128**  <br>64 位实数和虚数|


## 其他数字类型

以下列出了其他更多的数字类型：

|序号|类型和描述|
|---|---|
|1|**byte**  <br>类似 uint8|
|2|**rune**  <br>类似 int32|
|3|**uint**  <br>32 或 64 位|
|4|**int**  <br>与 uint 一样大小|
|5|**uintptr**  <br>无符号整型，用于存放一个指针|
## 数据类型转换：Type Convert

语法格式：Type(Value)

常数：在有需要的时候，会自动转型

变量：需要手动转型 T(V)

注意点：兼容类型可以转换
```go
func main() {  
    var a int8 = 16  
    var b int64  
    b = int64(a)  
    fmt.Printf("%T\n%d\n%T\n%d\n", a, a, b, b)  
}
```
## 字符串类型

Go中的字符串是一个字节的切片。可以通过将其内容封装在“”中来创建字符串。Go中的字符串是Unicode兼容的，并且是UTF-8编码的。

一些基本操作需要使用`string`包。

```go
func main() {  
    str := "123"  
    num, err := strconv.Atoi(str)  
    if err != nil {  
        fmt.Println("转换错误:", err)  
    } else {  
        fmt.Printf("字符串 '%s' 转换为整数为：%d\n", str, num)  
    }  
}
```

## 类型分类

### 值类型

值类型在赋值、传递参数或返回值时，直接复制其值。每个变量都有自己独立的内存空间，修改一个变量不会影响其他变量。

 常见的值类型

- **基本数据类型**：int, float64, bool, string 等
- **数组**：如 `[5]int`
- **结构体**：如 `struct`

特性

1. **独立副本**：赋值或传递时创建独立的副本。
2. **内存分配**：每个变量都有自己独立的内存空间。
3. **性能**：由于复制整个值，可能会有性能开销，特别是对于大数据结构。

### 引用类型

引用类型在赋值、传递参数或返回值时，传递的是内存地址的引用。多个变量可以引用同一个内存地址，修改其中一个变量会影响到其他引用同一地址的变量。

 常见的引用类型

- **切片（Slice）**
- **映射（Map）**
- **通道（Channel）**
- **指针（Pointer）**
- **接口（Interface）**

特性

1. **共享内存**：多个变量可以引用同一个内存地址。
2. **内存分配**：引用类型的变量存储的是内存地址，而不是实际的数据。
3. **性能**：由于传递的是内存地址，通常比值类型的复制操作更高效。

### 值类型和引用类型的对比

| 特性   | 值类型        | 引用类型               |
| ---- | ---------- | ------------------ |
| 内存分配 | 独立的内存空间    | 共享的内存地址            |
| 赋值   | 复制整个值      | 复制内存地址             |
| 参数传递 | 传递值的副本     | 传递内存地址             |
| 修改影响 | 修改副本不影响原值  | 修改引用会影响所有引用同一地址的变量 |
| 性能   | 可能有较高的复制开销 | 通常更高效，特别是对于大数据结构   |
# 运算符

运算符用于在程序运行时执行数学或逻辑运算。

Go 语言内置的运算符有：

- 算术运算符
- 关系运算符
- 逻辑运算符
- 位运算符
- 赋值运算符
- 其他运算符

接下来让我们来详细看看各个运算符的介绍。

## 算术运算符

下表列出了所有Go语言的算术运算符。假定 A 值为 10，B 值为 20。

|运算符|描述|实例|
|---|---|---|
|+|相加|A + B 输出结果 30|
|-|相减|A - B 输出结果 -10|
|*|相乘|A * B 输出结果 200|
|/|相除|B / A 输出结果 2|
|%|求余|B % A 输出结果 0|
|++|自增|A++ 输出结果 11|
|--|自减|A-- 输出结果 9|
## 关系运算符

下表列出了所有Go语言的关系运算符。假定 A 值为 10，B 值为 20。

| 运算符 | 描述                                    | 实例               |
| --- | ------------------------------------- | ---------------- |
| ==  | 检查两个值是否相等，如果相等返回 True 否则返回 False。     | (A == B) 为 False |
| !=  | 检查两个值是否不相等，如果不相等返回 True 否则返回 False。   | (A != B) 为 True  |
| >   | 检查左边值是否大于右边值，如果是返回 True 否则返回 False。   | (A > B) 为 False  |
| <   | 检查左边值是否小于右边值，如果是返回 True 否则返回 False。   | (A < B) 为 True   |
| >=  | 检查左边值是否大于等于右边值，如果是返回 True 否则返回 False。 | (A >= B) 为 False |
| <=  | 检查左边值是否小于等于右边值，如果是返回 True 否则返回 False。 | (A <= B) 为 True  |
## 逻辑运算符

下表列出了所有Go语言的逻辑运算符。假定 A 值为 True，B 值为 False。

| 运算符 | 描述                                                | 实例               |
| --- | ------------------------------------------------- | ---------------- |
| &&  | 逻辑 AND 运算符。 如果两边的操作数都是 True，则条件 True，否则为 False。   | (A && B) 为 False |
| \|  | 逻辑 OR 运算符。 如果两边的操作数有一个 True，则条件 True，否则为 False。   | (A \| B) 为 True  |
| !   | 逻辑 NOT 运算符。 如果条件为 True，则逻辑 NOT 条件 False，否则为 True。 | !(A && B) 为 True |
## 位运算符

位运算符对整数在内存中的二进制位进行操作。

下表列出了位运算符 &, |, 和 ^ 的计算：

| p   | q   | p & q | p \| q | p ^ q |
| --- | --- | ----- | ------ | ----- |
| 0   | 0   | 0     | 0      | 0     |
| 0   | 1   | 0     | 1      | 1     |
| 1   | 1   | 1     | 1      | 0     |
| 1   | 0   | 0     | 1      | 1     |
Go 语言支持的位运算符如下表所示。假定 A 为60，B 为13：

| 运算符 | 描述                                                                                    | 实例                              |
| --- | ------------------------------------------------------------------------------------- | ------------------------------- |
| &   | 按位与运算符"&"是双目运算符。 其功能是参与运算的两数各对应的二进位相与。                                                | (A & B) 结果为 12, 二进制为 0000 1100  |
| \|  | 按位或运算符"\|"是双目运算符。 其功能是参与运算的两数各对应的二进位相或                                                | (A \| B) 结果为 61, 二进制为 0011 1101 |
| ^   | 按位异或运算符"^"是双目运算符。 其功能是参与运算的两数各对应的二进位相异或，当两对应的二进位相异时，结果为1。                             | (A ^ B) 结果为 49, 二进制为 0011 0001  |
| <<  | 左移运算符"<<"是双目运算符。左移n位就是乘以2的n次方。 其功能把"<<"左边的运算数的各二进位全部左移若干位，由"<<"右边的数指定移动的位数，高位丢弃，低位补0。 | A << 2 结果为 240 ，二进制为 1111 0000  |
| >>  | 右移运算符">>"是双目运算符。右移n位就是除以2的n次方。 其功能是把">>"左边的运算数的各二进位全部右移若干位，">>"右边的数指定移动的位数。           | A >> 2 结果为 15 ，二进制为 0000 1111   |
## 赋值运算符

下表列出了所有Go语言的赋值运算符。

| 运算符 | 描述                      | 实例                           |
| --- | ----------------------- | ---------------------------- |
| =   | 简单的赋值运算符，将一个表达式的值赋给一个左值 | C = A + B 将 A + B 表达式结果赋值给 C |
| +=  | 相加后再赋值                  | C += A 等于 C = C + A          |
| -=  | 相减后再赋值                  | C -= A 等于 C = C - A          |
| *=  | 相乘后再赋值                  | C *= A 等于 C = C * A          |
| /=  | 相除后再赋值                  | C /= A 等于 C = C / A          |
| %=  | 求余后再赋值                  | C %= A 等于 C = C % A          |
| <<= | 左移后赋值                   | C <<= 2 等于 C = C << 2        |
| >>= | 右移后赋值                   | C >>= 2 等于 C = C >> 2        |
| &=  | 按位与后赋值                  | C &= 2 等于 C = C & 2          |
| ^=  | 按位异或后赋值                 | C ^= 2 等于 C = C ^ 2          |
| \|= | 按位或后赋值                  | C \|= 2 等于 C = C \| 2        |
## 其他运算符

下表列出了Go语言的其他运算符。

| 运算符 | 描述       | 实例              |
| --- | -------- | --------------- |
| &   | 返回变量存储地址 | &a; 将给出变量的实际地址。 |
| *   | 指针变量。    | *a; 是一个指针变量     |
## 运算符优先级

有些运算符拥有较高的优先级，二元运算符的运算方向均是从左至右。下表列出了所有运算符以及它们的优先级，由上至下代表优先级由高到低：

|优先级|运算符|
|---|---|
|5|* / % << >> & &^|
|4|+ - \| ^|
|3|== != < <= > >=|
|2|&&|
|1|\||

当然，你可以通过使用括号来临时提升某个表达式的整体运算优先级。
# Go 语言条件语句

条件语句需要开发者通过指定一个或多个条件，并通过测试条件是否为 true 来决定是否执行指定语句，并在条件为 false 的情况在执行另外的语句。

下图展示了程序语言中条件语句的结构：

![](https://www.runoob.com/wp-content/uploads/2015/06/ZBuVRsKmCoH6fzoz.png "Go 语言条件语句")

Go 语言提供了以下几种条件判断语句：

|语句|描述|
|---|---|
|[if 语句](https://www.runoob.com/go/go-if-statement.html "Go if 语句")|**if 语句** 由一个布尔表达式后紧跟一个或多个语句组成。|
|[if...else 语句](https://www.runoob.com/go/go-if-else-statement.html "Go if...else 语句")|**if 语句** 后可以使用可选的 **else 语句**, else 语句中的表达式在布尔表达式为 false 时执行。|
|[if 嵌套语句](https://www.runoob.com/go/go-nested-if-statements.html "Go if 嵌套语句")|你可以在 **if** 或 **else if** 语句中嵌入一个或多个 **if** 或 **else if** 语句。|
|[switch 语句](https://www.runoob.com/go/go-switch-statement.html "Go switch 语句")|**switch** 语句用于基于不同条件执行不同动作。|
|[select 语句](https://www.runoob.com/go/go-select-statement.html "Go select 语句")|**select** 语句类似于 **switch** 语句，但是select会随机执行一个可运行的case。如果没有case可运行，它将阻塞，直到有case可运行。|

> 注意：Go 没有三目运算符，所以不支持 **?:** 形式的条件判断。


```go
func main() {  
    var num int  
    fmt.Scan(&num)  
    if num < 10 {    // 还可以在判断前面先进行赋值，if num:=20 ; num <10 
       fmt.Println("num小于10")  
    } else if num < 20 {  
       fmt.Println("num小于20")  
    } else {  
       fmt.Println("error")  
    }  
    switch num {  // 如果省略参数，默认作用在true上
    case 1, 2, 3:  
        fmt.Println(num)  
        fallthrough // 强制执行吓一条语句，且不会进行判断，且只能在语句的后面
    case 5:  
        fmt.Println(num)  
    default:  
        fmt.Println(num)  
}
}
```
# Go 语言循环语句

在不少实际问题中有许多具有规律性的重复操作，因此在程序中就需要重复执行某些语句。

以下为大多编程语言循环程序的流程图：

![](https://www.runoob.com/wp-content/uploads/2015/06/go-loops.svg)

Go 语言提供了以下几种类型循环处理语句：

|循环类型|描述|
|---|---|
|[for 循环](https://www.runoob.com/go/go-for-loop.html)|重复执行语句块|
|[循环嵌套](https://www.runoob.com/go/go-nested-loops.html)|在 for 循环中嵌套一个或多个 for 循环|

## 循环控制语句

循环控制语句可以控制循环体内语句的执行过程。

GO 语言支持以下几种循环控制语句：

|控制语句|描述|
|---|---|
|[break 语句](https://www.runoob.com/go/go-break-statement.html)|经常用于中断当前 for 循环或跳出 switch 语句|
|[continue 语句](https://www.runoob.com/go/go-continue-statement.html)|跳过当前循环的剩余语句，然后继续进行下一轮循环。|
|[goto 语句](https://www.runoob.com/go/go-goto-statement.html)|将控制转移到被标记的语句。|

```go
func main() {  
    for i := 0; i <= 10; i++ {  
       fmt.Println(i)  
    }  
    i := 1  
    for i <= 10 {  
       i++  
       fmt.Println(i)  
    }  
  
    for {  
       fmt.Println(i) // 无限循环  
    }  
  
    strings := []string{"google", "runoob"}  
    for i, s := range strings { // 这种格式的循环可以对字符串、数组、切片等进行迭代输出元素。  
       fmt.Println(i, s)  
    }  
    /* 定义局部变量 */    var a int = 10  
  
    /* 循环 */    LOOP: for a < 20 {  
    if a == 15 {  
       /* 跳过迭代 */       a = a + 1  
       goto LOOP  
    }  
    fmt.Printf("a的值为 : %d\n", a)  
    a++  
}  
}  
}
```
# Go 语言数组

Go 语言提供了数组类型的数据结构。

数组是具有相同唯一类型的一组已编号且长度固定的数据项序列，这种类型可以是任意的原始类型例如整型、字符串或者自定义类型。

相对于去声明 **number0, number1, ..., number99** 的变量，使用数组形式 **numbers\[0], numbers\[1] ..., numbers\[99]** 更加方便且易于扩展。

数组元素可以通过索引（位置）来读取（或者修改），索引从 0 开始，第一个元素索引为 0，第二个索引为 1，以此类推。

![](https://www.runoob.com/wp-content/uploads/2015/06/goarray.png)

---

## 声明数组

Go 语言数组声明需要指定元素类型及元素个数，语法格式如下：

var arrayName \[size]dataType

其中，**arrayName** 是数组的名称，**size** 是数组的大小，**dataType** 是数组中元素的数据类型，**且数组是定长的，一旦声明不可更改长度**。

以下定义了数组 balance 长度为 10 类型为 float32：

var balance \[10]float32

## 初始化数组

以下演示了数组初始化：

以下实例声明一个名为 numbers 的整数数组，其大小为 5，在声明时，数组中的每个元素都会根据其数据类型进行默认初始化，对于整数类型，初始值为 0。

var numbers \[5]int

还可以使用初始化列表来初始化数组的元素：

var numbers = \[5]int{1, 2, 3, 4, 5}

以上代码声明一个大小为 5 的整数数组，并将其中的元素分别初始化为 1、2、3、4 和 5。

另外，还可以使用 := 简短声明语法来声明和初始化数组：

numbers := \[5]int{1, 2, 3, 4, 5}

以上代码创建一个名为 numbers 的整数数组，并将其大小设置为 5，并初始化元素的值。

**注意：**在 Go 语言中，数组的大小是类型的一部分，因此不同大小的数组是不兼容的，也就是说 \[5]int 和 \[10]int 是不同的类型。

以下定义了数组 balance 长度为 5 类型为 float32，并初始化数组的元素：

var balance = \[5]float32{1000.0, 2.0, 3.4, 7.0, 50.0}

我们也可以通过字面量在声明数组的同时快速初始化数组：

balance := \[5]float32{1000.0, 2.0, 3.4, 7.0, 50.0}

如果数组长度不确定，可以使用 ... 代替数组的长度，编译器会根据元素个数自行推断数组的长度：

var balance = \[...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
或
balance := \[...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}

如果设置了数组的长度，我们还可以通过指定下标来初始化元素：

//  将索引为 1 和 3 的元素初始化
balance := \[5]float32{1:2.0,3:7.0}

初始化数组中 {} 中的元素个数不能大于 \[] 中的数字。

如果忽略 \[] 中的数字不设置数组大小，Go 语言会根据元素的个数来设置数组的大小：

 balance\[4] = 50.0

以上实例读取了第五个元素。数组元素可以通过索引（位置）来读取（或者修改），索引从 0 开始，第一个元素索引为 0，第二个索引为 1，以此类推。

![](https://www.runoob.com/wp-content/uploads/2015/06/array_presentation.jpg)

---

## 访问数组元素

数组元素可以通过索引（位置）来读取。格式为数组名后加中括号，中括号中为索引的值。例如：

var salary float32 = balance\[9]

以上实例读取了数组 balance 第 10 个元素的值。

以下演示了数组完整操作（声明、赋值、访问）的实例：

## 实例 1
```go
package main  
  
import "fmt"  
  
func main() {  
   var n [10]int /* n 是一个长度为 10 的数组 */  
   var i,j int  
  
   /* 为数组 n 初始化元素 */          
   for i = 0; i < 10; i++ {  
      n[i] = i + 100 /* 设置元素为 i + 100 */  
   }  
  
   /* 输出每个数组元素的值 */  
   for j = 0; j < 10; j++ {  
      fmt.Printf("Element[%d] = %d\n", j, n[j] )  
   }  
}  

以上实例执行结果如下：

Element[0] = 100
Element[1] = 101
Element[2] = 102
Element[3] = 103
Element[4] = 104
Element[5] = 105
Element[6] = 106
Element[7] = 107
Element[8] = 108
Element[9] = 109
```
## 实例 2
```go
package main  
  
import "fmt"  
  
func main() {  
   var i,j,k int  
   // 声明数组的同时快速初始化数组  
   balance := [5]float32{1000.0, 2.0, 3.4, 7.0, 50.0}  
  
   /* 输出数组元素 */         ...  
   for i = 0; i < 5; i++ {  
      fmt.Printf("balance[%d] = %f\n", i, balance[i] )  
   }  
     
   balance2 := [...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}  
   /* 输出每个数组元素的值 */  
   for j = 0; j < 5; j++ {  
      fmt.Printf("balance2[%d] = %f\n", j, balance2[j] )  
   }  
  
   //  将索引为 1 和 3 的元素初始化  
   balance3 := [5]float32{1:2.0,3:7.0}    
   for k = 0; k < 5; k++ {  
      fmt.Printf("balance3[%d] = %f\n", k, balance3[k] )  
   }  
}  

以上实例执行结果如下：

balance[0] = 1000.000000
balance[1] = 2.000000
balance[2] = 3.400000
balance[3] = 7.000000
balance[4] = 50.000000
balance2[0] = 1000.000000
balance2[1] = 2.000000
balance2[2] = 3.400000
balance2[3] = 7.000000
balance2[4] = 50.000000
balance3[0] = 0.000000
balance3[1] = 2.000000
balance3[2] = 0.000000
balance3[3] = 7.000000
balance3[4] = 0.000000
```
## 多维数组

Go 语言支持多维数组，以下为常用的多维数组声明方式：
```go
var variable_name [SIZE1][SIZE2]...[SIZEN] variable_type
```

以下实例声明了三维的整型数组：
```go
var threedim [5][10][4]int
```
## 函数传递数组

Go 语言中的数组是值类型，因此在将数组传递给函数时，实际上是传递数组的副本。

如果你想向函数传递数组参数，你需要在函数定义时，声明形参为数组，我们可以通过以下两种方式来声明：

### 方式一

形参设定数组大小：
```go
func myFunction(param [10]int) {
    ....
}
```

### 方式二

形参未设定数组大小：
```go
func myFunction(param []int) {
    ....
}
```

如果你想要在函数内修改原始数组，可以通过传递数组的指针来实现。
# Go 语言切片(Slice)

Go 语言切片是对数组的抽象,**实际存储数据的是数组**。

Go 数组的长度不可改变，在特定场景中这样的集合就不太适用，Go 中提供了一种灵活，功能强悍的内置类型切片("动态数组")，与数组相比切片的长度是不固定的，可以追加元素，在追加时可能使切片的容量增大。

## 定义切片

你可以声明一个未指定大小的数组来定义切片：

var identifier \[]type

切片不需要说明长度。

或使用 **make()** 函数来创建切片:

var slice1 \[]type = make(\[]type, len)

也可以简写为

slice1 := make(\[]type, len)

也可以指定容量，其中 **capacity** 为可选参数。

make(\[]T, length, capacity)

这里 len 是数组的长度并且也是切片的初始长度。

### 切片初始化

s :=\[] int {1,2,3 } 

直接初始化切片，\[]int 表示是切片类型，**{1,2,3}** 初始化值依次是 1,2,3，其 **cap=len=3**。

s := arr\[:] 

初始化切片 **s**，是数组 arr 的引用。

s := arr\[startIndex:endIndex] 

将 arr 中从下标 startIndex 到 endIndex-1 下的元素创建为一个新的切片。

s := arr\[startIndex:] 

默认 endIndex 时将表示一直到arr的最后一个元素。

s := arr\[:endIndex] 

默认 startIndex 时将表示从 arr 的第一个元素开始。

s1 := s\[startIndex:endIndex] 

通过切片 s 初始化切片 s1。

s :=make(\[]int,len,cap) 

通过内置函数 **make()** 初始化切片**s**，**\[]int** 标识为其元素类型为 int 的切片。

---

## len() 和 cap() 函数

切片是可索引的，并且可以由 len() 方法获取长度。

切片提供了计算容量的方法 cap() 可以测量切片最长可以达到多少。

以下为具体实例：

## 实例

```go
package main  
  
import "fmt"  
  
func main() {  
   var numbers = make([]int,3,5)  
  
   printSlice(numbers)  
}  
  
func printSlice(x []int){  
   fmt.Printf("len=%d cap=%d slice=%v\n",len(x),cap(x),x)  
}  

以上实例运行输出结果为:

len=3 cap=5 slice=[0 0 0]
```

## 空(nil)切片

一个切片在未初始化之前默认为 nil，长度为 0，实例如下：

## 实例

```go
package main  
  
import "fmt"  
  
func main() {  
   var numbers []int  
  
   printSlice(numbers)  
  
   if(numbers == nil){  
      fmt.Printf("切片是空的")  
   }  
}  
  
func printSlice(x []int){  
   fmt.Printf("len=%d cap=%d slice=%v\n",len(x),cap(x),x)  
}  

以上实例运行输出结果为:

len=0 cap=0 slice=[]
切片是空的

```

## 切片截取

可以通过设置下限及上限来设置截取切片 \[lower-bound:upper-bound]，实例如下：
```go
package main  
  
import "fmt"  
  
func main() {  
   /* 创建切片 */  
   numbers := []int{0,1,2,3,4,5,6,7,8}    
   printSlice(numbers)  
  
   /* 打印原始切片 */  
   fmt.Println("numbers ==", numbers)  
  
   /* 打印子切片从索引1(包含) 到索引4(不包含)*/  
   fmt.Println("numbers[1:4] ==", numbers[1:4])  
  
   /* 默认下限为 0*/  
   fmt.Println("numbers[:3] ==", numbers[:3])  
  
   /* 默认上限为 len(s)*/  
   fmt.Println("numbers[4:] ==", numbers[4:])  
  
   numbers1 := make([]int,0,5)  
   printSlice(numbers1)  
  
   /* 打印子切片从索引  0(包含) 到索引 2(不包含) */  
   number2 := numbers[:2]  
   printSlice(number2)  
  
   /* 打印子切片从索引 2(包含) 到索引 5(不包含) */  
   number3 := numbers[2:5]  
   printSlice(number3)  
  
}  
  
func printSlice(x []int){  
   fmt.Printf("len=%d cap=%d slice=%v\n",len(x),cap(x),x)  
}  

执行以上代码输出结果为：

len=9 cap=9 slice=[0 1 2 3 4 5 6 7 8]
numbers == [0 1 2 3 4 5 6 7 8]
numbers[1:4] == [1 2 3]
numbers[:3] == [0 1 2]
numbers[4:] == [4 5 6 7 8]
len=0 cap=5 slice=[]
len=2 cap=9 slice=[0 1]
len=3 cap=7 slice=[2 3 4]
```
## append() 和 copy() 函数

如果想增加切片的容量，我们必须创建一个新的更大的切片并把原分片的内容都拷贝过来。

下面的代码描述了从拷贝切片的 copy 方法和向切片追加新元素的 append 方法。
```go
package main  
  
import "fmt"  
  
func main() {  
   var numbers []int  
   printSlice(numbers)  
  
   /* 允许追加空切片 */  
   numbers = append(numbers, 0)  
   printSlice(numbers)  
  
   /* 向切片添加一个元素 */  
   numbers = append(numbers, 1)  
   printSlice(numbers)  
  
   /* 同时添加多个元素 */  
   numbers = append(numbers, 2,3,4)  
   printSlice(numbers)  

   /* 允许将另一个切片添加 */  
   numbers = append(numbers, numbers...)  
   printSlice(numbers)  
  
   /* 创建切片 numbers1 是之前切片的两倍容量*/  
   numbers1 := make([]int, len(numbers), (cap(numbers))*2)  
  
   /* 拷贝 numbers 的内容到 numbers1 */  
   copy(numbers1,numbers)  
   printSlice(numbers1)    
}  
  
func printSlice(x []int){  
   fmt.Printf("len=%d cap=%d slice=%v\n",len(x),cap(x),x)  
}  

以上代码执行输出结果为：

len=0 cap=0 slice=[]
len=1 cap=1 slice=[0]
len=2 cap=2 slice=[0 1]
len=5 cap=6 slice=[0 1 2 3 4]
len=5 cap=12 slice=[0 1 2 3 4]

```
**append在扩容时，如果没有超过原始容量则不会创建新的切片，一旦超过原始容量就会创建一个新切片并复制老切片的内容进行新增。**
## 深拷贝和浅拷贝

- 浅拷贝：浅拷贝是指复制对象时，只复制对象的引用，而不复制对象本身。对于引用类型，浅拷贝后的新对象和原对象共享同一块内存，修改其中一个对象会影响到另一个对象。

- 深拷贝：深拷贝是指复制对象时，不仅复制对象的引用，还复制对象本身及其所有嵌套的对象。深拷贝后的新对象和原对象是完全独立的，修改其中一个对象不会影响到另一个对象。

|特性|浅拷贝|深拷贝|
|---|---|---|
|内存分配|复制引用，指向同一块内存|复制对象及其所有嵌套对象|
|数据共享|是|否|
|修改影响|修改一个对象会影响另一个对象|修改一个对象不会影响另一个对象|
|性能|通常更高效|可能有较高的性能开销|
# Go 语言Map(集合)

Map 是一种无序的键值对的集合。

Map 最重要的一点是通过 key 来快速检索数据，key 类似于索引，指向数据的值。

Map 是一种集合，所以我们可以像迭代数组和切片那样迭代它。不过，Map 是无序的，遍历 Map 时返回的键值对的顺序是不确定的。

在获取 Map 的值时，如果键不存在，返回该类型的零值，例如 int 类型的零值是 0，string 类型的零值是 ""。

Map 是引用类型，如果将一个 Map 传递给一个函数或赋值给另一个变量，它们都指向同一个底层数据结构，因此对 Map 的修改会影响到所有引用它的变量。

### 定义 Map

可以使用内建函数 make 或使用 map 关键字来定义 Map:
```go
/* 使用 make 函数 */
map_variable := make(map[KeyType]ValueType, initialCapacity)
```

其中 KeyType 是键的类型，ValueType 是值的类型，initialCapacity 是可选的参数，用于指定 Map 的初始容量。Map 的容量是指 Map 中可以保存的键值对的数量，当 Map 中的键值对数量达到容量时，Map 会自动扩容。如果不指定 initialCapacity，Go 语言会根据实际情况选择一个合适的值。

```go
// 通过这种方式创建的map，默认值为nil，且不能插入值
var m1 map[string]int

// 创建一个空的 Map
m := make(map[string]int)  
  
// 创建一个初始容量为 10 的 Map  
m := make(map[string]int, 10)  

也可以使用字面量创建 Map：

// 使用字面量创建 Map
m := map[string]int{
    "apple": 1,
    "banana": 2,
    "orange": 3,
}

获取元素：

// 获取键值对
v1 := m["apple"]
v2, ok := m["pear"]  // 如果键不存在，ok 的值为 false，v2 的值为该类型的零值

修改元素：

// 修改键值对
m["apple"] = 5

获取 Map 的长度：

// 获取 Map 的长度
len := len(m)

遍历 Map：

// 遍历 Map
for k, v := range m {
    fmt.Printf("key=%s, value=%d\n", k, v)
}

删除元素：

// 删除键值对
delete(m, "banana")
```

```go
package main  
  
import "fmt"  
  
func main() {  
    var siteMap map[string]string /*创建集合 */  
    siteMap = make(map[string]string)  
  
    /* map 插入 key - value 对,各个国家对应的首都 */  
    siteMap [ "Google" ] = "谷歌"  
    siteMap [ "Runoob" ] = "菜鸟教程"  
    siteMap [ "Baidu" ] = "百度"  
    siteMap [ "Wiki" ] = "维基百科"  
  
    /*使用键输出地图值 */  
    for site := range siteMap {  
        fmt.Println(site, "首都是", siteMap [site])  
    }  
  
    /*查看元素在集合中是否存在 */  
    name, ok := siteMap [ "Facebook" ] /*如果确定是真实的,则存在,否则不存在 */  
    /*fmt.Println(capital) */  
    /*fmt.Println(ok) */  
    if (ok) {  
        fmt.Println("Facebook 的 站点是", name)  
    } else {  
        fmt.Println("Facebook 站点不存在")  
    }  
}  

以上实例运行结果为：

Wiki 首都是 维基百科
Google 首都是 谷歌
Runoob 首都是 菜鸟教程
Baidu 首都是 百度
Facebook 站点不存在
```

## delete() 函数

delete() 函数用于删除集合的元素, 参数为 map 和其对应的 key。实例如下：

```go
package main  
  
import "fmt"  
  
func main() {  
        /* 创建map */  
        countryCapitalMap := map[string]string{"France": "Paris", "Italy": "Rome", "Japan": "Tokyo", "India": "New delhi"}  
  
        fmt.Println("原始地图")  
  
        /* 打印地图 */  
        for country := range countryCapitalMap {  
                fmt.Println(country, "首都是", countryCapitalMap [ country ])  
        }  
  
        /*删除元素*/ delete(countryCapitalMap, "France")  
        fmt.Println("法国条目被删除")  
  
        fmt.Println("删除元素后地图")  
  
        /*打印地图*/  
        for country := range countryCapitalMap {  
                fmt.Println(country, "首都是", countryCapitalMap [ country ])  
        }  
}  

以上实例运行结果为：

原始地图
India 首都是 New delhi
France 首都是 Paris
Italy 首都是 Rome
Japan 首都是 Tokyo
法国条目被删除
删除元素后地图
Italy 首都是 Rome
Japan 首都是 Tokyo
India 首都是 New delhi
```
# Go 语言函数

函数是基本的代码块，用于执行一个任务。

Go 语言最少有个 main() 函数。

你可以通过函数来划分不同功能，逻辑上每个函数执行的是指定的任务。

函数声明告诉了编译器函数的名称，返回类型，和参数。

Go 语言标准库提供了多种可动用的内置的函数。例如，len() 函数可以接受不同类型参数并返回该类型的长度。如果我们传入的是字符串则返回字符串的长度，如果传入的是数组，则返回数组中包含的元素个数。

## 函数定义

Go 语言函数定义格式如下：

```go
func function_name( [parameter list] ) [return_types] {
   函数体
}
```

函数定义解析：

- func：函数由 func 开始声明
- function_name：函数名称，参数列表和返回值类型构成了函数签名。
- parameter list：参数列表，参数就像一个占位符，当函数被调用时，你可以将值传递给参数，这个值被称为实际参数。参数列表指定的是参数类型、顺序、及参数个数。参数是可选的，也就是说函数也可以不包含参数。
- return_types：返回类型，函数返回一列值。return_types 是该列值的数据类型。有些功能不需要返回值，这种情况下 return_types 不是必须的。
- 函数体：函数定义的代码集合。

以下实例为 max() 函数的代码，该函数传入两个整型参数 num1 和 num2，并返回这两个参数的最大值：

```go
/* 函数返回两个数的最大值 */  
func max(num1, num2 int) int {  
   /* 声明局部变量 */  
   var result int  
  
   if (num1 > num2) {  
      result = num1  
   } else {  
      result = num2  
   }  
   return result  
}  
```

## 函数调用

当创建函数时，你定义了函数需要做什么，通过调用该函数来执行指定任务。

调用函数，向函数传递参数，并返回值，例如：

```go
package main  
  
import "fmt"  
  
func main() {  
   /* 定义局部变量 */  
   var a int = 100  
   var b int = 200  
   var ret int  
  
   /* 调用函数并返回最大值 */  
   ret = max(a, b)  
  
   fmt.Printf( "最大值是 : %d\n", ret )  
}  
  
/* 函数返回两个数的最大值 */  
func max(num1, num2 int) int {  
   /* 定义局部变量 */  
   var result int  
  
   if (num1 > num2) {  
      result = num1  
   } else {  
      result = num2  
   }  
   return result  
}  

以上实例在 main() 函数中调用 max（）函数，执行结果为：

最大值是 : 200
```

## 函数返回多个值
```go
Go 函数可以返回多个值，例如：

package main  
  
import "fmt"  
  
func swap(x, y string) (string, string) {  
   return y, x  
}  
  
func main() {  
   a, b := swap("Google", "Runoob")  
   fmt.Println(a, b)  
}  

以上实例执行结果为：

Runoob Google

// 也可以直接在返回值写默认值
// 如果为空，sum默认为类型的默认值
func swap(x, y string) (sum int) {  
   return  
}  
```

## 函数参数

函数如果使用参数，该变量可称为函数的形参。

形参就像定义在函数体内的局部变量。

调用函数，可以通过两种方式来传递参数：

|传递类型|描述|
|---|---|
|[值传递](https://www.runoob.com/go/go-function-call-by-value.html)|值传递是指在调用函数时将实际参数复制一份传递到函数中，这样在函数中如果对参数进行修改，将不会影响到实际参数。|
|[引用传递](https://www.runoob.com/go/go-function-call-by-reference.html)|引用传递是指在调用函数时将实际参数的地址传递到函数中，那么在函数中对参数所进行的修改，将影响到实际参数。|
```go
// 值传递
func swap(x, y int) int {
   var temp int

   temp = x /* 保存 x 的值 */
   x = y    /* 将 y 值赋给 x */
   y = temp /* 将 temp 值赋给 y*/

   return temp;
}

// 引用传递
func swap(x *int, y *int) {
   var temp int
   temp = *x    /* 保持 x 地址上的值 */
   *x = *y      /* 将 y 值赋给 x */
   *y = temp    /* 将 temp 值赋给 y */
}
```

默认情况下，Go 语言使用的是值传递，即在调用过程中不会影响到实际参数。

在函数中，除了一对一传递参数的方式，也可以使用可变参数的形式进行传递。

```go
// 如果多个形参类型都一样，可以只在最后写类型
func add(x,y int) int {
    return x+y
}

// 可变参数是一个slice，如果想把一个slice作为参数传递func(slice...)
// 最多只能有一个可变参数，且要在参数列表最后
// 不设置返回值也可以使用retuen来结束函数
func add(x ...int) int {  
    var sum int  
    for i := 0; i < len(x); i++ {  
       sum += x[i]  
    }  
    return sum  
}
```

## 函数用法

| 函数用法                                                                  | 描述                   |
| --------------------------------------------------------------------- | -------------------- |
| [函数作为另外一个函数的实参](https://www.runoob.com/go/go-function-as-values.html) | 函数定义后可作为另外一个函数的实参数传入 |
| [闭包](https://www.runoob.com/go/go-function-closures.html)             | 闭包是匿名函数，可在动态编程中使用    |
| [方法](https://www.runoob.com/go/go-method.html)                        | 方法就是一个包含了接受者的函数      |
```go

// 函数作为另一个函数的参数
func operat(a, b int, fun func(x ...int) int) {  
    res := fun(a, b)  
    fmt.Println(res)  
}  
  
func main() {  
    /* 使用函数 */  
   // 外面使用函数作为参数的是高级函数
   // 被调用的函数被叫做回调函数
    operat(1, 2, add)  
  
}

// 闭包
func getSequence() func() int {  
   i:=0  
   return func() int {  
      i+=1  
     return i    
   }  
}  
  
func main(){  
   /* nextNumber 为一个函数，函数 i 为 0 */  
   nextNumber := getSequence()    
  
   /* 调用 nextNumber 函数，i 变量自增 1 并返回 */  
   fmt.Println(nextNumber())  
   fmt.Println(nextNumber())  
   fmt.Println(nextNumber())  
     
   /* 创建新的函数 nextNumber1，并查看结果 */  
   nextNumber1 := getSequence()    
   fmt.Println(nextNumber1())  
   fmt.Println(nextNumber1())  
}


// 方法
/* 定义结构体 */  
type Circle struct {  
  radius float64  
}  
  
func main() {  
  var c1 Circle  
  c1.radius = 10.00  
  fmt.Println("圆的面积 = ", c1.getArea())  
}  
  
//该 method 属于 Circle 类型对象中的方法  
func (c Circle) getArea() float64 {  
  //c.radius 即为 Circle 类型对象中的属性  
  return 3.14 * c.radius * c.radius  
}
```
## 递归函数

- 递归函数(recursion)：一个函数自己调用自己，并且设置了一个出口，这样的函数就叫做递归函数。
```go
	
func fact(n int) int {
    if n == 0 {
        return 1
    }
    return n * fact(n-1)
}
```
## defer关键字

defer用于资源的释放，会在函数返回之前进行调用。

需要注意的是，延迟函数是延迟函数被执行，而不是延迟函数被调用，所以在运行到函数被调用时参数已经传递过去了，只不过要到最后才执行。

如果有多个defer表达式，调用顺序类似于栈，越后面的defer表达式越先被调用。

```go
func f() (r int) {
     t := 5
     defer func() {
       t = t + 5
     }()
     return t
}  // 返回值为5
```

为什么这个例子里面的返回值不是10呢？

defer是在return之前执行的。这个在 [官方文档](http://golang.org/ref/spec#defer_statements)中是明确说明了的。要使用defer时不踩坑，最重要的一点就是要明白，**return xxx这一条语句并不是一条原子指令!**

函数返回的过程是这样的：先给返回值赋值，然后调用defer表达式，最后才是返回到调用函数中。

所以如果改写成下面这样就不会有疑惑为什么返回值不是10了。

```go
func f() (r int) {
     t := 5
     r = t //赋值指令
     func() {        //defer被插入到赋值与返回之间执行，这个例子中返回值r没被修改过
         t = t + 5
     }
     return        //空的return指令
}
```
## 匿名函数

匿名函数就是没有名字的函数。由于没有名字，匿名函数往往只能使用一次，除非将这个匿名函数赋值给一个变量。

```go
t := func(a,b int) int {  
    fmt.Println("匿名函数")  
    return a+b
}(3,4)

s :=func() {  
    fmt.Println("匿名函数")  
}
```
# Go 语言指针

Go 语言中指针是很容易学习的，Go 语言中使用指针可以更简单的执行一些任务。

我们都知道，变量是一种使用方便的占位符，用于引用计算机内存地址。

Go 语言的取地址符是 &，放到一个变量前使用就会返回相应变量的内存地址。

```go
以下实例演示了变量在内存中地址：

package main  
  
import "fmt"  
  
func main() {  
   var a int = 10    
  
   fmt.Printf("变量的地址: %x\n", &a  )  
}  

执行以上代码输出结果为：

变量的地址: 20818a220
```
## 什么是指针

一个指针变量指向了一个值的内存地址。

类似于变量和常量，在使用指针前你需要声明指针。指针声明格式如下：

```go
var var_name *var-type
```

var-type 为指针类型，var_name 为指针变量名，* 号用于指定变量是作为一个指针。以下是有效的指针声明：
```go
var ip *int        /* 指向整型*/
var fp *float32    /* 指向浮点型 */
```

## 如何使用指针

指针使用流程：

- 定义指针变量。
- 为指针变量赋值。
- 访问指针变量中指向地址的值。

在指针类型前面加上 * 号（前缀）来获取指针所指向的内容。
`
```go
package main  
  
import "fmt"  
  
func main() {  
   var a int= 20   /* 声明实际变量 */  
   var ip *int        /* 声明指针变量 */  
  
   ip = &a  /* 指针变量的存储地址 */  
  
   fmt.Printf("a 变量的地址是: %x\n", &a  )  
  
   /* 指针变量的存储地址 */  
   fmt.Printf("ip 变量储存的指针地址: %x\n", ip )  
  
   /* 使用指针访问值 */  
   fmt.Printf("*ip 变量的值: %d\n", *ip )  
}  

以上实例执行输出结果为：

a 变量的地址是: 20818a220
ip 变量储存的指针地址: 2081`8a220
*ip 变量的值: 20
```

## NEW函数

在 Go 语言中，`new` 是一个内置函数，用于分配内存并返回指向该内存的指针。与 `make` 不同，`new` 只分配内存，不初始化内存。`new` 函数适用于值类型（如数组、结构体等），而 `make` 函数则用于分配和初始化引用类型（如切片、映射和通道）。
- **`new`**：用于分配内存并返回指向该内存的指针。适用于值类型，如数组、结构体等。分配的内存会被初始化为零值。
- **`make`**：用于分配和初始化引用类型，如切片、映射和通道。返回的是初始化后的引用类型，而不是指针。
```go
func main() {
    // 使用 make 分配和初始化切片
    s := make([]int, 5)
    fmt.Printf("Type: %T, Value: %v\n", s, s)
    // 输出: Type: []int, Value: [0 0 0 0 0]

    // 使用 make 分配和初始化映射
    m := make(map[string]int)
    fmt.Printf("Type: %T, Value: %v\n", m, m)
    // 输出: Type: map[string]int, Value: map[]

    // 使用 make 分配和初始化通道
    c := make(chan int, 5)
    fmt.Printf("Type: %T, Value: %v\n", c, c)
    // 输出: Type: chan int, Value: 0xc0000b2000
}
```

## Go 空指针

当一个指针被定义后没有分配到任何变量时，它的值为 nil。

nil 指针也称为空指针。

nil在概念上和其它语言的null、None、nil、NULL一样，都指代零值或空值。

一个指针变量通常缩写为 ptr。

查看以下实例：
```go
package main  
  
import "fmt"  
  
func main() {  
   var  ptr *int  
  
   fmt.Printf("ptr 的值为 : %x\n", ptr  )  
}  

以上实例输出结果为：

ptr 的值为 : 0

空指针判断：

if(ptr != nil)     /* ptr 不是空指针 */
if(ptr == nil)    /* ptr 是空指针 */
```

## Go指针更多内容

接下来我们将为大家介绍Go语言中更多的指针应用：

| 内容                                                                              | 描述                     |
| ------------------------------------------------------------------------------- | ---------------------- |
| [Go 指针数组](https://www.runoob.com/go/go-array-of-pointers.html)                  | 你可以定义一个指针数组来存储地址       |
| [Go 指向指针的指针](https://www.runoob.com/go/go-pointer-to-pointer.html)              | Go 支持指向指针的指针           |
| [Go 向函数传递指针参数](https://www.runoob.com/go/go-passing-pointers-to-functions.html) | 通过引用或地址传参，在函数调用时可以改变其值 |
```go
// 数组指针
func main() {  
    arr := [4]int{1, 2, 3, 4}  
    var p1 *[4]int  // 数组指针
    p1 = &arr  
    fmt.Printf("%T\n", p1)  
  
    p1[1] = 100    
    (*p1)[2] = 200  // 等价，修改数组内容 
    fmt.Println(arr)  
}

// 指针数组
a := 1  
b := 2  
arr2 := [2]int{a, b}  
p2 := [2]*int{&a, &b}   // 指针数组
fmt.Println(arr2, p2)

// 指向指针的指针
func main() {

   var a int
   var ptr *int
   var pptr **int

   a = 3000

   /* 指针 ptr 地址 */
   ptr = &a

   /* 指向指针 ptr 地址 */
   pptr = &ptr

   /* 获取 pptr 的值 */
   fmt.Printf("变量 a = %d\n", a )
   fmt.Printf("指针变量 *ptr = %d\n", *ptr )
   fmt.Printf("指向指针的指针变量 **pptr = %d\n", **pptr)
}
```
# Go 语言结构体

Go 语言中数组可以存储同一类型的数据，但在结构体中我们可以为不同项定义不同的数据类型。

结构体是由一系列具有相同类型或不同类型的数据构成的数据集合。

结构体表示一项记录，比如保存图书馆的书籍记录，每本书有以下属性：

- Title ：标题
- Author ： 作者
- Subject：学科
- ID：书籍ID

## 定义结构体

结构体定义需要使用 type 和 struct 语句。struct 语句定义一个新的数据类型，结构体中有一个或多个成员。type 语句设定了结构体的名称。结构体的格式如下：
```go
type struct_variable_type struct {
   member definition
   member definition
   ...
   member definition
}
```

一旦定义了结构体类型，它就能用于变量的声明，语法格式如下：
```go
variable_name := structure_variable_type {value1, value2...valuen}
或
variable_name := structure_variable_type { key1: value1, key2: value2..., keyn: valuen}
```

实例如下：
```go
package main  
  
import "fmt"  
  
type Books struct {  
   title string  
   author string  
   subject string  
   book_id int  
}  
  
  
func main() {  
  
    // 创建一个新的结构体  
    fmt.Println(Books{"Go 语言", "www.runoob.com", "Go 语言教程", 6495407})  
  
    // 也可以使用 key => value 格式  
    fmt.Println(Books{title: "Go 语言", author: "www.runoob.com", subject: "Go 语言教程", book_id: 6495407})  
  
    // 忽略的字段为 0 或 空  
   fmt.Println(Books{title: "Go 语言", author: "www.runoob.com"})  
}  

输出结果为：

{Go 语言 www.runoob.com Go 语言教程 6495407}
{Go 语言 www.runoob.com Go 语言教程 6495407}
{Go 语言 www.runoob.com  0}
```

## 访问结构体成员

如果要访问结构体成员，需要使用点号 . 操作符，格式为：

结构体.成员名

结构体类型变量使用 struct 关键字定义，实例如下：
```go
package main  
  
import "fmt"  
  
type Books struct {  
   title string  
   author string  
   subject string  
   book_id int  
}  
  
func main() {  
   var Book1 Books        /* 声明 Book1 为 Books 类型 */  
   var Book2 Books        /* 声明 Book2 为 Books 类型 */  
  
   /* book 1 描述 */  
   Book1.title = "Go 语言"  
   Book1.author = "www.runoob.com"  
   Book1.subject = "Go 语言教程"  
   Book1.book_id = 6495407  
  
   /* book 2 描述 */  
   Book2.title = "Python 教程"  
   Book2.author = "www.runoob.com"  
   Book2.subject = "Python 语言教程"  
   Book2.book_id = 6495700  
  
   /* 打印 Book1 信息 */  
   fmt.Printf( "Book 1 title : %s\n", Book1.title)  
   fmt.Printf( "Book 1 author : %s\n", Book1.author)  
   fmt.Printf( "Book 1 subject : %s\n", Book1.subject)  
   fmt.Printf( "Book 1 book_id : %d\n", Book1.book_id)  
  
   /* 打印 Book2 信息 */  
   fmt.Printf( "Book 2 title : %s\n", Book2.title)  
   fmt.Printf( "Book 2 author : %s\n", Book2.author)  
   fmt.Printf( "Book 2 subject : %s\n", Book2.subject)  
   fmt.Printf( "Book 2 book_id : %d\n", Book2.book_id)  
}  

以上实例执行运行结果为：

Book 1 title : Go 语言
Book 1 author : www.runoob.com
Book 1 subject : Go 语言教程
Book 1 book_id : 6495407
Book 2 title : Python 教程
Book 2 author : www.runoob.com
Book 2 subject : Python 语言教程
Book 2 book_id : 6495700
```

## 结构体作为函数参数

你可以像其他数据类型一样将结构体类型作为参数传递给函数。并以以上实例的方式访问结构体变量：
```go
package main  
  
import "fmt"  
  
type Books struct {  
   title string  
   author string  
   subject string  
   book_id int  
}  
  
func main() {  
   var Book1 Books        /* 声明 Book1 为 Books 类型 */  
   var Book2 Books        /* 声明 Book2 为 Books 类型 */  
  
   /* book 1 描述 */  
   Book1.title = "Go 语言"  
   Book1.author = "www.runoob.com"  
   Book1.subject = "Go 语言教程"  
   Book1.book_id = 6495407  
  
   /* book 2 描述 */  
   Book2.title = "Python 教程"  
   Book2.author = "www.runoob.com"  
   Book2.subject = "Python 语言教程"  
   Book2.book_id = 6495700  
  
   /* 打印 Book1 信息 */  
   printBook(Book1)  
  
   /* 打印 Book2 信息 */  
   printBook(Book2)  
}  
  
func printBook( book Books ) {  
   fmt.Printf( "Book title : %s\n", book.title)  
   fmt.Printf( "Book author : %s\n", book.author)  
   fmt.Printf( "Book subject : %s\n", book.subject)  
   fmt.Printf( "Book book_id : %d\n", book.book_id)  
}  

以上实例执行运行结果为：

Book title : Go 语言
Book author : www.runoob.com
Book subject : Go 语言教程
Book book_id : 6495407
Book title : Python 教程
Book author : www.runoob.com
Book subject : Python 语言教程
Book book_id : 6495700
```

## 结构体指针

你可以定义指向结构体的指针类似于其他指针变量，格式如下：

```go
var struct_pointer *Books
```

以上定义的指针变量可以存储结构体变量的地址。查看结构体变量地址，可以将 & 符号放置于结构体变量前：

```go
struct_pointer = &Book1
```

使用结构体指针访问结构体成员，使用 "." 操作符：

```go
struct_pointer.title
```

接下来让我们使用结构体指针重写以上实例，代码如下：
```go
package main  
  
import "fmt"  
  
type Books struct {  
   title string  
   author string  
   subject string  
   book_id int  
}  
  
func main() {  
   var Book1 Books        /* 声明 Book1 为 Books 类型 */  
   var Book2 Books        /* 声明 Book2 为 Books 类型 */  
  
   /* book 1 描述 */  
   Book1.title = "Go 语言"  
   Book1.author = "www.runoob.com"  
   Book1.subject = "Go 语言教程"  
   Book1.book_id = 6495407  
  
   /* book 2 描述 */  
   Book2.title = "Python 教程"  
   Book2.author = "www.runoob.com"  
   Book2.subject = "Python 语言教程"  
   Book2.book_id = 6495700  
  
   /* 打印 Book1 信息 */  
   printBook(&Book1)  
  
   /* 打印 Book2 信息 */  
   printBook(&Book2)  
}  
func printBook( book *Books ) {  
   fmt.Printf( "Book title : %s\n", book.title)  
   fmt.Printf( "Book author : %s\n", book.author)  
   fmt.Printf( "Book subject : %s\n", book.subject)  
   fmt.Printf( "Book book_id : %d\n", book.book_id)  
}  

以上实例执行运行结果为：

Book title : Go 语言
Book author : www.runoob.com
Book subject : Go 语言教程
Book book_id : 6495407
Book title : Python 教程
Book author : www.runoob.com
Book subject : Python 语言教程
Book book_id : 6495700
```
## 匿名结构体

匿名结构体跟匿名函数一样就是没有名字的结构体。
```go
func main() {  
    s := struct {  
       name string   // 可以省略字段名，会自动用数据类型作为字段名
       age  int  
    }{  
       name: "wang",  
       age:  20,  
    }  
    fmt.Printf("%s\n%T\n", s, s)  
}
```
## 结构体嵌套

结构体嵌套就是在一个结构体的字段设置为另一个结构体。
```go
type book struct {  
    name  string  
    price int  
}  
  
type student struct {  
    name  string  
    books book  
}  
  
t := student{  
    name: "jack",  
    books: book{  
       name:  "price",  
       price: 10,  
    },  
}  
fmt.Println(t)
```