Prometheus 的 `client_golang` 库中的 `prometheus` 包是用于实现监控指标定义、注册和暴露的核心模块。以下是其主要作用及常用函数的详细说明：

> ​**​主要作用​**​

1. ​**​指标类型定义​**​  
    提供四大基础监控指标类型，满足不同监控场景需求：
    
    - ​**​Counter（计数器）​**​：用于累计数值（如请求数、错误数），只增不减。
    - ​**​Gauge（仪表盘）​**​：表示瞬时值，可增可减（如内存使用量、并发连接数）。
    - ​**​Histogram（直方图）​**​：统计样本分布（如请求延迟），支持分桶计数。
    - ​**​Summary（摘要）​**​：提供分位数计算（如 P99 延迟），适合单机统计。
2. ​**​标签管理​**​  
    通过 `*Vec` 类型（如 `CounterVec`）支持多维度标签，实现灵活的数据分类。例如，按 HTTP 方法和状态码分类请求数。
    
3. ​**​注册中心（Registry）​**​  
    管理指标的注册与生命周期，支持全局注册表（`DefaultRegisterer`）和自定义注册表，避免指标重复注册。
    
4. ​**​自定义收集器（Collector）​**​  
    允许用户实现自定义指标采集逻辑，适用于集成第三方系统或复杂指标生成场景。
# 常量

> Summary

```go
const (
    DefMaxAge     = 10 * time.Minute  // 观测数据的默认有效期（10分钟）
    DefAgeBuckets = 5                 // 计算数据年龄的默认分桶数
    DefBufCap     = 500               // 收集观测值的默认缓冲区容量
)
```

- ​**​用途​**​：  
    这些常量用于配置 `Summary` 类型（摘要指标）的行为：
    
    - `DefMaxAge`：观测数据在内存中的保留时间，超过此时间的数据会被滚动淘汰。
    - `DefAgeBuckets`：用于按时间窗口分桶，计算观测数据的年龄分布（类似滑动窗口）。
    - `DefBufCap`：缓冲区大小，用于临时存储观测值，直到分位数计算完成。
- ​**​设计意图​**​：  
    平衡内存占用与计算精度。例如：
    
    - `DefMaxAge=10分钟` 表示只关注最近 10 分钟的数据分布。
    - `DefBufCap=500` 限制内存使用，防止高并发场景下的 OOM。

> Histogram

```go
const (
    DefNativeHistogramZeroThreshold = 2.938735877055719e-39  // 默认零值阈值（2^-128）
    NativeHistogramZeroThresholdZero = -1                    // 零宽度零值桶的特殊标记
)
```

- ​**​用途​**​：  
    配置直方图（`Histogram`）中“零值桶”的行为：
    
    - `DefNativeHistogramZeroThreshold`：默认零值阈值为 `2^-128`，用于定义“近似零值”的边界。所有绝对值小于此阈值的观测值会被归类到零值桶（`le=0`）。
    - `NativeHistogramZeroThresholdZero=-1`：表示创建一个“严格零值桶”，仅接收精确为零的观测值（如 `0`，而非 `0.0000001`）。
- ​**​设计意图​**​：
    
    - 通过 `2^-128` 确保零值桶在不同分辨率下的一致性（兼容 IEEE 754 浮点标准）。
    - 允许用户通过 `NativeHistogramZeroThresholdZero` 严格区分零与非零值（如统计零错误请求）。

> 标签

```go
const ExemplarMaxRunes = 128  // 示例标签的最大字符数（128个字符）
```

- ​**​用途​**​：  
    限制 Exemplar（附加在指标上的诊断信息，如 Trace ID）的标签长度，防止存储过大的标签数据。
    
- ​**​设计意图​**​：  
    在提供调试信息的同时，避免因标签过长导致性能问题。

# 变量

> 全局默认注册器与收集器

```go
var (
    DefaultRegisterer Registerer = defaultRegistry  // 默认指标注册器
    DefaultGatherer   Gatherer   = defaultRegistry   // 默认指标收集器
)
```

- ​**​作用​**​：  
    这两个全局变量用于管理指标的注册（`Registerer`）和收集（`Gatherer`），默认指向同一个 `Registry` 实例（`defaultRegistry`）。
