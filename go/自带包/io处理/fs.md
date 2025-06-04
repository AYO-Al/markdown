`io/fs` 包是 Go 1.16 引入的核心文件系统抽象层，提供了一套​**​统一接口​**​用于处理各种文件系统实现。

# 1 变量

```go
// fs 包定义的通用文件系统错误
var (
    // 无效参数错误 (错误信息: "invalid argument")
    // 在以下情况下可能发生:
    // - 无效的文件路径
    // - 无效的文件打开标志
    // - 不支持的操作
    // 应使用 errors.Is(err, fs.ErrInvalid) 进行检测
    ErrInvalid    = errInvalid()

    // 权限不足错误 (错误信息: "permission denied")
    // 在以下情况下可能发生:
    // - 尝试写入只读文件
    // - 访问受限目录
    // - 文件系统权限不足
    // 应使用 errors.Is(err, fs.ErrPermission) 进行检测
    ErrPermission = errPermission()

    // 文件已存在错误 (错误信息: "file already exists")
    // 在以下情况下可能发生:
    // - 尝试创建已存在的文件
    // - 创建目录时目标目录已存在
    // 应使用 errors.Is(err, fs.ErrExist) 进行检测
    ErrExist      = errExist()

    // 文件不存在错误 (错误信息: "file does not exist")
    // 在以下情况下可能发生:
    // - 尝试打开不存在的文件
    // - 操作不存在的文件
    // 应使用 errors.Is(err, fs.ErrNotExist) 进行检测
    ErrNotExist   = errNotExist()

    // 文件已关闭错误 (错误信息: "file already closed")
    // 在以下情况下可能发生:
    // - 在已关闭的文件上执行操作
    // - 使用已关闭的文件系统
    // 应使用 errors.Is(err, fs.ErrClosed) 进行检测
    ErrClosed     = errClosed()
)

// SkipAll 用于在 WalkDirFunc 中停止目录遍历
// 当从 WalkDirFunc 回调函数中返回 SkipAll 时，表示:
// - 终止整个文件系统遍历
// - 跳过所有剩余文件和目录
// - 停止进一步回调
// 该值不作为错误返回
var SkipAll = errors.New("skip everything and stop the walk")

// SkipDir 用于在 WalkDirFunc 中跳过当前目录
// 当从 WalkDirFunc 回调函数中返回 SkipDir 时，表示:
// - 跳过当前目录的所有内容
// - 继续遍历同级目录
// - 仅对目录返回值有效
// 该值不作为错误返回
var SkipDir = errors.New("skip this directory")

```
# 2 函数
## 2.1 func FormatDirEntry(dir DirEntry) string

​**​作用​**​：格式化目录条目信息为可读字符串

**参数​**​：

- `dir DirEntry`：目录条目对象

​**​返回值​**​：

- `string`：格式化后的字符串，包含名称、类型和模式信息

```go
func listDirectory(fsys fs.FS, path string) {
    entries, _ := fs.ReadDir(fsys, path)
    for _, entry := range entries {
        fmt.Println(fs.FormatDirEntry(entry))
        // 输出示例: -rw-r--r--  755 bytes  config.txt (file)
        //          drwxr-xr-x        0 bytes  subdir (directory)
    }
}
```

**注意​**​：

- 主要用于调试和日志输出
- 实际应用中使用`entry.Info()`获取完整信息
- 格式化方式可能随Go版本改变
## 2.2 func FormatFileInfo(info FileInfo) string

​**​作用​**​：格式化文件信息为可读字符串

**参数​**​：

- `info FileInfo`：文件信息对象

​**​返回值​**​：

- `string`：格式化后的字符串，包含模式、大小、修改时间和名称

```go
func fileStats(fsys fs.FS, path string) {
    info, _ := fs.Stat(fsys, path)
    fmt.Println(fs.FormatFileInfo(info))
    // 输出示例: -rw-r--r--  1024 bytes  Mon Jan 2 15:04:05 2023  data.txt
}
```

**注意​**​：

- 主要用于命令行工具和调试输出
- 时间格式固定为本地时间格式
- 实际应用中应使用`info`对象属性获取特定信息
## 2.3 func Glob(fsys FS, pattern string) (matches []string, err error)

​**​作用​**​：查找文件系统中匹配模式的文件

**参数​**​：

- `fsys FS`：文件系统对象
- `pattern string`：通配符模式（支持`*`、`?`、`[a-z]`等）

​**​返回值​**​：

