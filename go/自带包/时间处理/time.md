Go语言的`time`包是处理日期和时间的核心库，提供了丰富的时间操作功能。
# 1 常量

- 预定义布局

```go
const (
	Layout      = "01/02 03:04:05PM '06 -0700" // The reference time, in numerical order.
	ANSIC       = "Mon Jan _2 15:04:05 2006"
	UnixDate    = "Mon Jan _2 15:04:05 MST 2006"
	RubyDate    = "Mon Jan 02 15:04:05 -0700 2006"
	RFC822      = "02 Jan 06 15:04 MST"
	RFC822Z     = "02 Jan 06 15:04 -0700" // RFC822 with numeric zone
	RFC850      = "Monday, 02-Jan-06 15:04:05 MST"
	RFC1123     = "Mon, 02 Jan 2006 15:04:05 MST"
	RFC1123Z    = "Mon, 02 Jan 2006 15:04:05 -0700" // RFC1123 with numeric zone
	RFC3339     = "2006-01-02T15:04:05Z07:00"
	RFC3339Nano = "2006-01-02T15:04:05.999999999Z07:00"
	Kitchen     = "3:04PM"
	// Handy time stamps.
	Stamp      = "Jan _2 15:04:05"
	StampMilli = "Jan _2 15:04:05.000"
	StampMicro = "Jan _2 15:04:05.000000"
	StampNano  = "Jan _2 15:04:05.000000000"
	DateTime   = "2006-01-02 15:04:05"
	DateOnly   = "2006-01-02"
	TimeOnly   = "15:04:05"
)
```

| ​**​类别​**​      | ​**​常量​**​    | ​**​格式示例​**​                    | ​**​使用场景​**​   |
| --------------- | ------------- | ------------------------------- | -------------- |
| ​**​标准布局​**​    | `Layout`      | `01/02 03:04:05PM '06 -0700`    | 原生参考格式         |
| ​**​Unix格式​**​  | `ANSIC`       | `Mon Jan _2 15:04:05 2006`      | Unix系统日志       |
|                 | `UnixDate`    | `Mon Jan _2 15:04:05 MST 2006`  |                |
| ​**​RFC标准​**​   | `RFC822`      | `02 Jan 06 15:04 MST`           | 电子邮件/HTTP协议    |
|                 | `RFC1123`     | `Mon, 02 Jan 2006 15:04:05 MST` |                |
| ​**​ISO8601​**​ | `RFC3339`     | `2006-01-02T15:04:05Z07:00`     | 现代API/JSON数据交换 |
|                 | `RFC3339Nano` | `2006-01-02T15:04:05.999Z07:00` | 高精度时间戳         |
| ​**​简写格式​**​    | `Kitchen`     | `3:04PM`                        | 用户界面时间展示       |
| ​**​时间戳​**​     | `StampMicro`  | `Jan _2 15:04:05.000000`        | 微秒级日志记录        |
| ​**​分区格式​**​    | `DateOnly`    | `2006-01-02`                    | 仅日期存储          |
|                 | `TimeOnly`    | `15:04:05`                      | 仅时间存储          |
**参考时间​**​：`2006-01-02 15:04:05.999999999 -07:00`  
这是 Go 语言时间格式化的核心锚点时间，各字段含义：

- `2006` → 年份模板（可简写为 `06`）
- `01` → 月份（数字）
- `02` → 日
- `15` → 24小时制小时（`03`表示12小时制）
- `04` → 分钟
- `05` → 秒
- `999999999` → 纳秒
- `-07:00` → 时区偏移

**时区说明​**​：

- 以`-`或`+`开头：表示时区偏移，如"-0700"表示比UTC晚7小时。
- 以`Z`开头：表示时区为UTC（即偏移0）。对于非UTC时区，将显示实际偏移，如"Z07:00"格式，当时间在UTC时显示为"Z"，其他时区显示为"+07:00"或"-07:00"等。
- 注意：布局字符串中的非参考时间部分（如固定文字）将被原样保留。

- 持续时间常量

```go
const (
	Nanosecond  Duration = 1
	Microsecond          = 1000 * Nanosecond // 1μs = 1000ns
	Millisecond          = 1000 * Microsecond // 1ms = 1000μs
	Second               = 1000 * Millisecond // 1s = 1000ms
	Minute               = 60 * Second       // 1m = 60s
	Hour                 = 60 * Minute       // 1h = 60m
)
```
# 2 函数

## 2.1 func After(d Duration) <-chan Time

​**​作用​**​：创建单次计时通道  
​**​参数​**​：

- `d Duration`：等待时间（纳秒精度），负值被视为0  
    ​**​返回值​**​：只读时间通道（发送一次当前时间）  
    ​**​注意事项​**​：
- 通道不接收会导致计时器资源泄露
- 多路径选择时用 `select` 避免阻塞

```go
func afterExample() {
    fmt.Println("After启动:", time.Now().Format("05.000"))
    
    // ✅ 标准用法
    afterChan := time.After(150 * time.Millisecond)
    
    // ❌ 危险: 未接收的After通道
    _ = time.After(100 * time.Millisecond) // 会导致goroutine泄露
    
    select {
    case t := <-afterChan:
        fmt.Printf("After触发: %s\n", t.Format("05.000")) // 显示毫秒部分
    case <-time.After(200 * time.Millisecond): // 安全超时
        fmt.Println("After未被接收")
    }
}
/* 输出示例:
After启动: 30.123
After触发: 30.274 (约150ms后触发)
*/
```

## 2.2 func Sleep(d Duration)

​**​作用​**​：阻塞当前 goroutine  
​**​参数​**​：

- `d Duration`：休眠时间，负值被视为0  
    ​**​返回值​**​：无  
    ​**​注意事项​**​：
- 实际休眠时间可能略长于指定值
- 不可中断的阻塞操作
- 在并发场景中考虑使用可中断方案

```go
func sleepExample() {
    fmt.Println("Sleep开始:", time.Now().Format("05.000"))
    
    // ✅ 标准休眠
    time.Sleep(220 * time.Millisecond)
    fmt.Printf("正常结束: %s\n", time.Now().Format("05.000"))
    
    // ❌ 负值处理
    start := time.Now()
    time.Sleep(-5 * time.Second) // 被转为0
    elapsed := time.Since(start)
    fmt.Printf("负值休眠耗时: %v\n", elapsed) // ≈0s
}
/* 输出示例:
Sleep开始: 45.123
正常结束: 45.348 (约225ms后)
负值休眠耗时: 1.041µs
*/
```

## 2.3 func Tick(d Duration) <-chan Time

​**​作用​**​：创建周期计时通道  
​**​参数​**​：

- `d Duration`：间隔时间，负值会panic  
    ​**​返回值​**​：只读时间通道（周期性发送时间）  
    ​**​注意事项​**​：
- ​**​无法手动关闭​**​，永久占用资源
- 仅适用于程序生命周期内的任务
- 有限任务请改用 `time.NewTicker`

```go
func tickExample() {
    fmt.Println("Tick启动:", time.Now().Format("05.000"))
    defer fmt.Println("函数退出") // 验证资源释放
    
    // ✅ 使用带超时的Tick
    tickCh := time.Tick(180 * time.Millisecond)
    timeout := time.After(900 * time.Millisecond)
    
    for i := 1; ; i++ {
        select {
        case t := <-tickCh:
            fmt.Printf("Tick %d: %s\n", i, t.Format("05.000"))
        case <-timeout:
            // ❌ 重要: 无法释放tick资源!
            fmt.Println("=== 超时结束 ===")
            return
        }
    }
    
    // 危险: 无退出条件的Tick
    // for range time.Tick(1*time.Second) {} // 永久占用资源
}
/* 输出示例:
Tick启动: 15.123
Tick 1: 15.303
Tick 2: 15.483
Tick 3: 15.663
Tick 4: 15.843
=== 超时结束 ===
函数退出
*/
```
# 3 类型
## 3.1 Duration

表示两个时间点之间经过的时间（纳秒计数）  

​**​取值范围​**​:  
约 ±292 年（`math.MinInt64` 到 `math.MaxInt64` 纳秒）

```go
type Duration int64
```
### 3.1.1 func ParseDuration(s string) (Duration, error)

​**​作用​**​: 解析时间字符串为 Duration 类型  
​**​参数​**​:

- `s string`: 时间描述字符串（支持单位：ns/µs/us/ms/s/m/h）  
    ​**​返回值​**​:
- `Duration`: 解析成功的时间段
- `error`: 格式错误时返回非 nil

​**​错误情况​**​:

- 无效单位（如 `1x`）
- 非数字前缀（如 `abc3s`）
- 浮点数格式错误（如 `1.2.3s`）