- ​**​预注册的收集器​**​：
    - `defaultRegistry` 默认包含两个收集器：
        1. ​**​进程指标收集器​**​（`NewProcessCollector`，仅 Linux 有效）。
        2. ​**​Go 运行时指标收集器​**​（`NewGoCollector`，Go 1.9 之前版本可能引发 STW 停顿）。
- ​**​注意事项​**​：
    - 修改这些全局变量需谨慎，可能影响依赖它们的代码（如 `promhttp.Handler()`）。
    - 若需避免全局状态，应使用自定义的 `Registerer` 和 `Gatherer` 实例。

> 直方图默认分桶

```go
var DefBuckets = []float64{.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10}
```

- ​**​用途​**​：  
    `Histogram` 的默认分桶配置，适用于测量网络服务的响应时间（单位：秒）。
- ​**​设计意图​**​：  
    覆盖从 5 毫秒到 10 秒的典型延迟范围，但实际场景中通常需要自定义分桶（如微服务或高频交易场景）。
- ​**​示例​**​：
    - 若服务 99% 的响应时间 < 100ms，可缩小分桶范围以提高精度：

```go
customBuckets := []float64{.01, .05, .1, .2, .5}
```
# 常用函数

## ​**​指标命名与标签处理​**​

### ​BuildFQName(namespace, subsystem, name string) string`​

- ​**​作用​**​：生成指标的​**​完全限定名称​**​（Fully Qualified Name），格式为 `namespace_subsystem_name`.
- ​**​参数​**​：
    - `namespace`：命名空间（如 `http`）。
    - `subsystem`：子系统（如 `request`）。
    - `name`：指标名（如 `duration_seconds`）。
- ​**​示例​**​：
    
    ```go
    fqName := BuildFQName("http", "request", "duration_seconds")
    // 输出：http_request_duration_seconds
    ```
    
- ​**​注意​**​：若任一参数为空，会自动省略下划线分隔符。

### ​MakeLabelPairs(desc \*Desc, labelValues \[\]string) \[\]*dto.LabelPair​

- ​**​作用​**​：将标签名和值组合成 Protobuf 格式的 `LabelPair` 结构，用于序列化指标数据。
- ​**​参数​**​：
    - `desc`：指标描述符（包含标签名）。
    - `labelValues`：标签值列表（顺序需与 `desc` 中的标签名一致）。
- ​**​典型场景​**​：在自定义 `Collector` 实现中构造指标标签。

## ​**​直方图分桶生成​**​

### ​LinearBuckets(start, width float64, count int) \[\]float64

- ​**​作用​**​：生成​**​线性增长​**​的分桶边界。
- ​**​参数​**​：
    - `start`：第一个桶的上边界。
    - `width`：桶宽（每个桶比前一个增加 `width`）。
    - `count`：桶总数。
- ​**​示例​**​：
    
    ```go
    buckets := LinearBuckets(1, 2, 3) // [1, 3, 5]
    ```
    

### ExponentialBuckets(start, factor float64, count int) \[\]float64​

- ​**​作用​**​：生成​**​指数增长​**​的分桶边界。
- ​**​参数​**​：
    - `start`：第一个桶的上边界。
    - `factor`：增长因子（每个桶是前一个的 `factor` 倍）。
    - `count`：桶总数。
- ​**​示例​**​：
    
    ```go
    buckets := ExponentialBuckets(1, 2, 4) // [1, 2, 4, 8]
    ```
    

### ExponentialBucketsRange(minBucket, maxBucket float64, count int) \[\]float64

- ​**​作用​**​：生成在 `[minBucket, maxBucket]` 范围内​**​指数分布​**​的分桶。
- ​**​参数​**​：
    - `minBucket`：最小桶边界（>0）。
    - `maxBucket`：最大桶边界。
    - `count`：桶总数（≥2）。
- ​**​示例​**​：
    
    ```go
    buckets := ExponentialBucketsRange(0.1, 100, 5) // [0.1, 1, 10, 100]
    ```


## ​**​指标收集器（Collector）管理​**​

### Register(c Collector) error

- ​**​作用​**​：向 `DefaultRegisterer` 注册一个指标收集器。
- ​**​返回值​**​：若收集器已注册或标签冲突，返回错误。
- ​**​示例​**​：

    ```go
    err := Register(myCollector)
    ```


### MustRegister(cs ...Collector)

