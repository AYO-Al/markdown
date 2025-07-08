`reflect` 包实现了​**​运行时反射​**​机制。它允许程序在运行时检查和操作具有任意类型的对象。其典型用途是：获取一个静态类型为 `interface{}`（空接口）的值，并通过调用 `TypeOf` 函数来提取其​**​动态类型信息​**​（该函数返回一个 `Type` 类型）。

调用 `ValueOf` 函数会返回一个 `Value` 类型，它代表了该值的​**​运行时数据​**​（包括值和类型信息）。

`Zero` 函数接收一个 `Type` 类型作为参数，并返回一个代表该类型​**​零值​**​的 `Value`。

**核心目的：​**​

- ​**​动态类型检查与操作：​**​ 在编译时无法确定具体类型的情况下（例如处理 `interface{}`），在运行时获取类型信息（`Type`）和操作值（`Value`）。
- ​**​元编程：​**​ 编写能够处理任意类型数据的通用代码（如序列化/反序列化库、ORM框架、依赖注入容器等）。
# 1 常量

```go
const Ptr = Pointer
```

- 在 Go 语言的早期版本中，反射系统使用 `Ptr` 作为表示指针类型的常量名
- 后来为了代码清晰性和一致性，Go 团队决定将 `Ptr` 重命名为 `Pointer`
- 这个常量定义是为了​**​保持向后兼容性​**​而保留的
# 2 函数
## 2.1 func Copy(dst, src Value) int

`Copy` 函数用于将源切片或数组的内容复制到目标切片或数组中，直到目标被填满或源被耗尽。返回实际复制的元素数量。

**参数说明**

- `dst Value`：目标值，必须是切片或数组类型
- `src Value`：源值，必须是切片或数组类型（特殊情况：源可以是字符串，当目标元素类型为 `uint8` 时）

**返回值**

- `int`：实际复制的元素数量

**注意事项**

1. 目标和源必须都是切片或数组类型
2. 目标和源的元素类型必须相同
3. 如果目标是数组且不可设置（`CanSet() == false`），会引发 panic
4. 特殊规则：当目标元素类型为 `uint8` 时，源可以是字符串（相当于 `[]byte` 转换）

```go
package main

import (
	"fmt"
	"reflect"
)

func main() {
	// 示例1：切片到切片复制
	srcSlice := []int{1, 2, 3, 4, 5}
	dstSlice := make([]int, 3)
	
	copied := reflect.Copy(
		reflect.ValueOf(dstSlice),
		reflect.ValueOf(srcSlice),
	)
	
	fmt.Printf("示例1: 复制了 %d 个元素\n", copied)
	fmt.Printf("源切片: %v\n目标切片: %v\n\n", srcSlice, dstSlice)

	// 示例2：数组到切片复制
	srcArray := [4]string{"A", "B", "C", "D"}
	dstSlice2 := make([]string, 6) // 目标容量大于源
	
	copied = reflect.Copy(
		reflect.ValueOf(dstSlice2),
		reflect.ValueOf(srcArray[:]), // 数组转换为切片
	)
	
	fmt.Printf("示例2: 复制了 %d 个元素\n", copied)
	fmt.Printf("源数组: %v\n目标切片: %v\n\n", srcArray, dstSlice2)

	// 示例3：字符串到字节切片复制
	str := "Hello, 世界"
	dstBytes := make([]byte, 10) // 目标容量小于源长度
	
	copied = reflect.Copy(
		reflect.ValueOf(dstBytes),
		reflect.ValueOf(str),
	)
	
	fmt.Printf("示例3: 复制了 %d 个字节\n", copied)
	fmt.Printf("源字符串: %s\n目标字节: %v\n", str, dstBytes)
	
	// 错误示例：类型不匹配
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("\n错误捕获: %v\n", r)
		}
	}()
	
	intSlice := []int{1, 2, 3}
	strSlice := []string{"a", "b"}
	
	// 尝试复制不同类型切片会panic
	reflect.Copy(
		reflect.ValueOf(intSlice),
		reflect.ValueOf(strSlice),
	)
}

/**
示例1: 复制了 3 个元素
源切片: [1 2 3 4 5]
目标切片: [1 2 3]

示例2: 复制了 4 个元素
源数组: [A B C D]
目标切片: [A B C D  ]

示例3: 复制了 10 个字节
源字符串: Hello, 世界
目标字节: [72 101 108 108 111 44 32 228 184 150]

错误捕获: reflect.Copy: types []int and []string differ
*/
```
## 2.2 func DeepEqual(x, y any) bool

`DeepEqual` 递归比较两个值是否"深度(值)相等"，比普通的 `==` 操作符更深入。它遵循以下规则：

**比较规则**

1. ​**​数组​**​：对应元素深度相等
2. ​**​结构体​**​：所有字段（包括未导出字段）深度相等
3. ​**​函数​**​：只有两者都为 nil 时才相等
4. ​**​接口​**​：持有的具体值深度相等
5. ​**​映射​**​：
    - 两者都为 nil 或都不为 nil
    - 长度相同
    - 相同键映射到深度相等的值
6. ​**​指针​**​：
    - 指针值相等（\==）
    - 或指向深度相等的值
7. ​**​切片​**​：
    - 两者都为 nil 或都不为 nil
    - 长度相同
    - 指向相同底层数组或对应元素深度相等
    - ​**​注意​**​：`[]byte{}` 和 `[]byte(nil)` 不相等
8. ​**​基本类型​**​：使用 `==` 操作符比较

**特殊情况**

- ​**​NaN 值​**​：`math.NaN() != math.NaN()`，但包含 NaN 的指针相等
- ​**​循环引用​**​：检测到循环时认为指针相等
- ​**​函数​**​：非 nil 函数总是不相等（即使同一个函数）
## 2.3 func Swapper(slice any) func(i, j int)

`Swapper` 返回一个用于交换切片中元素的函数。该函数接收两个索引参数 `i` 和 `j`，交换切片中这两个位置的元素。

**参数说明**

- `slice any`：必须是切片类型

**返回值**

- `func(i, j int)`：交换函数，用于交换指定索引的元素

**注意事项**

1. 如果传入的不是切片类型，会引发 panic
2. 交换函数不检查索引是否越界（调用时需确保索引有效）
3. 返回的函数会修改原始切片内容

```go
package main

import (
	"fmt"
	"reflect"
)

func main() {
	// 示例1：整数切片交换
	intSlice := []int{10, 20, 30, 40, 50}
	swapInts := reflect.Swapper(intSlice)
	
	fmt.Println("原始切片:", intSlice)
	swapInts(1, 3) // 交换索引1和3
	fmt.Println("交换后:", intSlice)
	
	// 示例2：字符串切片交换
	strSlice := []string{"A", "B", "C", "D"}
	swapStrs := reflect.Swapper(strSlice)
	
	fmt.Println("\n原始切片:", strSlice)
	swapStrs(0, len(strSlice)-1) // 交换首尾元素
	fmt.Println("交换后:", strSlice)
	
	// 示例3：结构体切片交换
	type Point struct{ X, Y int }
	points := []Point{{1, 2}, {3, 4}, {5, 6}}
	swapPoints := reflect.Swapper(points)
	
	fmt.Println("\n原始切片:", points)
	swapPoints(0, 2)
	fmt.Println("交换后:", points)
	
	// 错误示例：非切片类型
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("\n错误捕获: %v\n", r)
		}
	}()
	
	array := [3]int{1, 2, 3}
	_ = reflect.Swapper(array) // 传入数组会panic
}

/**
原始切片: [10 20 30 40 50]
交换后: [10 40 30 20 50]

原始切片: [A B C D]
交换后: [D B C A]

原始切片: [{1 2} {3 4} {5 6}]
交换后: [{5 6} {3 4} {1 2}]

错误捕获: reflect: call of Swapper on [3]int Value
*/
```
## 2.4 最佳实践总结

### 2.4.1 `reflect.Copy`

1. 优先使用内置的 `copy()` 函数（类型安全）
2. 仅当处理 `interface{}` 类型时使用反射版本
3. 注意目标容量限制，避免数据截断
4. 特殊场景：字符串到 `[]byte` 的转换

### 2.4.2 `reflect.DeepEqual`

1. 测试中用于复杂结构的比较
2. 注意未导出字段也会被比较
3. 对于包含浮点数的结构，考虑自定义比较函数
4. 性能敏感场景避免使用（递归比较开销大）

### 2.4.3 `reflect.Swapper`

1. 实现排序算法时的便捷工具
2. 比手动交换更简洁
3. 注意只适用于切片，不适用于数组
# 3 类型
## 3.1 Type接口

`reflect.Type` 是 Go 反射系统的核心接口，用于表示 Go 类型的元信息。它提供了丰富的方法来查询类型的各种属性，是运行时类型检查和分析的基础。

