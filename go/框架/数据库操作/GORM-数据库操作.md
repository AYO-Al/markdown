# 1 基础设置
GROM官方文档：https://gorm.io/zh_CN/
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
## 定义命名规则

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

![[Gorm.excalidraw]]