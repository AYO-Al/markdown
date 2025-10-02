# 1 基础设置

GROM官方文档：https://gorm.io/zh_CN/
- 下载：go get -u gorm.io/gorm
## 1.1 连接Mysql数据库

```go
import (
  "gorm.io/driver/mysql"
  "gorm.io/gorm"
)

func main() {
  // 参考 https://github.com/go-sql-driver/mysql#dsn-data-source-name 获取详情
  dsn := "user:pass@tcp(127.0.0.1:3306)/dbname?charset=utf8mb4&parseTime=True&loc=Local"
  db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
}
```

## 1.2 设置全局sql日志输出

Gorm 有一个 [默认 logger 实现](https://github.com/go-gorm/gorm/blob/master/logger/logger.go)，默认情况下，它会打印慢 SQL 和错误

`Silent`、`Error`、`Warn`、`Info`是Gorm定义的四个日志等级。

```go
newLogger := logger.New(
  log.New(os.Stdout, "\r\n", log.LstdFlags), // io writer
  logger.Config{
    SlowThreshold:              time.Second,   // Slow SQL threshold
    LogLevel:                   logger.Silent, // Log level
    IgnoreRecordNotFoundError: true,           // Ignore ErrRecordNotFound error for logger
    ParameterizedQueries:      true,           // Don't include params in the SQL log
    Colorful:                  false,          // Disable color
  },
)

// Globally mode
db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{
  Logger: newLogger,
})
```
## 1.3 定义命名规则

```go
db, err := gorm.Open(sqlite.Open("gorm.db"), &gorm.Config{  
  NamingStrategy: schema.NamingStrategy{  
    TablePrefix: "t_",   // table name prefix, table for `User` would be `t_users`  
    SingularTable: true, // use singular table name, table for `User` would be `user` with this option enabled  
    NoLowerCase: true, // skip the snake_casing of names  
    NameReplacer: strings.NewReplacer("CID", "Cid"), // use name replacer to change struct/field name before convert it to db name  
  },  
})
```

# 2 错误处理

[错误处理](https://gorm.io/zh_CN/docs/error_handling.html)

# 3 save

在 GORM 中，`Save` 方法用于 ​**插入或更新记录**，其行为会根据记录是否存在（基于主键）自动判断是执行 `INSERT` 还是 `UPDATE`。以下是它的详细说明：

---

### 3.1.1 ​**1. `Save` 的核心功能**

- ​**如果记录不存在**​（主键为零值，如 `ID=0`）：执行 `INSERT`，插入新记录。
- ​**如果记录已存在**​（主键非零）：执行 `UPDATE`，更新所有字段（即使字段未修改）。

---

### 3.1.2 ​**2. 使用场景**

#### 3.1.2.1 ​**(1) 插入新记录**

当模型实例的主键字段（如 `ID`）为零值时，`Save` 会插入新记录：

go

```go
user := User{Name: "Alice", Age: 25}
result := db.Save(&user)  // 执行 INSERT
fmt.Println(user.ID)      // 插入后自动填充主键（如自增 ID）
```

#### 3.1.2.2 ​**(2) 更新现有记录**

当模型实例的主键非零时，`Save` 会更新该记录的所有字段：

```go
user := User{ID: 1, Name: "Bob", Age: 30}
result := db.Save(&user)  // 执行 UPDATE，更新所有字段（即使 Age 未变）
```

---

### 3.1.3 ​**3. 与 `Create`/`Update` 的区别**

| 方法       | 行为                                              |
| -------- | ----------------------------------------------- |
| `Create` | 仅插入新记录（主键为零值时触发），忽略非零主键。                        |
| `Update` | 仅更新指定字段（需配合 `Where` 或模型主键），不自动判断插入/更新。          |
| `Save`   | 根据主键自动判断插入或更新，且更新所有字段（包括零值）。如果更新的结构体中字段没有值会更新成空 |

### 3.1.4 ​**4. 注意事项**

#### 3.1.4.1 ​**(1) 零值覆盖问题**

`Save` 会更新所有字段，包括零值（如 `0`、`""`、`false`），可能导致数据意外覆盖：

go

```go
user := User{ID: 1, Name: ""}  // 假设原记录的 Name 是 "Alice"
db.Save(&user)                 // Name 会被更新为空字符串！
```

- ​**解决方案**：使用 `Select` 或 `Updates` 指定更新字段：
    ```go
    db.Model(&user).Select("Name").Updates(User{Name: ""})
    ```


# 4 `FirstOrInit`, 以及 `Attrs` 和 `Assign`

GORM 的 `FirstOrInit` 方法用于获取与特定条件匹配的第一条记录，如果没有成功获取，就初始化一个新实例。
```go
// 如果没找到 name 为 "non_existing" 的 User，就初始化一个新的 User  
var user 
User  <br>db.FirstOrInit(&user, User{Name: "non_existing"})  <br>// user -> User{Name: "non_existing"} if not found|
```

当记录未找到，你可以使用 `Attrs` 来初始化一个有着额外属性的结构体。 这些属性包含在新结构中，但不在 SQL 查询中使用。
```go
// 如果没找到 User，根据所给条件和额外属性初始化 User  
// 如果记录被找到，Attrs会被忽略
db.Where(User{Name: "non_existing"}).Attrs(User{Age: 20}).FirstOrInit(&user)  
// SQL: SELECT * FROM USERS WHERE name = 'non_existing' ORDER BY id LIMIT 1;  
// user -> User{Name: "non_existing", Age: 20} if not found
```


`Assign` 方法允许您在结构上设置属性，不管是否找到记录。 这些属性设定在结构上，但不用于生成 SQL 查询，最终数据不会被保存到数据库。
```go

// 根据所给条件和分配的属性初始化，不管记录是否存在  
db.Where(User{Name: "non_existing"}).Assign(User{Age: 20}).FirstOrInit(&user)  // user -> User{Name: "non_existing", Age: 20} if not found  
// 如果找到了名为“Jinzhu”的用户，使用分配的属性更新结构体  
db.Where(User{Name: "Jinzhu"}).Assign(User{Age: 20}).FirstOrInit(&user)  
// SQL: SELECT * FROM USERS WHERE name = 'Jinzhu' ORDER BY id LIMIT 1;  
// user -> User{ID: 111, Name: "Jinzhu", Age: 20} if found
```

# 5 Pluck

GORM 中的 `Pluck` 方法用于从数据库中查询单列并扫描结果到片段（slice）。 当您需要从模型中检索特定字段时，此方法非常理想。

如果需要查询多个列，可以使用 `Select` 配合 [Scan](https://gorm.io/zh_CN/docs/query.html) 或者 [Find](https://gorm.io/zh_CN/docs/query.html) 来代替。
```go
// 检索所有用户的 age
var ages []int64
db.Model(&User{}).Pluck("age", &ages)

// 检索所有用户的 name
var names []string
db.Model(&User{}).Pluck("name", &names)

// 从不同的表中检索 name
db.Table("deleted_users").Pluck("name", &names)

// 使用Distinct和Pluck
db.Model(&User{}).Distinct().Pluck("Name", &names)
// SQL: SELECT DISTINCT `name` FROM `users`

// 多列查询
db.Select("name", "age").Scan(&users)
db.Select("name", "age").Find(&users)

```
## 5.1 scope

GORM中的 `Scopes` 是一个强大的特性，它允许您将常用的查询条件定义为可重用的方法。 这些作用域可以很容易地在查询中引用，从而使代码更加模块化和可读。

```go
// Scope for filtering records where amount is greater than 1000
func AmountGreaterThan1000(db *gorm.DB) *gorm.DB {
  return db.Where("amount > ?", 1000)
}

// Scope for orders paid with a credit card
func PaidWithCreditCard(db *gorm.DB) *gorm.DB {
  return db.Where("pay_mode_sign = ?", "C")
}

// Scope for orders paid with cash on delivery (COD)
func PaidWithCod(db *gorm.DB) *gorm.DB {
  return db.Where("pay_mode_sign = ?", "COD")
}

// Scope for filtering orders by status
func OrderStatus(status []string) func(db *gorm.DB) *gorm.DB {
  return func(db *gorm.DB) *gorm.DB {
    return db.Where("status IN (?)", status)
  }
}

// 使用 scopes 来寻找所有的 金额大于1000的信用卡订单
db.Scopes(AmountGreaterThan1000, PaidWithCreditCard).Find(&orders)

// 使用 scopes 来寻找所有的 金额大于1000的货到付款（COD）订单
db.Scopes(AmountGreaterThan1000, PaidWithCod).Find(&orders)

//使用 scopes 来寻找所有的 具有特定状态且金额大于1000的订单
db.Scopes(AmountGreaterThan1000, OrderStatus([]string{"paid", "shipped"})).Find(&orders)

```

# 6 思维导图

![[Gorm.excalidraw]]