```go
func parseDurationExample() {
    // ✅ 合法格式
    if d, err := time.ParseDuration("1h30m45.75s"); err == nil {
        fmt.Printf("标准解析: %v (%.2f小时)\n", d, d.Hours())
    } else {
        fmt.Println("解析错误:", err)
    }
    
    // ❌ 无效单位
    _, err := time.ParseDuration("1y") // 年不被支持
    fmt.Println("错误解析:", err) // "time: unknown unit y in duration 1y"
    
    // ✅ 特殊单位支持
    d, _ := time.ParseDuration("500µs") // 微秒
    fmt.Println("微秒解析:", d) // 500µs
    
    // ✅ 小数支持
    d, _ = time.ParseDuration("1.5e3ms") // 1500ms
    fmt.Println("科学计数法:", d) // 1.5s
}
/* 输出:
标准解析: 1h30m45.75s (1.51小时)
错误解析: time: unknown unit y in duration 1y
微秒解析: 500µs
科学计数法: 1.5s
*/
```
### 3.1.2 func Since(t Time) Duration

​**​作用​**​: 计算当前时间与过去时间点 t 的差值  
​**​参数​**​:

- `t Time`: 过去的时间点  
    ​**​返回值​**​:
- `Duration`: t 到现在经过的时间（负值表示当前在 t 之前）

```go
func sinceExample() {
    start := time.Now()
    time.Sleep(250 * time.Millisecond)
    
    elapsed := time.Since(start)
    fmt.Printf("耗时: %v (%.2f秒)\n", elapsed, elapsed.Seconds())
    
    // ✅ 单调时钟确保精度
    futureTime := start.Add(1 * time.Hour)
    negative := time.Since(futureTime)
    fmt.Printf("未来时间差: %v (%.2f分钟)\n", 
                negative, negative.Minutes())
}
/* 输出:
耗时: 255.792ms (0.26秒)
未来时间差: -59m59.999999999s (-60.00分钟) 
*/
```
### 3.1.3 func Until(t Time) Duration

​**​作用​**​: 计算当前时间到未来时间点 t 的剩余时间  
​**​参数​**​:

- `t Time`: 未来的时间点  
    ​**​返回值​**​:
- `Duration`: 现在到 t 的剩余时间（负值表示 t 是过去时间）

```go
func untilExample() {
    deadline := time.Now().Add(30 * time.Second)
    
    // ✅ 定期检查剩余时间
    for {
        remaining := time.Until(deadline)
        if remaining <= 0 {
            fmt.Println("\n时间到!")
            break
        }
        
        fmt.Printf("\r剩余时间: %.1f秒", remaining.Seconds())
        time.Sleep(500 * time.Millisecond)
    }
    
    // ✅ 检查过去时间
    pastTime := time.Now().Add(-5 * time.Minute)
    result := time.Until(pastTime)
    fmt.Println("过去时间结果:", result) // 负值
}
/* 输出:
剩余时间: 29.5秒...0.0秒
时间到!
过去时间结果: -5m0s
*/
```
### 3.1.4 func (d Duration) Abs() Duration

**作用​**​: 返回持续时间的绝对值  
​**​返回值​**​:

- `Duration`: 正数表示的时间段

```go
func absExample() {
    d := -5*time.Minute + 30*time.Second
    fmt.Println("原值:", d)
    fmt.Println("绝对值:", d.Abs()) // 4m30s
    
    // ✅ 处理最小负值 (math.MinInt64)
    min := time.Duration(math.MinInt64)
    fmt.Printf("最小负值: %d纳秒 -> %d纳秒\n", 
               min.Nanoseconds(), min.Abs().Nanoseconds())
}
/* 输出:
原值: -4m30s
绝对值: 4m30s
最小负值: -9223372036854775808纳秒 -> 9223372036854775807纳秒
*/
```
### 3.1.5 单位转换方法集

​**​作用​**​: 转换时间到各种单位  
​**​返回值​**​:

|方法名|返回类型|说明|
|---|---|---|
|`Hours()`|float64|小时数|
|`Minutes()`|float64|分钟数|
|`Seconds()`|float64|秒数|
|`Milliseconds()`|int64|毫秒数|
|`Microseconds()`|int64|微秒数|
|`Nanoseconds()`|int64|纳秒数|
```go
func conversionExample() {
    d := 3*time.Hour + 30*time.Minute + 45*time.Second + 123*time.Millisecond
    
    fmt.Printf("原始值: %v\n", d)
    fmt.Printf("小时: %.3f\n", d.Hours())
    fmt.Printf("分钟: %.3f\n", d.Minutes())
    fmt.Printf("秒: %.3f\n", d.Seconds())
    fmt.Printf("毫秒: %d\n", d.Milliseconds())
    fmt.Printf("微秒: %d\n", d.Microseconds())
    fmt.Printf("纳秒: %d\n", d.Nanoseconds())
    
    // ⚠️ 整数溢出风险
    max := time.Duration(math.MaxInt64)
    fmt.Printf("\n最大值毫秒: %d (可能溢出? %t)\n", 
               max.Milliseconds(), max.Milliseconds() < 0)
}
/* 输出:
原始值: 3h30m45.123s
小时: 3.512
分钟: 210.752
秒: 12645.123
毫秒: 12645123
微秒: 12645123000
纳秒: 12645123000000

最大值毫秒: 9223372036854775 (可能溢出? false)
*/
```
### 3.1.6 func (d Duration) Round(m Duration) Duration

​**​作用​**​: 四舍五入到指定单位  
​**​参数​**​:

- `m Duration`: 基准时间单位（必须 > 0）  
    ​**​返回值​**​:
- `Duration`: 四舍五入后的时间

```go
func roundExample() {
    d := 123 * time.Millisecond
    fmt.Println("原始值:", d)
    
    // ✅ 基准为50毫秒
    rounded := d.Round(50 * time.Millisecond)
    fmt.Println("Round(50ms):", rounded) // 100ms
    
    // ✅ 基准为20毫秒
    fmt.Println("Round(20ms):", d.Round(20*time.Millisecond)) // 120ms
    
    // ❌ 零值会panic
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("❌ 捕获panic:", r) // "rounding to 0")
        }
    }()
    _ = d.Round(0)
}
/* 输出:
原始值: 123ms
Round(50ms): 100ms
Round(20ms): 120ms
❌ 捕获panic: time: bad rounding for 123ms
*/
```
### 3.1.7 func (d Duration) Truncate(m Duration) Duration

​**​作用​**​: 舍去小于基准单位的时间  
​**​参数​**​:

- `m Duration`: 基准时间单位（必须 > 0）  
    ​**​返回值​**​:
- `Duration`: 截断后的时间

```go
func truncateExample() {
    d := 123*time.Millisecond + 456*time.Microsecond
    fmt.Println("原始值:", d) // 123.456ms
    
    // ✅ 截断到毫秒
    truncated := d.Truncate(time.Millisecond)
    fmt.Println("Truncate(1ms):", truncated) // 123ms
    
    // ✅ 截断到10毫秒
    fmt.Println("Truncate(10ms):", d.Truncate(10*time.Millisecond)) // 120ms
    
    // ✅ 处理负值
    negative := -1250 * time.Millisecond
    fmt.Println("负值截断:", negative.Truncate(100*time.Millisecond)) // -1200ms
    
    // ✅ 边界情况（整除）
    exact := 150 * time.Millisecond
    fmt.Println("整除处理:", exact.Truncate(50*time.Millisecond)) // 150ms
}
/* 输出:
原始值: 123.456ms
Truncate(1ms): 123ms
Truncate(10ms): 120ms
负值截断: -1.2s
整除处理: 150ms
*/
```
### 3.1.8 func (d Duration) String() string

​**​作用​**​: 生成时间段的字符串表示  
​**​返回值​**​:

- `string`: 人性化的时间描述

```go
func stringExample() {
    tests := []time.Duration{
        0,
        123456 * time.Nanosecond,
        15 * time.Second,
        5 * time.Minute,
        3*time.Hour + 45*time.Minute,
        -10*time.Minute + 30*time.Second,
    }
    
    for _, d := range tests {
        fmt.Printf("%20s: %s\n", 
                   fmt.Sprint(d.Nanoseconds(), "ns"), 
                   d.String())
    }
}
/* 输出:
                  0ns: 0s
            123456ns: 123.456µs
         15000000000ns: 15s
        300000000000ns: 5m0s
     13500000000000ns: 3h45m0s
     -570000000000ns: -9m30s
*/
```
## 3.2 Location类型

`time.Location` 是 Go 语言中表示时区的核心类型

**作用​**​：

- 表示特定地理位置的时区信息
- 存储 UTC 偏移量和夏令时规则
- 支持不同时区的时间转换
### 3.2.1 func FixedZone(name string, offset int) \*Location

​**​作用​**​：创建固定偏移量的时区  
​**​参数​**​：

- `name string`：时区名称（自定义）
- `offset int`：UTC 偏移秒数（正东负西）  
    ​**​返回值​**​：`*Location`（固定偏移时区）  
    ​**​注意事项​**​：