```go
type Type interface {

	// Align returns the alignment in bytes of a value of
	// this type when allocated in memory.
	Align() int

	// FieldAlign returns the alignment in bytes of a value of
	// this type when used as a field in a struct.
	FieldAlign() int

	// Method returns the i'th method in the type's method set.
	// It panics if i is not in the range [0, NumMethod()).
	//
	// For a non-interface type T or *T, the returned Method's Type and Func
	// fields describe a function whose first argument is the receiver,
	// and only exported methods are accessible.
	//
	// For an interface type, the returned Method's Type field gives the
	// method signature, without a receiver, and the Func field is nil.
	//
	// Methods are sorted in lexicographic order.
	Method(int) Method

	// MethodByName returns the method with that name in the type's
	// method set and a boolean indicating if the method was found.
	//
	// For a non-interface type T or *T, the returned Method's Type and Func
	// fields describe a function whose first argument is the receiver.
	//
	// For an interface type, the returned Method's Type field gives the
	// method signature, without a receiver, and the Func field is nil.
	MethodByName(string) (Method, bool)

	// NumMethod returns the number of methods accessible using Method.
	//
	// For a non-interface type, it returns the number of exported methods.
	//
	// For an interface type, it returns the number of exported and unexported methods.
	NumMethod() int

	// Name returns the type's name within its package for a defined type.
	// For other (non-defined) types it returns the empty string.
	Name() string

	// PkgPath returns a defined type's package path, that is, the import path
	// that uniquely identifies the package, such as "encoding/base64".
	// If the type was predeclared (string, error) or not defined (*T, struct{},
	// []int, or A where A is an alias for a non-defined type), the package path
	// will be the empty string.
	PkgPath() string

	// Size returns the number of bytes needed to store
	// a value of the given type; it is analogous to unsafe.Sizeof.
	Size() uintptr

	// String returns a string representation of the type.
	// The string representation may use shortened package names
	// (e.g., base64 instead of "encoding/base64") and is not
	// guaranteed to be unique among types. To test for type identity,
	// compare the Types directly.
	String() string

	// Kind returns the specific kind of this type.
	Kind() Kind

	// Implements reports whether the type implements the interface type u.
	Implements(u Type) bool

	// AssignableTo reports whether a value of the type is assignable to type u.
	AssignableTo(u Type) bool

	// ConvertibleTo reports whether a value of the type is convertible to type u.
	// Even if ConvertibleTo returns true, the conversion may still panic.
	// For example, a slice of type []T is convertible to *[N]T,
	// but the conversion will panic if its length is less than N.
	ConvertibleTo(u Type) bool

	// Comparable reports whether values of this type are comparable.
	// Even if Comparable returns true, the comparison may still panic.
	// For example, values of interface type are comparable,
	// but the comparison will panic if their dynamic type is not comparable.
	Comparable() bool

	// Bits returns the size of the type in bits.
	// It panics if the type's Kind is not one of the
	// sized or unsized Int, Uint, Float, or Complex kinds.
	Bits() int

	// ChanDir returns a channel type's direction.
	// It panics if the type's Kind is not Chan.
	ChanDir() ChanDir

	// IsVariadic reports whether a function type's final input parameter
	// is a "..." parameter. If so, t.In(t.NumIn() - 1) returns the parameter's
	// implicit actual type []T.
	//
	// For concreteness, if t represents func(x int, y ... float64), then
	//
	//	t.NumIn() == 2
	//	t.In(0) is the reflect.Type for "int"
	//	t.In(1) is the reflect.Type for "[]float64"
	//	t.IsVariadic() == true
	//
	// IsVariadic panics if the type's Kind is not Func.
	IsVariadic() bool

	// Elem returns a type's element type.
	// It panics if the type's Kind is not Array, Chan, Map, Pointer, or Slice.
	Elem() Type

	// Field returns a struct type's i'th field.
	// It panics if the type's Kind is not Struct.
	// It panics if i is not in the range [0, NumField()).
	Field(i int) StructField

	// FieldByIndex returns the nested field corresponding
	// to the index sequence. It is equivalent to calling Field
	// successively for each index i.
	// It panics if the type's Kind is not Struct.
	FieldByIndex(index []int) StructField

	// FieldByName returns the struct field with the given name
	// and a boolean indicating if the field was found.
	// If the returned field is promoted from an embedded struct,
	// then Offset in the returned StructField is the offset in
	// the embedded struct.
	FieldByName(name string) (StructField, bool)

	// FieldByNameFunc returns the struct field with a name
	// that satisfies the match function and a boolean indicating if
	// the field was found.
	//
	// FieldByNameFunc considers the fields in the struct itself
	// and then the fields in any embedded structs, in breadth first order,
	// stopping at the shallowest nesting depth containing one or more
	// fields satisfying the match function. If multiple fields at that depth
	// satisfy the match function, they cancel each other
	// and FieldByNameFunc returns no match.
	// This behavior mirrors Go's handling of name lookup in
	// structs containing embedded fields.
	//
	// If the returned field is promoted from an embedded struct,
	// then Offset in the returned StructField is the offset in
	// the embedded struct.
	FieldByNameFunc(match func(string) bool) (StructField, bool)

	// In returns the type of a function type's i'th input parameter.
	// It panics if the type's Kind is not Func.
	// It panics if i is not in the range [0, NumIn()).
	In(i int) Type

	// Key returns a map type's key type.
	// It panics if the type's Kind is not Map.
	Key() Type

	// Len returns an array type's length.
	// It panics if the type's Kind is not Array.
	Len() int

	// NumField returns a struct type's field count.
	// It panics if the type's Kind is not Struct.
	NumField() int

	// NumIn returns a function type's input parameter count.
	// It panics if the type's Kind is not Func.
	NumIn() int

	// NumOut returns a function type's output parameter count.
	// It panics if the type's Kind is not Func.
	NumOut() int

	// Out returns the type of a function type's i'th output parameter.
	// It panics if the type's Kind is not Func.
	// It panics if i is not in the range [0, NumOut()).
	Out(i int) Type

	// OverflowComplex reports whether the complex128 x cannot be represented by type t.
	// It panics if t's Kind is not Complex64 or Complex128.
	OverflowComplex(x complex128) bool

	// OverflowFloat reports whether the float64 x cannot be represented by type t.
	// It panics if t's Kind is not Float32 or Float64.
	OverflowFloat(x float64) bool

	// OverflowInt reports whether the int64 x cannot be represented by type t.
	// It panics if t's Kind is not Int, Int8, Int16, Int32, or Int64.
	OverflowInt(x int64) bool

	// OverflowUint reports whether the uint64 x cannot be represented by type t.
	// It panics if t's Kind is not Uint, Uintptr, Uint8, Uint16, Uint32, or Uint64.
	OverflowUint(x uint64) bool

	// CanSeq reports whether a [Value] with this type can be iterated over using [Value.Seq].
	CanSeq() bool

	// CanSeq2 reports whether a [Value] with this type can be iterated over using [Value.Seq2].
	CanSeq2() bool
	// contains filtered or unexported methods
}
```

**基础信息查询**

| 方法名称         | 功能描述             | 返回值     | 适用类型 | 注意事项             | 示例（输出）                                           |
| ------------ | ---------------- | ------- | ---- | ---------------- | ------------------------------------------------ |
| Kind()       | 返回类型的底层种类        | Kind    | 所有类型 | 优先使用此方法判断类型      | reflect.TypeOf(42).Kind() -> reflect.Int         |
| Name()       | 返回类型名称（仅定义类型）    | string  | 所有类型 | 非定义类型返回空字符串      | reflect.TypeOf("").Name() -> "string" (预定义类型有名称) |
| PkgPath()    | 返回定义类型的包路径       | string  | 定义类型 | 非定义类型返回空字符串      | reflect.TypeOf(time.Time{}).PkgPath() -> "time"  |
| String()     | 返回类型的字符串表示       | string  | 所有类型 | 格式不保证唯一性，用于调试    | reflect.TypeOf([]int{}).String() -> "[]int"      |
| Size()       | 返回类型值的内存大小       | uintptr | 所有类型 | 对于引用类型，返回的是描述符大小 | reflect.TypeOf(int64(0)).Size() -> 8             |
| Align()      | 返回内存分配时的对齐字节数    | int     | 所有类型 |                  | reflect.TypeOf(int64(0)).Align() -> 8            |
| FieldAlign() | 返回作为结构体字段时的对齐字节数 | int     | 所有类型 |                  | reflect.TypeOf(int64(0)).FieldAlign() -> 8       |

**类型关系检查**

| 方法名称                  | 功能描述         | 返回值  | 适用类型 | 注意事项          | 示例（输出）                                   |
| --------------------- | ------------ | ---- | ---- | ------------- | ---------------------------------------- |
| Implements(u Type)    | 检查是否实现某接口    | bool | 所有类型 | 参数u必须是接口类型    | dogType.Implements(speakerType) -> true  |
| AssignableTo(u Type)  | 检查是否可赋值给目标类型 | bool | 所有类型 | 遵循Go赋值规则      | intType.AssignableTo(floatType) -> false |
| ConvertibleTo(u Type) | 检查是否可转换为目标类型 | bool | 所有类型 | 转换可能丢失精度或溢出   | intType.ConvertibleTo(floatType) -> true |
| Comparable()          | 检查类型值是否可比较   | bool | 所有类型 | 可比较类型才可用==操作符 | sliceType.Comparable() -> false          |

**复合类型操作**

- ​**​结构体操作​**​：

| 方法名称                                     | 功能描述        | 返回值                 | 适用类型   | 注意事项                 | 示例（输出）                                              |
| ---------------------------------------- | ----------- | ------------------- | ------ | -------------------- | --------------------------------------------------- |
| NumField()                               | 返回结构体字段数量   | int                 | Struct | 非结构体类型调用会panic       | userType.NumField() -> 2                            |
| Field(i int)                             | 返回结构体第i个字段  | StructField         | Struct | i必须在[0, NumField())内 | userType.Field(0).Name -> "ID"                      |
| FieldByName(name string)                 | 按名称查找结构体字段  | (StructField, bool) | Struct |                      | userType.FieldByName("Name") -> (StructField, true) |
| FieldByNameFunc(match func(string) bool) | 使用函数匹配字段名   | (StructField, bool) | Struct |                      | 略                                                   |
| FieldByIndex(index []int)                | 按索引序列查找嵌套字段 | StructField         | Struct | 索引序列表示嵌套访问路径         | 略                                                   |

