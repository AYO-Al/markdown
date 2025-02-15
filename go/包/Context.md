包context定义了Context类型，它携带跨API边界和进程之间的截止日期、取消信号和其他请求范围的值。

`context.Context` 是 Go 语言在 1.7 版本中引入标准库的接口，该接口定义了四个需要实现的方法，其中包括：

```go
type Context interface {
    Deadline() (deadline time.Time, ok bool)
    Done() <-chan struct{}
    Err() error
    Value(key any) any
}
```

1. `Deadline` — 返回 `context.Context` 被取消的时间，也就是完成工作的截止日期；

```go
// 示例：获取上下文的截止时间
// 返回一个截止时间，如果设置了截止时间，则 ok 为 true，否则为 false
func checkDeadline(ctx context.Context) {
    deadline, ok := ctx.Deadline()
    if ok {
        fmt.Printf("截止时间: %v\n", deadline)
    } else {
        fmt.Println("没有设置截止时间")
    }
}
```

2. `Done` — 返回一个 Channel，这个 Channel 会在当前工作完成或者上下文被取消后关闭，多次调用 `Done` 方法会返回同一个 Channel；

```go
// 示例：监听取消信号
// 返回一个 channel，当上下文被取消时，channel 会被关闭
func processWithCancel(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err() // 返回取消原因
        default:
            // 执行业务逻辑
        }
    }
}
```

3. `Err` — 返回 `context.Context` 结束的原因，它只会在 `Done` 方法对应的 Channel 关闭时返回非空的值；
    1. 如果 `context.Context` 被取消，会返回 `Canceled` 错误；
    2. 如果 `context.Context` 超时，会返回 `DeadlineExceeded` 错误；

```go
func checkContextError(ctx context.Context) {
    if ctx.Err() == context.Canceled {
        fmt.Println("上下文被取消")
    } else if ctx.Err() == context.DeadlineExceeded {
        fmt.Println("上下文超时")
    }
}
```

4. `Value` — 从 `context.Context` 中获取键对应的值，对于同一个上下文来说，多次调用 `Value` 并传入相同的 `Key` 会返回相同的结果，该方法可以用来传递请求特定的数据；

```go
// 示例：存取上下文中的值
// 返回上下文中的值，如果 key 不存在，则返回 nil
func handleRequestWithUser(ctx context.Context) {
    if username, ok := ctx.Value("user").(string); ok {
        fmt.Printf("处理用户 %s 的请求\n", username)
    }
}
```

# 解决问题

- 请求级别的数据传递

- 超时控制

- 取消信号传播

- 跨 API 边界的数据传递

- goroutine 生命周期管理
# 设计原理

在 Goroutine 构成的树形结构中对信号进行同步以减少计算资源的浪费是 `context.Context` 的最大作用。Go 服务的每一个请求都是通过单独的 Goroutine 处理的，HTTP/RPC 请求的处理器会启动新的 Goroutine 访问数据库和其他服务。

每一个 `context.Context` 都会从最顶层的 Goroutine 一层一层传递到最下层。`context.Context` 可以在上层 Goroutine 执行出现错误时，**将信号及时同步给下层**。例如：
```go
func main() {
	//deadline := time.Now().Add(5 * time.Second)
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()

	go handle(ctx, 1*time.Second)
	select {
	case <-ctx.Done():
		fmt.Println("main", ctx.Err())
	}
}

func handle(ctx context.Context, duration time.Duration) {
	select {
	case <-ctx.Done():
		fmt.Println(ctx.Err())
	case <-time.After(duration):
		fmt.Println("process request with", duration)
	}
}
/* 输出
process request with 1s
main context deadline exceeded
*/
```

`context.Context` 的使用方法和设计原理 — 多个 Goroutine 同时订阅 `ctx.Done()` 管道中的消息，一旦接收到取消信号就立刻停止当前正在执行的工作。
# 上下文使用
## 默认上下文

`context` 包中最常用的方法还是 `context.Background`、`context.TODO`，这两个方法都会返回预先初始化好的私有变量 `background` 和 `todo`，它们会在同一个 Go 程序中被复用：
```go
// 返回一个非零的空上下文。它永远不会被取消，没有值，没有截止日期。它通常由主函数、初始化和测试使用，并作为传入请求的顶级上下文
func Background() Context {  
    return backgroundCtx{}  
}

// 返回一个非零的空上下文。当不确定使用哪个Context的时候使用
func TODO() Context {  
    return todoCtx{}  
}
```

这两个结构体里面包含的都是emptyCtx空结构体。
```go
// Go 1.7版本之后变成空接口体
/* 
空结构体在 Go 语言中不占用任何内存空间。
减少内存分配和垃圾回收的开销。
更清晰地表达 `emptyCtx` 的语义，即它是一个空的上下文，没有任何附加信息。
*/

type emptyCtx struct{}  
  
func (emptyCtx) Deadline() (deadline time.Time, ok bool) {  
    return  
}  
  
func (emptyCtx) Done() <-chan struct{} {  
    return nil  
}  
  
func (emptyCtx) Err() error {  
    return nil  
}  
  
func (emptyCtx) Value(key any) any {  
    return nil  
}
```

从上述代码中，我们不难发现 `context.emptyCtx`、 通过空方法实现了 `context.Context` 接口中的所有方法，它没有任何功能。