- 不支持夏令时
- 名称仅用于标识，不影响功能
- 偏移量必须有效：-86400 < offset < 86400

```go
func fixedZoneExample() {
    // ✅ 有效时区
    shanghai := time.FixedZone("CST", 8 * 3600) // UTC+8
    t := time.Date(2025, 6, 6, 12, 0, 0, 0, shanghai)
    fmt.Println("上海时间:", t.UTC().Format(time.RFC3339)) // 2025-06-06T04:00:00Z
    
    // ⚠️ 无效偏移量（自动修正）
    invalidZone := time.FixedZone("BROKEN", 90000) 
    t = time.Now().In(invalidZone)
    fmt.Println("修正后偏移:", t.Format("-0700")) // +2359
    
    // ❌ 不支持夏令时
    summerTime := time.Date(2025, 7, 1, 12, 0, 0, 0, shanghai)
    winterTime := time.Date(2025, 12, 1, 12, 0, 0, 0, shanghai)
    fmt.Println("夏令时检测:", summerTime == winterTime) // true
}
/* 输出:
上海时间: 2025-06-06T04:00:00Z
修正后偏移: +2359
夏令时检测: true
*/
```
### 3.2.2 func LoadLocation(name string) (\*Location, error)

​**​作用​**​：加载系统时区数据库  
​**​参数​**​：

- `name string`：时区名称（如 "Asia/Shanghai"）  
    ​**​返回值​**​：
- `*Location`：加载的时区
- `error`：加载失败信息  
    ​**​错误情况​**​：
- `time: unknown time zone Asia/XXXXX`（名称错误）
- 找不到系统时区数据库（常见于容器环境）
- 数据库格式损坏（概率极低）

```go
func loadLocationExample() {
    // ✅ 标准时区
    loc, err := time.LoadLocation("America/New_York")
    if err != nil {
        panic(err)
    }
    fmt.Println("纽约时区:", loc.String())
    
    // ✅ 特殊名称
    utcLoc, _ := time.LoadLocation("UTC") // 正确
    localLoc, _ := time.LoadLocation("Local") // 系统本地时区
    
    // ❌ 错误名称
    _, err = time.LoadLocation("Asia/Beijing") // 正确名称是 Asia/Shanghai
    fmt.Println("错误时区结果:", err)
    
    // 🚨 环境问题 (容器)
    _, err = time.LoadLocation("Europe/Paris")
    if err != nil {
        fmt.Println("解决方案: 安装 tzdata 包")
        // Dockerfile 添加: RUN apk add --no-cache tzdata
    }
}
/* 输出:
纽约时区: EST
错误时区结果: unknown time zone Asia/Beijing
*/
```
### 3.2.3 func LoadLocationFromTZData(name string, data \[\]byte) (\*Location, error)

​**​作用​**​：从原始数据加载时区  
​**​参数​**​：

- `name string`：时区名称
- `data []byte`：IANA 时区数据库内容  
    ​**​返回值​**​：
- `*Location`：加载的时区
- `error`：数据无效时报错  
    ​**​注意事项​**​：
- 主要用于嵌入式系统或无 OS 时区场景
- 数据需是完整的时区文件内容
- 性能低于 `LoadLocation`

```go
func loadFromTZDataExample() {
    // ✅ 使用嵌入式数据
    tzData := loadTZData("Asia/Tokyo") // 假想函数获取数据
    tokyoLoc, err := time.LoadLocationFromTZData("JST", tzData)
    if err != nil {
        panic(err)
    }
    
    // 验证功能
    t := time.Now().In(tokyoLoc)
    fmt.Println("东京时间:", t.Format(time.RFC1123Z))
    
    // ❌ 无效数据
    _, err = time.LoadLocationFromTZData("BAD", []byte{0, 1, 2})
    fmt.Println("损坏数据结果:", err)
    
    // 💡 最佳实践：全局缓存
    var cachedLoc *time.Location
    func init() {
        data, _ := os.ReadFile("/usr/share/zoneinfo/Asia/Dubai")
        cachedLoc, _ = time.LoadLocationFromTZData("Dubai", data)
    }
}
```
### 3.2.4 func (l \*Location) String() string

​**​作用​**​：获取时区名称  
​**​返回值​**​：

- `string`：创建时指定的名称

```go
func locationStringExample() {
    utc := time.UTC
    fmt.Println("UTC时区名称:", utc.String()) // UTC
    
    fixed := time.FixedZone("MYZONE", 3 * 3600)
    fmt.Println("自定义时区:", fixed.String()) // MYZONE
    
    loaded, _ := time.LoadLocation("Europe/London")
    fmt.Println("伦敦时区:", loaded.String()) // Europe/London
}
```
## 3.3 Month类型

`Month` 类型用于表示月份，这是一个强类型定义，可以安全处理月份相关操作。

```go
type Month int
```

**特点​**​:

- 实际存储为整数（1-12）
- 定义有命名常量提高可读性
- 内置字符串转换方法

- **月份常量**

```go
const (
    January Month = 1 + iota
    February
    March
    April
    May
    June
    July
    August
    September
    October
    November
    December
)
```
### 3.3.1 func (m Month) String() string

​**​作用​**​：将月份数字转换为对应的英文名称  
​**​返回值​**​：月份的英文全名（从 "January" 到 "December"）  
​**​无效月份处理​**​：

- 有效范围 1-12（January=1 到 December=12）
- 超出范围返回格式为 "Month(N)" 的字符串

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	// 标准使用：通过常量获取月份
	fmt.Println("常量表示:")
	printMonth(time.January)
	printMonth(time.June)
	printMonth(time.December)
	
	// 直接使用整数创建 Month 类型
	fmt.Println("\n整数转换:")
	printMonth(time.Month(1))   // January
	printMonth(time.Month(6))   // June
	printMonth(time.Month(12))  // December
	printMonth(time.Month(13)) // 非法月份
	printMonth(time.Month(0))  // 非法月份
	printMonth(time.Month(-1)) // 非法月份
	
	// 实际应用：日期处理
	fmt.Println("\n实际应用:")
	processDate(time.Date(2025, 6, 15, 0, 0, 0, 0, time.UTC))
}

// 打印月份信息的辅助函数
func printMonth(m time.Month) {
	fmt.Printf("Month(%d): %-9s [类型: %T]\n", 
		m, m.String(), m)
}

// 处理日期的实际应用
func processDate(t time.Time) {
	m := t.Month()
	y := t.Year()
	
	// ✅ 正确方式：直接比较月份常量
	switch m {
	case time.June:
		fmt.Printf("%d年%s是夏季\n", y, m.String())
	case time.January:
		fmt.Printf("%d年%s是冬季\n", y, m.String())
	default:
		fmt.Printf("%d年%s是过渡季节\n", y, m)
	}
	
	// 🚫 错误做法：混淆数字与月份类型
	fmt.Println("月份作为整数使用:", int(m))
	
	// ✅ 正确处理季度
	quarter := (m-1)/3 + 1
	fmt.Printf("%d月份是第%d季度\n", m, quarter)
}
```
## 3.4 Weekday类型

`time.Weekday` 是 Go 中表示星期几的类型，提供了强类型支持和便捷的字符串转换功能。

```go
type Weekday int
```

**特性​**​:

- 使用 `0 = Sunday` 到 `6 = Saturday` 的整数值表示
- 提供命名常量增强可读性
- 内置字符串转换方法

- **星期常量**

```go
const (
    Sunday Weekday = iota // 0
    Monday                // 1
    Tuesday               // 2
    Wednesday             // 3
    Thursday              // 4
    Friday                // 5
    Saturday              // 6
)
```

### 3.4.1 func (d Weekday) String() string

​**​作用​**​：将星期数字转换为对应的英文名称  
​**​返回值​**​：星期的英文全名（如 "Sunday"）  
​**​无效值处理​**​：

- 有效范围 0-6（Sunday-Saturday）
- 超出范围返回格式为 "Weekday(N)" 的字符串

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	// 1. 基本用法演示
	fmt.Println("=== 基本用法 ===")
	printWeekday(time.Sunday)
	printWeekday(time.Wednesday)
	printWeekday(time.Saturday)
}

// 辅助函数：打印星期信息
func printWeekday(d time.Weekday) {
	fmt.Printf("Weekday(%d): %-9s [类型: %T]\n", 
		d, d.String(), d)
}
```
## 3.5 Ticker类型

`time.Ticker` 是 Go 语言中处理周期性任务的精妙工具。

```go
type Ticker struct {
    C <-chan Time // 接收时间事件的通道
    // 包含其他未导出字段
}
```

**核心特性​**​：

- 在指定时间间隔生成时间事件的计时器
- 通过通道 `C` 发送时间值
- ​**​单缓冲通道​**​：每次只缓冲一个事件
- 精确度受系统时间精度限制（通常 1-10ms）
### 3.5.1 func NewTicker(d Duration) \*Ticker

