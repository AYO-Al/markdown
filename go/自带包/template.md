# 1 text/template

这是 Go 标准库中用于生成​**​纯文本内容​**​的模板引擎，与 `html/template` 类似，但​**​不提供自动转义​**​功能。

 **核心用途​**​
- 生成代码、配置文件、日志、邮件内容等​**​非 HTML 文本​**​。
- 适用于需要动态生成结构化文本的场景（如 SQL 语句、CLI 输出）。

模板语法可以参考[gin-web开发](../框架/Web开发/gin-web开发.md)中的模板语法一块内容。
# 2 Type
## 2.1 Template

Template 是已解析模板的表示形式。

```go
type Template struct {
    name       string      // 模板名称
    *parse.Tree           // 解析后的语法树
    *common               // 共享状态（如同名模板、自定义函数等）
    leftDelim  string      // 左分隔符（默认 "{{"）
    rightDelim string      // 右分隔符（默认 "}}"）
}
```
### 2.1.1 模板创建和与初始化
#### 2.1.1.1 **`Must(t *Template, err error) *Template`​**

- 作用：在程序启动阶段加载模板文件，若解析失败则直接终止程序（而非继续运行不完整的服务）

```go
// 初始化阶段加载模板，解析失败则 panic
var tpl = template.Must(template.ParseFiles("layout.html", "content.html"))

func main() {
    // 正常启动服务...
}
```


#### 2.1.1.2 **`New(name string) *Template`​**

- 作用： 创建一个新的空模板对象，用于后续解析和组合。 

```go
tpl := template.New("main") // 创建名为 "main" 的模板
```

- **注意事项​**​：
    - 模板名需唯一，避免后续查找时冲突。
    - 空模板需通过 `Parse` 或 `ParseFiles` 加载内容后才能使用。
#### 2.1.1.3 **`(t)Parse(text string) (*Template, error)`​**

- 作用：解析字符串形式的模板内容（适用于硬编码或动态生成的模板文本）。

```go
tpl, _ := template.New("demo").Parse(`Hello, {{.Name}}!`)
```

- **注意事项​**​：
    - 多次调用 `Parse` 会 ​**​追加内容到同一模板​**​，可能导致同名模板覆盖。
    - 避免在运行时频繁解析，影响性能。
#### 2.1.1.4 **`ParseFiles(filenames ...string) (*Template, error)`**

- 作用：从本地文件加载一个或多个模板文件（如 HTML 页面、子模板）。

```go
tpl, _ := template.ParseFiles("header.html", "footer.html")
```
​
- **​注意事项​**​：
    - 每个文件中的模板必须通过 `{{define}}` 命名，否则无法引用。
    - 文件路径需正确，否则返回错误。
#### 2.1.1.5 **`ParseGlob(pattern string) (*Template, error)`​**

- 作用：批量加载匹配通配符模式的所有模板文件（如 `templates/*.html`）。

```go
tpl, _ := template.ParseGlob("templates/*.html")
```

**​注意事项​**​：
- 通配符需符合操作系统规则（如 `*` 匹配任意字符）。
- 文件加载顺序不固定，避免依赖解析顺序。
### 2.1.2 模板渲染
#### 2.1.2.1 **`(t)Execute(wr io.Writer, data interface{}) error`​**
​
- 作用：渲染 ​**​默认模板​**​（即首个通过 `Parse` 或 `ParseFiles` 加载的模板）。

```go
data := struct{ Name string }{Name: "Alice"}
tpl.Execute(os.Stdout, data) // 输出到标准输出
```

**注意事项​**​：
- 若模板集合中存在多个模板，需使用 `ExecuteTemplate` 指定名称。
- 数据字段需与模板中的变量名匹配，否则渲染失败。
#### 2.1.2.2 **`(t)ExecuteTemplate(wr io.Writer, name string, data interface{}) error`**

- 作用：渲染指定名称的模板（适用于多模板组合的场景）。

```go
tpl.ExecuteTemplate(os.Stdout, "footer", data) // 渲染名为 "footer" 的模板
```

- ​**​注意事项​**​：
    - 模板名必须存在，否则返回错误。
    - 常用于组合布局模板（如先渲染 `layout.html`，再嵌入 `content.html`）。
### 2.1.3 模板管理与查询
#### 2.1.3.1 **`(t)Lookup(name string) *Template`​**​

