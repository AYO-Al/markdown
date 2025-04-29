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
- 版本要求：Prometheus 服务端版本 ≥2.40。

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
## HistogramOpts

- 类型定义：

```go
type HistogramOpts struct {
	// Namespace, Subsystem, and Name are components of the fully-qualified
	// name of the Histogram (created by joining these components with
	// "_"). Only Name is mandatory, the others merely help structuring the
	// name. Note that the fully-qualified name of the Histogram must be a
	// valid Prometheus metric name.
	Namespace string
	Subsystem string
	Name      string

	// Help provides information about this Histogram.
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

	// Buckets defines the buckets into which observations are counted. Each
	// element in the slice is the upper inclusive bound of a bucket. The
	// values must be sorted in strictly increasing order. There is no need
	// to add a highest bucket with +Inf bound, it will be added
	// implicitly. If Buckets is left as nil or set to a slice of length
	// zero, it is replaced by default buckets. The default buckets are
	// DefBuckets if no buckets for a native histogram (see below) are used,
	// otherwise the default is no buckets. (In other words, if you want to
	// use both regular buckets and buckets for a native histogram, you have
	// to define the regular buckets here explicitly.)
	Buckets []float64

	// If NativeHistogramBucketFactor is greater than one, so-called sparse
	// buckets are used (in addition to the regular buckets, if defined
	// above). A Histogram with sparse buckets will be ingested as a Native
	// Histogram by a Prometheus server with that feature enabled (requires
	// Prometheus v2.40+). Sparse buckets are exponential buckets covering
	// the whole float64 range (with the exception of the “zero” bucket, see
	// NativeHistogramZeroThreshold below). From any one bucket to the next,
	// the width of the bucket grows by a constant
	// factor. NativeHistogramBucketFactor provides an upper bound for this
	// factor (exception see below). The smaller
	// NativeHistogramBucketFactor, the more buckets will be used and thus
	// the more costly the histogram will become. A generally good trade-off
	// between cost and accuracy is a value of 1.1 (each bucket is at most
	// 10% wider than the previous one), which will result in each power of
	// two divided into 8 buckets (e.g. there will be 8 buckets between 1
	// and 2, same as between 2 and 4, and 4 and 8, etc.).
	//
	// Details about the actually used factor: The factor is calculated as
	// 2^(2^-n), where n is an integer number between (and including) -4 and
	// 8. n is chosen so that the resulting factor is the largest that is
	// still smaller or equal to NativeHistogramBucketFactor. Note that the
	// smallest possible factor is therefore approx. 1.00271 (i.e. 2^(2^-8)
	// ). If NativeHistogramBucketFactor is greater than 1 but smaller than
	// 2^(2^-8), then the actually used factor is still 2^(2^-8) even though
	// it is larger than the provided NativeHistogramBucketFactor.
	//
	// NOTE: Native Histograms are still an experimental feature. Their
	// behavior might still change without a major version
	// bump. Subsequently, all NativeHistogram... options here might still
	// change their behavior or name (or might completely disappear) without
	// a major version bump.
	NativeHistogramBucketFactor float64
	// All observations with an absolute value of less or equal
	// NativeHistogramZeroThreshold are accumulated into a “zero” bucket.
	// For best results, this should be close to a bucket boundary. This is
	// usually the case if picking a power of two. If
	// NativeHistogramZeroThreshold is left at zero,
	// DefNativeHistogramZeroThreshold is used as the threshold. To
	// configure a zero bucket with an actual threshold of zero (i.e. only
	// observations of precisely zero will go into the zero bucket), set
	// NativeHistogramZeroThreshold to the NativeHistogramZeroThresholdZero
	// constant (or any negative float value).
	NativeHistogramZeroThreshold float64

	// The next three fields define a strategy to limit the number of
	// populated sparse buckets. If NativeHistogramMaxBucketNumber is left
	// at zero, the number of buckets is not limited. (Note that this might
	// lead to unbounded memory consumption if the values observed by the
	// Histogram are sufficiently wide-spread. In particular, this could be
	// used as a DoS attack vector. Where the observed values depend on
	// external inputs, it is highly recommended to set a
	// NativeHistogramMaxBucketNumber.) Once the set
	// NativeHistogramMaxBucketNumber is exceeded, the following strategy is
	// enacted:
	//  - First, if the last reset (or the creation) of the histogram is at
	//    least NativeHistogramMinResetDuration ago, then the whole
	//    histogram is reset to its initial state (including regular
	//    buckets).
	//  - If less time has passed, or if NativeHistogramMinResetDuration is
	//    zero, no reset is performed. Instead, the zero threshold is
	//    increased sufficiently to reduce the number of buckets to or below
	//    NativeHistogramMaxBucketNumber, but not to more than
	//    NativeHistogramMaxZeroThreshold. Thus, if
	//    NativeHistogramMaxZeroThreshold is already at or below the current
	//    zero threshold, nothing happens at this step.
	//  - After that, if the number of buckets still exceeds
	//    NativeHistogramMaxBucketNumber, the resolution of the histogram is
	//    reduced by doubling the width of the sparse buckets (up to a
	//    growth factor between one bucket to the next of 2^(2^4) = 65536,
	//    see above).
	//  - Any increased zero threshold or reduced resolution is reset back
	//    to their original values once NativeHistogramMinResetDuration has
	//    passed (since the last reset or the creation of the histogram).
	NativeHistogramMaxBucketNumber  uint32
	NativeHistogramMinResetDuration time.Duration
	NativeHistogramMaxZeroThreshold float64

	// NativeHistogramMaxExemplars limits the number of exemplars
	// that are kept in memory for each native histogram. If you leave it at
	// zero, a default value of 10 is used. If no exemplars should be kept specifically
	// for native histograms, set it to a negative value. (Scrapers can
	// still use the exemplars exposed for classic buckets, which are managed
	// independently.)
	NativeHistogramMaxExemplars int
	// NativeHistogramExemplarTTL is only checked once
	// NativeHistogramMaxExemplars is exceeded. In that case, the
	// oldest exemplar is removed if it is older than NativeHistogramExemplarTTL.
	// Otherwise, the older exemplar in the pair of exemplars that are closest
	// together (on an exponential scale) is removed.
	// If NativeHistogramExemplarTTL is left at its zero value, a default value of
	// 5m is used. To always delete the oldest exemplar, set it to a negative value.
	NativeHistogramExemplarTTL time.Duration
	// contains filtered or unexported fields
}
```