- 功能：构造Ticker结构体
- 参数：d Duration：触发间隔时间 ​**​必须 > 0​**
- 返回值：初始化后的定时器指针
- **错误**
    -  当 `d <= 0` 时触发 ​**​panic​**​（程序崩溃）

```go
func basicTicker() {
    // ✅ 创建1秒间隔的定时器
    ticker := time.NewTicker(1 * time.Second)
    defer ticker.Stop() // 关键！确保资源释放
    
    timeout := time.After(5 * time.Second) // 5秒后停止
    
    for {
        select {
        case t := <-ticker.C:
            fmt.Printf("定时触发: %s\n", t.Format("15:04:05"))
        case <-timeout:
            fmt.Println("5秒计时结束")
            return
        }
    }
}
```
### 3.5.2 func (t \*Ticker) Reset(d Duration)

- 功能：重置定时器
- 参数：新的触发间隔 ​​必须 > 0​​
- **注意事项**
    - 重置前​**​必须​**​保证 `t != nil`
    - ​**​禁止​**​在已停止的 Ticker 上调用 Reset（导致 panic）
    - 重置后立即生效，但​**​不会清空​**​已有事件

```go
func adjustableTicker() {
    ticker := time.NewTicker(500 * time.Millisecond)
    defer ticker.Stop()
    
    // 初始快速状态 (500ms)
    fastPhase := true
    phaseEnd := time.Now().Add(3 * time.Second)
    
    for {
        select {
        case t := <-ticker.C:
            fmt.Printf("触发: %s\n", t.Format("05.000"))
            
            // 3秒后切换为慢速模式
            if fastPhase && time.Now().After(phaseEnd) {
                fmt.Println("=== 切换到慢速模式 ===")
                ticker.Reset(1500 * time.Millisecond)
                fastPhase = false
                phaseEnd = time.Now().Add(5 * time.Second)
            }
            
            // 慢速模式持续时间检查
            if !fastPhase && time.Now().After(phaseEnd) {
                fmt.Println("=== 结束 ===")
                return
            }
        }
    }
}
```
### 3.5.3 func (t \*Ticker) Stop()

 **行为特性**

- 停止 Ticker 并释放相关资源
- ​**​不会关闭​**​通道 `C`
- 停止后继续读取 `C` 会阻塞
- 支持多次调用（安全无副作用）

```go
// ✅ 正确使用（defer保证停止）
ticker := time.NewTicker(interval)
defer ticker.Stop() // 关键语句

// 🚫 错误：忘记停止会导致goroutine泄露
func leakyTicker() {
    ticker := time.NewTicker(time.Second)
    // 没有调用 Stop()，定时器会一直存在
}
```
## 3.6 Timer类型

`time.Timer` 是 Go 语言中处理单次延时任务的强大工具，提供了精确的时间控制和丰富的操作选项。

```go
type Timer struct {
    C <-chan Time // 接收时间事件的通道
    // 包含其他未导出字段
}
```

**核心特性​**​：

- 用于表示单个定时事件的计时器
- 一旦触发后通道只发送一次时间值
- 可在触发前被停止或重置
- ​**​停止后通道不会被关闭​**

### 3.6.1 func NewTimer(d Duration) \*Timer

- **作用​**​：创建新的计时器，在指定时间后发送当前时间到通道 `C`
- **参数**：等待时间 ​**​必须 ≥ 0​**
- **返回值**：初始化后的计时器指针

**注意事项​**​：

- `d = 0` 时计时器会立即准备好（但需读取通道）
- 创建后应立即处理资源释放（推荐 `defer`）

```go
func basicTimer() {
    // ✅ 创建2秒后触发的计时器
    timer := time.NewTimer(2 * time.Second)
    defer timer.Stop() // 确保资源释放
    
    fmt.Println("启动时间:", time.Now().Format("15:04:05.000"))
    
    // 等待计时器触发
    t := <-timer.C
    fmt.Printf("触发时间: %s\n", t.Format("15:04:05.000"))
}
```
### 3.6.2 func AfterFunc(d Duration, f func()) \*Timer

- **作用​**​：在指定时间后在单独 goroutine 中执行函数
- **参数**：
    - 等待时间 ​**​必须 ≥ 0​**
    - 到期后执行的函数
- **返回值**：计时器指针（可用于提前停止）

**注意事项​**​：

- 执行环境在单独的 goroutine 中
- 函数执行不阻塞原调用链
- `d = 0` 时函数会立即在新 goroutine 中执行

```go
func timerWithCallback() {
    fmt.Println("开始时间:", time.Now().Format("05.000"))
    
    // ✅ 带回调的计时器
    timer := time.AfterFunc(1500*time.Millisecond, func() {
        fmt.Printf("回调执行: %s (在 goroutine %d)\n",
            time.Now().Format("05.000"), runtime.NumGoroutine())
    })
    
    // 提前停止 (0.5秒后)
    time.Sleep(500 * time.Millisecond)
    stopped := timer.Stop()
    if stopped {
        fmt.Println("1.5秒定时已取消!")
    } else {
        fmt.Println("定时器已触发，无法取消")
    }
    
    // 确保主goroutine等待完成
    time.Sleep(2 * time.Second)
}
```
### 3.6.3 func (t \*Timer) Reset(d Duration) bool

- **作用​**​：重新设置计时器的到期时间
- **参数**：新的等待时间 ​​必须 ≥ 0​​
- **返回值**：是否重置成功（`true`=重置时计时器未触发）

**关键规则​**​：

1. 当计时器已触发或已停止时，返回 `false`
2. 当计时器未触发时，返回 `true`
3. 对于已触发的计时器，需​**​先处理通道值​**​再重置：

```go
if !t.Stop() {
    <-t.C // 清空通道
}
t.Reset(newDuration)
```

### 3.6.4 func (t \*Timer) Stop() bool

- **作用​**​：阻止计时器触发并释放资源
- **返回值**：是否成功停止（`true`=成功阻止触发）

**关键规则​**​：

1. 停止已触发的计时器返回 `false`
2. 停止已停止的计时器返回 `false`
3. 停止后通道不会被关闭（未读取会阻塞）
4. 停止成功后通道中不会有值发送

```go
func stopBehavior() {
    timer := time.NewTimer(2 * time.Second)
    
    // 方案1: 同步停止
    go func() {
        time.Sleep(500 * time.Millisecond)
        if stopped := timer.Stop(); stopped {
            fmt.Println("定时器成功停止")
        }
    }()
    
    select {
    case t := <-timer.C:
        fmt.Println("定时器触发:", t.Format("05.000"))
    case <-time.After(3 * time.Second):
        fmt.Println("定时器未触发")
    }
    
    // 方案2: 停止后尝试读取通道
    timer2 := time.NewTimer(100 * time.Millisecond)
    time.Sleep(50 * time.Millisecond)
    if timer2.Stop() {
        fmt.Println("计时器提前停止")
        // 读取通道防止后续操作阻塞
        select {
        case <-timer2.C: // 不阻塞的读取尝试
        default:
        }
    }
    
    // 尝试重置（需要通道已清空）
    valid := timer2.Reset(500 * time.Millisecond)
    fmt.Println("重置有效:", valid) // true
}
```
## 3.7 Time类型

`time.Time`是Go语言时间处理的核心类型，用于表示一个精确到纳秒的时间点。

```go
type Time struct {
    // wall 和 ext 共同表示时间戳
    wall uint64  // 存储秒级和纳秒部分
    ext  int64   // 存储时区信息和闰秒
    
    // loc 表示时区
    loc *Location
}

```

### 3.7.1 func Date(year int, month Month, day, hour, min, sec, nsec int, loc \*Location) Time

​**​作用​**​：手动创建具体时间  
​**​参数​**​：

- `year`：年份（负数表示公元前）
- `month`：月份（可使用 `time.January` 等常量）
- `day`：日（1-31）
- `hour`：小时（0-23）
- `min`：分钟（0-59）
- `sec`：秒（0-59）
- `nsec`：纳秒（0-999999999）
- `loc`：时区（`time.UTC`、`time.Local` 或自定义）

​**​返回值​**​：构造的时间对象  
​**​错误情况​**​：

- 月份不合法（<1或>12）
- 日期超出月份范围
- 时间分量超出范围

