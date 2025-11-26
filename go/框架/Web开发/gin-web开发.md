# 1 gin介绍
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
# 2 创建一个简单的服务

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
# 3 设置图标

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
# 4 创建路由

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
## 4.1 路由匹配规则

Gin 框架的路由匹配规则基于 **HTTP 方法**​ 和 **URL 路径**，支持静态路由、参数路由、通配符等多种模式。

|路由类型|语法示例|匹配的示例路径|说明|
|---|---|---|---|
|静态路由|`/user`|`/user`|精确匹配，只匹配路径完全相同的请求。|
|路径参数|`/user/:id`|`/user/123`|匹配一个路径段，`:id`匹配任意非空字符串（不包括斜杠）。|
|通配符路由|`/file/*filepath`|`/file/abc/def.jpg`|匹配从`/file/`开始的所有路径，包括斜杠。`*filepath`必须放在路径最后。|

Gin 按以下顺序匹配路由（**静态路径优先**）：

1. **完全匹配的静态路径**（如 `/user`）
    
2. **路径参数**（如 `/user/:id`）
    
3. **通配符**（如 `/file/*filepath`）

**注意事项**：

1. **路径斜杠**：
    
    - Gin 默认严格匹配斜杠，`/user`和 `/user/`被视为不同路径。
        
    - 可通过 `RedirectFixedPath`选项自动重定向修正斜杠。
        
    
2. **参数冲突**：
    
    - 避免重叠的路由定义（如同时定义 `/user/:id`和 `/user/name`），可能意外匹配。
        
    
3. **通配符位置**：
    
    - 通配符只能放在路径末尾，如 `/*path`有效，但 `/user/*path/invalid`无效。
# 5 参数渲染

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

# 6 获取请求参数

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
# 7 数据绑定

Gin提供了两类绑定方法：
- `Must bind`
    - Bind、BindJSON、BindXML、BindQuery、BindYAML
    - 这些方法属于`MustBindWith`的具体调用。如果发生绑定错误，则请求终止，并触发 `c.AbortWithError(http.StatusBadRequest, err).SetType(ErrorTypeBind)`
    - 响应码被设置为400并且 `Content-Type`被设置为 `text/plain；charset-utf-8`
    - 只能把响应码设置为400-422之间
-  `Should bind`
    - ShouldBind、ShouldBindJSON、ShouldBindXML、ShouldBindQuery、ShouldBindYAML
    - 这些方法都属于 `ShouldBindWith`调用。如果发生绑定错误，Gin会返回错误并由开发者处理错误和请求。
- 使用 Bind 方法时，Gin 会尝试根据 Content-Type 推断如何绑定。 如果你明确知道要绑定什么，可以使用 `MustBindWith` 或 `ShouldBindWith`。
- 你也可以指定必须绑定的字段。 如果一个字段的 tag 加上了 `binding:"required"`，但绑定时是空值, Gin 会报错。

```go
<form action="/user/add" method="post">  
    <p>用户名: <input type="text" name="username"></p>  
    <p>密码: <input type="text" name="password"></p>  
    <p>地址: <input type="text" name="addr"></p>  
    <button type="submit">提交</button>  
</form>

// 参数绑定
type Users struct {  
    Name string `form:"name" uri:"name" json:"name"`  
    Pass string `form:"password" uri:"password" json:"password"`  
    Addr string `form:"addr" uri:"addr" json:"addr"`  
}  
  
func BindHtml(context *gin.Context) {  
    context.HTML(http.StatusOK, "user/bind_form.html", "")  
}  
  
func BindForm(context *gin.Context) {  
    var users Users  
    // 绑定表单
    _ = context.ShouldBind(&users)  
    context.JSON(http.StatusOK, users)  
}  
  
func BindQuery(context *gin.Context) {  
    var users Users  
    // 绑定查询参数  
    // http://127.0.0.1:8080/bindquery?name=123&age=18&addr=asdasd  
    context.ShouldBindQuery(&users)  
    context.JSON(http.StatusOK, users)  
}  
  
func BindUri(context *gin.Context) {  
    var users Users  
    // http://127.0.0.1:8080/binduri/123/123/123  
    context.ShouldBindUri(&users)  
    context.JSON(http.StatusOK, users)  
}

// 绑定 JSON
type Login struct {
	User     string `form:"user" json:"user" xml:"user"  binding:"required"`
	Password string `form:"password" json:"password" xml:"password" binding:"required"`
}

func main() {
	router := gin.Default()

	// 绑定 JSON ({"user": "manu", "password": "123"})
	router.POST("/loginJSON", func(c *gin.Context) {
		var json Login
		if err := c.ShouldBindJSON(&json); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		
		if json.User != "manu" || json.Password != "123" {
			c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
			return
		} 
		
		c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
	})

	// 绑定 XML (
	//	<?xml version="1.0" encoding="UTF-8"?>
	//	<root>
	//		<user>manu</user>
	//		<password>123</password>
	//	</root>)
	router.POST("/loginXML", func(c *gin.Context) {
		var xml Login
		if err := c.ShouldBindXML(&xml); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		
		if xml.User != "manu" || xml.Password != "123" {
			c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
			return
		} 
		
		c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
	})

	// 监听并在 0.0.0.0:8080 上启动服务
	router.Run(":8080")
}

/*
$ curl -v -X POST \
  http://localhost:8080/loginJSON \
  -H 'content-type: application/json' \
  -d '{ "user": "manu" }'
*/
```
## 7.1 数据验证

