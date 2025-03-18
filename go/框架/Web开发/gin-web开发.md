# 1. gin介绍
Gin 是一个用 Golang编写的 高性能的web 框架, 由于http路由的优化，速度提高了近 40 倍。 Gin的特点就是封装优雅、API友好。

Gin的一些特性：

- 快速  
    基于 Radix 树的路由，小内存占用。没有反射。可预测的 API 性能。
- 支持中间件  
    传入的 HTTP 请求可以由一系列中间件和最终操作来处理。 例如：Logger，Authorization，GZIP，最终操作 DB。
- Crash 处理  
    Gin 可以 catch 一个发生在 HTTP 请求中的 panic 并 recover 它。这样，你的服务器将始终可用。例如，你可以向 Sentry 报告这个 panic！
- JSON 验证  
    Gin 可以解析并验证请求的 JSON，例如检查所需值的存在。
- 路由组  
    更好地组织路由。是否需要授权，不同的 API 版本…… 此外，这些组可以无限制地嵌套而不会降低性能。
- 错误管理  
    Gin 提供了一种方便的方法来收集 HTTP 请求期间发生的所有错误。最终，中间件可以将它们写入日志文件，数据库并通过网络发送。
- 内置渲染  
    Gin 为 JSON，XML 和 HTML 渲染提供了易于使用的 API。
- 可扩展性  
    新建一个中间件非常简单。

安装十分简单：
```go
go get -u github.com/gin-gonic/gin
```
# 2. 创建一个简单的服务

```go
package main
// 导入gin包
import "github.com/gin-gonic/gin"

// 入口函数
func main() {
    // 初始化一个http服务对象
    // 默认使用Logger and Recovery中间件
	r := gin.Default()
        
    // 设置一个get请求的路由，url为/ping, 处理函数（或者叫控制器函数）是一个闭包函数。
	r.GET("/ping", func(c *gin.Context) {
    	// 通过请求上下文对象Context, 直接往客户端返回一个json
    	// type H map[string]any
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})

    // 不写具体address默认在0.0.0.0:8080启动
	r.Run(":8080") // 监听并在 0.0.0.0:8080 上启动服务
}
```
# 3. 设置图标

```go
import "github.com/thinkerou/favicon"
/*
Use函数是 Gin 框架中用于注册中间件的方法。依次按照顺序执行
  
func (engine *Engine) Use(middleware ...HandlerFunc) IRoutes {  
    engine.RouterGroup.Use(middleware...)  
    engine.rebuild404Handlers()  
    engine.rebuild405Handlers()  
    return engine  
}

favicon.New是一个用于处理favicon请求的中间件,返回指定的图标

func New(path string) gin.HandlerFunc

*/ 
r.Use(favicon.New("./favicon/18.ico"))
```
# 4. 创建路由

```go
/*
目录结构
gin/
    static/
        css/
        js/
    template/
*/

    // 创建服务
	r := gin.Default()
	// 设置图标
	r.Use(favicon.New("./favicon/18.ico"))

	// 加载静态页面
	r.LoadHTMLGlob("template/*")
	/* 
	加载资源文件
    func (group *RouterGroup) Static(relativePath, root string) IRoutes
    将relativePath路径映射到文件系统中的root中
	*/
	r.Static("/static", "./static")

	// 创建一个请求
	r.GET("/json", func(context *gin.Context) {
		// 返回一个JSON数据
		context.JSON(http.StatusOK, gin.H{"JSON": "YES"})
		// 返回字符串
		context.String(http.StatusOK, "pong")
	})

	r.GET("/html", func(context *gin.Context) {
    	/* 
    	HTML方法可以把参数传递给前端

        只需要在前端写下：
        	获取后端的数据为：  
            {{.msg}}
    	*/
		context.HTML(http.StatusOK, "index.html", gin.H{
			"msg": "前端传参测试",
		})
	})

    // 重定向，如果地址不加http/https的话会在路由后面追加路径
    r.GET("/redirect", func(context *gin.Context) {
		context.Redirect(302, "http://www.baidu.com/")
	})

    // 404
    // func (engine *Engine) NoRoute(handlers ...HandlerFunc)
    // `NoRoute` 方法用于定义处理未匹配路由的处理器。当客户端请求的路径没有匹配到任何已定义的路由时，Gin 会调用 `NoRoute` 方法中定义的处理器。默认情况下，Gin 会返回一个 404 状态码。
	r.NoRoute(func(context *gin.Context) {
		context.HTML(http.StatusNotFound, "404.html", "")
	})
```

