在Go语言中，`os`包提供了操作系统功能的接口。它的设计是Unix-like的，但错误处理是Go风格的；它提供了与操作系统平台无关的接口。这个包主要用于文件操作、环境变量、命令行参数、进程管理等。
# 1 常量

- **文件打开标志**：用于 `OpenFile()` 函数的文件操作控制（按位或组合使用）：

```go
const (
    O_RDONLY int = syscall.O_RDONLY // 只读模式（必须三选一）
    O_WRONLY int = syscall.O_WRONLY // 只写模式（必须三选一）
    O_RDWR   int = syscall.O_RDWR   // 读写模式（必须三选一）
    
    O_APPEND int = syscall.O_APPEND // 追加写入（不覆盖原有内容）
    O_CREATE int = syscall.O_CREAT  // 文件不存在时创建
    O_EXCL   int = syscall.O_EXCL   // 与 O_CREATE 同用，要求文件必须不存在（原子性创建）
    O_SYNC   int = syscall.O_SYNC   // 同步 I/O（写入直接刷盘）
    O_TRUNC  int = syscall.O_TRUNC  // 打开时清空文件
)
```

**组合示例：**

```go
// 以读写模式打开文件，不存在则创建，追加写入
file, err := os.OpenFile("log.txt", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0644)
```

- **文件模式**：描述文件类型和权限的位掩码（继承自 `fs` 包）

```go
const (
    ModeDir        = fs.ModeDir        // 目录 (d)
    ModeAppend     = fs.ModeAppend     // 仅追加 (a)
    ModeExclusive  = fs.ModeExclusive  // 独占使用 (l)
    ModeTemporary  = fs.ModeTemporary  // 临时文件 (T, Plan9 专用)
    ModeSymlink    = fs.ModeSymlink    // 符号链接 (L)
    ModeDevice     = fs.ModeDevice     // 设备文件 (D)
    ModeNamedPipe  = fs.ModeNamedPipe  // 命名管道 (p)
    ModeSocket     = fs.ModeSocket     // Unix 套接字 (S)
    ModeSetuid     = fs.ModeSetuid     // setuid 位 (u)
    ModeSetgid     = fs.ModeSetgid     // setgid 位 (g)
    ModeCharDevice = fs.ModeCharDevice // 字符设备 (c, 需与 ModeDevice 同用)
    ModeSticky     = fs.ModeSticky     // sticky 位 (t)
    ModeIrregular  = fs.ModeIrregular  // 非规则文件 (?)

    ModeType = fs.ModeType  // 文件类型位掩码
    ModePerm = fs.ModePerm  // 权限位掩码 (0o777)
)
```
# 2 变量

- **预定义错误变量**：这些错误提供了标准化的错误检查方式，可与 `errors.Is()` 配合使用

```go
var (
    // 无效参数（如 nil 文件指针）
    ErrInvalid = fs.ErrInvalid         // "invalid argument"
    
    // 权限不足（如只读文件尝试写入）
    ErrPermission = fs.ErrPermission   // "permission denied"
    
    // 文件已存在（与 O_EXCL 标志冲突）
    ErrExist = fs.ErrExist              // "file already exists"
    
    // 文件不存在（常见于 Open 操作）
    ErrNotExist = fs.ErrNotExist        // "file does not exist"
    
    // 文件已关闭（对已关闭文件操作）
    ErrClosed = fs.ErrClosed            // "file already closed"
    
    // 文件不支持超时控制（如管道）
    ErrNoDeadline = errNoDeadline()     // "file type does not support deadline"
    
    // I/O 操作超时
    ErrDeadlineExceeded = errDeadlineExceeded() // "i/o timeout"
)
```

- **示例**：

```go
file, err := os.Open("data.txt")
if errors.Is(err, os.ErrNotExist) {
    fmt.Println("文件不存在") // 处理特定错误
}
```

- **标准输入/输出流**：预定义的全局文件对象，对应操作系统的标准数据流

```go
var (
    Stdin  = NewFile(uintptr(syscall.Stdin), "/dev/stdin")   // 标准输入 (fd 0)
    Stdout = NewFile(uintptr(syscall.Stdout), "/dev/stdout") // 标准输出 (fd 1)
    Stderr = NewFile(uintptr(syscall.Stderr), "/dev/stderr") // 标准错误 (fd 2)
)
```
# 3 函数

## 3.1 func Mkdir(name string, perm FileMode) error

​**​功能​**​：创建单级目录  
​**​权限​**​：`perm` 为 Unix 风格权限位（如 0755）

```go
// 示例：创建目录 
err := os.Mkdir("my_dir", 0750) // 权限：所有者rwx，同组用户rx 
if err != nil {     
    // 检查是否为"目录已存在"错误     
    if errors.Is(err, os.ErrExist) {         
        fmt.Println("目录已存在")     
    } else {         
        log.Fatal("创建失败:", err)     
        } 
}
```

​**​注意​**​：

- 仅创建单级目录
- 父目录不存在会返回 `IsNotExist` 错误
- Windows 系统下权限位仅控制只读属性
## 3.2 func MkdirAll(path string, perm FileMode) error

​**​功能​**​：递归创建多级目录（类似 `mkdir -p`）

```go
// 示例：创建嵌套目录 
path := "/tmp/parent/child/grandchild" 
err := os.MkdirAll(path, 0750) 
if err != nil {     
    log.Fatal("创建失败:", err) // 自动创建所有不存在的父目录 
    } 
fmt.Println("目录结构已创建:", path)
```

​**​注意​**​：

- 成功时不报错（即使目录已存在）
- 目录部分存在时会自动续建后续部分
- 比循环调用 `Mkdir` 更高效
## 3.3 func MkdirTemp(dir, pattern string) (string, error)

​**​功能​**​：创建临时目录（Go 1.16+）

```go
// 示例：在系统临时目录创建以 "app_*" 命名的临时目录
// 返回临时目录绝对路径
tmpDir, err := os.MkdirTemp("", "app_*.tmp") 
if err != nil {
    log.Fatal(err) 
    } 
defer os.RemoveAll(tmpDir) // 程序结束时清理  
fmt.Println("临时目录:", tmpDir) // 输出如: /tmp/app_123456.tmp
```

​**​注意​**​：

- `dir` 为空时使用 `os.TempDir()` 路径
- `pattern` 中的 `*` 会被随机字符串替换
- 需手动删除（不会自动清理）
## 3.4 func Remove(name string) error

​**​功能​**​：删除文件或空目录

```go
// 示例：删除文件或空目录 
file := "unused.log" 
if err := os.Remove(file); err != nil {    
    if errors.Is(err, os.ErrNotExist) {  
           fmt.Println("文件不存在")     
    } else {    
         log.Fatal(err)     
         } 
    } 
fmt.Println("已删除:", file)
```

​**​注意​**​：

- 无法删除非空目录（返回 `ErrExist`）
- 删除符号链接仅移除链接本身
- Windows 中删除后可能短暂无法创建同名文件
## 3.5 func RemoveAll(path string) error

​**​功能​**​：递归删除目录及其所有内容（类似 `rm -rf`）

```go
// 示例：删除整个目录树 
if err := os.RemoveAll("/tmp/old_data"); err != nil { 
    log.Fatal("删除失败:", err) 
    } 
fmt.Println("目录已完全删除")
```

​**​警告​**​：

- ⚠️ 极度危险！无确认机制直接删除
- 路径错误可能导致数据意外删除
- 返回 `nil` 不代表所有文件都删除成功（某些系统限制）
## 3.6 func Rename(oldpath, newpath string) error

​**​功能​**​：重命名/移动文件或目录

```go
// 示例：移动文件到新位置 
err := os.Rename("old.txt", "newdir/archive.txt") 
if err != nil {
    if errors.Is(err, os.ErrNotExist) { 
            fmt.Println("原始文件不存在")     
    } else if errors.Is(err, os.ErrPermission) { 
            fmt.Println("目标位置无权限")     
            } 
    }
```

​**​注意​**​：

- 跨磁盘移动时可能失败（某些系统不支持）
- 目标存在时会覆盖（非原子操作）
- 移动目录时要确保目标路径为空
## 3.7 func Link(oldname, newname string) error

​**​功能​**​：创建硬链接

```go
// 示例：为文件创建硬链接 
err := os.Link("original.dat", "backup.dat") 
if err != nil {
    log.Fatal("链接失败:", err) 
    } 
fmt.Println("硬链接创建成功，共享inode")
```

​**​限制​**​：

- 无法为目录创建硬链接（POSIX限制）
- 不能跨磁盘/分区创建
- Windows 需要 SeCreateSymbolicLinkPrivilege 权限
## 3.8 func Symlink(oldname, newname string) error

​**​功能​**​：创建符号链接（软链接）

```go
// 示例：创建指向目录的符号链接 
linkName := "current_config" 
target := "/etc/app/config_v2" 
if err := os.Symlink(target, linkName); err != nil {
    log.Fatal(err) 
    } 
fmt.Printf("符号链接 %s → %s 已创建\n", linkName, target)
```

​**​注意​**​：

- `oldname` 可以是相对路径或绝对路径
- Windows 需要管理员权限（默认情况下）
- 目标不存在也可成功创建（悬垂链接）
## 3.9 func Readlink(name string) (string, error)

​**​功能​**​：获取符号链接的实际目标路径

```go
// 示例：解析符号链接 
if target, err := os.Readlink("current_config"); err == nil {
    fmt.Printf("符号链接指向: %s\n", target) 
    } else if errors.Is(err, os.ErrInvalid) {
         fmt.Println("不是符号链接") 
    }
```

​**​注意​**​：

- 非符号链接返回 `ErrInvalid`
- 结果可能是相对路径
- Windows 可能需要启用开发者模式
## 3.10 func Pipe() (r \*File, w \*File, err error)

​**​功能​**​：创建匿名管道（用于进程内通信）

```go
// 示例：管道数据传输 
r, w, err := os.Pipe() 
if err != nil { 
    log.Fatal(err) 
} 
defer r.Close() 
defer w.Close()  
// 写入端 
go func() {
    w.Write([]byte("通过管道传输的数据"))    
    w.Close() 
}()  

// 读取端 
buf := make([]byte, 100) 
n, _ := r.Read(buf) 
fmt.Println("收到:", string(buf[:n])) // 输出: 通过管道传输的数据
```

​**​关键点​**​：

- 管道内容在内存中，大小有限（通常64KB）
- 需要同步关闭写端才能触发读端EOF
- 不适合大文件传输（可能阻塞）
## 3.11 func ReadFile(name string) (\[\]byte, error)

​**​功能​**​：读取整个文件内容到内存  
​**​返回值​**​：

- `[]byte`：文件内容字节切片
- `error`：读取错误（如文件不存在、权限不足等）

