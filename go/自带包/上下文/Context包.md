`context` 是 Go 语言并发编程中的核心组件，设计用于处理请求作用域的数据、取消信号和超时控制。它广泛应用于并发控制、请求处理、API调用等场景。

 **核心目的：**

1. ​**​取消传播​**​：在多个goroutine间传递取消信号
2. ​**​超时控制​**​：设置截止时间(deadline)或超时(timeout)
3. ​**​请求域数据传递​**​：安全传递与请求相关的元数据
4. ​**​构建可取消操作​**​：实现资源友好的任务终止机制

**关键机制：**

​**1. ​取消传播​**​：

- 父 Context 被取消 → ​**​所有派生 Context 自动取消​**​
- 子 Context 单独取消 → ​**​不影响父 Context​**

​**​2. 派生方法​**​：

- ​**​必须调用 `cancel()`​**​：  
    避免资源泄漏（`go vet` 会检查控制流路径是否调用了 `cancel`）
- ​**​原因记录​**​：  
    `WithXXXCause` 系列函数支持记录取消的 error 原因（通过 `context.Cause()` 获取）

**必须遵守的规则​**​

1. ​**​显式传递​**​：
    
    - ❌ 禁止将 Context 存储到结构体字段中
    - ✅ 作为函数​**​首个参数​**​显式传递（命名惯例 `ctx context.Context`）
        
        > 📌 参考：https://go.dev/blog/context-and-structs
        
2. ​**​禁止传递 `nil`​**​：
    
    - ❌ 不允许 `nil` Context
    - ✅ 不确定时用 `context.TODO()`
3. ​**​作用域限制​**​：
    
    - ❌ ​**​避免​**​将 context.Value 作为函数可选参数
    - ✅ ​**​仅传递请求域数据​**​（如认证 token、TraceID）
    - ✅ ​**​线程安全​**​：可跨 goroutine 传递同一 Context
# 1 函数
## 1.1 func WithCancel(parent Context) (ctx Context, cancel CancelFunc)

**作用​**​：创建可手动取消的 Context  
​**​参数​**​：
- `parent`：父 Context（非 nil）  

​**​返回值​**​：
- `ctx`：派生的新 Context
- `cancel`：调用时取消 Context 的函数

​**​注意事项​**​：
- 必须调用 `cancel()` 释放资源
- 父 Context 取消时自动取消子 Context
- 多次调用 `cancel()` 是安全的

```go
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel() // 确保资源释放
    
    go func() {
        time.Sleep(500 * time.Millisecond)
        cancel() // 手动取消
    }()

    select {
    case <-time.After(1 * time.Second):
        fmt.Println("操作完成")
    case <-ctx.Done():
        fmt.Println("操作取消:", ctx.Err()) // 输出：context canceled
    }
}
```
## 1.2 func WithCancelCause(parent Context) (ctx Context, cancel CancelCauseFunc)

​**​作用​**​：创建可带取消原因的 Context  
​**​参数​**​：
- `parent`：父 Context  

**​返回值​**​：
- `ctx`：派生的新 Context
- `cancel`：接收错误参数的取消函数

​**​注意事项​**​：
- 通过 `Cause(ctx)` 获取取消原因
- 未设置原因时 `Cause()` 返回与 `ctx.Err()` 相同

```go
func main() {
    ctx, cancel := context.WithCancelCause(context.Background())
    defer cancel(nil) // 安全调用
    
    go func() {
        time.Sleep(500 * time.Millisecond)
        // 带错误原因取消
        cancel(fmt.Errorf("自定义错误"))
    }()

    <-ctx.Done()
    fmt.Println("原因:", context.Cause(ctx)) 
    // 输出：自定义错误
}
```
## 1.3 func WithDeadline(parent Context, d time.Time) (Context, CancelFunc)

​**​作用​**​：创建带绝对截止时间的 Context  
​**​参数​**​：
- `parent`：父 Context
- `d`：具体截止时间点  

**​返回值​**​：
- `ctx`：派生的新 Context
- `cancel`：可手动提前取消的函数

​**​注意事项​**​：
- 实际截止时间是父 Context 和设定时间的较早值
- 调用 `cancel()` 可提前取消

```go
func main() {
    deadline := time.Now().Add(500 * time.Millisecond)
    ctx, cancel := context.WithDeadline(context.Background(), deadline)
    defer cancel()
    
    start := time.Now()
    <-ctx.Done()
    
    fmt.Printf("等待时间: %v\n", time.Since(start).Round(time.Millisecond))
    fmt.Println("原因:", ctx.Err()) 
    // 输出：等待时间: 500ms  原因: context deadline exceeded
}
```
## 1.4 func WithDeadlineCause(parent Context, d time.Time, cause error) (Context, CancelFunc)

