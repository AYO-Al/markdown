---
number headings: first-level 1, max 6, start-at 1, 1.1
---
# 1 原始SQL

使用 `Scan` 查询原始 SQL

```go
type Result struct {  
ID int  
Name string  
Age int  
}  
  
var result Result  
db.Raw("SELECT id, name, age FROM users WHERE id = ?", 3).Scan(&result)  
  
db.Raw("SELECT id, name, age FROM users WHERE name = ?", "jinzhu").Scan(&result)  
  
var age int  
db.Raw("SELECT SUM(age) FROM users WHERE role = ?", "admin").Scan(&age)  
  
var users []User  
db.Raw("UPDATE users SET name = ? WHERE age = ? RETURNING id, name", "jinzhu", 20).Scan(&users)
```

Exec使用原始SQL

```go
db.Exec("DROP TABLE users")  
db.Exec("UPDATE orders SET shipped_at = ? WHERE id IN ?", time.Now(), []int64{1, 2, 3})  
  
// Exec with SQL Expression  
db.Exec("UPDATE users SET money = ? WHERE name = ?", gorm.Expr("money * ? + ?", 10000, 1), "jinzhu")
```

**GORM 允许缓存准备好的语句以提高性能，详情查看[performance](../配置/performance.md)**
# 2 命名参数

GORM 支持使用 sql.NamedArg 、 `map[string]interface{}{}` 或 struct 的命名参数，例如：

```go
db.Where("name1 = @name OR name2 = @name", sql.Named("name", "jinzhu")).Find(&user)
// SELECT * FROM `users` WHERE name1 = "jinzhu" OR name2 = "jinzhu"

db.Where("name1 = @name OR name2 = @name", map[string]interface{}{"name": "jinzhu2"}).First(&result3)
// SELECT * FROM `users` WHERE name1 = "jinzhu2" OR name2 = "jinzhu2" ORDER BY `users`.`id` LIMIT 1

// Named Argument with Raw SQL
db.Raw("SELECT * FROM users WHERE name1 = @name OR name2 = @name2 OR name3 = @name",
   sql.Named("name", "jinzhu1"), sql.Named("name2", "jinzhu2")).Find(&user)
// SELECT * FROM users WHERE name1 = "jinzhu1" OR name2 = "jinzhu2" OR name3 = "jinzhu1"

db.Exec("UPDATE users SET name1 = @name, name2 = @name2, name3 = @name",
   sql.Named("name", "jinzhunew"), sql.Named("name2", "jinzhunew2"))
// UPDATE users SET name1 = "jinzhunew", name2 = "jinzhunew2", name3 = "jinzhunew"

db.Raw("SELECT * FROM users WHERE (name1 = @name AND name3 = @name) AND name2 = @name2",
   map[string]interface{}{"name": "jinzhu", "name2": "jinzhu2"}).Find(&user)
// SELECT * FROM users WHERE (name1 = "jinzhu" AND name3 = "jinzhu") AND name2 = "jinzhu2"

type NamedArgument struct {
  Name string
  Name2 string
}

db.Raw("SELECT * FROM users WHERE (name1 = @Name AND name3 = @Name) AND name2 = @Name2",
   NamedArgument{Name: "jinzhu", Name2: "jinzhu2"}).Find(&user)
// SELECT * FROM users WHERE (name1 = "jinzhu" AND name3 = "jinzhu") AND name2 = "jinzhu2"

```
# 3 DryRun Mode

生成 `SQL` 及其参数但不执行，可用于准备或测试生成的 SQL，详情请查看[session](../配置/session.md)

```go
// db.DryRun().First(&user)
stmt := db.Session(&gorm.Session{DryRun: true}).First(&user, 1).Statement
stmt.SQL.String() //=> SELECT * FROM `users` WHERE `id` = $1 ORDER BY `id`
stmt.Vars         //=> []interface{}{1}
```
# 4 ToSQL 转 SQL

返回生成的 `SQL` 但不执行。