- ​**​函数操作​**​：

| 方法名称         | 功能描述        | 返回值  | 适用类型 | 注意事项               | 示例（输出）                        |
| ------------ | ----------- | ---- | ---- | ------------------ | ----------------------------- |
| NumIn()      | 返回函数参数数量    | int  | Func | 非函数类型调用会panic      | funcType.NumIn() -> 2         |
| In(i int)    | 返回第i个参数类型   | Type | Func | i必须在[0, NumIn())内  | funcType.In(0) -> int         |
| NumOut()     | 返回函数返回值数量   | int  | Func | 非函数类型调用会panic      | funcType.NumOut() -> 1        |
| Out(i int)   | 返回第i个返回值类型  | Type | Func | i必须在[0, NumOut())内 | funcType.Out(0) -> bool       |
| IsVariadic() | 检查是否为可变参数函数 | bool | Func | 非函数类型调用会panic      | funcType.IsVariadic() -> true |
- ​**​容器操作​**​：

|方法名称|功能描述|返回值|适用类型|注意事项|示例（输出）|
|---|---|---|---|---|---|
|Elem()|返回容器元素类型|Type|Array, Chan, Map, Ptr, Slice|非容器类型调用会panic|sliceType.Elem() -> int|
|Key()|返回映射的键类型|Type|Map|非映射类型调用会panic|mapType.Key() -> string|
|Len()|返回数组长度|int|Array|非数组类型调用会panic|arrayType.Len() -> 3|
|ChanDir()|返回通道方向|ChanDir|Chan|非通道类型调用会panic|chanType.ChanDir() -> reflect.BothDir|
- **数值类型专用方法**

| 方法名称                          | 功能描述           | 返回值  | 适用类型                          | 注意事项             | 示例（输出）                                                  |
| ----------------------------- | -------------- | ---- | ----------------------------- | ---------------- | ------------------------------------------------------- |
| Bits()                        | 返回类型位数         | int  | Int*, Uint*, Float*, Complex* | 非数值类型调用会panic    | intType.Bits() -> 64                                    |
| OverflowInt(x int64)          | 检查整数x是否超出类型范围  | bool | Int*, Uint*                   | 非整数类型调用会panic    | int8Type.OverflowInt(128) -> true                       |
| OverflowUint(x uint64)        | 检查无符号整数x是否超出范围 | bool | Uint*                         | 非无符号整数类型调用会panic | uint8Type.OverflowUint(256) -> true                     |
| OverflowFloat(x float64)      | 检查浮点数x是否超出范围   | bool | Float*                        | 非浮点类型调用会panic    | float32Type.OverflowFloat(1e100) -> true                |
| OverflowComplex(x complex128) | 检查复数x是否超出范围    | bool | Complex*                      | 非复数类型调用会panic    | complex64Type.OverflowComplex(complex(1e100,0)) -> true |
- **其他方法**

|方法名称|功能描述|返回值|适用类型|注意事项|示例（输出）|
|---|---|---|---|---|---|
|CanSeq()|是否可迭代（Go1.22+）|bool|所有类型|用于检查是否支持Seq迭代|sliceType.CanSeq() -> true|
|CanSeq2()|是否可键值迭代（Go1.22+）|bool|所有类型|用于检查是否支持Seq2迭代|mapType.CanSeq2() -> true|
### 3.1.1 ArrayOf(length int, elem Type) Type

​**​功能​**​：创建数组类型  
​**​参数​**​：

- `length int`：数组长度
- `elem Type`：元素类型

​**​返回值​**​：数组类型  
​**​注意事项​**​：

- 长度必须为正整数
- 元素类型不能为无效类型
- 总大小不能超过可用地址空间

```go
func main() {
	elemType := reflect.TypeOf(0) // int
	arrayType := reflect.ArrayOf(5, elemType)
	
	fmt.Println("创建的数组类型:", arrayType)
	fmt.Println("种类:", arrayType.Kind())
	fmt.Println("长度:", arrayType.Len())
	fmt.Println("元素类型:", arrayType.Elem())
}

/**
创建的数组类型: [5]int
种类: array
长度: 5
元素类型: int
*/
```
### 3.1.2 ChanOf(dir ChanDir, t Type) Type

​**​功能​**​：创建通道类型  
​**​参数​**​：

- `dir ChanDir`：通道方向（`reflect.RecvDir`, `reflect.SendDir`, `reflect.BothDir`）
- `t Type`：元素类型

​**​返回值​**​：通道类型  
​**​注意事项​**​：

- 元素类型不能超过 64KB 大小限制
- 元素类型必须为有效类型

```go
func main() {
	elemType := reflect.TypeOf("")
	chanType := reflect.ChanOf(reflect.BothDir, elemType)
	
	fmt.Println("创建的通道类型:", chanType)
	fmt.Println("种类:", chanType.Kind())
	fmt.Println("方向:", chanType.ChanDir())
	fmt.Println("元素类型:", chanType.Elem())
}

/**
创建的通道类型: chan string
种类: chan
方向: chan
元素类型: string
*/
```
### 3.1.3 FuncOf(in, out \[\]Type, variadic bool) Type

​**​功能​**​：创建函数类型  
​**​参数​**​：

- `in []Type`：输入参数类型
- `out []Type`：输出结果类型
- `variadic bool`：是否可变参数

​**​返回值​**​：函数类型  
​**​注意事项​**​：

- 可变参数时，最后一个输入参数必须是切片类型
- 参数类型不能为无效类型

```go
func main() {
	in := []reflect.Type{
		reflect.TypeOf(0),        // int
		reflect.TypeOf(""),        // string
	}
	out := []reflect.Type{
		reflect.TypeOf(true),       // bool
		reflect.TypeOf(error(nil)), // error
	}
	
	funcType := reflect.FuncOf(in, out, false)
	
	fmt.Println("创建的函数类型:", funcType)
	fmt.Println("参数数量:", funcType.NumIn())
	fmt.Println("返回值数量:", funcType.NumOut())
}

/**
创建的函数类型: func(int, string) (bool, error)
参数数量: 2
返回值数量: 2
*/
```
### 3.1.4 MapOf(key, elem Type) Type

​**​功能​**​：创建映射类型  
​**​参数​**​：

- `key Type`：键类型
- `elem Type`：值类型

​**​返回值​**​：映射类型  
​**​注意事项​**​：

- 键类型必须可比较（实现 `==` 操作符）
- 键类型不能为无效类型

```go
func main() {
	keyType := reflect.TypeOf("")
	elemType := reflect.TypeOf(0)
	mapType := reflect.MapOf(keyType, elemType)
	
	fmt.Println("创建的映射类型:", mapType)
	fmt.Println("键类型:", mapType.Key())
	fmt.Println("值类型:", mapType.Elem())
}

/**
创建的映射类型: map[string]int
键类型: string
值类型: int
*/
```
### 3.1.5 SliceOf(t Type) Type

​**​功能​**​：创建切片类型  
​**​参数​**​：

- `t Type`：元素类型

​**​返回值​**​：切片类型  
​**​注意事项​**​：

- 元素类型必须为有效类型

```go
func main() {
	elemType := reflect.TypeOf(3.14) // float64
	sliceType := reflect.SliceOf(elemType)
	
	fmt.Println("创建的切片类型:", sliceType)
	fmt.Println("元素类型:", sliceType.Elem())
}

/**
创建的切片类型: []float64
元素类型: float64
*/
```
### 3.1.6 StructOf(fields \[\]StructField) Type

​**​功能​**​：创建结构体类型  
​**​参数​**​：

- `fields []StructField`：字段定义

​**​返回值​**​：结构体类型  
​**​注意事项​**​：

- 不支持导出未导出字段
- 不支持嵌入字段的方法提升
- 字段偏移量会自动计算

```go
func main() {
	fields := []reflect.StructField{
		{
			Name: "ID",
			Type: reflect.TypeOf(0),
			Tag:  `json:"id"`,
		},
		{
			Name: "Name",
			Type: reflect.TypeOf(""),
			Tag:  `json:"name"`,
		},
	}
	
	structType := reflect.StructOf(fields)
	
	fmt.Println("创建的结构体类型:", structType)
	fmt.Println("字段数量:", structType.NumField())
	
	for i := 0; i < structType.NumField(); i++ {
		field := structType.Field(i)
		fmt.Printf("字段 %d: %s (类型: %s, 标签: %s)\n", 
			i+1, field.Name, field.Type, field.Tag)
	}
}

/**
创建的结构体类型: struct { ID int; Name string }
字段数量: 2
字段 1: ID (类型: int, 标签: json:"id")
字段 2: Name (类型: string, 标签: json:"name")
*/
```
### 3.1.7 PointerTo(t Type) Type (Go 1.18+)

​**​功能​**​：创建指针类型  
​**​参数​**​：

- `t Type`：指向的类型

​**​返回值​**​：指针类型  
​**​注意事项​**​：

- 替代已弃用的 `PtrTo`
- 类型必须为有效类型

```go
func main() {
	baseType := reflect.TypeOf(User{})
	ptrType := reflect.PointerTo(baseType)
	
	fmt.Println("创建的指针类型:", ptrType)
	fmt.Println("指向类型:", ptrType.Elem())
}

/**
创建的指针类型: *main.User
指向类型: main.User
*/
```
### 3.1.8 TypeFor\[T any\]() Type (Go 1.22+)

​**​功能​**​：获取泛型类型表示  
​**​返回值​**​：类型表示  
​**​注意事项​**​：

- 用于泛型场景的类型获取
- 比 `TypeOf` 更类型安全

