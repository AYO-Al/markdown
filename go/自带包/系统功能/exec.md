# exec

## 1 os/exec包

| ​**​特性​**​                                                                                                                                          | ​**​`os/exec` 包​**​ | ​**​系统 Shell (如 Bash)​**​ |
| --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------------------- |
| ​**​命令解析​**​                                                                                                                                        | 直接执行二进制文件，无参数扩展     | 自动展开通配符、变量替换、管道等          |
| ​**​安全性​**​                                                                                                                                         | 无隐式解析，避免注入风险        | 需谨慎处理用户输入，易受注入攻击          |
| ​**​资源消耗​**​                                                                                                                                        | 轻量级，无额外 Shell 进程开销  | 需要启动 Shell 进程，增加开销        |
| ​**​跨平台一致性​**​                                                                                                                                      | 行为一致，适合跨平台代码        | 依赖宿主 Shell，行为可能不一致        |
| `os/exec`包不是直接调用系统shell，也不拓展任何glob模式或处理通常由shell完成的其他扩展、管道或重定向。要扩展glob模式请直接调用 shell，注意转义任何危险的输入，或使用 path/[filepath](../路径处理/filepath.md) 包的 Glob 函数。 |                     |                           |

## 2 LookPath

`LookPath` 函数用于在系统的 ​**​PATH 环境变量​**​中查找可执行文件的绝对路径。默认不会带

* ​**​功能​**​：在系统的 `PATH` 环境变量中搜索指定命令的绝对路径。
* ​**​用途​**​：
  * 验证命令是否存在。
  * 获取可执行文件的完整路径（避免直接依赖 `PATH` 顺序）。
* ​**​底层行为​**​：
  * ​**​Windows​**​：自动尝试添加 `.exe`、`.bat` 等扩展名。
  * ​**​Unix/Linux​**​：直接匹配文件名（需文件有可执行权限）。

```go
func LookPath(file string) (string, error)
```

`exec.Command`内部自动调用LookPath解析命令，但命令不存在的错误将在 `cmd.Run` 才抛出。

## 3 Cmd类型

Cmd 表示正在准备或运行的外部命令。

```go
// Cmd 表示一个正在准备或执行的外部命令。
//
// 使用 exec.Command 或 exec.CommandContext 创建该结构体。
// 字段的线程安全性：一个 Cmd 实例在调用 Start、Run 或 Output 后，不得被并发修改。
type Cmd struct {
	// Path 指定要执行的可执行文件的路径。
	// 这是唯一必须设置为非零值的字段。
	// - 若为相对路径，则基于 Dir 字段解析。
	// - 若 Args 为空，默认使用 Path 作为命令名（Args[0]）。
	Path string

	// Args 保存命令行参数，包括命令名 Args[0]。
	// 若为空或 nil，默认使用 [Path] 作为 Args。
	// 示例：[]string{"git", "commit", "-m", "message"}
	Args []string

	// Env 指定进程的环境变量，格式为 "key=value"。
	// - 若为 nil，继承当前进程的环境变量。
	// - 重复的键（Key）将保留最后一个值。
	// - Windows 特殊处理：若未设置 SYSTEMROOT，自动添加。
	Env []string

	// Dir 设置命令的工作目录。
	// - 若为空，使用调用进程的当前目录。
	// - Unix 系统中，同时设置子进程的 PWD 环境变量。
	Dir string

	// Stdin 指定进程的标准输入。
	// - 若为 nil，从空设备（os.DevNull）读取。
	// - 若为 *os.File，直接连接文件；否则通过管道实时读取。
	Stdin io.Reader

	// Stdout 和 Stderr 指定进程的标准输出和错误。
	// - 若为 nil，输出到空设备（os.DevNull）。
	// - 若为同一 Writer 且可比较，保证单 goroutine 写入。
	Stdout io.Writer
	Stderr io.Writer

	// ExtraFiles 指定子进程继承的额外打开文件（不包括 stdin/stdout/stderr）。
	// - 文件描述符规则：索引 i 对应 fd 3+i。
	// - Windows 不支持此字段。
	ExtraFiles []*os.File

	// SysProcAttr 设置操作系统特定的进程属性。
	// 示例：
	// - Unix：设置 Chroot 或进程组。
	// - Windows：隐藏窗口标志 CREATE_NO_WINDOW。
	SysProcAttr *syscall.SysProcAttr

	// Process 表示已启动的底层进程对象。
	// 调用 Start 后可用，用于手动终止进程（如 Process.Kill()）。
	Process *os.Process

	// ProcessState 包含进程退出后的状态信息。
	// 调用 Wait 或 Run 后可用，获取退出码和资源使用情况。
	ProcessState *os.ProcessState

	// Err 记录 LookPath 查找 Path 时的错误（如命令未找到）。
	Err error

	// Cancel 是 CommandContext 创建的上下文取消回调函数。
	// - 默认行为：调用 Process.Kill() 终止进程。
	// - 可自定义：如关闭管道或发送网络关闭信号。
	// 注意：若 Start 失败，Cancel 不会被调用。
	Cancel func() error

	// WaitDelay 设置等待子进程退出和 I/O 管道关闭的超时时间。
	// - 若超时：强制终止进程并关闭管道。
	// - 若为 0（默认），等待管道自然关闭（可能被僵尸进程阻塞）。
	WaitDelay time.Duration
}
```

