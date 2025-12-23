关于 `Slice` 源码在 `runtime/slice.go` 文件中

```go
type slice struct {
	array unsafe.Pointer
	len   int
	cap   int
}
```

本质上一个 `Slice` 是一个结构体，包含一个 `len` / `cap` / `array`。

> 扩容

在1.18之前，`Slice` 扩容的策略为：

- 如果原Slice容量小于1024，则扩容为之前的两倍
- 如果原Slice容量大于1024，则扩容为之前的1.25倍

由此可以看出Go对Slice的性能和空间使用率的思考：

- 当容量较小时，使用较大倍率进行扩容，从而避免频繁扩容带来的性能损耗，主要是内存分配和数据拷贝
- 当容量比较大时，使用较小倍率进行扩容，避免空间浪费

在1.18之后，`Slice` 的扩容策略为：

- 如果新扩容的长度大于旧容量的两倍，则直接扩容到需要的长度
- 以256为边界
	- 如果旧容量小于256则直接扩容两倍
	- 如果大于256，则每次在旧容量的基础上+newcap+3\*256 /4(约1.25倍)，直到大于需要的长度

```go
func nextslicecap(newLen, oldCap int) int {
	newcap := oldCap
	doublecap := newcap + newcap
	if newLen > doublecap {
		return newLen
	}

	const threshold = 256
	if oldCap < threshold {
		return doublecap
	}
	for {
		// Transition from growing 2x for small slices
		// to growing 1.25x for large slices. This formula
		// gives a smooth-ish transition between the two.
		newcap += (newcap + 3*threshold) >> 2

		// We need to check `newcap >= newLen` and whether `newcap` overflowed.
		// newLen is guaranteed to be larger than zero, hence
		// when newcap overflows then `uint(newcap) > uint(newLen)`.
		// This allows to check for both with the same comparison.
		if uint(newcap) >= uint(newLen) {
			break
		}
	}

	// Set newcap to the requested cap when
	// the newcap calculation overflowed.
	if newcap <= 0 {
		return newLen
	}
	return newcap
}
```

> 扩容详解

以上只是初步获取扩容后的容量的方法，实际上在获取了对于的容量后，还需要做一些其他操作来最终决定扩容后的容量。

实际上 `nextslicecap` 只是计算扩容后的容量的方法，实际上完成扩容这个动作的是 `growslice` 函数。

在计算出新容量后，还会进行内存对齐操作。

根据元素大小进行不同的优化：

- **元素大小为 1**: 直接计算内存
	- `newcap = int(capmem)`
- **元素大小为指针大小**: 针对指针进行优化
	- newcap = int(capmem / goarch.PtrSize)
- **元素大小为 2 的幂次**: 使用位移运算优化
	- newcap = int(capmem >> shift)
- **其他情况**: 使用乘法计算
	- newcap = int(capmem / et.Size_)

内存对齐能够：

- 利用内存分配器的 size class，减少内存碎片
- 提高 CPU 访问效率
- 可能获得比预期更大的容量，减少后续扩容次数

判断步骤：

- 先判断是否是小对象，以32KB为分界线
	- 对于 ≤ 1024 字节的大小：使用 `SizeToSizeClass8` 表，粒度为 8 字节
	- 对于 > 1024 字节的大小：使用 `SizeToSizeClass128` 表，粒度为 128 字节
	- 对于大分配，该函数简单地向上舍入到下一个页面边界（8192 字节）
- 在计算最终内存大小时先使用 `divRoundUp` 函数进行向上取整

```go
func divRoundUp(n, a uintptr) uintptr {
	// a is generally a power of two. This will get inlined and
	// the compiler will optimize the division.
	return (n + a - 1) / a
}
```

- 然后使用 `gc.SizeClassToSize[gc.SizeToSizeClass8[divRoundUp(reqSize, gc.SmallSizeDiv)]]` 获取实际分配大小

采用不同粒度的双表方法是一种平衡内存效率和查找表大小的优化。较小的分配（≤1024 字节）非常普遍，并受益于更细的 8 字节粒度以减少内部碎片。较大的分配可以容忍 128 字节粒度，同时保持查找表大小可控。两个表的总大小为 129 + 249 = 378 字节，足够小以适应缓存，同时覆盖整个小对象范围（最高 32KB）。


> 示例

对于 100 字节的分配：

1. 在潜在的 malloc 头部调整后，计算 `divRoundUp(100, 8) = 13``divRoundUp(100, 8) = 13`
2. 查询 `SizeToSizeClass8[13]` 以获取大小类别
3. 查询 `SizeClassToSize[sizeClass]` 以获取实际分配大小
4. 减去之前添加的任何 malloc 头部开销

> 为什么使用三步查找法

Go 的内存分配器使用三步间接过程，主要目的是在保持高性能的同时大幅减少查找表的大小。选择这种设计的原因如下：

Go 有 67 个大小类别，跨度高达 32KB。直接查找表需要 32,768 个条目（每个字节一个）。三步法使用：

- **SizeToSizeClass8**:  129 个条目（用于 0-1024 字节，以 8 字节为增量）
- **SizeToSizeClass128**: 249 条目（用于 1024-32768 字节，以 128 字节为增量）
- **SizeClassToSize**: 68 条目

总计：约 446 条目与 32,768 条直接查找相比——表大小减少了 98.6%。

性能优异：所有三步都是简单的数组索引查找
