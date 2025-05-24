通过访问 `/metrics` 路径我们可以看到所有的类似于以下格式的样本数据。

```go
# HELP net_conntrack_listener_conn_closed_total Total number of connections closed that were made to the listener of a given name.
# TYPE net_conntrack_listener_conn_closed_total counter
net_conntrack_listener_conn_closed_total{listener_name="http"} 16
```

其中非#开头的每一行表示当前Node Exporter采集到的一个监控样本：net_conntrack_listener_conn_closed_total表明了当前指标的名称、大括号中的标签则反映了当前样本的一些特征和维度、浮点数则是该监控样本的具体值。
# 1 样本

Prometheus会将所有采集到的样本数据以时间序列（time-series）的方式保存在内存数据库中，并且定时保存到硬盘上。time-series是按照时间戳和值的序列顺序存放的，我们称之为向量(vector)。向量是某个时间点的时间序列集合。每条time-series通过指标名称(metrics name)和一组标签集(labelset)命名。如下所示，可以将time-series理解为一个以时间为Y轴的数字矩阵：

```
  ^
  │   . . . . . . . . . . . . . . . . .   . .   node_cpu{cpu="cpu0",mode="idle"}
  │     . . . . . . . . . . . . . . . . . . .  node_cpu{cpu="cpu0",mode="system"}
  │     . . . . . . . . . .   . . . . . . . .   node_load1{}
  │     . . . . . . . . . . . . . . . .   . .  
  v
    <------------------ 时间 ---------------->
```

在time-series中的每一个点称为一个样本（sample），样本由以下三部分组成：

- 指标(metric)：metric name和描述当前样本特征的labelsets;
    
- 时间戳(timestamp)：一个精确到毫秒的时间戳;
    
- 样本值(value)： 一个float64的浮点型数据表示当前样本的值。
    - 如果同一时间有多条数据，只会保留最后一条丢弃其他值。
# 2 指标

在形式上，所有的指标(Metric)都通过如下格式标示：
```
<metric name>{<label name>=<label value>, ...}
```

指标的名称(metric name)可以反映被监控样本的含义（比如，`http_request_total` - 表示当前系统接收到的HTTP请求总量）。指标名称只能由ASCII字符、数字、下划线以及冒号组成并必须符合正则表达式`[a-zA-Z_:][a-zA-Z0-9_:]*`。

标签(label)反映了当前样本的特征维度，通过这些维度Prometheus可以对样本数据进行过滤，聚合等。标签的名称只能由ASCII字符、数字以及下划线组成并满足正则表达式`[a-zA-Z_][a-zA-Z0-9_]*`。

其中以`__`作为前缀的标签，是系统保留的关键字，只能在系统内部使用。标签的值则可以包含任何Unicode编码的字符。在Prometheus的底层实现中指标名称实际上是以`__name__=<metric name>`的形式保存在数据库中的，因此以下两种方式均表示的同一条time-series：
```
api_http_requests_total{method="POST", handler="/messages"}

{__name__="api_http_requests_total"，method="POST", handler="/messages"}
```
# 3 Metrics类型

从存储上来讲所有的监控指标metric都是相同的，但是在不同的场景下这些metric又有一些细微的差异。 例如，在Node Exporter返回的样本中指标node_load1反应的是当前系统的负载状态，随着时间的变化这个指标返回的样本数据是在不断变化的。而指标node_cpu所获取到的样本数据却不同，它是一个持续增大的值，因为其反应的是CPU的累积使用时间，从理论上讲只要系统不关机，这个值是会无限变大的。

为了能够帮助用户理解和区分这些不同监控指标之间的差异，Prometheus定义了4种不同的指标类型(metric type)：Counter（计数器）、Gauge（仪表盘）、Histogram（直方图）、Summary（摘要）。

在Exporter返回的样本数据中，其注释中也包含了该样本的类型。例如：
```
# HELP net_conntrack_listener_conn_closed_total Total number of connections closed that were made to the listener of a given name.
# TYPE net_conntrack_listener_conn_closed_total counter
net_conntrack_listener_conn_closed_total{listener_name="http"} 16
```
## 3.1 Counter：只增不减的计数器

Counter类型的指标其工作方式和计数器一样，只增不减（除非系统发生重置）。常见的监控指标，如http_requests_total，node_cpu都是Counter类型的监控指标。 一般在定义Counter类型指标的名称时推荐使用_total作为后缀。

Counter是一个简单但有强大的工具，例如我们可以在应用程序中记录某些事件发生的次数，通过以时序的形式存储这些数据，我们可以轻松的了解该事件产生速率的变化。 PromQL内置的聚合操作和函数可以让用户对这些数据进行进一步的分析：

