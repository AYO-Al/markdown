| ​**​特性​**​        | `path` 包    | filepath 包           |
| ----------------- | ----------- | -------------------- |
| ​**​目标场景​**​      | 通用路径（如 URL） | 操作系统文件路径             |
| ​**​分隔符​**​       | 仅支持 `/`     | 自动适配系统分隔符（`/` 或 `\`） |
| ​**​跨平台处理能力​**​   | 无           | 是                    |
| ​**​通配符匹配的分隔符​**​ | 仅 `/`       | 系统分隔符                |
# 1 **路径拼接：`Join(elem ...string) string`​**​


```go
path.Join("a", "b/c", "../d") // 输出 "a/b/d"
```

# 2 ​**​路径分割：`Split(path string) (dir, file string)`​**​


```go
dir, file := path.Split("a/b/c.txt") 
// dir = "a/b/", file = "c.txt"
```

# 3 ​**​获取路径最后部分：`Base(path string) string`​**​


```go
path.Base("a/b/c.txt") // 输出 "c.txt"
```

# 4 ​**​获取上级目录：`Dir(path string) string`​**​


```go
path.Dir("a/b/c.txt") // 输出 "a/b"
```

# 5 ​**​获取扩展名：`Ext(path string) string`​**​

```go
path.Ext("file.txt") // 输出 ".txt"
```

# 6 ​**​路径规范化：`Clean(path string) string`​**​


```go
path.Clean("a/../b/./c") // 输出 "b/c"
```

# 7 ​**​通配符匹配：`Match(pattern, name string) (bool, error)`​**​


```go
matched, _ := path.Match("a/*/c", "a/b/c") // 输出 true
```