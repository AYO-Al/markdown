`errors` 提供了一系列操作错误的函数，用于创建、检查和操作错误对象。在Go语言中，错误是一种内建的接口类型，定义为：

```go
type error interface {
    Error() string
}
```
# 1 func New(text string) error

​**​作用​**​：创建简单错误对象  
​**​参数​**​：`text string`（错误信息文本）  
​**​返回值​**​：携带文本的错误对象  
​**​注意事项​**​：

- 不支持嵌套错误（不可用 `Unwrap()` 解析）
- 相同文本也会创建不同对象（需用 `errors.Is()` 判断相等性）

```go
package main

import (
	"errors"
	"fmt"
)

func main() {
	// 创建基础错误
	err := errors.New("文件读取失败")
	fmt.Println(err.Error()) // 输出: 文件读取失败

	// 相同文本创建的不同错误对象
	err2 := errors.New("文件读取失败")
	fmt.Println(err == err2) // false：不同内存地址
	fmt.Println(errors.Is(err, err2)) // false：无自定义Is方法，无法识别为相同错误
}
```
# 2 func Unwrap(err error) error

​**​作用​**​：解包嵌套错误  
​**​参数​**​：`err error`（嵌套错误对象）  
​**​返回值​**​：

- 成功：解包后的错误
- 失败：`nil`  
    ​**​注意事项​**​：
- 仅支持实现 `Unwrap() error` 的错误类型
- 多层嵌套需多次调用

```go
package main

import (
	"errors"
	"fmt"
)

func main() {
    // 创建两层嵌套错误
    baseErr := errors.New("原始错误")
    wrappedErr := fmt.Errorf("包装层1: %w", fmt.Errorf("包装层2: %w", baseErr))
    
    // 第一次解包
    if unwrapped := errors.Unwrap(wrappedErr); unwrapped != nil {
        fmt.Println(unwrapped) // 输出: 包装层2: 原始错误
    }
    
    // 第二次解包
    if unwrapped2 := errors.Unwrap(unwrapped); unwrapped2 != nil {
        fmt.Println(unwrapped2) // 输出: 原始错误
    }
    
    // 继续解包
    if unwrapped3 := errors.Unwrap(unwrapped2); unwrapped3 == nil {
        fmt.Println("无法继续解包") // 触发：baseErr未实现Unwrap()
    }
}
```
# 3 func Is(err, target error) bool

​**​作用​**​：检查错误链中是否存在目标错误  
​**​参数​**​：

- `err error`：错误链起点
- `target error`：目标错误  
    ​**​返回值​**​：
- `true`：错误链中存在目标错误
- `false`：不存在  
    ​**​注意事项​**​：
- 通过递归调用 `Unwrap()` 遍历错误链
- 支持自定义 `Is(error) bool` 方法（优先级最高）
- `target` 应为可比较的单一错误值

```go
package main

import (
	"errors"
	"fmt"
)

type TimeoutError struct{}

func (e TimeoutError) Error() string { return "请求超时" }

func main() {
    baseErr := TimeoutError{}
    wrappedErr := fmt.Errorf("操作失败: %w", baseErr)

    // 检查错误链
    if errors.Is(wrappedErr, baseErr) {
        fmt.Println("检测到TimeoutError") // 输出: 检测到TimeoutError
    }

    // 检查未实现的自定义错误
    customErr := errors.New("自定义错误")
    fmt.Println(errors.Is(wrappedErr, customErr)) // false：错误链中不存在
}
```
# 4 func As(err error, target any) bool

​**​作用​**​：提取错误链中特定类型的错误  
​**​参数​**​：

- `err error`：错误链起点
- `target any`：目标类型指针（必须非 `nil`）  
    ​**​返回值​**​：
- `true`：找到匹配类型并赋值给 `target`
- `false`：未找到  
    ​**​注意事项​**​：
- `target` 必须是接口或具体类型的指针
- 错误赋值到 `target` 时会保留原始错误信息
- 类型不匹配或 `target` 为 `nil` 时会导致 panic

```go
package main

import (
	"errors"
	"fmt"
)

type NetworkError struct{ Msg string }

func (e NetworkError) Error() string { return e.Msg }

func main() {
    baseErr := NetworkError{Msg: "连接断开"}
    wrappedErr := fmt.Errorf("网络故障: %w", baseErr)

    var target NetworkError
    if errors.As(wrappedErr, &target) {
        fmt.Println(target) // 输出: 连接断开
    }

    // 错误用法：target未初始化指针
    var p *NetworkError
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("触发panic:", r) // 输出: target不能为nil指针
        }
    }()
    errors.As(wrappedErr, p) // panic: target为nil指针
}
```
# 5 func Join(errs ...error) error

​**​作用​**​：合并多个错误为一个复合错误  
​**​参数​**​：`errs ...error`（错误列表）  
​**​返回值​**​：

- 非空错误列表：返回 `multiError` 对象
- 空列表：返回 `nil`  
    ​**​注意事项​**​：
- `Unwrap()` 返回 `nil`（需用 `As()`/`Is()` 处理）
- 遍历错误链时优先匹配第一个可解包错误
- 复合错误的 `Error()` 返回所有错误文本拼接

```go
package main

import (
	"errors"
	"fmt"
)

func main() {
    err1 := errors.New("错误1")
    err2 := errors.New("错误2")
    joinedErr := errors.Join(err1, err2)
    
    fmt.Println(joinedErr) // 输出: 错误1\n错误2
    
    // Unwrap无法解包复合错误
    if errors.Unwrap(joinedErr) == nil {
        fmt.Println("无法解包Join的错误") // 输出: 无法解包Join的错误
    }
    
    // 通过Is检查成员
    if errors.Is(joinedErr, err1) {
        fmt.Println("找到错误1") // 输出: 找到错误1
    }
    
    // 空列表返回nil
    emptyErr := errors.Join()
    fmt.Println(emptyErr) // nil
}
```

# 6 建议

1. ​**​错误比较​**​：
    - 不要用 `==` 比较 `errors.New()` 的错误（除非是同实例）
    - 用 `errors.Is()` 代替值比较（支持嵌套错误和自定义行为）
2. ​**​嵌套结构​**​：
    - 使用 `fmt.Errorf("...%w...", err)` 包裹错误
    - 避免深层嵌套（超过 5 层降低可读性）
3. ​**​复合错误​**​：
    - `Join()` 适合合并无关错误（如批量操作）
    - 优先包裹因果错误（`%w`）而非拼接文本（`fmt.Errorf`）
4. ​**​自定义错误​**​：
    - 实现 `Unwrap() error` 支持嵌套
    - 实现 `Is() bool` 或 `As()` 支持高级匹配