|字段名|类型|默认值|是否必填|描述|注意事项|
|---|---|---|---|---|---|
|​**​Namespace​**​|`string`|空字符串|否|指标命名空间，用于分类管理（如 `myapp`）|与 `Subsystem`、`Name` 组合成指标全名（格式：`Namespace_Subsystem_Name`）|
|​**​Subsystem​**​|`string`|空字符串|否|指标子系统，进一步细分命名空间（如 `http`）|同上|
|​**​Name​**​|`string`|无|​**​是​**​|指标名称（如 `request_duration_seconds`）|必须非空且符合 Prometheus 命名规则（仅允许 `[a-zA-Z0-9_]`）|
|​**​Help​**​|`string`|空字符串|否|指标的帮助信息|相同名称的指标必须拥有相同的 `Help` 字符串|
|​**​ConstLabels​**​|`Labels`|`nil`|否|固定标签（如 `{"env": "prod"}`）|避免高基数标签；禁止使用 `quantile`|
|​**​Buckets​**​|`[]float64`|`DefBuckets`（预设桶列表）|否|定义直方图的桶边界（如 `[]float64{0.1, 0.5, 1}`）|桶值必须严格递增；若为空则使用默认桶（若启用原生直方图则默认桶为空）|
|​**​NativeHistogramBucketFactor​**​|`float64`|1.0|否|稀疏桶的指数增长因子（≥1.0 启用原生直方图）|推荐值 `1.1`（平衡精度与性能）；仅 Prometheus ≥2.40 支持|
|​**​NativeHistogramZeroThreshold​**​|`float64`|`DefNativeHistogramZeroThreshold`|否|绝对值小于此阈值的观测值计入“零桶”|建议设为 2 的幂次方（如 `0.001`）；设为负数时仅精确零值计入零桶|
|​**​NativeHistogramMaxBucketNumber​**​|`uint32`|0|否|稀疏桶的最大数量限制（防止内存溢出）|生产环境建议设置合理值（如 `1000`）；设为 `0` 表示无限制|
|​**​NativeHistogramMinResetDuration​**​|`time.Duration`|0|否|触发桶重置的最小时间间隔（超限时重置直方图）|若设为 `10m`，则每 10 分钟检查一次重置条件|
|​**​NativeHistogramMaxZeroThreshold​**​|`float64`|0|否|自动调整零阈值的上限值|用于动态平衡桶数量；需配合 `MaxBucketNumber` 使用|
|​**​NativeHistogramMaxExemplars​**​|`int`|10|否|原生直方图保留的样本（Exemplar）最大数量|设为 `-1` 禁用原生样本；样本用于关联跟踪数据（如 TraceID）|
|​**​NativeHistogramExemplarTTL​**​|`time.Duration`|5 分钟|否|样本的存活时间（超时自动删除）|设为负值则优先删除最旧样本|


 **关键字段详解​**​

 1. ​**​Buckets​**​

