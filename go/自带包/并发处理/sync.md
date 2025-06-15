在 Go 语言中，`sync` 包是并发编程的核心标准库，提供了多种同步原语（synchronization primitives），用于协调多个 goroutine 之间的操作。

# 1 Mutex

Mutex是一种互斥锁。

```go
  
type Mutex struct {  
    _ noCopy  
  
    mu isync.Mutex  
}

type Mutex struct {
    state int32  // 锁状态和等待计数（复合位域）
    sema  uint32 // 信号量（用于阻塞/唤醒 goroutine）
}

```

- **作用**：保护共享资源的互斥访问，防止数据竞争（data race）。
- ​**使用场景**：当多个 goroutine 需要读写同一变量或数据结构时。
- **零值**：Mutex的零值是未锁定的Mutex。

```go
  
var mu sync.Mutex  
var count int  
  
func inc() {  
    
    //Lock：加锁，如果已经在加锁状态了则会阻塞直到Mutex可用
    mu.Lock()  

    /*
    Unlock：解锁，如果在解锁时未进入加锁状态会触发run-time error
    重复解锁会触发panic
    */
    defer mu.Unlock()  
    count++  
    fmt.Println(count)  
    time.Sleep(1 * time.Minute)  
}  
  
func main() {  
  
    go inc()  
    go inc()  
    time.Sleep(1 * time.Second)  
}
```
# 2 RWMutex

RWMutex时读写互斥锁。该锁可以由任意数量的读取器或单个写入起持有。RWMutex 的零值是未锁定的互斥锁。

```go
type RWMutex struct {
    w           Mutex        // 用于等待的写锁
    writerSem   uint32       // 写者等待的信号量
    readerSem   uint32       // 读者等待的信号量
    readerCount atomic.Int32 // 当前读者数量
    readerWait  atomic.Int32 // 等待的读者数量
}
```

- ​**作用**：允许多个读操作并行，但写操作互斥（读多写少场景性能更优）。
- ​**使用场景**：高并发读取、低频写入（如缓存系统）。

```go
  
var rwm sync.RWMutex  
var cache = make(map[string]string)  
  
func readinc(key string) string {  
    // 加读锁，允许多个goroutine同时获取读锁
    rwm.RLock()  
    defer rwm.RUnlock()  
    time.Sleep(1 * time.Second)  
    return cache[key]  
}  
  
func writeinc(key, value string) {  
    /* 
    用于写入。如果锁已被锁定以进行读取或写入，则 Lock 会阻塞，直到锁可用。
    获取写锁后会导致后来的读锁阻塞
    */
    rwm.Lock()  
    defer rwm.Unlock()  
    cache[key] = value  
}
```
## 2.1 RLocker方法

在 Go 语言的 `sync.RWMutex` 中，`RLocker()` 方法是一个容易被忽视但实用的工具，它允许将读写锁的 ​**读锁部分** 转换为标准的 `sync.Locker` 接口，从而适配需要互斥锁的 API（如条件变量 `sync.Cond`）。

```go
func (rw *RWMutex) RLocker() Locker
```

- ​**返回值**：一个实现了 `Locker` 接口的对象。
    - 调用其 `Lock()` 方法等价于调用 `rw.RLock()`。
    - 调用其 `Unlock()` 方法等价于调用 `rw.RUnlock()`。
- ​**本质**：读锁的适配器，使其符合 `Locker` 接口。
# 3 WaitGroup

`sync.WaitGroup` 是 Go 标准库中用于 ​**协调多个 goroutine 并发执行** 的核心工具，特别适用于需要等待一组任务全部完成的场景。

```go

type WaitGroup struct {
    noCopy noCopy          // 防止值复制的标记
    state  atomic.Uint64   // 高32位为计数器，低32位为等待者数量
    sema   uint32          // 信号量（用于阻塞/唤醒 goroutine）
}

```

- ​**作用**：等待一组 goroutine 完成。
- ​**使用场景**：主 goroutine 需要等待多个子任务完成。

```go
  
func main() {  
    w := sync.WaitGroup{}  
    // 增加或减少等待的 goroutine 数量（`delta` 可正可负）。
    // 如果计数器变为负数，引发Add panic
    w.Add(1)  
    go func() {  
       // 标记一个子任务完成（等价于 `Add(-1)`）。
       defer w.Done()  
       fmt.Println("down")  
    }()  
    // 阻塞当前 goroutine，直到所有子任务完成（计数器归零）。
    w.Wait()  
}
```
# 4 Once

`Once` 只执行一次。

