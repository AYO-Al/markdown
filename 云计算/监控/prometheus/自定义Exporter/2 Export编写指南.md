详细内容可查看[官方文档](https://prometheus.io/docs/instrumenting/writing_clientlibs/)

**注意：以下代码均非源码。只是为了理解的简化代码。**
# 1 整体结构

首先，Collector是核心类，有一个collect方法，用于返回指标及其样本。CollectorRegistry用来注册Collector，当有数据请求时，Registry会回调所有已注册的Collector的collect方法。用户常用的接口是Counter、Gauge、Summary和Histogram这些指标类型，它们本身也是Collector，覆盖大部分用例。高级场景可能需要自定义Collector，比如桥接其他监控系统。

1. ​**​回调机制​**​：

- 所有指标数据通过 `Collect()` 方法回调获取
- 注册中心在 `Scrape()` 时遍历调用所有收集器的 `Collect()`
- 避免主动轮询，实现按需获取最新数据

2. ​**​线程安全​**​：

- 注册中心使用 `sync.RWMutex` 保护收集器集合
- 计数器使用 `atomic` 包保证原子操作
- 自定义收集器使用 `sync.Mutex` 保护内部状态

3. ​**​扩展性​**​：

- 通过 Collector 接口支持自定义指标类型
- 可以创建多个 CollectorRegistry 实现不同数据隔离
- 桥接器模式支持不同输出格式

4. ​**​标准指标实现​**​：

- Counter/Gauge/Summary/Histogram 只需实现 Collector 接口
- 提供原子操作的增减方法
- 内置标签(label)支持实现多维度量

5. ​**​注册中心职责​**​：

- 管理 Collector 的生命周期
- 提供统一的指标收集入口
- 保证线程安全的并发访问

```go
package main

import (
	"fmt"
	"sync"
	"sync/atomic"
)

// Metric 表示一个指标样本
type Metric struct {
	Name   string
	Value  float64
	Labels map[string]string
}

// Collector 收集器接口
type Collector interface {
	// Collect 返回指标和样本，必须线程安全
	Collect() []Metric
}

// CollectorRegistry 收集器注册中心
type CollectorRegistry struct {
	collectors map[Collector]bool
	mu         sync.RWMutex // 保证线程安全
}

func NewCollectorRegistry() *CollectorRegistry {
	return &CollectorRegistry{
		collectors: make(map[Collector]bool),
	}
}

// Register 注册收集器
func (r *CollectorRegistry) Register(c Collector) {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.collectors[c] = true
}

// Unregister 注销收集器
func (r *CollectorRegistry) Unregister(c Collector) {
	r.mu.Lock()
	defer r.mu.Unlock()
	delete(r.collectors, c)
}

// Scrape 触发所有收集器回调并收集指标
func (r *CollectorRegistry) Scrape() []Metric {
	r.mu.RLock()
	defer r.mu.RUnlock()

	var metrics []Metric
	for collector := range r.collectors {
		metrics = append(metrics, collector.Collect()...)
	}
	return metrics
}

/* ================= 标准指标类型实现 ================= */

// Counter 计数器实现
type Counter struct {
	name   string
	labels map[string]string
	value  uint64 // 使用原子操作保证线程安全
}

func NewCounter(name string, labels map[string]string) *Counter {
	return &Counter{
		name:   name,
		labels: labels,
	}
}

// Inc 增加计数器值
func (c *Counter) Inc() {
	atomic.AddUint64(&c.value, 1)
}

// Collect 实现 Collector 接口
func (c *Counter) Collect() []Metric {
	return []Metric{{
		Name:   c.name,
		Value:  float64(atomic.LoadUint64(&c.value)),
		Labels: c.labels,
	}}
}

// Gauge 仪表盘实现（类似结构，增加Dec()方法）
type Gauge struct {
	name   string
	labels map[string]string
	value  uint64
}

func (g *Gauge) Dec() {
	atomic.AddUint64(&g.value, ^uint64(0))
}

/* ================= 使用示例 ================= */

func main() {
	// 创建注册中心
	registry := NewCollectorRegistry()

	// 创建指标
	httpRequests := NewCounter("http_requests_total", map[string]string{
		"handler": "/api",
	})

	// 注册指标到注册中心
	registry.Register(httpRequests)

	// 模拟请求处理
	for i := 0; i < 5; i++ {
		httpRequests.Inc()
	}

	// 桥接器：将指标转换为Prometheus格式
	bridge := func(metrics []Metric) string {
		var result string
		for _, m := range metrics {
			result += fmt.Sprintf("%s %f\n", m.Name, m.Value)
		}
		return result
	}

	// 每次抓取都会回调所有Collectors的Collect方法
	metrics := registry.Scrape()
	fmt.Println(bridge(metrics))
	// 输出：
	// http_requests_total 5.000000
}

/* ================= 自定义收集器示例 ================= */

// DatabaseStatsCollector 自定义数据库统计收集器
type DatabaseStatsCollector struct {
	mu          sync.Mutex
	connections int
	queries     map[string]int
}

func NewDatabaseStatsCollector() *DatabaseStatsCollector {
	return &DatabaseStatsCollector{
		queries: make(map[string]int),
	}
}

// UpdateConnection 更新连接数（业务方法）
func (d *DatabaseStatsCollector) UpdateConnection(count int) {
	d.mu.Lock()
	defer d.mu.Unlock()
	d.connections = count
}

// RecordQuery 记录查询类型（业务方法）
func (d *DatabaseStatsCollector) RecordQuery(queryType string) {
	d.mu.Lock()
	defer d.mu.Unlock()
	d.queries[queryType]++
}

// Collect 实现回调接口
func (d *DatabaseStatsCollector) Collect() []Metric {
	d.mu.Lock()
	defer d.mu.Unlock()

	return []Metric{
		{
			Name:  "database_connections",
			Value: float64(d.connections),
		},
		{
			Name:   "database_queries",
			Value:  float64(len(d.queries)),
			Labels: map[string]string{"type": "total"},
		},
	}
}

// PrometheusBridge 转换为 Prometheus 文本格式
func PrometheusBridge(metrics []Metric) string {
	var builder strings.Builder

	for _, m := range metrics {
		// 构建标签部分
		var labels []string
		for k, v := range m.Labels {
			labels = append(labels, fmt.Sprintf("%s=%q", k, v))
		}

		// 构建完整指标行
		if len(labels) > 0 {
			builder.WriteString(fmt.Sprintf("%s{%s} %v\n", m.Name, strings.Join(labels, ","), m.Value))
		} else {
			builder.WriteString(fmt.Sprintf("%s %v\n", m.Name, m.Value))
		}
	}

	return builder.String()
}

```
# 2 指标

****​1. 核心指标类型要求​**​

- ​**​必须包含​**​：Counter（计数器）和 Gauge（仪表盘）  
    Counter用于累加计数（如请求总数），Gauge表示瞬时值（如内存使用量）。
- ​**​至少包含一个高级类型​**​：Summary（摘要）或 Histogram（直方图）  
    Summary用于跟踪分位数（如响应时间的P99），Histogram通过预定义桶（Bucket）统计分布。

​**​2. 文件静态变量设计​**​

- 指标应作为​**​全局变量​**​定义在需要监控的代码文件内，与业务代码共存。
- 例如在`api_handler.go`中直接定义HTTP请求计数器，避免将指标对象在代码中层层传递。
- 客户端库需支持这种用法，减少用户的心智负担。

​**​3. 默认注册中心机制​**​

- 提供​**​默认CollectorRegistry​**​，自动收集所有标准指标。
- 用户创建指标时​**​无需手动注册​**​，默认即加入全局注册中心。
- 允许​**​禁用自动注册​**​或​**​指定自定义注册中心​**​，满足测试和批处理场景的隔离需求。

​**​4. 多语言实现差异​**​

- ​**​Java/Go​**​：适合使用Builder模式（链式调用配置参数），增强可读性和扩展性。
- ​**​Python​**​：利用关键字参数直接在构造函数中完成配置，保持简洁性。
- 所有语言实现需保持​**​一致的语义​**​，但API设计应符合语言习惯。

```go
// ================= Part1: 默认注册中心与构建模式 =================
package prometheus

import "sync"

// 默认注册中心（包级私有）
var (
	defaultRegistry     CollectorRegistry
	initDefaultRegistry sync.Once
)

// DefaultRegistry 获取默认注册中心（线程安全单例）
func DefaultRegistry() *CollectorRegistry {
	initDefaultRegistry.Do(func() {
		defaultRegistry = *NewCollectorRegistry()
	})
	return &defaultRegistry
}

// ================= Part2: 指标构建器模式实现 =================
// Option 配置选项类型
type Option func(*config)

type config struct {
	registry    *CollectorRegistry
	noRegister  bool
	labels      map[string]string
}

// WithLabels 设置标签的选项
func WithLabels(labels map[string]string) Option {
	return func(c *config) {
		c.labels = labels
	}
}

// WithRegistry 指定注册中心的选项
func WithRegistry(r *CollectorRegistry) Option {
	return func(c *config) {
		c.registry = r
	}
}

// WithNoRegistration 禁止自动注册的选项
func WithNoRegistration() Option {
	return func(c *config) {
		c.noRegister = true
	}
}

// ================= Part3: Counter 实现与自动注册 =================
// NewCounter 创建计数器（支持多种配置选项）
func NewCounter(name string, opts ...Option) *Counter {
	cfg := &config{
		registry: DefaultRegistry(), // 默认使用全局注册中心
	}

	// 应用配置选项
	for _, opt := range opts {
		opt(cfg)
	}

	c := &Counter{
		name:   name,
		labels: cfg.labels,
	}

	// 执行自动注册
	if !cfg.noRegister && cfg.registry != nil {
		cfg.registry.Register(c)
	}

	return c
}

// ================= Part4: 全局指标使用示例 =================
package api

import (
	"example/prometheus"
)

// 文件级全局指标（自动注册到默认注册中心）
var (
	HttpRequests = prometheus.NewCounter("http_requests_total", 
		prometheus.WithLabels(map[string]string{"handler": "/api"}))
	
	DBConnections = prometheus.NewGauge("db_connections",
		prometheus.WithLabels(map[string]string{"type": "mysql"}))
)

func HandleRequest() {
	HttpRequests.Inc() // 直接使用全局变量
}

// ================= Part5: 单元测试使用示例 =================
package api_test

import (
	"example/prometheus"
	"testing"
)

func TestHandler(t *testing.T) {
	// 创建不自动注册的计数器用于测试
	testCounter := prometheus.NewCounter("test_requests",
		prometheus.WithNoRegistration())

	testCounter.Inc()
	if testCounter.Value() != 1 {
		t.Error("Counter increment failed")
	}
}

// ================= Part6: Histogram 实现示例 =================
package prometheus

type Histogram struct {
	name    string
	labels  map[string]string
	buckets []float64
	mu      sync.Mutex
	counts  []uint64 // 每个桶的计数
}

// Observe 记录观测值
func (h *Histogram) Observe(value float64) {
	h.mu.Lock()
	defer h.mu.Unlock()

	// 寻找合适的桶
	for i, b := range h.buckets {
		if value <= b {
			h.counts[i]++
			return
		}
	}
	// 最后一个桶是 +Inf
	h.counts[len(h.counts)-1]++
}

// NewHistogram 创建直方图（必须实现至少一个高级指标）
func NewHistogram(name string, buckets []float64, opts ...Option) *Histogram {
	// ...类似Counter的配置处理...
	return &Histogram{
		// ...初始化字段...
	}
}
```
## 2.1 Counter

1. ​**​严格单调递增​**​：值只能增加或重置为0，不允许减少

2. ​**​必须包含方法​**​：

    - `Inc()` 增加1
    - `Inc(v)` 按给定值增加（需校验 `v ≥ 0`）(go 客户端为Add)

3. ​**​推荐功能​**​：统计代码块中的异常数量（如Python的`count_exceptions`）

4. ​**​初始值​**​：必须从0开始

```go
package metrics

import (
	"math"
	"sync/atomic"
)

type Counter struct {
	name  string
	value uint64
}

func NewCounter(name string) *Counter {
	return &Counter{
		name:  name,
		value: 0, // 强制初始化为0
	}
}

func (c *Counter) Inc() {
	atomic.AddUint64(&c.value, 1)
}

func (c *Counter) Add(v float64) {
	if v < 0 {
		panic("counter cannot decrease")
	}
	atomic.AddUint64(&c.value, uint64(math.Floor(v)))
}

func (c *Counter) Value() float64 {
	return float64(atomic.LoadUint64(&c.value))
}

func (c *Counter) Reset() {
	atomic.StoreUint64(&c.value, 0)
}

// 异常统计装饰器
func WithExceptionCounting(c *Counter, fn func()) {
	defer func() {
		if r := recover(); r != nil {
			c.Inc()
			panic(r)
		}
	}()
	fn()
}
```
## 2.2 Gauge

1. ​**​基础功能​**​
    
    - ​**​可增减数值​**​：表示瞬时值（如内存使用量、并发请求数）
    - ​**​必须方法​**​：
        - `Inc()`：+1
        - `Inc(v)`：+任意值（支持浮点）
        - `Dec()`：-1
        - `Dec(v)`：-任意值（支持浮点）
        - `Set(v)`：直接设值（允许任意数值）
    - ​**​初始值​**​：默认从0开始，可扩展支持自定义初始值
2. ​**​推荐功能​**​
    
    - `SetToCurrentTime()`：设为当前UNIX时间戳（秒级）
    - ​**​跟踪进行中请求​**​：自动增减计数器（如Python的`track_inprogress`）
    - ​**​测量代码耗时​**​：记录代码块执行时长（秒级精度）
3. ​**​设计约束​**​
    
    - 接口需与Histogram/Summary的计时模式兼容（但用`Set`代替`Observe`）
    - 线程安全（多协程并发安全）

```go
package prometheus

import (
	"sync"
	"time"
)

// Gauge 表示可上下浮动的数值指标，实现Prometheus规范要求的全部核心功能
type Gauge struct {
	mu    sync.RWMutex  // 读写锁保证线程安全
	value float64       // 当前指标值（允许正负）
	name  string        // 指标名称（符合Prometheus命名规范）
	start time.Time     // 用于计时功能的起始时间戳
}

// NewGauge 创建默认从0开始的Gauge
func NewGauge(name string) *Gauge {
	return &Gauge{
		name:  name,
		value: 0.0,
	}
}

// NewGaugeWithStart 创建带自定义初始值的Gauge（规范允许的扩展）
func NewGaugeWithStart(name string, initVal float64) *Gauge {
	return &Gauge{
		name:  name,
		value: initVal,
	}
}

// 核心方法实现 --------------------------------------------------------

// Inc 增加1（线程安全）
func (g *Gauge) Inc() {
	g.mu.Lock()
	defer g.mu.Unlock()
	g.value += 1.0
}

// Add 增加指定数值（允许任意浮点数）
func (g *Gauge) Add(v float64) {
	g.mu.Lock()
	defer g.mu.Unlock()
	g.value += v
}

// Dec 减少1（线程安全）
func (g *Gauge) Dec() {
	g.mu.Lock()
	defer g.mu.Unlock()
	g.value -= 1.0
}

// Sub 减少指定数值（允许任意浮点数）
func (g *Gauge) Sub(v float64) {
	g.mu.Lock()
	defer g.mu.Unlock()
	g.value -= v
}

// Set 设置绝对数值（线程安全）
func (g *Gauge) Set(v float64) {
	g.mu.Lock()
	defer g.mu.Unlock()
	g.value = v
}

// 推荐方法实现 --------------------------------------------------------

// SetToCurrentTime 设置为当前UNIX时间戳（秒级精度）
func (g *Gauge) SetToCurrentTime() {
	g.mu.Lock()
	defer g.mu.Unlock()
	g.value = float64(time.Now().Unix())
}

// TrackInProgress 跟踪进行中的请求（返回结束回调）
// 使用示例：defer gauge.TrackInProgress()()
func (g *Gauge) TrackInProgress() func() {
	g.Inc()
	return func() {
		g.Dec()
	}
}

// Time 测量代码执行时间（秒级精度）
// 使用示例：defer gauge.Time()()
func (g *Gauge) Time() func() {
	g.mu.Lock()
	g.start = time.Now() // 记录开始时间
	g.mu.Unlock()

	return func() {
		duration := time.Since(g.start).Seconds()
		g.Set(duration)
	}
}

// 辅助方法 --------------------------------------------------------

// Value 获取当前值（线程安全读取）
func (g *Gauge) Value() float64 {
	g.mu.RLock()
	defer g.mu.RUnlock()
	return g.value
}

/*
使用示例：

// 创建Gauge指标
cpuTemp := NewGauge("cpu_temperature")
activeRequests := NewGaugeWithStart("http_active_requests", 5.0)

// 基本操作
cpuTemp.Inc()         // +1
cpuTemp.Add(2.5)      // 当前值3.5
cpuTemp.Dec()         // 2.5
cpuTemp.Sub(1.5)      // 1.0
cpuTemp.Set(42.0)     // 直接设置

// 跟踪并发请求
func handleRequest() {
    defer activeRequests.TrackInProgress()()
    // 处理逻辑...
}

// 测量执行时间
func processBatch() {
    defer cpuTemp.Time()()
    // 批处理逻辑...
}

// 设置时间戳
cpuTemp.SetToCurrentTime()
*/
```
## 2.3 Summary

**​Summary​**​ 用于统计观察值（如请求耗时）的分布特征，提供以下核心数据：

- ​**​滑动窗口统计​**​：实时计算分位数（Quantile）、总数（_sum）、样本数（_count）
- ​**​不可聚合性​**​：分位数无法跨实例聚合，适用于单实例性能分析

> **​强制要求​**​

1. ​**​标签限制​**​：
    
    - 禁止使用 `quantile` 作为用户自定义标签（内部保留用于分位数标识）
2. ​**​默认行为​**​：
    
    - ​**​必须​**​ 默认只暴露 `_count`（总样本数）和 `_sum`（总和）
    - 分位数计算需​**​显式启用​**​（因计算开销大）
3. ​**​必须方法​**​：
    
    ```go
    Observe(v float64) // 记录观察值（如0.3秒）
    ```
    
4. ​**​初始值​**​：
    
    - `_count` 和 `_sum` 必须从0开始

```go
package prometheus

import (
	"sync"
	"time"
)

// Summary 实现Prometheus摘要指标
type Summary struct {
	mu         sync.Mutex
	count      uint64      // 样本总数
	sum        float64     // 观察值总和
	quantiles  []float64   // 需计算的分位数（如0.5,0.9）
	samples    []float64   // 存储原始样本（实际需用流式统计优化）
	name       string
}

// NewSummary 创建默认摘要（仅_count/_sum）
func NewSummary(name string) *Summary {
	return &Summary{
		name: name,
	}
}

// NewSummaryWithQuantiles 创建带分位数计算的摘要
func NewSummaryWithQuantiles(name string, quantiles []float64) *Summary {
	return &Summary{
		name:      name,
		quantiles: quantiles,
	}
}

// Observe 记录观察值（单位：秒）
func (s *Summary) Observe(v float64) {
	s.mu.Lock()
	defer s.mu.Unlock()

	s.count++
	s.sum += v

	// 简化的样本存储（实际应用需用流式统计库如go-fenix）
	if len(s.quantiles) > 0 {
		s.samples = append(s.samples, v)
	}
}

// Timer 获取计时器（自动记录耗时）
func (s *Summary) Timer() func() {
	start := time.Now()
	return func() {
		s.Observe(time.Since(start).Seconds())
	}
}

// 指标数据获取方法
func (s *Summary) Count() uint64 {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.count
}

func (s *Summary) Sum() float64 {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.sum
}

// 分位数计算（示例实现，实际需优化）
func (s *Summary) Quantile(q float64) float64 {
	s.mu.Lock()
	defer s.mu.Unlock()

	// 实际应使用TDigest等算法优化
	if len(s.samples) == 0 {
		return 0
	}
	// 简化的分位数计算（仅示例）
	return s.samples[int(float64(len(s.samples)-1)*q)]
}
```
## 2.4 Histogram

**Histogram​**​ 用于统计可聚合的事件分布（如请求延迟），通过预定义桶（Bucket）统计样本分布，提供：

- 各桶的样本计数（`_bucket{le="x"}`）
- 样本总数（`_count`）
- 样本总和（`_sum`）

>  ​**​强制要求​**​

1. ​**​标签限制​**​
    
    - 禁止用户使用 `le` 标签（内部保留用于桶边界）
2. ​**​桶配置​**​
    
    - ​**​必须​**​ 支持手动设置桶
    - ​**​推荐​**​ 提供线性/指数桶生成方法
    - 必须包含 `+Inf` 桶（自动添加）
3. ​**​方法要求​**​
    
    - `Observe(v float64)`：记录观察值（单位：秒）
    - ​**​推荐​**​ 提供计时器接口（如 `Timer()`）
4. ​**​初始值​**​
    
    - 所有计数器（`_count`、`_sum`、各桶）必须从0开始
5. ​**​不可变性​**​
    
    - 桶配置创建后不可修改

```go
package main

import (
	"fmt"
	"math"
	"sort"
	"strings"
	"sync"
	"time"
)

// Histogram 实现 Prometheus 直方图规范
type Histogram struct {
	mu      sync.Mutex    // 保证线程安全
	buckets []float64     // 排序后的桶边界（包含 +Inf）
	counts  []uint64      // 各桶的独立计数
	sum     float64       // 观察值总和
	count   uint64        // 总观察次数
	name    string        // 指标名称（用于输出）
}

// NewHistogram 创建直方图（自动处理 +Inf 桶）
func NewHistogram(name string, buckets []float64) *Histogram {
	// 1. 复制并排序桶
	sorted := make([]float64, len(buckets))
	copy(sorted, buckets)
	sort.Float64s(sorted)

	// 2. 添加 +Inf 桶（如果不存在）
	if len(sorted) == 0 || sorted[len(sorted)-1] != math.Inf(1) {
		sorted = append(sorted, math.Inf(1))
	}

	return &Histogram{
		name:    name,
		buckets: sorted,
		counts:  make([]uint64, len(sorted)),
	}
}

// Observe 记录观察值（单位：秒）
func (h *Histogram) Observe(v float64) {
	h.mu.Lock()
	defer h.mu.Unlock()

	// 更新总和和总计数
	h.sum += v
	h.count++

	// 查找第一个 >=v 的桶索引
	idx := sort.SearchFloat64s(h.buckets, v)
	if idx >= len(h.buckets) {
		idx = len(h.buckets) - 1
	}

	// 增加对应桶的计数
	h.counts[idx]++
}

// Timer 返回计时闭包（自动记录耗时）
func (h *Histogram) Timer() func() {
	start := time.Now()
	return func() {
		h.Observe(time.Since(start).Seconds())
	}
}

// String 生成 Prometheus 文本格式
func (h *Histogram) String() string {
	h.mu.Lock()
	defer h.mu.Unlock()

	var buf strings.Builder
	cumulative := uint64(0)

	// 生成每个桶的累积计数
	for i, bucket := range h.buckets {
		cumulative += h.counts[i]
		le := fmt.Sprintf("%f", bucket)
		if math.IsInf(bucket, 1) {
			le = "+Inf"
		}
		fmt.Fprintf(&buf, "%s_bucket{le=\"%s\"} %d\n", h.name, le, cumulative)
	}

	// 添加总和和总计数
	fmt.Fprintf(&buf, "%s_sum %f\n", h.name, h.sum)
	fmt.Fprintf(&buf, "%s_count %d\n", h.name, h.count)
	return buf.String()
}

// 桶生成工具函数 ---------------------------------------------------

// LinearBuckets 生成线性桶（起始值，间隔，数量）
func LinearBuckets(start, width float64, count int) []float64 {
	b := make([]float64, count)
	for i := range b {
		b[i] = start + float64(i)*width
	}
	return b
}

// ExponentialBuckets 生成指数桶（起始值，因子，数量）
func ExponentialBuckets(start, factor float64, count int) []float64 {
	b := make([]float64, count)
	current := start
	for i := range b {
		b[i] = current
		current *= factor
	}
	return b
}

// 示例使用 -----------------------------------------------------------------

func main() {
	// 1. 创建直方图（使用指数桶）
	hist := NewHistogram("http_request_duration_seconds", 
		ExponentialBuckets(0.05, 2, 5)) // 生成 0.05, 0.1, 0.2, 0.4, 0.8

	// 2. 记录观察值
	hist.Observe(0.12)
	hist.Observe(0.25)
	hist.Observe(0.6)

	// 3. 使用计时器
	func() {
		defer hist.Timer()()
		time.Sleep(350 * time.Millisecond) // 自动记录 0.35 秒
	}()

	// 4. 输出指标
	fmt.Println(hist.String())

	/* 输出示例：
	http_request_duration_seconds_bucket{le="0.050000"} 0
	http_request_duration_seconds_bucket{le="0.100000"} 0
	http_request_duration_seconds_bucket{le="0.200000"} 2
	http_request_duration_seconds_bucket{le="0.400000"} 3
	http_request_duration_seconds_bucket{le="0.800000"} 4
	http_request_duration_seconds_bucket{le="+Inf"} 4
	http_request_duration_seconds_sum 1.420000
	http_request_duration_seconds_count 4
	*/
}
```
## 2.5 指标规范

>  **1. 指标命名规则​**​

- ​**​格式要求​**​：  
    必须符合 `[namespace]_[subsystem]_name` 格式，其中 `name` 为必填，其他可选。  
    合法示例：`http_requests_total`、`node_memory_usage_bytes`
    
- ​**​禁止动态名称​**​：  
    避免动态生成指标名称（如 `api_<method>_requests`），应改用标签：  
    `api_requests_total{method="GET"}`
    
> ​**​2. 指标描述要求​**​

- ​**​强制要求​**​：  
    Gauge/Counter/Summary/Histogram 必须提供描述（Help 文本）。  
    自定义 Collector 中的指标也必须包含描述。
    
- ​**​推荐实践​**​：  
    描述应清晰说明指标用途，官方库示例需保持高质量文档。

> **​3. 数据展示规范​**​

- ​**​输出格式​**​：  
    必须支持 Prometheus 文本格式（text-based exposition format）。
    
- ​**​顺序要求​**​：  
    鼓励对指标进行稳定排序（如按字母顺序），前提是不显著影响性能。
### 2.5.1 指标命名规范

 > ** 命名规范​**​

- ​**​清晰明确​**​：指标名称需让熟悉 Prometheus 的用户能快速理解其含义。  
    ✅ 正确示例：`http_incoming_requests_total`（明确用途）  
    ❌ 避免示例：`requests_total`（含义模糊）
    
- ​**​子系统关联​**​：每个指标应严格对应一个子系统或文件。  
    ✅ 示例：`kafka_message_queue_size`（Kafka 消息队列大小）
    
- ​**​前缀规范​**​：
    
    - 应用指标应添加导出器名称前缀，如 `haproxy_up`。
    - 保留前缀 `process_` 和 `scrape_` 需谨慎使用，例如 `jmx_scrape_duration_seconds`。

> ​**​2. 单位与数据格式​**​

- ​**​基础单位​**​：使用秒（`seconds`）、字节（`bytes`）等标准单位，避免转换（如毫秒）。  
    ✅ 正确示例：`request_duration_seconds`  
    ❌ 错误示例：`request_duration_millis`
    
- ​**​比率与百分比​**​：
    
    - 暴露两个独立计数器而非百分比，例如：
        
        ```prometheus
        http_requests_total{status="success"} 1000
        http_requests_total{status="failed"} 50
        ```
        
    - 计算失败率：`rate(http_requests_total{status="failed"}[5m]) /  rate(http_requests_total[5m])`


 > ​**​3. 命名格式​**​

- ​**​蛇形命名法​**​（`snake_case`）：  
    ✅ 示例：`node_cpu_usage_seconds`  
    ❌ 避免驼峰式：`nodeCPUUsageSeconds`
    
- ​**​合法字符​**​：仅使用 `[a-zA-Z0-9_:]`，冒号（`:`）保留给记录规则。  
    ✅ 正确示例：`api:http_requests_total`（记录规则）  
    ❌ 错误示例：`api.http.requests.total`

> ​**​4. 后缀与类型匹配​**​

- ​**​保留后缀​**​：`_sum`、`_count`、`_bucket` 和 `_total` 后缀用于摘要、直方图和计数器。除非您要生成其中之一，否则请避免使用这些后缀。
    
- ​**​避免滥用​**​：非上述类型的指标不得使用这些后缀。

> ​**​5. 特殊场景处理​**​

- ​**​成功/失败指标​**​：
    
    - 使用独立指标而非标签：
        
        ```prometheus
        http_successful_requests_total 950
        http_failed_requests_total 50
        ```
        
    - 计算失败率：`http_failed_requests_total / (http_successful_requests_total + http_failed_requests_total)`
- ​**​领域特定名称​**​：
    
    - 对 SNMP、网络设备等保留原名，但在帮助信息中说明。
    
    ```prometheus
    # HELP snmp_ifHCInOctets SNMP 接口输入字节数 (原名 ifHCInOctets)
    # TYPE snmp_ifHCInOctets counter
    snmp_ifHCInOctets{ifIndex="1"} 123456
    ```
## 2.6 标签

> **1. 标签一致性要求​**​

- ​**​同一指标标签名必须一致​**​  
    同一指标（如 Counter、Gauge）的不同实例​**​禁止​**​使用不同标签名。例如：  
    ✅ 合法：`http_requests_total{method="GET"}`, `http_requests_total{method="POST"}`  
    ❌ 非法：`http_requests_total{method="GET"}`, `http_requests_total{status="200"}`
    
- ​**​自定义收集器标签建议​**​  
    建议自定义 Collector 保持标签名一致，但客户端库​**​不强制验证​**​，以支持少数特殊场景。
    

> ​**​2. API 设计原则​**​

- ​**​标签可选性​**​  
    API 应支持标签但不强制使用，允许创建无标签指标：
    
    ```go
    // 无标签指标
    counter := NewCounter("requests_total", "Total requests")
    
    // 带标签指标
    labeledCounter := NewCounter("requests_total", "Total requests", "method", "status")
    ```
    
- ​**​标签名验证​**​  
    客户端库​**​必须验证​**​标签名合法性（仅允许 `[a-zA-Z0-9_]` 且不以数字开头）。

> ​**​3. 标签操作方法​**​

- ​**​Child 模式​**​  
    通过 `labels()` 方法获取带标签的指标实例（Child）：
    
    ```go
    // 获取 Child 实例
    getCounter := counter.Labels("GET", "200")
    getCounter.Inc()
    ```
    
- ​**​缓存优化​**​  
    Child 实例应支持缓存，避免重复查找开销：
    
    ```go
    // 提前缓存高频率使用的标签组合
    successCounter := apiCounter.Labels("200")
    for req := range requests {
        successCounter.Inc()
    }
    ```
    
- ​**​生命周期管理​**​
    
    - ​**​remove()​**​：删除指定标签的 Child，停止导出数据。
    - ​**​clear()​**​：删除所有 Child，重置指标。

    ```go
    // 删除特定标签的指标
    apiCounter.Remove("GET", "500")
    
    // 清空所有标签实例
    apiCounter.Clear()
    ```

> ​**​4. 初始化要求​**​

- ​**​无标签指标必须初始化​**​  
    避免因未初始化导致指标缺失：

    ```go
    // 正确：显式初始化
    totalRequests := NewCounter("requests_total", "Help").Labels() 
    
    // 错误：未初始化的指标可能不存在
    // （客户端库应自动初始化无标签指标）
    ```
    
>  ​**​5. 标签策略​**​

- ​**​避免指标名称包含标签​**​：  
    ✅ 正确示例：`cache_operations_total` + 标签 `{type="hit"}`  
    ❌ 错误示例：`cache_hits_total`（标签值不应成为指标名）
    
- ​**​高基数处理​**​：
    
    - 当单一指标标签组合过多时，拆分为多个指标（如按操作类型拆分）。
    - 示例：`db_query_duration_seconds{operation="select"}`, `db_query_duration_seconds{operation="insert"}
# 3 推送指标

有时，需要监控无法抓取的组件。这 [Prometheus Pushgateway](https://github.com/prometheus/pushgateway) 允许将时间序列从[短期服务级别批处理作业](https://prometheus.io/docs/practices/pushing/)推送到 Prometheus 可以抓取的中间作业。结合 Prometheus 基于文本的简单公开格式，这使得在没有客户端库的情况下，甚至可以轻松插桩 shell 脚本。

有关从 Go 中使用的信息，请参阅 [Push](https://godoc.org/github.com/prometheus/client_golang/prometheus/push#Pusher.Push) 和 [Add](https://godoc.org/github.com/prometheus/client_golang/prometheus/push#Pusher.Add) 方法。
# 4 配置规范

> **1. 导出器设计原则​**​

- ​**​开箱即用​**​：  
    默认导出所有核心指标，无需用户额外配置，仅需指定监控目标地址。
    
- ​**​灵活过滤​**​：  
    提供指标过滤功能，允许按需禁用高开销或细粒度指标（如 HAProxy 的每服务器统计）。
    
- ​**​性能优化​**​：  
    高成本指标默认关闭，用户可手动开启（如大集群中的详细资源跟踪）。

> **2. 配置最佳实践​**​

- ​**​零配置优先​**​：  
    默认提供完整监控覆盖，降低用户启动门槛。
    
- ​**​示例配置库​**​：  
    为复杂场景提供预置配置模板（如 Kafka 主题监控、JVM 线程分析）。
    
- ​**​渐进式引导​**​：  
    通过注释说明配置项作用，帮助用户理解高级功能

> **3. 标准化配置格式​**​

- ​**​强制使用 YAML​**​：  
    所有配置文件必须采用 YAML 格式，保持生态统一性。
