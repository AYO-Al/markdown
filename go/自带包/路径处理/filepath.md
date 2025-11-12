`path/filepath` 包是用于处理 ​**​文件路径​**​ 的核心工具，尤其擅长解决跨平台（Windows、Unix 等）的路径兼容性问题。

filepath 包使用正斜杠或反斜杠，具体取决于作系统。要处理始终使用正斜杠的 URL 等路径，而不考虑作系统，请参阅 [path](path.md) 包。

- **路径拼接与分割​**​：自动处理不同操作系统的路径分隔符（`/` 或 `\`）。
- ​**​路径规范化​**​：消除冗余（如 `..` 和 `.`），生成简洁的绝对或相对路径。
- ​**​通配符匹配​**​：支持 `*` 和 `?` 等模式匹配文件路径。
- ​**​跨平台兼容​**​：透明适配不同操作系统的路径规则。

|​**​特性​**​|`path` 包|`filepath` 包|
|---|---|---|
|​**​适用场景​**​|通用斜杠路径（如 URL）|文件系统路径（处理 OS 差异）|
|​**​分隔符处理​**​|固定使用 `/`|自动适配当前系统的分隔符|
|​**​跨平台支持​**​|无|是|
# 1 **`路径拼接 Join(elem ...string) string`​**

```go
// 自动处理分隔符和冗余路径
path := filepath.Join("dir", "sub", "../file.txt") 
// Unix → "dir/file.txt", Windows → "dir\file.txt"​
```

# 2 **路径分割：`Split(path string) (dir, file string)`​**

```go
dir, file := filepath.Split("/home/user/docs/file.txt")
// dir = "/home/user/docs/", file = "file.txt"
```

# 3 **获取绝对路径：`Abs(path string) (string, error)`​**

```go
absPath, _ := filepath.Abs("file.txt") 
// 返回当前目录下的绝对路径，如 "/home/user/file.txt"
```

# 4 **获取相对路径：`Rel(basepath, targpath string) (string, error)`​**

```go
rel, _ := filepath.Rel("/home/user", "/home/user/docs/file.txt")
// rel → "docs/file.txt"
```

# 5 **路径规范化：`Clean(path string) string`​**

```go
cleanPath := filepath.Clean("dir/.././file.txt") 
// → "file.txt"
```

# 6 **通配符匹配：`Match(pattern, name string) (bool, error)`​**

```go
​matched, _ := filepath.Match("*.go", "main.go") 
// → true
```

# 7 **文件搜索：`Glob(pattern string) ([]string, error)`​**

```go
files, _ := filepath.Glob("data/*.csv") 
// 匹配所有 CSV 文件，如 ["data/1.csv", "data/2.csv"]
```

# 8 **目录遍历：`Walk(root string, walkFn WalkFunc) error`​**

```go
err := filepath.Walk(".", func(path string, info os.FileInfo, err error) error {
    if !info.IsDir() {
        fmt.Println("文件:", path)
    }
    return nil
})
```

# 9 常量

| ​**​常量​**​      | 说明                   | 示例值（Windows/Unix） |
| --------------- | -------------------- | ----------------- |
| `Separator`     | 路径分隔符（如 `\` 或 `/`）   | `'\\'` 或 `'/'`    |
| `ListSeparator` | 环境变量分隔符（如 `;` 或 `:`） | `';'` 或 `':'`     |

| 分类              | 函数名                                              | 主要作用说明                                               | 使用示例 (输入 → 输出)                                                                                  | 注意事项                                                             |
| --------------- | ------------------------------------------------ | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| ​**​路径构建与清理​**​ | `Join(elem ...string) string`                    | ​**​安全地连接​**​多个路径片段，自动处理分隔符。是拼接路径的​**​首选方法​**​。      | `filepath.Join("a", "b", "c")`→ `a/b/c`(Unix) 或 `a\b\c`(Windows)                                | 比手动字符串拼接更安全可靠，会自动清理多余的分隔符 <br><br>。                              |
|                 | `Clean(path string) string`                      | ​**​清理和简化​**​路径，去除多余的`..`、`.`和重复的分隔符，返回最简形式。         | `filepath.Clean("a/../b/./c")`→ `b/c`                                                           | 仅通过字符串处理，不会在文件系统中检查路径是否存在 <br><br>。                              |
| ​**​路径分解​**​    | `Split(path string) (dir, file string)`          | ​**​分割路径​**​为目录部分（`dir`）和文件名部分（`file`）。              | `filepath.Split("/home/user/file.txt")`→ `("/home/user/", "file.txt")`                          | 如果路径中无分隔符，`dir`为空字符串，`file`为整个路径 <br><br>。                       |
|                 | `Dir(path string) string`                        | 获取路径中​**​最后一个分隔符之前​**​的部分（目录路径）。                     | `filepath.Dir("/home/user/file.txt")`→ `/home/user`                                             | 返回的路径通常不以分隔符结尾，除非是根目录 <br><br>。                                  |
|                 | `Base(path string) string`                       | 获取路径中​**​最后一个分隔符之后​**​的部分（文件或目录名）。                   | `filepath.Base("/home/user/file.txt")`→ `file.txt`                                              | 如果路径为空，返回 "."；如果路径全为分隔符，返回单个分隔符 <br><br>。                        |
|                 | `Ext(path string) string`                        | 获取文件的​**​扩展名​**​（包括点号，如`.txt`）。                      | `filepath.Ext("archive.tar.gz")`→ `.gz`                                                         | 返回最后一个点开始的后缀。如果没有点，则返回空字符串 <br><br>。                             |
| ​**​路径检查与转换​**​ | `IsAbs(path string) bool`                        | 判断路径是否为​**​绝对路径​**​。                                 | `filepath.IsAbs("/home/user")`→ `true`(Unix)  <br>`filepath.IsAbs("C:\Users")`→ `true`(Windows) | 结果依赖于操作系统。                                                       |
|                 | `Abs(path string) (string, error)`               | 返回路径的​**​绝对路径​**​表示。如果路径不是绝对路径，会将其与当前工作目录连接。         | `filepath.Abs("file.txt")`→ `("/current/working/dir/file.txt", nil)`                            | 如果路径无法转换为绝对路径（如无效字符），会返回错误。                                      |
|                 | `Rel(basepath, targpath string) (string, error)` | 计算从 `basepath`到 `targpath`的​**​相对路径​**​。             | `filepath.Rel("/a/b", "/a/b/c/d")`→ `c/d`                                                       | `basepath`和 `targpath`必须都是相对路径或都是绝对路径，否则会报错 <br><br>。            |
|                 | `ToSlash(path string) string`                    | 将路径分隔符统一转换为​**​斜杠(`/`)​**​，常用于格式化输出。                 | `filepath.ToSlash("C:\a\b")`→ `C:/a/b`                                                          | 主要用于标准化路径表示，不用于实际文件操作。                                           |
|                 | `FromSlash(path string) string`                  | 将路径中的斜杠(`/`)转换为​**​当前系统的路径分隔符​**​。                   | `filepath.FromSlash("a/b/c")`→ `a\b\c`(Windows)                                                 |                                                                  |
|                 | `VolumeName(path string) string`                 | （主要在Windows下）返回路径的​**​卷名​**​（如 `C:`）。                | `filepath.VolumeName("C:\\foo\\bar")`→ `C:`                                                     | 在类Unix系统上，通常返回空字符串。                                              |
| ​**​路径匹配与遍历​**​ | `Match(pattern, name string) (bool, error)`      | 检查文件名是否与​**​Shell风格的通配符模式​**​（如`*.go`, `test?.*`）匹配。 | `filepath.Match("*.go", "hello.go")`→ `true, nil`                                               | 模式要求匹配整个文件名，而非一部分。`*`不匹配路径分隔符 <br><br>。                          |
|                 | `Glob(pattern string) (matches []string, error)` | ​**​查找所有匹配模式​**​的文件路径。                               | `filepath.Glob("*.go")`→ `["hello.go", "main.go"]`, `nil`                                       | 适用于简单的模式匹配。对于复杂遍历，`Walk`更强大 <br><br>。                            |
|                 | `Walk(root string, walkFn WalkFunc) error`       | ​**​递归遍历​**​指定目录及其所有子目录，对每个文件/目录执行自定义操作。             | 详见下方示例代码。                                                                                       | 对于大型目录树，性能开销可能较大。Go 1.16 引入了更高效的 `WalkDir`函数，建议在新代码中使用 <br><br>。 |