例如，通过rate()函数获取HTTP请求量的增长率：

```
rate(http_requests_total[5m])
```

查询当前系统中，访问量前10的HTTP地址：

```
topk(10, http_requests_total)
```
## 3.2 Gauge：可增可减的仪表盘

与Counter不同，Gauge类型的指标侧重于反应系统的当前状态。因此这类指标的样本数据可增可减。常见指标如：node_memory_MemFree（主机当前空闲的内容大小）、node_memory_MemAvailable（可用内存大小）都是Gauge类型的监控指标。

通过Gauge指标，用户可以直接查看系统的当前状态：

```
node_memory_MemFree
```

对于Gauge类型的监控指标，通过PromQL内置函数delta()可以获取样本在一段时间返回内的变化情况。例如，计算CPU温度在两个小时内的差异：

```
delta(cpu_temp_celsius{host="zeus"}[2h])
```

还可以使用deriv()计算样本的线性回归模型，甚至是直接使用predict_linear()对数据的变化趋势进行预测。例如，预测系统磁盘空间在4个小时之后的剩余情况：

```
predict_linear(node_filesystem_free{job="node"}[1h], 4 * 3600)
```
## 3.3 Histogram和Summary：分析数据分布情况

在大多数情况下人们都倾向于使用某些量化指标的平均值，例如CPU的平均使用率、页面的平均响应时间。这种方式的问题很明显，以系统API调用的平均响应时间为例：如果大多数API请求都维持在100ms的响应时间范围内，而个别请求的响应时间需要5s，那么就会导致某些WEB页面的响应时间落到中位数的情况，而这种现象被称为长尾问题。

为了区分是平均的慢还是长尾的慢，最简单的方式就是按照请求延迟的范围进行分组。例如，统计延迟在0~10ms之间的请求数有多少而10~20ms之间的请求数又有多少。通过这种方式可以快速分析系统慢的原因。Histogram和Summary都是为了能够解决这样问题的存在，通过Histogram和Summary类型的监控指标，我们可以快速了解监控样本的分布情况。

例如，指标prometheus_tsdb_wal_fsync_duration_seconds的指标类型为Summary。 它记录了Prometheus Server中wal_fsync处理的处理时间，通过访问Prometheus Server的/metrics地址，可以获取到以下监控样本数据：

```
# HELP prometheus_tsdb_wal_fsync_duration_seconds Duration of WAL fsync.
# TYPE prometheus_tsdb_wal_fsync_duration_seconds summary
prometheus_tsdb_wal_fsync_duration_seconds{quantile="0.5"} 0.012352463
prometheus_tsdb_wal_fsync_duration_seconds{quantile="0.9"} 0.014458005
prometheus_tsdb_wal_fsync_duration_seconds{quantile="0.99"} 0.017316173
prometheus_tsdb_wal_fsync_duration_seconds_sum 2.888716127000002
prometheus_tsdb_wal_fsync_duration_seconds_count 216
```

从上面的样本中可以得知当前Prometheus Server进行wal_fsync操作的总次数为216次，耗时2.888716127000002s。其中中位数（quantile=0.5）的耗时为0.012352463，9分位数（quantile=0.9）的耗时为0.014458005s。

在Prometheus Server自身返回的样本数据中，我们还能找到类型为Histogram的监控指标prometheus_tsdb_compaction_chunk_range_bucket。

```
# HELP prometheus_tsdb_compaction_chunk_range Final time range of chunks on their first compaction
# TYPE prometheus_tsdb_compaction_chunk_range histogram
prometheus_tsdb_compaction_chunk_range_bucket{le="100"} 0
prometheus_tsdb_compaction_chunk_range_bucket{le="400"} 0
prometheus_tsdb_compaction_chunk_range_bucket{le="1600"} 0
prometheus_tsdb_compaction_chunk_range_bucket{le="6400"} 0
prometheus_tsdb_compaction_chunk_range_bucket{le="25600"} 0
prometheus_tsdb_compaction_chunk_range_bucket{le="102400"} 0
prometheus_tsdb_compaction_chunk_range_bucket{le="409600"} 0
prometheus_tsdb_compaction_chunk_range_bucket{le="1.6384e+06"} 260
prometheus_tsdb_compaction_chunk_range_bucket{le="6.5536e+06"} 780
prometheus_tsdb_compaction_chunk_range_bucket{le="2.62144e+07"} 780
prometheus_tsdb_compaction_chunk_range_bucket{le="+Inf"} 780
prometheus_tsdb_compaction_chunk_range_sum 1.1540798e+09
prometheus_tsdb_compaction_chunk_range_count 780
```

