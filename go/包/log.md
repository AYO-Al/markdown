# 1 基础

`log`是 Go 标准库提供的，不需要另外安装。可直接使用：

```go
package main  
  
import "log"  
  
func main() {  
    log.Printf("Printf")  
    log.Println("Println")  
    log.Print("Print")  
}
```
`log`默认输出到标准错误（`stderr`），每条日志前会自动加上日期和时间。如果日志不是以换行符结尾的，那么`log`会自动加上换行符。即每条日志会在新行中输出。

`log`提供了三组函数：

- `Print/Printf/Println`：正常输出日志；
- `Panic/Panicf/Panicln`：输出日志后，以拼装好的字符串为参数调用`panic`；
- `Fatal/Fatalf/Fatalln`：输出日志后，调用`os.Exit(1)`退出程序。
# 2 定制

在log库中提供了这么一组常量。

```go
const (
	Ldate         = 1 << iota     // the date in the local time zone: 2009/01/23
	Ltime                         // the time in the local time zone: 01:23:23
	Lmicroseconds                 // microsecond resolution: 01:23:23.123123.  assumes Ltime.
	Llongfile                     // full file name and line number: /a/b/c/d.go:23
	Lshortfile                     // final file name element and line number: d.go:23. overrides Llongfile
	LUTC                          // if Ldate or Ltime is set, use UTC rather than the local time zone
	Lmsgprefix                    // move the "prefix" from the beginning of the line to before the message
	LstdFlags     = Ldate| Ltime // initial values for the standard logger
)
```

可以在标准logger上添加前缀和对应标签。

```go
package main  
  
import "log"  
  
func main() {  
    log.SetPrefix("logger:  ")  // 设置前缀
    log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)  // 设置输出选项
    log.Println(log.Flags())   // 获取输出选项
    log.Println(log.Prefix())  // 获取输出前缀
    log.Printf("Printf")  
    log.Println("Println")  
    log.Fatalf("yes")  
}

/*
logger:  2024/11/27 19:57:44 log.go:8: 19
logger:  2024/11/27 19:57:44 log.go:9: logger:  
logger:  2024/11/27 19:57:44 log.go:10: Printf
logger:  2024/11/27 19:57:44 log.go:11: Println
logger:  2024/11/27 19:57:44 log.go:12: yes
*/
```

前面一直使用的是`log`包提供的标准Logger对象，我们也可以自己新建一个。

```go
package main

import (
	"bytes"
	"io"
	"log"
	"os"
)

func main() {
	buf1 := &bytes.Buffer{}
	buf2 := os.Stdout
	buf3, _ := os.OpenFile("test.log", os.O_CREATE|os.O_RDWR, os.ModePerm)

	// func New(out io.Writer, prefix string, flag int) *Logger
	logger := log.New(io.MultiWriter(buf1, buf2, buf3), "NewLogger\t", log.Lmicroseconds|log.Lshortfile)

	logger.Fatalf(" NewLogger Test")
}

// NewLogger       20:14:43.363719 log.go:18:  NewLogger Test
```
# 3 实现

Log库提供的标准Loggeer对象也是使用New方法创建出来的。

```go
var std = New(os.Stderr, "", LstdFlags)

func Fatalf(format string, v ...any) {  
    std.Output(2, fmt.Sprintf(format, v...))  
    os.Exit(1)  
}
```

Log库的核心方法是`Output`方法。

```go
func (l *Logger) output(pc uintptr, calldepth int, appendOutput func([]byte) []byte) error {  
    if l.isDiscard.Load() {  
       return nil  
    }  
  
    now := time.Now() // get this early.  
  
    // Load prefix and flag once so that their value is consistent within    // this call regardless of any concurrent changes to their value.    prefix := l.Prefix()  
    flag := l.Flags()  
  
    var file string  
    var line int  
    if flag&(Lshortfile|Llongfile) != 0 {  
       if pc == 0 {  
          var ok bool  
          _, file, line, ok = runtime.Caller(calldepth)  
          if !ok {  
             file = "???"  
             line = 0  
          }  
       } else {  
          fs := runtime.CallersFrames([]uintptr{pc})  
          f, _ := fs.Next()  
          file = f.File  
          if file == "" {  
             file = "???"  
          }  
          line = f.Line  
       }  
    }  
  
    buf := getBuffer()  
    defer putBuffer(buf)  
    formatHeader(buf, now, prefix, flag, file, line)  
    *buf = appendOutput(*buf)  
    if len(*buf) == 0 || (*buf)[len(*buf)-1] != '\n' {  
       *buf = append(*buf, '\n')  
    }  
  
    l.outMu.Lock()  
    defer l.outMu.Unlock()  
    _, err := l.out.Write(*buf)  
    return err  
}
```