- ​**​作用​**​：批量注册收集器，若失败则 `panic`。
- ​**​典型用法​**​：在程序初始化时注册全局收集器。
    
    ```go
    MustRegister(cpuCollector, memCollector)
    ```
    

### ​Unregister(c Collector) bool

- ​**​作用​**​：从 `DefaultRegisterer` 注销收集器。
- ​**​返回值​**​：是否成功注销。
- ​**​场景​**​：动态卸载插件或模块的指标。

### ​​DescribeByCollect(c Collector, descs chan<- \*Desc)​​

- ​**​作用​**​：辅助函数，通过调用 `Collect` 方法自动生成指标的 `Desc` 描述。
- ​**​用途​**​：简化自定义 `Collector` 的实现，避免手动定义 `Describe` 方法。
- ​**​示例​**​：
    
    ```go
    func (c *MyCollector) Describe(ch chan<- *Desc) {
      DescribeByCollect(c, ch)
    }
    ```

### ​**​工具函数​**​

### ​NewPidFileFn(pidFilePath string) func() (int, error)

- ​**​作用​**​：生成一个函数，用于读取指定 PID 文件并返回进程 ID。
- ​**​场景​**​：监控守护进程时，确认进程是否存活。
- ​**​示例​**​：
    
    ```go
    pidFn := NewPidFileFn("/var/run/myapp.pid")
    pid, err := pidFn()
    ```
    

### WriteToTextfile(filename string, g Gatherer) error

- ​**​作用​**​：将指标数据写入文本文件，格式符合 Prometheus 的 `textfile` 规范。
- ​**​用途​**​：供 `node_exporter` 的 `textfile` 收集器采集自定义指标。
- ​**​示例​**​：
    
    ```go
    WriteToTextfile("/path/to/metrics.prom", DefaultGatherer)
    ```
# 类型
## Counter

- 类型定义：

```go
type Counter interface {
	Metric
	Collector

	// Inc increments the counter by 1. Use Add to increment it by arbitrary
	// non-negative values.
	Inc()
	// Add adds the given value to the counter. It panics if the value is <
	// 0.
	Add(float64)
}
```


Counter 是一个 Metric，它表示一个只会上升的数值。这意味着它不能用于计算数量也可以减少的项目。统计请求总数、错误数、任务完成数等。

### func NewCounter(opts CounterOpts) Counter

- 作用：根据提供的 `CounterOpt` 创建一个新的Counter。

```go
tasksProcessed := prometheus.NewCounter(prometheus.CounterOpts{
    Name: "task_queue_processed_total",
    Help: "Total tasks processed from the queue",
})
```
## CounterVec

- 类型定义

```go
type CounterVec struct {
    *metricVec // 内部维护 sync.Map，存储标签组合到 Counter 的映射
}```

CounterVec 是一个 Collector，它捆绑了一组 Counter，这些 Counter 都共享相同的 Desc，但其变量标签具有不同的值。如果你想计算按各种维度分区的同一事物（例如，按响应代码和方法分区的 HTTP 请求数量），则使用此方法。使用 NewCounterVec 创建实例。

```go
httpReqs := prometheus.NewCounterVec(
	prometheus.CounterOpts{
		Name: "http_requests_total",
		Help: "How many HTTP requests processed, partitioned by status code and HTTP method.",
	},
	[]string{"code", "method"},
)
prometheus.MustRegister(httpReqs)

httpReqs.WithLabelValues("404", "POST").Add(42)

// If you have to access the same set of labels very frequently, it
// might be good to retrieve the metric only once and keep a handle to
// it. But beware of deletion of that metric, see below!
m := httpReqs.WithLabelValues("200", "GET")
for i := 0; i < 1000000; i++ {
	m.Inc()
}
// Delete a metric from the vector. If you have previously kept a handle
// to that metric (as above), future updates via that handle will go
// unseen (even if you re-create a metric with the same label set
// later).
httpReqs.DeleteLabelValues("200", "GET")
// Same thing with the more verbose Labels syntax.
httpReqs.Delete(prometheus.Labels{"method": "GET", "code": "200"})

// Just for demonstration, let's check the state of the counter vector
// by registering it with a custom registry and then let it collect the
// metrics.
reg := prometheus.NewRegistry()
reg.MustRegister(httpReqs)

metricFamilies, err := reg.Gather()
if err != nil || len(metricFamilies) != 1 {
	panic("unexpected behavior of custom test registry")
}

fmt.Println(toNormalizedJSON(sanitizeMetricFamily(metricFamilies[0])))
```