```go
type Once struct {  
    _ noCopy  
  
    // done indicates whether the action has been performed.    // It is first in the struct because it is used in the hot path.    // The hot path is inlined at every call site.    // Placing done first allows more compact instructions on some architectures (amd64/386),    // and fewer instructions (to calculate offset) on other architectures.    
    done atomic.Uint32  
    m    Mutex  
}
```

**Do方法流程**
1. ​**原子检查 `done`**：若为 `1`，直接返回。
2. ​**加锁**：获取互斥锁。
3. ​**二次检查 `done`**：防止其他 goroutine 已执行。
4. ​**执行函数 `f`**。
5. ​**原子写 `done`**：标记为 `1`。
6. ​**释放锁**。

- ​**作用**：确保某个操作只执行一次（如初始化配置）。
- ​**使用场景**：单例模式、延迟初始化。
## 4.1 Do(f func())

- **作用**：确保 `f` 函数在整个程序生命周期内 ​**仅执行一次**​（即使被多个 goroutine 并发调用）。
- ​**底层机制**：
    1. ​**原子标志位**：通过 `done` 标记（`uint32`）记录是否已执行。
    2. ​**互斥锁（Mutex）​**：首次调用时加锁，防止并发重复执行。
    3. ​**双重检查（Double-Check）​**：先原子读标志位，再通过锁确保原子性。
```go
var (
    once sync.Once
    config map[string]string
)

func loadConfig() {
    once.Do(func() {
        config = readConfigFile() // 只会执行一次
    })
}

```
# 5 Pool

`sync.Pool` 是 Go 标准库中用于 ​**临时对象缓存和重用** 的工具，旨在减少高频内存分配的开销（如网络请求、序列化等场景）。

```go
type Pool struct {
    noCopy    noCopy           // 禁止值拷贝的标记（静态分析检测）
    local     unsafe.Pointer  // 指向 [P]poolLocal 数组（每个 P 的本地池）
    localSize uintptr         // 本地池数组的大小（即 P 的数量）
    victim    unsafe.Pointer  // 上一轮 GC 保留的旧池（分代回收）
    victimSize uintptr        // 旧池大小
    New       func() any      // 对象创建函数（池为空时调用）
}
```

| 方法/字段                 | 作用                              |
| --------------------- | ------------------------------- |
| ​**`New func() any`** | 当池中无可用对象时，调用此函数创建新对象（需用户定义）。    |
| ​**`Get() any`**      | 从池中获取一个对象。若池为空，则调用 `New` 生成新对象。 |
| ​**`Put(x any)`**     | 将对象放回池中，供后续重用。                  |


- ​**作用**：缓存临时对象，减少内存分配开销（如频繁创建的缓冲区）。
- ​**使用场景**：高频率创建/销毁对象的场景（如 HTTP 请求解析）。

```go
var bufferPool = sync.Pool{
    New: func() any { return new(bytes.Buffer) },
}

func GetBuffer() *bytes.Buffer {
    return bufferPool.Get().(*bytes.Buffer)
}

func PutBuffer(b *bytes.Buffer) {
    b.Reset()
    bufferPool.Put(b)
}
```

- ​**注意事项**：
    - 对象放回池前需重置状态。
    - 池中对象可能被随时回收（不可依赖对象存活时间）。
    - 池化的对象不会被 GC 回收，减少垃圾回收频率。
    - 若对象占用内存较大，长期驻留池中可能导致内存浪费。
    - 池不保证 `Get()` 返回的对象状态，需用户自行重置。
    - `Get/Put` 可被多个 goroutine 并发调用。
    - 仅缓存无状态或可重置的对象（如 `bytes.Buffer`、`sync.Pool` 自身）。
# 6 Cond

- ​**作用**：让 goroutine 在满足特定条件时被唤醒。
- ​**使用场景**：生产者-消费者模型、事件等待。

| 方法名                | 作用                                                | 使用场景                                 |
| ------------------ | ------------------------------------------------- | ------------------------------------ |
| ​**`Wait()`**      | 释放锁并阻塞当前 goroutine，直到被 `Signal` 或 `Broadcast` 唤醒。 | 在条件不满足时挂起 goroutine，等待其他协程修改状态后唤醒。   |
| ​**`Signal()`**    | 唤醒 ​**一个** 等待的 goroutine（随机选择）。                   | 当共享状态改变，且只需唤醒单个协程处理时（如单任务通知）。        |
| ​**`Broadcast()`** | 唤醒 ​**所有** 等待的 goroutine。                         | 当共享状态改变，且所有等待协程都需要响应时（如全局配置更新、资源释放）。 |
```go
var (
    cond  = sync.NewCond(&sync.Mutex{})
    queue []int
)

// 生产者
go func() {
    cond.L.Lock()
    defer cond.L.Unlock()
    queue = append(queue, 1)
    cond.Signal() // 唤醒一个消费者
}()

// 消费者
go func() {
    cond.L.Lock()
    defer cond.L.Unlock()
    for len(queue) == 0 {
        cond.Wait() // 队列空时等待
    }
    item := queue[0]
    queue = queue[1:]
}()
```
# 7 Map

