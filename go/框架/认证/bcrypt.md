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

- 格式说明

```go
// 固定总长度：60 个字符
$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy
↓  ↓  ↓                          ↓
│  │  │                          └── 哈希结果 (31字符)
│  │  └───────────────────────────── 盐值 (22字符)  
│  └───────────────────────────────── 成本因子=10
└──────────────────────────────────── 算法版本=2a

```

1. **算法标识**​ (`$2a$`)

- `$2a$`表示使用 bcrypt 算法
    
- 其他可能的值：`$2b$`, `$2y$`（不同版本的bcrypt实现）
    

2. **成本因子**​ (`$10$`)

- 这里的 `10`表示哈希计算的工作因子
    
- 计算轮数 = 2^成本因子
    
- 例如：`10`→ 2^10 = 1024 轮计算
    
- 值越大，计算越慢，安全性越高
    

 3. **盐值**​ (22个字符)

- 长度：22个字符（使用修改的Base64编码）
    
- 对应：16字节的随机盐值
    
- 作用：防止彩虹表攻击，确保相同密码产生不同哈希
    

 4. **哈希结果**​ (31个字符)

- 长度：31个字符
    
- 对应：24字节的实际密码哈希值
    
- 这是密码经过bcrypt算法处理后的最终结果

