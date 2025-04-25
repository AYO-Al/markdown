`atomic` 包（`sync/atomic`）提供了​**​原子操作​**​的底层支持，用于在多线程并发场景下安全地操作共享内存。它直接利用 CPU 的原子指令（如 CAS, Compare-And-Swap）实现无锁编程，适用于高性能、低延迟的场景。

`atomic` 包主要用于对 ​**​基本类型​**​（如 `int32`, `int64`, `uintptr`, `unsafe.Pointer` 等）进行原子操作，保证操作的 ​**​原子性​**​（即操作不可中断，不会被其他协程干扰）。

1. ​**​原子操作类型​**​
    
    - ​**​Swap（交换）​**​：直接替换内存中的值，返回旧值。
        
        ```go
        *addr, new = new, *addr  // 伪代码示意
        ```
        
    - ​**​Compare-and-Swap（CAS，比较并交换）​**​：仅在当前值等于 `old` 时更新为 `new`，返回是否成功。
        
        ```go
        if *addr == old { *addr = new }  // 伪代码示意
        ```
        
    - ​**​Add（增减）​**​：原子增减操作，返回新值。
        
        ```go
        *addr += delta  // 伪代码示意
        ```
        
    - ​**​Load（读取）​**​：原子读取值，避免读取到中间状态。
        
        ```go
        return *addr  // 伪代码示意
        ```
        
    - ​**​Store（写入）​**​：原子写入值，保证其他协程看到完整更新。
        
        ```go
        *addr = val  // 伪代码示意
        ```
        
2. ​**​使用注意事项​**​
    
    - ​**​需要极高的谨慎​**​：错误使用易引发数据竞争或逻辑错误。
    - ​**​优先选择高层同步工具​**​：多数场景应优先使用 `channel` 或 `sync` 包（如 `Mutex`、`WaitGroup`）。
    - ​**​设计原则​**​：
        - _“通过通信共享内存，而非通过共享内存通信”_（Go 并发哲学）。
3. ​**​内存模型与同步语义​**​
    
    - ​**​顺序一致性​**​：所有原子操作的行为像是按某种全局一致的顺序执行。
    - ​**​同步保证​**​：若原子操作 A 的结果被原子操作 B 观察到，则 A “同步发生于” B（保证操作可见性）。
    - ​**​与 C++/Java 的类比​**​：
        - 等同于 C++ 的 `sequentially consistent` 原子操作。
        - 类似于 Java 的 `volatile` 变量（但 Go 的原子操作更底层）。

# 1 不支持的类型
## 1.1 ​**​非固定位宽类型​**​

- ​**​`int` / `uint`​**​  
    不支持，因为其位宽依赖平台（32 位或 64 位），而原子操作需要明确的内存对齐和硬件指令支持。  
    ​**​替代方案​**​：显式使用 `int32`/`int64` 或 `uint32`/`uint64`。

## 1.2 ​**​浮点类型（`float32`/`float64`）​**​

- 不支持直接的原子操作。  
    ​**​原因​**​：硬件通常不提供浮点数的原子指令，且浮点数的位模式操作容易出错（如 NaN 的多种表示）。  
    ​**​替代方案​**​：通过 `math.Float64bits` 转为 `uint64` 进行原子操作，再转换回来。

## 1.3 ​**​结构体或复杂类型​**​

- 不支持直接操作。  
    ​**​原因​**​：原子操作的最小单位是“字长”（通常 32 或 64 位），复杂类型无法保证原子更新。  
    ​**​替代方案​**​：通过 `unsafe.Pointer` 或 `atomic.Pointer[T]` 替换整个结构体指针（需自行保证线程安全）。
# 2 为什么不支持？

## 2.1 ​**​硬件原子指令的局限性​**​

- CPU 的原子指令（如 CAS、LL/SC）通常仅针对整数和指针操作，无法直接支持复杂类型或浮点数。
- 例如，x86 的 `LOCK CMPXCHG` 指令支持 32/64 位整数，但不支持浮点数。

## 2.2 ​**​内存对齐要求​**​

- 原子操作要求变量必须 ​**​按自然对齐​**​（如 32 位变量按 4 字节对齐，64 位变量按 8 字节对齐）。
- Go 的 `atomic` 包隐式处理对齐问题，但用户仍需避免手动填充破坏对齐的结构体。

## 2.3 ​**​类型系统的安全性​**​

- `unsafe.Pointer` 和 `uintptr` 支持指针操作，但需要开发者自行保证内存安全。
- Go 1.19+ 的泛型原子类型（如 `atomic.Pointer[T]`）通过类型系统增强安全性，避免滥用 `unsafe`。

## 2.4 **​跨平台一致性​**​

- 固定位宽类型（如 `int32`）能确保不同平台上的行为一致，而 `int` 的位宽依赖平台，可能导致原子性失效。
# 3 常用函数

## 3.1 ** 原子增减（Add）​**​

​**​函数​**​：

