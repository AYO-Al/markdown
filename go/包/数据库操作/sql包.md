Go 语言的标准库 ​**​`database/sql`​**​ 是一个通用的 SQL 数据库操作接口，提供统一的 API 支持多种关系型数据库（如 MySQL、PostgreSQL、SQLite 等）。其核心设计是 ​**​解耦驱动与操作​**​，开发者只需实现对应数据库的驱动（Driver），即可通过统一接口访问数据库。

sql 包必须与数据库驱动程序结合使用。有关驱动程序列表，请参阅：[驱动列表](https://go.dev/wiki/SQLDrivers)。

**核心设计**：

- **​驱动接口（Driver）​**​：由第三方库实现（如 `github.com/go-sql-driver/mysql`）。
- ​**​连接池管理​**​：自动管理数据库连接的创建、复用和释放。
- ​**​接口统一​**​：无论底层是哪种数据库，操作方式一致（如 `Query`, `Exec` 等）。
# 变量

- sql包提供了三个错误变量：

```go
var ErrConnDone = errors.New("sql: connection is already closed")

var ErrNoRows = errors.New("sql: no rows in result set")

var ErrTxDone = errors.New("sql: transaction has already been committed or rolled back")
```

- **变量说明**：

|错误变量|触发条件|处理重点|典型场景|
|---|---|---|---|
|`ErrConnDone`|操作已释放的连接|确保连接在有效期内使用|手动管理连接、提前关闭rows|
|`ErrNoRows`|单行查询无结果|显式处理“无数据”逻辑|按ID查询不存在的记录|
|`ErrTxDone`|操作已结束的事务|严格管理事务生命周期|提交后误用事务对象|

# ​核心接口与结构​​

## ​sql.DB​

- ​**​作用​**​：表示数据库连接池，是操作的入口。
    
- ​**​创建方式​**​：
    
    ```go
    db, err := sql.Open("mysql", "user:password@tcp(localhost:3306)/dbname")
    ```
    
    - `sql.Open` 的第一个参数是驱动名（需提前注册驱动）。
    - 第二个参数是数据库的 ​**​DSN（数据源名称）​**​，格式由驱动定义。dbname是可选的，可以在查询中使用 `dbname.tablename` 指定使用库。

### func Open(driverName, dataSourceName string) (\*DB, error)

- ​**​功能​**​：创建数据库连接池，通过驱动名称和数据源字符串初始化。
    - Open 可能只验证其参数而不创建连接 添加到数据库。要验证数据源名称是否有效，请调用Ping方法 。
    - 返回的 DB 可以安全地被多个 goroutine 并发使用，并维护自己的空闲连接池。因此，Open 函数应该只调用一次。很少需要关闭 DB。
### (db \*DB) Begin() (\*Tx, error)​

- **功能​**​：开启事务，返回事务对象 `*Tx`。
- ​**​错误场景​**​：
    - ​**​连接获取失败​**​：连接池中无可用连接，且无法创建新连接（如达到 `SetMaxOpenConns` 限制）。
    - ​**​数据库不支持事务​**​：某些数据库或驱动可能不支持事务。
    - ​**​上下文超时​**​：底层驱动在获取连接时超时。

```go
tx, err := db.Begin()
if err != nil {
    log.Fatal("事务开启失败:", err)
}
```
### (db \*DB) BeginTx(ctx context.Context, opts \*TxOptions) (\*Tx, error)​ 

- ​**​功能​**​：支持上下文和事务选项（如隔离级别）的事务开启。
    - 如果要使用默认的 `TxOptions` 则值为nil。
- ​**​错误场景​**​：
    - 同 `Begin()`，外加：
    - ​**​上下文取消​**​：`ctx` 被取消或超时。
    - ​**​无效事务选项​**​：`opts` 中指定了数据库不支持的事务隔离级别。

```go
ctx := context.Background()
tx, err := db.BeginTx(ctx, &sql.TxOptions{Isolation: sql.LevelSerializable})
if err != nil {
    log.Fatal("事务开启失败:", err)
}
```
###  (db \*DB) Close() error​

- ​**​功能​**​：关闭数据库连接池，释放所有连接。
- ​**​错误场景​**​：
    - ​**​连接关闭失败​**​：某些连接在释放时发生错误（如数据库连接已断开）。
    - ​**​重复关闭​**​：多次调用 `Close()` 可能返回未定义行为，但通常返回 `nil`。
- ​**​注意​**​：通常应忽略此错误，但建议记录日志：
    
```go
    if err := db.Close(); err != nil {
        log.Println("关闭数据库连接池失败:", err)
    }
```
### **`(db *DB) Exec(query string, args ...any) (Result, error)`​**​

### ​(db \*DB) ExecContext(ctx context.Context, query string, args ...any) (Result, error)

- ​**​功能​**​：执行不返回行的 SQL 操作（如 INSERT/UPDATE/DELETE）。
- ​**​错误场景​**​：
    - ​**​SQL 语法错误​**​：查询语句有误。
    - ​**​参数类型不匹配​**​：`args` 与 SQL 中的占位符类型不一致。
    - ​**​违反约束​**​：如主键冲突、外键约束失败。
    - ​**​连接问题​**​：执行期间连接断开。
    - ​**​上下文取消​**​：`ctx` 超时或被取消。
- ​**​示例​**​：
    
```go
import (
	"context"
	"database/sql"
	"log"
)

var (
	ctx context.Context
	db  *sql.DB
)

func main() {
	id := 47
	result, err := db.ExecContext(ctx, "UPDATE balances SET balance = balance + 10 WHERE user_id = ?", id)
	if err != nil {
		log.Fatal(err)
	}
	rows, err := result.RowsAffected()
	if err != nil {
		log.Fatal(err)
	}
	if rows != 1 {
		log.Fatalf("expected to affect 1 row, affected %d", rows)
	}
}

```
### (db \*DB) Ping() error​

### ​(db \*DB) PingContext(ctx context.Context) error​

- ​**​功能​**​：检查数据库连通性。
- ​**​错误场景​**​：
    - ​**​数据库不可达​**​：网络问题或数据库服务未运行。
    - ​**​认证失败​**​：用户名/密码错误。
    - ​**​上下文取消​**​：`PingContext` 中 `ctx` 超时或被取消。
- ​**​示例​**​：
    
```go
    if err := db.Ping(); err != nil {
        log.Fatal("数据库连接异常:", err)
    }
```
### (db \*DB) Prepare(query string) (\*Stmt, error)​

### ​(db \*DB) PrepareContext(ctx context.Context, query string) (\*Stmt, error)​

- ​**​功能​**​：创建预处理语句，提升重复执行效率。
    - 当不再需要语句时，调用方必须调用语句的 \*Stmt.Close 方法。
- ​**​错误场景​**​：
    - ​**​SQL 语法错误​**​：查询语句无效。
    - ​**​连接问题​**​：无法获取连接或连接断开。
    - ​**​上下文取消​**​：`PrepareContext` 中 `ctx` 超时或被取消。
- ​**​示例​**​：
    
```go
    stmt, err := db.Prepare("SELECT * FROM users WHERE id = ?")
    if err != nil {
        log.Fatal("预处理失败:", err)
    }
    defer stmt.Close()
```
### (db \*DB) Query(query string, args ...any) (\*Rows, error)​

### ​(db \*DB) QueryContext(ctx context.Context, query string, args ...any) (\*Rows, error)​

- ​**​功能​**​：执行查询并返回多行结果（`*Rows`）。
- ​**​错误场景​**​：
    - 同 `Exec()`，外加：
    - ​**​结果集迭代错误​**​：在 `rows.Next()` 或 `rows.Scan()` 时可能发生错误（但此错误在 `Query` 调用后才会返回）。
- ​**​注意​**​：必须调用 `rows.Close()` 释放连接。
    
```go
    rows, err := db.Query("SELECT * FROM users")
    if err != nil {
        log.Fatal("查询失败:", err)
    }
    defer rows.Close()
```
### (db \*DB) QueryRow(query string, args ...any) \*Row​

### (db \*DB) QueryRowContext(ctx context.Context, query string, args ...any) \*Row​

- ​**​功能​**​：执行单行查询，返回 `*Row`（延迟错误检查到 `Scan`）。
- ​**​错误场景​**​：
    - 错误不会直接返回，需在 `Scan()` 时检查：
        - `sql.ErrNoRows`：查询结果为空。
        - 其他错误同 `Query()`。
- ​**​示例​**​：
    
```go
    var name string
    err := db.QueryRow("SELECT name FROM users WHERE id = ?", 1).Scan(&name)
    if errors.Is(err, sql.ErrNoRows) {
        log.Println("用户不存在")
    } else if err != nil {
        log.Fatal("查询失败:", err)
    }
```
### (db \*DB) Stats() DBStats​

- ​**​功能​**​：返回连接池的统计信息（如打开连接数、空闲连接数）。
- ​**​错误场景​**​：无错误返回。
### 连接池配置方法

| **方法​**​                                      | ​**​参数类型​**​    | ​**​默认值​**​ | ​**​作用​**​                                  | ​**​适用场景​**​                                             | ​**​注意事项​**​                                                  |
| --------------------------------------------- | --------------- | ----------- | ------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------- |
| ​**​`SetMaxOpenConns(n int)`​**​              | `int`           | 无限制         | 设置连接池中​**​最大打开的连接数​**​（包括活跃和空闲连接）。          | 高并发场景下，防止数据库因连接数过多而过载。                                   | - 设为 `0` 表示无限制。  <br>- 应根据数据库的 `max_connections` 配置合理调整。      |
| ​**​`SetMaxIdleConns(n int)`​**​              | `int`           | 2           | 设置连接池中​**​最大空闲连接数​**​（未被使用但保持打开的连接）。        | 平衡资源消耗与性能：空闲连接过多浪费资源，过少则需频繁创建新连接。                        | - 建议设为 `SetMaxOpenConns` 的 1/4 到 1/2。  <br>- 若设为 `0`，则禁用空闲连接。 |
| ​**​`SetConnMaxLifetime(d time.Duration)`​**​ | `time.Duration` | 无限制         | 设置​**​连接的最长存活时间​**​（从创建到关闭的总时间，即使空闲也会超时关闭）。 | 数据库有连接存活时间限制（如 MySQL 的 `wait_timeout`），避免应用使用已被数据库关闭的连接。 | - 建议设为略小于数据库的 `wait_timeout`。  <br>- 设为 `0` 表示无限制。            |
| ​**​`SetConnMaxIdleTime(d time.Duration)`​**​ | `time.Duration` | 无限制         | 设置​**​连接的最长空闲时间​**​（连接在空闲状态下可保留的最长时间）。      | 释放长时间未使用的空闲连接，减少资源占用（适用于连接使用频率波动较大的场景）。                  | - 建议设为分钟级（如 `5*time.Minute`）。  <br>- 设为 `0` 表示无限制。            |
## sql.DBStats

```go
type DBStats struct {
	MaxOpenConnections int // Maximum number of open connections to the database.

	// Pool Status
	OpenConnections int // The number of established connections both in use and idle.
	InUse           int // The number of connections currently in use.
	Idle            int // The number of idle connections.

	// Counters
	WaitCount         int64         // The total number of connections waited for.
	WaitDuration      time.Duration // The total time blocked waiting for a new connection.
	MaxIdleClosed     int64         // The total number of connections closed due to SetMaxIdleConns.
	MaxIdleTimeClosed int64         // The total number of connections closed due to SetConnMaxIdleTime.
	MaxLifetimeClosed int64         // The total number of connections closed due to SetConnMaxLifetime.
}

```

- **字段说明：**

|字段名|类型|说明|
|---|---|---|
|​**​MaxOpenConnections​**​|`int`|连接池允许的最大打开连接数（由 `SetMaxOpenConns` 设置）。|
|​**​OpenConnections​**​|`int`|当前已建立的连接总数（包括正在使用和空闲的连接）。|
|​**​InUse​**​|`int`|正在被使用的连接数（例如：活跃的查询或事务）。|
|​**​Idle​**​|`int`|当前空闲的连接数（可被复用的连接）。|
|​**​WaitCount​**​|`int64`|因连接池耗尽而等待获取连接的总次数（从 `DB` 创建开始累计）。|
|​**​WaitDuration​**​|`time.Duration`|所有等待获取连接的总耗时（反映因连接不足导致的延迟）。|
|​**​MaxIdleClosed​**​|`int64`|因超过 `SetMaxIdleConns` 设置的空闲连接数而被关闭的连接总数。|
|​**​MaxIdleTimeClosed​**​|`int64`|因超过 `SetConnMaxIdleTime` 设置的空闲时间而被关闭的连接总数。|
|​**​MaxLifetimeClosed​**​|`int64`|因超过 `SetConnMaxLifetime` 设置的连接最大存活时间而被关闭的连接总数。|
- **核心用途**：​

    - ​**​监控连接池状态​**​：实时查看连接使用情况（活跃、空闲、总量）。
    - ​**​性能调优​**​：根据统计指标优化连接池参数配置。
    - ​**​故障排查​**​：识别连接泄漏、资源竞争或配置不当问题。

## sql.Result

Result 接口用于描述 ​​非查询类 SQL 操作​​（如 INSERT/UPDATE/DELETE）的执行结果，提供两个核心方法获取操作元数据：

```go
type Result interface {
    LastInsertId() (int64, error)  // 获取自增 ID（如插入行的主键）
    RowsAffected() (int64, error)  // 获取受影响的行数
}
```

- **方法详解**​​

|方法|返回值|适用场景|常见错误场景|
|---|---|---|---|
|​**​`LastInsertId()`​**​|`int64`, `error`|插入操作后获取自增主键（如 MySQL 的 `AUTO_INCREMENT`）。|- 数据库/驱动不支持自增 ID（如 PostgreSQL 默认不返回，需用 `RETURNING` 子句）。  <br>- 操作非插入语句（如 `UPDATE`）。|
|​**​`RowsAffected()`​**​|`int64`, `error`|获取 `INSERT`/`UPDATE`/`DELETE` 影响的行数。|
## sql.Row​

`Row` 是调用 `DB.QueryRow` 或 `Tx.QueryRow` 方法后返回的结果，用于处理​**​预期最多返回一行​**​的查询（如按主键查询）。其核心特点是：

- ​**​单行处理​**​：若查询返回多行，仅扫描第一行，其余丢弃。
- ​**​延迟错误处理​**​：查询错误不会立即返回，而是在调用 `Scan()` 或 `Err()` 时暴露。​
- **资源释放**：即使不读取数据，也需调用 `Scan()` 或 `Err()` 确保底层连接释放。

### ​func (r \*Row) Scan(dest ...any) error​

- ​**​功能​**​：将查询结果的列值复制到 `dest` 变量中。
- ​**​行为​**​：
    - ​**​成功​**​：返回 `nil`，数据存入 `dest`。
    - ​**​无结果​**​：返回 `sql.ErrNoRows`。
    - ​**​查询错误​**​：返回执行查询时的错误（如 SQL 语法错误、连接失败）。
    - ​**​多行结果​**​：静默丢弃后续行，仅扫描第一行。
- ​**​必须调用​**​：即使不关心结果，也应调用 `Scan()` 以确保释放资源。

### ​func (r \*Row) Err() error（Go 1.15+）​​

- ​**​功能​**​：直接返回查询过程中的错误，无需调用 `Scan()`。
- ​**​适用场景​**​：需要提前检查错误（如日志记录），或在不扫描数据时获取错误信息。

- **常见错误**：

|**错误场景​**​|​**​触发条件​**​|​**​处理方法​**​|
|---|---|---|
|​**​`sql.ErrNoRows`​**​|查询结果为空（如按不存在的 ID 查询）。|根据业务逻辑处理，如返回 404 或忽略。|
|​**​多行结果​**​|查询返回多行（如未在 SQL 中限制为单行）。|确保查询条件唯一（如使用主键），或在 SQL 中添加 `LIMIT 1`。|
|​**​SQL 语法错误​**​|SQL 语句错误（如表名拼写错误）。|检查 SQL 语句，记录错误详情。|
|​**​连接错误​**​|数据库连接中断或超时。|重试逻辑或返回服务不可用状态。|
|​**​类型不匹配​**​|`Scan` 目标变量类型与数据库列类型不兼容（如字符串扫描到 `int`）。|确保目标变量类型与查询列类型匹配。|
## sql.Rows

`Rows` 表示一个查询结果集，用于处理​**​多行数据​**​的遍历与解析。其核心机制是通过游标逐行读取数据，支持多结果集处理（如存储过程或批量查询）。

### ​核心方法​

|​**​方法​**​|​**​功能​**​|​**​关键行为​**​|
|---|---|---|
|​**​`Close() error`​**​|关闭结果集，释放连接。|幂等操作，多次调用安全。必须显式或通过 `defer` 调用，避免连接泄漏。|
|​**​`Columns() ([]string, error)`​**​|返回列名列表。|若 `Rows` 已关闭，返回错误。通常在遍历前调用，用于动态处理结果集。|
|​**​`Next() bool`​**​|移动游标至下一行，准备扫描。|返回 `true` 表示有数据；`false` 表示无数据或出错，需检查 `Err()`。|
|​**​`Scan(dest ...any) error`​**​|将当前行数据扫描到 `dest` 变量中。|`dest` 数量须与列数一致。支持类型自动转换，处理 `NULL` 需用 `sql.Null*` 类型。|
|​**​`Err() error`​**​|返回遍历过程中发生的错误（如网络中断、SQL 异常）。|应在 `Next()` 返回 `false` 后调用，以区分正常结束与错误。|
|​**​`NextResultSet() bool`​**​|移动到下一个结果集（如多语句查询）。|返回 `true` 表示存在下一个结果集，需再次调用 `Next()` 遍历其数据。|
|​**​`ColumnTypes() ([]*ColumnType, error)`​**​|返回列元数据（类型、精度、是否可为 `NULL`）。|用于动态解析结果集，部分驱动可能不支持某些元数据。|

### ​**​标准使用流程​**​

```go
rows, err := db.Query("SELECT id, name FROM users")
if err != nil {
    log.Fatal("查询失败:", err)
}
defer rows.Close() // 确保资源释放

// 遍历每一行
for rows.Next() {
    var id int
    var name string
    if err := rows.Scan(&id, &name); err != nil {
        log.Fatal("扫描失败:", err)
    }
    fmt.Printf("ID: %d, Name: %s\n", id, name)
}

// 检查遍历过程中是否出错
if err := rows.Err(); err != nil {
    log.Fatal("遍历错误:", err)
}
```

- 处理 NULL 值​**​

    - 使用 `sql.Null*` 类型或指针接收可能为 `NULL` 的列：

```go
var name sql.NullString
var age *int
err := rows.Scan(&name, &age)
if name.Valid {
    fmt.Println("Name:", name.String)
} else {
    fmt.Println("Name: NULL")
}
if age != nil {
    fmt.Println("Age:", *age)
} else {
    fmt.Println("Age: NULL")
}
```

- 多结果集处理​**​

    - 适用于批量查询或存储过程：

```go
for {
    // 处理当前结果集
    for rows.Next() {
        // Scan 数据...
    }
    if err := rows.Err(); err != nil {
        log.Fatal(err)
    }
    // 跳转至下一个结果集
    if !rows.NextResultSet() {
        break
    }
}
```

### ​错误处理与陷阱​​

|​**​错误场景​**​|​**​原因与示例​**​|​**​解决方案​**​|
|---|---|---|
|​**​未关闭 `Rows`​**​|忘记调用 `rows.Close()`，导致连接泄漏。|始终使用 `defer rows.Close()`。|
|​**​`Scan` 参数不符​**​|`dest` 变量数量或类型与查询列不匹配。|检查 SQL 列数与 `Scan` 参数，使用 `Columns()` 动态适配。|
|​**​忽略 `Err()`​**​|未在 `Next()` 循环后检查错误，导致隐藏的连接问题。|循环结束后调用 `if err := rows.Err(); err != nil { ... }`。|
|​**​类型转换错误​**​|将 `NULL` 扫描到非指针类型，或大数值存入小类型（如 `int64` → `int8`）。|使用 `sql.Null*` 类型或指针接收 `NULL`，验证数值范围。|
|​**​跨行引用 `RawBytes`​**​|`RawBytes` 数据在下次 `Next()` 后被覆盖。|仅在当前行使用 `RawBytes`，或复制数据到独立 `[]byte`。|

> 总结​

- ​**​`Rows` 是处理多行查询的核心​**​，需严格遵循 `Open → Next → Scan → Close` 的生命周期。
- ​**​错误处理不可忽略​**​：检查 `Query` 错误、`Scan` 错误及遍历结束后的 `Err()`。
- ​**​灵活应对复杂场景​**​：动态列处理、多结果集遍历需结合 `Columns()` 和 `ColumnTypes()`。
## sql.Stmt

`sql.Stmt` 类型表示一个预处理语句（Prepared Statement），用于高效执行重复的 SQL 操作。

1. ​**​预处理 SQL​**​  
    将 SQL 语句预先编译并缓存，后续执行时只需传递参数，减少数据库解析开销。
2. ​**​防止 SQL 注入​**​  
    通过参数化查询（占位符 `?` 或 `$1`），避免用户输入直接拼接 SQL。
3. ​**​高效执行重复操作​**​  
    适用于批量插入、更新等需要多次执行相同 SQL 的场景。

|方法|功能|返回类型|
|---|---|---|
|​**​`Exec(args ...any) (Result, error)`​**​|执行非查询操作（如 `INSERT`, `UPDATE`）并返回结果。|`sql.Result`|
|​**​`Query(args ...any) (*Rows, error)`​**​|执行查询操作（如 `SELECT`）并返回多行结果集。|`*sql.Rows`|
|​**​`QueryRow(args ...any) *Row`​**​|执行单行查询，返回一行结果。|`*sql.Row`|
|​**​`Close() error`​**​|释放预处理语句占用的资源（如数据库连接）。|`error`|
|​**​`ExecContext(ctx, args...)`​**​|支持上下文的 `Exec` 操作（可设置超时或取消）。|`sql.Result`, `error`|
|​**​`QueryContext(ctx, args...)`​**​|支持上下文的 `Query` 操作。|`*sql.Rows`, `error`|
|​**​`QueryRowContext(ctx, args...)`​**​|支持上下文的 `QueryRow` 操作。|`*sql.Row`|
- **使用流程**：​

    1. ​**​准备语句​**​：使用 `DB.Prepare` 或 `DB.PrepareContext` 创建 `Stmt`。
    2. ​**​执行操作​**​：调用 `Exec`、`Query` 或 `QueryRow` 方法（可多次执行）。
    3. ​**​关闭资源​**​：通过 `defer stmt.Close()` 确保释放资源。

```go
// 1. 准备预处理语句
stmt, err := db.Prepare("INSERT INTO users (name, age) VALUES (?, ?)")
if err != nil {
    log.Fatal("预处理失败:", err)
}
defer stmt.Close() // 确保关闭

// 2. 多次执行
users := []struct {
    Name string
    Age  int
}{
    {"Alice", 30},
    {"Bob", 25},
}

for _, user := range users {
    result, err := stmt.Exec(user.Name, user.Age)
    if err != nil {
        log.Fatal("执行失败:", err)
    }
    id, _ := result.LastInsertId()
    fmt.Println("插入用户 ID:", id)
}
```


> ​​特性与注意事项​​


1. ​**​并发安全​**​

    - `Stmt` 是并发安全的，多个 Goroutine 可同时调用同一 `Stmt` 的方法。
    - 内部通过连接池管理，无需用户处理底层连接。

 2. ​**​资源管理​**​

    - ​**​必须调用 `Close()`​**​：及时释放数据库资源（如连接、游标），避免泄漏。
    - ​**​长期复用优化​**​：高频使用的 `Stmt` 可在应用生命周期内保持打开，避免重复准备。

 3. ​**​参数绑定​**​

    - 参数数量必须与 SQL 中的占位符数量一致。
    - 参数类型需与数据库列类型兼容（如字符串、数值、时间等）。

 4. ​**​错误处理​**​

    - ​**​预处理错误​**​：`Prepare` 失败可能因 SQL 语法错误或连接问题。
    - ​**​执行错误​**​：`Exec` 或 `Query` 失败可能因参数错误、约束冲突等。
## sql.Tx

`Tx` 类型代表一个数据库事务，用于确保一系列操作的原子性（要么全部成功，要么全部回滚）。

- **核心作用**：

    1. ​**​原子性保证​**​：事务内的操作要么全部提交成功，要么全部回滚。
    2. ​**​隔离性​**​：事务中的操作对其他事务暂时不可见，直到提交。
    3. ​**​资源管理​**​：事务对象（`*Tx`）需显式提交或回滚，否则会导致连接泄漏。

- **注意事项**：

    1. 事务必须调用对 Tx.Commit 或 Tx.Rollback 的结束。
    2. 调用 Tx.Commit 或 Tx.Rollback 后，对事务的所有操作都失败，并显示 ErrTxDone。
    3. 通过调用事务的 Tx.Prepare 或 Tx.Stmt 方法为事务准备的语句通过调用 Tx.Commit 或 Tx.Rollback 来关闭。
### Commit() error

- ​**​功能​**​：提交事务，永久保存所有变更。
- ​**​错误场景​**​：
    - 网络中断或数据库连接失败。
    - 违反约束（如唯一键冲突）。
- ​**​示例​**​：
    
```go
    if err := tx.Commit(); err != nil {
        log.Fatal("提交失败:", err)
    }
```
### Rollback() error

- ​**​功能​**​：回滚事务，撤销所有未提交的变更。
- ​**​幂等性​**​：多次调用安全，但可能返回错误。
- ​**​最佳实践​**​：使用 `defer tx.Rollback()` 确保异常时回滚。
    
```go
    tx, _ := db.Begin()
    defer tx.Rollback() // 提交后调用 Rollback 会返回 ErrTxDone，但无害
```
### Exec` 和 `ExecContext

- ​**​功能​**​：执行非查询 SQL（如 INSERT/UPDATE/DELETE）。
- ​**​错误场景​**​：
    - SQL 语法错误。
    - 违反约束（如外键不存在）。
    - 事务已关闭（返回 `ErrTxDone`）。
- ​**​示例​**​：
    
```go
    result, err := tx.Exec("UPDATE users SET active=? WHERE id=?", true, 123)
    if err != nil {
        return err
    }
```
### Query 和 QueryContext​

- ​**​功能​**​：执行查询并返回多行结果（`*Rows`）。
- ​**​资源释放​**​：必须调用 `rows.Close()`。
    
```go
    rows, _ := tx.Query("SELECT * FROM orders WHERE user_id=?", 123)
    defer rows.Close()
```
### ​QueryRow 和 QueryRowContext

- ​**​功能​**​：执行单行查询，结果通过 `Scan` 获取。
- ​**​错误处理​**​：检查 `Scan` 的错误，如 `ErrNoRows`。
    
```go
    var total int
    err := tx.QueryRow("SELECT SUM(amount) FROM payments").Scan(&total)
    if errors.Is(err, sql.ErrNoRows) {
        log.Println("无支付记录")
    }
```
### Prepare 和 PrepareContext​

- ​**​功能​**​：创建事务作用域的预处理语句，事务提交/回滚后自动关闭。
- ​**​示例​**​：
    
```go
    stmt, _ := tx.Prepare("INSERT INTO logs (message) VALUES (?)")
    defer stmt.Close() // 可选，事务结束会自动关闭
    stmt.Exec("Transaction started")
```
    

### Stmt 和 StmtContext​

- ​**​功能​**​：将全局预处理语句转换为事务专用语句。
- ​**​适用场景​**​：复用全局预处理语句，提升事务效率。
    
```go
    updateStmt, _ := db.Prepare("UPDATE accounts SET balance = balance + ? WHERE id = ?")
    txStmt := tx.Stmt(updateStmt)
    txStmt.Exec(100.0, 456)
```

> 最佳实践

1. ​**​资源管理​**​：
    
    - 使用 `defer tx.Rollback()` 确保事务回滚。
    - 及时关闭 `Rows` 和 `Stmt` 对象。
2. ​**​错误处理​**​：
    
    - 检查所有操作的错误，尤其是 `Commit`。
    - 使用 `errors.Is(err, sql.ErrTxDone)` 判断事务状态。
3. ​**​性能优化​**​：
    
    - 复用预处理语句（`tx.Stmt`）减少解析开销。
    - 合理设置事务隔离级别（通过 `TxOptions`）。
4. ​**​上下文控制​**​：
    
    - 使用 `ExecContext`/`QueryContext` 设置超时或取消。
    
```go
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    _, err := tx.ExecContext(ctx, "DELETE FROM tmp_data")
```
## sql.Txoptions

- `TxOptions` 结构体用于配置数据库事务的隔离级别和访问模式（只读或读写）。它通常与 `DB.BeginTx` 方法结合使用，允许开发者对事务行为进行更精细的控制。

```go
type TxOptions struct {
    Isolation IsolationLevel // 事务隔离级别
    ReadOnly  bool           // 是否只读
}
```

### **`Isolation IsolationLevel`​**​

- ​**​作用​**​：指定事务的隔离级别，决定事务在并发操作中的数据可见性和锁行为。
- ​**​可选值​**​：

|常量|值|描述|
|---|---|---|
|`LevelDefault`|-1|使用数据库或驱动的默认隔离级别。|
|`LevelReadUncommitted`|0|读未提交：允许读取未提交的数据（可能脏读）。|
|`LevelReadCommitted`|1|读已提交：只能读取已提交的数据（避免脏读，允许不可重复读）。|
|`LevelRepeatableRead`|2|可重复读：保证同一事务内多次读取结果一致（防止不可重复读，可能幻读）。|
|`LevelSerializable`|3|串行化：最高隔离级别，完全串行执行事务（避免脏读、不可重复读、幻读）。|
|`LevelLinearizable`|4|线性化（部分数据库支持，如 MongoDB）。|
- ​**​默认行为​**​：若 `Isolation` 为 `LevelDefault` 或零值，使用数据库默认级别（通常为 `LevelReadCommitted`）。
### ReadOnly bool

- **作用​**​：标记事务是否为只读。只读事务可能触发数据库优化（如避免写锁、减少日志记录）。
- ​**​示例​**​：
    - `ReadOnly: true`：事务内只能执行 `SELECT` 查询。
    - `ReadOnly: false`（默认）：允许读写操作（`INSERT`, `UPDATE`, `DELETE`）。