```go
func main() {
	// 获取泛型类型
	intType := reflect.TypeFor[int]()
	stringType := reflect.TypeFor[string]()
	
	fmt.Println("int 类型:", intType)
	fmt.Println("string 类型:", stringType)
	
	// 泛型结构体
	type Box[T any] struct {
		Content T
	}
	
	boxType := reflect.TypeFor[Box[string]]()
	fmt.Println("Box[string] 类型:", boxType)
}

/**
int 类型: int
string 类型: string
Box[string] 类型: main.Box[string]
*/
```
### 3.1.9 func TypeOf(i any) Type

`TypeOf` 返回一个 `reflect.Type` 值，该值表示参数 `i` 的动态类型（运行时实际类型）。返回值是一个接口类型，提供了对类型信息的全面访问能力。

**参数说明**

- `i any`：任意类型的值（通常为空接口 `interface{}`）
    - 可以是基本类型、复合类型、函数、接口等任何 Go 值
    - 可以接收指针、结构体、切片等任意值

**返回值**

- `Type`：表示 `i` 的动态类型的 `reflect.Type` 接口值
- 特殊返回值：当 `i` 是未赋值的 `nil` 接口时（`var i interface{}`），返回 `nil`

```go
package main

import (
	"fmt"
	"reflect"
)

func main() {
	// 基本类型
	fmt.Printf("int: %s\n", reflect.TypeOf(42))
	fmt.Printf("string: %s\n", reflect.TypeOf("hello"))
	fmt.Printf("float64: %s\n", reflect.TypeOf(3.14))
	fmt.Printf("bool: %s\n", reflect.TypeOf(true))
	
	// 复合类型
	fmt.Printf("slice: %s\n", reflect.TypeOf([]int{1, 2, 3}))
	fmt.Printf("map: %s\n", reflect.TypeOf(map[string]int{"a": 1}))
	fmt.Printf("channel: %s\n", reflect.TypeOf(make(chan int)))
	
	// 结构体类型
	type Point struct{ X, Y int }
	fmt.Printf("struct: %s\n", reflect.TypeOf(Point{}))
	
	// 函数类型
	fmt.Printf("function: %s\n", reflect.TypeOf(func() {}))
	
	// 接口处理
	var i interface{}
	fmt.Printf("nil interface: %v\n", reflect.TypeOf(i)) // nil
	
	var s *string
	fmt.Printf("nil pointer: %s\n", reflect.TypeOf(s)) // *string
}

/**
int: int
string: string
float64: float64
bool: bool
slice: []int
map: map[string]int
channel: chan int
struct: main.Point
function: func()
nil interface: <nil>
nil pointer: *string
*/
```
## 3.2 Value类型

`reflect.Value` 是 Go 反射系统的核心类型，它封装了 Go 值的运行时表示，提供了操作值的强大能力。

### 3.2.1 func ValueOf(i any) Value

​**​功能​**​：创建 `Value` 实例  
​**​参数​**​：`i any` - 任意 Go 值  
​**​返回值​**​：表示该值的 `Value`  
​**​注意事项​**​：

- 接收任何类型的值
- 包含接口的运行时类型信息
- 对于 `nil` 接口返回零值 `Value`
### 3.2.2 func Zero(typ Type) Value

​**​功能​**​：创建类型零值的 `Value`  
​**​参数​**​：`typ Type` - 目标类型  
​**​返回值​**​：零值 `Value`  
​**​注意事项​**​：

- 返回的值不可设置
- 对于指针类型返回 `nil`

```go
func main() {
    // 基本类型零值
    intZero := reflect.Zero(reflect.TypeOf(0))
    fmt.Printf("int zero: %v\n", intZero)
    
    // 结构体零值
    type User struct{ Name string }
    userZero := reflect.Zero(reflect.TypeOf(User{}))
    fmt.Printf("struct zero: %v\n", userZero)
    
    // 切片零值
    sliceZero := reflect.Zero(reflect.TypeOf([]int(nil)))
    fmt.Printf("slice zero: %v (is nil: %t)\n", sliceZero, sliceZero.IsNil())
}
/* 输出:
int zero: 0
struct zero: {}
slice zero: [] (is nil: true)
*/
```
### 3.2.3 func New(typ Type) Value

​**​功能​**​：创建指向类型零值的指针 `Value`  
​**​参数​**​：`typ Type` - 目标类型  
​**​返回值​**​：指向新分配值的指针 `Value`  
​**​注意事项​**​：

- 返回的值可设置
- 相当于 `&new(T)`

```go
func main() {
    // 创建新指针
    ptrValue := reflect.New(reflect.TypeOf(0))
    fmt.Printf("指针类型: %s\n", ptrValue.Type()) // *int
    
    // 设置值
    ptrValue.Elem().SetInt(42)
    fmt.Printf("指针值: %v\n", ptrValue.Elem())
    
    // 结构体指针
    type User struct{ Name string }
    userPtr := reflect.New(reflect.TypeOf(User{}))
    userPtr.Elem().FieldByName("Name").SetString("Alice")
    fmt.Printf("用户: %v\n", userPtr.Elem())
}
/* 输出:
指针类型: *int
指针值: 42
用户: {Alice}
*/
```

|                          **​函数名​**​                           | ​**​功能描述​**​ | ​**​参数说明​**​                      | ​**​返回值​**​ | ​**​注意事项​**​      |
| :-----------------------------------------------------------: | ------------ | --------------------------------- | ----------- | ----------------- |
|                       `ValueOf(i any)`                        | 创建值的反射表示     | `i`: 任意值                          | `Value`     | 返回值的运行时表示         |
|                       `Zero(typ Type)`                        | 创建类型零值       | `typ`: 目标类型                       | `Value`     | 返回的值不可设置          |
|                        `New(typ Type)`                        | 创建指向类型零值的指针  | `typ`: 目标类型                       | `Value`     | 返回指针的 `Value`，可设置 |
|              `NewAt(typ Type, p unsafe.Pointer)`              | 在指定地址创建指针    | `typ`: 类型, `p`: 内存地址              | `Value`     | 用于访问特定内存地址        |
|               `MakeChan(typ Type, buffer int)`                | 创建通道         | `typ`: 通道类型, `buffer`: 缓冲区大小      | `Value`     | 通道元素类型必须有效        |
| `MakeFunc(typ Type, fn func(args []Value) (results []Value))` | 动态创建函数       | `typ`: 函数类型, `fn`: 实现函数           | `Value`     | 函数签名必须匹配          |
|                      `MakeMap(typ Type)`                      | 创建空映射        | `typ`: 映射类型                       | `Value`     | 键类型必须可比较          |
|              `MakeMapWithSize(typ Type, n int)`               | 创建预分配大小的映射   | `typ`: 映射类型, `n`: 初始容量            | `Value`     | 性能优化用             |
|              `MakeSlice(typ Type, len, cap int)`              | 创建切片         | `typ`: 切片类型, `len`: 长度, `cap`: 容量 | `Value`     | 返回可设置的切片          |
|         `SliceAt(typ Type, p unsafe.Pointer, n int)`          | 在地址创建切片      | `typ`: 切片类型, `p`: 地址, `n`: 长度     | `Value`     | 用于底层内存操作          |

### 3.2.4 值获取方法

#### 3.2.4.1 Interface() any

​**​功能​**​：将 `Value` 转换为 `interface{}`  
​**​注意事项​**​：

- 需要值可导出或可寻址
- 返回原始值的副本

```go
func main() {
    v := reflect.ValueOf("hello")
    iface := v.Interface().(string)
    fmt.Println("接口值:", iface) // hello
    
    // 不可寻址值的处理
    s := []int{1, 2, 3}
    sliceVal := reflect.ValueOf(s)
    elem := sliceVal.Index(0)
    // elem.Interface() // 会panic，因为切片元素不可寻址
}
```
#### 3.2.4.2 类型特定获取方法

- `Int() int64`：获取整数值
- `Uint() uint64`：获取无符号整数值
- `Float() float64`：获取浮点数值
- `Bool() bool`：获取布尔值
- `String() string`：获取字符串值
- `Bytes() []byte`：获取字节切片值
- `Complex() complex128`：获取复数值

```go
func main() {
    values := []interface{}{
        42,
        uint(100),
        3.14,
        true,
        "hello",
        []byte{1, 2, 3},
        complex(1, 2),
    }
    
    for _, v := range values {
        val := reflect.ValueOf(v)
        switch val.Kind() {
        case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
            fmt.Printf("整数值: %d\n", val.Int())
        case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64, reflect.Uintptr:
            fmt.Printf("无符号值: %d\n", val.Uint())
        case reflect.Float32, reflect.Float64:
            fmt.Printf("浮点值: %f\n", val.Float())
        case reflect.Bool:
            fmt.Printf("布尔值: %t\n", val.Bool())
        case reflect.String:
            fmt.Printf("字符串值: %q\n", val.String())
        case reflect.Slice:
            if val.Type().Elem().Kind() == reflect.Uint8 {
                fmt.Printf("字节切片: %v\n", val.Bytes())
            }
        case reflect.Complex64, reflect.Complex128:
            fmt.Printf("复数值: %v\n", val.Complex())
        }
    }
}
```
### 3.2.5 值设置方法

#### 3.2.5.1 Set(x Value)

​**​功能​**​：设置值（需可设置）  
​**​前提​**​：

- `v.CanSet() == true`
- `x` 类型可赋值给 `v` 类型

```go
func main() {
    var x int
    v := reflect.ValueOf(&x).Elem() // 获取可设置的Value
    
    fmt.Println("原始值:", x)
    v.Set(reflect.ValueOf(42))
    fmt.Println("设置后:", x)
    
    // 直接设置方法
    v.SetInt(100)
    fmt.Println("再次设置:", x)
}
/* 输出:
原始值: 0
设置后: 42
再次设置: 100
*/
```
#### 3.2.5.2 类型特定设置方法