```go
// 示例：安全读取配置文件
func LoadConfig(path string) (Config, error) {
    // 注意事项1：不适合大文件（可能内存溢出）
    data, err := os.ReadFile("config.json")
    if err != nil {
        // 处理常见错误类型
        if errors.Is(err, os.ErrNotExist) {
            log.Printf("配置文件 %s 不存在", path)
        } else if errors.Is(err, os.ErrPermission) {
            log.Printf("无权限读取 %s", path)
        }
        return Config{}, err
    }

    // 注意事项2：不检查文件类型，确保内容可解析
    var conf Config
    if err := json.Unmarshal(data, &conf); err != nil {
        return Config{}, fmt.Errorf("配置文件解析错误: %w", err)
    }
    return conf, nil
}
```

​**​关键注意事项​**​：

- ⚠️ 最大文件限制：根据可用内存决定，通常不适合 >1GB 文件
- 文件被锁定直到读取完成（单次操作处理）
- Windows 路径需处理 `\`（如 `C:\\data\\file.txt`）
## 3.12 func WriteFile(name string, data \[\]byte, perm FileMode) error

​**​功能​**​：创建或覆盖文件并写入数据  
​**​返回值​**​：

- `error`：写入错误（如权限不足、磁盘满等）

```go
// 示例：记录关键数据到日志文件
func LogEvent(event string) error {
    timestamp := time.Now().Format(time.RFC3339)
    logEntry := fmt.Sprintf("[%s] %s\n", timestamp, event)
    
    // 注意事项1：始终指定文件权限（否则默认0666）
    err := os.WriteFile("events.log", []byte(logEntry), 0644)
    if err != nil {
        // 处理磁盘空间不足的特殊情况
        if errors.Is(err, syscall.ENOSPC) {
            alerts.Notify("磁盘空间不足!")
        }
        return err
    }
    
    // 注意事项2：自动创建文件，目录必须存在
    return nil
}

// 原子写入模式（避免写入时崩溃导致文件损坏）
func AtomicWrite(path string, data []byte) error {
    tmpFile := path + ".tmp"
    if err := os.WriteFile(tmpFile, data, 0644); err != nil {
        return err
    }
    return os.Rename(tmpFile, path) // 原子替换
}
```

​**​关键注意事项​**​：

- ⚠️ 数据安全：写入过程中崩溃可能导致文件损坏（使用原子写入）
- 权限继承：新文件权限由 `perm` 参数决定（不受 umask 影响）
- 并发写入：需外部同步机制（如文件锁）
## 3.13 func Truncate(name string, size int64) error

​**​功能​**​：修改文件大小（截断或扩展）  
​**​返回值​**​：

- `error`：操作错误（如文件不存在、权限不足等）

```go
// 示例：清理日志文件（保留最后1MB）
func TrimLogFile(path string) error {
    // 注意事项1：获取当前文件大小
    info, err := os.Stat(path)
    if err != nil {
        return err
    }
    
    currentSize := info.Size()
    maxSize := int64(1 * 1024 * 1024) // 1MB
    
    if currentSize > maxSize {
        // 注意事项2：截断操作不可逆！
        if err := os.Truncate(path, maxSize); err != nil {
            // 处理特定错误
            if errors.Is(err, os.ErrPermission) {
                return fmt.Errorf("需要管理员权限")
            }
            return err
        }
        log.Printf("已截断文件 %s 到 %.2fMB", path, float64(maxSize)/1e6)
    }
    return nil
}

// 示例：预分配磁盘空间（创建稀疏文件）
func PreallocateDiskSpace(path string, sizeGB int) error {
    size := int64(sizeGB) * 1e9
    if err := os.Truncate(path, size); err != nil {
        return fmt.Errorf("预分配失败: %w", err)
    }
    log.Printf("已创建 %dGB 稀疏文件 %s", sizeGB, path)
    return nil
}
```

​**​关键注意事项​**​：

- ⚠️ 数据丢失：截断操作会丢弃超出部分（不可恢复）
- 扩展行为：
    - 稀疏文件（Linux/Unix）：快速扩展，不实际占用磁盘
    - 非稀疏文件：填充空字节（\x00），可能触发磁盘分配
- 系统限制：
    - FAT32 文件系统不支持 >4GB 文件
    - 超出磁盘空间返回 `ENOSPC` 错误
## 3.14 func Chmod(name string, mode FileMode) error

​**​功能​**​：修改文件或目录的权限位  
​**​参数说明​**​：

- `name`：文件/目录路径
- `mode`：Unix风格的权限位值（如0644）  
    ​**​返回值​**​：成功返回 nil，失败返回错误对象

​**​错误返回情况​**​：

- 路径不存在时返回 `ErrNotExist`
- 权限不足时返回 `ErrPermission`
- 路径指向目录但无执行权限时可能返回错误
- Windows上只读文件修改权限可能失败
- 传入无效路径格式时返回路径错误

```go
// 示例：设置配置文件为只读权限
func secureConfigFile(filePath string) error {
    // 设置权限：用户可读，组可读，其他无权限
    if err := os.Chmod(filePath, 0440); err != nil {
        if os.IsPermission(err) {
            fmt.Println("错误：需要管理员权限或文件所有者账户")
        } else if os.IsNotExist(err) {
            fmt.Println("错误：配置文件不存在，请检查路径")
        } else {
            fmt.Printf("未知错误：%v\n", err)
        }
        return err
    }
    fmt.Printf("文件 %s 权限已更新为只读\n", filePath)
    return nil
}
```

- Unix系统权限模式为八进制值（如0644）
- Windows只支持设置只读属性（其他权限无效）
- 修改权限需要文件所有者或管理员权限
- 目录需要执行(x)权限才能访问内容
- 修改符号链接会影响其目标文件
## 3.15 func Chown(name string, uid, gid int) error

​**​功能​**​：修改文件所有者  
​**​参数说明​**​：

- `name`：文件/目录路径
- `uid`：用户ID（-1保持原值）
- `gid`：组ID（-1保持原值）  
    ​**​返回值​**​：成功返回 nil，失败返回错误对象

​**​错误返回情况​**​：

- 路径不存在时返回 `ErrNotExist`
- 权限不足时返回 `ErrPermission`
- 指定用户/组不存在时返回系统错误
- Windows系统总是返回不支持错误
- NFS文件系统可能返回服务端错误

```go
// 示例：将日志文件移交给专用用户
func transferFileOwnership(filePath, userName string) error {
    // 查找目标用户ID
    appUser, err := user.Lookup(userName)
    if err != nil {
        fmt.Printf("错误：用户 %s 不存在\n", userName)
        return err
    }
    
    uid, _ := strconv.Atoi(appUser.Uid)
    gid, _ := strconv.Atoi(appUser.Gid)
    
    if err := os.Chown(filePath, uid, gid); err != nil {
        if os.IsPermission(err) {
            fmt.Println("错误：需要root权限执行此操作")
        } else if os.IsNotExist(err) {
            fmt.Println("错误：日志文件不存在")
        } else {
            fmt.Printf("所有权转移失败：%v\n", err)
        }
        return err
    }
    fmt.Printf("文件所有权已转移给用户 %s\n", userName)
    return nil
}
```

**注意事项​**​：

- Windows系统完全不支持此功能
- 需要root权限或`CAP_CHOWN`能力
- 修改目录时不会递归影响子项
- 确保用户/组ID存在于系统中
- 修改后可能影响文件访问权限
## 3.16 func Lchown(name string, uid, gid int) error

​**​功能​**​：修改符号链接自身所有者  
​**​参数说明​**​：同`Chown`  
​**​返回值​**​：同`Chown`

​**​错误返回情况​**​：

- 符号链接不存在时返回 `ErrNotExist`
- 权限不足时返回 `ErrPermission`
- Windows系统总是返回不支持错误
- 旧UNIX系统可能不支持此操作
- 无效链接路径返回路径错误

```go
// 示例：修改关键符号链接所有权
func secureSymlink(linkPath string) {
    // 修改链接自身（不影响目标文件）
    if err := os.Lchown(linkPath, 0, 0); err != nil {
        if os.IsPermission(err) {
            fmt.Println("错误：需要root权限修改系统链接")
        } else if os.IsNotExist(err) {
            fmt.Println("错误：符号链接不存在")
        } else if os.IsNotExist(err) {
            fmt.Println("错误：此操作在Windows上不被支持")
        }
        return
    }
    fmt.Println("符号链接所有权已更新")
}
```

**注意事项​**​：

- 与`Chown`的区别在于不跟随符号链接
- 修改链接所有权不影响目标文件
- 需要与`Chown`相同的权限级别
- 某些旧文件系统可能不支持此操作
- 系统关键链接修改可能导致功能异常
## 3.17 func Chtimes(name string, atime time.Time, mtime time.Time) error

​**​功能​**​：修改访问时间(atime)和修改时间(mtime)  
​**​参数说明​**​：

- `name`：文件/目录路径
- `atime`：新的访问时间
- `mtime`：新的修改时间  
    ​**​返回值​**​：成功返回 nil，失败返回错误对象

​**​错误返回情况​**​：

- 路径不存在时返回 `ErrNotExist`
- 权限不足时返回 `ErrPermission`
- FAT32文件系统可能返回无效时间错误
- 挂载为noatime的文件系统返回权限错误
- 超出文件系统时间范围返回无效参数错误

```go
// 示例：重置备份文件时间戳
func fixBackupTimestamps(backupPath string) {
    // 获取原始修改时间
    fileInfo, err := os.Stat(backupPath)
    if err != nil {
        fmt.Println("错误：无法读取文件信息")
        return
    }
    originalMtime := fileInfo.ModTime()
    
    // 设置新的访问时间
    newAccessTime := time.Now()
    
    if err := os.Chtimes(backupPath, newAccessTime, originalMtime); err != nil {
        if os.IsPermission(err) {
            fmt.Println("错误：需要文件所有者权限")
        } else if os.IsNotExist(err) {
            fmt.Println("错误：备份文件已被删除")
        } else {
            fmt.Printf("时间戳更新失败：%v\n", err)
        }
        return
    }
    fmt.Println("备份文件时间戳已恢复")
}
```

**注意事项​**​：

- FAT32文件系统仅支持2秒精度
- noatime挂载选项会禁用访问时间更新
- 修改目录时间会影响父目录的mtime
- NTFS支持100纳秒精度
- 时间修改可能影响备份和同步系统
## 3.18 func Environ() \[\]string

​**​功能​**​：获取所有环境变量的副本  
​**​返回值​**​：字符串切片，格式为 `KEY=VALUE`  

```go
// 示例：打印所有环境变量
func printEnvironment() {
    envVars := os.Environ()
    
    // 按字母排序输出
    sort.Strings(envVars)
    
    for _, env := range envVars {
        fmt.Println(env)
    }
}

/*
输出示例：
GOPATH=/home/user/go
HOME=/home/user
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
*/
```

**注意事项​**​：

- 返回的是当前进程环境变量的拷贝
- 修改返回的切片不会影响实际环境变量
- Windows 环境变量名称不区分大小写
- 结果包含父进程传递的所有环境变量
- 敏感信息（如密码）可能暴露在输出中
## 3.19 func Clearenv()

​**​功能​**​：清除所有环境变量  
​
```go
// 示例：创建干净环境
func runInIsolatedEnv() {
    // 保存原始环境
    originalEnv := os.Environ()
    
    // 清空环境
    os.Clearenv()
    
    // 设置必要的安全环境
    os.Setenv("SAFE_MODE", "1")
    
    // 执行敏感操作...
    
    // 恢复原始环境
    restoreEnv(originalEnv)
}