与Summary类型的指标相似之处在于Histogram类型的样本同样会反应当前指标的记录的总数(以_count作为后缀)以及其值的总量（以_sum作为后缀）。不同在于Histogram指标直接反应了在不同区间内样本的个数，区间通过标签len进行定义。

同时对于Histogram的指标，我们还可以通过histogram_quantile()函数计算出其值的分位数。不同在于Histogram通过histogram_quantile函数是在服务器端计算的分位数。 而Sumamry的分位数则是直接在客户端计算完成。因此对于分位数的计算而言，Summary在通过PromQL进行查询时有更好的性能表现，而Histogram则会消耗更多的资源。反之对于客户端而言Histogram消耗的资源更少。在选择这两种方式时用户应该按照自己的实际场景进行选择。

| ​**​特性​**​      | ​**​Histogram​**​ | ​**​Summary​**​ |
| --------------- | ----------------- | --------------- |
| ​**​分位数计算时机​**​ | 查询时               | 客户端预先计算         |
| ​**​精度控制​**​    | 依赖桶配置             | 可配置误差范围         |
| ​**​跨实例聚合​**​   | 支持                | 不支持             |
| ​**​存储开销​**​    | 高（每个桶一个时间序列）      | 中（每个分位数一个序列）    |
| ​**​客户端计算开销​**​ | 低（仅计数）            | 高（需实时计算分位数）     |
| ​**​适用场景​**​    | 全局分位数、灵活查询        | 单实例高精度分位数       |
# 4 PromQL

Prometheus通过指标名称（metrics name）以及对应的一组标签（labelset）唯一定义一条时间序列。指标名称反映了监控样本的基本标识，而label则在这个基本特征上为采集到的数据提供了多种特征维度。用户可以基于这些特征维度过滤，聚合，统计从而产生新的计算后的一条时间序列。

PromQL（Prometheus Query Language）是专为 Prometheus 设计的时间序列数据查询语言，用于实时分析和告警。它支持复杂的聚合、运算和预测功能，适用于监控场景中的多维数据分析。

PromQL 有四种基本数据类型：

1. ​**​即时向量（Instant Vector）​**​
    
    - ​**​定义​**​：某单一时间戳下的一组时间序列数据。
    - ​**​示例​**​：`http_requests_total{status="200"}`（当前时刻状态码为200的请求总数）。
2. ​**​范围向量（Range Vector）​**​
    
    - ​**​定义​**​：某时间段内的多个时间序列数据点集合。
    - ​**​示例​**​：`http_requests_total{status="200"}[5m]`（过去5分钟内状态码为200的请求总数）。
3. ​**​标量（Scalar）​**​
    
    - ​**​定义​**​：单一数值，无时间维度。
    - **限制**：标量不能作为查询的最终结果，必须与向量结合。
    - ​**​示例​**​：`42` 或 `sum(http_requests_total)`（所有请求的总和）。
4. ​**​字符串（String）​**​
    
    - ​**​定义​**​：文本类型，主要用于注释或展示（实际查询中极少使用）。
    - **限制**：字符串不能存储在时间序列数据库中。
    - ​**​示例​**​：`"Hello, Prometheus!"`。
## 4.1 查询语法

当Prometheus通过Exporter采集到相应的监控指标样本数据后，我们就可以通过PromQL对监控样本数据进行查询。

当我们直接使用监控指标名称查询时，可以查询该指标下的所有时间序列。如：

```
http_requests_total
```

等同于：

```
http_requests_total{}
```

该表达式会返回指标名称为http_requests_total的所有时间序列：

```
http_requests_total{code="200",handler="alerts",instance="localhost:9090",job="prometheus",method="get"}=(20889@1518096812.326)
http_requests_total{code="200",handler="graph",instance="localhost:9090",job="prometheus",method="get"}=(21287@1518096812.326)
```

PromQL还支持用户根据时间序列的标签匹配模式来对时间序列进行过滤，目前主要支持两种匹配模式：完全匹配和正则匹配。

>  完全匹配模式

PromQL支持使用`=`和`!=`两种完全匹配模式：

- 通过使用`label=value`可以选择那些标签满足表达式定义的时间序列；
    
- 反之使用`label!=value`则可以根据标签匹配排除时间序列；

例如，如果我们只需要查询所有http_requests_total时间序列中满足标签instance为localhost:9090的时间序列，则可以使用如下表达式：

```
http_requests_total{instance="localhost:9090"}
```

反之使用`instance!="localhost:9090"`则可以排除这些时间序列：

```
http_requests_total{instance!="localhost:9090"}
```

多个匹配器可用于同一标签名称;它们都必须通过才能返回结果。