- `matches []string`：匹配的文件路径列表（相对路径）
- `err error`：可能错误

​**​错误情况​**​：

- `fs.ErrNotExist`：模式匹配未找到文件
- `fs.ErrPermission`：目录访问权限不足
- `ErrInvalidPattern`：无效模式语法

```go
func findConfigFiles(fsys fs.FS) {
    matches, err := fs.Glob(fsys, "config*.{json,yaml,toml}")
    if errors.Is(err, fs.ErrNotExist) {
        fmt.Println("未找到配置文件")
        return
    }
    
    for _, file := range matches {
        fmt.Println("找到配置文件:", file)
    }
}
```

**注意​**​：

- 使用`filepath.Match`语法规则
- 路径分隔符始终为`/`
- 结果按路径字母顺序排序
- 不支持`**`递归匹配
## 2.4 func ReadFile(fsys FS, name string) ([]byte, error)

​**​作用​**​：读取文件系统中的文件内容

**参数​**​：

- `fsys FS`：文件系统对象
- `name string`：文件路径（相对路径）

​**​返回值​**​：

- `[]byte`：文件内容字节切片
- `error`：可能错误

​**​错误情况​**​：

- `fs.ErrNotExist`：文件不存在
- `fs.ErrPermission`：文件读取权限不足
- `fs.ErrInvalid`：路径无效或为目录

```go
func loadTemplate(fsys fs.FS) string {
    // 读取模板文件
    content, err := fs.ReadFile(fsys, "templates/main.html")
    if err != nil {
        // 回退到默认内容
        if errors.Is(err, fs.ErrNotExist) {
            return "<html>默认模板</html>"
        }
        panic(fmt.Errorf("模板读取失败: %w", err))
    }
    
    // 验证内容
    if len(content) == 0 {
        return "空模板"
    }
    
    return string(content)
}
```

**​注意​**​：

- 一次性读取整个文件，不适合大文件
- 文件路径使用正向斜杠`/`
- 内存文件系统可能返回非标准错误
- 文件内容不会缓存
## 2.5 func ValidPath(name string) bool

​**​作用​**​：验证路径字符串是否有效

**参数​**​：

- `name string`：要验证的路径

​**​返回值​**​：

- `bool`：路径是否有效

​**​规则​**​：

- 非空字符串
- 不包含`/`连续出现
- 不以`/`开头（相对路径）
- 不包含U+0000（空字符）
- 不包含`.`或`..`路径段

```go
func sanitizeUploadPath(path string) (string, error) {
    // 清理路径
    cleanPath := filepath.Clean(path)
    
    // 验证有效性
    if !fs.ValidPath(cleanPath) {
        return "", errors.New("无效文件路径")
    }
    
    // 额外安全检查
    if strings.Contains(cleanPath, "..") {
        return "", errors.New("路径包含上级引用")
    }
    
    return cleanPath, nil
}
```

**注意​**​：

- 仅验证语法有效性，不检查路径是否存在
- 设计用于`fs.WalkDir`等函数的前置检查
- 无效路径示例：
    - `../file.txt`
    - `/absolute/path`
    - `dir//file`
    - `bad\path`（含有反斜杠）
## 2.6 func WalkDir(fsys FS, root string, fn WalkDirFunc) error

​**​作用​**​：递归遍历文件系统树

**参数​**​：

- `fsys FS`：文件系统对象
- `root string`：遍历起始路径
- `fn WalkDirFunc`：遍历回调函数

```go
type WalkDirFunc func(path string, d DirEntry, err error) error
```

**回调函数返回值行为​**​：

- `nil`：继续遍历
- `SkipDir`：跳过当前目录
- `SkipAll`：立即终止整个遍历
- 其他错误：终止遍历并返回该错误

**错误情况​**​：

- 权限错误（`fs.ErrPermission`）
- 无效路径（`fs.ErrInvalid`）
- 回调函数返回的错误

```go
func calculateTotalSize(fsys fs.FS) (int64, error) {
    var totalSize int64
    
    err := fs.WalkDir(fsys, ".", func(path string, d fs.DirEntry, err error) error {
        // 处理遍历错误
        if err != nil {
            // 记录错误但继续遍历
            log.Printf("跳过 %s: %v", path, err)
            return nil
        }
        
        // 跳过隐藏文件
        if strings.HasPrefix(d.Name(), ".") {
            if d.IsDir() {
                return fs.SkipDir // 跳过隐藏目录
            }
            return nil // 仅跳过文件
        }
        
        // 计算文件大小
        if !d.IsDir() {
            info, _ := d.Info()
            totalSize += info.Size()
            fmt.Printf("添加 %s (%s)\n", path, humanize.Bytes(uint64(info.Size())))
        }
        
        return nil
    })
    
    if errors.Is(err, fs.ErrPermission) {
        log.Println("警告：部分目录未扫描")
        return totalSize, nil
    }
    
    return totalSize, err
}
```

