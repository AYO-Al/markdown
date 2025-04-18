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