```
http_requests_total{replica!="rep-a",replica=~"rep.*"}
```

> 正则匹配模式

除了使用完全匹配的方式对时间序列进行过滤以外，PromQL还可以支持使用正则表达式作为匹配条件，多个表达式之间使用`|`进行分离：

- 使用`label=~regx`表示选择那些标签符合正则表达式定义的时间序列；
    
- 反之使用`label!~regx`进行排除；

例如，如果想查询多个环节下的时间序列序列可以使用如下表达式：

```
http_requests_total{environment=~"staging|testing|development",method!="GET"}
```
## 4.2 范围查询

直接通过类似于PromQL表达式`http_requests_total`查询时间序列时，返回值中只会包含该时间序列中的最新的一个样本值，这样的返回结果我们称之为**瞬时向量**。而相应的这样的表达式称之为**瞬时向量表达式**。

而如果我们想过去一段时间范围内的样本数据时，我们则需要使用**区间向量表达式**。区间向量表达式和瞬时向量表达式之间的差异在于在区间向量表达式中我们需要定义时间选择的范围，时间范围通过时间范围选择器`[]`进行定义。例如，通过以下表达式可以选择最近5分钟内的所有样本数据：

```
http_requests_total{}[5m：] // 过去5min，步长默认等于全局 `evaluation_interval`（通常1m）。

```

该表达式将会返回查询到的时间序列中最近5分钟的所有样本数据：

```
http_requests_total{code="200",handler="alerts",instance="localhost:9090",job="prometheus",method="get"}=[
    1@1518096812.326
    1@1518096817.326
    1@1518096822.326
    1@1518096827.326
    1@1518096832.326
    1@1518096837.325
]
http_requests_total{code="200",handler="graph",instance="localhost:9090",job="prometheus",method="get"}=[
    4 @1518096812.326
    4@1518096817.326
    4@1518096822.326
    4@1518096827.326
    4@1518096832.326
    4@1518096837.325
]
```

通过区间向量表达式查询到的结果我们称为**区间向量**。

除了使用m表示分钟以外，PromQL的时间范围选择器支持其它时间单位：

| 单位   | 描述  | 示例    |
| ---- | --- | ----- |
| `ms` | 毫秒  | `2ms` |
| `s`  | 秒   | `10s` |
| `m`  | 分钟  | `5m`  |
| `h`  | 小时  | `2h`  |
| `d`  | 天   | `7d`  |
| `w`  | 周   | `2w`  |
| `y`  | 年   | `2y`  |

> 时间位移操作

时间选择器 `[]` 可以与时间偏移选择器 `offset` 配合使用。左开右闭。

```promql
http_requests_total{job="api-server"} offset 1d  # 24小时前的瞬时值

# 对比今日与昨日同一时间段的请求速率
rate(http_requests_total[5m]) - rate(http_requests_total[5m] offset 1d)

```

> 指定时间点操作

还可以与时间点选择器 `@` 配合使用。

```promql
# 查询2023-01-01 00:00时的过去5分钟请求速率
rate(http_requests_total[5m] @ 1672531200)
```

**仅支持UTC时间戳**：

- **统一性​**​：Unix 时间戳是跨平台和编程语言的时间表示标准（如 `1629450000` 表示 2021-08-20 00:00:00 UTC）。
- ​**​时区无关性​**​：避免因时区转换导致的歧义，Prometheus 内部所有时间均以 UTC 处理。
## 4.3 合法的promql表达式

所有的PromQL表达式都必须至少包含一个指标名称(例如http_request_total)，或者一个不会匹配到空字符串的标签过滤器(例如{code="200"})。

因此以下两种方式，均为合法的表达式：

```
http_request_total # 合法
http_request_total{} # 合法
{method="get"} # 合法
```

而如下表达式，则不合法：

```
{job=~".*"} # 不合法
```

同时，除了使用`<metric name>{label=value}`的形式以外，我们还可以使用内置的`__name__`标签来指定监控指标名称：

```
{__name__=~"http_request_total"} # 合法
{__name__=~"node_disk_bytes_read|node_disk_bytes_written"} # 合法
```
## 4.4 PromQL操作符

使用PromQL除了能够方便的按照查询和过滤时间序列以外，PromQL还支持丰富的操作符，用户可以使用这些操作符对进一步的对事件序列进行二次加工。这些操作符包括：数学运算符，逻辑运算符，布尔运算符等等。

**Prometheus对空值的任何运算结果仍然是空值，如果想设置默认值可以使用以下方式**

```promql
# vector将标量转换为向量
# 逻辑运算符两侧必须都是向量
(node_cpu_seconds_total{cpu="19"} or vector(0)) + 1
```
### 4.4.1 数学运算