​**​作用​**​：创建带截止时间和超时原因的 Context  
​**​参数​**​：
- `parent`：父 Context
- `d`：截止时间点
- `cause`：超时原因  

**​返回值​**​：
- `ctx`：派生的新 Context
- `cancel`：可手动提前取消的函数

​**​注意事项​**​：
- 仅当因截止时间取消时返回预设原因
- 手动取消需单独设置原因

```go
func main() {
    cause := fmt.Errorf("服务响应超时")
    ctx, cancel := context.WithTimeoutCause(context.Background(), 100*time.Millisecond, cause)
    defer cancel()
    
    if err := slowOperation(ctx); err != nil {
        fmt.Println("原因:", context.Cause(ctx))
        // 输出：服务响应超时
    }
}

func slowOperation(ctx context.Context) error {
    time.Sleep(200 * time.Millisecond)
    return nil
}
```
## 1.5 func AfterFunc(ctx Context, f func()) (stop func() bool)

​**​作用​**​：在 Context 完成时异步执行函数  
​**​参数​**​：
- `ctx`：监听的 Context
- `f`：Context 完成时执行的函数  

​**​返回值​**​：
- `stop`：可阻止函数执行的停止函数（返回是否成功阻止）

​**​注意事项​**​：
- Context 已完成时立即执行 `f`
- `stop()` 只能在 `f` 执行前生效
- `f` 在自己的 goroutine 中执行

```go
func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 300*time.Millisecond)
    defer cancel()
    
    // 注册结束回调
    stop := context.AfterFunc(ctx, func() {
        fmt.Println("清理资源")
    })
    
    go func() {
        time.Sleep(100 * time.Millisecond)
        if stop() {
            fmt.Println("成功阻止回调")
        }
    }()
    
    time.Sleep(1 * time.Second)
    // 可能输出：清理资源 或 成功阻止回调
}
```
## 1.6 func Cause(c Context) error

​**​作用​**​：获取 Context 取消的原因  

​**​参数​**​：
- `c`：要检查的 Context  

**​返回值​**​：
- 取消的错误原因（未取消返回 nil）

​**​注意事项​**​：
- 优先返回通过 `WithXXXCause` 设置的错误
- 没有设置原因时返回 `ctx.Err()`
- 未取消时返回 nil

```go
func main() {
    // 场景1：设置自定义原因
    ctx1, cancel1 := context.WithCancelCause(context.Background())
    cancel1(fmt.Errorf("用户强制终止"))
    fmt.Println(context.Cause(ctx1)) 
    // 输出：用户强制终止

    // 场景2：默认超时原因
    ctx2, cancel2 := context.WithTimeout(context.Background(), time.Microsecond)
    defer cancel2()
    time.Sleep(10 * time.Millisecond)
    fmt.Println(context.Cause(ctx2)) 
    // 输出：context deadline exceeded

    // 场景3：未取消
    fmt.Println(context.Cause(context.Background()))
    // 输出：<nil>
}
```

| ​**​功能​**​       | `context.Err()`                        | `context.Cause(ctx)`           |
| ---------------- | -------------------------------------- | ------------------------------ |
| ​**​返回内容​**​     | 标准取消类型 (`Canceled`/`DeadlineExceeded`) | 具体取消原因（自定义错误或标准错误）             |
| ​**​获取原因机制​**​   | Context 接口的内置方法                        | 外部函数检查取消原因                     |
| ​**​自定义错误支持​**​  | 不返回自定义原因                               | 优先返回通过 `WithXXXCause` 设置的自定义错误 |
| ​**​未取消时的返回值​**​ | `nil`                                  | `nil`                          |
| ​**​设计目的​**​     | 检查是否取消                                 | 获取取消的具体原因                      |
# 2 关键错误说明

1. ​**​context.Canceled​**：`var Canceled = errors.New("context canceled")`​
    
    - 手动取消 Context 时的默认错误
    - 可通过 `WithCancelCause` 覆盖
2. ​**​context.DeadlineExceeded​**：`var DeadlineExceeded error = deadlineExceededError{}
`​ 

    - 超时/截止时间到的默认错误
    - 可通过 `WithDeadlineCause`/`WithTimeoutCause` 覆盖
3. ​**​nil 错误​**​
    
    - `Cause()` 在 Context 未取消时返回 nil
    - 调用前应检查 `ctx.Err() != nil`
# 3 类型
## 3.1 Context接口

跨 API 和进程传递请求范围的数据、截止时间和取消信号

```go
Deadline() (deadline time.Time, ok bool) // 返回截止时间
Done() <-chan struct{}                  // 返回取消信号通道
Err() error                             // 返回取消原因
Value(key any) any                      // 获取请求域值
```

**特性​**​：

