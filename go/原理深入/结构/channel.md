/src/runtime/chan.go定义了channel的数据结构

```go
type hchan struct {
	qcount   uint           // total data in the queue
	dataqsiz uint           // size of the circular queue
	buf      unsafe.Pointer // points to an array of dataqsiz elements
	elemsize uint16
	synctest bool // true if created in a synctest bubble
	closed   uint32
	timer    *timer // timer feeding this chan
	elemtype *_type // element type
	sendx    uint   // send index
	recvx    uint   // receive index
	recvq    waitq  // list of recv waiters
	sendq    waitq  // list of send waiters

	// lock protects all fields in hchan, as well as several
	// fields in sudogs blocked on this channel.
	//
	// Do not change another G's status while holding this lock
	// (in particular, do not ready a G), as this can deadlock
	// with stack shrinking.
	lock mutex
}
```

# 1 环形队列

chan内部实现了一个环形队列作为其缓冲区，队列长度在使用make创建时指定

![[channel_time_1.png]]
# 2 等列队列

hchan中使用 `recvq` 和 `sendq` 表示当缓冲区满或没有缓冲区时，向该chan读取和发送的堵塞grouting队列。

![[channel_time_2.png]]
处在等待队列的协程会被其他协程操作管道时的操作唤醒：

- 因为读操作被堵塞的协程会被写入操作的协程唤醒
- 因为写操作被堵塞的协程会被读操作协程唤醒

一般来说 `recvq` 和 `send` 不会同时有排队情况，除非是在 一个协程中用select一边向channel中读数据一边写数据。

等待队列为一个 FIFO 的队列，会按顺序获取。且当因为读操作和写操作要被堵塞时，如果对应的 `sendq` 和 `recvq` 中有对应的协程会直接将该协程唤醒，而不进入缓冲区。

```go
func (q *waitq) enqueue(sgp *sudog) {
	sgp.next = nil
	x := q.last
	if x == nil {
		sgp.prev = nil
		q.first = sgp
		q.last = sgp
		return
	}
	sgp.prev = x
	x.next = sgp
	q.last = sgp
}

func (q *waitq) dequeue() *sudog {
	for {
		sgp := q.first
		if sgp == nil {
			return nil
		}
		y := sgp.next
		if y == nil {
			q.first = nil
			q.last = nil
		} else {
			y.prev = nil
			q.first = y
			sgp.next = nil // mark as removed (see dequeueSudoG)
		}

		// if a goroutine was put on this queue because of a
		// select, there is a small window between the goroutine
		// being woken up by a different case and it grabbing the
		// channel locks. Once it has the lock
		// it removes itself from the queue, so we won't see it after that.
		// We use a flag in the G struct to tell us when someone
		// else has won the race to signal this goroutine but the goroutine
		// hasn't removed itself from the queue yet.
		if sgp.isSelect {
			if !sgp.g.selectDone.CompareAndSwap(0, 1) {
				// We lost the race to wake this goroutine.
				continue
			}
		}

		return sgp
	}
}
```