func restoreEnv(env []string) {
    os.Clearenv()
    for _, e := range env {
        parts := strings.SplitN(e, "=", 2)
        os.Setenv(parts[0], parts[1])
    }
}
```

**注意事项​**​：

- 立即删除所有环境变量
- 子进程会继承当前空环境
- 清除后无法自动恢复之前的状态
- 可能导致依赖环境的应用崩溃
- 仅应在严格控制的场景使用
## 3.20 func ExpandEnv(s string) string

​**​功能​**​：替换字符串中的环境变量占位符  
​**​参数​**​：`s` - 包含环境变量引用的字符串  
​**​返回值​**​：已展开的字符串

```go
// 示例：处理配置文件模板
func renderConfigTemplate() {
    template := `# 数据库配置
host = ${DB_HOST}
port = ${DB_PORT|3306}`
    
    // 设置真实环境变量
    os.Setenv("DB_HOST", "db.example.com")
    
    result := os.ExpandEnv(template)
    fmt.Println(result)
    
    /*
    输出:
    # 数据库配置
    host = db.example.com
    port = 3306
    */
}
```

**注意事项​**​：

- 仅支持 `$VAR` 和 `${VAR}` 格式
- 未设置变量替换为空字符串
- Windows 支持 `%VAR%` 格式（自动转换）
- 不支持默认值语法如 `${VAR|default}`
- 递归替换可能导致死循环（如 `A=$B`, `B=$A`）
## 3.21 func Getenv(key string) string

​**​功能​**​：获取指定环境变量的值  
​**​参数​**​：`key` - 环境变量名  
​**​返回值​**​：变量值（未设置返回空字符串）

```go
// 示例：获取用户配置路径
func getConfigPath() string {
    // 优先检查自定义配置路径
    if path := os.Getenv("APP_CONFIG_PATH"); path != "" {
        return path
    }
    
    // 默认配置位置
    home, _ := os.UserHomeDir()
    return filepath.Join(home, ".config", "app.conf")
}
```

**注意事项​**​：

- 变量名区分大小写（Windows 除外）
- 返回值为字符串类型
- 未定义时返回空字符串而非错误
- 包含敏感信息时注意安全处理
- 无法检测变量是否存在或已被设置
## 3.22 func Setenv(key, value string) error

​**​功能​**​：设置环境变量  
​**​参数​**​：

- `key` - 环境变量名
- `value` - 要设置的值  
    ​**​返回值​**​：成功返回 nil，错误返回错误对象  

```go
// 示例：安全设置API密钥
func setupSecureEnvironment() {
    // 从加密存储加载密钥
    apiKey, err := secrets.Load("API_KEY")
    if err != nil {
        log.Fatal("无法加载API密钥")
    }
    
    if err := os.Setenv("API_KEY", apiKey); err != nil {
        log.Fatal("设置环境变量失败:", err)
    }
    
    // 设置内存保护（非标准功能）
    protectInMemory(apiKey)
}
```

**错误返回情况​**​：

- 无效变量名（如包含 `=` 字符）
- 内存分配失败（系统资源耗尽）
- 安全策略限制（如 SELinux）
- 长度超过系统限制
- Windows 的 `%PATH%` 超长错误

**注意事项​**​：

- 仅影响当前进程及子进程
- Windows 最长约32K字符（所有变量总和）
- 变量名建议全大写字母和数字
- 设置后无法通过 `Unsetenv` 完全清除内存痕迹
- 高安全场景应避免在环境变量中存储密码
## 3.23 func Unsetenv(key string) error

​**​功能​**​：删除环境变量  
​**​参数​**​：`key` - 环境变量名  
​**​返回值​**​：成功返回 nil，错误返回错误对象

```go
// 示例：清理敏感临时变量
func cleanTempCredentials() {
    // 临时使用变量
    os.Setenv("TEMP_TOKEN", "abc123")
    
    // 执行操作...
    
    // 立即清除
    if err := os.Unsetenv("TEMP_TOKEN"); err != nil {
        log.Println("警告：临时令牌清除失败")
    }
    
    // 验证清除结果
    if os.Getenv("TEMP_TOKEN") != "" {
        log.Fatal("严重：敏感信息未清除！")
    }
}
```

**错误返回情况​**​：

- 无效变量名（包含特殊字符）
- 未实现该系统调用（旧系统）
- 安全策略限制
- Windows 某些核心变量无法删除

​**​注意事项​**​：

- Windows 不保证立即移除内存内容
- 对不存在变量操作不返回错误
- 删除后子进程无法访问该变量
- 不会影响同名变量在不同进程中的值
- 某些系统变量删除可能导致意外行为
## 3.24 func LookupEnv(key string) (string, bool)

​**​功能​**​：安全获取环境变量值  
​**​参数​**​：`key` - 环境变量名  
​**​返回值​**​：

- 第一个值：变量值
- 第二个值：变量是否存在的布尔值

```go
// 示例：配置缺省值处理
func getLogLevel() string {
    // 安全获取变量值
    if level, exists := os.LookupEnv("LOG_LEVEL"); exists {
        return validateLevel(level)
    }
    
    // 使用默认值
    return "INFO"
}

func validateLevel(level string) string {
    validLevels := map[string]bool{"DEBUG": true, "INFO": true, "WARN": true, "ERROR": true}
    if _, valid := validLevels[strings.ToUpper(level)]; valid {
        return strings.ToUpper(level)
    }
    return "INFO"
}
```

**注意事项​**​：

- 正确区分空值和未设置状态
- 比 `Getenv` 更安全的替代方案
- Windows 变量名大小写不敏感
- 即使存在也可能返回空值
- 适合处理重要配置参数
## 3.25 func Expand(s string, mapping func(string) string) string

​**​功能​**​：自定义变量展开规则  
​**​参数​**​：

- `s` - 要处理的字符串
- `mapping` - 自定义替换函数  
    ​**​返回值​**​：已展开的字符串

```go
// 示例：带默认值的模板渲染
func renderTemplate(tpl string) string {
    // 自定义展开函数
    return os.Expand(tpl, func(key string) string {
        // 支持默认值语法：key|default
        parts := strings.SplitN(key, "|", 2)
        
        if val, exists := os.LookupEnv(parts[0]); exists {
            return val
        }
        
        if len(parts) > 1 {
            return parts[1] // 返回默认值
        }
        
        return "" // 无默认值
    })
}

// 使用示例
func main() {
    os.Setenv("PORT", "8080")
    template := "监听地址: $HOST|localhost:$PORT|8080"
    fmt.Println(renderTemplate(template))
    // 输出: 监听地址: localhost:8080
}
```

**注意事项​**​：

- 支持 `$VAR` 和 `${VAR}` 语法
- `mapping` 函数负责转换变量名到值
- 未处理的变量名返回空字符串
- 可用来实现复杂模板引擎
- 注意防止恶意输入导致无限递归
## 3.26 func Chdir(dir string) error

​**​功能​**​：更改当前工作目录  
​**​参数​**​：`dir` - 目标路径（绝对或相对路径）  
​**​返回值​**​：成功返回 `nil`，失败返回错误对象

```go
// 示例：安全执行目录操作
func processInDirectory(targetDir string) {
    // 保存当前目录
    originalDir, err := os.Getwd()
    if err != nil {
        log.Fatal("无法获取当前目录:", err)
    }
    
    // 改变目录
    if err := os.Chdir(targetDir); err != nil {
        handleDirError(targetDir, err)
        return
    }
    defer os.Chdir(originalDir) // 确保恢复目录
    
    // 执行操作
    files, _ := os.ReadDir(".")
    fmt.Printf("在 %s 中找到 %d 个文件\n", targetDir, len(files))
}

func handleDirError(dir string, err error) {
    if os.IsNotExist(err) {
        fmt.Printf("错误：目录 %s 不存在\n", dir)
    } else if os.IsPermission(err) {
        fmt.Printf("错误：无权访问 %s\n", dir)
    } else if runtime.GOOS == "windows" && strings.Contains(err.Error(), "device") {
        fmt.Println("错误：无效的驱动器或网络路径")
    } else {
        fmt.Printf("目录切换失败: %v\n", err)
    }
}
```

**错误情况​**​：

- `ErrNotExist`：目录不存在
- `ErrPermission`：没有目录访问权限
- Windows 无效设备错误
- 相对路径解析失败
- 符号链接目标无效

​**​注意事项​**​：

- 影响整个进程的工作目录
- Windows 路径使用反斜杠（建议用 `filepath.Join()`）
- 目标目录需要执行权限（UNIX系统）
- 绝对路径更安全可靠
- 使用 `defer` 恢复原始工作目录
## 3.27 func Getwd() (string, error)

​**​功能​**​：获取当前工作目录的绝对路径  
​**​返回值​**​：路径字符串和错误对象

```go
// 示例：验证工作目录
func checkWorkingDirectory() {
    if wd, err := os.Getwd(); err == nil {
        fmt.Println("当前工作目录:", wd)
    } else {
        // 处理特殊错误
        if pathErr, ok := err.(*os.PathError); ok {
            fmt.Printf("路径错误: %v (操作: %s)\n", pathErr.Err, pathErr.Op)
        } else if err == syscall.ENOENT {
            fmt.Println("警告：工作目录已被删除")
        } else {
            fmt.Printf("无法确定工作目录: %v\n", err)
        }
    }
}
```

**错误情况​**​：

- `ErrPermission`：目录访问权限不足
- `ErrNotExist`：目录已被删除
- 路径长度超过系统限制
- 网络路径断开连接
- 内存分配失败
## 3.28 func TempDir() string

​**​功能​**​：获取系统临时目录路径  
​**​返回值​**​：临时目录路径（字符串）

```go
// 示例：安全创建临时目录
func createAppTempDir() (string, error) {
    tempDir := os.TempDir()
    
    // 检查临时目录状态
    if info, err := os.Stat(tempDir); err != nil {
        return "", fmt.Errorf("临时目录不可用: %w", err)
    } else if !info.IsDir() {
        return "", fmt.Errorf("%s 不是目录", tempDir)
    }
    
    // 创建应用专用目录
    appTempDir := filepath.Join(tempDir, "myapp_tmp")
    if err := os.MkdirAll(appTempDir, 0700); err != nil {
        return "", fmt.Errorf("创建临时目录失败: %w", err)
    }
    
    // 设置清理钩子
    runtime.SetFinalizer(&appTempDir, cleanTempDir)
    return appTempDir, nil
}