从源代码来看，context.Background 和 context.TODO 也只是互为别名，没有太大的差别，只是在使用和语义上稍有不同：

- context.Background 是上下文的默认值，所有其他的上下文都应该从它衍生出来；
- context.TODO 应该仅在不确定应该使用哪种上下文时使用；

在多数情况下，如果当前函数没有上下文作为入参，我们都会使用 context.Background 作为起始的上下文向下传递。
## 取消信号

context.WithCancel 函数能够从 context.Context 中衍生出一个新的子上下文并返回用于取消该上下文的函数。一旦我们执行返回的取消函数，当前上下文以及它的子上下文都会被取消，所有的 Goroutine 都会同步收到这一取消信号。

```go
type cancelCtx struct {  
    Context  
  
    mu       sync.Mutex            // protects following fields  
    done     atomic.Value          // of chan struct{}, created lazily, closed by first cancel call    children map[canceler]struct{} // set to nil by the first cancel call    err      error                 // set to non-nil by the first cancel call    cause    error                 // set to non-nil by the first cancel call}  
  
func (c *cancelCtx) Value(key any) any {  
    if key == &cancelCtxKey {  
       return c  
    }  
    return value(c.Context, key)  
}  
  
func (c *cancelCtx) Done() <-chan struct{} {  
    d := c.done.Load()  
    if d != nil {  
       return d.(chan struct{})  
    }  
    c.mu.Lock()  
    defer c.mu.Unlock()  
    d = c.done.Load()  
    if d == nil {  
       d = make(chan struct{})  
       c.done.Store(d)  
    }  
    return d.(chan struct{})  
}  
  
func (c *cancelCtx) Err() error {  
    c.mu.Lock()  
    err := c.err  
    c.mu.Unlock()  
    return err  
}  
  
// propagateCancel arranges for child to be canceled when parent is.// It sets the parent context of cancelCtx.  
func (c *cancelCtx) propagateCancel(parent Context, child canceler) {  
    c.Context = parent  
  
    done := parent.Done()  
    if done == nil {  
       return // parent is never canceled  
    }  
  
    select {  
    case <-done:  
       // parent is already canceled  
       child.cancel(false, parent.Err(), Cause(parent))  
       return  
    default:  
    }  
  
    if p, ok := parentCancelCtx(parent); ok {  
       // parent is a *cancelCtx, or derives from one.  
       p.mu.Lock()  
       if p.err != nil {  
          // parent has already been canceled  
          child.cancel(false, p.err, p.cause)  
       } else {  
          if p.children == nil {  
             p.children = make(map[canceler]struct{})  
          }  
          p.children[child] = struct{}{}  
       }  
       p.mu.Unlock()  
       return  
    }  
  
    if a, ok := parent.(afterFuncer); ok {  
       // parent implements an AfterFunc method.  
       c.mu.Lock()  
       stop := a.AfterFunc(func() {  
          child.cancel(false, parent.Err(), Cause(parent))  
       })  
       c.Context = stopCtx{  
          Context: parent,  
          stop:    stop,  
       }  
       c.mu.Unlock()  
       return  
    }  
  
    goroutines.Add(1)  
    go func() {  
       select {  
       case <-parent.Done():  
          child.cancel(false, parent.Err(), Cause(parent))  
       case <-child.Done():  
       }  
    }()  
}

func withCancel(parent Context) *cancelCtx {  
    if parent == nil {  
       panic("cannot create context from nil parent")  
    }  
    c := &cancelCtx{}  
    c.propagateCancel(parent, c)  
    return c  
}

func WithCancel(parent Context) (ctx Context, cancel CancelFunc) {  
    c := withCancel(parent)  
    return c, func() { c.cancel(true, Canceled, nil) }  
}
```

示例：

```go
func main() {  
    //deadline := time.Now().Add(5 * time.Second)  
    ctx, cancel := context.WithCancel(context.Background())  
    go func() {  
       i := 1  
       for {  
          select {  
          case <-ctx.Done():  
             fmt.Println("press done...")  
             return  
          default:  
             fmt.Println(i, "....")  
             i++  
             time.Sleep(1 * time.Second)  
          }  
       }  
    }()  
  
    time.Sleep(1 * time.Second)  
  
    cancel()  // 退出后goroutine也退出
  
    time.Sleep(1 * time.Second)  
}
```
## 超时时间

设置超时时间的ctx有两种`WithDeadline`和`WithTimeout`

```go
func WithDeadline(parent Context, d time.Time) (Context, CancelFunc)

func WithTimeout(parent Context, timeout time.Duration) (Context, CancelFunc)
```

这两个上下文的区别是一个设置的具体日期，一个设置持续时间。
## 值传递

```go
package main

import (
	"context"
	"fmt"
)

func main() {
	type favContextKey string

	f := func(ctx context.Context, k favContextKey) {
		if v := ctx.Value(k); v != nil {
			fmt.Println("found value:", v)
			return
		}
		fmt.Println("key not found:", k)
	}

	k := favContextKey("language")
	ctx := context.WithValue(context.Background(), k, "Go")

	f(ctx, k)
	f(ctx, favContextKey("color"))

}
/*
Output:

found value: Go
key not found: color
*/
```

在真正使用传值的功能时我们也应该非常谨慎，使用 context.Context 传递请求的所有参数一种非常差的设计，比较常见的使用场景是传递请求对应用户的认证令牌以及用于进行分布式追踪的请求 ID。