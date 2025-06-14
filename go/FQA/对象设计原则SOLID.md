SOLID 是面向对象设计（OOD）的核心原则，由 Robert C. Martin (Uncle Bob) 总结提出，代表了五个关键设计原则的首字母缩写。这些原则帮助开发者构建灵活、可维护、可扩展的软件系统。

## SOLID 原则全景图

| 原则  | 英文全称                  | 核心理念 | 关键作用   |
| --- | --------------------- | ---- | ------ |
| S   | Single Responsibility | 单一职责 | 降低耦合度  |
| O   | Open/Closed           | 开闭原则 | 提升扩展性  |
| L   | Liskov Substitution   | 里氏替换 | 确保继承安全 |
| I   | Interface Segregation | 接口隔离 | 最小化依赖  |
| D   | Dependency Inversion  | 依赖倒置 | 解耦高层模块 |

## 单一职责原则 (SRP)

### 关键要点

- ​**​职责隔离​**​：每个结构体/包只承担​**​一个核心功能领域​**​
- ​**​变更驱动​**​：设计时思考"什么原因会导致这个结构体改变？"
- ​**​命名即承诺​**​：结构体/函数命名应清晰反映其单一职责

### 实施要点


```go
// 不推荐：多个职责混合
type UserManager struct {
    DB *sql.DB
}

func (m *UserManager) Create(user User) error { /* 1. 存储逻辑 */ }
func (m *UserManager) Notify(user User) error { /* 2. 通知逻辑 */ }

// 推荐：职责分离
type UserRepository struct { DB *sql.DB }
func (r *UserRepository) Save(user User) error { /* 仅存储 */ }

type UserNotifier struct { /* 邮件/短信客户端 */ }
func (n *UserNotifier) SendWelcome(user User) error { /* 仅通知 */ }

// 服务层协调
type UserService struct {
    repo   *UserRepository
    notify *UserNotifier
}
```

## 开闭原则 (OCP)

### 关键要点

- ​**​抽象定义契约​**​：面向接口编程而非具体实现
- ​**​扩展点设计​**​：预留hook/策略位置支持未来功能
- ​**​增量演进​**​：新功能通过添加代码实现而非修改

### 实施要点

```go
// 抽象层：定义支付接口
type PaymentProcessor interface {
    Process(amount float64) error
}

// 具体实现
type CreditCardProcessor struct{}

// 新增支付方式不用修改原有代码
type CryptoProcessor struct{}

// 依赖注入保持扩展性
type OrderHandler struct {
    payment PaymentProcessor
}

func NewOrderHandler(processor PaymentProcessor) *OrderHandler {
    return &OrderHandler{payment: processor}
}

func (h *OrderHandler) Pay(amount float64) error {
    return h.payment.Process(amount) // 支持所有实现
}
```

## 里氏替换原则 (LSP)

### 关键要点

- ​**​行为契约一致性​**​：确保实现符合接口预期行为
- ​**​前置条件不强于​**​：子类型输入要求不能更严格
- ​**​后置条件不弱于​**​：子类型输出承诺不能更宽松

### 实施要点

```go
// 文件操作接口
type FileOperation interface {
    Read() ([]byte, error)
}

// 磁盘文件实现
type DiskFile struct{}

// 内存文件实现 (必须符合接口约定)
type MemoryFile struct{}

// 测试辅助函数验证LSP
func TestFileOperations(t *testing.T) {
    testCases := []FileOperation{
        &DiskFile{},
        &MemoryFile{},
    }
    
    for _, f := range testCases {
        data, err := f.Read()
        assert.NoError(t, err)
        assert.True(t, len(data) > 0) // 所有实现必须满足该基础检查
    }
}
```

## 接口隔离原则 (ISP)

### 关键要点

- ​**​细粒度接口​**​：基于功能角色划分接口
- ​**​无强制依赖​**​：客户端不被迫实现不用的方法
- ​**​接口组合复用​**​：通过组合创建复杂接口

### 实施要点

```go
// 不推荐：胖接口
type DataStore interface {
    Save(Data) error
    Retrieve(id string) (Data, error)
    Delete(id string) error
    Backup() error
}

// 推荐：拆分为细粒度接口
type BasicStore interface {
    Save(Data) error
    Retrieve(id string) (Data, error)
}

type AdminStore interface {
    Delete(id string) error
    Backup() error
}

// 只实现必要接口
type UserStore struct{} // 只实现BasicStore

// 高级实现可选择组合
type SystemStore struct {
    BasicStore
    AdminStore
}

// 客户端按需使用
func UserFunc(store BasicStore) {
    // 不需要关心Admin功能
}
```

## 依赖倒置原则 (DIP)

### 关键要点

- ​**​解耦依赖关系​**​：高层模块不直接依赖低层实现
- ​**​抽象指向稳定​**​：依赖抽象层保证系统健壮性
- ​**​依赖注入实现​**​：运行时动态注入具体实现

### 实施要点

```go
// 数据库抽象层
type Database interface {
    Query(q string) ([]Row, error)
}

// 具体实现
type MySQL struct{}
type PostgreSQL struct{}

// 高层业务模块
type ReportService struct {
    db Database // 依赖抽象
}

// 构造函数注入依赖
func NewReportService(db Database) *ReportService {
    return &ReportService{db: db}
}

// 使用依赖注入工具 (如google/wire)
var ServiceSet = wire.NewSet(
    wire.Bind(new(Database), new(*PostgreSQL)), // 绑定接口实现
    PostgreSQL.New,                             // 创建具体实现
    NewReportService,                           // 注入依赖
)

// 测试替换实现
func TestReportService(t *testing.T) {
    mockDB := new(MockDatabase) 
    service := NewReportService(mockDB) // 注入模拟对象
    /* 测试逻辑 */
}
```

## SOLID原则实施策略矩阵

| 原则  | 设计阶段实施策略 | 编码阶段检查点       | 测试验证方法    |
| --- | -------- | ------------- | --------- |
| SRP | 功能领域划分模块 | 单一文件代码不超过300行 | 变更影响分析测试  |
| OCP | 定义稳定抽象层  | 是否通过新类型添加功能   | 新功能集成测试   |
| LSP | 行为契约文档化  | 接口方法输入输出约束    | 可替换性兼容测试  |
| ISP | 角色接口设计   | 接口方法数≤3个      | 单功能接口单元测试 |
| DIP | 依赖关系图设计  | import无具体实现依赖 | Mock替换测试  |