- 作用：根据名称查找已解析的模板，用于动态检查模板是否存在。

```go
if t := tpl.Lookup("header"); t != nil {
    t.Execute(os.Stdout, data)
}
```

- **注意事项​**​：
    - 若模板不存在，返回 `nil`，需做空值判断。
    - 查找效率高，适合高频调用。
#### 2.1.3.2 **`(t)DefinedTemplates() string`​**

- 作用：列出所有已定义的模板名称（调试或日志记录）。

```go
fmt.Println(tpl.DefinedTemplates()) // 输出："; defined templates: header, footer"
```

**注意事项​**​：
- 返回的字符串格式固定，需自行解析。
- 主要用于调试，非生产逻辑。
#### 2.1.3.3 **`(t)Templates() []*Template`**

- 作用：获取所有关联的模板对象（遍历或批量操作）。

```go
for _, t := range tpl.Templates() {
    fmt.Println(t.Name())
}
```

- ​**​注意事项​**​：
    - 返回顺序不固定，可能与解析顺序不同。
    - 返回的切片为副本，修改不影响原模板集合。
### 2.1.4 **模板配置与扩展​**

#### 2.1.4.1 **`(t)Funcs(funcMap FuncMap) *Template`​**

- 作用：注册自定义函数到模板中（如格式化日期、数学运算）。

```go
funcMap := template.FuncMap{"add": func(a, b int) int { return a + b }}
tpl := template.New("demo").Funcs(funcMap)
```

- ​**​注意事项​**​：
    - 必须在调用 `Parse` 前注册，否则函数不可用。
    - 自定义函数最多返回两个值（第二个为 `error`），非 `nil` 会终止渲染。
#### 2.1.4.2 **`(t)Delims(left, right string) *Template`​**​

- 作用：修改模板动作的分隔符（默认 `{{` 和 `}}`），避免与前端框架（如 Vue）冲突。

```go
tpl := template.New("demo").Delims("[[", "]]") // 分隔符改为 [[ 和 ]]
```

- **​注意事项​**​：
    - 修改后所有动作需使用新分隔符（如 `[[.Name]]`）。
    - 确保不与模板内容中的其他文本冲突。
#### 2.1.4.3 **`(t)Option(opt ...string) *Template`**

- 作用：设置模板解析选项（如 `missingkey=zero` 或 `missingkey=error`）。

```go
tpl.Option("missingkey=zero") // 缺失字段时返回零值而非错误
```
- 支持的选项包括：
    - `missingkey=zero`：缺失字段返回零值。
    - `missingkey=error`：缺失字段返回错误（默认）。
    - `missingkey=invalid`：保留旧行为（不推荐）。
#### 2.1.4.4 **`(t)Clone() (*Template, error)`**

- 作用：克隆模板对象，用于并发渲染或避免原模板被修改。

```go
clonedTpl, _ := tpl.Clone()
clonedTpl.Execute(os.Stdout, data) // 安全并发
```

- **注意事项​**​：
    - 克隆后的模板与原模板独立，修改互不影响。
    - 深度复制可能带来性能开销，非高频场景使用。
# 3 **与 `html/template` 的区别​**​

| ​**​特性​**​   | `text/template` | `html/template` |
| ------------ | --------------- | --------------- |
| ​**​自动转义​**​ | 无（需手动处理）        | 有（根据上下文智能转义）    |
| ​**​安全防护​**​ | 不防 XSS          | 自动转义防 XSS       |
| ​**​适用场景​**​ | 生成纯文本、代码、配置文件   | 生成 HTML 网页      |
**总结**：

1. ​**​性能优化​**​：
    
    - ​**​预加载模板​**​：在服务启动时解析并缓存，避免运行时解析。
    - ​**​避免重复解析​**​：多次调用 `Parse` 会追加内容，可能导致错误。

2. ​**​错误处理​**​：
    
    - 所有解析和渲染方法返回 `error`，需显式检查。
    - 使用 `template.Must` 简化初始化，但需确保模板无误。

3. ​**​并发安全​**​：
    
    - 解析后的模板（`*Template`）是并发安全的，可在多个 goroutine 中调用 `Execute`。
    - 解析过程中（如调用 `Parse`）不保证并发安全。

4. ​**​安全规范​**​（`html/template`）：
    
    - 自动转义 HTML/JS，防止 XSS 攻击。
    - 谨慎使用 `template.HTML` 类型，确保内容可信。