1. ​**​字段分类​**​
   * ​**​必须字段​**​：`Path` 是唯一必须设置的字段。
   * ​**​输入/输出控制​**​：`Stdin`、`Stdout`、`Stderr` 管理进程的 I/O 流。
   * ​**​高级控制​**​：`SysProcAttr` 和 `ExtraFiles` 处理平台相关逻辑。
   * ​**​生命周期管理​**​：`Process` 和 `ProcessState` 提供进程运行时和退出后的信息。
2. ​**​线程安全​**​
   * ​**​不可变性​**​：调用 `Start()`、`Run()` 或 `Output()` 后，禁止并发修改字段。
3. ​**​跨平台行为​**​
   * ​**​路径解析​**​：`Path` 在 Windows 中自动尝试 `.exe`、`.bat` 等扩展名。
   * ​**​环境变量​**​：Windows 自动处理 `SYSTEMROOT`，Unix 严格检查文件权限。
4. ​**​错误处理​**​
   * ​**​提前验证​**​：通过 `LookPath` 检查 `Path` 有效性（见 `Err` 字段）。
   * ​**​超时控制​**​：结合 `CommandContext` 和 `WaitDelay` 防止僵尸进程。

### 3.1 **`Command(name string, arg ...string) *Cmd`​**

* **作用​**​：创建表示外部命令的 `Cmd` 对象。
* **​关键点​**​：
  * `name` 为可执行文件路径或系统 `PATH` 中的命令名。
  * `arg` 为参数列表（需拆分，避免直接传递字符串拼接的命令）。
  * 它仅在返回的结构中设置 Path 和 Args。
  * 如果 name 不包含路径分隔符，则 Command 会尽可能使用 LookPath将 name 解析为完整路径。否则，它将直接使用 name 作为 Path。

```go
cmd := exec.Command("ls", "-l", "/tmp") // 正确：参数拆分
// 错误示例：exec.Command("sh", "-c", "ls -l /tmp") （可能引发注入风险）
```

### 3.2 CommandContext(ctx context.Context, name string, arg ...string) \*Cmd

* **作用**：跟Command类似，但包含上下文。
* **关键点**：
  * 提供的上下文用于中断进程
  * CommandContext 将命令的 Cancel 函数设置为在其 Process 上调用 Kill 方法，并未设置其 WaitDelay。调用方可以通过在启动命令之前修改这些字段来更改取消行为。

```go
package main

import (
	"context"
	"os/exec"
	"time"
)

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()

	if err := exec.CommandContext(ctx, "sleep", "5").Run(); err != nil {
		// This will fail after 100 milliseconds. The 5 second sleep
		// will be interrupted.
	}
}
```

### 3.3 **`(c)Run() error`​**

**作用​**​：启动命令并等待其完成（同步执行）。\
​**​返回值​**​：命令退出状态错误（若命令返回非零状态码，返回 `ExitError`）。

* 如果命令已启动但未成功完成，则错误为 \*ExitError 类型。对于其他情况，可能会返回其他错误类型。

```go
​err := cmd.Run()
if exitErr, ok := err.(*exec.ExitError); ok {
    fmt.Printf("命令退出码: %d\n", exitErr.ExitCode())
}
```

### 3.4 **`(c)Start() error`​**

**作用​**​：异步启动命令（不等待完成）。\
​**​典型用法​**​：配合 `Wait()` 实现异步执行。