```go
func createDate() {
    // ✅ 正确创建 (2025年6月6日 UTC时间)
    t := time.Date(2025, time.June, 6, 15, 30, 45, 123456789, time.UTC)
    fmt.Printf("创建时间: %s\n", t.Format(time.RFC3339Nano))
    
    // ⚠️ 闰年处理 (2024年2月29日合法)
    leap := time.Date(2024, time.February, 29, 12, 0, 0, 0, time.UTC)
    fmt.Println("闰年日期:", leap.IsDST())
    
    // ❌ 错误参数 (13月32日)
    t2 := time.Date(2025, 13, 32, 25, 70, 90, 0, time.UTC)
    fmt.Println("错误日期:", t2) // 自动规范化: 2026-02-01 02:10:30...
    
    // ✅ 公元前时间
    bc := time.Date(-100, time.January, 1, 0, 0, 0, 0, time.UTC)
    fmt.Println("公元前日期:", bc.Year(), bc.Month())
}
```
### 3.7.2 func Now() Time

​**​作用​**​：获取当前时间（高精度）  
​**​特点​**​：

- 包含单调时钟（用于时间计算）
- 时区为本地时区

```go
func captureNow() {
    // ✅ 获取当前时间
    now := time.Now()
    fmt.Printf("当前时间: %s\n", now.Format("2006-01-02 15:04:05.999"))
    
    // ✅ 计算程序耗时
    start := time.Now()
    time.Sleep(250 * time.Millisecond)
    elapsed := time.Since(start)
    fmt.Printf("实际耗时: %.2fms\n", float64(elapsed)/float64(time.Millisecond))
}
```
### 3.7.3 func Parse(layout, value string) (Time, error)

​**​作用​**​：按照布局解析时间字符串（默认UTC）  
​**​参数​**​：

- `layout`：时间格式（使用参考时间定义）
- `value`：要解析的时间字符串

​**​返回值​**​：

- `Time`：解析成功的时间对象
- `error`：格式不匹配时返回错误

​**​常见错误​**​：

- `parsing time ...: extra text`（有多余字符）
- `parsing time ...: month out of range`
- `parsing time ...: unknown time zone ...`

```go
func parseTime() {
    // ✅ 标准解析 (RFC3339格式)
    t1, err := time.Parse(time.RFC3339, "2025-06-06T15:30:45Z")
    if err != nil {
        panic(err)
    }
    fmt.Println("解析时间1:", t1.UTC().Format(time.Stamp))
    
    // ✅ 自定义格式
    t2, err := time.Parse("01/02 2006", "06/06 2025")
    if err == nil {
        fmt.Println("解析时间2:", t2.Format("2006-01-02"))
    }
    
    // ❌ 格式错误 (月份超出范围)
    _, err = time.Parse("2006-13-02", "2025-13-06")
    fmt.Println("月份错误:", err) // parsing time "2025-13-06": month out of range
    
    // ⚠️ 时区问题 (默认UTC)
    t3, _ := time.Parse("2006-01-02 15:04", "2025-06-06 15:30")
    fmt.Println("无时区时间:", t3.Location()) // UTC
}
```
### 3.7.4 func ParseInLocation(layout, value string, loc \*Location) (Time, error)

**作用​**​：在指定时区解析时间  
​**​参数​**​：

- `layout`：时间格式
- `value`：时间字符串
- `loc`：指定时区

​**​与 `Parse` 区别​**​：

- 指定默认时区代替UTC
- 字符串中无时区信息时使用指定时区

```go
func parseWithLocation() {
    loc, _ := time.LoadLocation("Asia/Shanghai")
    
    // ✅ 解析无时区信息时间
    t, err := time.ParseInLocation("2006-01-02 15:04", "2025-06-06 15:30", loc)
    if err != nil {
        panic(err)
    }
    fmt.Printf("上海时间: %s (UTC%+d)\n", 
              t.Format(time.Kitchen), 
              t.UTC().Hour()-t.Hour())
    
    // ⚠️ 解析含时区信息时间 (时区信息优先)
    t2, _ := time.ParseInLocation(time.RFC3339, "2025-06-06T15:30:45-08:00", loc)
    fmt.Println("解析带时区时间:", t2.Location()) // UTC-8
    
    // ❌ 时区未加载
    _, err = time.ParseInLocation(time.RFC1123, "Mon, 06 Jun 2025 15:30:45 EST", nil)
    fmt.Println("时区错误:", err) // time: missing Location in call to ParseInLocation
}
```
### 3.7.5 func Unix(sec int64, nsec int64) Time

​**​作用​**​：从Unix时间戳创建时间  
​**​参数​**​：

- `sec`：从1970-01-01 UTC开始的秒数
- `nsec`：纳秒偏移（0-999999999）

​**​注意​**​：

- 结果时间固定为UTC时区
- `nsec` 超出范围自动进位

```go
func fromUnix() {
    // ✅ 标准时间戳 (2025-06-06 00:00:00 UTC)
    t := time.Unix(1749254400, 0)
    fmt.Println("对应时间:", t.Format("2006-01-02"))
    
    // ✅ 带纳秒的时间戳
    t2 := time.Unix(1749254400, 500_000_000) // +0.5秒
    fmt.Println("带纳秒时间:", t2.Format("15:04:05.999"))
    
    // ⚠️ 大整数处理
    t3 := time.Unix(math.MaxInt64, 0)
    fmt.Println("最大时间:", t3.Year()) // 约292277年
}
```
### 3.7.6 func UnixMicro(usec int64) Time

​**​作用​**​：从微秒级时间戳创建  
​**​参数​**​：

- `usec`：从1970-01-01 UTC开始的微秒数
### 3.7.7 func UnixMilli(msec int64) Time

​**​作用​**​：从毫秒级时间戳创建  
​**​参数​**​：

- `msec`：从1970-01-01 UTC开始的毫秒数
### 3.7.8 func (t Time) Add(d Duration) Time

​**​作用​**​：增加指定时间段  
​**​参数​**​：

- `d Duration`：要添加的时间段（支持负值表示减少时间）

​**​返回值​**​：计算后的新时间  
​**​特点​**​：

- 支持纳秒级精度
- 自动处理时区转换
- 自动处理日期边界（如月末进位）

```go
func addExample() {
    t := time.Date(2025, 6, 6, 12, 0, 0, 0, time.UTC)
    fmt.Println("原始时间:", t.Format("2006-01-02 15:04:05 MST"))
    
    // ✅ 增加1小时30分钟
    t1 := t.Add(1*time.Hour + 30*time.Minute)
    fmt.Println("增加1.5小时:", t1.Format("15:04:05"))
    
    // ✅ 减少天数 (支持负值)
    t2 := t.Add(-48 * time.Hour) // 减2天
    fmt.Println("减少2天:", t2.Format("2006-01-02"))
    
    // ⚠️ 月末处理
    t3 := time.Date(2025, 1, 31, 0, 0, 0, 0, time.UTC)
    t4 := t3.Add(24 * time.Hour) // 加1天 (2月1日)
    fmt.Println("1月31日+1天:", t4.Format("2006-01-02"))
}
```
### 3.7.9 func (t Time) AddDate(years int, months int, days int) Time

​**​作用​**​：增加年月日分量  
​**​参数​**​：

- `years`：年数
- `months`：月数
- `days`：天数

​**​返回值​**​：计算后的新时间  
​**​特点​**​：

- 智能处理月份进位和月末情况
- 时间分量保持不变
- 支持负值减少时间

```go
func addDateExample() {
    base := time.Date(2025, 6, 6, 15, 30, 0, 0, time.UTC)
    fmt.Println("基准时间:", base.Format("2006-01-02 15:04:05"))
    
    // ✅ 增加1年2个月3天
    t1 := base.AddDate(1, 2, 3)
    fmt.Println("加1年2月3天:", t1.Format("2006-01-02"))
    
    // ✅ 减少时间
    t2 := base.AddDate(0, -3, -15) // 减3月15天
    fmt.Println("减3月15天:", t2.Format("2006-01-02"))
    
    // ⚠️ 特殊月末处理 (2月29日)
    leap := time.Date(2024, 2, 29, 0, 0, 0, 0, time.UTC)
    t3 := leap.AddDate(1, 0, 0) // 加1年 (非闰年)
    fmt.Println("2024闰年+1年:", t3.Format("2006-01-02")) // 2025-03-01
    
    // ❌ 边界测试
    maxTime := time.Unix(1<<63-62135596801, 999999999)
    fmt.Println("最大时间加1天:", maxTime.AddDate(0,0,1).IsZero()) // 返回零值
}
```
### 3.7.10 func (t Time) Sub(u Time) Duration

​**​作用​**​：计算两个时间的差值  
​**​参数​**​：

- `u Time`：要减去的时间

​**​返回值​**​：时间段差值 `(t - u)`  
​**​特点​**​：

- 返回负值表示 `t < u`
- 高精度（纳秒级）
- 考虑单调时钟（精度更高）

