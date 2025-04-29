`promhttp` 是 Prometheus 客户端库中用于 ​**​通过 HTTP 暴露指标数据​**​ 的核心包。它提供了标准化的方式将注册表（`Registry`）中的指标转换为 HTTP 端点（如 `/metrics`），供 Prometheus Server 抓取。
# 1 核心函数
## 1.1 Handler` 与 `HandlerFor

| ​**​函数​**​                                                     | ​**​说明​**​                                  |
| -------------------------------------------------------------- | ------------------------------------------- |
| `func Handler() http.Handler`                                  | 使用默认注册表（`prometheus.DefaultRegistry`）生成处理器。 |
| `func HandlerFor(reg Registry, opts HandlerOpts) http.Handler` | 自定义注册表和配置生成处理器（更灵活）。                        |

​**​示例​**​：

```go
// 使用默认注册表
http.Handle("/metrics", promhttp.Handler())

// 使用自定义注册表
registry := prometheus.NewRegistry()
```

## 1.2 HandlerOpts类型

```go
type HandlerOpts struct {
	// ErrorLog specifies an optional Logger for errors collecting and
	// serving metrics. If nil, errors are not logged at all. Note that the
	// type of a reported error is often prometheus.MultiError, which
	// formats into a multi-line error string. If you want to avoid the
	// latter, create a Logger implementation that detects a
	// prometheus.MultiError and formats the contained errors into one line.
	ErrorLog Logger
	// ErrorHandling defines how errors are handled. Note that errors are
	// logged regardless of the configured ErrorHandling provided ErrorLog
	// is not nil.
	ErrorHandling HandlerErrorHandling
	// If Registry is not nil, it is used to register a metric
	// "promhttp_metric_handler_errors_total", partitioned by "cause". A
	// failed registration causes a panic. Note that this error counter is
	// different from the instrumentation you get from the various
	// InstrumentHandler... helpers. It counts errors that don't necessarily
	// result in a non-2xx HTTP status code. There are two typical cases:
	// (1) Encoding errors that only happen after streaming of the HTTP body
	// has already started (and the status code 200 has been sent). This
	// should only happen with custom collectors. (2) Collection errors with
	// no effect on the HTTP status code because ErrorHandling is set to
	// ContinueOnError.
	Registry prometheus.Registerer
	// DisableCompression disables the response encoding (compression) and
	// encoding negotiation. If true, the handler will
	// never compress the response, even if requested
	// by the client and the OfferedCompressions field is set.
	DisableCompression bool
	// OfferedCompressions is a set of encodings (compressions) handler will
	// try to offer when negotiating with the client. This defaults to identity, gzip
	// and zstd.
	// NOTE: If handler can't agree with the client on the encodings or
	// unsupported or empty encodings are set in OfferedCompressions,
	// handler always fallbacks to no compression (identity), for
	// compatibility reasons. In such cases ErrorLog will be used if set.
	OfferedCompressions []Compression
	// The number of concurrent HTTP requests is limited to
	// MaxRequestsInFlight. Additional requests are responded to with 503
	// Service Unavailable and a suitable message in the body. If
	// MaxRequestsInFlight is 0 or negative, no limit is applied.
	MaxRequestsInFlight int
	// If handling a request takes longer than Timeout, it is responded to
	// with 503 ServiceUnavailable and a suitable Message. No timeout is
	// applied if Timeout is 0 or negative. Note that with the current
	// implementation, reaching the timeout simply ends the HTTP requests as
	// described above (and even that only if sending of the body hasn't
	// started yet), while the bulk work of gathering all the metrics keeps
	// running in the background (with the eventual result to be thrown
	// away). Until the implementation is improved, it is recommended to
	// implement a separate timeout in potentially slow Collectors.
	Timeout time.Duration
	// If true, the experimental OpenMetrics encoding is added to the
	// possible options during content negotiation. Note that Prometheus
	// 2.5.0+ will negotiate OpenMetrics as first priority. OpenMetrics is
	// the only way to transmit exemplars. However, the move to OpenMetrics
	// is not completely transparent. Most notably, the values of "quantile"
	// labels of Summaries and "le" labels of Histograms are formatted with
	// a trailing ".0" if they would otherwise look like integer numbers
	// (which changes the identity of the resulting series on the Prometheus
	// server).
	EnableOpenMetrics bool
	// EnableOpenMetricsTextCreatedSamples specifies if this handler should add, extra, synthetic
	// Created Timestamps for counters, histograms and summaries, which for the current
	// version of OpenMetrics are defined as extra series with the same name and "_created"
	// suffix. See also the OpenMetrics specification for more details
	// https://github.com/prometheus/OpenMetrics/blob/v1.0.0/specification/OpenMetrics.md#counter-1
	//
	// Created timestamps are used to improve the accuracy of reset detection,
	// but the way it's designed in OpenMetrics 1.0 it also dramatically increases cardinality
	// if the scraper does not handle those metrics correctly (converting to created timestamp
	// instead of leaving those series as-is). New OpenMetrics versions might improve
	// this situation.
	//
	// Prometheus introduced the feature flag 'created-timestamp-zero-ingestion'
	// in version 2.50.0 to handle this situation.
	EnableOpenMetricsTextCreatedSamples bool
	// ProcessStartTime allows setting process start timevalue that will be exposed
	// with "Process-Start-Time-Unix" response header along with the metrics
	// payload. This allow callers to have efficient transformations to cumulative
	// counters (e.g. OpenTelemetry) or generally _created timestamp estimation per
	// scrape target.
	// NOTE: This feature is experimental and not covered by OpenMetrics or Prometheus
	// exposition format.
	ProcessStartTime time.Time
}

```