# 参数渲染

在后端中可以给前端传递各种类型的参数

```go
// string渲染
func RenderStr(context *gin.Context) {
	context.HTML(http.StatusOK, "user/user.html", "user string")
}

/*
stuct渲染：
type H map[string]any
使用gin.H{}是一样的使用方法
*/
func RenderStruct(context *gin.Context) {
	userinfo := UserInfo{UserID: 1, UserName: "ky"}
	context.HTML(http.StatusOK, "user/struct.html", userinfo)
}

// 数组渲染
func RenderArray(context *gin.Context) {
	userarr := []int{1, 2, 3}
	context.HTML(http.StatusOK, "user/array.html", userarr)
}


// 前端文件
<!-- 字符串渲染 -->  
<H1>{{.}}</H1>

<!-- 结构体渲染 --> 
<h1>UserID:{{.UserID}}</h1>  
<h1>UserName:{{.UserName}}</h1>

<!-- 数组渲染 --> 
{{/*第一种方式*/}}  
{{range $i,$v := .}}  
  {{$i}}  
  {{$v}}  
<br>  
{{end}}  
  
<br>  
{{/*第二种方式*/}}  
{{range .}}  
    {{.}}  
{{end}}
```

# 5. 获取请求参数

```go
    // usl?userid=ks&username=k
    /*
        context.DefaultQuery("id","123")  

        ?id=1,2,3
        context.QueryArray("id")

        ?name[1]=ha&name[2]=he
        context.QueryMap("name") map[1:ha 2:he]
    */
	r.GET("/user/info", func(context *gin.Context) {
		uid := context.Query("userid")
		username := context.Query("username")
		context.JSON(http.StatusOK, gin.H{
			"uid":      uid,
			"username": username,
		})
	})

	//  /user/info/ks/k
	// 占位符可以使用*，这样可以在不完全匹配情况下请求到该路由
	r.GET("/users/info/:userid/:username", func(context *gin.Context) {
		userid := context.Param("userid")
		username := context.Param("username")
		context.JSON(http.StatusOK, gin.H{
			"uid":      userid,
			"username": username,
		})
	})

	// 前端给后端传递json
	r.POST("/post", func(context *gin.Context) {
		// request.body
		// func (c *Context) GetRawData() ([]byte, error)
		b, _ := context.GetRawData()
		var m map[string]interface{}
		
		// func Unmarshal(data []byte, v interface{}) error
		// 将 JSON 数据解码（反序列化）为 Go 数据结构
		_ = json.Unmarshal(b, &m)
		context.JSON(http.StatusOK, m)
	})

	// 处理表单
	/*
	context.DefaultPostForm("age","18")  
    context.PostFormArray("name")  // 多选框返回列表
    context.PostFormMap("password") // input name属性写成map形式即可
	*/
	/*
    <form action="/user/add" method="post">  
        <p>username: <input type="text" name="username"></p>  
        <p>userword1: <input type="text" name="password[1]"></p>  
        <p>userword2: <input type="text" name="password[2]"></p>  
        <button type="submit">提交</button>  
    </form>
	*/
	r.POST("/user/add", func(context *gin.Context) {
		username := context.PostForm("username")
		context.JSON(http.StatusOK, gin.H{
			"username": username,
		})
	})
```
# 参数绑定