- 线程安全
- 不可变性（派生产生新 Context）
- 取消传播（父取消 → 子取消）
### 3.1.1 func Background() Context

​**​作用​**​：创建根 Context（空状态）  

​**​使用场景​**​：
- 入口函数初始化
- 测试用例起点
- 顶层请求起点

​**​注意事项​**​：
- 不会被取消、无截止时间、不存储值
- ​**​不应传递 nil​**​ 时用此代替

```go
func main() {
    ctx := context.Background()
    
    // 添加请求ID
    reqCtx := context.WithValue(ctx, "requestID", "12345")
    
    fmt.Println("请求ID:", reqCtx.Value("requestID"))
    // 输出: 请求ID: 12345
}
```
### 3.1.2 func TODO() Context

​**​作用​**​：创建占位 Context  

​**​使用场景​**​：
- 重构过程临时使用
- 不确定使用哪个 Context 时
- 避免传递 `nil`

​**​注意事项​**​：
- 设计意图标记"待处理"区域
- 静态分析工具可检测 TODO 使用

```go
func legacyFunction() {
    // 重构期间临时使用
    ctx := context.TODO()
    
    // 执行操作...
    fmt.Println("使用临时Context:", ctx)
}
```
### 3.1.3 func WithValue(parent Context, key, val any) Context

​**​作用​**​：创建携带键值对的派生 Context  

​**​参数​**​：
- `parent`: 父 Context
- `key`: 键 (推荐使用自定义类型避免冲突)，不能为nil否则panic
- `val`: 值

​**​返回值​**​：  
新的 Context（包含键值对）

​**​注意事项​**​：
- 仅存储请求域数据（认证信息、追踪ID）
- ​**​避免存储函数参数或可选参数​**​
- 使用自定义键类型

```go
type traceIDKey struct{} // 自定义键类型

func handler(ctx context.Context) {
    // 安全获取追踪ID
    if id, ok := ctx.Value(traceIDKey{}).(string); ok {
        fmt.Println("追踪ID:", id)
    }
}

func main() {
    parent := context.Background()
    
    // 添加追踪ID
    ctx := context.WithValue(parent, traceIDKey{}, "trace-abc123")
    
    handler(ctx) // 输出: 追踪ID: trace-abc123
}
```
### 3.1.4 func WithoutCancel(parent Context) Context

​**​作用​**​：创建不受父 Context 取消影响的 Context  

​**​参数​**​：  
`parent`：父 Context

​**​返回值​**​：  
新的 Context（屏蔽取消）

​**​注意事项​**​：
- 父取消时不会传播到子 Context
- 但子 Context 可独立取消
- 典型场景：
    - 清理操作需在父取消后继续
    - 独立的后台任务

```go
func cleanupTask(ctx context.Context) {
    select {
    case <-time.After(2 * time.Second):
        fmt.Println("清理完成")
    case <-ctx.Done():
        fmt.Println("清理取消")
    }
}

func main() {
    parent, cancel := context.WithCancel(context.Background())
    
    // 创建独立清理Context
    cleanupCtx := context.WithoutCancel(parent)
    go cleanupTask(cleanupCtx)
    
    // 取消主Context
    cancel()
    
    time.Sleep(3 * time.Second)
    // 输出: 清理完成 (即使parent已取消)
}
```
## 3.2 CancelFunc func()

**作用​**​：取消关联的 Context 及其子 Context  

​**​使用场景​**​：  
用于 `WithCancel`, `WithDeadline`, `WithTimeout` 的返回值

​**​注意事项​**​：
- 多次调用安全
- ​**​必须调用​**​以避免资源泄漏
- 取消顺序：子→孙→关联资源

```go
func worker(ctx context.Context) {
    // 处理中检查取消信号
    if ctx.Err() != nil {
        return
    }
}

func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel() // 确保取消
    
    go worker(ctx)
    time.Sleep(100 * time.Millisecond)
    cancel() // 通知 worker 停止
    
    fmt.Println(ctx.Err()) // 输出: context canceled
}
```
## 3.3 CancelCauseFunc func(cause error)

**作用​**​：取消关联 Context 并记录错误原因  

​**​使用场景​**​：  
用于 `WithCancelCause`, `WithDeadlineCause`, `WithTimeoutCause` 的返回值

​**​注意事项​**​：
- 通过 `Cause(ctx)` 获取错误
- 设置原因优于默认错误
- 可传递 `nil` 原因（回退默认错误）

```go
func main() {
    ctx, cancel := context.WithCancelCause(context.Background())
    
    // 在函数中设置错误原因
    go func() {
        time.Sleep(100 * time.Millisecond)
        cancel(fmt.Errorf("资源不足"))
    }()
    
    <-ctx.Done()
    fmt.Println("原因:", context.Cause(ctx))
    // 输出: 原因: 资源不足
}
```