- `SetInt(x int64)`
- `SetUint(x uint64)`
- `SetFloat(x float64)`
- `SetBool(x bool)`
- `SetString(x string)`
- `SetBytes(x []byte)`
- `SetComplex(x complex128)`

```go
func main() {
    // 可设置的结构体
    type Config struct {
        Timeout int
        Enabled bool
    }
    
    cfg := &Config{}
    v := reflect.ValueOf(cfg).Elem()
    
    // 设置字段值
    v.FieldByName("Timeout").SetInt(30)
    v.FieldByName("Enabled").SetBool(true)
    
    fmt.Printf("配置: %+v\n", cfg)
}
/* 输出:
配置: &{Timeout:30 Enabled:true}
*/
```
### 3.2.6 切片操作

#### 3.2.6.1 func MakeSlice(typ Type, len, cap int) Value

​**​功能​**​：创建切片 `Value`  
​**​参数​**​：

- `typ Type`：切片元素类型
- `len int`：切片长度
- `cap int`：切片容量

​**​返回值​**​：切片 `Value`  
​**​注意事项​**​：

- 返回的切片可设置
- 容量不能小于长度

```go
func main() {
    // 创建 int 切片
    sliceType := reflect.SliceOf(reflect.TypeOf(0))
    sliceVal := reflect.MakeSlice(sliceType, 3, 5)
    
    // 设置元素值
    for i := 0; i < sliceVal.Len(); i++ {
        sliceVal.Index(i).SetInt(int64(i * 10))
    }
    
    fmt.Println("切片:", sliceVal.Interface()) // [0 10 20]
    
    // 修改长度
    sliceVal.SetLen(2)
    fmt.Println("截断后:", sliceVal.Interface()) // [0 10]
}
```
#### 3.2.6.2 Append(s Value, x ...Value) Value

​**​功能​**​：向切片追加元素  
​**​参数​**​：

- `s Value`：目标切片
- `x ...Value`：要追加的元素

​**​返回值​**​：新切片 `Value`  
​**​注意事项​**​：

- 原始切片不会被修改
- 返回新切片需重新赋值

```go
func main() {
    slice := []int{1, 2, 3}
    sVal := reflect.ValueOf(slice)
    
    // 追加单个元素
    newSlice := reflect.Append(sVal, reflect.ValueOf(4))
    fmt.Println("追加后:", newSlice.Interface()) // [1 2 3 4]
    
    // 追加多个元素
    newSlice = reflect.Append(newSlice, reflect.ValueOf(5), reflect.ValueOf(6))
    fmt.Println("再次追加:", newSlice.Interface()) // [1 2 3 4 5 6]
}
```
#### 3.2.6.3 AppendSlice(s, t Value) Value

​**​功能​**​：向切片追加另一个切片  
​**​参数​**​：

- `s Value`：目标切片
- `t Value`：要追加的切片

​**​返回值​**​：新切片 `Value`  
​**​注意事项​**​：

- 两个切片元素类型必须相同

```go
func main() {
    s1 := []int{1, 2, 3}
    s2 := []int{4, 5, 6}
    
    s1Val := reflect.ValueOf(s1)
    s2Val := reflect.ValueOf(s2)
    
    newSlice := reflect.AppendSlice(s1Val, s2Val)
    fmt.Println("合并切片:", newSlice.Interface()) // [1 2 3 4 5 6]
}
```

| **方法名​**​                     | ​**​功能描述​**​ | ​**​参数说明​**​     | ​**​返回值​**​ | ​**​注意事项​**​ |
| ----------------------------- | ------------ | ---------------- | ----------- | ------------ |
| `Append(s Value, x ...Value)` | 追加元素         | `s`: 切片, `x`: 元素 | `Value`     | 返回新切片        |
| `AppendSlice(s, t Value)`     | 追加切片         | `s`: 目标, `t`: 源  | `Value`     | 元素类型必须相同     |
| `Cap()`                       | 获取容量         | 无                | `int`       | 适用于切片/数组/通道  |
| `Len()`                       | 获取长度         | 无                | `int`       | 适用于容器类型      |
| `Index(i int)`                | 获取元素         | `i`: 索引          | `Value`     |              |
| `Slice(i, j int)`             | 切片操作         | `i,j`: 起止索引      | `Value`     |              |
| `Slice3(i, j, k int)`         | 带容量切片        | `i,j,k`: 索引      | `Value`     |              |
| `SetLen(n int)`               | 设置长度         | `n`: 新长度         | 无           | 必须可设置        |
| `SetCap(n int)`               | 设置容量         | `n`: 新容量         | 无           | 必须可设置        |
| `Grow(n int)`                 | 增加容量         | `n`: 增加量         | 无           | Go 1.20+     |
| `Clear()`                     | 清空容器         | 无                | 无           | 切片设长度0，映射清空  |
### 3.2.7 映射操作
#### 3.2.7.1 func MakeMap(typ Type) Value

​**​功能​**​：创建映射 `Value`  
​**​参数​**​：`typ Type` - 映射类型  
​**​返回值​**​：映射 `Value`  
​**​注意事项​**​：

- 键类型必须可比较
- 返回的映射可设置

```go
func main() {
    // 创建 map[string]int
    mapType := reflect.MapOf(
        reflect.TypeOf(""),
        reflect.TypeOf(0),
    )
    mapVal := reflect.MakeMap(mapType)
    
    // 添加键值对
    key := reflect.ValueOf("score")
    value := reflect.ValueOf(95)
    mapVal.SetMapIndex(key, value)
    
    fmt.Println("映射:", mapVal.Interface()) // map[score:95]
}
```
#### 3.2.7.2 SetMapIndex(key, elem Value)

​**​功能​**​：设置映射键值对  
​**​参数​**​：

- `key Value`：键
- `elem Value`：值

​**​注意事项​**​：

- 映射必须可设置
- 键类型必须匹配

```go
func main() {
    m := make(map[string]int)
    mVal := reflect.ValueOf(m)
    
    key := reflect.ValueOf("score")
    value := reflect.ValueOf(95)
    mVal.SetMapIndex(key, value)
    
    fmt.Println("映射:", m) // map[score:95]
}
```
#### 3.2.7.3 MapIndex(key Value) Value

​**​功能​**​：获取映射值  
​**​返回值​**​：值 `Value`（无效值表示键不存在）

```go
func main() {
    m := map[string]int{"score": 95}
    mVal := reflect.ValueOf(m)
    
    key := reflect.ValueOf("score")
    value := mVal.MapIndex(key)
    fmt.Println("分数:", value.Int()) // 95
    
    // 不存在的键
    key = reflect.ValueOf("age")
    value = mVal.MapIndex(key)
    fmt.Println("值有效:", value.IsValid()) // false
}
```

| **方法名​**​                      | ​**​功能描述​**​ | ​**​参数说明​**​        | ​**​返回值​**​ | ​**​注意事项​**​ |
| ------------------------------ | ------------ | ------------------- | ----------- | ------------ |
| `MapIndex(key Value)`          | 获取键值         | `key`: 键            | `Value`     | 无效值表示键不存在    |
| `MapKeys()`                    | 获取所有键        | 无                   | `[]Value`   |              |
| `MapRange()`                   | 获取迭代器        | 无                   | `*MapIter`  |              |
| `SetMapIndex(key, elem Value)` | 设置键值         | `key`: 键, `elem`: 值 | 无           |              |
| `SetIterKey(iter *MapIter)`    | 设置迭代器键       | `iter`: 迭代器         | 无           |              |
| `SetIterValue(iter *MapIter)`  | 设置迭代器值       | `iter`: 迭代器         | 无           |              |
### 3.2.8 通道操作
#### 3.2.8.1 func MakeChan(typ Type, buffer int) Value

​**​功能​**​：创建通道 `Value`  
​**​参数​**​：

- `typ Type`：通道元素类型
- `buffer int`：缓冲区大小

​**​返回值​**​：通道 `Value`  
​**​注意事项​**​：

- 返回的通道可操作
- 缓冲区大小 >= 0

```go
func main() {
    // 创建 int 通道
    chanType := reflect.ChanOf(reflect.BothDir, reflect.TypeOf(0))
    chanVal := reflect.MakeChan(chanType, 1)
    
    // 发送值
    sendVal := reflect.ValueOf(42)
    chanVal.Send(sendVal)
    
    // 接收值
    recvVal, ok := chanVal.Recv()
    if ok {
        fmt.Println("接收值:", recvVal.Int()) // 42
    }
}
```
#### 3.2.8.2 Send(x Value)

​**​功能​**​：向通道发送值  
​**​注意事项​**​：

- 通道必须可发送
- 值类型必须匹配

```go
func main() {
    ch := make(chan int, 1)
    chVal := reflect.ValueOf(ch)
    
    // 发送值
    chVal.Send(reflect.ValueOf(42))
    
    // 接收验证
    fmt.Println("接收值:", <-ch) // 42
}
```
#### 3.2.8.3 Recv() (Value, bool)

​**​功能​**​：从通道接收值  
​**​返回值​**​：

- `Value`：接收的值
- `bool`：是否成功接收

```go
func main() {
    ch := make(chan string, 1)
    ch <- "hello"
    
    chVal := reflect.ValueOf(ch)
    val, ok := chVal.Recv()
    fmt.Printf("值: %s, 成功: %t\n", val.String(), ok) // hello, true
}
```

