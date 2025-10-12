`has many` 关联与另一个模型建立一对多连接，与 `has one` 不同，所有者可以拥有零个或多个模型实例。

例如，如果的应用程序包括用户和信用卡，并且每个用户可以拥有多张信用卡。

```go
// User has many CreditCards, UserID is the foreign key
type User struct {
  gorm.Model
  CreditCards []CreditCard
}

type CreditCard struct {
  gorm.Model
  Number string
  UserID uint
}
```


```go
// Retrieve user list with eager loading credit cards
func GetAll(db *gorm.DB) ([]User, error) {
    var users []User
    err := db.Model(&User{}).Preload("CreditCards").Find(&users).Error
    return users, err
}
```
# 覆盖外键

要定义 `has many` 关系，必须存在外键。默认外键的名称是所有者的类型名称加上其主键字段的名称

例如，要定义属于 `User` 的模型，外键应该是 `UserID` 。

要使用另一个字段作为外键，可以使用 `foreignKey` 标签对其进行自定义，例如：

```go
type User struct {
  gorm.Model
  CreditCards []CreditCard `gorm:"foreignKey:UserRefer"`
}

type CreditCard struct {
  gorm.Model
  Number    string
  UserRefer uint
}
```
# 覆盖引用

GORM 通常使用所有者的主键作为外键的值，对于上面的例子，它是 `User` 的 `ID` ，

当您将信用卡分配给用户时，GORM 会将用户的 `ID` 保存到信用卡的 `UserID` 字段中。

可以使用标签 `references` 来更改它，例如：

```go
type User struct {
  gorm.Model
  MemberNumber string
  CreditCards  []CreditCard `gorm:"foreignKey:UserNumber;references:MemberNumber"`
}

type CreditCard struct {
  gorm.Model
  Number     string
  UserNumber string
}
```
# 自关联



```go
type User struct {
    gorm.Model
    Name      string
    ManagerID *uint
    Team      []User `gorm:"foreignkey:ManagerID"` // 一对多关系
}

```

- **关系类型​**​：一对多 (一个经理管理多个团队成员)
    
- ​**​方向​**​：经理 → 团队成员
    
- ​**​外键​**​：`ManagerID`指向经理的 ID