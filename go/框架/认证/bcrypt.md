- 下载

```go
go get -u golang.org/x/crypto/bcrypt
```

-  func CompareHashAndPassword(hashedPassword, password \[\]byte) error

	- CompareHashAndPassword 比较 bcrypt 哈希密码与其可能的明文等效形式。成功时返回 nil，失败时返回错误。

- func GenerateFromPassword(password \[\]byte, cost int) (\[\]byte, error)

	- GenerateFromPassword 返回给定成本的密码的 bcrypt 哈希值。如果给定的成本小于 MinCost，成本将被设置为 DefaultCost。使用本包中定义的 CompareHashAndPassword 函数，将返回的哈希密码与其明文版本进行比较。GenerateFromPassword 不接受超过 72 字节的密码，这是 bcrypt 将处理的密码最长长度。

```go
const (
	MinCost     int = 4  // the minimum allowable cost as passed in to GenerateFromPassword
	MaxCost     int = 31 // the maximum allowable cost as passed in to GenerateFromPassword
	DefaultCost int = 10 // the cost that will actually be set if a cost below MinCost is passed into GenerateFromPassword
)
```