- ​**​默认桶​**​：`DefBuckets = []float64{0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10}`
- ​**​自定义示例​**​：
    
    ```go
    Buckets: []float64{0.1, 0.5, 1, 2.5}  // 自定义延迟分布桶
    ```
    

 2. ​**​NativeHistogramBucketFactor​**​

- ​**​稀疏桶特性​**​：
    - 桶宽按指数增长，覆盖全范围浮点数（如 `1.1` 表示桶宽增长 10%）。
    - ​**​适用场景​**​：高动态范围数据（如延迟从毫秒到小时）。

 3. ​**​NativeHistogramZeroThreshold​**​

- ​**​示例​**​：
    
    ```go
    NativeHistogramZeroThreshold: 0.001  // 绝对值 ≤0.001 的值计入零桶
    ```
    

 4. ​**​NativeHistogramMaxBucketNumber​**​

- ​**​动态调整策略​**​：
    1. 若桶数超限且超过 `MinResetDuration`，重置直方图。
    2. 否则增大零阈值或降低分辨率（桶宽翻倍）。

 5. ​**​NativeHistogramExemplarTTL​**​

- ​**​示例​**​：
    
    ```go
    NativeHistogramExemplarTTL: 10 * time.Minute  // 样本保留 10 分钟
    ```

- 整体代码示例：

```go
opts := prometheus.HistogramOpts{
    Name:      "http_request_duration_seconds",
    Help:      "HTTP request latency distribution in seconds",
    Namespace: "myapp",
    Subsystem: "http",
    Buckets:   []float64{0.1, 0.5, 1, 2.5},
    ConstLabels: prometheus.Labels{
        "env": "production",
    },
    NativeHistogramBucketFactor:     1.1,
    NativeHistogramZeroThreshold:    0.001,
    NativeHistogramMaxBucketNumber:  1000,
    NativeHistogramMinResetDuration: 10 * time.Minute,
    NativeHistogramMaxExemplars:     20,
    NativeHistogramExemplarTTL:      5 * time.Minute,
}
```
## \*Func

`CounterFunc` 是 Prometheus 客户端库提供的一种特殊计数器类型，允许通过 ​**​回调函数​**​ 动态获取计数器的值。与普通 `Counter` 不同，`CounterFunc` 的值由用户定义的函数在每次指标被抓取时计算，无需手动调用 `Inc()` 或 `Add()`。

| ​**​类型​**​    | ​**​语义​**​ | ​**​典型场景​**​     |
| ------------- | ---------- | ---------------- |
| `CounterFunc` | 单调递增的累计值   | 总任务处理量（需外部系统提供值） |
| `GaugeFunc`   | 可任意变化的瞬时值  | 当前内存使用量、活跃连接数    |
**注意事项：**

1. ​**​单调性要求​**​：
    
    - `CounterFunc` 的值 ​**​理论上应单调递增​**​（符合计数器的语义）。
    - 若值可能减少（如当前连接数），应改用 `GaugeFunc`。
2. ​**​性能优化​**​：
    
    - 回调函数应 ​**​快速执行​**​，避免阻塞指标抓取。
    - 复杂计算或 I/O 操作建议异步更新并缓存结果。
3. ​**​错误处理​**​：
    
    - 回调函数中抛出 panic 会导致整个指标抓取失败，需自行处理异常。
4. ​**​注册与注销​**​：
    
    - 使用 `MustRegister` 注册后，若回调函数依赖外部资源，需在资源释放后调用 `Unregister`。