```go
err := cmd.Start()
if err != nil {
    log.Fatal(err)
}
// 执行其他操作...
err = cmd.Wait() // 等待命令完成
```

### 3.5 **(c)`Wait() error`​**

**作用​**​：等待由 `Start()` 启动的命令完成。\
​**​注意​**​：必须在 `Start()` 后调用，否则返回错误。

### 3.6 **`(c)Output() ([]byte, error)`**

**作用​**​：执行命令并捕获其标准输出。\
​**​等价于​**​：`Run()` + 捕获 `Stdout`。

```go
output, err := exec.Command("date").Output()
if err != nil {
    log.Fatal(err)
}
fmt.Println(string(output)) // 输出当前时间
```

### 3.7 **`(c)CombinedOutput() ([]byte, error)`​**

**作用​**​：执行命令并捕获标准输出 + 标准错误的合并结果。\
​**​适用场景​**​：需要同时获取正常和错误输出。

```go
output, err := exec.Command("ls", "/nonexistent").CombinedOutput()
if err != nil {
    fmt.Printf("错误输出:\n%s", output) // 输出 "ls: /nonexistent: No such file or directory"
}
```

### 3.8 **`(c)StdinPipe() (io.WriteCloser, error)`​**

**作用​**​：获取命令的标准输入管道，用于向命令传递数据。\
​**​流程​**​：

1. 调用 `StdinPipe()` 获取写入器。
2. 在 `Start()` 后向管道写入数据。
3. 关闭管道以通知命令输入结束。

```go
cmd := exec.Command("grep", "error")
stdin, _ := cmd.StdinPipe() // io.WriteCloser, error
stdout, _ := cmd.StdoutPipe()  // io.ReadCloser, error
stderr,_ := cmd.StderrPipe() // io.ReadCloser, error

cmd.Start()
stdin.Write([]byte("info: ok\nerror: found\n"))
stdin.Close() // 必须关闭

scanner := bufio.NewScanner(stdout)
for scanner.Scan() {
    fmt.Println(scanner.Text()) // 输出 "error: found"
}
cmd.Wait()
```

```go
package main

import (
    "bufio"
    "fmt"
    "os"
    "os/exec"
    "strings"
)

func main() {
    // 步骤1: 执行 ps -ef
    psCmd := exec.Command("ps", "-ef")
    psOutput, err := psCmd.StdoutPipe()
    if err != nil {
        panic(err)
    }
    if err := psCmd.Start(); err != nil {
        panic(err)
    }

    // 步骤2: 过滤包含 "prome" 的行
    grepCmd := exec.Command("grep", "prome")
    grepCmd.Stdin = psOutput
    grepOutput, err := grepCmd.StdoutPipe()
    if err != nil {
        panic(err)
    }
    if err := grepCmd.Start(); err != nil {
        panic(err)
    }

    // 步骤3: 排除包含 "grep" 的行
    grepVCmd := exec.Command("grep", "-v", "grep")
    grepVCmd.Stdin = grepOutput
    vOutput, err := grepVCmd.StdoutPipe()
    if err != nil {
        panic(err)
    }
    if err := grepVCmd.Start(); err != nil {
        panic(err)
    }

    // 步骤4: 提取第二列（PID）
    awkCmd := exec.Command("awk", "{print $2}")
    awkCmd.Stdin = vOutput
    awkOutput, err := awkCmd.StdoutPipe()
    if err != nil {
        panic(err)
    }
    if err := awkCmd.Start(); err != nil {
        panic(err)
    }

    // 步骤5: 读取 PID 并传递给 kill -9
    scanner := bufio.NewScanner(awkOutput)
    var pids []string
    for scanner.Scan() {
        pids = append(pids, scanner.Text())
    }

    if len(pids) == 0 {
        fmt.Println("未找到匹配的进程")
        return
    }

    // 执行 kill -9
    killCmd := exec.Command("kill", "-9", strings.Join(pids, " "))
    killCmd.Stdout = os.Stdout
    killCmd.Stderr = os.Stderr
    if err := killCmd.Run(); err != nil {
        fmt.Printf("终止进程失败: %v\n", err)
    }

    // 等待所有命令完成
    psCmd.Wait()
    grepCmd.Wait()
    grepVCmd.Wait()
    awkCmd.Wait()
}
```