func cleanTempDir(dir *string) {
    os.RemoveAll(*dir)
}
```

**注意事项​**​：

- Windows： `%TEMP%` 或 `%TMP%`
- Unix： `/tmp`
- 目录权限通常为 0777
- 文件可能被系统自动清理
- 敏感文件应设置适当权限
## 3.29 func UserCacheDir() (string, error)

​**​功能​**​：获取用户缓存目录路径  
​**​返回值​**​：路径字符串和错误对象

```go
// 示例：管理应用缓存
func getAppCache(appName string) string {
    cacheDir, err := os.UserCacheDir()
    if err != nil {
        // 回退机制
        fmt.Println("警告：使用临时目录代替缓存目录")
        cacheDir = os.TempDir()
    }
    
    appCache := filepath.Join(cacheDir, appName)
    if err := os.MkdirAll(appCache, 0700); err != nil {
        fmt.Printf("缓存目录创建失败: %v\n", err)
        return ""
    }
    
    // 设置大小限制
    monitorCacheSize(appCache, 100 * 1024 * 1024) // 100MB限制
    return appCache
}
```

**平台路径​**​：

- Windows： `%LOCALAPPDATA%`
- macOS： `~/Library/Caches`
- Linux： `~/.cache`
- 错误情况：用户配置不可用或权限问题
## 3.30 func UserCacheDir() (string, error)

​**​功能​**​：获取用户缓存目录路径  
​**​返回值​**​：路径字符串和错误对象

```go
// 示例：管理应用缓存
func getAppCache(appName string) string {
    cacheDir, err := os.UserCacheDir()
    if err != nil {
        // 回退机制
        fmt.Println("警告：使用临时目录代替缓存目录")
        cacheDir = os.TempDir()
    }
    
    appCache := filepath.Join(cacheDir, appName)
    if err := os.MkdirAll(appCache, 0700); err != nil {
        fmt.Printf("缓存目录创建失败: %v\n", err)
        return ""
    }
    
    // 设置大小限制
    monitorCacheSize(appCache, 100 * 1024 * 1024) // 100MB限制
    return appCache
}
```

​**​平台路径​**​：

- Windows： `%LOCALAPPDATA%`
- macOS： `~/Library/Caches`
- Linux： `~/.cache`
- 错误情况：用户配置不可用或权限问题

## 3.31 func UserConfigDir() (string, error)

​**​功能​**​：获取用户配置目录路径  
​**​返回值​**​：路径字符串和错误对象


```go
// 示例：加载用户配置
func loadUserSettings() map[string]string {
    configDir, err := os.UserConfigDir()
    if err != nil {
        fmt.Println("警告：使用默认配置")
        return defaultConfig()
    }
    
    configPath := filepath.Join(configDir, "myapp", "settings.conf")
    if data, err := os.ReadFile(configPath); err == nil {
        return parseConfig(data)
    }
    
    // 配置文件不存在则创建
    if os.IsNotExist(err) {
        if err := writeDefaultConfig(configPath); err == nil {
            fmt.Println("已创建默认配置文件")
        }
    }
    return defaultConfig()
}
```

​**​平台路径​**​：

- Windows： `%APPDATA%`
- macOS： `~/Library/Application Support`
- Linux： `~/.config`
- XDG兼容系统：遵循 XDG 规范

## 3.32 func UserHomeDir() (string, error)

​**​功能​**​：获取用户主目录路径  
​**​返回值​**​：路径字符串和错误对象


```go
// 示例：定位用户文件
func findUserResource(fileName string) string {
    home, err := os.UserHomeDir()
    if err != nil {
        if runtime.GOOS == "windows" {
            // Windows 备用方案
            if drive := os.Getenv("SystemDrive"); drive != "" {
                home = filepath.Join(drive, "Users", os.Getenv("USERNAME"))
            }
        }
    }
    
    if home == "" {
        // 最终回退方案
        home = "."
    }
    
    return filepath.Join(home, ".myapp", "resources", fileName)
}
```

​**​错误情况​**​：

- 用户目录未设置（无 `$HOME`）
- 用户账号无效
- 虚拟环境限制
- 权限问题
- 内存分配失败
## 3.33 func Getpid() int

​**​功能​**​：获取当前进程ID  
​**​返回值​**​：进程ID（整数值）

```go
// 示例：进程唯一标识
func generateProcessTag() string {
    pid := os.Getpid()
    timestamp := time.Now().UnixNano()
    return fmt.Sprintf("proc_%d_%d", pid, timestamp)
}

// 监控进程资源使用
func startResourceMonitor() {
    pid := os.Getpid()
    go func() {
        for {
            time.Sleep(5 * time.Second)
            mem := getMemoryUsage(pid) // 伪代码：获取内存使用
            fmt.Printf("[%d] 内存使用: %.2f MB\n", pid, mem)
        }
    }()
}
```

​**​注意事项​**​：

- 在Unix系统中PID可重复使用
- Windows中PID为32位值
- 容器环境下为容器内PID
- 返回值在进程生命周期内不变
- 可安全用于日志标识
## 3.34 func Getppid() int

​**​功能​**​：获取父进程ID  
​**​返回值​**​：父进程ID（整数值）

```go
// 示例：进程关系验证
func checkProcessParent() {
    ppid := os.Getppid()
    
    // 获取父进程信息
    cmd := exec.Command("ps", "-p", strconv.Itoa(ppid), "-o", "comm=")
    out, _ := cmd.Output()
    
    fmt.Printf("父进程ID: %d (%s)\n", ppid, strings.TrimSpace(string(out)))
    
    // 检查是否为特定父进程（如systemd）
    if strings.Contains(string(out), "systemd") {
        fmt.Println("作为系统服务运行")
    }
}
```

​**​注意事项​**​：

- 父进程结束后返回1（init进程ID）
- Windows中为创建当前进程的进程ID
- 容器环境下为容器父进程
- 返回值在进程启动后不变
- 守护进程的父进程通常是init
## 3.35 func Getuid() int 和 func Geteuid() int

​**​功能​**​：

- `Getuid()`: 获取实际用户ID
- `Geteuid()`: 获取有效用户ID  
    ​**​返回值​**​：用户ID整数值

```go
// 示例：权限升级检测
func checkPrivileges() {
    uid := os.Getuid()
    euid := os.Geteuid()
    
    fmt.Printf("实际用户ID: %d\n", uid)
    fmt.Printf("有效用户ID: %d\n", euid)
    
    if euid == 0 {
        fmt.Println("警告：以root权限运行")
        if uid != 0 {
            fmt.Println("说明程序具有SUID权限位")
        }
    } else if euid != uid {
        fmt.Println("权限升级模式 (setuid)")
    } else {
        fmt.Println("标准权限模式")
    }
}
```

​**​注意事项​**​：

- Windows返回-1或0
- 通常实际ID用于文件创建
- 有效ID用于权限检查
- SUID程序显示euid为root
- 容器中UID可能映射到非零值
## 3.36 func Getgid() int 和 func Getegid() int

​**​功能​**​：

- `Getgid()`: 获取实际组ID
- `Getegid()`: 获取有效组ID  
    ​**​返回值​**​：组ID整数值

```go
// 示例：组权限验证
func checkGroupAccess(file string) {
    gid := os.Getgid()
    egid := os.Getegid()
    
    // 检查文件组权限
    fileInfo, err := os.Stat(file)
    if err != nil {
        return
    }
    
    fileGid := fileInfo.Sys().(*syscall.Stat_t).Gid
    if egid == int(fileGid) {
        fmt.Printf("具有文件组 %d 的权限\n", fileGid)
    } else {
        // 检查辅助组权限
        groups, _ := os.Getgroups()
        for _, g := range groups {
            if g == int(fileGid) {
                fmt.Printf("通过辅助组 %d 拥有权限\n", g)
                return
            }
        }
        fmt.Println("无文件组访问权限")
    }
}
```

​**​注意事项​**​：

- Windows返回0
- 实际组ID用于文件创建
- 有效组ID用于权限检查
- SGID程序显示egid为特权组
- 文件权限需检查主组和辅助组
## 3.37 func Getgroups() (\[\]int, error)

​**​功能​**​：获取辅助组ID列表  
​**​返回值​**​：组ID切片和错误对象

```go
// 示例：验证组成员资格
func isGroupMember(targetGroup string) (bool, error) {
    groupID := findGroupID(targetGroup)
    if groupID == 0 {
        return false, fmt.Errorf("组 %s 不存在", targetGroup)
    }
    
    groups, err := os.Getgroups()
    if err != nil {
        return false, fmt.Errorf("无法获取组列表: %w", err)
    }
    
    for _, gid := range groups {
        if gid == groupID {
            return true, nil
        }
    }
    return false, nil
}

// 辅助函数：获取组ID
func findGroupID(name string) int {
    // 伪代码实现
    groups := map[string]int{"admins": 1001, "devs": 1002}
    return groups[name]
}
```

​**​错误情况​**​：

- `ENOSYS`：系统不支持（Windows）
- `EINVAL`：组数超过限制
- `EPERM`：权限不足
- `ENOMEM`：内存分配失败
- 系统资源耗尽

​**​注意事项​**​：

- 结果包含主要组ID
- Unix系统最多支持`NGROUPS_MAX`个组
- Windows总是返回空切片
- 容器环境可能返回主机组ID
- 修改用户组后需要重启进程生效
## 3.38 func Exit(code int)

​**​功能​**​：立即终止当前进程  
​**​参数​**​：`code` - 退出状态码

```go
// 示例：受控关闭过程
func safeShutdown(exitCode int) {
    // 保存当前状态
    if err := saveSessionState(); err != nil {
        fmt.Println("警告：会话状态保存失败")
    }
    
    // 清理资源
    cleanupResources()
    
    // 通知监控系统
    reportShutdownToMonitoring()
    
    // 正式退出
    fmt.Printf("进程退出，状态码: %d\n", exitCode)
    os.Exit(exitCode)
}