- **`CounterVec` 内部使用 `metricVec` 结构​**​，通过 `sync.Map` 管理标签组合到 `Counter` 的映射
    
- ​**​标签组合的哈希​**​：每个标签键值对会被编码为唯一的哈希值，用于快速查找对应的 `Counter`。
​
- ​**​`WithLabelValues()` 和 `With()` 方法是线程安全的​**​，但频繁调用可能导致锁竞争。

- ​**​优化建议​**​：预先获取常用标签组合的 `Counter` 对象，避免重复计算哈希。
### func NewCounterVec(opts CounterOpts, labelNames \[\]string) \*CounterVec

- 作用：NewCounterVec 根据提供的 CounterOpt 创建一个新的 CounterVec，并按给定的标签名称进行分区。

```go
counterVec := prometheus.NewCounterVec(
    prometheus.CounterOpts{
        Name: "my_counter_total",
        Help: "Example of a CounterVec",
    },
    []string{"label1", "label2"}, // 标签维度
)
```

### func (v \*CounterVec) WithLabelValues(lvs ...string) Counter

- 作用：按标签值的顺序获取对应的 `Counter`
- 错误处理：在遇到错误时触发panic

```go
myVec.WithLabelValues("404", "GET").Add(42)
```
### func (v \*CounterVec) With(labels Labels) Counter

- 作用：通过 `Labels` 对象指定标签键值对，返回对应的Counter
- 错误处理：在遇到错误时触发panic

```go
myVec.With(prometheus.Labels{"code": "404", "method": "GET"}).Add(42)
```
## Gauge

- 类型定义

```go
type Gauge interface {
	Metric
	Collector

	// Set sets the Gauge to an arbitrary value.
	Set(float64)
	// Inc increments the Gauge by 1. Use Add to increment it by arbitrary
	// values.
	Inc()
	// Dec decrements the Gauge by 1. Use Sub to decrement it by arbitrary
	// values.
	Dec()
	// Add adds the given value to the Gauge. (The value can be negative,
	// resulting in a decrease of the Gauge.)
	Add(float64)
	// Sub subtracts the given value from the Gauge. (The value can be
	// negative, resulting in an increase of the Gauge.)
	Sub(float64)

	// SetToCurrentTime sets the Gauge to the current Unix time in seconds.
	SetToCurrentTime()
}
```

`Gauge` 表示一个可以任意上升和下降的数值。Gauge 通常用于温度或当前内存使用等测量值，但也用于可以上下波动的 “计数”，例如正在运行的 goroutine 的数量。
### func NewGauge(opts GaugeOpts) Gauge

- 作用：根据 `GaugeOpts` 创建一个Gauge对象

```go
// 创建 Gauge 记录内存使用量
memUsage := prometheus.NewGauge(prometheus.GaugeOpts{
    Name: "memory_usage_bytes",
    Help: "Current memory usage in bytes",
})
prometheus.MustRegister(memUsage)

// 更新值（例如定时从系统读取）
memUsage.Set(1024 * 1024) // 设置为 1MB
```

返回的实现针对快速 Set 方法进行了优化。如果可以选择通过 Set 而不是 Inc/Dec/Add/Sub 来管理 Gauge 的值，请选择前者。例如，返回的 Gauge 的 Inc 方法比 NewCounter 返回的 Counter 的 Inc 方法慢。这与仪表和计数器的典型情况相匹配，前者往往是 Set 密集型，后者是 Inc 密集型的。
## GaugeVec

- 类型定义：

```go
type GaugeVec struct {
	*MetricVec
}
```
### func NewGaugeVec(opts GaugeOpts, labelNames \[\]string) \*GaugeVec

- 作用：NewGaugeVec 根据提供的 GaugeOpts 创建一个新的 GaugeVec，并按给定的标签名称进行分区。

