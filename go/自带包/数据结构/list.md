`container/list` 是 Go 标准库中实现​**​双向链表​**​的包，它提供了高效的插入和删除操作，特别适合需要频繁在首尾修改元素的场景。

`container/list` 作为 Go 标准库中的重要数据结构，为开发者提供了简洁高效的**非线程安全双向链表**实现。虽然在随机访问方面不如 slice，但在处理需要频繁插入、删除的队列式数据时，其 O(1) 的操作复杂度使其成为无可替代的选择。

| 特性    | list            | slice        | map          |
| ----- | --------------- | ------------ | ------------ |
| 首部插入  | ​**​O(1)​**​    | O(n)         | 不支持          |
| 中间插入  | O(1)            | O(n)         | 不支持          |
| 随机访问  | O(n)            | ​**​O(1)​**​ | ​**​O(1)​**​ |
| 内存占用  | 中等 (每个元素额外16字节) | 低            | 高            |
| 元素有序性 | 保持插入顺序          | 保持索引顺序       | 无序           |
# 1 Element

```go
// Element 表示双向链表中的一个节点
type Element struct {
    next, prev *Element // 前后节点指针
    list       *List    // 所属链表
    Value      any      // 存储的实际值
}
```
## 1.1 func (e \*Element) Next() \*Element

**功能说明**

- 返回当前元素的下一个元素
- 如果当前元素是尾元素或者不属于任何链表，则返回 `nil`

**返回值**

- `*Element`: 下一个链表节点指针
- 无错误返回

**使用注意事项**

1. ​**​空链表调用​**​：当元素不属于任何链表时返回 `nil`
2. ​**​尾元素处理​**​：尾元素的 `Next()` 必然返回 `nil`
3. ​**​并发安全​**​：遍历时可能被其他协程修改，需加锁

```go
package main

import (
    "container/list"
    "fmt"
    "sync"
)

func main() {
    l := list.New()
    l.PushBack("A")
    l.PushBack("B")
    l.PushBack("C")

    // 获取第一个元素
    first := l.Front()
    
    // 案例1：正常遍历
    fmt.Print("正向遍历: ")
    for e := first; e != nil; e = e.Next() {
        fmt.Printf("%s → ", e.Value)
    }
    // 输出: A → B → C → 
    
    // 案例2：尾元素测试
    last := l.Back()
    if last.Next() == nil {
        fmt.Println("\n尾元素的Next()返回nil") 
    }
    
    // 案例3：孤儿元素测试
    orphan := &list.Element{Value: "Orphan"}
    if orphan.Next() == nil {
        fmt.Println("孤儿元素的Next()返回nil")
    }
    
    // 案例4：并发安全处理
    var wg sync.WaitGroup
    var mu sync.Mutex
    
    wg.Add(1)
    go func() {
        defer wg.Done()
        
        mu.Lock()
        defer mu.Unlock()
        
        // 安全遍历
        for e := l.Front(); e != nil; e = e.Next() {
            fmt.Printf("%s ", e.Value)
        }
    }()
    wg.Wait()
    // 输出: A B C
}
```
## 1.2 func (e \*Element) Prev() \*Element

**功能说明**

- 返回当前元素的前一个元素
- 如果当前元素是首元素或者不属于任何链表，则返回 `nil`

**返回值**

- `*Element`: 前一个链表节点指针
- 无错误返回

**使用注意事项**

1. ​**​空链表调用​**​：当元素不属于任何链表时返回 `nil`
2. ​**​首元素处理​**​：首元素的 `Prev()` 必然返回 `nil`
3. ​**​环形链表模拟​**​：当用于环形结构时需手动连接首尾

```go
package main

import (
    "container/list"
    "fmt"
)

func main() {
    l := list.New()
    l.PushBack("X")
    l.PushBack("Y")
    l.PushBack("Z")
    
    // 获取最后一个元素
    last := l.Back()
    
    // 案例1：反向遍历
    fmt.Print("反向遍历: ")
    for e := last; e != nil; e = e.Prev() {
        fmt.Printf("%s → ", e.Value)
    }
    // 输出: Z → Y → X → 
    
    // 案例2：首元素测试
    first := l.Front()
    if first.Prev() == nil {
        fmt.Println("\n首元素的Prev()返回nil")
    }
    
    // 案例3：孤儿元素测试
    isolated := &list.Element{Value: "Isolated"}
    if isolated.Prev() == nil {
        fmt.Println("孤儿元素的Prev()返回nil")
    }
    
    // 案例4：手动创建环形链表
    fmt.Println("\n手动环形结构:")
    ringStart := &list.Element{Value: "LoopStart"}
    ringEnd := &list.Element{Value: "LoopEnd"}
    
    // 手动链接节点
    ringStart.next = ringEnd
    ringEnd.prev = ringStart
    ringEnd.next = ringStart // 关键：形成环
    ringStart.prev = ringEnd // 关键：形成环
    
    // 模拟环形遍历
    fmt.Print("环形遍历: ")
    current := ringStart
    for i := 0; i < 4; i++ {
        fmt.Printf("%s → ", current.Value)
        current = current.Prev() // 注意：使用Prev模拟逆时针
    }
    // 输出: LoopStart → LoopEnd → LoopStart → LoopEnd → 
}
```
# 2 List