```go
<form action="/user/add" method="post">  
    <p>用户名: <input type="text" name="username"></p>  
    <p>密码: <input type="text" name="password"></p>  
    <p>地址: <input type="text" name="addr"></p>  
    <button type="submit">提交</button>  
</form>

// 参数绑定
type User struct {
	// 参数绑定需要结构体名和表单控件名一致，不一致可以使用form/json结构体标签进行绑定
	// json:"username
	Username string `form:"username"`
	Password int    `form:"password"`
	Addr     string `form:"addr"`
}

func UserAdd(context *gin.Context) {
	context.HTML(http.StatusOK, "user/user_add.html", "")
}

func UserToAdd(context *gin.Context) {
	var user User
	// 将参数绑定到结构体
	err := context.ShouldBind(&user)
	fmt.Println(err)
	fmt.Println(user)
	context.String(http.StatusOK, "user")
}
```
# 6. 路由组

```go
    // 路由组
    //func (group *RouterGroup) Group(relativePath string, handlers ...HandlerFunc) *RouterGroup
    // 第一层路由/user，可以在路由组中指定中间件，这样路由组中的所有路由都会使用这个中间件
	userGroup := r.Group("/user")
	{
    	// 第二层路由/user/add
		userGroup.GET("/add")
	}
	// 子路由组/user/yes
	yes := userGroup.Group("/yes")
	yes.GET("1", myHandler(), func(context *gin.Context) {
		handler := context.MustGet("Handler").(string)
		context.JSON(http.StatusOK, gin.H{
			"子路由组":    "/user/yes/1",
			"handler": handler,
		})
	})
```
# 7. 自定义中间件

```go
  
// 自定义中间件  
func myHandler() gin.HandlerFunc {  
    return func(context *gin.Context) {  
       // 后续所有处理都能拿到这里的参数  
       // 设置上下文中的键值对
       context.Set("Handler", "myHandler")  

       //  MustGet用于从上下文中获取存储的键值对
       // func (c *Context) MustGet(key string) interface{}
       if context.MustGet("Handler").(string) == "myHandlers" {  
          context.Next() // 放行  
       } else {  
          context.Abort() // 阻止  
       }  
    }  
}


func main(){
    h := gin.New()

    // 注册自定义中间件
	h.Use(myHandler())

	h.GET("/test", func(context *gin.Context) {
		context.String(200, "yes")
	})

	// 运行
	h.Run()
}
```
# 模板语法

**统一使用{{和}}作为左右标签**
```go
// 后端给前端传递的数据
func UserTemplate(contest *gin.Context) {  
  
    arr := []int{1, 2, 3, 4}  
    maps := map[string]interface{}{  
       "one":   "one",  
       "tow":   "2",  
       "three": 3,  
    }  
    names := Person{  
       Name: "k",  
       Age:  18,  
       Addr: "beijin",  
    }  
  
    contest.HTML(http.StatusOK, "user/user_template.html", gin.H{  
       "string": "string message",  
       "arr":    arr,  
       "map":    maps,  
       "struct": names,  
       "funcname": SubStr,
    })  
}

func SubStr(str string, l int) string {  
    ret := str[0:l]  
    return (ret + "...")  
}
```
## 上下文

- `.`：访问当前位置的上下文
- `$`：引用当前模板根级的上下文
- `$.`：引用模板中的根级上下文
## 去除空格

- `{{-` ：去除前空格
- `-}}`：去除后空格

## 支持go语言的符号