```go
// 按节点和资源类型（CPU/Memory）监控使用率
resourceUsage := prometheus.NewGaugeVec(
    prometheus.GaugeOpts{
        Name: "resource_usage_percent",
        Help: "Resource usage by node and type",
    },
    []string{"node", "resource_type"}, 
)

// 更新节点1的 CPU 使用率
resourceUsage.WithLabelValues("node1", "cpu").Set(80.3)
// 更新节点1的内存使用率
resourceUsage.WithLabelValues("node1", "memory").Set(65.7)
```

**WithLabelValue/With方法跟CounterVec类型一致。**
## Histogram

- 类型定义

```go
type Histogram interface {
	Metric
	Collector

	// Observe adds a single observation to the histogram. Observations are
	// usually positive or zero. Negative observations are accepted but
	// prevent current versions of Prometheus from properly detecting
	// counter resets in the sum of observations. (The experimental Native
	// Histograms handle negative observations properly.) See
	// https://prometheus.io/docs/practices/histograms/#count-and-sum-of-observations
	// for details.
	Observe(float64)
}

```

**`Histogram`​**​ 用于记录观测值的分布（如请求延迟、响应大小），并将数据分配到预定义的桶（Buckets）中，支持后续计算分位数（如 P90、P99）。

与 Summary 的 Observe 方法相比，Histogram 的 Observe 方法具有非常低的性能开销。

**Observe方法：**

- 负值可能干扰计数器重置检测（仅影响普通 Histogram，Native Histogram 已修复）。
- 实验性 Native Histograms 需 Prometheus v2.40+ 并启用特性标志。

**​Native Histograms（实验性）​**​
    
- 动态稀疏桶，解决传统 Histogram 需预定义桶的问题。
- 启用方式：在 `HistogramOpts` 中配置 `NativeHistogramBucketFactor`。

```go
import "github.com/prometheus/client_golang/prometheus"

// 创建启用 Native Histogram 的 Histogram
histogram := prometheus.NewHistogram(prometheus.HistogramOpts{
    Name: "http_request_duration_seconds",
    Help: "Request latency distribution with native buckets",
    // 启用 Native Histogram，设置桶的指数增长因子
    NativeHistogramBucketFactor: 1.1, // 桶宽按 1.1 倍指数增长
    NativeHistogramMaxBucketNumber: 100, // 限制最大桶数（可选）
})
```
### func NewHistogram(opts HistogramOpts) Histogram

- 作用：NewHistogram 根据提供的 HistogramOpts 创建新的 Histogram。如果 HistogramOpts 中的存储桶没有严格按递增顺序排列，它会 panic。

```go
import "github.com/prometheus/client_golang/prometheus"

// 定义 Histogram
requestLatency := prometheus.NewHistogram(prometheus.HistogramOpts{
    Name:    "http_request_duration_seconds",
    Help:    "Request latency distribution in seconds",
    Buckets: []float64{0.1, 0.5, 1, 2, 5}, // 自定义桶边界
})

// 注册到默认 Registry
prometheus.MustRegister(requestLatency)

// 记录观测值
requestLatency.Observe(0.7) // 分配到 >=0.5 且 <1 的桶
```

- ​**​常用预设桶​**​：
    
    - `DefBuckets`：默认的指数增长桶（适用于秒级延迟：`[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]`）。
    - `LinearBuckets(start, width float64, count int)`：线性递增桶。
    - `ExponentialBuckets(start, factor float64, count int)`：指数递增桶。
## HistogramVec

- 作用：HistogramVec 是一个 Collector，它捆绑了一组直方图，这些直方图都共享相同的描述，但其变量标签具有不同的值。如果您想对按各种维度分区的同一事物进行计数（例如 HTTP 请求延迟，按状态代码和方法分区），则使用此方法。使用 NewHistogramVec 创建实例。

```go
type HistogramVec struct {
	*MetricVec
}
```
### func NewHistogramVec(opts HistogramOpts, labelNames \[\]string) \*HistogramVec

- 作用：NewHistogramVec 根据提供的 HistogramOpts 创建一个新的 HistogramVec，并按给定的标签名称进行分区。

```go
// 按方法和路径统计延迟
latencyVec := prometheus.NewHistogramVec(
    prometheus.HistogramOpts{
        Name:    "http_request_duration_seconds",
        Buckets: prometheus.DefBuckets,
    },
    []string{"method", "path"},
)

// 记录 GET /api 的延迟
latencyVec.WithLabelValues("GET", "/api").Observe(0.3)
```
## Summary