| **方法名​**​          | ​**​功能描述​**​ | ​**​参数说明​**​ | ​**​返回值​**​     | ​**​注意事项​**​ |
| ------------------ | ------------ | ------------ | --------------- | ------------ |
| `Send(x Value)`    | 发送值          | `x`: 发送值     | 无               | 通道必须可发送      |
| `Recv()`           | 接收值          | 无            | `(Value, bool)` |              |
| `TryRecv()`        | 尝试接收         | 无            | `(Value, bool)` | 非阻塞          |
| `TrySend(x Value)` | 尝试发送         | `x`: 发送值     | `bool`          | 非阻塞          |
| `Close()`          | 关闭通道         | 无            | 无               |              |
### 3.2.9 结构体操作

#### 3.2.9.1 Field(i int) Value

​**​功能​**​：获取结构体字段值  
​**​注意事项​**​：

- 仅适用于结构体类型
- 索引从 0 开始

```go
func main() {
    type User struct {
        Name string
        Age  int
    }
    
    u := User{"Alice", 30}
    uVal := reflect.ValueOf(u)
    
    // 获取字段
    nameField := uVal.Field(0)
    ageField := uVal.Field(1)
    
    fmt.Printf("字段0: %s (%s)\n", nameField.String(), nameField.Type())
    fmt.Printf("字段1: %d (%s)\n", ageField.Int(), ageField.Type())
}
/* 输出:
字段0: Alice (string)
字段1: 30 (int)
*/
```
#### 3.2.9.2 FieldByName(name string) Value

​**​功能​**​：按名称获取字段值  
​**​返回值​**​：字段值 `Value`（无效值表示字段不存在）

```go
func main() {
    type Config struct {
        Timeout int
        Retry   bool
    }
    
    cfg := Config{Timeout: 30, Retry: true}
    cfgVal := reflect.ValueOf(cfg)
    
    // 获取字段
    timeoutField := cfgVal.FieldByName("Timeout")
    retryField := cfgVal.FieldByName("Retry")
    
    fmt.Printf("超时: %d\n", timeoutField.Int())
    fmt.Printf("重试: %t\n", retryField.Bool())
    
    // 不存在的字段
    invalidField := cfgVal.FieldByName("Invalid")
    fmt.Println("字段有效:", invalidField.IsValid()) // false
}
```

| **方法名​**​                                  | ​**​功能描述​**​ | ​**​参数说明​**​  | ​**​返回值​**​      | ​**​注意事项​**​ |
| ------------------------------------------ | ------------ | ------------- | ---------------- | ------------ |
| `Field(i int)`                             | 获取字段         | `i`: 字段索引     | `Value`          |              |
| `FieldByIndex(index []int)`                | 嵌套字段访问       | `index`: 索引路径 | `Value`          |              |
| `FieldByIndexErr(index []int)`             | 嵌套字段访问(带错误)  | `index`: 索引路径 | `(Value, error)` |              |
| `FieldByName(name string)`                 | 按名称获取字段      | `name`: 字段名   | `Value`          |              |
| `FieldByNameFunc(match func(string) bool)` | 函数匹配字段       | `match`: 匹配函数 | `Value`          |              |
| `NumField()`                               | 字段数量         | 无             | `int`            |              |
### 3.2.10 函数调用方法

#### 3.2.10.1 Call(in \[\]Value) \[\]Value

​**​功能​**​：调用函数  
​**​参数​**​：`in []Value` - 参数列表  
​**​返回值​**​：返回值列表  
​**​注意事项​**​：

- 函数必须为 `Func` 类型
- 参数数量和类型必须匹配

```go
func main() {
    // 定义函数
    add := func(a, b int) int {
        return a + b
    }
    
    addVal := reflect.ValueOf(add)
    
    // 准备参数
    args := []reflect.Value{
        reflect.ValueOf(10),
        reflect.ValueOf(20),
    }
    
    // 调用函数
    results := addVal.Call(args)
    fmt.Println("结果:", results[0].Int()) // 30
}
```
#### 3.2.10.2 CallSlice(in \[\]Value) \[\]Value

​**​功能​**​：调用可变参数函数  
​**​参数​**​：`in []Value` - 参数列表  
​**​返回值​**​：返回值列表  
​**​注意事项​**​：

- 最后一个参数必须是切片
- 相当于展开切片作为可变参数

```go
func main() {
    // 可变参数函数
    sum := func(nums ...int) int {
        total := 0
        for _, n := range nums {
            total += n
        }
        return total
    }
    
    sumVal := reflect.ValueOf(sum)
    
    // 准备参数
    args := []reflect.Value{
        reflect.ValueOf([]int{1, 2, 3, 4}),
    }
    
    // 调用函数
    results := sumVal.CallSlice(args)
    fmt.Println("总和:", results[0].Int()) // 10
}
```

| **方法名​**​                   | ​**​功能描述​**​ | ​**​参数说明​**​ | ​**​返回值​**​ | ​**​注意事项​**​ |
| --------------------------- | ------------ | ------------ | ----------- | ------------ |
| `Call(in []Value)`          | 调用函数         | `in`: 参数列表   | `[]Value`   | 参数必须匹配       |
| `CallSlice(in []Value)`     | 调用可变函数       | `in`: 参数列表   | `[]Value`   | 最后参数为切片      |
| `NumMethod()`               | 方法数量         | 无            | `int`       |              |
| `Method(i int)`             | 获取方法         | `i`: 方法索引    | `Value`     |              |
| `MethodByName(name string)` | 按名称获取方法      | `name`: 方法名  | `Value`     |              |
### 3.2.11 指针操作

| **方法名​**​                      | ​**​功能描述​**​      | ​**​参数说明​**​ | ​**​返回值​**​      | ​**​注意事项​**​ |
| ------------------------------ | ----------------- | ------------ | ---------------- | ------------ |
| `Elem()`                       | 解引用               | 无            | `Value`          | 适用于指针/接口     |
| `Pointer()`                    | 获取指针值             | 无            | `uintptr`        |              |
| `UnsafeAddr()`                 | 获取地址              | 无            | `uintptr`        | 值必须可寻址       |
| `UnsafePointer()`              | 获取 unsafe.Pointer | 无            | `unsafe.Pointer` |              |
| `SetPointer(x unsafe.Pointer)` | 设置指针              | `x`: 新指针     | 无                |              |
| `Indirect(v Value)`            | 解引用指针             | `v`: 值       | `Value`          | 非指针返回原值      |
### 3.2.12 类型检查与转换

#### 3.2.12.1 CanConvert(t Type) bool

​**​功能​**​：检查值是否可转换为目标类型  
​**​返回值​**​：是否可转换

```go
func main() {
    v := reflect.ValueOf(3.14)
    intType := reflect.TypeOf(0)
    stringType := reflect.TypeOf("")
    
    fmt.Println("可转换为 int:", v.CanConvert(intType)) // true
    fmt.Println("可转换为 string:", v.CanConvert(stringType)) // false
}
```
#### 3.2.12.2 Convert(t Type) Value

​**​功能​**​：转换值到目标类型  
​**​返回值​**​：转换后的 `Value`  
​**​注意事项​**​：

- 转换可能丢失精度
- 必须 `CanConvert` 返回 `true`

```go
func main() {
    v := reflect.ValueOf(3.14)
    intVal := v.Convert(reflect.TypeOf(0))
    fmt.Println("转换结果:", intVal.Int()) // 3
}
```

| **方法名​**​            | ​**​功能描述​**​ | ​**​参数说明​**​ | ​**​返回值​**​ | ​**​注意事项​**​ |
| -------------------- | ------------ | ------------ | ----------- | ------------ |
| `Kind()`             | 获取底层类型       | 无            | `Kind`      | 优先使用此方法      |
| `Type()`             | 获取类型信息       | 无            | `Type`      |              |
| `CanAddr()`          | 是否可寻址        | 无            | `bool`      |              |
| `CanSet()`           | 是否可设置        | 无            | `bool`      |              |
| `CanConvert(t Type)` | 是否可转换        | `t`: 目标类型    | `bool`      |              |
| `IsNil()`            | 是否为 nil      | 无            | `bool`      | 适用于指针/接口等    |
| `IsValid()`          | 是否有效         | 无            | `bool`      | 零值 Value 无效  |
| `IsZero()`           | 是否零值         | 无            | `bool`      |              |
| `Comparable()`       | 是否可比较        | 无            | `bool`      |              |
### 3.2.13 特殊操作
#### 3.2.13.1 Indirect(v Value) Value

​**​功能​**​：获取指针指向的值  
​**​等价于​**​：

- 如果 `v` 是指针：`v.Elem()`
- 否则：`v`

```go
func main() {
    x := 42
    vPtr := reflect.ValueOf(&x)
    
    // 直接获取值
    v := reflect.Indirect(vPtr)
    fmt.Println("值:", v.Int()) // 42
}
```
#### 3.2.13.2 SetZero()

​**​功能​**​：将值设为零值  
​**​注意事项​**​：

- 值必须可设置
- 相当于 `v.Set(reflect.Zero(v.Type()))`

```go
func main() {
    var x int = 42
    v := reflect.ValueOf(&x).Elem()
    
    fmt.Println("原始值:", x)
    v.SetZero()
    fmt.Println("设零后:", x) // 0
}
```
#### 3.2.13.3 Select(cases \[\]SelectCase) (chosen int, recv Value, recvOK bool)

**功能说明**

动态模拟 `select` 语句，在多个通道操作中选择一个就绪的操作执行。

**参数说明**

- `cases []SelectCase`：选择分支列表
    - `Dir SelectDir`：操作方向（`SelectSend`、`SelectRecv`、`SelectDefault`）
    - `Chan Value`：通道值
    - `Send Value`：发送值（仅 `SelectSend` 时使用）