- `AddInt32(addr *int32, delta int32) (new int32)`
- `AddInt64(addr *int64, delta int64) (new int64)`
- `AddUint32(addr *uint32, delta uint32) (new uint32)`
- `AddUint64(addr *uint64, delta uint64) (new uint64)`
- `AddUintptr(addr *uintptr, delta uintptr) (new uintptr)`

​**​作用​**​：  
原子地将 `delta` 值加到目标变量，返回操作后的新值。

​**​支持类型​**​：  
`int32`、`int64`、`uint32`、`uint64`、`uintptr`（无符号指针整数表示）。

​**​适用场景​**​：

- 计数器累加（如统计请求次数）。
- 无锁队列/栈的索引更新。

​**​注意事项​**​：

- ​**​无减法函数​**​：负数 `delta` 可用于 `int32`/`int64` 实现减法。
- ​**​溢出风险​**​：需自行处理数值溢出（如 `uint32` 溢出后回绕）。

## 3.2 ​**​原子位操作（And/Or）​**​

​**​函数​**​：

- ​**​按位与（And）​**​：  
    `AndInt32`、`AndInt64`、`AndUint32`、`AndUint64`、`AndUintptr`。
- ​**​按位或（Or）​**​：  
    `OrInt32`、`OrInt64`、`OrUint32`、`OrUint64`、`OrUintptr`。

​**​作用​**​：  
原子地对变量进行按位与（或）操作，返回操作前的旧值。

​**​支持类型​**​：  
`int32`、`int64`、`uint32`、`uint64`、`uintptr`。

​**​适用场景​**​：

- 标志位管理（如清除/设置某一位）。
- 状态机的位掩码操作。

​**​示例​**​：

```go
var flags uint32 = 0x0F
// 原子清除第3位（0-based）
old := atomic.AndUint32(&flags, ^uint32(1<<3))
```


## 3.3 ​**​原子比较并交换（Compare-and-Swap, CAS）​**​

​**​函数​**​：

- `CompareAndSwapInt32`、`CompareAndSwapInt64`、`CompareAndSwapUint32`、`CompareAndSwapUint64`、`CompareAndSwapUintptr`。
- `CompareAndSwapPointer(addr *unsafe.Pointer, old, new unsafe.Pointer) (swapped bool)`。

​**​作用​**​：  
若变量当前值等于 `old`，则替换为 `new`，返回是否成功。

​**​支持类型​**​：  
`int32`、`int64`、`uint32`、`uint64`、`uintptr`、`unsafe.Pointer`。

​**​适用场景​**​：

- 无锁数据结构（如链表节点更新）。
- 单次初始化（如 `sync.Once` 实现）。
- 乐观锁（先读后写，失败重试）。

​**​注意事项​**​：

- ​**​ABA问题​**​：需额外机制（如版本号）防止值被其他协程修改后恢复。

## 3.4 ​**​ 原子加载（Load）​**​

​**​函数​**​：

- `LoadInt32`、`LoadInt64`、`LoadUint32`、`LoadUint64`、`LoadUintptr`。
- `LoadPointer(addr *unsafe.Pointer) (val unsafe.Pointer)`。

​**​作用​**​：  
原子读取变量的值，避免读取到中间状态。

​**​支持类型​**​：  
`int32`、`int64`、`uint32`、`uint64`、`uintptr`、`unsafe.Pointer`。

​**​适用场景​**​：

- 安全读取其他协程可能修改的共享变量。
- 双检锁（Double-Checked Locking）中的条件检查。

## 3.5 ​**​原子存储（Store）​**​

​**​函数​**​：

- `StoreInt32`、`StoreInt64`、`StoreUint32`、`StoreUint64`、`StoreUintptr`。
- `StorePointer(addr *unsafe.Pointer, val unsafe.Pointer)`。

​**​作用​**​：  
原子写入新值到变量，保证其他协程看到完整更新。

​**​支持类型​**​：  
`int32`、`int64`、`uint32`、`uint64`、`uintptr`、`unsafe.Pointer`。

​**​适用场景​**​：

- 安全发布配置或资源指针。
- 状态标志的原子更新。

## 3.6 ​**​ 原子交换（Swap）​**​

​**​函数​**​：

- `SwapInt32`、`SwapInt64`、`SwapUint32`、`SwapUint64`、`SwapUintptr`。
- `SwapPointer(addr *unsafe.Pointer, new unsafe.Pointer) (old unsafe.Pointer)`。

​**​作用​**​：  
原子替换变量的值为 `new`，返回操作前的旧值。

​**​支持类型​**​：  
`int32`、`int64`、`uint32`、`uint64`、`uintptr`、`unsafe.Pointer`。

​**​适用场景​**​：

- 替换旧资源并释放（如连接池）。
- 实现无锁的线程安全发布。

## 3.7 ​**​类型支持总结​**​