```go
func subExample() {
    start := time.Date(2025, 6, 6, 9, 0, 0, 0, time.UTC)
    end := time.Date(2025, 6, 6, 10, 30, 45, 123456789, time.UTC)
    
    // ✅ 计算时间差
    diff := end.Sub(start)
    fmt.Printf("时间差: %v (%.3f小时)\n", 
               diff, diff.Hours())
    
    // ✅ 负值示例
    negDiff := start.Sub(end)
    fmt.Println("负差值:", negDiff > 0) // false
    
    // ⚠️ 时区处理
    loc, _ := time.LoadLocation("Asia/Shanghai")
    shanghaiTime := start.In(loc)
    fmt.Printf("UTC时间: %s\n", start.UTC().Format(time.Kitchen))
    fmt.Printf("上海时间: %s\n", shanghaiTime.Format(time.Kitchen))
    fmt.Println("带时区差值:", end.Sub(shanghaiTime))
}
```
### 3.7.11 func (t Time) Round(d Duration) Time

​**​作用​**​：四舍五入到指定精度  
​**​参数​**​：

- `d Duration`：时间精度（必须 > 0）

​**​返回值​**​：舍入后的时间  
​**​规则​**​：

- 默认使用单调时钟计时
- 到零点的距离 >= 1/2 精度则进位

```go
func roundExample() {
    t := time.Date(2025, 6, 6, 12, 30, 45, 500_000_000, time.UTC)
    fmt.Println("原始时间:", t.Format("15:04:05.000000000"))
    
    // ✅ 四舍五入到秒
    t1 := t.Round(1 * time.Second)
    fmt.Println("舍入到秒:", t1.Format("15:04:05.000000000")) // 12:30:46
    
    // ✅ 舍入到10分钟
    t2 := t.Round(10 * time.Minute)
    fmt.Println("舍入到10分钟:", t2.Format("15:04:05")) // 12:30:00 (或13:00:00)
    
    // ⚠️ 边界测试 (精确1.5小时)
    t3 := time.Date(2025, 6, 6, 12, 45, 0, 0, time.UTC)
    t4 := t3.Round(90 * time.Minute) // 1.5小时
    fmt.Println("1.5小时精度:", t4.Format("15:04:05")) // 13:00:00
    
    // ❌ 非法参数 (d <= 0)
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("捕获panic:", r) 
        }
    }()
    t.Round(0)
}
```
### 3.7.12 func (t Time) Truncate(d Duration) Time

​**​作用​**​：截断到指定精度  
​**​参数​**​：

- `d Duration`：时间精度（必须 > 0）

​**​返回值​**​：截断后的时间  
​**​特点​**​：

- 简单去除小数部分
- 不会自动进位
- 保持单调时钟

```go
func truncateExample() {
    t := time.Date(2025, 6, 6, 12, 30, 45, 500_000_000, time.UTC)
    fmt.Println("原始时间:", t.Format("15:04:05.000000000"))
    
    // ✅ 截断到分钟
    t1 := t.Truncate(1 * time.Minute)
    fmt.Println("截断到分:", t1.Format("15:04:05.000000000")) // 12:30:00
    
    // ✅ 截断到天
    t2 := t.Truncate(24 * time.Hour)
    fmt.Println("截断到日:", t2.Format("2006-01-02 15:04:05"))
    
    // ⚠️ 月末测试
    feb29 := time.Date(2024, 2, 29, 12, 30, 45, 0, time.UTC)
    t3 := feb29.Truncate(30 * 24 * time.Hour) // 一个月
    fmt.Println("闰年截断:", t3.Format("2006-01-02"))
    
    // ⚠️ 负时区处理
    t4 := time.Date(2025, 6, 6, 0, 0, 0, 0, time.FixedZone("CST", -8 * 3600))
    t5 := t4.Truncate(1 * time.Hour)
    fmt.Println("负时区截断:", t5.Format("15:04:05 Z07:00")) // 00:00:00 CST-08:00
}
```

**Go 语言中的时间比较方法提供精确的时序关系判断，这些方法都使用单调时钟保证精度，即使系统时间发生变化也能保持准确性。**
### 3.7.13 func (t Time) After(u Time) bool

​**​作用​**​：检查时间 `t` 是否在时间 `u` 之后  
​**​返回值​**​：如果 `t > u` 则为 `true`

```go
func afterExample() {
    now := time.Now()
    future := now.Add(1 * time.Hour)
    
    // ✅ 基本比较
    fmt.Printf("现在是否在1小时后之后？%t\n", now.After(future)) // false
    
    // ✅ 时区一致比较
    shanghai := now.In(time.FixedZone("CST", 8 * 3600))
    fmt.Printf("现在是否在上海时间之后？%t\n", now.After(shanghai)) // false
    
    // ⚠️ 单调时钟保护
    t1 := time.Now()
    time.Sleep(100 * time.Millisecond)
    t2 := time.Now()
    fmt.Printf("t2是否在t1之后？%t\n", t2.After(t1)) // true（即使系统时间回拨）
}
```
### 3.7.14 func (t Time) Before(u Time) bool

​**​作用​**​：检查时间 `t` 是否在时间 `u` 之前  
​**​返回值​**​：如果 `t < u` 则为 `true`

```go
func beforeExample() {
    deadline := time.Date(2025, 6, 6, 23, 59, 59, 0, time.UTC)
    
    // ✅ 截至时间检查
    current := time.Now().UTC()
    if current.Before(deadline) {
        fmt.Println("项目仍在有效期内")
    }
    
    // ⚠️ 时区影响
    localTime := current.Local()
    fmt.Printf("UTC时间是否在本地时间之前？%t\n", 
              current.Before(localTime)) // 取决于时区偏移
}
```
### 3.7.15 func (t Time) Equal(u Time) bool

​**​作用​**​：检查两个时间是否相等  
​**​返回值​**​：如果 `t == u` 则为 `true`  
​**​特殊规则​**​：

- 比较时间点的纳秒级精度
- 考虑时区位置（不同时区相同时刻可能不等）
- 考虑单调时钟状态

```go
func equalExample() {
    t1 := time.Date(2025, 6, 6, 12, 0, 0, 0, time.UTC)
    t2 := t1.Add(0) // 完全复制
    
    // ✅ 相同时间和时区
    fmt.Printf("t1等于t2？%t\n", t1.Equal(t2)) // true
    
    // ✅ 不同时区相同时刻
    shanghaiLoc, _ := time.LoadLocation("Asia/Shanghai")
    t3 := t1.In(shanghaiLoc)
    fmt.Printf("UTC等于上海时间？%t\n", t1.Equal(t3)) // true（相同绝对时间）
    
    // ⚠️ 单调时钟影响
    now := time.Now()
    nowCopy := now.Round(0) // 移除单调时钟
    fmt.Printf("带单调时钟是否等于移除后？%t\n", now.Equal(nowCopy)) // true
}
```
### 3.7.16 func (t Time) Compare(u Time) int

​**​作用​**​：三态比较两个时间（Go 1.20+）  
​**​返回值​**​：

- `-1`：如果 `t < u`
- `0`：如果 `t == u`
- `1`：如果 `t > u`

```go
func compareExample() {
    dates := []time.Time{
        time.Date(2025, 1, 1, 0, 0, 0, 0, time.UTC),
        time.Date(2025, 12, 31, 23, 59, 59, 0, time.UTC),
        time.Date(2025, 6, 6, 12, 0, 0, 0, time.UTC),
    }
    
    // ✅ 排序时间
    sort.Slice(dates, func(i, j int) bool {
        return dates[i].Compare(dates[j]) < 0
    })
    
    fmt.Println("排序后日期:")
    for _, d := range dates {
        fmt.Println(d.Format("2006-01-02"))
    }
    
    // ✅ 边界情况
    zeroTime := time.Time{}
    result := zeroTime.Compare(time.Now())
    fmt.Printf("零时间比较结果: %d\n", result) // -1 (零时间小于任何时间)
}
```
### 3.7.17 func (t Time) IsZero() bool

​**​作用​**​：检查时间是否为零值  
​**​零值定义​**​：`time.Time{}` (year=1, month=1, day=1, UTC)

```go
func isZeroExample() {
    var uninitialized time.Time
    initialized := time.Now()
    
    // ✅ 基本检查
    fmt.Printf("未初始化是零值？%t\n", uninitialized.IsZero()) // true
    fmt.Printf("已初始化是零值？%t\n", initialized.IsZero()) // false
    
    // ✅ JSON处理
    data := `{"date": "0001-01-01T00:00:00Z"}`
    var event struct{ Date time.Time }
    json.Unmarshal([]byte(data), &event)
    fmt.Printf("解析的时间是零值？%t\n", event.Date.IsZero()) // true
}
```
### 3.7.18 func (t Time) IsDST() bool

​**​作用​**​：检查时间是否处于夏令时（Daylight Saving Time）  
​**​注意​**​：结果取决于时区规则