**返回值**

- `chosen int`：选中的分支索引
- `recv Value`：接收的值（仅接收操作）
- `recvOK bool`：接收是否成功

**使用场景**

- 动态处理多个通道
- 实现通用通道选择器
- 构建事件驱动系统

```go
package main

import (
	"fmt"
	"reflect"
	"time"
)

func main() {
	ch1 := make(chan int, 1)
	ch2 := make(chan string, 1)
	
	// 发送初始值
	ch1 <- 42
	ch2 <- "hello"
	
	// 创建选择分支
	cases := []reflect.SelectCase{
		{
			Dir:  reflect.SelectRecv,
			Chan: reflect.ValueOf(ch1),
		},
		{
			Dir:  reflect.SelectRecv,
			Chan: reflect.ValueOf(ch2),
		},
		{
			Dir:  reflect.SelectDefault,
		},
	}
	
	// 执行选择
	for i := 0; i < 3; i++ {
		chosen, recv, recvOK := reflect.Select(cases)
		fmt.Printf("选择分支 %d: ", chosen)
		
		switch chosen {
		case 0, 1: // 接收分支
			if recvOK {
				fmt.Printf("接收值: %v (%s)\n", recv, recv.Type())
			} else {
				fmt.Println("通道已关闭")
			}
		case 2: // 默认分支
			fmt.Println("默认分支")
		}
		
		// 清空通道
		if chosen == 0 || chosen == 1 {
			cases[chosen].Chan = reflect.ValueOf(nil)
		}
	}
	
	// 添加发送操作
	sendCase := reflect.SelectCase{
		Dir:  reflect.SelectSend,
		Chan: reflect.ValueOf(ch1),
		Send: reflect.ValueOf(100),
	}
	cases = append(cases, sendCase)
	
	// 执行发送
	chosen, _, _ := reflect.Select(cases)
	fmt.Printf("选择分支 %d: 发送成功\n", chosen)
	
	// 验证发送结果
	val := <-ch1
	fmt.Println("接收发送值:", val)
}
```
#### 3.2.13.4 Seq() iter.Seq\[Value\] (Go 1.22+)

**功能说明**

返回值的迭代序列（实现 `iter.Seq[Value]`）

**支持类型**

- 数组
- 切片
- 字符串
- 映射（迭代键）
- 通道（接收值）

**使用场景**

- 统一迭代接口
- 简化反射迭代代码
- 与 Go 1.22 迭代器函数集成

```go
package main

import (
	"fmt"
	"iter"
	"reflect"
)

func main() {
	// 切片迭代
	slice := []int{10, 20, 30}
	sliceSeq := reflect.ValueOf(slice).Seq()
	
	fmt.Println("切片迭代:")
	for v := range sliceSeq {
		fmt.Printf("值: %v\n", v.Interface())
	}
	
	// 字符串迭代
	str := "Hello"
	strSeq := reflect.ValueOf(str).Seq()
	
	fmt.Println("\n字符串迭代:")
	for v := range strSeq {
		fmt.Printf("字符: %c\n", v.Interface().(rune))
	}
	
	// 映射迭代
	m := map[string]int{"a": 1, "b": 2}
	mapSeq := reflect.ValueOf(m).Seq()
	
	fmt.Println("\n映射键迭代:")
	for k := range mapSeq {
		fmt.Printf("键: %s\n", k.Interface())
	}
	
	// 通道迭代
	ch := make(chan int, 2)
	ch <- 100
	ch <- 200
	close(ch)
	
	chSeq := reflect.ValueOf(ch).Seq()
	
	fmt.Println("\n通道迭代:")
	for v := range chSeq {
		fmt.Printf("接收值: %v\n", v.Interface())
	}
}

/**
切片迭代:
值: 10
值: 20
值: 30

字符串迭代:
字符: H
字符: e
字符: l
字符: l
字符: o

映射键迭代:
键: a
键: b

通道迭代:
接收值: 100
接收值: 200
*/
```

| **方法名​**​                    | ​**​功能描述​**​ | ​**​参数说明​**​  | ​**​返回值​**​               | ​**​注意事项​**​       |
| ---------------------------- | ------------ | ------------- | ------------------------- | ------------------ |
| `Select(cases []SelectCase)` | 多路选择         | `cases`: 选择分支 | `(int, Value, bool)`      | 模拟 select          |
| `Equal(u Value)`             | 深度比较         | `u`: 比较值      | `bool`                    | 递归比较               |
| `Seq()`                      | 迭代序列         | 无             | `iter.Seq[Value]`         | Go 1.22+           |
| `Seq2()`                     | 键值迭代         | 无             | `iter.Seq2[Value, Value]` | Go 1.22+  **仅限映射** |
### 3.2.14 数值检查

|**方法名​**​|​**​功能描述​**​|​**​参数说明​**​|​**​返回值​**​|​**​注意事项​**​|
|---|---|---|---|---|
|`OverflowInt(x int64)`|检查整数溢出|`x`: 测试值|`bool`||
|`OverflowUint(x uint64)`|检查无符号溢出|`x`: 测试值|`bool`||
|`OverflowFloat(x float64)`|检查浮点溢出|`x`: 测试值|`bool`||
|`OverflowComplex(x complex128)`|检查复数溢出|`x`: 测试值|`bool`||
## 3.3 Kind类型

`reflect.Kind` 是 Go 反射系统中表示类型基础种类的枚举类型，它是理解和使用反射的基础。

```go
type Kind uint
```

`Kind` 表示 Go 类型系统的基本分类，它标识了类型的底层表示形式。与 `reflect.Type` 不同，`Kind` 不区分自定义类型和内置类型，只关注基础种类。

```go
const (
    Invalid Kind = iota  // 无效类型
    Bool                 // 布尔类型
    Int                  // 有符号整型（平台相关）
    Int8                 // int8
    Int16                // int16
    Int32                // int32
    Int64                // int64
    Uint                 // 无符号整型（平台相关）
    Uint8                // uint8
    Uint16               // uint16
    Uint32               // uint32
    Uint64               // uint64
    Uintptr              // uintptr
    Float32              // float32
    Float64              // float64
    Complex64            // complex64
    Complex128           // complex128
    Array                // 数组
    Chan                 // 通道
    Func                 // 函数
    Interface            // 接口
    Map                  // 映射
    Pointer              // 指针
    Slice                // 切片
    String               // 字符串
    Struct               // 结构体
    UnsafePointer        // unsafe.Pointer
)
```

### 3.3.1 func (k Kind) String() string

​**​功能​**​：返回种类的字符串表示  
​**​返回值​**​：种类名称（如 "int"、"slice" 等）  
​**​注意事项​**​：

- 用于调试和日志输出
- 比直接使用整数更易读

**核心用途**

1. ​**​类型基础判断​**​：快速确定值的底层表示形式
2. ​**​类型安全操作​**​：在调用类型特定方法前进行验证
3. ​**​性能优化​**​：比完整类型检查更高效
4. ​**​泛型处理​**​：在泛型代码中处理不同类型的基础操作

```go
package main

import (
	"fmt"
	"reflect"
	"unsafe"
)

func main() {
	// 测试各种类型
	testTypes := []interface{}{
		true,                      // Bool
		int(42),                   // Int (平台相关)
		int8(8),                   // Int8
		int16(16),                 // Int16
		int32(32),                 // Int32
		int64(64),                 // Int64
		uint(42),                  // Uint
		uint8(8),                  // Uint8
		uint16(16),                // Uint16
		uint32(32),                // Uint32
		uint64(64),                // Uint64
		uintptr(unsafe.Pointer(nil)), // Uintptr
		float32(3.14),             // Float32
		float64(3.14159),          // Float64
		complex64(1 + 2i),         // Complex64
		complex128(3 + 4i),        // Complex128
		[3]int{1, 2, 3},           // Array
		make(chan int),            // Chan
		func() {},                 // Func
		interface{}(nil),          // Interface
		make(map[string]int),      // Map
		new(int),                  // Pointer
		[]int{1, 2, 3},            // Slice
		"hello",                   // String
		struct{}{},                // Struct
		unsafe.Pointer(new(int)),  // UnsafePointer
	}

	// 遍历并识别类型
	for i, v := range testTypes {
		kind := reflect.TypeOf(v).Kind()
		fmt.Printf("%2d. %-15T -> Kind: %-15s (%d)\n", 
			i+1, v, kind, kind)
	}
}
```
## 3.4 StructField 类型

`StructField` 描述结构体中的单个字段，包含字段的元数据信息。

```go
type StructField struct {
    Name    string      // 字段名
    Type    Type        // 字段类型
    Tag     StructTag   // 字段标签
    Offset  uintptr     // 字段在结构体中的字节偏移量
    Index   []int       // 索引序列（用于嵌套字段）
    Anonymous bool      // 是否为匿名字段
}
```

**核心用途**

1. 获取结构体字段信息
2. 解析字段标签
3. 处理嵌套结构
4. 动态访问字段值

### 3.4.1 func VisibleFields(t Type) \[\]StructField (Go 1.17+)

**功能说明**

获取结构体所有可见字段（包括嵌入字段的字段）

**参数说明**

- `t Type`：结构体类型

**返回值**

- `[]StructField`：所有可见字段

**核心用途**

处理包含嵌入字段的结构体