Gin使用 [**go-playground/validator/v10**](https://github.com/go-playground/validator) 进行验证。 查看标签用法的全部[文档](https://pkg.go.dev/github.com/go-playground/validator/v10#hdr-Baked_In_Validators_and_Tags).
不满足校验会报错：`Error:Field validation for 'Desc' failed on the 'required' tag`

如果有多个验证字段，按顺序进行验证，如果前面验证不通过不会对后面的进行验证：
- - ：忽略字段
- required：不为空校验，binding:"required"
- regexp：正则表达式校验
- min：最小长度，binding:"min=1"
- max：最大长度
- |：或
- structonly：如果有嵌套可以决定只验证结构体上的
- Exists
- omitempty：省略空，如果为空，则不会继续校验该字段其他的规则，只有不为空才会继续验证其他的
- dive：嵌套验证
```go
Name [][]int `binding:"min=10,dive,max=20,deive required"`
// min=10针对第一个[]
// max=20针对第二个[]
// required针对Name
```
- len：长度
- eq/ne/gte/ge/lt/lte：gt、gte、lt、lte等都可以用于时间的比较，后面可以不跟值，表示大于当前utc时间
- eqfield：等于其他字段的值
- nefield：不等于其他字段的值
- eqcsfield：类似eqfield，它会验证相对于顶层结构提供的字段
```go
eqcsfield = InnerStructField.Fiedl
```
- nqcsfield
- gtfield：大于其他字段的值
- gtefield
- gtcsfield
- gtecsfield
- alpha：字符串仅包含字母字符
- alphanum：仅包含字母数字字符
- numeric：字符串包含基本数字值。不包含指数等
- hexadecimal：字符串包含有效的十六进程
- hexcolor：字符串值包含有效的十六进程颜色，包括#
- rgb：包含有效的rgb颜色
- rgba
- email：包含有效的电子邮件
- url：包含有效的网址，必须包含http://等
- uri：包含有效的uri。将接受golang请求uri接受的任何uri
- contains：包含子字符串
- excludes：排除
- uuid
- ip
## 7.2 自定义验证器

1. 安装包
```go
go   get github.com/go-playground/validator/v10
```
2. 定义验证器
```go
// 必须是validator.Func 类型  
var Len6Valid validator.Func = func(fl validator.FieldLevel) bool {  
    data := fl.Field().Interface().(string)  
    if len(data) > 6 {  
       fmt.Println("false")  
       return false  
    } else {  
       fmt.Println("true")  
       return true  
    }  
}
```
3. 注册验证器
```go
// 在路由匹配前，main中即可  
if v, ok := binding.Validator.Engine().(*validator.Validate); ok {  
    v.RegisterValidation("len_valid", user.Len6Valid)  
}
```
4. 使用验证器
```go
type Article struct {  
    Id      int    `form:"Id" binding:"required"`  
    Title   string `form:"title" binding:"required,len_valid"`  
    Content string `form:"content" binding:"required"`  
    Desc    string `form:"desc" binding:"required"`  
}
```
## 7.3 beego验证器

1. 下载包
```go
go get github.com/astaxie/beego/validation
```
2. 常用验证器
![](gin-web开发_time_1.png)
3. 使用
```go
/*
- 验证函数写在"valid"tag标签里
- 各个验证规则使用；分割
- 参数使用括号包裹，多个参数使用，分割
- 正则函数匹配模式用//括起来
- 各个函数的key值为字段名.验证函数名
*/
type Article struct {  
    Id      int    `valid:"Required"`  
}
// 初始化验证器
var article Article
valid := validation.Validation{}
b,err := valid.Valid(&article) // ->bool,err
if !b{
    for _,err1 := range valid.Errors{
        fmt.Println(err1.Key)
        fmt.Println(err1.Message)
    }
}
```
4. 自定义错误信息
    1. #TODO:如何使用beego自定义验证器
```go
var MessageTmpls = map[string]string{  
    "Required":     "Can not be empty",  
    "Min":          "Minimum is %d",  
    "Max":          "Maximum is %d",  
    "Range":        "Range is %d to %d",
    }
validation.SetDefaultMessage(MessageTmpls)
```
# 8 文件上传

```go
  
// 方式一：表单单文件  
/*  
curl -X POST http://localhost:8080/upload \  
  -F "file=@/Users/appleboy/test.zip" \  -H "Content-Type: multipart/form-data"*/  
func FormSingleFile(context *gin.Context) {  
    file, _ := context.FormFile("file")  
    log.Println(file.Filename)  
  
    // 这个路径是从项目根目录开始  
    // 会自动创建目录  
    dst := "./files/" + file.Filename  
    // 上传文件至指定的完整文件路径  
    // 会覆盖同名文件  
    context.SaveUploadedFile(file, dst)  
  
    context.String(http.StatusOK, fmt.Sprintf("'%s' uploaded!", file.Filename))  
}  
  
// 方式二：表单多文件  
/*  
curl -X POST http://localhost:8080/upload \  
  -F "upload[]=@/Users/appleboy/test1.zip" \  -F "upload[]=@/Users/appleboy/test2.zip" \  -H "Content-Type: multipart/form-data"*/  
func FormManyFile(context *gin.Context) {  
    file, _ := context.MultipartForm()  
    files := file.File["file"]  
  
    dst := "./files/"  
    for _, f := range files {  
       log.Println(f.Filename)  
       context.SaveUploadedFile(f, dst+f.Filename)  
    }  
    context.String(http.StatusOK, fmt.Sprintf("%d files uploaded!", len(files)))  
}
```
# 9 响应数据类型

```go
func OutJson(context *gin.Context) {  
    context.JSON(http.StatusOK, gin.H{  
       "code": 200,  
       "tag":  "<br>",  
       "msg":  "提交成功",  
       "html": "<b>Hello,world!</b>",  
    })  
}  
  
// 生成具有转义的非ASCLL字符的ASCLL-only JSON  
func OutAscJson(context *gin.Context) {  
    context.AsciiJSON(http.StatusOK, gin.H{  
       "code": 200,  
       "tag":  "<br>",  
       "msg":  "提交成功",  
       "html": "<b>Hello,world!</b>",  
    })  
}  
  
// 使用JSONP向不同域的服务器请求数据。如果查询参数存在回调，则将回调添加到响应体中  
func OutJsonp(context *gin.Context) {  
    context.JSONP(http.StatusOK, gin.H{  
       "code": 200,  
       "tag":  "<br>",  
       "msg":  "提交成功",  
       "html": "<b>Hello,world!</b>",  
    })  
}  
  
/*  
c.JSON()：默认会转义 HTML 敏感字符，以确保安全性。  
c.PureJSON()：直接输出原始字符，保持 JSON 数据的原貌。  
*/  
func OutPureJson(context *gin.Context) {  
    context.PureJSON(http.StatusOK, gin.H{  
       "code": 200,  
       "tag":  "<br>",  
       "msg":  "提交成功",  
       "html": "<b>Hello,world!</b>",  
    })  
}  
  
// 使用SecureJSON防止json劫持。如果给定的结构是数组值，则默认预置“while(1)”到响应体  
// json劫持：利用网站的cookie未过期，如何访问攻击者的虚假页面，该页面就可以拿到json形式的用户敏感信息  
func OutSecureJson(context *gin.Context) {  
    context.SecureJSON(http.StatusOK, gin.H{  
       "code": 200,  
       "tag":  "<br>",  
       "msg":  "提交成功",  
       "html": "<b>Hello,world!</b>",  
    })  
}  
  
func OutXml(context *gin.Context) {  
    context.XML(http.StatusOK, gin.H{  
       "code": 200,  
       "tag":  "<br>",  
       "msg":  "提交成功",  
       "html": "<b>Hello,world!</b>",  
    })  
}  
  
func OutYaml(context *gin.Context) {  
    context.YAML(http.StatusOK, gin.H{  
       "code": 200,  
       "tag":  "<br>",  
       "msg":  "提交成功",  
       "html": "<b>Hello,world!</b>",  
    })  
}
```
# 10 路由组

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
	yes.GET("/1", myHandler(), func(context *gin.Context) {
		handler := context.MustGet("Handler").(string)
		context.JSON(http.StatusOK, gin.H{
			"子路由组":    "/user/yes/1",
			"handler": handler,
		})
	})
```
# 11 中间件

- 什么是中间件
    - 开发者自定义的钩子函数
- 中间件的作用
    - 中间件适合处理一些公共的业务逻辑，比如登陆认证、权限校验、数据分页、记录日志、耗时统计等
    - 需要对某一类的函数进行通用的前置或后置处理
- 中间件的回调要先于用户定义的路由处理函数
- Use是追加中间件，会按照顺序调用中间件
- 常用中间件
![](gin-web开发_time_2.png)
## 11.1 自定义中间件
```go
  
// 自定义中间件第一种方式
func MyHandler() gin.HandlerFunc {  
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

// 自定义中间件第二种方式
func MiddleWarel(context *gin.Context) {  
    fmt.Println("这是中间件定义的第二种方式")  
}

func main(){
    h := gin.New()

    // 注册自定义中间件
    // 如果在路由组之后再使用中间件，会对前面的路由组无效
	h.Use(MyHandler())

	h.GET("/test", func(context *gin.Context) {
		context.String(200, "yes")
	})

	// 运行
	h.Run()
}
```
## 11.2 Next和Abort

 - Next
     - 在定义的众多中间件会形成一条中间件链，而通过Next函数来对后面的中间件进行执行
     - 当遇到c.Netx()函数时，它取出所有的没有被执行过的注册函数都执行一边，然后再回到本函数中
     - Next函数是在请求前执行，而Next函数后是在请求后执行
         - **`c.Next()` 之前的代码会在请求处理前（Pre-Request）​** 执行。
        - ​**`c.Next()` 之后的代码会在请求处理后（Post-Request）​** 执行（即响应已生成，但尚未发送给客户端）。
     - 可以用在token校验，把用户id存起来给功能性函数使用
 - Abort
     - 终止调用整个链条,但只是不会调用此函数所有中间件的后面中间件，本中间件和之前的中间件会调用完毕
     - 比如token认证没有通过，不能直接使用return返回，而是使用Abort来终止
```go
func MiddleWare1(context *gin.Context) {  
    fmt.Println("中间件一开始")  
    context.Next()  
    fmt.Println("中间件一结束")  
}  
  
func MiddleWare2() gin.HandlerFunc {  
    return func(context *gin.Context) {  
       fmt.Println("中间件二开始")  
       context.Next()  
       fmt.Println("中间件二结束")  
    }  
}

/*
中间件一开始
中间件二开始
中间件二结束
中间件一结束
*/
```
## 11.3 利用Next计算请求时间

```go
func MiddleWare1(context *gin.Context) {  
    start_time := time.Now()  
  
    fmt.Println("中间件一开始")  
    context.Next()  
  
    fmt.Println(time.Since(start_time))  
    fmt.Println("中间件一结束")  
}  
  
func MiddleWare2() gin.HandlerFunc {  
    return func(context *gin.Context) {  
       fmt.Println("中间件二开始")  
       time.Sleep(time.Second * 3)  
       fmt.Println("中间件二结束")  
    }  
}  
func MiddleWare3(context *gin.Context) {  
    fmt.Println("中间件三开始")  
    context.Next()  
    time.Sleep(time.Second * 3)  
    fmt.Println("中间件三结束")  
}
// 请注意设置的HTTP超时时间
```
## 11.4 中间件作用域

- 全局中间件：直接在创建出来的路由引擎中使用
```go
router := gin.Default()  
  
router.Use(middle.MiddleWare1, middle.MiddleWare2(), middle.MiddleWare3)
```

- 路由组中间件：在创建出来的路由组直接使用，该路由组下的所有路由都将使用该中间件
```go
userGroup := r.Group("/user")
userGroup.Use(middle.MiddleWare1, middle.MiddleWare2(), middle.MiddleWare3)
```

- 局部中间件：直接在路由上使用
```go
yes.GET("/1", myHandler(), func(context *gin.Context) {
		handler := context.MustGet("Handler").(string)
		context.JSON(http.StatusOK, gin.H{
			"子路由组":    "/user/yes/1",
			"handler": handler,
		})
	})
```
## 11.5 gin.BasicAuth()中间件

```go
router.Use(gin.BasicAuth(gin.Accounts{  
    "zs": "123",  
}))
```
## 11.6 WrapH和WrapF

```go
func WrapFTest(w http.ResponseWriter, r *http.Request) {  
  
}
router.GET("/middle", gin.WrapF(middle.WrapFTest), middle.MiddleAuth)

/*
WrapH和WrapF区别：
- 需要自己去定义struct实现这个Handler接口
*/
type Test struct {  
}  
  
func (test *Test) TestH(w http.ResponseWriter,r *http.Request){  
      
} 
```
# 12 模板语法

**统一使用{{和}}作为左右标签，在该左右标签中的内容会被解析为Go代码逻辑（如变量、条件、循环等），在左右标签之外的内容原样输出。**

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
## 12.1 上下文

- `.`：访问当前位置的上下文
- `$`：引用当前模板根级的上下文
- `$.`：引用模板中的根级上下文
## 12.2 去除空格

- `{{-` ：去除前空格
- `-}}`：去除后空格

## 12.3 支持go语言的符号

1. 字符串：{{"zhaoli"}}
2. 原始字符串：{{\`yes\`}}
3. 字节类型：{{'a'}} ->97字符编码号
4. nil类型：{{print nil}}
    - {{nil}}只有nil会报错：nil is not a command
## 12.4 定义变量

1. 定义：
```go
{{$username := "xxxx"}}
```
2. 使用
```go
{{$username}}
```
**注意：只能在当前模板使用**
## 12.5 pipline

可以是上下文的变量输出，也可以是函数通过管道传递的返回值
- {{.Name}}是上下文的变量输出，是个pipline
- {{"h"|len}}是函数通过管道传递的返回值，是个pipline
## 12.6 流程控制-if

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
## 12.7 循环range

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
## 12.8 with

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
## 12.9 template

- 作用：导入其他的模板

```go
{{/*调用子结构传递参数*/}}
{{template "user/base.html" .}}
```

- 导入的模板文件也要使用define包含
- 如果想在引用的模板中获取动态数据，必须使用.访问当前位置的上下文
- 引入的作用位置跟 `template`使用的位置有关
## 12.10 模板函数

- `print`
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

- `and`：只要有一个为空，则整体为空，如果都不为空，则返回最后一个
```go
{{and .arr $.name}}
```

- `or`：只要有有一个不为空，则返回第一个不为空的，否则返回空

- `call`：是一个**动态调用其他函数或方法**的工具，主要用于在模板中灵活执行传入的函数或方法。
```go
{{$funcname := .funcname }}  
{{ call $funcname "yes" 2}}
```

- `index`：读取指定类型对于下标的值
    - 支持map/array/slice/string
```go
{{index .arr 1}}
```

- `len`：返回指定类型的长度
```go
{{len .arr}}
```

- `not`：返回输入参数的否定值，布尔类型

- `urlquery`： 有些符号在URL中是不能直接传递的，如果要在URL中传递这些特殊符号，那么就要使用该符号的编码
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

- `Format`：实现时间的格式化，返回字符串。也可以在后端转换在前端使用。
    - {{.time_data.Format "2006/01/02 15:04:05"}}

- `html`：转义文本中的html标签

- `js`：返回用JavaScript的escape处理后的文本
    - escape函数可以对字符串进行编码，这样就可以在所有的计算机上读取该字符串，可以使用unescape解码

- `slice`：对string/slice/array进行切片
```go
{{ slice "hello" 1 3 }} → "el"
{{ slice .Items 0 2 }}  → 获取列表前两项
```

- 
### 12.10.1 自定义模板函数

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
# 13 日志

## 13.1 基于gin的日志中间件

- 使用日志文件

```go
// 创建日志文件  
f, _ := os.Create("gin.log")  
  
// 重新赋值DefaultWriter  
gin.DefaultWriter = io.MultiWriter(f)  
  
// 同时在控制台打印信息  
gin.DefaultWriter = io.MultiWriter(f, os.Stdout)
```
## 13.2 logrus
#TODO:logrus

- 下载包
```go
go get github.com/sirupsen/logrus
```

- 定义logrus配置文件
```json
{  
  "log_dir": "logs/gin_project.log",  
  "log_level": "info"  
}
```

- 设置logrus
```go
type Conf struct {  
    LogDir   string `json:"log_dir"`  
    LogLevel string `json:"log_level"`  
}  
  
func Load_conf() *Conf {  
    var config = new(Conf)  
    f, _ := os.Open("conf/log_conf.json")  
    defer f.Close()  
    conf, _ := io.ReadAll(f)  
    json.Unmarshal(conf, config)  
    fmt.Println(config)  
    return config  
}

// 创建一个日志实例  
var Log = logrus.New()  
  
func init() {  
    logConf := Load_conf()  
  
    // 设置日志输出文件  
    f, err := os.OpenFile(logConf.LogDir, os.O_APPEND|os.O_WRONLY, os.ModeAppend)  
    if err != nil {  
       panic(err)  
    }  
  
    Log.Out = f  
  
    // 设置日志级别  
    level_map := map[string]logrus.Level{  
       "error": logrus.ErrorLevel,  
       "info":  logrus.InfoLevel,  
       "debug": logrus.DebugLevel,  
    }  
  
    Log.SetLevel(level_map[logConf.LogLevel])  
  
    // 日志格式化  
    // JSONFormatter  
    Log.SetFormatter(&logrus.TextFormatter{})  
}
```

- logrus使用
```go
r.GET("/json", func(context *gin.Context) {  
    // 返回一个JSON数据  
    f := logrus.Fields{  
       "name": "k",  
       "age":  12,  
    }  
    // WithFields在日志输出中增加字段
    logs_source.Log.WithFields(f).Info("这是info级别")  
    context.JSON(http.StatusOK, gin.H{"JSON": "YES"})  
})

/*
time="2025-03-20T19:57:07+08:00" level=info msg="这是info级别"  
time="2025-03-20T20:07:03+08:00" level=info msg="这是info级别" age=12 name=k
*/
```
# 14 cookie和session

- 什么是session
    - Session是在无状态的http协议下，服务端记录用户状态时用于标识具体用户的机制
    - 它是在服务端保存的用来跟踪用户状态的数据结构，可以保存在文件、数据库或者集群中
    - 在浏览器关闭后这次的Session就消失了，下次打开就不再拥有这个Session。其实并不是Session消失了，而是Session ID变了。

- 什么是Cookie
    - Cookie是客户端保存用户信息的一种机制，用来记录用户的一些信息
    - 每次HTTP请求时，客户端都会发送相应的Cookie信息到服务端。它的过期时间可以任意设置，如果不主动清除它，很长一段时间都可以保留

- session和cookie
    - Cookie在客户端，Session在服务器端
    - Cookie安全性一般，他人可以通过分析存放在本地的Cookie并进行Cookie欺骗。在安全性第一的前提下，选择Session更优。重要的交互信息比如权限等放在Session中，一般的信息记录放在Cookie
    - 单个Cookie保存的数据不能超过4K，很多浏览器都限制一个站点最多保存20个Cookie
    - Session可以放在文件、数据库或内存中
    - 用户验证这种场合一般会用到Session。因此维持一个会话的核心就是客户端的唯一标识，即Session ID
    - Session的运行依赖Session ID，而Session ID是存在Cookie中的，也就是说，如果浏览器禁用了Cookie，Session也会失效（但是可以通过其他方式实现，比如在url中传递SessionID）
## 14.1 使用Session和Cookie
#TODO ：怎么发送session并认证
- 下载包
```go
go get github.com/gin-contrib/sessions
```

- 基于Cookie存储引擎使用
```go
// 加密的盐  
store := cookie.NewStore([]byte("kelly"))  
  
// 使用session中间件  
r.Use(sessions.Sessions("gin_session", store))

r.GET("/json", func(context *gin.Context) {  
  
    // 初始化session对象  
    session := sessions.Default(context)  
  
    // 设置session  
    session.Set("name", "kelly")  
  
    // 获取session  
    name := session.Get("name")  
    fmt.Println("==========_____++++++++")  
    fmt.Println(name) // kelly  
  
    // 删除指定session  
    session.Delete("name")  
  
    // 清除所有的session  
    session.Clear()  
  
    // 保存session  
    session.Save()  
  
    // 返回一个JSON数据  
    context.JSON(http.StatusOK, gin.H{"JSON": "YES"})  
})
```

- 基于redis存储引擎
```go
// 下载
go get github.com/gin-contrib/sessions/redis

//参数从左到右依次为：redis最大空闲连接数，通信协议，redis地址，redis密码，加密密钥  
store, err := redis.NewStore(10, "tcp", "localhost:6379", "", []byte("secret"))  
fmt.Println(err)  
r.Use(sessions.Sessions("session_test", store))
```
