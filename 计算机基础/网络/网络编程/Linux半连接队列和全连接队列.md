**以下结论皆处于Linux 2.6.32版本内核**
# 定义

- 半连接队列：存放SYN请求的队列，又叫做SYN队列
- 全连接队列：存放接收到客户端ACK请求的队列，又叫ACK队列

服务器在接收到客户端发起的SYN请求后，内核会将该连接存储到半连接队列中，并向客户端响应SYN+ACK。随后，客户端会返回ACK。服务器在接收到第三次握手的ACK后，内核会将连接从半连接队列中移除，然后创建一个新的完整连接，并将其添加到accept队列中，等待进程调用accept函数来取出连接。

不管是全连接队列还是半连接队列，都有最大长度限制，一但超出，就会丢弃连接或发挥RST包。

# 如何查看全连接队列大小

- 查看全连接队列大小
    - LISTEN状态：ss -tnl  send-Q列即是全连接队列最大长度，recv-Q是当前全连接队列大小
    - 非LISTEN：ss -nt send-Q列已发送但未收到确认的字节数，recv-Q是已接收但未被程序读取的字节数

- 如何查看全连接队列溢出情况
    - grep "TcpExt" /proc/net/netstat 
    - 查看对应的ListenOverflows和ListenDrops值
    - ListenDrops：因溢出导致的连接丢弃总数
    - ListenOverflows：全连接队列溢出次数
    - 也可以使用使用netstat -s|grep overflowed 查看，但如果没有发生溢出行为是不会有相关信息的

- 全连接队列满了会怎么样？行为，修改，情况选择。
    - 全连接满了之后，会丢弃ACK请求
    - 满了之后的行为由 cat /proc/sys/net/ipv4/tcp_abort_on_overflow 控制
        - 0:丢弃第三次握手的ACK报文。客户端连接状态可能显示为ESTABLISHED，但发送数据后​​长时间无响应​​，最终超时。	
        - 1:直接回复RST报文复位连接。连接尝试​​立刻被拒绝​​，通常会收到“Connection reset”或类似“connection reset by peer”错误。	
    - 情况选择：
        - 如果是突发大量流量的情况：选择0，因为可能是短时间内的全连接队列满，等流量下去之后，客户端发送ACK报文就会被接受，从而完成连接
        - 如果能确认是大量时间队列满的情况下：设置为1.让客户端能收到消息中断连接，避免重复重试
    - 内核允许队列长度短暂超过`backlog`值（通常可超过1-2个连接）
    - 这样设计是为了​**​避免在高速连接建立时出现"队列锁死"​**​  
(当新连接进入时恰好被`accept()`取走一个连接，可避免完全拒绝服务)

- 全连接队列是每个应用程序独有还是操作系统共用？
    - 每个监听套接字独有
# 如何修改全连接队列大小

- min(somaxconn,backlog)
    - somaxconn参数在/proc/sys/net/core/somaxconn文件中设置
    - backlog则根据工具的不同设置方式也不同
        - nginx：server { listen 8080 default backlog=5000 }。默认情况下，`backlog` 在 FreeBSD、DragonFly BSD 和 macOS 上设置为 -1，在其他平台上设置为 511。
        - 编程语言一般在listen函数中进行设置


取最小值体现了内核“双重保险”的设计哲学：既要尊重应用的需求，又要服从系统的总体管控。

| **参数​**​            | 作用层级          | 配置方式                        | 默认值（典型）         | 设计目标          |
| ------------------- | ------------- | --------------------------- | --------------- | ------------- |
| ​**​`backlog`​**​   | ​**​应用层​**​   | 程序代码中 `listen(fd, backlog)` | 语言相关（如Python=5） | 声明应用能处理的并发预备量 |
| ​**​`somaxconn`​**​ | ​**​操作系统层​**​ | `sysctl net.core.somaxconn` | 128~4096        | 防止单个应用耗尽系统资源  |
# 如何查看半连接队列大小

- 查看半连接队列大小
    - 并没有具体的方法可以查看
    - 近似认为当前半连接队列中连接数：netstat -antp |grep SYN_RECV|grep pid/pro_name|wc -l

