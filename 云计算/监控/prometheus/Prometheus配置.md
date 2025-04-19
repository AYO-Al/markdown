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
## 3.3 基于文件的服务发现

- **动态更新​**​：通过外部工具（如Ansible）生成目标列表文件，Prometheus监听文件变化。
```yaml
scrape_configs:
  - job_name: 'file-sd'
    file_sd_configs:
      - files: ['/etc/prometheus/targets/*.json']

# 文件格式
[
  {
    "targets": ["10.0.0.3:8080"],
    "labels": { "service": "api", "region": "us-west" }
  }
]
```
## 3.4 DNS服务发现

- **动态DNS记录​**​：通过SRV或A记录解析目标地址。
```yaml
scrape_configs:
  - job_name: 'dns-sd'
    dns_sd_configs:
      - names: ['_prometheus._tcp.example.com']
        type: SRV
        port: 9100
```

## 3.5 抓取参数

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
# 7 alertmanager配置

Alertmanager 的配置是其告警处理的核心，定义了告警的路由、分组、抑制、通知方式等规则。

```yaml
global:          # 全局配置（所有接收器的默认设置）
route:           # 告警路由的根节点
receivers:       # 告警接收者定义（如邮件、Slack、Webhook）
inhibit_rules:   # 告警抑制规则
templates:       # 自定义通知模板文件路径
```
## 7.1 全局配置

```yaml
global:
  resolve_timeout: 5m          # 告警恢复后持续通知的时间（防抖动）
  smtp_smarthost: 'smtp.example.com:25'  # SMTP服务器地址
  smtp_from: 'alertmanager@example.com' # 发件人邮箱
  smtp_auth_username: 'user'
  smtp_auth_password: 'pass'
  smtp_require_tls: true        # 强制使用TLS
  slack_api_url: 'https://hooks.slack.com/services/...'  # Slack Webhook URL
  http_config:                  # HTTP客户端配置（代理、TLS）
    proxy_url: 'http://proxy:8080'
    tls_config:
      ca_file: '/path/to/ca.pem'
```
## 7.2 路由配置

该配置定义告警如何被分组、过滤和路由到接收器。路由树支持嵌套。

|字段|说明|
|---|---|
|`receiver`|默认接收器名称（必须存在）。|
|`group_by`|分组依据的标签（如 `[cluster, alertname]`）。|
|`group_wait`|初次发送告警前的等待时间（默认 `30s`，收集同组告警）。|
|`group_interval`|相同组告警的间隔时间（默认 `5m`）。|
|`repeat_interval`|重复发送未修复告警的间隔（默认 `4h`）。|
|`routes`|子路由列表（支持嵌套匹配）。|
|`match` / `match_re`|标签精确匹配或正则匹配。|
```yaml
route:
  receiver: 'default-email'     # 默认接收器
  group_by: [alertname, cluster]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 12h
  routes:                       # 子路由规则
  - match:                      
      severity: 'critical'
    receiver: 'pagerduty-team'
    continue: false             # 匹配后停止后续路由
  - match_re:
      team: '^(frontend|backend)$'
    receiver: 'slack-notify'
    routes:                     # 嵌套子路由
    - match:
        environment: 'prod'
      receiver: 'prod-slack'
```
## 7.3 接收器

定义告警通知的发送目标，每个接收器可配置多种通知方式（如同时发邮件和Slack）。
## 7.4 抑制规则

防止特定条件下重复发送告警（如网络故障时抑制服务不可达告警）。

```yaml
# 抑制规则（减少冗余告警）
inhibit_rules:
# 规则1：当网络不可达时，抑制相关服务告警
- source_match:
    alertname: NetworkDown     # 源告警名称
    severity: critical         # 源告警级别
  target_match:
    severity: warning          # 被抑制的目标告警级别
  equal: ['cluster']           # 要求cluster标签值相同才抑制

# 规则2：主机宕机时抑制其上的所有服务告警
- source_match:
    alertname: HostDown
  target_match_re:
    instance: '^.*$'           # 匹配所有实例
  equal: ['instance']          # 抑制相同实例的其他告警

```
## 7.5 自定义模板

通过 Go 模板引擎定制通知内容格式，需指定模板文件路径。

- 定义模板文件

```html
{{ define "email.custom.html" }}
<h2>告警列表（{{ len .Alerts }}条）</h2>
{{ range .Alerts }}
  <p><strong>告警名称</strong>: {{ .Labels.alertname }}</p>
  <p><strong>主机</strong>: {{ .Labels.instance }}</p>
  <p><strong>时间</strong>: {{ .StartsAt.Format "2006-01-02 15:04:05" }}</p>
  <hr>
{{ end }}
{{ end }}
```