- **`Summary`​**​ 用于记录观测值的滑动窗口分位数（如 P99 延迟），在​**​客户端实时计算分位数​**​，适合单实例的精确统计。
- ​**​核心特性​**​：
    - 在客户端计算分位数，无需服务端聚合。
    - 适用于需要实时分位数的场景（如监控单服务的接口延迟）。
    - ​**​不支持跨实例聚合​**​（不同实例的分位数无法合并）。

| ​**​特性​**​      | `Summary`    | `Histogram`       |
| --------------- | ------------ | ----------------- |
| ​**​分位数计算位置​**​ | 客户端（实时计算）    | 服务端（通过 PromQL 聚合） |
| ​**​适用场景​**​    | 单实例精确分位数     | 跨实例全局分位数          |
| ​**​资源消耗​**​    | 高（需维护滑动窗口数据） | 低（预分桶，内存固定）       |
| ​**​分位数精度​**​   | 高（实时计算）      | 依赖分桶配置（可能有误差）     |

- 类型定义：

```go
type Summary interface {
	Metric
	Collector

	// Observe adds a single observation to the summary. Observations are
	// usually positive or zero. Negative observations are accepted but
	// prevent current versions of Prometheus from properly detecting
	// counter resets in the sum of observations. See
	// https://prometheus.io/docs/practices/histograms/#count-and-sum-of-observations
	// for details.
	Observe(float64)
}
```
### func NewSummary(opts SummaryOpts) Summary

- 作用：NewSummary 根据提供的 SummaryOpts 创建新的 Summary。

```go
import "github.com/prometheus/client_golang/prometheus"

// 定义 Summary（计算 P50 和 P99 分位数）
requestLatency := prometheus.NewSummary(
    prometheus.SummaryOpts{
        Name: "http_request_duration_seconds",
        Help: "Request latency distribution",
        Objectives: map[float64]float64{
            0.5: 0.05,   // P50，允许 5% 误差
            0.99: 0.001, // P99，允许 0.1% 误差
        },
        MaxAge: 10 * time.Minute, // 滑动窗口时间（默认 10 分钟），内存数据保留时间，超时不参于分位数计算
    },
)

// 注册到默认 Registry
prometheus.MustRegister(requestLatency)

// 记录观测值
requestLatency.Observe(0.3)
```

**MaxAge作用机制：**

1. ​**​滑动窗口模型​**​
    
    - `Summary` 维护一个​**​时间滑动窗口​**​，仅保留最近 `MaxAge` 时间段内的观测数据。
    - 例如，若 `MaxAge: 5 * time.Minute`，则只有过去 5 分钟内的观测值会被保留并用于计算分位数。
2. ​**​数据清理​**​
    
    - 客户端库会​**​周期性检查并清理过期数据​**​（默认每 1 分钟清理一次）。
    - 超过 `MaxAge` 的旧数据会被移除，释放内存。
3. ​**​分位数计算​**​
    
    - 清理后，分位数（如 P99）仅基于窗口内剩余的数据计算。
    - 如果窗口内无数据，分位数指标（如 `quantile="0.99"`）可能暂时消失或显示为 `NaN`。

**注意事项：**

1. ​**​数据清理是渐进的​**​
    
    - 清理操作不是实时触发，而是周期性执行（默认每分钟一次）。
    - 极端情况下，数据可能在过期后最多延迟 1 分钟才被删除。
2. ​**​短 MaxAge 的影响​**​
    
    - 若 `MaxAge` 过短（如 1 分钟），可能导致分位数波动较大（数据样本少）。
    - 适用于需要快速反映最新状态的场景（如实时监控）。
3. ​**​长 MaxAge 的影响​**​
    
    - 若 `MaxAge` 过长（如 1 小时），内存占用会持续增长。
    - 适用于需要长期趋势分析的场景（需权衡资源消耗）。

### SummaryVec

- 作用：SummaryVec 是一个 Collector，它捆绑了一组 Summation，这些 Summaries 都共享相同的 Desc，但其变量标签具有不同的值。如果您想对按各种维度分区的同一事物进行计数（例如 HTTP 请求延迟，按状态代码和方法分区），则使用此方法。使用 NewSummaryVec 创建实例。

```go
type SummaryVec struct {
	*MetricVec
}
```
### func NewSummaryVec(opts SummaryOpts, labelNames \[\]string) \*SummaryVec

