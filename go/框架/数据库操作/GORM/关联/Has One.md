`has one` 关联与另一个模型建立了一对一的连接，但语义（和结果）略有不同。此关联表示一个模型的每个实例都包含或拥有另一个模型的一个实例。

例如，如果应用程序包含用户和信用卡，并且每个用户只能拥有一张信用卡。

```go
// User has one CreditCard, UserID is the foreign key
type User struct {
  gorm.Model
  CreditCard CreditCard
}

type CreditCard struct {
  gorm.Model
  Number string
  UserID uint
}
```
# 查询关联信息

```go
func GetAll(db *gorm.DB) ([]User, error) {
  var users []User
  err := db.Model(&User{}).Preload("CreditCard").Find(&users).Error
  return users, err
}
```
# 覆盖外键

对于 `has one` 关系，还必须存在一个外键字段，所有者将所属模型的主键保存到此字段中。

字段的名称通常由 `has one` 模型的类型加上它的 `primary key` 生成，对于上面的例子它是 `UserID` 。

当向用户提供信用卡时，它会将用户的 `ID` 保存到其 `UserID` 字段中。

如果要使用其他字段来保存关系，可以使用标签 `foreignKey` 进行更改，例如：

```go
type User struct {
  gorm.Model
  CreditCard CreditCard `gorm:"foreignKey:UserName"`
  // use UserName as foreign key
}

type CreditCard struct {
  gorm.Model
  Number   string
  UserName string
}
```
# 覆盖引用

默认情况下，所属实体会将 `has one` 模型的主键保存到外键中，可以更改为保存另一个字段的值，如下例中使用 `Name` 。

```go
type User struct {
  gorm.Model
  Name       string     `gorm:"index"`
  CreditCard CreditCard `gorm:"foreignKey:UserName;references:Name"`
}

type CreditCard struct {
  gorm.Model
  Number   string
  UserName string
}
```
# Belons To 与 Has One

在 GORM 中，`Has One`和 `Belongs To`都是描述一对一关系的模型关联方式，但它们​**​代表完全不同的关系方向和所有权​**​。理解它们的区别是构建正确数据模型的关键。

|**特性​**​|​**​Has One​**​|​**​Belongs To​**​|
|---|---|---|
|​**​关系方向​**​|父 → 子|子 → 父|
|​**​外键位置​**​|子表中|子表中|
|​**​所有权​**​|父拥有子|子属于父|
|​**​创建顺序​**​|先父后子|先父后子|
|​**​删除行为​**​|通常级联删除|通常不级联|
|​**​语义重点​**​|强调父对子的所有权|强调子对父的归属|
**选择 Has One 当：**

```go
// 1. 父对象是关系核心
type Product struct {
    ID     uint
    Detail ProductDetail `gorm:"foreignKey:ProductID"`
}

// 2. 子对象不能独立存在
type User struct {
    ID     uint
    Config UserConfig `gorm:"foreignKey:UserID"`
}

// 3. 需要级联操作
type Order struct {
    ID      uint
    Payment Payment `gorm:"constraint:OnDelete:CASCADE"`
}
```

**选择 Belongs To 当：**

```go
// 1. 子对象是关系核心
type Review struct {
    ID      uint
    Product Product `gorm:"foreignKey:ProductID"`
}

// 2. 需要从子访问父
type Employee struct {
    ID       uint
    Dept     Department `gorm:"foreignKey:DeptID"`
}

// 3. 多模型共享父对象
type Address struct {
    ID        uint
    User      User `gorm:"foreignKey:UserID"`
    Company   Company `gorm:"foreignKey:CompanyID"`
}
```

**创建行为**

|**关系类型​**​|​**​AutoMigrate 行为​**​|​**​表创建顺序​**​|​**​外键约束​**​|
|---|---|---|---|
|​**​Has One​**​|只创建父表|仅父表|❌ 不自动添加|
|​**​Belongs To​**​|创建子表和父表|先父表后子表|✅ 自动添加|