```go
package main

import (
	"fmt"
	"reflect"
)

type Base struct {
	ID        int `json:"id"`
	CreatedAt int64
}

type User struct {
	Base        // 嵌入字段
	Name     string
	Email    string
	internal int // 未导出字段
}

func main() {
	userType := reflect.TypeOf(User{})
	
	fmt.Println("=== 标准字段 ===")
	for i := 0; i < userType.NumField(); i++ {
		field := userType.Field(i)
		fmt.Printf("%s (匿名字段: %t)\n", field.Name, field.Anonymous)
	}
	
	fmt.Println("\n=== 可见字段 ===")
	visible := reflect.VisibleFields(userType)
	for _, field := range visible {
		fmt.Printf("%s (来源: %s, 匿名字段: %t)\n", 
			field.Name, field.Type, field.Anonymous)
	}
}

/**
=== 标准字段 ===
Base (匿名字段: true)
Name (匿名字段: false)
Email (匿名字段: false)
internal (匿名字段: false)

=== 可见字段 ===
ID (来源: int, 匿名字段: false)
CreatedAt (来源: int64, 匿名字段: false)
Name (来源: string, 匿名字段: false)
Email (来源: string, 匿名字段: false)
internal (来源: int, 匿名字段: false)
*/
```

**注意事项**

1. ​**​字段顺序​**​：按字段在内存中的布局排序
2. ​**​包含未导出字段​**​：但无法直接访问值
3. ​**​嵌入字段展开​**​：将嵌入字段的字段提升到外层
### 3.4.2 func (f StructField) IsExported() bool (Go 1.17+)

**功能说明**

检查字段是否为导出字段（首字母大写）

**返回值**

- `bool`：是否导出

**使用场景**

安全地处理可能包含未导出字段的结构体

```go
func printExportedFields(t reflect.Type) {
	fmt.Printf("\n结构体 %s 的导出字段:\n", t.Name())
	
	for _, field := range reflect.VisibleFields(t) {
		if field.IsExported() {
			fmt.Printf("- %s\n", field.Name)
		}
	}
}

func main() {
	printExportedFields(reflect.TypeOf(User{}))
}

/**
结构体 User 的导出字段:
- ID
- CreatedAt
- Name
- Email
*/
```
## 3.5 StructTag 类型

表示结构体字段的标签字符串（反引号内的内容）

```go
type StructTag string
```

解析字段标签（如 JSON、XML、数据库ORM标签）
### 3.5.1 func (tag StructTag) Get(key string) string

​**​功能​**​：获取标签值  
​**​参数​**​：`key string` - 标签键  
​**​返回值​**​：标签值（不存在时返回空字符串）  
​**​注意事项​**​：

- 不区分大小写
- 只返回第一个匹配值
- 支持逗号分隔的多个值
### 3.5.2 func (tag StructTag) Lookup(key string) (value string, ok bool)

​**​功能​**​：检查并获取标签值  
​**​参数​**​：`key string` - 标签键  
​**​返回值​**​：

- `value string`：标签值
- `ok bool`：是否存在  
    ​**​注意事项​**​：
- 区分大小写（Go 1.14+）
- 可以明确区分空值和不存在

```go
package main

import (
	"fmt"
	"reflect"
)

type Config struct {
	Host     string `env:"HOST" default:"localhost"`
	Port     int    `env:"PORT" default:"8080"`
	LogLevel string `env:"LOG_LEVEL" options:"debug,info,warn,error"`
	Timeout  int    `env:"TIMEOUT"` // 无默认值
	Secret   string `env:"SECRET,secret"` // 带选项
}

func parseConfigTag(tag reflect.StructTag) {
	fmt.Println("\n解析配置标签:")
	
	// 使用 Get
	host := tag.Get("env")
	fmt.Printf("Get(\"env\"): %q\n", host)
	
	// 使用 Lookup
	if port, ok := tag.Lookup("env"); ok {
		fmt.Printf("Lookup(\"env\"): %q (存在)\n", port)
	}
	
	// 获取默认值
	if def, ok := tag.Lookup("default"); ok {
		fmt.Printf("默认值: %q\n", def)
	}
	
	// 获取选项
	if opts, ok := tag.Lookup("options"); ok {
		fmt.Printf("选项: %q\n", opts)
	}
	
	// 处理逗号分隔值
	if secret, ok := tag.Lookup("env"); ok {
		fmt.Printf("原始值: %q\n", secret)
		// 分割键值
		if value, opts := parseTagOptions(secret); value != "" {
			fmt.Printf("解析后: 值=%q, 选项=%v\n", value, opts)
		}
	}
}

// 解析逗号分隔的标签值
func parseTagOptions(tag string) (value string, options []string) {
	parts := strings.Split(tag, ",")
	if len(parts) > 0 {
		value = parts[0]
		options = parts[1:]
	}
	return
}

func main() {
	configType := reflect.TypeOf(Config{})
	
	// 遍历字段解析标签
	for i := 0; i < configType.NumField(); i++ {
		field := configType.Field(i)
		fmt.Printf("\n字段: %s\n", field.Name)
		parseConfigTag(field.Tag)
	}
}
```
## 3.6 MapIter 类型

`reflect.MapIter` 是 Go 反射系统中用于安全、高效遍历映射的迭代器类型。它提供了比 `MapKeys()` 更高效的内存使用方式，特别适合处理大型映射。

```go
type MapIter struct {
    // 包含未导出字段
}
```

`MapIter` 是一个映射迭代器，用于遍历映射的键值对。它通过避免一次性分配所有键值对，显著降低了大型映射遍历时的内存开销。

#### 3.6.1.1 func (iter \*MapIter) Key() Value

​**​功能​**​：返回当前键的 `Value`  
​**​返回值​**​：键的反射值  
​**​注意事项​**​：

- 必须在 `Next()` 返回 `true` 后调用
- 返回的值在迭代期间有效

#### 3.6.1.2 func (iter \*MapIter) Value() Value

​**​功能​**​：返回当前值的 `Value`  
​**​返回值​**​：值的反射值  
​**​注意事项​**​：

- 必须在 `Next()` 返回 `true` 后调用
- 返回的值在迭代期间有效

#### 3.6.1.3 func (iter \*MapIter) Next() bool

​**​功能​**​：推进到下一个键值对  
​**​返回值​**​：

- `true`：还有下一个键值对
- `false`：迭代结束

​**​注意事项​**​：

- 首次调用前迭代器未定位
- 返回 `false` 后不应再调用 `Key()` 或 `Value()`

#### 3.6.1.4 func (iter \*MapIter) Reset(v Value)

​**​功能​**​：重置迭代器以遍历新映射  
​**​参数​**​：`v Value` - 新的映射值  
​**​注意事项​**​：

- `v` 必须是映射类型
- 重置后需重新调用 `Next()` 开始迭代

```go
package main

import (
	"fmt"
	"reflect"
)

func main() {
	// 创建测试映射
	population := map[string]int{
		"China":  1411,
		"India":  1380,
		"USA":    331,
		"Russia": 146,
		"Japan":  126,
	}
	
	// 获取映射的反射值
	mapVal := reflect.ValueOf(population)
	
	// 创建映射迭代器
	iter := mapVal.MapRange()
	
	fmt.Println("=== 国家人口数据 ===")
	
	// 遍历映射
	for iter.Next() {
		key := iter.Key()
		value := iter.Value()
		
		// 安全获取键值
		country := key.String()
		pop := value.Int()
		
		fmt.Printf("%-10s: %d 百万\n", country, pop)
	}
	
	// 重新创建迭代器计算平均值
	iter = mapVal.MapRange()
	total := 0
	count := 0
	
	for iter.Next() {
		total += int(iter.Value().Int())
		count++
	}
	
	if count > 0 {
		avg := float64(total) / float64(count)
		fmt.Printf("\n平均人口: %.1f 百万\n", avg)
	}
}

```
## 3.7 SelectCase 类型

表示 select 的一个 case

```go
type SelectCase struct {
    Dir  SelectDir // 操作方向
    Chan Value     // 通道值
    Send Value     // 发送值（仅当 Dir 为 SelectSend 时使用）
}
```
**使用场景​**​：

- 动态构建 select 语句
- 实现基于反射的通道选择

**关键点说明**

1. ​**​操作方向​**​：
    
    - `SelectSend`：向通道发送值
    - `SelectRecv`：从通道接收值
    - `SelectDefault`：默认操作（立即执行）
2. ​**​返回值​**​：
    
    - `chosen int`：选中的 case 索引
    - `recv Value`：接收的值（仅接收操作）
    - `recvOK bool`：接收是否成功
3. ​**​错误处理​**​：
    
    - 向已关闭通道发送会 panic
    - 从 nil 通道操作会永久阻塞
    - 使用 recover 处理可能的 panic
4. ​**​性能考虑​**​：
    
    - 比原生 select 慢约 10 倍
    - 适合动态构建 select 的场景

**使用注意事项**

1. ​**​通道状态​**​：
    
    - 关闭的通道接收会返回 `recvOK = false`
    - nil 通道会永久阻塞（除非有默认 case）
2. ​**​类型安全​**​：
    
    - 发送值类型必须匹配通道元素类型
    - 使用前检查 `Chan.IsValid()` 和 `Chan.Kind() == Chan`
3. ​**​默认操作​**​：
    
    - 当没有其他 case 就绪时执行
    - 没有 `Chan` 和 `Send` 字段
4. ​**​重置使用​**​：
    
    - 可以重用 `SelectCase` 切片
    - 修改 `Chan` 为 nil 可禁用 case
## 3.8 SelectDir 类型

表示 select 操作的方向

```go
const (
    SelectSend    SelectDir = iota // 发送操作
    SelectRecv                     // 接收操作
    SelectDefault                  // 默认操作
)
```

**使用场景​**​：

- 定义 `SelectCase` 的操作类型
- 指示通道操作方向
