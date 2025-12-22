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
	- 如果大于256，则每次在旧容量的基础上+3\*256 /4(约1.25倍)，直到大于需要的长度

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
