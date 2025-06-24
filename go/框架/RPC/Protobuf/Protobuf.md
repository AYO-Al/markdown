更多详细信息可以参考：[Protobuf中文文档](https://protobuf.com.cn/)

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
// 如果不指定则默认使用proto2
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
  map<string, MerchItem> items = 1; // 生成map[string]MerchItem类型
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

## 3.1 message

message：protobuf中定义一个消息类型是通过关键字 `message` 字段指定的。消息就是需要传输的数据格式的定义。

message类似于go中的struct。

在消息承载的数据分别对应于每一个字段，其中每个字段都有一个名字和一种类型。

一个proto文件中可以定义多个消息类型。

请注意，即使 `.proto` 文件中的字段名称使用带下划线的 小写形式，生成的 Go 字段名称始终使用驼峰式命名。大小写转换的工作方式如下

1. 第一个字母大写以导出。如果第一个字符是下划线，则将其删除并预先添加一个大写 X。
2. 如果内部下划线后跟一个小写字母，则删除下划线，并将后面的字母大写。

因此，proto 字段 `birth_year` 在 Go 中变为 `BirthYear`，而 `_birth_year_2` 变为 `XBirthYear_2`。

## 3.2 字段规则

`required`：消息体中必填的字段，不设置会导致编码异常，在protobuf2中使用，protobuf3中被删除。

`optional`：消息体中的可选字段。protobuf3没有required，optional等说明关键字，默认为optional。为了兼容proto2版本，推荐显式指定该字段。

`repeated`：消息体中可以重复的字段，重复的值的顺序会被保留在go中定义为切片。

`map`：键/值对字段类型。

## 3.3 消息号

- 在消息体的定义中，**每个字段都必须要有一个唯一的标识号**，标识号是\[1,2^29-1\]范围内的一个整数。
- 字段编号 `19,000` 到 `19,999` 已为 Protocol Buffers 实现保留。如果你在消息中使用这些保留的字段编号之一，protocol buffer 编译器将报错。

一旦你的消息类型**投入使用，此编号就不能更改**，因为它标识了消息 wire 格式中的字段。“更改”字段编号相当于删除该字段并创建一个具有相同类型但编号不同的新字段。有关如何正确执行此操作，请参阅删除字段。

## 3.4 重用字段编号的后果

重用字段编号会使解码 wire 格式消息变得模棱两可。

protobuf wire 格式是精简的，并且没有提供一种方法来检测使用一种定义编码并使用另一种定义解码的字段。

使用一个定义编码字段，然后使用不同的定义解码同一字段可能会导致

- 开发者时间浪费在调试上
- 解析/合并错误（最佳情况）
- PII/SPII 泄露
- 数据损坏

重用字段编号的常见原因

- 重新编号字段（有时是为了实现更美观的字段编号顺序而完成的）。重新编号实际上会删除并重新添加所有涉及重新编号的字段，从而导致不兼容的 wire 格式更改。
- 删除字段并且不保留该编号以防止将来重用。

## 3.5 删除字段

当你不再需要某个字段并且所有引用都已从客户端代码中删除时，你可以从消息中删除字段定义。但是必须保留已删除的字段编号。

如果任何未来的开发人员尝试使用这些保留的字段编号，protoc 编译器将生成错误消息。
```protobuf
message foo{
    reserved 2,3,4,9 to 11,12 to max; // 不能在一个reserved语句中混用字段名称和数值
    reserved "foo", "bar";
}
```

稍后重用旧字段名称通常是安全的，除非在使用 TextProto 或 JSON 编码时，字段名称会被序列化。为避免此风险，你可以将删除的字段名称添加到 `reserved` 列表中。

## 3.6 嵌套消息

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

**go会生成两个结构体 `PersonInfo`和 `PersonInfo_Person`**
## 3.7 服务定义

如果想将消息类型用在rpc系统中，可以在 **.proto文件中定义一个RPC服务接口**，protocol buffer编译器将会根据所选择的不同语言生成服务接口代码及存根。

```protobuf
service SayHello {  
  rpc SayHello(HelloRequest) returns (HelloResponse) {}  
}  
```

上述表示定义了一个RPC服务，该方法接受 `HelloRequest` 返回 `HelloResponse`

## 3.8 注释

- 单行注释：//
- 多行注释：/\*\*/
## 3.9 标量类型

标量消息字段可以具有以下类型之一 – 该表显示了 `.proto` 文件中指定的类型，以及自动生成的类中对应的类型

|Proto 类型|注释|
|---|---|
|double||
|float||
|int32|使用变长编码。编码负数效率低下 – 如果你的字段可能包含负值，请改用 sint32。|
|int64|使用变长编码。编码负数效率低下 – 如果你的字段可能包含负值，请改用 sint64。|
|uint32|使用变长编码。|
|uint64|使用变长编码。|
|sint32|使用变长编码。有符号整数值。这些比常规 int32 更有效地编码负数。|
|sint64|使用变长编码。有符号整数值。这些比常规 int64 更有效地编码负数。|
|fixed32|始终四个字节。如果值通常大于 228，则比 uint32 更有效。|
|fixed64|始终八个字节。如果值通常大于 256，则比 uint64 更有效。|
|sfixed32|始终四个字节。|
|sfixed64|始终八个字节。|
|bool||
|string|字符串必须始终包含 UTF-8 编码或 7 位 ASCII 文本，并且长度不能超过 232。|
|bytes|可能包含任何任意字节序列，长度不超过 232。|

| Proto 类型 | C++ 类型      | Java/Kotlin 类型[1] | Python 类型[3]                     | Go 类型   | Ruby 类型                | C# 类型      | PHP 类型            | Dart 类型 | Rust 类型     |
| -------- | ----------- | ----------------- | -------------------------------- | ------- | ---------------------- | ---------- | ----------------- | ------- | ----------- |
| double   | double      | double            | float                            | float64 | Float                  | double     | float             | double  | f64         |
| float    | float       | float             | float                            | float32 | Float                  | float      | float             | double  | f32         |
| int32    | int32_t     | int               | int                              | int32   | Fixnum 或 Bignum (根据需要) | int        | integer           | int     | i32         |
| int64    | int64_t     | long              | int/long[4]                      | int64   | Bignum                 | long       | integer/string[6] | Int64   | i64         |
| uint32   | uint32_t    | int[2]            | int/long[4]                      | uint32  | Fixnum 或 Bignum (根据需要) | uint       | integer           | int     | u32         |
| uint64   | uint64_t    | long[2]           | int/long[4]                      | uint64  | Bignum                 | ulong      | integer/string[6] | Int64   | u64         |
| sint32   | int32_t     | int               | int                              | int32   | Fixnum 或 Bignum (根据需要) | int        | integer           | int     | i32         |
| sint64   | int64_t     | long              | int/long[4]                      | int64   | Bignum                 | long       | integer/string[6] | Int64   | i64         |
| fixed32  | uint32_t    | int[2]            | int/long[4]                      | uint32  | Fixnum 或 Bignum (根据需要) | uint       | integer           | int     | u32         |
| fixed64  | uint64_t    | long[2]           | int/long[4]                      | uint64  | Bignum                 | ulong      | integer/string[6] | Int64   | u64         |
| sfixed32 | int32_t     | int               | int                              | int32   | Fixnum 或 Bignum (根据需要) | int        | integer           | int     | i32         |
| sfixed64 | int64_t     | long              | int/long[4]                      | int64   | Bignum                 | long       | integer/string[6] | Int64   | i64         |
| bool     | bool        | boolean           | bool                             | bool    | TrueClass/FalseClass   | bool       | boolean           | bool    | bool        |
| string   | std::string | String            | str/unicode[5]                   | string  | String (UTF-8)         | string     | string            | String  | ProtoString |
| bytes    | std::string | ByteString        | str (Python 2), bytes (Python 3) | []byte  | String (ASCII-8BIT)    | ByteString | string            | List    | ProtoBytes  |
## 3.10 默认字段值

当解析消息时，如果编码的消息字节不包含特定字段，则访问已解析对象中的该字段将返回该字段的默认值。默认值是类型特定的

- 对于字符串，默认值是空字符串。
- 对于字节，默认值是空字节。
- 对于布尔值，默认值是 false。
- 对于数值类型，默认值是零。
- 对于消息字段，该字段未设置。它的确切值与语言有关。请参阅[代码生成指南](https://protobuf.com.cn/reference/)以获取详细信息。
- 对于枚举，默认值是**第一个定义的枚举值**，它必须是 0。

重复字段的默认值是空（通常是相应语言中的空列表）。

map 字段的默认值是空（通常是相应语言中的空映射）。
## 3.11 枚举类型

```protobuf
enum Corpus {
  option allow_alias = true; // 开启允许重复枚举值
  CORPUS_UNSPECIFIED = 0; // 必须存在作为默认值，推荐为第一个元素，跟protobuf2兼容
  CORPUS_UNIVERSAL = 1;
  CORPUS_UNIVERSALS = 1;
  CORPUS_WEB = 2;
  CORPUS_IMAGES = 3;
  CORPUS_LOCAL = 4;
  CORPUS_NEWS = 5;
  CORPUS_PRODUCTS = 6 [deprecated = true]; // 不再使用这个值
  CORPUS_VIDEO = 7;
}

message SearchRequest {
  string query = 1;
  int32 page_number = 2;
  int32 results_per_page = 3;
  Corpus corpus = 4;   
}

```

枚举器常量必须在 32 位整数的范围内。由于 `enum` 值在 wire 上使用[varint 编码](https://protobuf.com.cn/programming-guides/encoding)，因此负值效率低下，因此不建议使用。

```protobuf
message Venue {
  enum Kind {
    KIND_UNSPECIFIED = 0;
    KIND_CONCERT_HALL = 1;
    KIND_STADIUM = 2;
    KIND_BAR = 3;
    KIND_OPEN_AIR_FESTIVAL = 4;
  }
  Kind kind = 1;
  // ...
}

// 一个类型和一系列具有该类型的常量
// 对于消息内的枚举（如上面的枚举），类型名称以消息名称开头
// 包级枚举直接使用枚举名
type Venue_Kind int32

const (
    Venue_KIND_UNSPECIFIED       Venue_Kind = 0
    Venue_KIND_CONCERT_HALL      Venue_Kind = 1
    Venue_KIND_STADIUM           Venue_Kind = 2
    Venue_KIND_BAR               Venue_Kind = 3
    Venue_KIND_OPEN_AIR_FESTIVAL Venue_Kind = 4
)

```
## 3.12 导入定义

可以通过_导入_来使用其他 `.proto` 文件中的定义。要导入另一个 `.proto` 文件的定义，请在文件顶部添加导入语句。

```go
import "myproject/other_protos.proto";
```

默认情况下，您只能使用直接导入的 `.proto` 文件中的定义。但是，有时您可能需要将 `.proto` 文件移动到新的位置。与其直接移动 `.proto` 文件并在一次更改中更新所有调用点，不如在旧位置放置一个占位符 `.proto` 文件，以使用 `import public` 概念将所有导入转发到新位置。

**请注意，公共导入功能在 Java、Kotlin、TypeScript、JavaScript、GCL 以及使用 protobuf 静态反射的 C++ 目标中不可用。**

| 特性            | 普通 `import` | `import public`              |
| ------------- | ----------- | ---------------------------- |
| ​**​依赖可见性​**​ | 仅当前文件可见     | 当前文件 ​**​及导入当前文件的其他文件​**​ 可见 |
| ​**​传递性​**​   | ❌ 不可传递      | ✅ 可传递                        |
| ​**​典型用途​**​  | 直接使用其他文件的定义 | 创建公共接口或聚合依赖                  |
```go
// new.proto
// All definitions are moved here


// old.proto
// This is the proto that all clients are importing.
import public "new.proto";
import "other.proto";

// client.proto
import "old.proto";
// You use definitions from old.proto and new.proto, but not other.proto

```
## 3.13 Oneof

如果您有一个包含许多 singular 字段的消息，并且最多同时设置一个字段，则可以使用 oneof 功能来强制执行此行为并节省内存。

Oneof 字段类似于可选字段，不同之处在于 oneof 中的所有字段共享内存，并且最多可以同时设置一个字段。设置 oneof 的任何成员都会自动清除所有其他成员。您可以使用特殊的 `case()` 或 `WhichOneof()` 方法（取决于您选择的语言）来检查 oneof 中设置了哪个值（如果有）。

请注意，如果设置了多个值，则由 proto 中的顺序确定的最后一个设置值将覆盖所有先前的值。

Oneof 字段的字段编号在封闭消息中必须是唯一的。

```protobuf
message SampleMessage {
  oneof test_oneof {
    string name = 4;
    SubMessage sub_message = 9;
  }
}
```

然后，将您的 oneof 字段添加到 oneof 定义中。您可以添加任何类型的字段，除了 `map` 字段和 `repeated` 字段。如果需要向 oneof 添加重复字段，可以使用包含重复字段的消息，Oneof 不能是 `repeated`。

```go
  
type HelloResponse struct {  
    state       protoimpl.MessageState `protogen:"open.v1"`  
    ResponseMsg string                 `protobuf:"bytes,1,opt,name=responseMsg,proto3" json:"responseMsg,omitempty"`  
    // Types that are valid to be assigned to TestOneof:  
    //    // *HelloResponse_One  
    // *HelloResponse_Tow  
    TestOneof     isHelloResponse_TestOneof `protobuf_oneof:"test_oneof"`  
    unknownFields protoimpl.UnknownFields  
    sizeCache     protoimpl.SizeCache  
}

  
type isHelloResponse_TestOneof interface {  
    isHelloResponse_TestOneof()  
}  
  
type HelloResponse_One struct {  
    One string `protobuf:"bytes,3,opt,name=one,proto3,oneof"`  
}  
  
type HelloResponse_Tow struct {  
    Tow string `protobuf:"bytes,4,opt,name=tow,proto3,oneof"`  
}  
  
func (*HelloResponse_One) isHelloResponse_TestOneof() {}  
  
func (*HelloResponse_Tow) isHelloResponse_TestOneof() {}
```
### 3.13.1 使用oneof类型

```go
package account;
message Profile {
  oneof avatar {
    string image_url = 1;
    bytes image_data = 2;
  }
}


type Profile struct {
    // Types that are valid to be assigned to Avatar:
    //  *Profile_ImageUrl
    //  *Profile_ImageData
    Avatar isProfile_Avatar `protobuf_oneof:"avatar"`
}

type Profile_ImageUrl struct {
        ImageUrl string
}
type Profile_ImageData struct {
        ImageData []byte
}


p1 := &account.Profile{
  Avatar: &account.Profile_ImageUrl{ImageUrl: "http://example.com/image.png"},
}

// imageData is []byte
imageData := getImageData()
p2 := &account.Profile{
  Avatar: &account.Profile_ImageData{ImageData: imageData},
}


switch x := m.Avatar.(type) {
case *account.Profile_ImageUrl:
    // Load profile image based on URL
    // using x.ImageUrl
case *account.Profile_ImageData:
    // Load profile image based on bytes
    // using x.ImageData
case nil:
    // The field is not set.
default:
    return fmt.Errorf("Profile.Avatar has unexpected type %T", x)
}

```

编译器还会生成 get 方法 `func (m *Profile) GetImageUrl() string` 和 `func (m *Profile) GetImageData() []byte`。每个 get 函数都返回该字段的值，如果未设置，则返回零值。
# 4 ProtoBuf限制

## 4.1 字段数量

仅包含奇异 proto 字段（例如 Boolean）的消息

- ~2100 个字段 (proto2)
- ~3100 (proto3，不使用可选字段)

由奇异字段（例如 Boolean）扩展的空消息

- ~4100 个字段 (proto2)

proto3 中不支持扩展。

要测试此限制，请创建一个字段数量超过上限的 proto 消息，并使用 Java proto 规则进行编译。此限制来自 JVM 规范。

## 4.2 枚举中值的数量

最低限制约为 1700 个值，在 Java 中。其他语言有不同的限制。

## 4.3 消息总大小

任何序列化形式的 proto 都必须 <2GiB，因为这是所有实现都支持的最大大小。建议限制请求和响应大小。

## 4.4 Proto 反序列化的深度限制

- Java: 100
- C++: 100
- Go: 10000（计划将其减少到 100）

如果您尝试反序列化深度超过深度限制的嵌套消息，则反序列化将失败。
# 5 语言风格

## 5.1 标准文件格式

- 保持行长为 80 个字符。
- 使用 2 个空格的缩进。
- 首选使用双引号表示字符串。

## 5.2 文件结构

文件应命名为 `lower_snake_case.proto`。

所有文件应按以下顺序排列

1. 许可证标头（如果适用）
2. 文件概述
3. 语法
4. 包
5. 导入（已排序）
6. 文件选项
7. 其他所有内容

## 5.3 包

使用点分隔的 lower_snake_case 名称作为包名称。

多词包名称可以是 lower_snake_case 或点分隔的（点分隔的包名称在大多数语言中作为嵌套包/命名空间发出）。

包名称应尝试成为基于项目名称的简短但唯一的名称。包名称不应是 Java 包（`com.x.y`）；而应使用 `x.y` 作为包，并根据需要使用 `java_package` 选项。

## 5.4 消息名称

对消息名称使用 TitleCase。

```protobuf
`message SongRequest { }`
```

## 5.5 字段名称

对字段名称（包括扩展）使用 snake_case。

对重复字段使用复数名称。

```protobuf
`string song_name = 1; repeated Song songs = 2;`
```

## 5.6 Oneof 名称

对 oneof 名称使用 lower_snake_case。

```protobuf
`oneof song_id {   string song_human_readable_id = 1;  int64 song_machine_id = 2; }`

```
## 5.7 枚举

对枚举类型名称使用 TitleCase。

对枚举值名称使用 UPPER_SNAKE_CASE。

```protobuf
`enum FooBar {   FOO_BAR_UNSPECIFIED = 0;  FOO_BAR_FIRST_VALUE = 1;  FOO_BAR_SECOND_VALUE = 2; }`
```

第一个列出的值应为零值枚举，并带有 `_UNSPECIFIED` 或 `_UNKNOWN` 后缀。此值可用作未知/默认值，并且应与您期望显式设置的任何语义值不同。有关未指定的枚举值的更多信息，请参阅 [Proto 最佳实践页面](https://protobuf.com.cn/best-practices/dos-donts#unspecified-enum)。

#### 5.7.1.1 枚举值前缀

枚举值在语义上被认为不受其包含的枚举名称的范围限制，因此两个同级枚举中的相同名称是不允许的。例如，以下内容将被 protoc 拒绝，因为在两个枚举中定义的 `SET` 值被认为在同一范围内

```protobuf
`enum CollectionType {   
COLLECTION_TYPE_UNSPECIFIED = 0;  
SET = 1;  
MAP = 2;  
ARRAY = 3; } 

enum TennisVictoryType {   
TENNIS_VICTORY_TYPE_UNSPECIFIED = 0;  
GAME = 1; 
SET = 2; 
MATCH = 3; }`
```

当枚举在文件的顶层定义时（未嵌套在消息定义内），名称冲突的风险很高；在这种情况下，同级包括在设置相同包的其他文件中定义的枚举，protoc 可能无法在代码生成时检测到冲突已发生。

为了避免这些风险，强烈建议执行以下操作之一

- 使用枚举名称（转换为 UPPER_SNAKE_CASE）作为每个值的前缀
- 将枚举嵌套在包含消息中

任一选项都足以减轻冲突风险，但首选带有前缀值的顶级枚举，而不是仅为减轻问题而创建消息。由于某些语言不支持在“struct”类型中定义枚举，因此首选前缀值可确保跨绑定语言的一致方法。

## 5.8 服务

对服务名称和方法名称使用 TitleCase。

```protobuf
`service FooService {   
rpc GetSomething(GetSomethingRequest) returns (GetSomethingResponse);  
rpc ListSomething(ListSomethingRequest) returns (ListSomethingResponse); }`
```