`sync.Map` 是 Go 标准库中提供的 ​**并发安全映射**，专为 ​**读多写少** 的场景优化，设计通过 ​**读写分离** 和 ​**无锁读路径** 显著提升性能，适用于高并发且键值对相对稳定的情况。

```go
type Map struct {
    _     noCopy          // 禁止值拷贝的标记（静态分析检测）
    mu    Mutex           // 互斥锁，保护写操作和 dirty 字段
    read  atomic.Pointer[readOnly] // 原子指针，指向只读数据
    dirty map[any]*entry  // 需加锁访问的可写数据
    misses int            // read 未命中计数，触发 dirty 提升
}

type readOnly struct {
    m       map[any]*entry
    amended bool // 标记 dirty 是否包含 read 中不存在的键
}

type entry struct {
    p atomic.Pointer[any] // 存储值的指针（支持原子操作）
}
```

- ​**作用**：线程安全的 `map`，适用于读多写少的并发场景。
- ​**使用场景**：高频读取、低频写入的键值存储。

| 方法名                                                          | 作用                              | 使用场景                   |
| ------------------------------------------------------------ | ------------------------------- | ---------------------- |
| ​**`Store(key, value any)`**                                 | 存储键值对（若键已存在则覆盖）。                | 插入或更新数据（如缓存更新）。        |
| ​**`Load(key any) (value any, ok bool)`**                    | 读取键对应的值。                        | 高频读取操作（如缓存查询）。         |
| ​**`Delete(key any)`**                                       | 删除指定键的键值对。                      | 清理不再需要的数据。             |
| ​**`LoadOrStore(key, value any) (actual any, loaded bool)`** | 若键存在则返回原值，否则存储并返回给定值。           | 初始化或原子性插入（如单例初始化）。     |
| ​**`LoadAndDelete(key any) (value any, loaded bool)`**       | 删除键并返回其原值（若存在）。                 | 原子性删除并获取数据（如任务队列取走任务）。 |
| ​**`Range(f func(key, value any) bool)`**                    | 遍历所有键值对，若 `f` 返回 `false` 则停止遍历。 | 批量处理数据（如缓存全量导出）。<br>   |
| **func (m *Map) Clear()**                                    | Clear 将删除所有条目，从而生成空 Map。        | 全量删除数据                 |
- **读多写少**：`sync.Map` 在读远多于写的场景下性能优异（无锁读路径），但 ​**频繁写入性能不如分片锁的普通 Map**。
- ​**适用阈值**：当普通 Map + `sync.RWMutex` 的锁竞争成为瓶颈时（如 `GOMAXPROCS > 4`），考虑使用 `sync.Map`。
- ​**需手动类型断言**：`Load` 返回 `any`，直接使用可能触发 `panic`。

- 原生Map VS sync.Map

|​**对比维度**|​**原生 `map`**|​**`sync.Map`**|
|---|---|---|
|​**并发安全性**|非并发安全，需手动加锁（如 `sync.Mutex`/`RWMutex`）|内部实现并发安全，无需额外锁|
|​**读性能**|高（无锁时），但有锁时性能下降（`RWMutex`）|极高（无锁读路径，适合读多写少）|
|​**写性能**|高（无锁时），但有锁时性能下降（`Mutex`）|较低（需加锁操作 `dirty`，适合低频写入）|
|​**内存占用**|低（单 `map` 结构）|较高（维护 `read` 和 `dirty` 双 `map`）|
|​**适用场景**|读写均衡、需复杂操作（如遍历、计数）|读多写少、键相对稳定（如缓存、全局配置）|
|​**键值删除**|立即释放内存|延迟删除（标记为 `expunged`，GC 后回收）|
|​**功能支持**|完整（`len()`、`range`、`delete` 等）|有限（仅基础方法：`Store`、`Load`、`Delete`、`Range`）|
|​**类型安全**|是（泛型支持）|否（需手动类型断言，`any` 类型）|
|​**锁粒度**|粗粒度（整个 `map` 加锁）|细粒度（`read` 无锁，`dirty` 加锁）|
|​**实现复杂度**|简单（直接操作）|复杂（读写分离、`dirty` 提升机制）|
|​**典型使用场景**|实时数据更新、计数器、高频写入|配置缓存、服务发现、只读为主的映射|