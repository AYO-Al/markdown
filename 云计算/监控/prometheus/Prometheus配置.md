# 1 配置文件结构

```yaml
global:           # 全局配置（抓取间隔、超时等）
scrape_configs:   # 定义抓取目标（监控对象）
alerting:         # 告警管理器（Alertmanager）配置
rule_files:       # 告警规则文件路径
remote_write:     # 远程存储写入配置（如 Thanos、InfluxDB）
remote_read:      # 远程存储读取配置
```
# 2 全局配置

```yaml
global:
  scrape_interval: 15s      # 默认抓取间隔（可被单个任务覆盖）
  evaluation_interval: 15s  # 规则评估间隔（告警规则和记录规则）
  scrape_timeout: 10s       # 单次抓取超时时间

  # 外部标签（附加到所有时间序列和告警）
  external_labels:
    region: "us-west"
    env: "prod"

```
# 3 数据抓取配置

定义需要监控的目标（如服务器、数据库、应用），支持静态配置或动态服务发现。
## 3.1 静态配置
```yaml
# 静态配置
scrape_configs:
  - job_name: "node_exporter"    # 任务名称（唯一标识）
    static_configs:
      - targets: ["192.168.1.10:9100", "192.168.1.11:9100"]  # 监控目标地址
    # 重命名标签（可选）
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - source_labels: []
        target_label: job
        replacement: "node_exporter_custom"
```
## 3.2 动态服务发现

```yaml
scrape_configs:
  - job_name: "kubernetes-pods"
    kubernetes_sd_configs:       # 使用 Kubernetes 服务发现
      - role: pod                # 发现所有 Pod
    relabel_configs:
      # 仅抓取包含注解 prometheus.io/scrape: "true" 的 Pod
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      # 从 Pod 注解中提取抓取路径和端口
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2

```
## 3.3 抓取参数

- `metrics_path`: 指标路径（默认 `/metrics`）
- `scheme`: 协议（`http` 或 `https`）
- `basic_auth`: 基础认证
- `tls_config`: TLS 证书配置
# 4 告警配置
## 4.1 告警规则文件

```yaml
rule_files:
  - "rules/node_alerts.yml"    # 告警规则文件路径
  - "rules/custom_*.yml"       # 支持通配符
```
## 4.2 Alertmanager配置

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]  # Alertmanager 地址
      # 配置请求超时和 TLS
      timeout: 10s
      scheme: http
```
# 5 存储与远程读写
## 5.1 远程写入

```yaml
remote_write:
  - url: "http://thanos-receive:19291/api/v1/receive"
    queue_config:
      max_samples_per_send: 1000  # 每批发送最大样本数
      capacity: 10000             # 队列容量
    write_relabel_configs:        # 过滤需写入的指标
      - source_labels: [job]
        regex: "node|kubelet"
        action: keep
```
## 5.2 远程读取

```yaml
remote_read:
  - url: "http://thanos-query:10902/api/v1/read"
    read_recent: true   # 同时查询本地和远程数据
```
# 6 完整示例

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 30s
  external_labels:
    cluster: "my-cluster"

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "node_exporter"
    static_configs:
      - targets: ["node1:9100", "node2:9100"]
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

rule_files:
  - "/etc/prometheus/rules/*_alerts.yml"

remote_write:
  - url: "http://thanos:10901/api/v1/receive"

```