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
# 5. 获取请求参数

```go
    // usl?userid=ks&username=k
	r.GET("/user/info", func(context *gin.Context) {
		uid := context.Query("userid")
		username := context.Query("username")
		context.JSON(http.StatusOK, gin.H{
			"uid":      uid,
			"username": username,
		})
	})

	//  /user/info/ks/k
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
    <form action="/user/add" method="post">  
        <p>username: <input type="text" name="username"></p>  
        <p>userword: <input type="text" name="password"></p>  
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