**注意​**​：

- 遍历顺序为字典序
- 总是先处理文件再处理目录内容
- 对大文件系统可能效率低
- 使用`SkipDir`跳过目录
- 使用`SkipAll`提前终止遍历
# 3 类型
## 3.1 DirEntry接口

`DirEntry` 接口表示从目录中读取的条目，提供文件/子目录的基本信息，避免立即调用`Stat()`的系统开销。

```go
type DirEntry interface {
    // 返回文件或子目录的名称（不含路径）
    // 示例："file.txt" 而不是 "/home/user/file.txt"
    Name() string
    
    // 判断条目是否为目录
    // 返回值：true=目录, false=文件或其他
    IsDir() bool
    
    // 返回文件类型位（FileMode的子集）
    // 包含的模式位：ModeDir | ModeSymlink | ModeNamedPipe | ModeSocket | ModeDevice | ModeCharDevice | ModeIrregular
    Type() FileMode
    
    // 获取完整的文件信息（可能涉及系统调用）
    // 返回值：FileInfo对象和可能的错误
    // 错误情况：文件已删除/重命名返回ErrNotExist
    Info() (FileInfo, error)
}
```

### 3.1.1 func FileInfoToDirEntry(info FileInfo) DirEntry

​**​作用​**​：将`FileInfo`对象转换为`DirEntry`条目

​**​参数​**​：

- `info FileInfo`：文件信息对象

​**​返回值​**​：

- `DirEntry`：转换后的目录条目
- 当`info`为`nil`时返回`nil`

**使用场景​**​：

- 需要将已存在的`FileInfo`对象用在期望`DirEntry`的API中
- 避免重复查询文件信息

**注意事项​**​：

- 转换后的`DirEntry`不包含原始路径信息
- `Info()`方法始终返回转换时使用的`FileInfo`，即使文件已修改
- 不适用于需要实时文件状态的场景
### 3.1.2 func ReadDir(fsys FS, name string) (\[\]DirEntry, error)

​**​作用​**​：读取目录内容并按文件名排序

​**​参数​**​：

- `fsys FS`：文件系统实现
- `name string`：目录路径（相对路径）

​**​返回值​**​：

- `[]DirEntry`：目录条目切片（按文件名升序排序）
- `error`：可能错误
## 3.2 FS接口

`FS` 是文件系统的抽象接口，提供对分层文件系统的访问能力，是所有文件系统操作的基础接口。

```go
type FS interface {
    Open(name string) (File, error)
}

```
### 3.2.1 关键方法 `Open`

​**​作用​**​：打开指定路径的文件  
​**​声明​**​：`Open(name string) (File, error)`  
​**​参数​**​：

- `name string`：文件路径（必须满足 `ValidPath(name)`）

​**​返回值​**​：

- `File`：打开的文件对象
- `error`：错误对象（通常为 `*PathError` 类型）

​**​错误情况​**​：

- `*PathError` 类型错误，其中：
    - `Op` 字段值为 `"open"`
    - `Path` 字段为传入的 `name` 参数
    - `Err` 字段描述具体问题：
        - `ErrInvalid`：路径无效（不满足 `ValidPath(name)`）
        - `ErrNotExist`：文件不存在
        - `ErrPermission`：权限不足

​**​实现要求​**​：

1. 必须返回满足 `io.Reader` 接口的文件对象
2. 文件使用后必须调用 `Close()` 释放资源
3. 路径必须通过 `ValidPath(name)` 验证
4. 错误信息必须封装为 `*PathError`
### 3.2.2 func Sub(fsys FS, dir string) (FS, error)

​**​作用​**​：返回以指定目录为根的文件系统视图

**参数​**​：

- `fsys FS`：父文件系统
- `dir string`：子目录路径（相对路径）

​**​返回值​**​：

- `FS`：新的子目录文件系统
- `error`：可能的错误

​**​实现原理​**​：

