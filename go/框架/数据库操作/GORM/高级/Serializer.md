序列化器是一个可扩展的接口，允许自定义如何序列化和反序列化数据库数据。

GORM 提供了一些默认的序列化器： `json` 、 `gob` 、 `unixtime` 。

```go
type User struct {  
  Name        []byte                 `gorm:"serializer:json"`  
  Roles       Roles                  `gorm:"serializer:json"`  
  Contracts   map[string]interface{} `gorm:"serializer:json"`  
  JobInfo     Job                    `gorm:"type:bytes;serializer:gob"`  
  CreatedTime int64                  `gorm:"serializer:unixtime;type:time"` // store int as datetime into database  
}  
  
type Roles []string  
  
type Job struct {  
  Title    string  
  Location string  
  IsIntern bool  
}  
  
createdAt := time.Date(2020, 1, 1, 0, 8, 0, 0, time.UTC)  
data := User{  
  Name:        []byte("jinzhu"),  
  Roles:       []string{"admin", "owner"},  
  Contracts:   map[string]interface{}{"name": "jinzhu", "age": 10},  
  CreatedTime: createdAt.Unix(),  
  JobInfo: Job{  
    Title:    "Developer",  
    Location: "NY",  
    IsIntern: false,  
  },  
}  
  
DB.Create(&data)  
// INSERT INTO `users` (`name`,`roles`,`contracts`,`job_info`,`created_time`) VALUES  
//   ("\"amluemh1\"","[\"admin\",\"owner\"]","{\"age\":10,\"name\":\"jinzhu\"}",<gob binary>,"2020-01-01 00:08:00")  
  
var result User  
DB.First(&result, "id = ?", data.ID)  
// result => User{  
//   Name:        []byte("jinzhu"),  
//   Roles:       []string{"admin", "owner"},  
//   Contracts:   map[string]interface{}{"name": "jinzhu", "age": 10},  
//   CreatedTime: createdAt.Unix(),  
//   JobInfo: Job{  
//     Title:    "Developer",  
//     Location: "NY",  
//     IsIntern: false,  
//   },  
// }  
  
DB.Where(User{Name: []byte("jinzhu")}).Take(&result)  
// SELECT * FROM `users` WHERE `users`.`name` = "\"amluemh1\"
```
# 注册序列化器

一个序列化器需要实现如何序列化和反序列化数据，因此它需要实现以下接口

```go
import "gorm.io/gorm/schema"  
  
type SerializerInterface interface {  
  Scan(ctx context.Context, field *schema.Field, dst reflect.Value, dbValue interface{}) error  
  SerializerValuerInterface  
}  
  
type SerializerValuerInterface interface {  
  Value(ctx context.Context, field *schema.Field, dst reflect.Value, fieldValue interface{}) (interface{}, error)  
}
```

例如，默认的 `JSONSerializer` 实现如下：

```go
// JSONSerializer json serializer
type JSONSerializer struct {
}

// Scan implements serializer interface
func (JSONSerializer) Scan(ctx context.Context, field *schema.Field, dst reflect.Value, dbValue interface{}) (err error) {
  fieldValue := reflect.New(field.FieldType)

  if dbValue != nil {
    var bytes []byte
    switch v := dbValue.(type) {
    case []byte:
      bytes = v
    case string:
      bytes = []byte(v)
    default:
      return fmt.Errorf("failed to unmarshal JSONB value: %#v", dbValue)
    }

    err = json.Unmarshal(bytes, fieldValue.Interface())
  }

  field.ReflectValueOf(ctx, dst).Set(fieldValue.Elem())
  return
}

// Value implements serializer interface
func (JSONSerializer) Value(ctx context.Context, field *Field, dst reflect.Value, fieldValue interface{}) (interface{}, error) {
  return json.Marshal(fieldValue)
}
```

并通过以下代码进行注册：

```go
schema.RegisterSerializer("json", JSONSerializer{})
```