| ​**​操作类型​**​           | ​**​支持的数据类型​**​                                              |
| ---------------------- | ------------------------------------------------------------ |
| ​**​Add​**​            | `int32`、`int64`、`uint32`、`uint64`、`uintptr`                  |
| ​**​And/Or​**​         | `int32`、`int64`、`uint32`、`uint64`、`uintptr`                  |
| ​**​CompareAndSwap​**​ | `int32`、`int64`、`uint32`、`uint64`、`uintptr`、`unsafe.Pointer` |
| ​**​Load​**​           | `int32`、`int64`、`uint32`、`uint64`、`uintptr`、`unsafe.Pointer` |
| ​**​Store​**​          | `int32`、`int64`、`uint32`、`uint64`、`uintptr`、`unsafe.Pointer` |
| ​**​Swap​**​           | `int32`、`int64`、`uint32`、`uint64`、`uintptr`、`unsafe.Pointer` |
# 4 常用类型

## 4.1 **`atomic.Bool`​**​

​**​作用​**​：提供原子布尔值操作，替代手动使用 `int32` 模拟布尔标志位。  
​**​方法​**​：

- ​**​`CompareAndSwap(old, new bool) (swapped bool)`​**​：若当前值等于 `old`，则替换为 `new`。
- ​**​`Load() bool`​**​：原子读取布尔值。
- ​**​`Store(val bool)`​**​：原子写入布尔值。
- ​**​`Swap(new bool) (old bool)`​**​：原子替换为新值，返回旧值。

```go
var flag atomic.Bool
flag.Store(true)
if flag.CompareAndSwap(true, false) {
    // 成功将标志位从 true 改为 false
}
```

​**​适用场景​**​：并发环境下的开关标志、状态标记。

## 4.2 ​**​`atomic.Int32` 和 `atomic.Int64`​**​

​**​作用​**​：封装有符号整数的原子操作，简化计数器、状态值管理。  
​**​方法​**​：

- ​**​`Add(delta int32/int64) (new int32/int64)`​**​：原子加减，返回新值。
- ​**​`And(mask int32/int64) (old int32/int64)`​**​：按位与操作，返回旧值。
- ​**​`Or(mask int32/int64) (old int32/int64)`​**​：按位或操作，返回旧值。
- ​**​`CompareAndSwap(old, new int32/int64) (swapped bool)`​**​：条件替换。
- ​**​`Load() int32/int64`​**​ / ​**​`Store(val int32/int64)`​**​：读写操作。
- ​**​`Swap(new int32/int64) (old int32/int64)`​**​：替换并返回旧值。

```go
var counter atomic.Int32
counter.Add(5) // 原子增加5
if counter.CompareAndSwap(5, 0) {
    // 重置计数器为0
}
```

​**​适用场景​**​：计数器、状态码、位掩码操作。


## 4.3 ​**​`atomic.Uint32`、`atomic.Uint64`、`atomic.Uintptr`​**​

​**​作用​**​：与 `Int32/Int64` 类似，但针对无符号整数和指针整数。  
​**​方法​**​：与 `Int32/Int64` 完全对称，支持 `Add`、`And`、`Or`、`CAS`、`Load`、`Store`、`Swap`。

​**​特殊类型​**​：

- ​**​`Uintptr`​**​：用于指针地址的原子操作（如手动管理内存）。

​**​示例​**​：

```go
var addr atomic.Uintptr
ptr := uintptr(unsafe.Pointer(new(int)))
old := addr.Swap(ptr) // 替换指针地址
```

​**​适用场景​**​：无符号计数器、位操作、底层指针管理。

## 4.4 ​**​atomic.Pointer\[T\]​**​

​**​作用​**​：类型安全的泛型指针原子操作，替代 `unsafe.Pointer`。  
​**​方法​**​：

- ​**​`CompareAndSwap(old, new *T) (swapped bool)`​**​：替换指针指向的对象。
- ​**​`Load() *T`​**​：读取当前指针。
- ​**​`Store(val *T)`​**​：写入新指针。
- ​**​`Swap(new *T) (old *T)`​**​：替换指针并返回旧值。

```go
type Data struct { value int }
var node atomic.Pointer[Data]

newNode := &Data{value: 42}
oldNode := node.Swap(newNode) // 原子替换节点
```

​**​适用场景​**​：无锁数据结构（如链表、树）、资源池、配置热更新。

​**​优势​**​：泛型确保类型安全，避免 `unsafe.Pointer` 的潜在错误。

## 4.5 ​**​ atomic.Value**​

​**​作用​**​：存储任意类型的原子对象，类似于旧版 `atomic.Value`，但方法更丰富。  
​**​方法​**​：

- ​**​`CompareAndSwap(old, new any) (swapped bool)`​**​：若当前值等于 `old`，则替换为 `new`。
- ​**​`Load() (val any)`​**​：读取存储的值。
- ​**​`Store(val any)`​**​：写入新值。
- ​**​`Swap(new any) (old any)`​**​：替换并返回旧值。


```go
var config atomic.Value
config.Store(map[string]string{"key": "value"})
current := config.Load().(map[string]string) // 类型断言
```