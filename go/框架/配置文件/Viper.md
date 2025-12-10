
[Viper](https://github.com/spf13/viper)是适用于Go应用程序的完整配置解决方案。它被设计用于在应用程序中工作，并且可以处理所有类型的配置需求和格式。

- 安装
```go
go get -u github.com/spf13/viper
```

# 1 介绍

Viper是适用于Go应用程序（包括`Twelve-Factor App`）的完整配置解决方案。它被设计用于在应用程序中工作，并且可以处理所有类型的配置需求和格式。它支持以下特性：

- 设置默认值
- 从`JSON`、`TOML`、`YAML`、`HCL`、`envfile`和`Java properties`格式的配置文件读取配置信息
- 实时监控和重新读取配置文件（可选）
- 从环境变量中读取
- 从远程配置系统（etcd或Consul）读取并监控配置变化
- 从命令行参数读取配置
- 从buffer读取配置
- 显式配置值
# 2 为什么选择Viper

Viper能够为你执行下列操作：

1. 查找、加载和反序列化`JSON`、`TOML`、`YAML`、`HCL`、`INI`、`envfile`和`Java properties`格式的配置文件。
2. 提供一种机制为你的不同配置选项设置默认值。
3. 提供一种机制来通过命令行参数覆盖指定选项的值。
4. 提供别名系统，以便在不破坏现有代码的情况下轻松重命名参数。
5. 当用户提供了与默认值相同的命令行或配置文件时，可以很容易地分辨出它们之间的区别。

Viper会按照下面的优先级。每个项目的优先级都高于它下面的项目:

- 显示调用`Set`设置值
- 命令行参数（flag）
- 环境变量
- 配置文件
- key/value存储
- 默认值
**注意：Viper配置的key是大小写不敏感的**
# 3 把值存入viper
## 3.1 设置默认值

一个好的配置系统应该支持默认值。键不需要默认值，但如果没有通过配置文件、环境变量、远程配置或命令行标志（flag）设置键，则默认值非常有用。

```go
viper.SetDefault("ContentDir", "content")
viper.SetDefault("LayoutDir", "layouts")
viper.SetDefault("Taxonomies", map[string]string{"tag": "tags", "category": "categories"})
```
## 3.2 读取配置文件

Viper需要最少知道在哪里查找配置文件的配置。Viper支持`JSON`、`TOML`、`YAML`、`HCL`、`envfile`和`Java properties`格式的配置文件。Viper可以搜索多个路径，但目前单个Viper实例只支持单个配置文件。Viper不默认任何配置搜索路径，将默认决策留给应用程序。

```go
viper.SetConfigFile("./config.yaml") // 指定配置文件路径

viper.SetConfigName("config") // 配置文件名称(无扩展名)
viper.SetConfigType("yaml") // 如果配置文件的名称中没有扩展名，则需要配置此项
viper.AddConfigPath("/etc/appname/")   // 查找配置文件所在的路径
viper.AddConfigPath("$HOME/.appname")  // 多次调用以添加多个搜索路径
viper.AddConfigPath(".")               // 还可以在工作目录中查找配置
err := viper.ReadInConfig() // 查找并读取配置文件
if err != nil { // 处理读取配置文件的错误
	panic(fmt.Errorf("Fatal error config file: %s \n", err))
}
```

同级目录下的同名文件，会按照支持顺序读取

```go
/*
conf/
    mysql.json
    mysql.yaml
*/

// 源码定义
var SupportedExts = []string{"json", "toml", "yaml", "yml", "properties", "props", "prop", "hcl", "tfvars", "dotenv", "env", "ini"}

viper.SetConfigName("mysql")  
viper.SetConfigType("yaml") 
viper.AddConfigPath("conf")

/* 
SetConfigType只是设置配置文件解析格式，并不会去读取指定后缀的配置文件
- 文件无后缀
- 从io流中读取配置
- 从远程读取配置时使用
*/
```

在加载配置文件出错时，你可以像下面这样处理找不到配置文件的特定情况：

```go
if err := viper.ReadInConfig(); err != nil {
    if _, ok := err.(viper.ConfigFileNotFoundError); ok {
        // 配置文件未找到错误；如果需要可以忽略
    } else {
        // 配置文件被找到，但产生了另外的错误
    }
}

// 配置文件找到并成功解析

```

 你也可以有不带扩展名的文件，并以编程方式指定其格式。对于位于用户`$HOME`目录中的配置文件没有任何扩展名，如`.bashrc`
## 3.3 合并配置文件

**用途**：与 `ReadInConfig` 类似，但**合并**配置内容到现有的配置存储中，而不是覆盖。  
**适用场景**：需要从多个配置文件加载配置（例如 `base.yaml` + `override.yaml`）。

```go
// MergeInConfig() error

// 先加载基础配置
viper.SetConfigName("base")
viper.AddConfigPath(".")
err := viper.ReadInConfig()
if err != nil {
    panic(err)
}

// 再加载覆盖配置并合并
viper.SetConfigName("override")
err = viper.MergeInConfig() // 将 override.yaml 的内容合并到当前配置
if err != nil {
    panic(err)
}
```
## 3.4 读取环境变量

### 3.4.1 启用环境变量自动绑定

使用 `AutomaticEnv()` 让 Viper ​**自动绑定所有环境变量**到配置键，键名默认转换为大写+下划线格式：

```go
viper.AutomaticEnv() // 自动绑定所有环境变量
```

```bash
# 环境变量
export PORT=8080
export DB_HOST=localhost
```

```go
// 代码中访问
port := viper.GetInt("PORT")       // 8080
dbHost := viper.GetString("DB_HOST") // "localhost"
```

### 3.4.2 ​设置环境变量前缀

通过 `SetEnvPrefix` 设置前缀，避免与其他应用的环境变量冲突：

```go
viper.SetEnvPrefix("APP") // 环境变量需以 APP_ 开头
viper.AutomaticEnv()
```

```bash
export APP_PORT=8080      # 对应键名 PORT
export APP_DB_HOST=localhost # 对应键名 DB_HOST
```

### 3.4.3 ​手动绑定指定环境变量

使用 `BindEnv` 将特定环境变量绑定到配置键（支持多个备选环境变量名）：

```go
viper.BindEnv("user.name", "APP_USERNAME", "USERNAME") 
// 按顺序查找环境变量：APP_USERNAME → USERNAME
```

### 3.4.4 ​读取嵌套配置的环境变量

Viper 支持用 `.` 分隔的嵌套键名，对应环境变量需转换为 ​**大写+下划线** 格式：

```go
// 访问 database.port
port := viper.GetInt("database.port")
```

```bash
# 对应环境变量
export DATABASE_PORT=3306
```

# 4 写入配置文件

- WriteConfig - 将当前的`viper`配置写入预定义的路径并覆盖（如果存在的话）。如果没有预定义的路径，则报错。
- SafeWriteConfig - 将当前的`viper`配置写入预定义的路径。如果没有预定义的路径，则报错。如果存在，将不会覆盖当前的配置文件。
- WriteConfigAs - 将当前的`viper`配置写入给定的文件路径。将覆盖给定的文件(如果它存在的话)。
- SafeWriteConfigAs - 将当前的`viper`配置写入给定的文件路径。不会覆盖给定的文件(如果它存在的话)。

 根据经验，标记为`safe`的所有方法都不会覆盖任何文件，而是直接创建（如果不存在），而默认行为是创建或截断。

```go
viper.WriteConfig() // 将当前配置写入“viper.AddConfigPath()”和“viper.SetConfigName”设置的预定义路径
viper.SafeWriteConfig()
viper.WriteConfigAs("/path/to/my/.config")
viper.SafeWriteConfigAs("/path/to/my/.config") // 因为该配置文件写入过，所以会报错Config File "conf/mysql.yaml" Already Exists

viper.SafeWriteConfigAs("/path/to/my/.other_config")
```
## 4.1 监控并重新读取文件

Viper支持在运行时实时读取配置文件的功能。

只需告诉viper实例watchConfig。可选地，你可以为Viper提供一个回调函数，以便在每次发生更改时运行。

```go
viper.WatchConfig()
viper.OnConfigChange(func(in fsnotify.Event) {
  // 配置文件发生变更之后会调用的回调函数
	fmt.Println("Config file changed:", e.Name)
})

/*
in.Op：表示事件的操作类型，是一个位掩码类型的值（但通常单次事件对应单一操作）。
- 常见值：
    - `fsnotify.Write`：文件内容被修改。
    - `fsnotify.Create`：文件被创建。
    - `fsnotify.Remove`：文件被删除。
    - `fsnotify.Rename`：文件被重命名。
    - `fsnotify.Chmod`：文件权限被修改。
in.String()：将事件信息格式化为 ​**易读的字符串**，包含操作类型和文件名。
in.Name：返回触发事件的 ​**文件完整路径**。
in.Has(op)：判断是否有对应事件发生
*/

```
## 4.2 从io.Reader读取配置

Viper预先定义了许多配置源，如文件、环境变量、标志和远程K/V存储，但你不受其约束。你还可以实现自己所需的配置源并将其提供给viper。

```go
viper.SetConfigType("yaml") // 或者 viper.SetConfigType("YAML")

// 任何需要将此配置添加到程序中的方法。
var yamlExample = []byte(`
Hacker: true
name: steve
hobbies:
- skateboarding
- snowboarding
- go
clothing:
  jacket: leather
  trousers: denim
age: 35
eyes : brown
beard: true
`)

viper.ReadConfig(bytes.NewBuffer(yamlExample))

viper.Get("name") // 这里会得到 "steve"

```
## 4.3 覆盖设置

```go
viper.Set("Verbose", true)
viper.Set("LogFile", LogFile)
```
## 4.4 别名设置

```go
// func RegisterAlias(alias, key string)
viper.RegisterAlias("3", "1")
```
# 5 获取值

在Viper中，有几种方法可以根据值的类型获取值。存在以下功能和方法:

- `Get(key string) : interface{}`
- `GetBool(key string) : bool`
- `GetFloat64(key string) : float64`
- `GetInt(key string) : int`
- `GetIntSlice(key string) : []int`
- `GetString(key string) : string`
- `GetStringMap(key string) : map[string]interface{}`
- `GetStringMapString(key string) : map[string]string`
- `GetStringSlice(key string) : []string`
- `GetTime(key string) : time.Time`
- `GetDuration(key string) : time.Duration`
- `IsSet(key string) : bool`
- `AllSettings() : map[string]interface{}`

需要认识到的一件重要事情是，**每一个Get方法在找不到值的时候都会返回零值**。为了检查给定的键是否存在，提供了`IsSet()`方法。
## 5.1 访问嵌套的键

访问器方法也接受深度嵌套键的格式化路径。例如，如果加载下面的JSON文件：

```json
{
    "host": {
        "address": "localhost",
        "port": 5799
    },
    "datastore": {
        "metric": {
            "host": "127.0.0.1",
            "port": 3099
        },
        "warehouse": {
            "host": "198.0.0.1",
            "port": 2112
        }
    }
}
```

Viper可以通过传入`.`分隔的路径来访问嵌套字段：

```go
GetString("datastore.metric.host") // (返回 "127.0.0.1")
```
## 5.2 反序列化

你还可以选择将所有或特定的值解析到结构体、map等。

有两种方法可以做到这一点：

- `Unmarshal(rawVal interface{}) : error`
- `UnmarshalKey(key string, rawVal interface{}) : error`

举个例子：

```go
type config struct {
	Port int
	Name string
	PathMap string `mapstructure:"path_map"`
}

var C config

err := viper.Unmarshal(&C)
if err != nil {
	t.Fatalf("unable to decode into struct, %v", err)
}
```

如果你想要解析那些键本身就包含`.`(默认的键分隔符）的配置，你需要修改分隔符：

```go
v := viper.NewWithOptions(viper.KeyDelimiter("::"))

v.SetDefault("chart::values", map[string]interface{}{
    "ingress": map[string]interface{}{
        "annotations": map[string]interface{}{
            "traefik.frontend.rule.type":                 "PathPrefix",
            "traefik.ingress.kubernetes.io/ssl-redirect": "true",
        },
    },
})

type config struct {
	Chart struct{
        Values map[string]interface{}
    }
}

var C config

v.Unmarshal(&C)
```

# 6 使用多个viper实例

你还可以在应用程序中创建许多不同的viper实例。每个都有自己独特的一组配置和值。每个人都可以从不同的配置文件，key value存储区等读取数据。每个都可以从不同的配置文件、键值存储等中读取。viper包支持的所有功能都被镜像为viper实例的方法。

例如：

```go
x := viper.New()
y := viper.New()

x.SetDefault("ContentDir", "content")
y.SetDefault("ContentDir", "foobar")

//...
```

当使用多个viper实例时，由用户来管理不同的viper实例。
# 7 远程配置中心读取

## 7.1 **`ReadRemoteConfig() error`**

**用途**：从远程配置中心（如 ​**etcd、Consul、AWS Parameter Store** 等）加载配置。  
**依赖**：需要先配置远程访问的地址和认证信息。

```go
viper.AddRemoteProvider("etcd", "http://127.0.0.1:4001", "/config/app.yaml")
viper.SetConfigType("yaml") // 必须明确指定远程配置的格式
err := viper.ReadRemoteConfig()
if err != nil {
    panic(err)
}
```

## 7.2  `WatchRemoteConfig() error`

**用途**：启动后台监控，当远程配置发生变化时自动重新加载。  

```go
viper.AddRemoteProvider(...) // 同上
viper.SetConfigType("yaml")
err := viper.ReadRemoteConfig()
if err != nil {
    panic(err)
}

// 启动监控
err = viper.WatchRemoteConfig()
if err != nil {
    panic(err)
}

// 监听配置变化事件
viper.OnConfigChange(func(e fsnotify.Event) {
    fmt.Println("远程配置已更新:", e.Name)
})
```