// 错误处理
func handleFatalError(msg string) {
    fmt.Fprintf(os.Stderr, "致命错误: %s\n", msg)
    crashReporter.Report(msg)
    saveCrashDump()
    os.Exit(1) // 非零状态表示失败
}
```

​**​注意事项​**​：

- 跳过所有defer函数执行
- 立即终止程序不返回
- 子进程不受影响
- Windows状态码范围0-255
- 避免在库函数中使用
- 非0状态码表示失败

​**​推荐状态码​**​：

- 0: 成功退出
- 1: 一般错误
- 2: 命令行错误
- 126: 权限不足
- 127: 命令未找到
- 130: Ctrl+C终止 (SIGINT)
- 137: OOM终止 (SIGKILL)
## 3.39 func IsExist(err error) bool

​**​功能​**​：检查是否为"已存在"错误  
​**​参数​**​：错误对象  
​**​返回值​**​：相关错误时返回 true

```go
// 示例：安全创建唯一文件
func createUniqueFile(path string) (*os.File, error) {
    // 重试机制（注意事项：避免无限重试）
    for i := 0; i < 10; i++ {
        name := fmt.Sprintf("%s_%d", path, time.Now().UnixNano())
        file, err := os.OpenFile(name, os.O_CREATE|os.O_EXCL, 0644)
        
        if err == nil {
            return file, nil // 成功创建
        }
        
        // 文件已存在则重试（注意事项：区分错误类型）
        if os.IsExist(err) {
            continue
        }
        return nil, err // 其他错误
    }
    return nil, fmt.Errorf("无法创建唯一文件")
}
```

| 函数                                                 | 功能说明        |
| -------------------------------------------------- | ----------- |
| `IsExist(err error) bool`                          | 是否"文件已存在"错误 |
| `IsNotExist(err error) bool`                       | 是否"文件不存在"错误 |
| `IsPermission(err error) bool`                     | 是否权限错误      |
| `IsTimeout(err error) bool`                        | 是否超时错误      |
| `IsPathSeparator(c uint8) bool`                    | 是否是路径分隔符    |
| `NewSyscallError(syscall string, err error) error` | 创建系统调用错误    |
## 3.40 func SameFile(fi1, fi2 FileInfo) bool

​**​功能​**​：检查文件是否相同  
​**​参数​**​：两个文件信息对象  
​**​返回值​**​：相同返回 true

```go
// 示例：避免重复处理硬链接
func processFile(fpath string) {
    currentInfo, _ := os.Stat(fpath)
    
    // 检查与上次处理文件的关系（注意事项：硬链接处理）
    if lastProcessed != nil && os.SameFile(currentInfo, lastProcessed) {
        fmt.Printf("跳过重复文件: %s\n", fpath)
        return
    }
    
    // 处理新文件...
    
    // 更新上次处理记录（注意事项：包含文件信息）
    lastProcessed = currentInfo
}
```

**注意事项​**​：

- 比较 inode 和设备 ID
- 硬链接文件返回 true
- 路径不同但指向相同文件返回 true
- 文件删除后重新创建可能不同
- 不适用于网络文件系统
# 4 类型
## 4.1 File类型

`os.File` 是 Go 语言标准库中处理文件 I/O 的核心类型，代表操作系统文件描述符的封装。

### 4.1.1 func Create(name string) (\*File, error)

​**​功能​**​：创建新文件，如果文件已存在则截断  
​**​参数​**​：

- `name`：文件路径  
    ​**​返回值​**​：
- `*File`：文件对象
- `error`：创建失败的错误

```go
package main

import (
    "log"
    "os"
)

func main() {
    // 创建新文件 - 如果存在会被覆盖
    file, err := os.Create("data.txt")
    if err != nil {
        log.Fatalf("创建文件失败: %v", err)
    }
    defer file.Close() // 确保关闭文件
    
    // 写入内容
    _, err = file.WriteString("Hello, World!\n")
    if err != nil {
        log.Fatalf("写入文件失败: %v", err)
    }
    log.Println("文件创建并写入成功")
}
```

**注意事项​**​：

- 如果文件已存在，会​**​截断​**​（清空）原文件
- Windows 路径可以使用反斜杠 `\`
- 默认权限为 0666（所有人可读写）
- 重要错误情况：
    - `ErrPermission`：目录没有写权限
    - `ErrNotExist`：父目录不存在
    - `EEXIST`：路径已存在但非文件（Linux）
### 4.1.2 func CreateTemp(dir, pattern string) (\*File, error)

**功能​**​：在指定目录创建临时文件  
​**​参数​**​：

- `dir`：目标目录（空表示默认临时目录）
- `pattern`：文件名模式（支持 `*` 通配符）  
    ​**​返回值​**​：
- `*File`：文件对象
- `error`：创建失败的错误

```go
func secureTempFile() {
    // 创建临时文件，文件名包含随机字符
    tmpFile, err := os.CreateTemp("", "data_*.tmp")
    if err != nil {
        log.Fatalf("创建临时文件失败: %v", err)
    }
    defer os.Remove(tmpFile.Name()) // 程序退出时删除
    defer tmpFile.Close()
    
    log.Printf("临时文件: %s", tmpFile.Name())
}

```

**注意事项​**​：

- 文件名会替换 `*` 为随机字符
- 目录必须有写权限
- 临时文件不会自动删除
- 重要错误情况：
    - `ErrPermission`：目录没有写权限
    - `ErrNotExist`：目录不存在
### 4.1.3 func NewFile(fd uintptr, name string) \*File

​**​功能​**​：根据文件描述符创建文件对象  
​**​参数​**​：

- `fd`：文件描述符
- `name`：文件名（可空）  
    ​**​返回值​**​：文件对象（无错误）

```go
func reuseDescriptor() {
    // 标准输出文件描述符
    stdout := os.NewFile(uintptr(syscall.Stdout), "/dev/stdout")
    if stdout == nil {
        log.Fatal("无法创建stdout文件对象")
    }
    defer stdout.Close()
    
    stdout.WriteString("通过文件描述符写入标准输出\n")
}
```

**注意事项​**​：

- 主要用于转换系统调用的文件描述符
- 需确保描述符有效
- ​**​不会​**​自动关闭底层文件描述符
### 4.1.4 func Open(name string) (\*File, error)

​**​功能​**​：以只读方式打开文件  
​**​参数​**​：

- `name`：文件路径  
    ​**​返回值​**​：
- `*File`：文件对象
- `error`：打开失败的错误

```go
func readConfig() {
    file, err := os.Open("config.cfg")
    if os.IsNotExist(err) {
        log.Fatal("配置文件不存在")
    } else if err != nil {
        log.Fatalf("打开配置文件失败: %v", err)
    }
    defer file.Close()
    
    // 读取配置...
}
```

**注意事项​**​：

- 只读模式，不允许写入
- 文件必须存在
- 重要错误情况：
    - `ErrNotExist`：文件不存在
    - `ErrPermission`：无读取权限
    - `EISDIR`：路径是目录（Linux）
### 4.1.5 func OpenFile(name string, flag int, perm FileMode) (\*File, error)

**功能​**​：灵活打开文件  
​**​参数​**​：

- `name`：文件路径
- `flag`：打开标志（见下表）
- `perm`：文件权限（创建时生效）

```go
func appendLog(message string) {
    // 以追加方式打开，不存在则创建
    logFile, err := os.OpenFile("app.log", 
        os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
        log.Fatalf("打开日志文件失败: %v", err)
    }
    defer logFile.Close()
    
    // 写入带时间戳的日志
    _, err = fmt.Fprintf(logFile, "[%s] %s\n", 
        time.Now().Format(time.RFC3339), message)
    if err != nil {
        log.Fatalf("写入日志失败: %v", err)
    }
}
```

**注意事项​**​：

- `O_RDONLY | O_WRONLY | O_RDWR` 必须指定一个
- `O_EXCL` 需要与 `O_CREATE` 一起使用
- 权限位仅在创建文件时生效
- 重要错误情况：
    - `EEXIST`：使用 O_EXCL 但文件存在
    - `EACCES`：权限不足（Linux）
    - `ENOTDIR`：路径前缀存在但不是目录
### 4.1.6 func (f \*File) Read(b \[\]byte) (n int, err error)

**功能​**​：从当前位置读取数据  
​**​参数​**​：

- `b`：目标字节切片  
    ​**​返回值​**​：
- `n`：实际读取字节数
- `err`：错误（常为 `io.EOF`）

```go
func readChunks(file *os.File) {
    buf := make([]byte, 4 * 1024) // 4KB 缓冲区
    for {
        n, err := file.Read(buf)
        if err == io.EOF {
            break
        }
        if err != nil {
            log.Fatalf("读取错误: %v", err)
        }
        processData(buf[:n])
    }
}

