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
   . "fmt" # 在使用时不需要写包名
   f "fmt" # 在使用时可以使用别名
   _ "fmt" # 不使用该包的函数，而是调用init函数
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

| 命令        | 说明                    |
| --------- | --------------------- |
| -d        | 让命令程序只执行下载动作，而不执行安装动作 |
| -f        |                       |
| -fix      |                       |
| -insecure |                       |
| -t        |                       |
| -u        |                       |