- 查看溢出情况
    - netstat -s | grep -i 'SYNs to LISTEN sockets dropped'
    -  grep "TcpExt" /proc/net/netstat 
        - 查看对应的ListenOverflows和ListenDrops值
        - ListenDrops：因溢出导致的连接丢弃总数
        - ListenOverflows：全连接队列溢出次数
        - 用总数减去全连接

- 半连接队列满了会怎么样？行为，修改，情况选择
    - 满了会丢弃客户端发送的SYN请求
    - 丢弃
        - 如果半连接队列已满，并且没有启用tcp_syncookies，则会丢弃；
        - 如果全连接队列已满，且没有超过1个重传SYN+ACK包的连接请求，则会丢弃；
        - 如果没有启用tcp_syncookies，并且max_syn_backlog减去当前半连接队列长度小于(max_syn_backlog>>2位)，则会丢弃；

- tcp_syncookies设置作用
    - 当半连接队列满的时候，启动syncookies功能可以跳过半连接队列直接连接成功，避免有用SYN攻击把半连接队列打满
    - 设置/proc/sys/net/ipv4/tcp_syncookies
        - 0:不开启
        - 1:当半连接队列满的时候开启
        - 2:无条件开启
# 修改半连接队列大小

理论半连接队列最大值：
- 当 max_syn_backlog > min(somaxconn, backlog) 时， 半连接队列最大值 max_qlen_log = min(somaxconn, backlog) * 2; 
- 当 max_syn_backlog < min(somaxconn, backlog) 时， 半连接队列最大值 max_qlen_log = max_syn_backlog * 2;

- tcp_max_syn_backlog:   /proc/sys/net/ipv4/tcp_max_syn_backlog设置
- 修改半连接队列大小要连同somaxconn，backlog参数一起修改

- 如果「当前半连接队列」没超过「理论半连接队列最大值」，但是超过 max_syn_backlog - (max_syn_backlog >> 2)，那么处于 SYN_RECV 状态的最大个数就是 max_syn_backlog - (max_syn_backlog >> 2)； 
- 如果「当前半连接队列」超过「理论半连接队列最大值」，那么处于 SYN_RECV 状态的最大个数就是「理论半连接队列最大值」；

# 半连接队列大小设置哲学

首先是安全防御的考量，取最小值是为了建立“双保险”机制。比如当攻击者用SYN Flood冲击半连接队列时，如果只依赖 max_syn_backlog 这个单一阈值，一旦被突破就会直接冲击更脆弱的全连接队列。而双重限制就像两道防线，尤其在全连接队列较小时能提前掐断攻击流量。

其次是资源匹配原则。半连接本质是为全连接服务的，所以其容量不该孤立设置。想象全连接队列只有100的容量，即使把 max_syn_backlog 设为10000，允许1万个半连接也没有意义——因为最终只有100个能转化成功。这种设计强制半连接队列容量与全连接队列保持比例关系（通常是2倍），避免资源错配。

最后是历史教训的体现。早期Linux内核曾发生过半连接队列过大反而导致全连接队列被压垮的事故，现在的设计确保当全连接处理能力不足时，协议栈会通过拒绝半连接来“减速”。这类似于交通管制：当主干道堵塞时，就在匝道口限制车辆进入。
# 为什么要设计半连接和全连接队列

设计 ​**​半连接队列（SYN Queue）​**​ 和 ​**​全连接队列（Accept Queue）​**​ 是 Linux TCP 协议栈的核心机制，根本目的是为了解决 ​**​资源安全隔离​**​ 和 ​**​流量异步缓冲​**​ 两大问题。

- 资源安全隔离：将SYN队列与ACK队列分开，这样SYN Flood攻击就无法污染已建立的合法连接。并且可以启用SYN Cookie单独加固半连接。

    - **如果没有SYN队列，操作系统会为每一个SYN请求都创建完整结构体，导致操作系统资源耗尽（CPU/内存）。**

- 流量异步缓冲：把SYN和ACK队列开分，操作系统可以批量处理 SYN + ACK半连接请求。ACK队列缓冲避免请求一次性压到业务上，如果没有队列，应用 accept() 被海量请求淹没 导致 服务崩溃。
