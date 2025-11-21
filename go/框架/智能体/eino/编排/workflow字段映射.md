**1. 基础字段映射 `MapFields`**

这是最常用、最直观的映射方式，适用于简单的字段对接。

```go
// 假设节点A输出类型为 SourceOutput { TaskID string; Query string }
// 假设节点B输入类型为 DestInput { JobID string; Question string }

wf.AddLambdaNode("nodeB", processor).
   AddInput("nodeA", compose.MapFields("TaskID", "JobID"), 
                         compose.MapFields("Query", "Question"))
// 这会将 nodeA 输出的 TaskID 映射到 nodeB 输入的 JobID，Query 映射到 Question。
```


**2. 整体到局部的映射 `ToField`**

当你需要将上一个节点的全部输出结果，作为当前节点输入的一部分时，这个功能非常有用。它体现了Workflow**控制流与数据流分离**的特点：一个节点的输入可以灵活地从多个前驱节点的输出中抽取不同部分组合而成。

```go
// 假设我们需要组合来自不同节点的数据
// 节点A输出：用户资料 UserProfile { Name string }
// 节点B输出：当前时间 CurrentTime { Timestamp string }
// 节点C输入：需要组合信息 FullInput { UserInfo UserProfile; Context string; TimeInfo string }

wf.AddLambdaNode("nodeC", complexProcessor).
   AddInput("nodeA", compose.ToField("UserInfo")). // 将整个UserProfile对象放入UserInfo字段
   AddInput("nodeB", compose.ToField("TimeInfo"))  // 将整个CurrentTime对象放入TimeInfo字段
// 至于 Context 字段，可以从START节点或其他节点映射，或使用默认值。
```


**3. 局部到整体的映射 `FromField`**

这个API常用于从上游的一个复杂结果中，只抽取某个关键字段给下游节点处理。

```go
// 节点A完成复杂验证，输出 ValidationResult { IsValid bool; Data map[string]any, ErrorMsg string }
// 节点B只需要关心验证是否通过，输入就是 boolean

wf.AddLambdaNode("nodeB", nextStep).
   AddInput("nodeA", compose.FromField("IsValid")) // 只将 ValidationResult 的 IsValid 字段传给 nodeB
```


**4. 处理嵌套结构的 `MapFieldPaths`等**

对于复杂嵌套结构，你需要使用 `FieldPath`来指定路径。Eino 内部使用 Unit Separator 字符 (`\x1F`) 作为路径分隔符，以高效且安全地处理任意深度的嵌套字段。

```go
// 映射深层嵌套的字段
wf.AddLambdaNode("nodeDeep", deepProcessor).
   AddInput("someNode", 
        compose.MapFieldPaths(
            compose.FieldPath{"response", "data", "user", "name"}, // 源路径
            compose.FieldPath{"output", "userName"}                // 目标路径
        ))
```


`ToFieldPath`和 `FromFieldPath`是上述功能的自然延伸，分别用于将整个输出映射到嵌套字段，以及从嵌套字段中提取值作为整体输入。

**5. 最简单的直接传递 `AddInput`**

当上下游节点的输入输出类型完全一致，或者你希望传递整个对象时，这是最直接的方式。

```go
wf.AddLambdaNode("nodeB", processor).
   AddInput("nodeA") // 无需任何映射配置，nodeA的输出直接整体传给nodeB
```

|映射目标|核心 API|功能描述|适用场景举例|
|---|---|---|---|
|**字段 → 字段**​|`MapFields("源字段", "目标字段")`|将前驱节点输出对象的**某个顶层字段**映射到后继节点输入对象的**某个顶层字段**。|将 `User`对象的 `Name`字段映射到 `Request`对象的 `UserName`字段。|
|**整体输出 → 字段**​|`ToField("目标字段")`|将**整个前驱节点的输出**作为后继节点输入对象的**一个字段**的值。|将上一个节点的完整结果（如一条AI回复）存入当前节点输入对象的 `context`字段。|
|**字段 → 整体输入**​|`FromField("源字段")`|将前驱节点输出对象的**某个特定字段**作为**整个后继节点的输入**。|从一个复杂配置对象中仅提取 `query`字段的值，作为问答模型的输入问题。|
|**嵌套字段 → 嵌套字段**​|`MapFieldPaths(FieldPath{...}, FieldPath{...})`|在**复杂的嵌套结构**之间进行深度映射，支持任意层级的字段访问。|映射 `response.data.user.profile.name`到 `output.userName`。|
|**整体输出 → 嵌套字段**​|`ToFieldPath(FieldPath{...})`|将**整个前驱节点的输出**映射到后继节点输入对象的**一个嵌套字段**中。|将检索到的文档列表，整体放入输入对象的 `context.documents`嵌套字段里。|
|**嵌套字段 → 整体输入**​|`FromFieldPath(FieldPath{...})`|从前驱节点的输出中提取一个**嵌套字段的值**，并将其作为**整个后继节点的输入**。|从 API 响应的多层结构中提取最内部的 `result`字段，直接传递给下一个处理器。|
|**整体输出 → 整体输入**​|`AddInput(前驱节点名)`|将前驱节点的**整个输出**直接传递给后继节点作为其**完整输入**。|简单的线性链式调用，节点间传递完整的数据结构，无需拆分或重组。|