```go
import (
    "runtime"
    "github.com/prometheus/client_golang/prometheus"
)

func main() {
    // 定义 CounterFunc（注意：实际应使用 GaugeFunc！此处仅为示例）
    goroutineCounter := prometheus.NewCounterFunc(
        prometheus.CounterOpts{
            Name: "app_goroutines_total",
            Help: "Total number of goroutines (示例，实际应用不推荐).",
        },
        func() float64 {
            return float64(runtime.NumGoroutine())
        },
    )

    prometheus.MustRegister(goroutineCounter)

    // 启动 HTTP 服务暴露指标
    http.Handle("/metrics", promhttp.Handler())
    http.ListenAndServe(":8080", nil)
}
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
## SummaryOpts

- 类型定义：

```go
type SummaryOpts struct {
	// Namespace, Subsystem, and Name are components of the fully-qualified
	// name of the Summary (created by joining these components with
	// "_"). Only Name is mandatory, the others merely help structuring the
	// name. Note that the fully-qualified name of the Summary must be a
	// valid Prometheus metric name.
	Namespace string
	Subsystem string
	Name      string

	// Help provides information about this Summary.
	//
	// Metrics with the same fully-qualified name must have the same Help
	// string.
	Help string

	// ConstLabels are used to attach fixed labels to this metric. Metrics
	// with the same fully-qualified name must have the same label names in
	// their ConstLabels.
	//
	// Due to the way a Summary is represented in the Prometheus text format
	// and how it is handled by the Prometheus server internally, “quantile”
	// is an illegal label name. Construction of a Summary or SummaryVec
	// will panic if this label name is used in ConstLabels.
	//
	// ConstLabels are only used rarely. In particular, do not use them to
	// attach the same labels to all your metrics. Those use cases are
	// better covered by target labels set by the scraping Prometheus
	// server, or by one specific metric (e.g. a build_info or a
	// machine_role metric). See also
	// https://prometheus.io/docs/instrumenting/writing_exporters/#target-labels-not-static-scraped-labels
	ConstLabels Labels

	// Objectives defines the quantile rank estimates with their respective
	// absolute error. If Objectives[q] = e, then the value reported for q
	// will be the φ-quantile value for some φ between q-e and q+e.  The
	// default value is an empty map, resulting in a summary without
	// quantiles.
	Objectives map[float64]float64

	// MaxAge defines the duration for which an observation stays relevant
	// for the summary. Only applies to pre-calculated quantiles, does not
	// apply to _sum and _count. Must be positive. The default value is
	// DefMaxAge.
	MaxAge time.Duration

	// AgeBuckets is the number of buckets used to exclude observations that
	// are older than MaxAge from the summary. A higher number has a
	// resource penalty, so only increase it if the higher resolution is
	// really required. For very high observation rates, you might want to
	// reduce the number of age buckets. With only one age bucket, you will
	// effectively see a complete reset of the summary each time MaxAge has
	// passed. The default value is DefAgeBuckets.
	AgeBuckets uint32

	// BufCap defines the default sample stream buffer size.  The default
	// value of DefBufCap should suffice for most uses. If there is a need
	// to increase the value, a multiple of 500 is recommended (because that
	// is the internal buffer size of the underlying package
	// "github.com/bmizerany/perks/quantile").
	BufCap uint32
	// contains filtered or unexported fields
}
```

|字段名|类型|默认值|是否必填|描述|注意事项|
|---|---|---|---|---|---|
|​**​Namespace​**​|`string`|空字符串|否|指标命名空间，用于分类管理（如 `myapp`）|与 `Subsystem`、`Name` 共同组成指标全名（格式：`Namespace_Subsystem_Name`）|
|​**​Subsystem​**​|`string`|空字符串|否|指标子系统，进一步细分命名空间（如 `http`）|同上|
|​**​Name​**​|`string`|无|​**​是​**​|指标名称（如 `request_duration_seconds`）|必须非空且符合 Prometheus 指标命名规则（仅允许 `[a-zA-Z0-9_]`）|
|​**​Help​**​|`string`|空字符串|否|指标的帮助信息，用于描述指标用途|相同名称的指标必须拥有相同的 `Help` 字符串|
|​**​ConstLabels​**​|`prometheus.Labels`|`nil`|否|固定标签（如 `{"env": "prod"}`）|禁止使用 `quantile` 作为标签名；避免高基数标签|
|​**​Objectives​**​|`map[float64]float64`|空 `map`|否|分位数目标及允许误差（如 `{0.5: 0.05}` 表示中位数误差 ±5%）|默认值将在 v1.0.0 变更为空，建议显式设置；误差值越小，资源消耗越大|
|​**​MaxAge​**​|`time.Duration`|`DefMaxAge`（通常 10 分钟）|否|观测值的有效时间窗口（旧数据过期后被丢弃）|仅影响分位数计算；必须为正数|
|​**​AgeBuckets​**​|`uint32`|`DefAgeBuckets`（通常 5）|否|时间窗口内的分段数量（用于管理 `MaxAge` 内的数据分布）|值越大，内存消耗越高；设为 1 时窗口过期后分位数完全重置|
|​**​BufCap​**​|`uint32`|`DefBufCap`（通常 500）|否|采样数据流的缓冲区容量|建议设置为 500 的倍数（如 1000）；高吞吐场景可增大此值|

 ​​**字段关键点总结​：**

1. ​**​必填字段​**​：仅 `Name` 必须设置。
2. ​**​名称规则​**​：
    - 全名格式：`Namespace_Subsystem_Name`（如 `myapp_http_request_duration_seconds`）。
    - 名称需符合正则表达式 `^[a-zA-Z_][a-zA-Z0-9_]*$`。
3. ​**​分位数配置​**​：
    - 若不设置 `Objectives`，则不会生成分位数指标（仅有 `_count` 和 `_sum`）。
    - 示例：`Objectives: map[float64]float64{0.9: 0.01}` 表示计算 P90，误差不超过 ±1%。
4. ​**​性能调优​**​：
    - `MaxAge` 和 `AgeBuckets`：平衡分位数精度与内存开销。
    - `BufCap`：影响高吞吐场景下的观测值缓冲能力。​

```go
opts := prometheus.SummaryOpts{
    Name:      "http_request_duration_seconds",
    Help:      "HTTP request latency distribution in seconds",
    Namespace: "myapp",
    Subsystem: "http",
    ConstLabels: prometheus.Labels{
        "env": "production",
    },
    Objectives: map[float64]float64{
        0.5:  0.05,  // 中位数 ±5%
        0.95: 0.01,  // P95 ±1%
    },
    MaxAge:     5 * time.Minute,
    AgeBuckets: 10,
    BufCap:     1000,
}
```
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

// CounterOpts
type CounterOpts Opts

// GaugeOpts
type GaugeOpts Opts
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
## Colletcor

- 类型定义：

```go
type Collector interface {
	Describe(chan<- *[Desc]
	Collect(chan<- [Metric]
}
```

| **方法名​**​          | ​**​参数名​**​ | ​**​参数类型​**​    | ​**​作用​**​                                       |
| ------------------ | ----------- | --------------- | ------------------------------------------------ |
| ​**​`Describe`​**​ | `ch`        | `chan<- *Desc`  | 传递指标的 ​**​描述符​**​（Descriptor），用于注册时检查指标的唯一性和一致性。 |
| ​**​`Collect`​**​  | `ch`        | `chan<- Metric` | 传递实际的 ​**​指标数据​**​（Metric），用于收集当前时刻的指标值。         |
1. **`Describe` 方法​**​
    
    - ​**​通道内容​**​：发送 `*Desc` 类型指针，描述指标的元信息（名称、帮助文档、标签等）。
    - ​**​一致性检查​**​：Prometheus 在注册时通过此方法验证指标是否冲突或重复。
    - ​**​示例​**​：
        
        ```go
        func (c *MyCollector) Describe(ch chan<- *Desc) {
            ch <- myMetricDesc // 发送指标描述符
        }
        ```
        
2. ​**​`Collect` 方法​**​
    
    - ​**​通道内容​**​：发送 `Metric` 接口实现的具体指标数据（如 `Gauge`, `Counter` 等）。
    - ​**​实时收集​**​：每次调用 `Gather()` 或 HTTP 暴露指标时触发此方法，生成当前时刻的指标值。
    - ​**​示例​**​：
        
        ```go
        func (c *MyCollector) Collect(ch chan<- Metric) {
            ch <- myMetric.WithLabelValues("label1").Set(42) // 发送指标数据
        }
        ```

3. ​**​单一指标 Collector​**​（如 `Gauge`, `Counter`）

```go
type MyGauge struct {
    desc *Desc
    value float64
}

func (g *MyGauge) Describe(ch chan<- *Desc) {
    ch <- g.desc
}

func (g *MyGauge) Collect(ch chan<- Metric) {
    ch <- g
}
```

4. ​**​复合指标 Collector​**​（如 `GaugeVec`, `HistogramVec`）

```go
type MyCollector struct {
    desc      *Desc
    metrics   []Metric
}

func (c *MyCollector) Describe(ch chan<- *Desc) {
    ch <- c.desc
}

func (c *MyCollector) Collect(ch chan<- Metric) {
    for _, m := range c.metrics {
        ch <- m
    }
}
```

> ​注意事项​​

|​**​场景​**​|​**​处理方式​**​|
|---|---|
|​**​高并发调用​**​|`Describe` 和 `Collect` 需实现为 ​**​线程安全​**​（如加锁或无状态）。|
|​**​指标动态生成​**​|在 `Collect` 中实时生成指标（如从外部系统读取数据），避免在 `Describe` 中生成。|
|​**​错误处理​**​|若 `Describe` 执行失败，需发送 `NewInvalidDesc()` 到通道通知 Registry。|

通过实现 `Collector` 接口，可以灵活扩展自定义指标（如集成第三方系统数据），并纳入 Prometheus 的统一管理中。
## Registerer 接口​​/Registry类型

​**​`Registerer`​**​ 是用于注册和管理指标收集器（`Collector`）的接口。`Registry` 是其默认实现，负责管理指标的生命周期。

> 核心方法​​

|​**​方法​**​|​**​说明​**​|
|---|---|
|`Register(Collector) error`|注册一个 `Collector`，若名称冲突或标签不一致返回错误。|
|`MustRegister(...Collector)`|批量注册 `Collector`，失败时触发 `panic`。|
|`Unregister(Collector) bool`|注销一个 `Collector`，返回是否成功。|


**​`Registry`​**​ 是 `Registerer` 的具体实现，用于管理多个 `Collector` 的注册和指标收集。

> 创建方法

|​**​函数​**​|​**​说明​**​|
|---|---|
|`NewRegistry() *Registry`|创建标准 Registry，仅检查指标名称和标签冲突。|
|`NewPedanticRegistry() *Registry`|创建严格模式 Registry，额外检查 `Help` 字符串和类型一致性（适合测试）。|


```go
// 创建标准 Registry
registry := prometheus.NewRegistry()

// 创建严格模式 Registry（用于测试）
pedanticRegistry := prometheus.NewPedanticRegistry()
```

> 核心方法

|​**​方法​**​|​**​说明​**​|
|---|---|
|`Gather() ([]*dto.MetricFamily, error)`|收集所有注册的指标数据，转换为 Protobuf 格式（用于 HTTP 暴露或自定义处理）。|
|`Collect(chan<- Metric)`|实现 `Collector` 接口，收集所有指标到通道中。|
|`Describe(chan<- *Desc)`|实现 `Collector` 接口，描述所有注册的指标。|

​**​示例​**​：暴露指标到 HTTP 服务

```go
http.Handle("/metrics", promhttp.HandlerFor(registry, promhttp.HandlerOpts{}))
```

> 包装 Registerer​​

通过包装现有 `Registerer`，可以全局修改注册的指标名称或标签。

> ​WrapRegistererWith(labels, reg)

- ​**​作用​**​：为所有注册的指标添加 ​**​固定标签​**​。
- ​**​参数​**​：
    - `labels Labels`：需要添加的标签键值对。
    - `reg Registerer`：被包装的原始 `Registerer`。
- ​**​示例​**​：
    
    ```go
    // 添加环境标签到所有指标
    wrappedReg := prometheus.WrapRegistererWith(
        prometheus.Labels{"env": "prod"},
        registry,
    )
    wrappedReg.MustRegister(cpuCollector) // 所有 cpuCollector 的指标自动包含 env="prod"
    ```

> WrapRegistererWithPrefix(prefix, reg)​​

- ​**​作用​**​：为所有注册的指标名称添加 ​**​前缀​**​。
- ​**​参数​**​：
    - `prefix string`：名称前缀（如 `myapp_`）。
    - `reg Registerer`：被包装的原始 `Registerer`。
- ​**​示例​**​：
    
    ```go
    // 添加前缀 "myapp_"
    wrappedReg := prometheus.WrapRegistererWithPrefix("myapp_", registry)
    wrappedReg.MustRegister(cpuCollector) // 指标名称变为 myapp_cpu_usage
    ```


### ​**​使用场景​**​

#### ​**​默认注册表​**​

- ​**​直接使用全局注册表​**​：
    
    ```go
    // 注册到默认 Registry（prometheus.DefaultRegisterer）
    prometheus.MustRegister(httpRequests)
    ```
    

#### ​**​自定义注册表​**​

- ​**​隔离指标​**​：不同模块使用独立的 Registry，避免名称冲突。
    
    ```go
    // 模块 A 的 Registry
    registryA := prometheus.NewRegistry()
    registryA.MustRegister(collectorA)
    
    // 模块 B 的 Registry
    registryB := prometheus.NewRegistry()
    registryB.MustRegister(collectorB)
    ```
    

#### ​**​添加全局标签​**​

- ​**​统一标记环境信息​**​：
    
    ```go
    wrappedReg := prometheus.WrapRegistererWith(
        prometheus.Labels{"cluster": "east-1"},
        prometheus.DefaultRegisterer,
    )
    wrappedReg.MustRegister(httpRequests) // 所有指标包含 cluster="east-1"
    ```
    

#### ​**​指标聚合与暴露​**​

- ​**​自定义 HTTP 端点​**​：
    
    ```go
    // 创建自定义 Registry
    registry := prometheus.NewRegistry()
    registry.MustRegister(cpuCollector)
    
    // 暴露指标
    http.Handle("/metrics", promhttp.HandlerFor(registry, promhttp.HandlerOpts{}))
    ```


### ​**​方法详解​**​

#### ​Register(c Collector) error

- ​**​作用​**​：注册一个 `Collector`，失败返回错误（如名称冲突）。
- ​**​示例​**​：
    
    ```go
    err := registry.Register(myCollector)
    if err != nil {
        log.Fatal("注册失败:", err)
    }
    ```
    

#### ​MustRegister(cs ...Collector)

- ​**​作用​**​：批量注册 `Collector`，失败时 `panic`。
- ​**​示例​**​：
    
    ```go
    registry.MustRegister(cpuCollector, memCollector)
    ```
    

#### ​Unregister(c Collector) bool

- ​**​作用​**​：注销已注册的 `Collector`，返回是否成功。
- ​**​示例​**​：
    
    ```go
    if ok := registry.Unregister(oldCollector); ok {
        log.Println("注销成功")
    }
    ```
    

#### Gather() (\[\]\*dto.MetricFamily, error)

- ​**​作用​**​：收集所有指标数据，转换为 Protobuf 格式。
- ​**​用途​**​：自定义指标处理或导出到其他系统。
- ​**​示例​**​：
    
    ```go
    metrics, err := registry.Gather()
    if err != nil {
        log.Fatal("收集指标失败:", err)
    }
    ```
​

|​**​场景​**​|​**​推荐方法​**​|
|---|---|
|​**​全局默认监控​**​|使用 `prometheus.DefaultRegisterer` 和 `prometheus.MustRegister`。|
|​**​模块化指标隔离​**​|为每个模块创建独立的 `Registry`。|
|​**​添加环境标签​**​|使用 `WrapRegistererWith` 包装默认 Registry。|
|​**​严格指标检查（测试环境）​**​|使用 `NewPedanticRegistry()`。|
|​**​动态注销指标（如插件）​**​|结合 `Register` 和 `Unregister` 管理 Collector 生命周期。|


### ​注意事项​​

1. ​**​避免重复注册​**​：同一 `Collector` 不可重复注册到同一 Registry。
2. ​**​高基数标签​**​：避免在 `WrapRegistererWith` 中使用动态值（如用户 ID）。
3. ​**​线程安全​**​：`Registry` 的 `Register`/`Unregister` 方法需在并发环境中加锁。
4. ​**​性能影响​**​：频繁调用 `Gather()` 可能影响性能，建议与 HTTP 暴露间隔结合使用。
### 为什么要注册到不同的Registry

> 1. ​​指标隔离与模块化​​

- ​**​场景​**​：不同模块（如微服务、插件、中间件）需要独立管理自己的指标。
- ​**​优势​**​：
    - ​**​避免命名冲突​**​：不同模块的同名指标（如 `http_requests_total`）可以隔离在不同 Registry 中。
    - ​**​独立生命周期​**​：模块卸载时，直接销毁对应的 Registry，无需遍历全局 Registry 删除指标。
- ​**​示例​**​：
    
    ```go
    // 模块 A 的 Registry
    registryA := prometheus.NewRegistry()
    registryA.MustRegister(moduleACollector)
    
    // 模块 B 的 Registry
    registryB := prometheus.NewRegistry()
    registryB.MustRegister(moduleBCollector)
    ```
    

> ​2. ​​定制化指标暴露​​

- ​**​场景​**​：将不同模块的指标暴露到独立的 HTTP 端点。
- ​**​优势​**​：
    - ​**​按需暴露​**​：敏感指标（如调试接口）可绑定到特定端口，不与业务指标混用。
    - ​**​权限隔离​**​：不同端口的指标可配置不同的访问权限。
- ​**​示例​**​：
    
    ```go
    // 业务指标暴露在默认端口
    http.Handle("/metrics", promhttp.HandlerFor(businessRegistry, opts))
    
    // 调试指标暴露在专用端口
    debugServer := &http.Server{
        Addr:    ":9091",
        Handler: promhttp.HandlerFor(debugRegistry, opts),
    }
    ```

> ​​3. ​​动态配置与灵活性​​

- ​**​场景​**​：动态加载/卸载插件或功能模块。
- ​**​优势​**​：
    - ​**​热更新​**​：插件启用时注册到独立 Registry，禁用时直接销毁，无需重启服务。
    - ​**​资源节省​**​：避免全局 Registry 残留未使用的指标描述符（`Desc`）。
- ​**​示例​**​：
    
    ```go
    // 动态加载插件
    func loadPlugin() {
        pluginRegistry := prometheus.NewRegistry()
        pluginRegistry.MustRegister(pluginCollector)
        pluginManager.Add(pluginRegistry)
    }
    
    // 卸载插件时
    pluginRegistry.Unregister(pluginCollector)
    ```

> ​​4. ​​性能优化​​

- ​**​场景​**​：高频更新或大规模指标的监控场景。
- ​**​优势​**​：
    - ​**​减少锁竞争​**​：全局 Registry 的 `Register`/`Gather` 使用互斥锁，独立 Registry 可降低锁粒度。
    - ​**​并行收集​**​：多个 Registry 的 `Gather()` 可并发执行，提升指标收集效率。
- ​**​示例​**​：
    
    ```go
    // 高吞吐模块使用独立 Registry
    highLoadRegistry := prometheus.NewRegistry()
    go func() {
        for {
            metrics := highLoadRegistry.Gather() // 独立收集，不影响主流程
            sendToMonitoringSystem(metrics)
            time.Sleep(5 * time.Second)
        }
    }()
    ```

> ​5. ​​测试与调试​​

- ​**​场景​**​：单元测试或集成测试中验证特定模块的指标。
- ​**​优势​**​：
    - ​**​精准断言​**​：测试时仅关注目标 Registry 的指标，排除其他模块干扰。
    - ​**​严格模式​**​：使用 `NewPedanticRegistry()` 在测试中检查指标规范（如 `Help` 描述是否为空）。
- ​**​示例​**​：
    
    ```go
    func TestModuleA(t *testing.T) {
        testRegistry := prometheus.NewPedanticRegistry() // 严格模式
        testRegistry.MustRegister(moduleACollector)
        
        // 触发模块 A 的逻辑
        moduleA.ProcessRequest()
        
        metrics, _ := testRegistry.Gather()
        assert.Contains(t, metrics, "module_a_requests_total")
    }
    ```

> ​6. ​​多租户与多环境支持​​

- ​**​场景​**​：同一服务需要为不同租户或环境（如开发、生产）生成隔离的指标。
- ​**​优势​**​：
    - ​**​标签隔离​**​：通过不同 Registry 为指标添加租户/环境专属标签（如 `tenant_id="user1"`）。
    - ​**​数据分离​**​：避免跨租户的指标混合导致查询复杂度上升。
- ​**​示例​**​：
    
    ```go
    // 租户专属 Registry 工厂
    func NewTenantRegistry(tenantID string) *prometheus.Registry {
        reg := prometheus.NewRegistry()
        wrappedReg := prometheus.WrapRegistererWith(
            prometheus.Labels{"tenant_id": tenantID},
            reg,
        )
        wrappedReg.MustRegister(tenantCollector)
        return reg
    }
    ```

> ​​总结：何时使用多个 Registry​

|​**​场景​**​|​**​推荐方案​**​|
|---|---|
|模块化服务开发|每个模块使用独立 Registry|
|动态插件机制|插件生命周期绑定到独立 Registry|
|多租户/多环境监控|为每个租户创建专属 Registry|
|高频指标收集|分离高负载模块到独立 Registry|
|严格测试|使用 `NewPedanticRegistry()`|

通过合理使用多 Registry，可实现监控系统的​**​高内聚、低耦合​**​，提升可维护性和性能。