```

**注意事项​**​：

- 会修改文件偏移量
- `n < len(b)` 时不一定是错误
- `io.EOF` 表示文件结束
- 可能返回 `0, nil`
### 4.1.7 func (f \*File) Write(b \[\]byte) (n int, err error)

​**​功能​**​：向文件写入数据  
​**​参数​**​：

- `b`：源字节切片  
    ​**​返回值​**​：
- `n`：实际写入字节数
- `err`：写入错误

```go
func writeData(file *os.File, data []byte) {
    n, err := file.Write(data)
    if err != nil {
        log.Fatalf("写入错误: %v", err)
    }
    if n < len(data) {
        log.Printf("部分写入: %d/%d 字节", n, len(data))
    }
}
```

**注意事项​**​：

- 实际写入数小于请求数时为错误
- 追加模式 (`O_APPEND`) 下总是写到文件尾
- 重要错误：
    - `EBADF`：文件未打开为写入
    - `ENOSPC`：磁盘满
    - `EINTR`：信号中断
### 4.1.8 func (f \*File) ReadAt(b \[\]byte, off int64) (n int, err error)

​**​功能​**​：从指定位置读取（不影响偏移）  
​**​参数​**​：

- `b`：目标缓冲区
- `off`：读取位置  
    ​**​返回值​**​：同 `Read`

```go
func readHeader(file *os.File) []byte {
    header := make([]byte, 128)
    _, err := file.ReadAt(header, 0)
    if err != nil {
        log.Fatalf("读取文件头失败: %v", err)
    }
    return header
}
```

**注意事项​**​：

- 独立于文件当前偏移
- 允许超出文件长度（返回 `io.EOF`）
- 重要错误：
    - `ESPIPE`：管道或不可定位
    - `EINVAL`：偏移为负
### 4.1.9 func (f \*File) WriteAt(b \[\]byte, off int64) (n int, err error)

​**​功能​**​：向指定位置写入（不影响偏移）  
​**​参数​**​：

- `b`：数据
- `off`：写入位置  
    ​**​返回值​**​：同 `Write`

```go
func updateFile(file *os.File) {
    timestamp := []byte(time.Now().Format(time.RFC3339))
    _, err := file.WriteAt(timestamp, 100)
    if err != nil {
        log.Fatalf("更新时间戳失败: %v", err)
    }
}
```

**注意事项​**​：

- 如果 `off > 文件大小`，会扩展文件（空洞）
- 不支持管道、终端等特殊文件
### 4.1.10 func (f \*File) Seek(offset int64, whence int) (ret int64, err error)

​**​功能​**​：改变读写位置  
​**​参数​**​：

- `offset`：偏移量
- `whence`：基准位置（0=起始，1=当前，2=末尾）  
    ​**​返回值​**​：
- `ret`：新位置
- `err`：错误

```go
func appendData(file *os.File, data []byte) {
    // 移动到文件末尾
    _, err := file.Seek(0, io.SeekEnd)
    if err != nil {
        log.Fatalf("定位失败: %v", err)
    }
    
    // 追加数据
    _, err = file.Write(data)
    if err != nil {
        log.Fatalf("追加失败: %v", err)
    }
}
```

**注意事项​**​：

- `whence` 使用 io 包常量：
    - `io.SeekStart`
    - `io.SeekCurrent`
    - `io.SeekEnd`
- 返回的新位置可用于验证
- 重要错误：
    - `EINVAL`：无效基准或偏移
    - `ESPIPE`：不可定位
### 4.1.11 func (f \*File) Chmod(mode FileMode) error

​**​功能​**​：修改文件权限  
​**​参数​**​：

- `mode`：新权限位（如 0644）  
    ​**​返回值​**​：错误对象
### 4.1.12 func (f \*File) Chown(uid, gid int) error

​**​功能​**​：修改文件所有者和组  
​**​参数​**​：

- `uid`：用户ID（-1 表示不变）
- `gid`：组ID（-1 表示不变）  
    ​**​返回值​**​：错误对象
### 4.1.13 func (f \*File) Stat() (FileInfo, error)

​**​功能​**​：获取文件元数据  
​**​返回值​**​：

- `FileInfo`：文件信息接口
- `error`：错误对象

```go
func checkSize(file *os.File) {
    info, err := file.Stat()
    if os.IsPermission(err) {
        log.Print("无权限获取文件信息")
        return
    } else if err != nil {
        log.Fatalf("获取文件信息失败: %v", err)
    }
    
    if info.Size() > 1000000 {
        log.Printf("文件过大: %.2f MB", float64(info.Size())/1024/1024)
    }
}
```

**注意事项​**​：

- 信息缓存于文件打开时
- 重要错误：
    - `EBADF`：文件描述符无效
    - `ENOENT`：文件被删除
### 4.1.14 func (f \*File) Truncate(size int64) error

​**​功能​**​：截断/扩展文件  
​**​参数​**​：

- `size`：目标文件大小  
    ​**​返回值​**​：错误对象
### 4.1.15 func (f \*File) Chdir() error

​**​功能​**​：切换到文件所在目录（需为目录）  
​**​返回值​**​：错误对象
### 4.1.16 func (f \*File) ReadDir(n int) (\[\]DirEntry, error)

​**​功能​**​：读取目录内容  
​**​参数​**​：

- `n`：最多返回条目数（≤0 表示全部）  
    ​**​返回值​**​：
- `[]DirEntry`：目录条目切片
- `error`：错误对象

```go
func listDir(dir *os.File) {
    entries, err := dir.ReadDir(-1) // 全部条目
    if os.IsPermission(err) {
        log.Print("无目录读取权限")
        return
    } else if err != nil {
        log.Fatalf("读取目录失败: %v", err)
    }
    
    for _, entry := range entries {
        if entry.IsDir() {
            fmt.Printf("[DIR] %s\n", entry.Name())
        } else {
            fmt.Printf("[FILE] %s\n", entry.Name())
        }
    }
}
```

**注意事项​**​：

- 高效实现（不加载完整信息）
- 返回顺序取决于文件系统
- 重要错误：
    - `EBADF`：文件不是目录
    - `ENOTDIR`：文件描述符无效
### 4.1.17 func (f \*File) Sync() error

​**​功能​**​：同步文件内容到磁盘  
​**​返回值​**​：错误对象

```go
func criticalWrite(file *os.File, data []byte) {
    if _, err := file.Write(data); err != nil {
        log.Fatal("写入失败: ", err)
    }
    
    // 确保数据落盘
    if err := file.Sync(); err != nil {
        if runtime.GOOS == "windows" {
            log.Print("Windows部分文件系统不支持完全同步")
        }
        log.Fatal("数据同步失败: ", err)
    }
}
```

**注意事项​**​：

- 确保数据写入持久化存储
- 可能影响性能
- 重要错误：
    - `EIO`：I/O错误
    - `EROFS`：只读文件系统
### 4.1.18 func (f \*File) Fd() uintptr

​**​功能​**​：获取底层文件描述符  
​**​返回值​**​：文件描述符

```go
func useSystemCall(file *os.File) {
    fd := file.Fd()
    
    // 系统特定操作
    if runtime.GOOS == "linux" {
        // 刷新文件内容
        syscall.Syscall(syscall.SYS_FDATASYNC, fd, 0, 0)
    }
}
```

**注意事项​**​：

- 描述符在文件关闭后失效
- 破坏跨平台性
- 可用于设置非阻塞模式等
### 4.1.19 func (f \*File) SyscallConn() (syscall.RawConn, error)

​**​功能​**​：获取原始连接对象  
​**​返回值​**​：

- `RawConn`：原始连接接口
- `error`：错误对象

```go
func fileLock(file *os.File) error {
    raw, err := file.SyscallConn()
    if err != nil {
        return err
    }
    
    var lockErr error
    err = raw.Control(func(fd uintptr) {
        // 设置写锁定（非阻塞）
        lock := syscall.Flock_t{
            Type:   syscall.F_WRLCK,
            Whence: io.SeekStart,
            Start:  0,
            Len:    0,
            Pid:    int32(os.Getpid()),
        }
        lockErr = syscall.FcntlFlock(fd, syscall.F_SETLK, &lock)
    })
    if err != nil {
        return err
    }
    return lockErr
}
```

**注意事项​**​：

- 可执行自定义系统调用
- 高级用户功能
- 需要理解底层系统机制
### 4.1.20 func (f \*File) SetDeadline(t time.Time) error

​**​功能​**​：设置读写操作的绝对截止时间  
​**​返回值​**​：错误对象

**适用于网络文件系统​**​：

```go
func readNetworkFile(file *os.File) {
    // 设置10秒超时
    if err := file.SetDeadline(time.Now().Add(10 * time.Second)); err != nil {
        log.Fatalf("设置超时失败: %v", err)
    }
    
    buf := make([]byte, 1024)
    _, err := file.Read(buf)
    if os.IsTimeout(err) {
        log.Fatal("网络文件读取超时")
    } else if err != nil {
        log.Fatalf("读取失败: %v", err)
    }
}
```

**注意事项​**​：

- 同时影响读写操作
- 适用于网络/管道文件
- 重要错误：
    - `ENOTSOCK`：文件不是套接字
### 4.1.21 func (f \*File) Name() string

**功能​**​：获取文件名（打开时的路径）  
​**​返回值​**​：文件名

```go
func logFileName(file *os.File) { log.Printf("操作文件: %s", file.Name()) }
```

**注意事项​**​：

- 可能为相对路径
- 文件移动或重命名后不变
- 不保证文件仍存在
### 4.1.22 func (f \*File) Close() error

​**​功能​**​：关闭文件  
​**​返回值​**​：错误对象（通常为 nil）

```go
func processFile(path string) error {
    file, err := os.Open(path)
    if err != nil {
        return err
    }
    defer file.Close() // 确保关闭
    
    // 处理文件内容...
    return nil
}
```

**注意事项​**​：

- 必须调用以释放资源
- 多次关闭可能导致 panic
- 关闭后所有操作失败
## 4.2 FileInfo接口

```go
type FileInfo = fs.FileInfo // 从Go 1.16起成为fs.FileInfo的别名

// 接口方法：
type FileInfo interface {
    Name() string       // 基础文件名（不含路径）
    Size() int64        // 文件大小(字节)
    Mode() FileMode     // 文件权限和类型
    ModTime() time.Time // 最后修改时间
    IsDir() bool        // 是否为目录
    Sys() interface{}   // 底层系统数据
}
```
### 4.2.1 func Stat(name string) (FileInfo, error)

**功能​**​：获取文件详细信息（​**​跟随符号链接​**​）  
​**​返回值​**​：

- `FileInfo`：文件信息对象
- `error`：错误信息（通常是`*PathError`类型）

### 4.2.2 func Lstat(name string) (FileInfo, error)

**功能​**​：获取文件信息（​**​不跟随符号链接​**​）  
​**​返回值​**​：

- `FileInfo`：文件信息对象（符号链接自身）
- `error`：错误信息（通常是`*PathError`类型）
## 4.3 DirEntry接口

```go
type DirEntry = fs.DirEntry

// 接口方法：
type DirEntry interface {
    Name() string          // 基础文件名
    IsDir() bool           // 是否为目录
    Type() FileMode        // 文件类型位 (不需要访问磁盘)
    Info() (FileInfo, error) // 完整元数据 (可能需要磁盘访问)
}
```
### 4.3.1 func ReadDir(name string) (\[\]DirEntry, error)

- **功能**：跟 `File.ReadDir` 方法一致。
### 4.3.2 DirEntry与FileInfo对比

| ​**​特性​**​   | ​**​DirEntry​**​                        | ​**​FileInfo​**​                          |
| ------------ | --------------------------------------- | ----------------------------------------- |
| ​**​核心目的​**​ | 快速目录遍历优化                                | 完整文件元数据表示                                 |
| ​**​设计目标​**​ | 最小化系统开销                                 | 提供完整文件信息                                  |
| ​**​获取成本​**​ | ⚡ 低成本（通常不需要额外系统调用）                      | ⚠️ 高成本（可能需要单独系统调用）                        |
| ​**​实现来源​**​ | 目录读取操作（如 readdir）                       | 文件状态获取（如 stat、fstat）                      |
| ​**​主要方法​**​ | `Name()`, `IsDir()`, `Type()`, `Info()` | `Name()`, `Size()`, `Mode()`, `ModTime()` |
| ​**​使用场景​**​ | 批量目录列表、递归遍历                             | 文件详情展示、权限检查、大小统计                          |
| ​**​扩展功能​**​ | 可延迟加载完整信息                               | 包含系统特定数据（Sys()方法）                         |
| ​**​性能影响​**​ | ✅ 高效（避免不必要的系统调用）                        | ❌ 可能显著影响性能                                |
## 4.4 FileMode类型

`FileMode`是Go语言中表示文件模式和权限的核心类型。

```go
type FileMode = fs.FileMode // 底层为uint32类型
```

### 4.4.1 核心特性

1. ​**​跨平台一致性​**​：所有系统使用相同的位定义
2. ​**​位掩码组合​**​：通过位运算组合多种属性
3. ​**​目录强制要求​**​：`ModeDir`位唯一所有平台必需的标志位
4. ​**​权限独立​**​：权限位在所有系统有效

| 常量               | 值 (八进制)        | 描述       | 典型示例                   |
| ---------------- | -------------- | -------- | ---------------------- |
| `ModeDir`        | `040000`       | 目录       | `/usr/bin`             |
| `ModeAppend`     | `020000000000` | 只追加模式    | 日志文件                   |
| `ModeExclusive`  | `020000000000` | 独占使用     | 数据库文件                  |
| `ModeTemporary`  | `010000000000` | 临时文件     | `*.tmp`                |
| `ModeSymlink`    | `0120000`      | 符号链接     | 快捷方式                   |
| `ModeDevice`     | `0060000`      | 设备文件     | `/dev/sda`             |
| `ModeNamedPipe`  | `0010000`      | 命名管道     | IPC管道                  |
| `ModeSocket`     | `0140000`      | Unix域套接字 | `/var/run/docker.sock` |
| `ModeSetuid`     | `0004000`      | SetUID位  | `/usr/bin/passwd`      |
| `ModeSetgid`     | `0002000`      | SetGID位  | `/usr/bin/wall`        |
| `ModeSticky`     | `0001000`      | 粘滞位      | `/tmp`                 |
| `ModeCharDevice` | `0020000`      | 字符设备     | `/dev/tty`             |
| `ModeIrregular`  | `0100000`      | 非常规文件    | 特殊文件                   |

```go
// 文件类型判断
func printFileType(mode os.FileMode) {
    switch {
    case mode.IsDir():
        fmt.Println("目录")
    case mode.IsRegular():
        fmt.Println("普通文件")
    case mode&os.ModeSymlink != 0:
        fmt.Println("符号链接")
    case mode&os.ModeDevice != 0:
        if mode&os.ModeCharDevice != 0 {
            fmt.Println("字符设备")
        } else {
            fmt.Println("块设备")
        }
    case mode&os.ModeNamedPipe != 0:
        fmt.Println("命名管道")
    case mode&os.ModeSocket != 0:
        fmt.Println("套接字")
    case mode&os.ModeIrregular != 0:
        fmt.Println("非常规文件")
    default:
        fmt.Println("未知类型")
    }
}
```
## 4.5 ProAttr类型

`ProcAttr` 是 Go 语言中用于控制新进程创建的关键结构体，包含子进程的配置信息：

```go
type ProcAttr struct {
    Dir  string              // 子进程工作目录
    Env  []string            // 子进程环境变量
    Files []*os.File         // 继承的文件句柄
    Sys  *syscall.SysProcAttr // 系统特定属性
}
```

```go
// 子进程启动前切换的工作目录
// 空值表示继承父进程工作目录