1. 字符串：{{"zhaoli"}}
2. 原始字符串：{{\`yes\`}}
3. 字节类型：{{'a'}} ->97字符编码号
4. nil类型：{{print nil}}
    - {{nil}}只有nil会报错：nil is not a command
## 定义变量

1. 定义：
```go
{{$username := "xxxx"}}
```
2. 使用
```go
{{$username}}
```
**注意：只能在当前模板使用**
## pipline

可以是上下文的变量输出，也可以是函数通过管道传递的返回值
- {{.Name}}是上下文的变量输出，是个pipline
- {{"h"|len}}是函数通过管道传递的返回值，是个pipline
## 流程控制-if

1. if...else...
```go
{{ if .string1 }}  
    {{.string}}  
{{ else }}  
    {{ print "else" }}  
{{end}}
```
2. if嵌套
```go
{{ if .string1 }}  
    {{.string}}  
{{ else if .string1 }}  
    {{ print "no" }}  
{{ else }}  
    {{ print "else" }}  
{{end}}
```
## 循环range

```go
{{ range.map }}  
    {{.}} 
    <br>  
{{end}}

{{ range $v := .map }}   
    {{$v}}  
    <br>  
{{end}}

{{ range $i,$v := .map }}  
    {{$i}}  
    {{$v}}  
    <br>  
{{end}}

// 支持else，长度为0的时候执行else
{{ range $i,$v := .map1 }}  
    {{$i}}  
    {{$v}}  
    <br>  
{{else}}  
    {{ 0 }}  
{{end}}
```
## with伴随

- 作用：**用于重定向pipline**
```go
// 不用每个字段前都加struct了
{{with .struct}}  
    {{.Name}}  
    {{.Age}}  
    {{.Addr}}  
{{else}} // 逻辑跟range一样
    {{0}}
{{end}}
```
## template

- 作用：导入其他的模板

```go
{{/*调用子模板并传递参数*/}}
{{template "user/base.html" .}}
```

- 导入的模板文件也要使用define包含
- 如果想在引用的模板中获取动态数据，必须使用.访问当前位置的上下文
- 引入的作用位置跟 `template`使用的位置有关
## 模板函数

- print
    - print：fmt.Sprint
    - printf：fmt.Sprintf
    - println：fmt.Sprintln

|格  式|描  述|
|---|---|
|%v|按值的本来值输出|
|%+v|在 %v 基础上，对结构体字段名和值进行展开|
|%#v|输出 Go 语言语法格式的值|
|%T|输出 Go 语言语法格式的类型和值|
|\%\%|输出 % 本体|
|%b|整型以二进制方式显示|
|%o|整型以八进制方式显示|
|%d|整型以十进制方式显示|
|%x|整型以十六进制方式显示|
|%X|整型以十六进制、字母大写方式显示|
|%U|Unicode 字符|
|%f|浮点数|
|%p|指针，十六进制方式显示|
```go
{{print "hello" "world"}}  
{{printf "name:%s name:%s" "k" "s"}}
```

- 括号：设置优先级
```go
{{printf "name:%s name:%s" "k" (printf "%s-%s" "1" "2")}}
```

- and：只要有一个为空，则整体为空，如果都不为空，则返回最后一个
```go
{{and .arr $.name}}
```

- or：只要有有一个不为空，则返回第一个不为空的，否则返回空

- call：是一个**动态调用其他函数或方法**的工具，主要用于在模板中灵活执行传入的函数或方法。
```go
{{$funcname := .funcname }}  
{{ call $funcname "yes" 2}}
```

- index：读取指定类型对于下标的值
    - 支持map/array/slice/string
```go
{{index .arr 1}}
```

- len：返回指定类型的长度
```go
{{len .arr}}
```

- not：返回输入参数的否定值，布尔类型

- urlquery： 有些符号在URL中是不能直接传递的，如果要在URL中传递这些特殊符号，那么就要使用该符号的编码
```go
{{urlquery "http://www.baidu.com"}}
{{/*
http%3A%2F%2Fwww.baidu.com
%后面的就是自负的16进制字符码
*/}}
 
```

- 判断符，返回布尔值
    - eq：等于,可以用于字符串判断
        - 支持多个参数，只要有一个与第一个值相等就返回true
    - ne：不等于
    - lt：大于
    - le：大于等于
    - gt：小于
    - ge：小于等于

- Format：实现时间的格式化，返回字符串。也可以在后端转换在前端使用。
    - {{.time_data.Format "2006/01/02 15:04:05"}}

- html：转义文本中的html标签

- js：返回用JavaScript的escape处理后的文本
    - escape函数可以对字符串进行编码，这样就可以在所有的计算机上读取该字符串，可以使用unescape解码
### 自定义模板函数

1. 定义函数
```go
func SubStr(str string, l int) string {  
    ret := str[0:l]  
    return (ret + "...")  
}
```
2. 注册函数：注册函数要在控制器加载静态文件之前
```go
router.SetFuncMap(template.FuncMap{  
    "SubStr": user.SubStr, // 字符串为前端使用的名称  
})
```
3. 使用函数
```go
{{SubStr "yes" 2}}
```