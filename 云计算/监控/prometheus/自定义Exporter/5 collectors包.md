以下是 Prometheus Go 客户端库中 `collectors` 包的常用组件整理：

| ​**​Collector 名称​**​       | ​**​用途​**​                 | ​**​常用指标示例​**​                                                                   | ​**​备注​**​                                              |
| -------------------------- | -------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------- |
| ​**​GoCollector​**​        | 收集 Go 运行时指标                | `go_goroutines`（当前协程数）  <br>`go_gc_duration_seconds`（GC 耗时统计）                    | 默认自动注册，提供 Go 进程的运行时状态（GC、内存、协程等）。                       |
| ​**​ProcessCollector​**​   | 收集进程级资源使用情况                | `process_cpu_seconds_total`（CPU 占用时间）  <br>`process_resident_memory_bytes`（内存占用） | 需手动注册，监控进程的 CPU、内存、文件描述符等系统资源。                          |
| ​**​DBStatsCollector​**​   | 数据库连接池统计（如 `database/sql`） | `db_connections_open`（打开连接数）  <br>`db_connections_wait_duration_seconds`（等待耗时）   | 需结合具体数据库驱动实现，通常基于 `sql.DBStats` 结构生成指标。                 |
| ​**​BuildInfoCollector​**​ | 暴露应用版本信息                   | `app_info{version="1.0.0"}`（应用元数据）                                               | 需自定义实现，通过常量标签记录版本、Commit 等构建信息。                         |
| ​**​Custom Collectors​**​  | 用户自定义指标采集逻辑                | 如 `custom_requests_total`（自定义请求计数）                                               | 需实现 `Collector` 接口的 `Describe` 和 `Collect` 方法，灵活适配业务场景。 |

### 关键说明：

1. ​**​自动注册​**​：`GoCollector` 通常在初始化时通过 `prometheus.NewGoCollector()` 自动注册。
2. ​**​手动注册​**​：`ProcessCollector` 需调用 `prometheus.NewProcessCollector()` 并显式注册到 `prometheus.Register()`。
3. ​**​数据库集成​**​：`DBStatsCollector` 的实现依赖于具体数据库驱动（如 PostgreSQL/MySQL 的监控库），非标准库内置。
4. ​**​自定义实践​**​：`BuildInfoCollector` 是常见实践示例，需用户自行实现以暴露应用元数据。
5. ​**​扩展性​**​：通过实现自定义 `Collector` 接口，可采集任意指标（如业务逻辑、外部系统状态）。

### 示例代码片段：

```go
import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/collectors"
)

func main() {
    // 注册 GoCollector 和 ProcessCollector
    registry := prometheus.NewRegistry()
    registry.MustRegister(collectors.NewGoCollector())
    registry.MustRegister(collectors.NewProcessCollector(collectors.ProcessCollectorOpts{}))
    
    // 自定义指标和采集逻辑（示例）
    customCollector := NewCustomCollector()
    registry.MustRegister(customCollector)
}
```

通过合理利用这些 Collector，可以快速为 Go 应用添加丰富的监控指标，并集成到 Prometheus 生态中。