- 作用：NewSummaryVec 根据提供的 SummaryOpts 创建一个新的 SummaryVec，并按给定的标签名称进行分区。
- 注意：“quantile”是一个非法的标签名称。如果使用此标签名称，NewSummaryVec 将 panic。

```go
// 按接口统计分位数
latencyByEndpoint := prometheus.NewSummaryVec(
    prometheus.SummaryOpts{
        Name:       "api_request_duration_seconds",
        Help:       "API latency by endpoint",
        Objectives: map[float64]float64{0.99: 0.001},
    },
    []string{"endpoint"}, // 标签维度
)

// 记录观测值
latencyByEndpoint.WithLabelValues("/users").Observe(0.5)
```
### CurryWith(labels Labels) (ObserverVec, error)​

- ​**​作用​**​：​**​部分绑定标签​**​，生成一个预设部分标签的新 `SummaryVec`。
- ​**​参数​**​：`labels Labels`：预设的标签键值对（如 `Labels{"method": "GET"}`）。
- ​**​返回值​**​：
    - `ObserverVec`：新生成的 `SummaryVec`，仅需提供剩余标签。
    - `error`：标签未定义或键不匹配时返回错误。

```go
// 预设 "method=GET"
getSummaryVec, err := summaryVec.CurryWith(prometheus.Labels{"method": "GET"})
if err != nil {
    panic(err)
}
// 后续只需提供 "path"
getSummaryVec.WithLabelValues("/api").Observe(0.3)
```
### MustCurryWith(labels Labels) ObserverVec​

- ​**​作用​**​：与 `CurryWith` 类似，但出错时直接触发 `panic`，简化代码。
- ​**​参数​**​：`labels Labels`：预设的标签键值对。
- ​**​返回值​**​：`ObserverVec`。

```go
// 预设 "method=POST"，若出错则 panic
postSummaryVec := summaryVec.MustCurryWith(prometheus.Labels{"method": "POST"})
postSummaryVec.WithLabelValues("/login").Observe(0.4)
```
### With(labels Labels) Observer

- ​**​作用​**​：通过标签键值对直接获取 `Observer`，​**​不返回错误​**​（若标签无效会触发 `panic`）。
- ​**​参数​**​：`labels Labels`：完整的标签键值对。
- ​**​返回值​**​：`Observer`。

```go
summaryVec.With(prometheus.Labels{
    "method": "DELETE",
    "path":   "/user",
}).Observe(0.1)
```
### WithLabelValues(lvs ...string) Observer​

- ​**​作用​**​：通过标签值列表直接获取 `Observer`，​**​不返回错误​**​（若标签值无效会触发 `panic`）。
- ​**​参数​**​：`lvs ...string`：标签值列表，​**​顺序必须严格匹配定义时的标签顺序​**​。
- ​**​返回值​**​：`Observer`。

```go
// 正确顺序：method, path
summaryVec.WithLabelValues("PUT", "/settings").Observe(0.6)
```

| ​**​方法​**​                 | ​**​核心作用​**​                                  | ​**​错误处理​**​ | ​**​适用场景​**​    |
| -------------------------- | --------------------------------------------- | ------------ | --------------- |
| `NewSummaryVec`            | 创建带标签的 SummaryVec                             | 无            | 初始化多维分位数监控指标    |
| `CurryWith`                | 部分绑定标签                                        | 返回 error     | 减少重复标签配置        |
| `GetMetricWith`            | 安全获取带标签的 Summary                              | 返回 error     | 需要错误处理的动态标签场景   |
| `GetMetricWithLabelValues` | 安全通过标签值获取 Summary                             | 返回 error     | 需要错误处理的固定标签顺序场景 |
| `MustCurryWith`            | 部分绑定标签（简化版）                                   | panic        | 已知标签合法的场景       |
| `With`                     | 直接获取带标签的 Summary。跟GetMetricWith类似             | panic        | 快速操作已知合法的标签键值对  |
| `WithLabelValues`          | 直接通过标签值获取 Summary。跟GetMetricWithLabelValues类似 | panic        | 快速操作已知合法的标签值顺序  |
## Opts

`Opts` 是用于创建各类指标（如 Counter、Gauge、Histogram）的通用配置选项。不同指标类型（如 `CounterOpts`、`GaugeOpts`）本质上是 `Opts` 的别名或扩展。