GORM 使用 database/sql 的参数占位符来构造 SQL 语句，它会自动转义参数以避免 SQL 注入，但生成的 SQL 不提供安全保障，请仅将其用于调试。

```go
sql := db.ToSQL(func(tx *gorm.DB) *gorm.DB {
  return tx.Model(&User{}).Where("id = ?", 100).Limit(10).Order("age desc").Find(&[]User{})
})
sql //=> SELECT * FROM "users" WHERE id = 100 AND "users"."deleted_at" IS NULL ORDER BY age desc LIMIT 10

```

**DryRun/ToSQL区别**

|**特性​**​|​**​DryRun​**​|​**​ToSQL​**​|
|---|---|---|
|​**​功能定位​**​|调试模式开关|SQL 生成工具|
|​**​调用方式​**​|会话级配置|方法级调用|
|​**​输出位置​**​|日志输出|返回字符串|
|​**​钩子触发​**​|✅ 触发所有钩子|❌ 不触发钩子|
|​**​完整流程​**​|模拟完整执行路径|仅生成 SQL|
|​**​错误处理​**​|返回执行错误|仅返回 SQL 生成错误|
|​**​关联处理​**​|包含预加载 SQL|仅主查询 SQL|
|​**​最佳场景​**​|全流程调试|获取 SQL 字符串|
# 5 Row & Rows

获取结果为 `*sql.Row`

```go
// Use GORM API build SQL
row := db.Table("users").Where("name = ?", "jinzhu").Select("name", "age").Row()
row.Scan(&name, &age)

// Use Raw SQL
row := db.Raw("select name, age, email from users where name = ?", "jinzhu").Row()
row.Scan(&name, &age, &email)
```

获取结果为 `*sql.Rows`

```go
// Use GORM API build SQL
rows, err := db.Model(&User{}).Where("name = ?", "jinzhu").Select("name, age, email").Rows()
defer rows.Close()
for rows.Next() {
  rows.Scan(&name, &age, &email)

  // do something
}

// Raw SQL
rows, err := db.Raw("select name, age, email from users where name = ?", "jinzhu").Rows()
defer rows.Close()
for rows.Next() {
  rows.Scan(&name, &age, &email)

  // do something
}


rows, err := db.Model(&User{}).Where("name = ?", "jinzhu").Select("name, age, email").Rows() // (*sql.Rows, error)
defer rows.Close()

var user User
for rows.Next() {
  // ScanRows scan a row into user
  db.ScanRows(rows, &user) // 直接扫到结构体中

  // do something
}
```

查看 [高级查询](高级查询.md) FindInBatches 了解如何批量查询和处理记录

查看[高级查询](高级查询.md) Group Conditions 以了解如何构建复杂的 SQL 查询
# 6 函数说明

## 6.1 `func (db *DB) Raw(sql string, values ...interface{}) (tx *DB)`

执行查询类 SQL 并返回结果集

```go
// 字段名需匹配
type Temp struct {
    Total int // 需要匹配 SELECT COUNT(*) AS total
}
```
## 6.2 `func (db *DB) Exec(sql string, values ...interface{}) (tx *DB)`

执行非查询类 SQL 并返回影响行数

```go
// 插入
result := db.Exec("INSERT INTO users (name, age) VALUES (?, ?)", "Alice", 25)
fmt.Println("插入ID:", result.LastInsertId())

// 更新
result := db.Exec("UPDATE users SET age = ? WHERE name = ?", 26, "Alice")
fmt.Println("影响行数:", result.RowsAffected)

// 删除
db.Exec("DELETE FROM users WHERE age < ?", 18)
```

|**方面​**​|​**​Raw​**​|​**​Exec​**​|
|---|---|---|
|​**​SQL 类型​**​|SELECT 查询|INSERT/UPDATE/DELETE/DDL|
|​**​返回值​**​|结果集|影响行数|
|​**​结果处理​**​|Scan/Find|RowsAffected|
|​**​链式调用​**​|支持后续操作|终止链|
|​**​使用频率​**​|复杂报表查询|数据维护操作|
