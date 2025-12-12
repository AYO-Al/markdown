- 安装

```go
go get github.com/go-playground/validator/v10
```

```go
validate := validator.New(validator.WithRequiredStructEnabled())
```

WithRequiredStructEnabled 使非指针结构体上的 required 标签生效，而不是被忽略。这是 v11+中的默认行为

- 自定义验证函数

```go
// Structure
func customFunc(fl validator.FieldLevel) bool {

	if fl.Field().String() == "invalid" {
		return false
	}

	return true
}

validate.RegisterValidation("custom tag name", customFunc)
// NOTES: using the same tag name as an existing function
//        will overwrite the existing one
```

- FieldLevel接口

```go
type FieldLevel interface {

	// Top 返回顶层的结构体（如果存在的话）
	Top() reflect.Value

	// Parent 返回当前字段的父级结构体（如果存在的话），或者
	// 在调用 'VarWithValue' 时返回比较值
	Parent() reflect.Value

	// Field 返回当前待验证的字段
	Field() reflect.Value

	// FieldName 返回字段的名称，其中标签名称优先于字段的实际名称
	FieldName() string

	// StructFieldName 返回结构体字段的名称
	StructFieldName() string

	// Param 返回用于验证当前字段的参数
	Param() string

	// GetTag 返回当前验证的标签名称
	GetTag() string

	// ExtractType 获取字段值的实际底层类型。
	// 它会深入指针、自定义类型，并返回底层的值及其种类（Kind）
	ExtractType(field reflect.Value) (value reflect.Value, kind reflect.Kind, nullable bool)

	// GetStructFieldOK 遍历父级结构体以检索由参数中提供的命名空间指定的特定字段，
	// 并返回该字段、字段的种类以及是否成功检索到该字段。
	//
	// 注意：当不成功时，ok 将为 false，这可能发生在嵌套结构体为 nil 时，
	// 因此无法检索到该字段，因为该字段不存在。
	//
	// 已弃用：请改用 GetStructFieldOK2()，它还会返回值是否可为 null。
	GetStructFieldOK() (reflect.Value, reflect.Kind, bool)

	// GetStructFieldOKAdvanced 与 GetStructFieldOK 相同，但它接受父级结构体作为起始点来查找字段和命名空间，
	// 为验证器提供了更好的可扩展性。
	//
	// 已弃用：请改用 GetStructFieldOKAdvanced2()，它还会返回值是否可为 null。
	GetStructFieldOKAdvanced(val reflect.Value, namespace string) (reflect.Value, reflect.Kind, bool)

	// GetStructFieldOK2 遍历父级结构体以检索由参数中提供的命名空间指定的特定字段，
	// 并返回该字段、字段的种类、它是否可为 null 类型以及是否成功检索到该字段。
	//
	// 注意：当不成功时，ok 将为 false，这可能发生在嵌套结构体为 nil 时，
	// 因此无法检索到该字段，因为该字段不存在。
	GetStructFieldOK2() (reflect.Value, reflect.Kind, bool, bool)

	// GetStructFieldOKAdvanced2 与 GetStructFieldOK 相同，但它接受父级结构体作为起始点来查找字段和命名空间，
	// 为验证器提供了更好的可扩展性。
	GetStructFieldOKAdvanced2(val reflect.Value, namespace string) (reflect.Value, reflect.Kind, bool, bool)
}
```


FieldLevel 包含所有用于验证字段的信息和辅助函数