```go
type Opts struct {
	// Namespace, Subsystem, and Name are components of the fully-qualified
	// name of the Metric (created by joining these components with
	// "_"). Only Name is mandatory, the others merely help structuring the
	// name. Note that the fully-qualified name of the metric must be a
	// valid Prometheus metric name.
	Namespace string
	Subsystem string
	Name      string

	// Help provides information about this metric.
	//
	// Metrics with the same fully-qualified name must have the same Help
	// string.
	Help string

	// ConstLabels are used to attach fixed labels to this metric. Metrics
	// with the same fully-qualified name must have the same label names in
	// their ConstLabels.
	//
	// ConstLabels are only used rarely. In particular, do not use them to
	// attach the same labels to all your metrics. Those use cases are
	// better covered by target labels set by the scraping Prometheus
	// server, or by one specific metric (e.g. a build_info or a
	// machine_role metric). See also
	// https://prometheus.io/docs/instrumenting/writing_exporters/#target-labels-not-static-scraped-labels
	ConstLabels Labels
	// contains filtered or unexported fields
}
```

| **字段名​**​     | ​**​类型​**​ | ​**​是否必填​**​ | ​**​默认值​**​ | ​**​说明​**​                                      | ​**​示例​**​                                   | ​**​注意事项​**​                                                            |
| ------------- | ---------- | ------------ | ----------- | ----------------------------------------------- | -------------------------------------------- | ----------------------------------------------------------------------- |
| `Namespace`   | `string`   | 否            | `""`        | 指标命名空间，用于组织指标层级。                                | `"order_service"`                            | 与 `Subsystem` 和 `Name` 共同组成全限定名（如 `order_service_http_requests_total`）。 |
| `Subsystem`   | `string`   | 否            | `""`        | 指标子系统，进一步细化分类。                                  | `"http"`                                     | 通常按功能模块划分（如 `http`、`database`）。                                         |
| `Name`        | `string`   | ​**​是​**​    | -           | 指标核心名称，需符合 Prometheus 命名规范（仅允许 `[a-zA-Z0-9_]`）。 | `"requests_total"`                           | 必须非空，否则注册时报错。                                                           |
| `Help`        | `string`   | ​**​强烈建议​**​ | `""`        | 指标的帮助信息，描述其用途。相同名称的指标必须拥有相同的 `Help`。            | `"Total HTTP requests processed."`           | 未设置可能导致监控数据难以理解。                                                        |
| `ConstLabels` | `Labels`   | 否            | `nil`       | 固定标签，为所有指标实例添加静态元信息（如环境、版本）。                    | `Labels{"env": "prod", "version": "v1.2.0"}` | 避免动态值（如用户 ID），防止时间序列基数爆炸。                                               |
1. ​**​全限定名生成规则​**​
    
    - 格式为 `<Namespace>_<Subsystem>_<Name>`，缺失部分自动省略。
    - 示例：
        
        ```go
        Namespace: "myapp",  
        Subsystem: "http",  
        Name:      "requests_total"  
        // 全限定名: myapp_http_requests_total
        ```
        
2. ​**​命名规范​**​
    
    - 仅允许字母、数字和下划线（`_`），如 `http_requests_total`。
    - 错误示例：`http-requests-total`（包含短横线）。
3. ​**​`ConstLabels` 的替代方案​**​
    
    - 动态标签应通过 `*Vec` 类型（如 `CounterVec`、`GaugeVec`）管理，而非 `ConstLabels`。
    - 固定元信息（如 `env="prod"`）适合用 `ConstLabels`。

```go
opts := prometheus.CounterOpts{
    Namespace:   "order_service",
    Subsystem:   "http",
    Name:        "requests_total",
    Help:        "Total HTTP requests processed by the order service.",
    ConstLabels: prometheus.Labels{"env": "production"},
}
// 全限定名: order_service_http_requests_total
```
## Labels

`Labels` 是一个键值对集合，用于表示 Prometheus 指标的标签（Metadata），其类型定义为：

```go
type Labels map[string]string
```

- ​**​键（Label Name）​**​：标识标签的维度（如 `method`、`status_code`）。
- ​**​值（Label Value）​**​：对应维度的具体取值（如 `GET`、`200`）。