例如，我们可以通过指标node_memory_free_bytes_total获取当前主机可用的内存空间大小，其样本单位为Bytes。这是如果客户端要求使用MB作为单位响应数据，那只需要将查询到的时间序列的样本值进行单位换算即可：

```
node_memory_free_bytes_total / (1024 * 1024)
```

node_memory_free_bytes_total表达式会查询出所有满足表达式条件的时间序列，在上一小节中我们称该表达式为瞬时向量表达式，而返回的结果成为瞬时向量。

当瞬时向量与标量之间进行数学运算时，数学运算符会依次作用域瞬时向量中的每一个样本值，从而得到一组新的时间序列。

而如果是瞬时向量与瞬时向量之间进行数学运算时，过程会相对复杂一点。 例如，如果我们想根据node_disk_bytes_written和node_disk_bytes_read获取主机磁盘IO的总量，可以使用如下表达式：

```
node_disk_bytes_written + node_disk_bytes_read
```

那这个表达式是如何工作的呢？依次找到与左边向量元素匹配（标签完全一致）的右边向量元素进行运算，如果没找到匹配元素，则直接丢弃。同时新的时间序列将不会包含指标名称。 该表达式返回结果的示例如下所示：

```
{device="sda",instance="localhost:9100",job="node_exporter"}=>1634967552@1518146427.807 + 864551424@1518146427.807
{device="sdb",instance="localhost:9100",job="node_exporter"}=>0@1518146427.807 + 1744384@1518146427.807
```

PromQL支持的所有数学运算符如下所示：

|运算符|描述|示例|
|---|---|---|
|`+`|加法|`http_requests_total + 10`|
|`-`|减法|`memory_used - memory_cached`|
|`*`|乘法|`node_disk_bytes_read * 8`（转bit）|
|`/`|除法|`bytes_total / 1024^2`（转MB）|
|`%`|取模|`http_requests_total % 1000`|
|`^`|幂运算|`2 ^ (instance_count)`|

**特性​**​：

- ​**​标量混合运算​**​：支持向量与标量运算（如 `vector * 2`）。
- ​**​单位转换​**​：常用于字节转换（如 `B → MB`）。
- ​**​标签保留​**​：结果继承输入向量的所有标签。
### 4.4.2 布尔运算符

在PromQL通过标签匹配模式，用户可以根据时间序列的特征维度对其进行查询。而布尔运算则支持用户根据时间序列中样本的值，对时间序列进行过滤。

例如，通过数学运算符我们可以很方便的计算出，当前所有主机节点的内存使用率：

```
(node_memory_bytes_total - node_memory_free_bytes_total) / node_memory_bytes_total
```

而系统管理员在排查问题的时候可能只想知道当前内存使用率超过95%的主机呢？通过使用布尔运算符可以方便的获取到该结果：

```
(node_memory_bytes_total - node_memory_free_bytes_total) / node_memory_bytes_total > 0.95
```

瞬时向量与标量进行布尔运算时，PromQL依次比较向量中的所有时间序列样本的值，如果比较结果为true则保留，反之丢弃。

瞬时向量与瞬时向量直接进行布尔运算时，同样遵循默认的匹配模式：依次找到与左边向量元素匹配（标签完全一致）的右边向量元素进行相应的操作，如果没找到匹配元素，则直接丢弃。

目前，Prometheus支持以下布尔运算符如下：

|运算符|描述|示例|
|---|---|---|
|`==`|等于|`up == 1`|
|`!=`|不等于|`status_code != 200`|
|`>`|大于|`cpu_usage > 90`|
|`<`|小于|`latency_ms < 100`|
|`>=`|大于等于|`queue_size >= 1000`|
|`<=`|小于等于|`temperature <= 30`|
- ​**​布尔过滤​**​：结果为 `1`（真）或空（假），可用 `bool` 修饰符生成布尔值。
- ​**​条件筛选​**​：常用于告警规则中的阈值判断。

```promql
node_cpu_seconds_total{cpu="0"} >= 6 # 输出原值

node_cpu_seconds_total{cpu="0"} >= bool 6 # 生成布尔值丢弃原值
```
### 4.4.3 逻辑运算符

使用瞬时向量表达式能够获取到一个包含多个时间序列的集合，我们称为瞬时向量。 通过集合运算，可以在两个瞬时向量与瞬时向量之间进行相应的集合操作。目前，Prometheus支持以下集合运算符：

