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

### ​**​1. 指标命名与标签处理​**​

#### ​**​`BuildFQName(namespace, subsystem, name string) string`​**​

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

#### ​**​`MakeLabelPairs(desc *Desc, labelValues []string) []*dto.LabelPair`​**​

- ​**​作用​**​：将标签名和值组合成 Protobuf 格式的 `LabelPair` 结构，用于序列化指标数据。
- ​**​参数​**​：
    - `desc`：指标描述符（包含标签名）。
    - `labelValues`：标签值列表（顺序需与 `desc` 中的标签名一致）。
- ​**​典型场景​**​：在自定义 `Collector` 实现中构造指标标签。

### ​**​2. 直方图分桶生成​**​

#### ​**​`LinearBuckets(start, width float64, count int) []float64`​**​

- ​**​作用​**​：生成​**​线性增长​**​的分桶边界。
- ​**​参数​**​：
    - `start`：第一个桶的上边界。
    - `width`：桶宽（每个桶比前一个增加 `width`）。
    - `count`：桶总数。
- ​**​示例​**​：
    
    ```go
    buckets := LinearBuckets(1, 2, 3) // [1, 3, 5]
    ```
    

#### ​**​`ExponentialBuckets(start, factor float64, count int) []float64`​**​

- ​**​作用​**​：生成​**​指数增长​**​的分桶边界。
- ​**​参数​**​：
    - `start`：第一个桶的上边界。
    - `factor`：增长因子（每个桶是前一个的 `factor` 倍）。
    - `count`：桶总数。
- ​**​示例​**​：
    
    go
    
    复制
    
    ```go
    buckets := ExponentialBuckets(1, 2, 4) // [1, 2, 4, 8]
    ```
    

#### ​**​`ExponentialBucketsRange(minBucket, maxBucket float64, count int) []float64`​**​

- ​**​作用​**​：生成在 `[minBucket, maxBucket]` 范围内​**​指数分布​**​的分桶。
- ​**​参数​**​：
    - `minBucket`：最小桶边界（>0）。
    - `maxBucket`：最大桶边界。
    - `count`：桶总数（≥2）。
- ​**​示例​**​：
    
    ```go
    buckets := ExponentialBucketsRange(0.1, 100, 5) // [0.1, 1, 10, 100]
    ```


### ​**​3. 指标收集器（Collector）管理​**​

#### ​**​`Register(c Collector) error`​**​

- ​**​作用​**​：向 `DefaultRegisterer` 注册一个指标收集器。
- ​**​返回值​**​：若收集器已注册或标签冲突，返回错误。
- ​**​示例​**​：

    ```go
    err := Register(myCollector)
    ```


#### ​**​`MustRegister(cs ...Collector)`​**​

- ​**​作用​**​：批量注册收集器，若失败则 `panic`。
- ​**​典型用法​**​：在程序初始化时注册全局收集器。
    
    ```go
    MustRegister(cpuCollector, memCollector)
    ```
    

#### ​**​`Unregister(c Collector) bool`​**​

- ​**​作用​**​：从 `DefaultRegisterer` 注销收集器。
- ​**​返回值​**​：是否成功注销。
- ​**​场景​**​：动态卸载插件或模块的指标。

#### ​**​`DescribeByCollect(c Collector, descs chan<- *Desc)`​**​

- ​**​作用​**​：辅助函数，通过调用 `Collect` 方法自动生成指标的 `Desc` 描述。
- ​**​用途​**​：简化自定义 `Collector` 的实现，避免手动定义 `Describe` 方法。
- ​**​示例​**​：
    
    ```go
    func (c *MyCollector) Describe(ch chan<- *Desc) {
      DescribeByCollect(c, ch)
    }
    ```

### ​**​4. 工具函数​**​

#### ​**​`NewPidFileFn(pidFilePath string) func() (int, error)`​**​

- ​**​作用​**​：生成一个函数，用于读取指定 PID 文件并返回进程 ID。
- ​**​场景​**​：监控守护进程时，确认进程是否存活。
- ​**​示例​**​：
    
    ```go
    pidFn := NewPidFileFn("/var/run/myapp.pid")
    pid, err := pidFn()
    ```
    

#### ​**​`WriteToTextfile(filename string, g Gatherer) error`​**​

- ​**​作用​**​：将指标数据写入文本文件，格式符合 Prometheus 的 `textfile` 规范。
- ​**​用途​**​：供 `node_exporter` 的 `textfile` 收集器采集自定义指标。
- ​**​示例​**​：
    
    ```go
    WriteToTextfile("/path/to/metrics.prom", DefaultGatherer)
    ```
# 类型