```go
// List 表示一个双向链表
type List struct {
    root Element // 哨兵节点（不存储实际值）
    len  int     // 当前链表长度
}
```

​**​作用​**​：提供双向链表数据结构实现，支持高效的头尾操作和任意位置插入删除。
## 2.1 func New() \*List

**功能​**​：创建并初始化一个新的空链表  
​**​返回值​**​：新链表指针

```go
// 创建空链表
emptyList := list.New()
fmt.Println("长度:", emptyList.Len()) // 输出: 0

// 创建带元素的链表
filledList := list.New()
filledList.PushBack("A")
filledList.PushBack("B")
fmt.Printf("首元素: %v, 尾元素: %v\n", 
    filledList.Front().Value, 
    filledList.Back().Value) // 输出: 首元素: A, 尾元素: B
```
## 2.2 func (l \*List) Back() \*Element

**功能​**​：返回链表最后一个元素  
​**​返回值​**​：尾元素指针（链表为空时返回 nil）  
​**​注意事项​**​：

- 空链表调用返回 nil
- 修改尾元素需使用链表方法（如 MoveToBack）

```go
l := list.New()
l.PushBack(10)
l.PushBack(20)

last := l.Back()
fmt.Println("尾元素值:", last.Value) // 输出: 20

// 危险：直接修改可能导致数据不一致
last.Value = 30 // ⚠️ 可直接修改值但不改变链表结构

// 安全移动尾元素
l.MoveToFront(last) // ✅ 使用链表方法操作元素位置
fmt.Println("新尾元素:", l.Back().Value) // 输出: 10
```
## 2.3 func (l \*List) Front() \*Element

**功能​**​：返回链表第一个元素  
​**​返回值​**​：首元素指针（链表为空时返回 nil）

```go
l := list.New()
l.PushFront("First")
l.PushFront("NewFirst")

first := l.Front()
fmt.Println("首元素:", first.Value) // 输出: NewFirst

// 当链表为空时
emptyList := list.New()
if emptyList.Front() == nil {
    fmt.Println("空链表没有首元素") // ✅ 正确检测
}
```
## 2.4 func (l \*List) Init() \*List

**功能​**​：重置链表为空状态（O(1)时间）  
​**​返回值​**​：当前链表指针（便于链式调用）  
​**​注意事项​**​：

- 不会回收元素内存（可能需手动清空引用）
- 被移除的元素仍可能被外部引用

```go
l := list.New()
l.PushBack("A")
l.PushBack("B")

// 记录元素用于后续检查
elem := l.Front()

// 清空链表
l.Init() 
fmt.Println("长度:", l.Len()) // 输出: 0

// 危险：外部引用元素已被移出链表
fmt.Println("孤立元素值:", elem.Value) // 输出: A（还能访问值）
elem.Value = nil // ✅ 手动解引用防内存泄漏
```
## 2.5 func (l \*List) InsertAfter(v any, mark \*Element) \*Element

**参数​**​：

- `v`：插入的值
- `mark`：参照元素（新元素插入在其后）

​**​返回值​**​：新元素指针（无效操作时返回 nil）  
​**​注意事项​**​：

- `mark` 必须属于当前链表
- 插入位置必须在链表内

```go
l := list.New()
a := l.PushBack("A")
b := l.PushBack("B")

// 正确插入
newElem := l.InsertAfter("C", a)
fmt.Println(a.Next().Value) // 输出: C

// 错误示例1：使用不属于链表的元素
foreignElem := &list.Element{Value: "Foreign"}
if l.InsertAfter("X", foreignElem) == nil {
    fmt.Println("插入失败：无效参照元素") // ✅ 正确处理
}

// 错误示例2：使用已删除的元素
removed := l.Remove(b)
if l.InsertAfter("Y", removed) == nil {
    fmt.Println("插入失败：元素已被移除") // ✅
}
```
## 2.6 func (l \*List) InsertBefore(v any, mark \*Element) \*Element

类似 InsertAfter，但插入在 mark 元素之前
## 2.7 func (l \*List) Len() int