1. 如果 `dir` 是 `.`，直接返回 `fsys`
2. 如果 `fsys` 实现了 `SubFS` 接口，调用 `fsys.Sub(dir)`
3. 否则返回包装的 `FS`，其 `Open(name)` 调用 `fsys.Open(path.Join(dir, name))`

​**​错误情况​**​：

- `*PathError` 类型错误：
    - `ErrNotExist`：子目录不存在
    - `ErrInvalid`：子目录路径无效
    - `ErrPermission`：无访问权限
## 3.3 File接口

`File` 接口是文件系统中最核心的接口之一，提供对单个文件的访问能力，是标准 `os.File` 的抽象版本。

```go
type File interface {
    // 获取文件元数据信息
    Stat() (FileInfo, error)
    
    // 从文件读取数据到字节切片
    Read([]byte) (int, error)
    
    // 关闭文件并释放资源
    Close() error
}
```
## 3.4 FileInfo接口

`FileInfo` 接口提供文件的元数据信息，是文件系统中最基础也最核心的接口之一。

```go
type FileInfo interface {
    // 文件的基本名称（不含路径）
    Name() string
    
    // 文件大小（字节），对于非普通文件（如目录），其返回值依赖系统
    Size() int64
    
    // 文件权限和类型信息（FileMode）
    Mode() FileMode
    
    // 文件的最后修改时间
    ModTime() time.Time
    
    // 是否是目录（等效于 Mode().IsDir()）
    IsDir() bool
    
    // 返回底层数据源（系统特定信息）
    Sys() any
}
```

## 3.5 func Stat(fsys FS, name string) (FileInfo, error)

-  核心作用

高效获取文件的元数据信息，避免手动打开文件并调用 `Stat()`。

-  参数说明

    - `fsys FS`：文件系统对象
    - `name string`：文件路径（相对路径）

-  返回值

    - `FileInfo`：文件信息对象
    - `error`：可能错误
## 3.6 FileMode类型

`FileMode` 类型是Go文件系统中处理文件类型和权限的核心工具，它提供了跨平台的统一表示方式。

```go
// FileMode 表示文件的模式和权限位
// 采用 uint32 类型存储，位定义兼容所有系统
type FileMode uint32

// 文件类型模式位常量
const (
    // 类型位（高16位）
    ModeDir        FileMode = 1 << (32 - 1 - iota) // d: 目录 (1<<31)
    ModeAppend                                     // a: 仅追加
    ModeExclusive                                  // l: 独占访问
    ModeTemporary                                  // T: 临时文件(Plan 9专用)
    ModeSymlink                                    // L: 符号链接 (1<<27)
    ModeDevice                                     // D: 设备文件
    ModeNamedPipe                                  // p: 命名管道(FIFO)
    ModeSocket                                     // S: Unix域套接字
    ModeSetuid                                     // u: setuid位 (1<<22)
    ModeSetgid                                     // g: setgid位
    ModeCharDevice                                 // c: Unix字符设备
    ModeSticky                                     // t: sticky位
    ModeIrregular                                  // ?: 非常规文件
    
    // 类型位掩码
    ModeType = ModeDir | ModeSymlink | ModeNamedPipe | 
               ModeSocket | ModeDevice | ModeCharDevice | 
               ModeIrregular
    
    // 权限位掩码（低9位）
    ModePerm FileMode = 0777 // Unix标准权限位
)
```

### 3.6.1 func (m FileMode) IsRegular() bool

​**​作用​**​：检查是否为普通文件  
​**​实现​**​：`return m&ModeType == 0`
### 3.6.2 func (m FileMode) Type() FileMode

​**​作用​**​：提取文件类型位
### 3.6.3 func (m FileMode) String() string

​**​作用​**​：生成UNIX风格权限字符串  
​**​格式​**​：类型位 + 权限位（9字符）
### 3.6.4 func (m FileMode) Perm() FileMode

​**​作用​**​：提取Unix权限位（移除类型位）

```go
func manageSpecialBits(path string) error {
    info, err := os.Stat(path)
    if err != nil {
        return err
    }
    
    mode := info.Mode()
    
    // 安全清理 - 移除特殊执行位
    if mode&(fs.ModeSetuid|fs.ModeSetgid|fs.ModeSticky) != 0 {
        safeMode := mode.Perm()
        
        // 保留必要权限: 目录保留sticky位
        if mode.IsDir() {
            safeMode |= (mode & fs.ModeSticky)
        }
        
        return os.Chmod(path, safeMode)
    }
    
    return nil
}
```