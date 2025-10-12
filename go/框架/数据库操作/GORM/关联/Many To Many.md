多对多在两个模型之间添加连接表。

例如，如果应用程序包含用户和语言，并且一个用户可以说多种语言，并且许多用户可以说一种指定的语言。

```go
// User has and belongs to many languages, `user_languages` is the join table
type User struct {
  gorm.Model
  Languages []Language `gorm:"many2many:user_languages;"`
}

type Language struct {
  gorm.Model
  Name string
}
```

当使用 GORM `AutoMigrate` 为 `User` 创建表时，GORM 将自动创建连接表
# Back-Reference

```go
// User has and belongs to many languages, use `user_languages` as join table
type User struct {
  gorm.Model
  Languages []*Language `gorm:"many2many:user_languages;"`
}

type Language struct {
  gorm.Model
  Name string
  Users []*User `gorm:"many2many:user_languages;"`
}
```
## 查找关联的信息

```go
// Retrieve user list with eager loading languages
func GetAllUsers(db *gorm.DB) ([]User, error) {
  var users []User
  err := db.Model(&User{}).Preload("Languages").Find(&users).Error
  return users, err
}

// Retrieve language list with eager loading users
func GetAllLanguages(db *gorm.DB) ([]Language, error) {
  var languages []Language
  err := db.Model(&Language{}).Preload("Users").Find(&languages).Error
  return languages, err
}
```
# 覆盖外键

对于 `many2many` 关系，连接表拥有引用两个模型的外键，例如：

```go
type User struct {
  gorm.Model
  Languages []Language `gorm:"many2many:user_languages;"`
}

type Language struct {
  gorm.Model
  Name string
}

// Join Table: user_languages
//   foreign key: user_id, reference: users.id
//   foreign key: language_id, reference: languages.id

```

要覆盖它们，可以使用标签 `foreignKey` ， `references` ， `joinForeignKey` ， `joinReferences` ，不必一起使用它们，只需使用其中一个来覆盖一些外键/引用

```go
type User struct {
  gorm.Model
  Profiles []Profile `gorm:"many2many:user_profiles;foreignKey:Refer;joinForeignKey:UserReferID;References:UserRefer;joinReferences:ProfileRefer"`
  Refer    uint      `gorm:"index:,unique"`
}

type Profile struct {
  gorm.Model
  Name      string
  UserRefer uint `gorm:"index:,unique"`
}

// Which creates join table: user_profiles
//   foreign key: user_refer_id, reference: users.refer
//   foreign key: profile_refer, reference: profiles.user_refer
```

| **标签​**​         | ​**​作用对象​**​   | ​**​功能说明​**​    | ​**​示例值​**​    | ​**​实际作用​**​               |
| ---------------- | -------------- | --------------- | -------------- | -------------------------- |
| `foreignKey`     | 主模型 (User)     | 指定主模型中外键字段      | `Refer`        | 使用 `Refer`代替默认 ID          |
| `joinForeignKey` | 连接表            | 指定连接表中指向主模型的外键  | `UserReferID`  | 连接表使用 `user_refer_id`字段    |
| `references`     | 关联模型 (Profile) | 指定关联模型中被引用的字段   | `UserRefer`    | 引用 Profile 的 `UserRefer`字段 |
| `joinReferences` | 连接表            | 指定连接表中指向关联模型的外键 | `ProfileRefer` | 连接表使用 `profile_refer`字段    |
# 自关联

```go
type User struct {
  gorm.Model
  Friends []*User `gorm:"many2many:user_friends"`
}

// Which creates join table: user_friends
//   foreign key: user_id, reference: users.id
//   foreign key: friend_id, reference: users.id

```
# 自定义JoinTable

`JoinTable` 可以是一个功能齐全的模型，比如拥有 `Soft Delete` ， `Hooks` 支持以及更多的字段，你可以使用 `SetupJoinTable` 来设置它，例如：

**自定义连接表的外键要求为复合主键或复合唯一索引**

```go
type Person struct {
  ID        int
  Name      string
  Addresses []Address `gorm:"many2many:person_addresses;"`
}

type Address struct {
  ID   uint
  Name string
}

type PersonAddress struct {
  PersonID  int `gorm:"primaryKey"`
  AddressID int `gorm:"primaryKey"`
  CreatedAt time.Time
  DeletedAt gorm.DeletedAt
}

func (PersonAddress) BeforeCreate(db *gorm.DB) error {
  // ...
}

// Change model Person's field Addresses' join table to PersonAddress
// PersonAddress must defined all required foreign keys or it will raise error
err := db.SetupJoinTable(&Person{}, "Addresses", &PersonAddress{})

// func (db *DB) SetupJoinTable(model interface{}, field string, joinTable interface{}) error
|`model`|`interface{}`|主模型（如 `User`）|
|`field`|`string`|关联字段名（如 `"Roles"`）|
|`joinTable`|`interface{}`|自定义连接表模型|
```