**功能​**​：返回链表长度  
​**​返回值​**​：当前元素数量（≥0）  
​**​特性​**​：复杂度 O(1)
## 2.8 func (l \*List) MoveAfter(e, mark \*Element)

**功能​**​：将元素 e 移动到 mark 之后  
​**​参数​**​：

- `e`：要移动的元素
- `mark`：目标位置元素

​**​注意事项​**​：

- 两元素必须属于同一链表
- e 和 mark 不能为同一元素
- 操作后原位置元素自动连接

```go
l := list.New()
elems := []*Element{
    l.PushBack(1),
    l.PushBack(2),
    l.PushBack(3),
}

// 移动元素3到元素1之后
l.MoveAfter(elems[2], elems[0])

// 验证结果
fmt.Println("链表顺序:")
current := l.Front()
for current != nil {
    fmt.Print(current.Value, " ")
    current = current.Next()
}
// 输出: 1 3 2
```
## 2.9 func (l \*List) MoveBefore(e, mark \*Element)

类似 MoveAfter，但移动到 mark 元素之前
## 2.10 func (l \*List) MoveToBack(e \*Element)

**功能​**​：移动元素到链表尾部  
​**​注意事项​**​：

- 元素必须属于当前链表
- 移动尾元素无实际效果但允许操作

```go
l := list.New()
a := l.PushBack("A")
b := l.PushBack("B")

// 移动首元素到尾部
l.MoveToBack(a)

// 危险：移动不属于链表的元素
foreign := &list.Element{Value: "X"}
l.MoveToBack(foreign) // ⚠️ 会导致panic崩溃！

// 安全检测（推荐实践）
if e.list == l {
    l.MoveToBack(e)
} else {
    fmt.Println("非法元素操作")
}
```
## 2.11 func (l \*List) MoveToFront(e \*Element)

类似 MoveToBack，但移动到头部
## 2.12 func (l \*List) PushBack(v any) \*Element

**功能​**​：尾部添加元素（O(1)）  
​**​返回值​**​：新元素指针

```go
l := list.New()

// 连续添加
e1 := l.PushBack("First")
e2 := l.PushBack("Second")

// 结果验证
fmt.Printf("尾元素: %v\n", l.Back().Value)  // Second
fmt.Printf("首元素: %v\n", l.Front().Value) // First
```
## 2.13 func (l \*List) PushBackList(other \*List)

**功能​**​：将另一链表所有元素添加到当前链表尾部  
​**​注意事项​**​：

- other 链表会被清空（元素移动）
- 添加后两个链表互不影响

```go
listA := list.New()
listA.PushBack("A1")
listA.PushBack("A2")

listB := list.New()
listB.PushBack("B1")
listB.PushBack("B2")

// 合并链表
listA.PushBackList(listB)

fmt.Println("合并后长度:", listA.Len()) // 4
fmt.Println("listB长度:", listB.Len())    // 0 (已清空)
```
## 2.14 func (l \*List) PushFront(v any) \*Element

类似 PushBack，但在头部添加

## 2.15 func (l \*List) PushFrontList(other \*List)

类似 PushBackList，但添加到头部
## 2.16 func (l \*List) Remove(e \*Element) any

**功能​**​：移除链表中的元素  
​**​参数​**​：要移除的元素指针  
​**​返回值​**​：被移除元素的值  
​**​错误情况​**​：

- 如果 e 为 nil：panic("list: Remove called on nil Element")
- 如果 e 不属于当前链表：panic("list: Remove called on element not in list")

​**​注意事项​**​：

- 移除后该元素不再属于链表
- 仍可访问该元素的值，但不应再用于链表操作

```go
l := list.New()
elem := l.PushBack("ToRemove")

// 正确移除
removedValue := l.Remove(elem)
fmt.Println("被移除的值:", removedValue)

// 致命错误1：移除空元素
// l.Remove(nil) // 触发panic

// 致命错误2：重复移除相同元素
// l.Remove(elem) // 触发panic (元素已不属于链表)

// 安全移除模式
if elem.list == l {
    value := l.Remove(elem)
    // 安全清理
    elem.Value = nil // 帮助GC
}
```

| 操作                 | 时间复杂度 | 解释     |
| ------------------ | ----- | ------ |
| PushFront/PushBack | O(1)  | 常数时间完成 |
| InsertBefore/After | O(1)  | 修改指针即可 |
| MoveToFront/Back   | O(1)  | 直接调整指针 |
| Remove             | O(1)  | 解除节点链接 |
| 按索引访问              | O(n)  | 需要顺序遍历 |
| 查找元素               | O(n)  | 需要顺序遍历 |