| 运算符      | 描述  | 示例                                        |
| -------- | --- | ----------------------------------------- |
| `and`    | 与   | `error_rate > 0.1 and request_rate > 100` |
| `or`     | 或   | `cpu_temp > 80 or env_temp > 40`          |
| `unless` | 排除  | `up unless up{env="test"}`（排除测试环境）        |
- `vector1 and vector2`：返回 ​**​两个向量中标签完全匹配的时间序列​**​，且保留 ​**​左侧向量的值​**​（右侧向量的值被忽略）。
- `vector1 or vector2`：返回 ​**​两个向量中所有时间序列的并集​**​，但若存在 ​**​标签完全相同的序列​**​，则仅保留 ​**​左侧向量​**​ 的值。
- `vector1 unless vector2`：返回 ​**​左侧向量中存在，但右侧向量中不存在标签完全匹配项​**​ 的所有时间序列。
### 4.4.4 向量匹配运算符

控制不同向量之间的标签匹配方式，解决多对多关联问题。

> **匹配模式​**​

| 修饰符                 | 描述        |
| ------------------- | --------- |
| `on (labels)`       | 仅按指定标签匹配  |
| `ignoring (labels)` | 排除指定标签后匹配 |

 > ​**​扩展模式​**​

|修饰符|描述|
|---|---|
|`group_left (labels)`|左侧向量标签多于右侧|
|`group_right (labels)`|右侧向量标签多于左侧|
在结果中保留左(右)侧的指定标签（即使这些标签未参与匹配）。保留的标签不能和on匹配一样。

- `on(label3)` 要求该标签必须匹配，但 `group_left(label3)` 又试图将其视为左侧的额外标签保留。
- Prometheus 禁止这种冲突，因为它无法确定标签 `label3` 的归属（是匹配标签还是保留标签）。
### 4.4.5 符号优先级

PromQL 操作符按以下优先级从高到低执行（可使用括号改变顺序）：

1. `^`
2. `*`, `/`, `%`
3. `+`, `-`
4. `==`, `!=`, `>`, `<`, `>=`, `<=`
5. `and`, `unless`
6. `or`
## 4.5 匹配模式

向量与向量之间进行运算操作时会基于默认的匹配规则：依次找到与左边向量元素匹配（标签完全一致）的右边向量元素进行运算，如果没找到匹配元素，则直接丢弃。

在 PromQL 中，​**​向量匹配模式（Vector Matching）​**​ 用于控制不同时间序列之间的标签对齐规则，确保运算仅在符合条件的序列间进行。

-  **忽略标签匹配​**​：
    
    ```promql
    # 错误：未指定标签匹配，可能导致笛卡尔积
    memory_used / memory_total
    # 修复：按 instance 匹配
    memory_used / on(instance) memory_total
    ```

### 4.5.1 一对一匹配

一对一匹配模式会从操作符两边表达式获取的瞬时向量依次比较并找到唯一匹配(标签完全一致)的样本值。默认情况下，使用表达式：

```
vector1 <operator> vector2
```