func StartWithWorkdir() {
    // 创建临时工作目录
    tempDir, _ := os.MkdirTemp("", "appdata_")

    cleanEnv := []string{ "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin", "HOME=/var/empty", "USER=nobody", }
    
    attr := &os.ProcAttr{
        Dir: tempDir,
        Env: cleanEnv,
        Files: []*os.File{
            os.Stdin,  // 标准输入
            os.Stdout,  // 标准输出
            os.Stderr,  // 标准错误
        },
    }
    
    // 启动子进程
    cmd := "/usr/bin/myapp"
    proc, _ := os.StartProcess(cmd, []string{"myapp"}, attr)
    defer proc.Close()
    
    // 验证工作目录
    pid := proc.Pid
    fmt.Printf("子进程 %d 在 %s 中运行\n", pid, tempDir)
}
```

1. Dir：工作目录控制
    - 设置后改变 `os.Getwd()` 结果
    - 路径不存在时启动失败
    - Windows 路径格式敏感
2. Env：环境变量定制
3. Files：文件句柄继承

```go
// 继承的文件句柄列表
// 索引0: 标准输入(Stdin)
// 索引1: 标准输出(Stdout)
// 索引2: 标准错误(Stderr)
```
## 4.6 Process类型

`os.Process` 类型表示一个正在运行或已经退出的操作系统进程。它包含了该进程的信息以及用于操作该进程的方法。

```go
type Process struct {
	Pid int
	// contains filtered or unexported fields
}
```
### 4.6.1 FindProcess(pid int) (\*Process, error)

​**​功能​**​：根据进程ID查找现有进程  
​**​参数​**​：

- `pid`：目标进程ID（PID）

​**​返回值​**​：

- `*Process`：进程对象指针
- `error`：错误信息

​**​关键特性​**​：

- Unix系统：即使进程不存在也可能返回对象（需配合Signal验证）
- Windows系统：无效PID直接返回错误
- 权限要求：需有权限操作目标进程

```go
func findAndSignalProcess(pid int) {
    // 查找进程
    proc, err := os.FindProcess(pid)
    if err != nil {
        log.Fatalf("无法查找进程 %d: %v", pid, err)
    }
    
    // Unix: 验证进程是否存在
    if runtime.GOOS != "windows" {
        if err := proc.Signal(syscall.Signal(0)); err != nil {
            log.Printf("进程 %d 不存在或无法访问", pid)
            return
        }
    }
    
    // 发送SIGTERM优雅终止
    if err := proc.Signal(syscall.SIGTERM); err != nil {
        log.Printf("终止信号发送失败: %v", err)
    } else {
        log.Printf("已发送终止信号给进程 %d", pid)
    }
}
```
### 4.6.2 StartProcess(name string, argv \[\]string, attr \*ProcAttr) (\*Process, error)

**功能​**​：启动新进程  
​**​参数​**​：

- `name`：可执行文件路径
- `argv`：命令行参数（`argv[0]`通常为程序名）
- `attr`：进程属性配置

​**​返回值​**​：

- `*Process`：新启动的进程对象
- `error`：启动错误

​**​关键特性​**​：

- 与父进程环境隔离
- 文件句柄自动继承（仅限attr.Files指定）
- 跨平台支持不同执行策略

```go
func launchBackgroundService() {
    // 配置进程属性
    attr := &os.ProcAttr{
        Files: []*os.File{os.Stdin, os.Stdout, os.Stderr},
        Env:   append(os.Environ(), "APP_MODE=BACKGROUND"),
        Sys:   configureSysProcAttr(), // 系统特有配置
    }
    
    // 启动后台进程
    binPath, _ := exec.LookPath("my_service")
    proc, err := os.StartProcess(binPath, []string{"my_service", "--daemon"}, attr)
    if err != nil {
        log.Fatalf("服务启动失败: %v", err)
    }
    
    // 监控进程状态（非阻塞）
    go func(p *os.Process) {
        state, _ := p.Wait()
        if state.Success() {
            log.Printf("服务 %d 正常退出", p.Pid)
        } else {
            log.Printf("服务异常退出: %v", state)
        }
    }(proc)
    
    log.Printf("后台服务已启动 PID: %d", proc.Pid)
}

// 平台相关配置
func configureSysProcAttr() *syscall.SysProcAttr {
    if runtime.GOOS == "windows" {
        return &syscall.SysProcAttr{HideWindow: true}
    }
    return &syscall.SysProcAttr{Setpgid: true}
}
```

### 4.6.3 Kill() error

​**​功能​**​：立即强制终止进程（`SIGKILL`/`TerminateProcess`）  
​**​返回值​**​：操作错误

​**​关键特性​**​：

- Unix: 发送SIGKILL信号
- Windows: 调用TerminateProcess API
- 无资源清理，强制终止

```go
func forceKillProcess(proc *os.Process) {
    // 尝试优雅终止
    if err := proc.Signal(gracefulSignal()); err == nil {
        // 设置超时后强制终止
        select {
        case <-time.After(5 * time.Second):
            log.Println("进程未响应，强制终止")
            if err := proc.Kill(); err != nil {
                log.Printf("强制终止失败: %v", err)
            }
        }
    } else {
        // 直接强制终止
        if err := proc.Kill(); err != nil {
            log.Printf("终止操作失败: %v", err)
        }
    }
}

func gracefulSignal() os.Signal {
    if runtime.GOOS == "windows" {
        return os.Interrupt
    }
    return syscall.SIGTERM
}
```
### 4.6.4 Release() error

​**​功能​**​：释放进程资源，不影响进程运行  
​**​返回值​**​：操作错误

​**​关键特性​**​：

- 仅释放父进程持有的资源
- 不会终止目标进程
- 调用后无法再操作此进程

```go
func trackProcessWithoutHolding(pid int) {
    proc, err := os.FindProcess(pid)
    if err != nil {
        log.Printf("查找进程失败: %v", err)
        return
    }
    
    // 记录进程信息后立即释放资源
    log.Printf("开始监控进程 %d", pid)
    proc.Release()  // 防止资源泄露
    
    // 继续监控但不持有资源
    go monitorExternalProcess(pid)
}
```
### 4.6.5 Signal(sig Signal) error

​**​功能​**​：向进程发送指定信号  
​**​参数​**​：

- `sig`：要发送的信号

​**​返回值​**​：操作错误

​**​关键特性​**​：

- Unix: 支持所有标准POSIX信号
- Windows: 仅支持特定信号：
    - `os.Interrupt` (Ctrl+C)
    - `os.Kill` (强制终止)
- 需目标进程可接收信号

```go
func sendProcessSignal(pid int, sigName string) error {
    proc, err := os.FindProcess(pid)
    if err != nil {
        return err
    }
    
    // 将信号名称转换为Signal对象
    sig, err := parseSignal(sigName)
    if err != nil {
        return err
    }
    
    return proc.Signal(sig)
}

func parseSignal(name string) (os.Signal, error) {
    switch strings.ToUpper(name) {
    case "SIGHUP", "HUP":
        return syscall.SIGHUP, nil
    case "SIGINT", "INT":
        return os.Interrupt, nil
    case "SIGTERM", "TERM":
        return syscall.SIGTERM, nil
    case "SIGKILL", "KILL":
        return os.Kill, nil
    case "SIGUSR1", "USR1":
        return syscall.SIGUSR1, nil
    default:
        return nil, fmt.Errorf("不支持的信号类型: %s", name)
    }
}
```
### 4.6.6 Wait() (\*ProcessState, error)

​**​功能​**​：等待进程结束并返回状态  
​**​返回值​**​：

- `*ProcessState`：进程结束状态
- `error`：等待错误

​**​关键特性​**​：

- 阻塞调用直到进程退出
- 自动释放进程资源
- 对每个进程应调用且仅调用一次

```go

```
## 4.7 ProcessState

`os.ProcessState` 类型表示一个已退出进程的状态信息，它由`Process.Wait`方法返回。

```go
type ProcessState struct {
    // 非导出字段
}