`HandlerOpts` 用于定制处理器行为，以下是关键字段的表格说明：

| ​**​字段名​**​           | ​**​类型​**​          | ​**​默认值​**​ | ​**​作用​**​                                             |
| --------------------- | ------------------- | ----------- | ------------------------------------------------------ |
| `ErrorHandling`       | `HTTPErrorHandling` | `ServeHTTP` | 指标收集错误时的处理策略                                           |
| `Timeout`             | `time.Duration`     | 无超时         | 收集指标的最大等待时间（防止慢收集器阻塞 HTTP 请求）。                         |
| `EnableOpenMetrics`   | `bool`              | `false`     | 是否支持 OpenMetrics 格式（如 `application/openmetrics-text`）。 |
| `Registry`            | `Registry`          | 无           | 指定要暴露的注册表（通常通过 `HandlerFor` 的 `reg` 参数传递）。             |
| `MaxRequestsInFlight` | `int`               | 无限制         | 并发处理的最大请求数（防止高负载导致 OOM）。                               |
| `DisableCompression`  | `bool`              | `false`     | 禁用响应压缩（默认启用 GZIP）。                                     |
## 1.3 HTTPErrorHandling类型

- 作用：HandlerErrorHandling 定义 Handler 提供指标将如何处理错误。

```go
type HandlerErrorHandling int
```

```go
const (
	// Serve an HTTP status code 500 upon the first error
	// encountered. Report the error message in the body. Note that HTTP
	// errors cannot be served anymore once the beginning of a regular
	// payload has been sent. Thus, in the (unlikely) case that encoding the
	// payload into the negotiated wire format fails, serving the response
	// will simply be aborted. Set an ErrorLog in HandlerOpts to detect
	// those errors.
	HTTPErrorOnError HandlerErrorHandling = iota
	// Ignore errors and try to serve as many metrics as possible.  However,
	// if no metrics can be served, serve an HTTP status code 500 and the
	// last error message in the body. Only use this in deliberate "best
	// effort" metrics collection scenarios. In this case, it is highly
	// recommended to provide other means of detecting errors: By setting an
	// ErrorLog in HandlerOpts, the errors are logged. By providing a
	// Registry in HandlerOpts, the exposed metrics include an error counter
	// "promhttp_metric_handler_errors_total", which can be used for
	// alerts.
	ContinueOnError
	// Panic upon the first error encountered (useful for "crash only" apps).
	PanicOnError
)
```

当指标收集（`Collect` 方法）失败时，`promhttp` 提供以下三种处理方式：

|​**​策略​**​|​**​常量值​**​|​**​行为​**​|
|---|---|---|
|终止请求并返回 500|`HTTPErrorOnError`|返回 HTTP 500 错误，日志记录错误信息（适合生产环境）。|
|忽略错误继续处理|`ContinueOnError`|跳过错误指标，返回部分数据（适合容忍部分失败的场景）。|
|触发 panic|`PanicOnError`|直接触发 panic（适合测试环境快速定位问题）。|
# 2 示例

```go
func main() {
    // 创建独立注册表
    registry := prometheus.NewRegistry()
    counter := prometheus.NewCounter(prometheus.CounterOpts{Name: "my_counter"})
    registry.MustRegister(counter)

    // 配置处理器
    opts := promhttp.HandlerOpts{
        EnableOpenMetrics: true,
        ErrorHandling:     promhttp.ContinueOnError,
    }
    handler := promhttp.HandlerFor(registry, opts)

    // 暴露端点
    http.Handle("/metrics", handler)
    http.ListenAndServe(":8080", nil)
}
```