# Belongs TO

`belongs to` 关联与另一个模型建立一对一连接，使得声明模型的每个实例“属于”另一个模型的一个实例。

例如，如果您的应用程序包含用户和公司，并且每个用户只能分配给一家公司，则以下类型代表该关系。请注意，在 `User` 对象上，既有 `CompanyID` ，也有 `Company` 。默认情况下， `CompanyID` 隐式用于在 `User` 和 `Company` 表之间创建外键关系，因此**必须**将其包含在 `User` 结构体中才能填充 `Company` 内部结构体。

```go
// `User` belongs to `Company`, `CompanyID` is the foreign key
type User struct {
  gorm.Model
  Name      string
  CompanyID int
  Company   Company
}

type Company struct {
  ID   int
  Name string
}
```

## 覆盖外键

要定义属于关系，外键必需存在，默认外键使用所有者的类型名称加上其主键字段名称。

对于上面的例子，要定义属于 `Company` 的 `User` 模型，外键按照惯例应该是 `CompanyID`

GORM 提供了自定义外键的方法，例如：

```go
type User struct {
  gorm.Model
  Name         string
  CompanyRefer int
  Company      Company `gorm:"foreignKey:CompanyRefer"`
  // use CompanyRefer as foreign key
}

type Company struct {
  ID   int
  Name string
}
```

## 覆盖引用

对于属于关系，GORM 通常使用所有者的主键字段作为外键的值，对于上面的例子，它是 `Company` 的字段 `ID` 。

将用户分配给公司时，GORM 会将公司的 `ID` 保存到用户的 `CompanyID` 字段中。

可以使用标签 `references` 来更改它，例如：

```go
type User struct {
  gorm.Model
  Name      string
  CompanyID string
  Company   Company `gorm:"references:Code"` // use Code as references
}

type Company struct {
  ID   int
  Code string
  Name string
}
```

&#x20;如果覆盖外键名称已经存在于所有者的类型中，GORM 通常会猜测关系为 `has one` ，我们需要在 `belongs to` 关系中指定 `references` 。

```go
type User struct {
  gorm.Model
  Name      string
  CompanyID int
  Company   Company `gorm:"references:CompanyID"` // use Company.CompanyID as references
}

type Company struct {
  CompanyID   int
  Code        string
  Name        string
}
```

## 注意事项

1. 外键声明位置在Belongs to 的模型中（user）
2. 外键字段必需存在
3. 外键字段类型必须匹配
4. 使用预加载提升性能
5. 必须先创建 `Company` 记录再创建 `User` 记录
6. Belongs to 不支持堕胎

## 使用示例

### 创建关联关系表

```go
  
type User struct {  
    ID        int  
    Num       int  
    Name      string  
    CompanyID int  
    Company   Company  
}  
  
type Company struct {  
    ID   int  
    Name string  
}

company := []*Company{
		{Name: "keji"},
		{Name: "yule"},
		{Name: "shenghuo"},
	}
	user := []*User{
		{Name: "ke", CompanyID: 1},
		{Name: "yu", CompanyID: 2},
		{Name: "sheng", CompanyID: 3},
	}
	gdb.Create(company)
	gdb.Create(user)
```

### 查询关联

```go
// 普通查询无法直接插到关联信息
var u User
gdb.First(&u)
fmt.Println(u) // {ID:12 Num:0 Name:ke CompanyID:4 Company:{ID:0 Name:}}

// 通过user去查询Company
var u User  
gdb.Preload("Company").First(&u)  
fmt.Printf("%+v", u)
```

## 更新关联

```go
// 更新关联公司
gdb.Model(&u.Company).Update("name", "dakeji")  
```