func (p *ProcessState) ExitCode() int      // Windows: 返回退出码
func (p *ProcessState) Exited() bool       // 进程是否已退出
func (p *ProcessState) Success() bool      // 是否成功退出(Unix: status=0, Windows: exitCode=0)
func (p *ProcessState) SystemTime() time.Duration  // 进程系统CPU时间
func (p *ProcessState) UserTime() time.Duration    // 进程用户CPU时间
func (p *ProcessState) String() string     // 格式化输出状态信息
```

```go
func analyzeProcessState(proc *os.Process) {
    state, err := proc.Wait()
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Printf("进程 %d 结束状态:\n", proc.Pid)
    fmt.Printf("  退出码: %d\n", state.ExitCode())
    fmt.Printf("  成功退出: %v\n", state.Success())
    fmt.Printf("  用户CPU时间: %v\n", state.UserTime())
    fmt.Printf("  系统CPU时间: %v\n", state.SystemTime())
    fmt.Printf("  总运行时间: %v\n", time.Since(startTime))
    
    if runtime.GOOS == "windows" {
        // Windows特有信息
    } else if sys, ok := state.Sys().(syscall.WaitStatus); ok {
        fmt.Printf("  终止信号: %v\n", sys.Signal())
        fmt.Printf("  核心转储: %v\n", sys.CoreDump())
    }
}
```
## 4.8 Signal接口

该接口表示操作系统信号。通常，底层的实现是依赖于操作系统的：在Unix系统上，它是 syscall.Signal 类型。

```go
type Signal interface {
	String() [string](https://pkg.go.dev/builtin#string)
	Signal() // to distinguish from other Stringers
}
```

- 预定义常量

```go
var (
    Interrupt Signal = syscall.SIGINT   // 中断信号 (Ctrl+C)
    Kill      Signal = syscall.SIGKILL  // 强制终止信号
)
```
## 4.9 Root类型

`Root` 类型是 Go 1.24 引入的文件系统安全隔离机制，用于​**​限制访问仅限于单一目录树​**​，增强了应用的文件系统操作安全性。

**设计特点**：

1. ​**​单目录树限制​**​：所有操作限制在根目录下
2. ​**​符号链接保护​**​：允许符号链接但禁止引用根目录外
3. ​**​并发安全​**​：多个 goroutine 可安全调用
4. ​**​路径逃逸防护​**​：组件路径外引用导致错误
5. ​**​平台特定行为​**​：不同系统有不同限制

|​**​函数/方法名​**​|​**​声明​**​|​**​作用​**​|​**​实现细节​**​|​**​参数说明​**​|​**​返回值​**​|​**​注意事项​**​|
|---|---|---|---|---|---|---|
|​**​OpenRoot​**​|`func OpenRoot(name string) (*Root, error)`|打开指定目录作为安全操作的根对象|创建文件描述符/句柄，锁定目录位置|`name string`: 目录路径|`*Root`: 根对象  <br>`error`: 错误对象|错误情况：  <br>- `ErrNotExist`：目录不存在  <br>- `ErrPermission`：权限不足  <br>- Windows：拒绝保留设备名（NUL/COM1等）|
|​**​Close​**​|`func (r *Root) Close() error`|关闭并释放根对象资源|释放文件描述符/句柄，标记为关闭状态|无|`error`: 关闭错误|关闭后所有操作返回错误  <br>应使用 `defer` 确保释放资源|
|​**​Create​**​|`func (r *Root) Create(name string) (*File, error)`|在根下创建文件（截断存在文件）|调用 `OpenFile(name, O_RDWR\|O_CREATE\|O_TRUNC, 0666)`|`name string`: 相对路径|`*File`: 文件对象  <br>`error`: 错误对象|路径检查：  <br>1. 禁止 `../` 逃逸  <br>2. 符号链接必须在根内  <br>Windows：过滤保留设备名|
|​**​FS​**​|`func (r *Root) FS() fs.FS`|获取根目录的只读文件系统接口|返回实现 `fs.StatFS`, `fs.ReadFileFS`, `fs.ReadDirFS` 的结构体|无|`fs.FS`: 只读文件系统|不支持写操作  <br>兼容 `io/fs` 生态系统|
|​**​Lstat​**​|`func (r *Root) Lstat(name string) (FileInfo, error)`|获取文件元数据（不解引用符号链接）|通过 `syscall.Lstat` 实现|`name string`: 相对路径|`FileInfo`: 文件信息  <br>`error`: 错误对象|符号链接：返回链接自身信息  <br>边界检查：  <br>- 路径必须在根下  <br>- 符号链接目标不验证|
|​**​Mkdir​**​|`func (r *Root) Mkdir(name string, perm FileMode) error`|创建子目录|调用 `syscall.Mkdir`，权限受 umask 影响|`name string`: 目录路径  <br>`perm FileMode`: 权限位|`error`: 错误对象|权限限制：  <br>仅允许低9位权限位(0o777)  <br>错误：  <br>- `EEXIST`: 目录已存在  <br>- `EPERM`: 权限不足|
|​**​Name​**​|`func (r *Root) Name() string`|获取根目录原始路径|返回 `OpenRoot()` 输入的路径字符串|无|`string`: 根目录路径|关闭后仍可调用  <br>返回值未规范化  <br>Windows：保留大小写原始输入|
|​**​Open​**​|`func (r *Root) Open(name string) (*File, error)`|以只读方式打开文件|调用 `OpenFile(name, O_RDONLY, 0)`|`name string`: 相对路径|`*File`: 文件对象  <br>`error`: 错误对象|仅支持读取  <br>打开目录会成功但后续读取失败  <br>路径必须存在于根下|
|​**​OpenFile​**​|`func (r *Root) OpenFile(name string, flag int, perm FileMode) (*File, error)`|完整控制的文件打开|包含所有标准打开标志|`name string`: 相对路径  <br>`flag int`: 打开标志  <br>`perm FileMode`: 权限位|`*File`: 文件对象  <br>`error`: 错误对象|权限限制：  <br>仅允许低9位权限位  <br>标志兼容性：  <br>支持所有标准 `os.OpenFile` 标志|
|​**​OpenRoot​**​|`func (r *Root) OpenRoot(name string) (*Root, error)`|在现有根下打开子目录作为新根|类似 `OpenRoot` 但使用相对路径|`name string`: 子目录路径|`*Root`: 新根对象  <br>`error`: 错误对象|深度限制：  <br>最多允许32层嵌套  <br>目标必须存在且为目录  <br>Plan9：不跟踪目录重命名|
|​**​Remove​**​|`func (r *Root) Remove(name string) error`|删除文件或空目录|调用 `syscall.Unlink` 或 `syscall.Rmdir`|`name string`: 相对路径|`error`: 错误对象|限制：  <br>- 不能删除非空目录  <br>- 符号链接删除链接自身  <br>错误：  <br>- `ENOTEMPTY`：目录非空|
|​**​Stat​**​|`func (r *Root) Stat(name string) (FileInfo, error)`|获取文件元数据（解引用符号链接）|通过 `syscall.Stat` 实现|`name string`: 相对路径|`FileInfo`: 文件信息  <br>`error`: 错误对象|与Lstat区别：  <br>返回目标文件信息  <br>安全注意：  <br>可访问符号链接指向的根外文件(但被系统阻止)|
```go
package main

import (
	"fmt"
	"io"
	"io/fs"
	"os"
	"path/filepath"
	"runtime"
)

// Root 安全文件操作演示
func main() {
	// 1. 创建临时工作区
	tempDir, err := os.MkdirTemp("", "root-demo")
	if err != nil {
		panic(fmt.Errorf("创建临时目录失败: %w", err))
	}
	defer os.RemoveAll(tempDir) // 清理临时文件

	fmt.Printf("工作目录: %s\n", tempDir)

	// 2. 打开根目录
	root, err := os.OpenRoot(tempDir)
	if err != nil {
		panic(fmt.Errorf("打开根目录失败: %w", err))
	}
	defer root.Close()

	fmt.Printf("根名称: %s\n", root.Name())

	// 3. 在根下创建文件
	fileContent := "安全文件操作示例"
	if err := writeFile(root, "data.txt", fileContent); err != nil {
		panic(err)
	}

	// 4. 读取文件内容
	content, err := readFile(root, "data.txt")
	if err != nil {
		panic(err)
	}
	fmt.Printf("文件内容: %q\n", content)

	// 5. 创建子目录
	if err := root.Mkdir("docs", 0700); err != nil {
		panic(fmt.Errorf("创建docs目录失败: %w", err))
	}

	// 6. 在子目录中创建文件
	subContent := "子目录中的内容"
	if err := writeFile(root, "docs/note.txt", subContent); err != nil {
		panic(err)
	}

	// 7. 打开子根目录
	subRoot, err := root.OpenRoot("docs")
	if err != nil {
		panic(fmt.Errorf("打开子根目录失败: %w", err))
	}
	defer subRoot.Close()

	fmt.Println("子根目录内容:")
	if err := listDir(subRoot); err != nil {
		panic(err)
	}

	// 8. 尝试路径逃逸（安全验证）
	if err := escapeAttempt(root); err != nil {
		fmt.Printf("安全拦截: %v\n", err)
	}

	// 9. 清理操作
	if err := cleanup(root); err != nil {
		panic(err)
	}

	fmt.Println("所有操作成功完成!")
}

// writeFile 在根下安全写入文件
func writeFile(root *os.Root, name, content string) error {
	// 文件名安全处理
	safeName := filepath.Base(name) // 防止目录遍历
	
	file, err := root.Create(safeName)
	if err != nil {
		return fmt.Errorf("创建文件失败: %w", err)
	}
	defer file.Close()

	_, err = file.WriteString(content)
	if err != nil {
		return fmt.Errorf("写入内容失败: %w", err)
	}
	
	fmt.Printf("文件创建成功: %s\n", safeName)
	return nil
}

// readFile 安全读取文件内容
func readFile(root *os.Root, name string) (string, error) {
	// 使用只读FS接口
	fsys := root.FS()
	
	content, err := fs.ReadFile(fsys, name)
	if err != nil {
		return "", fmt.Errorf("读取文件失败: %w", err)
	}
	
	return string(content), nil
}

// listDir 列出根目录内容
func listDir(root *os.Root) error {
	dir, err := root.Open(".")
	if err != nil {
		return fmt.Errorf("打开目录失败: %w", err)
	}
	defer dir.Close()

	entries, err := dir.Readdir(-1)
	if err != nil {
		return fmt.Errorf("读取目录失败: %w", err)
	}

	for _, entry := range entries {
		fmt.Printf(" - %s (目录: %v)\n", entry.Name(), entry.IsDir())
	}
	return nil
}

// escapeAttempt 尝试路径逃逸（验证安全机制）
func escapeAttempt(root *os.Root) error {
	testNames := []string{
		"../escape.txt",        // 上级目录引用
		"safe/../../escape.txt", // 多层逃逸尝试
	}
	
	for _, name := range testNames {
		_, err := root.Create(name)
		if err == nil {
			return fmt.Errorf("安全漏洞: %s 创建成功", name)
		}
		fmt.Printf("拦截逃逸尝试: %s -> %v\n", name, err)
	}
	
	// 验证符号链接安全
	if runtime.GOOS != "windows" {
		symlinkPath := filepath.Join(root.Name(), "link")
		targetPath := filepath.Join(root.Name(), "../../")
		os.Symlink(targetPath, symlinkPath)
		
		_, err := root.Open("link")
		if err == nil {
			return fmt.Errorf("符号链接逃逸成功")
		}
		fmt.Printf("拦截符号链接逃逸: %v\n", err)
	}
	
	return nil
}

// cleanup 清理根目录内容
func cleanup(root *os.Root) error {
	// 删除文件
	if err := root.Remove("data.txt"); err != nil {
		return fmt.Errorf("删除文件失败: %w", err)
	}
	
	// 删除子目录及其内容
	if err := removeAll(root, "docs"); err != nil {
		return err
	}
	
	return nil
}

// removeAll 安全删除子目录
func removeAll(root *os.Root, path string) error {
	// 打开子目录
	subDir, err := root.Open(path)
	if err != nil {
		return fmt.Errorf("打开目录失败: %w", err)
	}
	defer subDir.Close()
	
	// 删除目录内容
	names, err := subDir.Readdirnames(-1)
	if err != nil {
		return fmt.Errorf("读取目录失败: %w", err)
	}
	
	for _, name := range names {
		fullPath := filepath.Join(path, name)
		err := root.Remove(fullPath)
		if err != nil {
			return fmt.Errorf("删除文件失败: %w", err)
		}
	}
	
	// 删除空目录
	if err := root.Remove(path); err != nil {
		return fmt.Errorf("删除目录失败: %w", err)
	}
	
	fmt.Printf("目录已删除: %s\n", path)
	return nil
}
```