```go
func dstExample() {
    nyLoc, _ := time.LoadLocation("America/New_York")
    
    // ✅ 夏令时期间
    summerTime := time.Date(2025, 7, 1, 12, 0, 0, 0, nyLoc)
    fmt.Printf("7月1日纽约是夏令时？%t\n", summerTime.IsDST()) // true
    
    // ✅ 标准时期间
    winterTime := time.Date(2025, 12, 1, 12, 0, 0, 0, nyLoc)
    fmt.Printf("12月1日纽约是夏令时？%t\n", winterTime.IsDST()) // false
    
    // ⚠️ 时区影响
    utcTime := summerTime.UTC()
    fmt.Printf("UTC时间永远不是夏令时？%t\n", utcTime.IsDST()) // true
}
```
### 3.7.19 func (t Time) Date() (year int, month Month, day int)

​**​作用​**​：获取时间的年、月、日  
​**​返回值​**​：

- `year`：年份（负数表示公元前）
- `month`：月份对象（`time.January` 等）
- `day`：月中天数（1-31）

```go
func dateComponents() {
    t := time.Date(2025, time.June, 6, 15, 30, 45, 0, time.UTC)
    
    year, month, day := t.Date()
    fmt.Printf("日期分量: %d年 %s %d日\n", 
              year, month.String(), day)
    
    // 🏆 实用技巧：快速获取日期
    fmt.Printf("标准格式日期: %d-%02d-%02d\n",
              year, month, day) // 2025-06-06
    
    // ⚠️ 公元前日期处理
    bcDate := time.Date(-100, time.January, 1, 0, 0, 0, 0, time.UTC)
    bcYear, _, _ := bcDate.Date()
    fmt.Println("公元前年份:", bcYear) // -100
}
```
### 3.7.20 func (t Time) Clock() (hour, min, sec int)

​**​作用​**​：获取时分秒分量  
​**​返回值​**​：

- `hour`：小时（0-23）
- `min`：分钟（0-59）
- `sec`：秒（0-59）

```go
func clockComponents() {
    t := time.Date(2025, 6, 6, 15, 30, 45, 0, time.UTC)
    
    hour, min, sec := t.Clock()
    fmt.Printf("时间分量: %02d:%02d:%02d\n", hour, min, sec)
    
    // ✅ 实际应用：格式化输出
    amPm := "AM"
    if hour >= 12 {
        amPm = "PM"
        hour -= 12
    }
    if hour == 0 {
        hour = 12
    }
    fmt.Printf("AM/PM格式: %d:%02d %s\n", hour, min, amPm)
}
```
### 3.7.21 各时间分量独立获取​​

|方法|返回值|范围|示例|
|---|---|---|---|
|`Year()`|`int`|年份|`t.Year()` → 2025|
|`Month()`|`Month`|月份对象|`t.Month().String()` → "June"|
|`Day()`|`int`|月中天数|`t.Day()` → 6|
|`Weekday()`|`Weekday`|星期|`t.Weekday().String()` → "Friday"|
|`Hour()`|`int`|小时|`t.Hour()` → 15|
|`Minute()`|`int`|分钟|`t.Minute()` → 30|
|`Second()`|`int`|秒|`t.Second()` → 45|
|`Nanosecond()`|`int`|纳秒|`t.Nanosecond()` → 0|
### 3.7.22 func (t Time) ISOWeek() (year, week int)

​**​作用​**​：获取ISO周数和年份  
​**​规则​**​：

- 每周从周一开始
- 每年第一周包含至少4天

```go
func isoWeekExample() {
    dates := []time.Time{
        time.Date(2025, 1, 1, 0, 0, 0, 0, time.UTC),
        time.Date(2025, 6, 6, 0, 0, 0, 0, time.UTC),
        time.Date(2025, 12, 31, 0, 0, 0, 0, time.UTC),
    }
    
    for _, d := range dates {
        year, week := d.ISOWeek()
        fmt.Printf("%s: ISO %d-W%02d\n",
                  d.Format("2006-01-02"), year, week)
    }
    
    // ⚠️ 边界情况：跨年周
    // 2024-12-30 → 2025-W01
}
```
### 3.7.23 func (t Time) YearDay() int

​**​作用​**​：获取年中天数（1-366）  
​**​闰年​**​：2月29日为第60天
### 3.7.24 func (t Time) Zone() (name string, offset int)

​**​作用​**​：获取时区信息  
​**​返回值​**​：

- `name`：时区缩写（如"CST"、"EST"）
- `offset`：UTC偏移秒数（东正西负）

```go
func zoneInfo() {
    locs := []*time.Location{
        time.UTC,
        time.FixedZone("BJT", 8 * 3600),
        time.FixedZone("NST", -3 * 3600-30 * 60),
    }
    
    for _, loc := range locs {
        t := time.Now().In(loc)
        name, offset := t.Zone()
        fmt.Printf("%15s: %s (UTC%+03d%02d)\n",
                  loc.String(), name,
                  offset/3600, (offset%3600)/60)
    }
    
    // ⚠️ 时区名称限制
    customZone := time.FixedZone("", 12345)
    _, offset := time.Now().In(customZone).Zone()
    fmt.Println("无名称时区偏移:", offset) // 12345
}
```
### 3.7.25 func (t Time) ZoneBounds() (start, end Time)

​**​作用​**​：获取当前时区规则的有效时间范围（Go 1.21+）  
​**​返回值​**​：

- `start`：当前时区规则开始时间
- `end`：当前时区规则结束时间
- 如规则是固定偏移，则 `start = -∞`, `end = +∞`

```go
func zoneBoundsExample() {
    loc, _ := time.LoadLocation("America/New_York")
    t := time.Date(2025, 6, 6, 12, 0, 0, 0, loc)
    
    // ✅ 获取时区有效范围
    start, end := t.ZoneBounds()
    
    fmt.Printf("纽约当前时区规则:\n")
    fmt.Printf("开始时间: %s\n", start.Format(time.RFC3339))
    fmt.Printf("结束时间: %s\n", end.Format(time.RFC3339))
    
    // ⚠️ 无规则变化的时区
    tUTC := time.Now().UTC()
    startUTC, endUTC := tUTC.ZoneBounds()
    fmt.Printf("UTC时区范围: %s - %s\n",
              startUTC, endUTC) // 显示 -inf +inf
}
```
### 3.7.26 func (t Time) Location() \*Location

​**​作用​**​：获取时间关联的时区  
​**​返回值​**​：`*time.Location` 指针  
​**​特性​**​：

- 创建时间对象时设置的时区
- 默认为 UTC（使用 `time.Unix` 创建时）
- 可以来自 `time.Local` 系统本地时区

```go
func locationExample() {
    // ✅ 创建带时区的时间
    shanghaiLoc, _ := time.LoadLocation("Asia/Shanghai")
    t := time.Date(2025, 6, 6, 12, 0, 0, 0, shanghaiLoc)
    
    // 获取时区
    loc := t.Location()
    fmt.Printf("时区名称: %s\n", loc.String())
    
    // ⚠️ 时区转换影响
    tUTC := t.UTC()
    fmt.Printf("转换后时区: %s\n", tUTC.Location()) // UTC
    
    // ✅ 检查时区类型
    if loc == time.Local {
        fmt.Println("系统本地时区")
    } else if loc == time.UTC {
        fmt.Println("UTC时区")
    } else {
        fmt.Println("自定义时区")
    }
}
```
### 3.7.27 func (t Time) In(loc *Location) Time

​**​作用​**​：将时间转换为指定时区的时间  
​**​参数​**​：

- `loc *Location`：目标时区对象  
    ​**​返回值​**​：转换后的时间（相同时间点的新表示）  
    ​**​注意事项​**​：
- 传入 nil 会导致 panic
- 转换精度到纳秒（不损失精度）

```go
func inExample() {
    // 创建基础时间 (UTC)
    utcTime := time.Date(2025, 6, 6, 12, 0, 0, 0, time.UTC)
    
    // ✅ 转换为上海时区
    shanghaiLoc, _ := time.LoadLocation("Asia/Shanghai")
    shanghaiTime := utcTime.In(shanghaiLoc)
    fmt.Printf("UTC时间: %s\n", utcTime.Format("2006-01-02 15:04 MST"))
    fmt.Printf("上海时间: %s\n", shanghaiTime.Format("2006-01-02 15:04 MST"))
    
    // ✅ 特殊时区转换 (UTC+0)
    northPole := time.FixedZone("NPX", 0)
    northPoleTime := utcTime.In(northPole)
    fmt.Printf("北极时间: %s\n", northPoleTime.Format("15:04 MST"))
    
    // ⚠️ 危险：nil 时区会导致 panic
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("捕获panic: loc不能为nil")
        }
    }()
    utcTime.In(nil)
}
```
### 3.7.28 func (t Time) Local() Time

​**​作用​**​：将时间转换为系统本地时区的时间  
​**​返回值​**​：本地时区时间  
​**​特性​**​：

- 使用 `time.Local` 系统设置
- 自动处理夏令时

