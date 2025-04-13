[Protobuf中文文档](https://protobuf.com.cn/)
# 1 下载protobuf

protocol buffer 编译器 `protoc` 用于编译 `.proto` 文件，其中包含服务和消息定义。选择以下方法之一来安装 `protoc`。

## 1.1 安装预编译二进制文件 (任何操作系统)

要从预编译二进制文件安装最新版本的协议编译器，请按照以下说明操作

1. 从 [https://github.com/google/protobuf/releases](https://github.com/google/protobuf/releases)，手动下载与您的操作系统和计算机架构 (`protoc-<version>-<os>-<arch>.zip`) 对应的 zip 文件，或使用如下命令获取文件
    
    `PB_REL="https://github.com/protocolbuffers/protobuf/releases" curl -LO $PB_REL/download/v< param protoc-version >/protoc-< param protoc-version >-linux-x86_64.zip`
    
2. 将文件解压缩到 `$HOME/.local` 或您选择的目录。例如
    
    `unzip protoc-< param protoc-version >-linux-x86_64.zip -d $HOME/.local`
    
3. 更新您环境的路径变量，以包含 `protoc` 可执行文件的路径。例如
    
    `export PATH="$PATH:$HOME/.local/bin"`
    

## 1.2 使用包管理器安装

>**警告⚠️**
>
>在使用包管理器安装后，运行 `protoc --version` 以检查 `protoc` 的版本，确保版本足够新。某些包管理器安装的 `protoc` 版本可能非常旧。请参阅[版本支持页面](https://protobuf.com.cn/support/version-support)，将版本检查的输出与您正在使用的语言的受支持版本的次要版本号进行比较。

您可以使用包管理器在 Linux、macOS 或 Windows 下安装协议编译器 `protoc`，使用以下命令。

- Linux，例如使用 `apt` 或 `apt-get`
```bash
    apt install -y protobuf-compiler 
    protoc --version  # Ensure compiler version is 3+
```
    
- MacOS，使用 [Homebrew](https://brew.sh.cn/)
    
```bash
    brew install protobuf 
    protoc --version  # Ensure compiler version is 3+
```
    
- Windows，使用 [Winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
```bash
    winget install protobuf 
    protoc --version # Ensure compiler version is 3+
```
# 2 编写Protobuf文件

- 文件必须以 `proto` 结尾
- 客户端和服务端所有关于 `proto` 文件是要一样的

```go
// hello.proto
// 版本说明使用proto3  
syntax = "proto3";  
  
// 关于最后生成的go文件是处于哪个目录哪个包中，  
// . 代表当前目录生成，service代表了生成的go文件的包名是service  
option go_package = ".;service";  
  
// 定义一个服务，服务中需要有一个方法，这个方法可以接受客户端的参数，返回服务端的响应  
// 这个service叫SayHello，这个服务中有一个方法叫SayHello  
// 这个方法会发送一个HelloRequest，然后返回一个HelloResponse  
service SayHello {  
  rpc SayHello(HelloRequest) returns (HelloResponse) {}  
}  
  
// message关键字可以理解为Go中的结构体  
// 注意，这里并不是赋值，而是定义这个变量在message中的位置  
message HelloRequest {  
  string requestName = 1;  
}  
  
message HelloResponse {  
  string responseMsg = 1;  
}


// 编写完之后在同级目录下
cd hello-server/proto 

// 生成 ​Protobuf 消息的序列化/反序列化代码​（数据结构的 Go 代码）。
// 包含 `.proto` 文件中定义的所有 ​消息（Message）的 Go 结构体。
protoc --go_out=. hello.proto // hello.pb.go 

// 生成 ​**gRPC 服务端和客户端的接口代码**​（通信逻辑的 Go 代码）。
// 包含 `.proto` 文件中定义的 ​gRPC 服务接口。
// --go-grpc_out 表示使用 `protoc-gen-go-grpc` 插件（负责生成 gRPC 服务端/客户端代码）。
protoc --go-grpc_out=. hello.proto  // hello_grpc.pb.go

protoc --go_out=. --go-grpc_out=. hello.proto
```
# 3 proto编写语法

> message

message：protobuf中定义一个消息类型是通过关键字 `message` 字段指定的。消息就是需要传输的数据格式的定义。

message类似于go中的struct。

在消息承载的数据分别对应于每一个字段，其中每个字段都有一个名字和一种类型。

一个proto文件中可以定义多个消息类型。

> 字段规则

required：消息体中必填的字段，不设置会导致编码异常，在protobuf2中使用，protobuf3中被删除。

optional：消息体中的可选字段。protobuf3没有required，optional等说明关键字，默认为optional。

repeated：消息体中可以重复的字段，重复的值的顺序会被保留在go中定义为切片。

> 消息号

在消息体的定义中，**每个字段都必须要有一个唯一的标识号**，标识号是\[1,2^29-1\]范围内的一个整数。

> 嵌套消息

可以在其他消息类型中定义、使用消息类型

```protobuf
message PersonInfo{
    message Person{
        string name = 1;
        int32 height = 2; 
    }
    repeated Person info = 1;
}
```

如果要在外部重复这个消息类型

```protobuf
message PersonMessage{
    PersionInfo.Person info = 1;
}
```

> 服务定义

如果想将消息类型用在rpc系统中，可以在 **.proto文件中定义一个RPC服务接口**，protocol buffer编译器将会根据所选择的不同语言生成服务接口代码及存根。

```protobuf
service SayHello {  
  rpc SayHello(HelloRequest) returns (HelloResponse) {}  
}  
```

上述表示定义了一个RPC服务，该方法接受 `HelloRequest` 返回 `HelloResponse`