在操作符两边表达式标签不一致的情况下，可以使用on(label list)或者ignoring(label list）来修改便签的匹配行为。使用ignoreing可以在匹配时忽略某些便签。而on则用于将匹配行为限定在某些便签之内。

```
<vector expr> <bin-op> ignoring(<label list>) <vector expr>
<vector expr> <bin-op> on(<label list>) <vector expr>
```

例如当存在样本：

```
method_code:http_errors:rate5m{method="get", code="500"}  24
method_code:http_errors:rate5m{method="get", code="404"}  30
method_code:http_errors:rate5m{method="put", code="501"}  3
method_code:http_errors:rate5m{method="post", code="500"} 6
method_code:http_errors:rate5m{method="post", code="404"} 21

method:http_requests:rate5m{method="get"}  600
method:http_requests:rate5m{method="del"}  34
method:http_requests:rate5m{method="post"} 120
```

使用PromQL表达式：

```
method_code:http_errors:rate5m{code="500"} / ignoring(code) method:http_requests:rate5m
```

该表达式会返回在过去5分钟内，HTTP请求状态码为500的在所有请求中的比例。如果没有使用ignoring(code)，操作符两边表达式返回的瞬时向量中将找不到任何一个标签完全相同的匹配项。

因此结果如下：

```
{method="get"}  0.04            //  24 / 600
{method="post"} 0.05            //   6 / 120
```

同时由于method为put和del的样本找不到匹配项，因此不会出现在结果当中。
### 4.5.2 多对一和一对多

多对一和一对多两种匹配模式指的是“一”侧的每一个向量元素可以与"多"侧的多个元素匹配的情况。在这种情况下，必须使用group修饰符：group_left或者group_right来确定哪一个向量具有更高的基数（充当“多”的角色）。

```
<vector expr> <bin-op> ignoring(<label list>) group_left(<label list>) <vector expr>
<vector expr> <bin-op> ignoring(<label list>) group_right(<label list>) <vector expr>
<vector expr> <bin-op> on(<label list>) group_left(<label list>) <vector expr>
<vector expr> <bin-op> on(<label list>) group_right(<label list>) <vector expr>
```

多对一和一对多两种模式一定是出现在操作符两侧表达式返回的向量标签不一致的情况。**因此需要使用ignoring和on修饰符来排除或者限定匹配的标签列表。**

例如,使用表达式：

```
method_code:http_errors:rate5m / ignoring(code) group_left method:http_requests:rate5m
```

该表达式中，左向量`method_code:http_errors:rate5m`包含两个标签method和code。而右向量`method:http_requests:rate5m`中只包含一个标签method，因此匹配时需要使用ignoring限定匹配的标签为code。 在限定匹配标签后，右向量中的元素可能匹配到多个左向量中的元素 因此该表达式的匹配模式为多对一，需要使用group修饰符group_left指定左向量具有更好的基数。

最终的运算结果如下：

```
{method="get", code="500"}  0.04            //  24 / 600
{method="get", code="404"}  0.05            //  30 / 600
{method="post", code="500"} 0.05            //   6 / 120
{method="post", code="404"} 0.175           //  21 / 120
```

> 提醒：group修饰符只能在比较和数学运算符中使用。在逻辑运算and,unless和or才注意操作中默认与右向量中的所有元素进行匹配。

**PromQL ​​不支持多对多匹配​，需通过聚合或调整标签维度将问题转化为多对一或一对多模式。且group修饰符会默认保留多的一侧全部表情，可以通过group left(label)指定保留什么标签**
## 4.6 聚合操作

Prometheus还提供了下列内置的聚合操作符，这些操作符作用于**瞬时向量**。可以将瞬时表达式返回的样本数据根据标签进行聚合，形成一个新的时间序列。

| 操作符                | 描述                                      | 示例                                                                 |
| ------------------ | --------------------------------------- | ------------------------------------------------------------------ |
| `sum()`            | 对分组内的值求和                                | `sum(http_requests_total) by (cluster)`（按集群统计总请求量）                 |
| `min()`            | 返回分组内的最小值                               | `min(node_cpu_usage) by (instance)`（按实例统计最低 CPU 使用率）               |
| `max()`            | 返回分组内的最大值                               | `max(container_memory_usage_bytes) by (namespace)`（按命名空间统计最大内存使用量） |
| `avg()`            | 计算分组内的平均值                               | `avg(rate(network_bytes_total[5m])) by (region)`（按区域统计平均网络流量）      |
| `stddev()`         | 计算分组内值的样本标准差                            | `stddev(disk_latency_seconds) by (device)`（按磁盘设备统计延迟标准差）           |
| `stdvar()`         | 计算分组内值的样本方差                             | `stdvar(node_temperature) by (datacenter)`（按数据中心统计温度方差）            |
| `count()`          | 统计分组内时间序列的数量                            | `count(up == 1) by (job)`（按作业统计健康实例数）                              |
| `count_values()`   | 统计指定值的出现次数，生成 `__value__` 标签            | `count_values("status", http_responses_total)`（统计不同 HTTP 状态码的出现次数） |
| `bottomk(k, ...)`  | 返回分组内最小的 `k` 个值（按值升序）                   | `bottomk(3, node_disk_free_bytes)`（显示磁盘剩余空间最小的 3 个节点）              |
| `topk(k, ...)`     | 返回分组内最大的 `k` 个值（按值降序）                   | `topk(5, rate(http_errors_total[5m]))`（显示错误率最高的 5 个服务）             |
| `quantile(φ, ...)` | 计算分组内值的分位数（`φ ∈ [0,1]`，如 `0.95` 表示 P95） | `quantile(0.95, http_request_duration_seconds)`（按接口统计 P95 延迟）      |
| `group()`          | 将所有值设为 `1`，用于统计存在性                      | `group(container_running) by (namespace)`（统计各命名空间中处于运行状态的容器数量）     |

使用聚合操作的语法如下：

```
<aggr-op>([parameter,] <vector expression>) [without|by (<label list>)]
```

其中只有`count_values`, `quantile`, `topk`, `bottomk`支持参数(parameter)。

without用于从计算结果中移除列举的标签，而保留其它标签。by则正好相反，结果向量中只保留列出的标签，其余标签则移除。通过without和by可以按照样本的问题对数据进行聚合。
## 4.7 内置函数

想查看内置函数详细列表可以查看[内置函数](https://prometheus.io/docs/prometheus/latest/querying/functions/)。

| 函数名称                                              | 描述                                              | 示例                                                                               |
| ------------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------- |
| ​**​`rate(v range-vector)`​**​                    | 计算范围向量中​**​计数器（Counter）​**​的每秒平均增长率（自动处理计数器重置）。 | `rate(http_requests_total[5m])`（过去5分钟的每秒请求速率）                                    |
| ​**​`irate(v range-vector)`​**​                   | 基于范围向量中​**​最后两个样本​**​计算瞬时速率（对短期波动敏感）。           | `irate(node_network_receive_bytes_total[2m])`（当前网络接收速率）                          |
| ​**​`increase(v range-vector)`​**​                | 计算范围向量中的​**​绝对增量​**​（适用于计数器）。                   | `increase(http_errors_total[1h])`（过去1小时的总错误数）                                    |
| ​**​`sum()`/`avg()`/`min()`/`max()`​**​           | 对向量求和、平均值、最小值、最大值。                              | `sum(rate(http_requests_total[5m])) by (service)`（按服务统计总请求速率）                    |
| ​**​`histogram_quantile(φ, v)`​**​                | 计算​**​直方图指标​**​的分位数（φ∈[0,1]，如0.9表示P90）。         | `histogram_quantile(0.95, sum(rate(http_duration_bucket[5m])) by (le))`（全局P95延迟） |
| ​**​`predict_linear(v, t)`​**​                    | 基于范围向量的线性回归，预测未来`t`秒后的值。                        | `predict_linear(node_filesystem_free_bytes[6h], 3600 * 4)`（预测4小时后磁盘剩余空间）         |
| ​**​`label_replace(v, dst, repl, src, regex)`​**​ | 通过正则表达式修改标签（如提取子字符串）。                           | `label_replace(up, "ip", "$1", "instance", "([0-9.]+):.*")`（从`instance`标签提取IP地址） |
| ​**​`time()`​**​                                  | 返回当前时间的Unix时间戳（秒）。                              | `time() - process_start_time_seconds`（计算服务运行时长）                                  |
| ​**​`absent()`​**​                                | 检测指标是否不存在（用于监控数据缺失告警）。                          | `absent(up{job="api"})`（如果所有`api`实例宕机，返回1）                                       |
| ​**​`resets()`​**​                                | 统计计数器在时间范围内的重置次数。                               | `resets(http_requests_total[24h])`（过去24小时请求计数器的重置次数）                             |
| ​**​`clamp_min()`/`clamp_max()`​**​               | 限制指标值的下限或上限。                                    | `clamp_min(node_memory_used_bytes, 1024^3)`（内存使用低于1GB时显示为1GB）                    |
| ​**​`scalar()`​**​                                | 将单元素向量转换为标量。                                    | `scalar(count(up))`（返回健康实例总数的标量值）                                                |
## 4.8 子查询

子查询（Subquery）是 PromQL 中一种嵌套查询结构，允许在另一个查询内部对历史数据进行二次计算。它的核心目的是在单个查询中实现 ​**​多级时间窗口分析​**​ 或 ​**​动态时间范围统计​**​。

```promql
<函数名>(<指标>[<子查询时间范围>:<子查询步长>])
```

| 参数                  | 说明                                                                                           |
| ------------------- | -------------------------------------------------------------------------------------------- |
| ​**​`<函数名>`​**​     | 作用于子查询结果的聚合函数（如 `avg_over_time`、`max_over_time`等所有范围向量函数）。                                   |
| ​**​`<指标>`​**​      | 被查询的原始指标。                                                                                    |
| ​**​`<子查询时间范围>`​**​ | 子查询覆盖的历史数据范围（如 `7d` 表示过去7天）。                                                                 |
| ​**​`<子查询步长>`​**​   | 可选参数，定义子查询的执行间隔（默认等于全局 `evaluation_interval`）。应合理设置步长，- 步长越小 → 结果精度越高 → 性能开销越大。步长应 >= 数据采集间隔 |
1. ​**​多级时间窗口聚合​**​
    
    - 示例：先按 1 小时窗口计算均值，再统计过去 7 天内的最大值。

    ```promql
    max_over_time(avg_over_time(cpu_usage[1h])[7d:1h])
    ```
    
2. ​**​动态时间范围分析​**​
    
    - 示例：统计过去 30 天内每天的请求量趋势。
    
    ```promql
    avg_over_time(sum(http_requests_total)[30d:1d])
    ```
    
3. ​**​复杂阈值检测​**​
    
    - 示例：判断某指标在过去 1 小时内是否有超过 5 分钟持续高于阈值。
    
    ```promql
    count_over_time((cpu_usage > 90)[1h:1m]) >= 5
    ```