```go
func localExample() {
    // 创建 UTC 时间
    utcTime := time.Date(2025, 6, 6, 12, 0, 0, 0, time.UTC)
    
    // ✅ 转换本地时间
    localTime := utcTime.Local()
    localOffset := time.Since(localTime) - time.Since(utcTime)
    
    fmt.Printf("UTC时间: %s\n", utcTime.Format("2006-01-02 15:04 -0700"))
    fmt.Printf("本地时间: %s (偏移 %.0f小时)\n",
              localTime.Format("2006-01-02 15:04 -0700"),
              localOffset.Hours())
    
    // ✅ 夏令时测试
    loc := time.FixedZone("TestZone", 0)
    t := time.Date(2025, 7, 1, 12, 0, 0, 0, loc)
    fmt.Printf("系统本地夏令时状态: %t\n", t.Local().IsDST())
    
    // 💡 本地时区识别
    name, _ := localTime.Zone()
    fmt.Printf("系统时区: %s\n", name)
}
```
### 3.7.29 func (t Time) UTC() Time

​**​作用​**​：将时间转换为 UTC 时区时间  
​**​返回值​**​：UTC 时区的时间表示  
​**​特点​**​：

- 清除本地时区信息
- 国际数据交换标准格式

**最佳实践建议​**​

- ​**​服务层​**​：始终使用 UTC 时间处理逻辑
- ​**​存储层​**​：所有时间戳用 UTC 存储
- ​**​表示层​**​：在最后一刻转换为本地时间
### 3.7.30 func (t Time) Format(layout string) string

​**​作用​**​：按指定布局格式化时间为字符串  
​**​参数​**​：`layout` - 使用参考时间（`2006-01-02 15:04:05`）的格式  
​**​返回值​**​：格式化后的字符串  
​**​特点​**​：

- 支持自定义时间显示格式
- 不会改变原时间值
- 线程安全

```go
func formatExample() {
    t := time.Date(2025, 6, 6, 15, 30, 45, 123456789, time.UTC)
    
    // ✅ 常用格式
    fmt.Printf("RFC1123: %s\n", t.Format(time.RFC1123))
    fmt.Printf("自定义格式: %s\n", t.Format("2006年01月02日 03:04:05 PM"))
    
    // 🚩 常见错误：忘记时区处理
    fmt.Printf("时区问题: %s\n", t.Format("2006-01-02 15:04:05")) // 显示UTC时间
    
    // 💡 带时区格式化
    shanghaiLoc, _ := time.LoadLocation("Asia/Shanghai")
    fmt.Printf("上海时间: %s\n", 
              t.In(shanghaiLoc).Format("2006-01-02 15:04:05 -0700"))
}
/* 输出:
RFC1123: Fri, 06 Jun 2025 15:30:45 UTC
自定义格式: 2025年06月06日 03:30:45 PM
时区问题: 2025-06-06 15:30:45
上海时间: 2025-06-06 23:30:45 +0800
*/
```
### 3.7.31 func (t Time) AppendFormat(b \[\]byte, layout string) \[\]byte

​**​作用​**​：高效地将时间追加到字节切片  
​**​参数​**​：

- `b`：目标字节切片
- `layout`：格式字符串  
    ​**​返回值​**​：新字节切片  
    ​**​优势​**​：
- 零分配（无临时字符串）
- 比 `Format` + `[]byte()` 快3-5倍

```go
func appendFormatExample() {
    t := time.Now()
    buf := make([]byte, 0, 50) // 预分配容量
    
    // ✅ 高效追加时间
    buf = t.AppendFormat(buf, "2006-01-02")
    buf = append(buf, 'T')
    buf = t.AppendFormat(buf, "15:04:05...)
    
    fmt.Printf("组合结果: %s\n", string(buf))
    
    // ⏱️ 性能对比
    start := time.Now()
    for i := 0; i < 10_000; i++ {
        _ = t.Format(time.RFC3339Nano) // 每次分配
    }
    fmt.Printf("Format: %v\n", time.Since(start))
    
    start = time.Now()
    buf = buf[:0] // 重用缓存
    for i := 0; i < 10_000; i++ {
        buf = t.AppendFormat(buf, time.RFC3339Nano)
        buf = buf[:0] // 清空重用
    }
    fmt.Printf("AppendFormat: %v\n", time.Since(start))
}
/* 输出:
组合结果: 2025-06-06T15:30:45...
Format: 2.356ms
AppendFormat: 0.782ms
*/
```
### 3.7.32 func (t Time) String() string

​**​作用​**​：返回默认格式的字符串表示  
​**​格式​**​：`2006-01-02 15:04:05.999999999 -0700 MST`  
​**​特点​**​：

- 包含时区信息
- 显示单调时钟（当存在时）
- 适合调试日志

```go
func stringMethodExample() {
    t := time.Now()
    fmt.Printf("默认格式: %s\n", t.String())
    // 输出示例: 2025-06-06 15:30:45.123456789 +0800 CST m=+0.000123456
    
    t = t.Round(0) // 移除单调时钟
    fmt.Printf("移除单调时钟后: %s\n", t.String())
    // 输出: 2025-06-06 15:30:45.123456789 +0800 CST
}
```
### 3.7.33 func (t Time) GoString() string

​**​作用​**​：返回 Go 源码格式的时间表示  
​**​格式​**​：类似 `time.Date(2025, 6, 6, 15, 30, 45, 123456789, time.UTC)`  
​**​用途​**​：

- 调试输出
- 测试用例
- 错误消息

```go
func goStringExample() {
    t := time.Date(2025, 6, 6, 15, 30, 45, 123456789, time.UTC)
    fmt.Printf("Go表示: %#v\n", t)
    
    // 💡 用于测试断言
    if t.String() != time.Date(2025, 6, 6, 15, 30, 45, 123456789, time.UTC).String() {
        fmt.Println("时间不相等")
    }
}
```
### 3.7.34 func (t Time) MarshalJSON() (\[\]byte, error)

​**​作用​**​：序列化为 JSON(RFC3339格式)  
​**​格式​**​：`"2025-06-06T15:30:45.123456789Z"`  
​**​规则​**​：

- 纳秒精度
- 时区转换为 UTC
- 始终包含 'Z' 后缀

```go
func jsonMarshalExample() {
    t := time.Date(2025, 6, 6, 15, 30, 45, 123456789, time.UTC)
    
    // ✅ 序列化
    data, err := t.MarshalJSON()
    if err != nil {
        panic(err)
    }
    fmt.Printf("JSON数据: %s\n", data) // "2025-06-06T15:30:45.123456789Z"
    
    // ⚠️ 非UTC时区处理
    shanghaiTime := t.In(time.FixedZone("CST", 8 * 3600))
    data, _ = shanghaiTime.MarshalJSON()
    fmt.Printf("非UTC时区JSON: %s\n", data) // "2025-06-06T07:30:45.123456789Z" (自动转UTC)
}

```
### 3.7.35 func (t \*Time) UnmarshalJSON(data \[\]byte) error

​**​作用​**​：从JSON反序列化(RFC3339)  
​**​支持格式​**​：

- RFC3339
- RFC3339Nano
- Unix时间戳数值（毫秒）

```go
func jsonUnmarshalExample() {
    validJSON := []byte(`"2025-06-06T15:30:45.123456789Z"`)
    invalidJSON := []byte(`"2025-06-06 15:30:45"`) // 无效分隔符
    
    // ✅ 正常解析
    var t time.Time
    if err := t.UnmarshalJSON(validJSON); err == nil {
        fmt.Printf("解析成功: %s\n", t.Format(time.RFC3339Nano))
    }
    
    // ❌ 错误处理
    if err := t.UnmarshalJSON(invalidJSON); err != nil {
        fmt.Printf("解析失败: %v\n", err)
    }
    
    // ✅ 支持数字时间戳
    ts := time.Now().UnixMilli()
    if err := t.UnmarshalJSON([]byte(fmt.Sprint(ts))); err == nil {
        fmt.Printf("时间戳解析成功: %s\n", t.UTC().Format(time.RFC3339))
    }
}
```
### 3.7.36 func (t Time) MarshalText() (\[\]byte, error)

​**​作用​**​：序列化为 RFC3339 文本  
​**​等同​**​：与 `MarshalJSON` 相同但无引号

```go
func textMarshalExample() {
    t := time.Now()
    data, _ := t.MarshalText()
    fmt.Printf("文本序列化: %s\n", data) // 2025-06-06T15:30:45.123456789Z
}
```
### 3.7.37 func (t \*Time) UnmarshalText(data \[\]byte) error

​**​作用​**​：从 RFC3339 文本反序列化  
​**​同​**​：与 `UnmarshalJSON` 逻辑一致

```go
func textUnmarshalExample() {
    data := []byte("2025-06-06T15:30:45.123456789+08:00")
    var t time.Time
    if err := t.UnmarshalText(data); err == nil {
        fmt.Printf("解析成功: %s\n", t.Location())
    }
}
```