- 配置文件引用模板

```yaml
templates:
- '/etc/alertmanager/templates/*.tmpl'
```
## 7.6 完整示例

```yaml
# alertmanager.yml

# 全局配置（所有接收器的默认设置）
global:
  # 告警恢复后持续发送通知的时间（防止短暂恢复后再次触发）
  resolve_timeout: 5m
  # SMTP服务器配置（会被接收器中的email_configs覆盖）
  smtp_smarthost: 'smtp.example.com:587'
  smtp_from: 'alertmanager@example.com'
  smtp_auth_username: 'admin@example.com'
  smtp_auth_password: 'password123'
  smtp_require_tls: true  # 强制使用TLS加密
  
  # Slack Webhook URL（会被接收器中的slack_configs覆盖）
  slack_api_url: 'https://hooks.slack.com/services/TXXXXXX/BXXXXXX/XXXXXX'

# 告警路由树的根节点配置
route:
  # 默认接收器（必须与receivers中的某个name对应）
  receiver: 'default-email'
  # 分组依据的标签，相同标签值的告警会被合并
  group_by: ['alertname', 'cluster', 'service']
  # 初次发送告警前的等待时间（等待30秒以收集同组告警）
  group_wait: 30s
  # 同一组告警下次发送的时间间隔（若未修复，每5分钟发送一次）
  group_interval: 5m
  # 重复发送未修复告警的间隔（每3小时重复提醒）
  repeat_interval: 3h
  
  # 子路由规则（按顺序匹配）
  routes:
  # 路由1：严重级别为critical的告警发送到pagerduty
  - match:
      severity: critical
    receiver: 'pagerduty-team'
    # 是否继续匹配后续路由（false表示匹配到此终止）
    continue: false
  
  # 路由2：服务名为web或db的告警发送到Slack
  - match_re:
      service: ^(web|db)$
    receiver: 'slack-notify'
    # 子路由：生产环境的告警单独路由到另一个Slack频道
    routes:
    - match:
        environment: prod
      receiver: 'prod-slack'

# 接收器列表（定义告警通知发送到哪里）
receivers:
# 接收器1：默认邮件通知
- name: 'default-email'
  email_configs:
  - to: 'admin@example.com'      # 收件人
    send_resolved: true         # 发送恢复通知
    # 自定义邮件主题
    headers:
      Subject: '[ALERT] {{ .CommonLabels.severity }}: {{ .CommonLabels.alertname }}'

# 接收器2：PagerDuty通知
- name: 'pagerduty-team'
  pagerduty_configs:
  - service_key: 'pd_api_key_123'  # PagerDuty集成的API密钥
    severity: 'critical'           # 设置事件严重级别
    # 自定义事件详情
    details:
      firing: '{{ .Alerts | len }}个告警触发'
      summary: '{{ .CommonAnnotations.summary }}'

# 接收器3：Slack通知（非生产环境）
- name: 'slack-notify'
  slack_configs:
  - channel: '#alerts'           # Slack频道
    title: '{{ .CommonLabels.alertname }}'  # 消息标题
    # 消息正文（使用模板语法）
    text: |-
      *描述*: {{ .CommonAnnotations.description }}
      *环境*: {{ .CommonLabels.environment }}
      *详情链接*: <{{ .GeneratorURL }}|查看>
    send_resolved: true          # 发送恢复通知
    # 自定义颜色（warning: 黄色, critical: 红色）
    color: '{{ if eq .CommonLabels.severity "critical" }}danger{{ else }}warning{{ end }}'

# 接收器4：生产环境专用Slack频道
- name: 'prod-slack'
  slack_configs:
  - channel: '#prod-alerts'
    title: '生产告警: {{ .CommonLabels.alertname }}'

# 抑制规则（减少冗余告警）
inhibit_rules:
# 规则1：当网络不可达时，抑制相关服务告警
- source_match:
    alertname: NetworkDown     # 源告警名称
    severity: critical         # 源告警级别
  target_match:
    severity: warning          # 被抑制的目标告警级别
  equal: ['cluster']           # 要求cluster标签值相同才抑制

# 规则2：主机宕机时抑制其上的所有服务告警
- source_match:
    alertname: HostDown
  target_match_re:
    instance: '^.*$'           # 匹配所有实例
  equal: ['instance']          # 抑制相同实例的其他告警

# 自定义模板文件路径（可选）
templates:
- '/etc/alertmanager/templates/*.tmpl'
```