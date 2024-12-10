[toc]



# A

## ab

Apache HTTP 服务器性能测试

```bash
"ab"指令是一个常用的命令行工具，用于进行 Apache HTTP 服务器的性能测试。它允许你模拟多个并发用户向特定URL发送请求，并计算服务器的响应时间、吞吐量等性能指标。下面是常用的"ab"指令的用法：

shell
复制
ab [选项] [URL]
常用选项和用法如下：

-n：指定总请求数。例如，-n 1000表示发送1000个请求。

-c：指定并发请求数。例如，-c 10表示同时发送10个请求。

-t：指定测试的最长时间（秒）。例如，-t 60表示测试持续60秒。

-k：启用HTTP Keep-Alive功能。默认情况下，每个请求都会打开和关闭一个连接。

-p：指定包含POST数据的文件。例如，-p data.txt表示将data.txt文件中的数据作为POST请求的主体。

-H：指定自定义的HTTP头部。例如，-H "Host: example.com"表示在请求中包含自定义的Host头部。

-g：生成可用于GNU Plot绘图的收集数据文件。

-s：设置显示详细性能报告之前的等待时间（以秒为单位）。例如，-s 5表示等待5秒后显示结果。

-e：指定包含SSL/TLS密钥和证书的文件。

示例用法：

shell
复制
ab -n 1000 -c 10 http://example.com/
此命令会向http://example.com/发送1000个请求，每次并发发送10个请求。
```



# B 

# C 

## createrepo

用于创建软件仓库和生成元数据

```bash
createrepo /root/shell_c/cloud/
```



# D 

# E 

## ethtool

用于配置和显示以太网接口的状态和参数

### 显示以太网接口eth0的配置和状态信息

```bash
ethtool eth0

-s/--change：修改接口的设置。例如：ethtool -s eth0 autoneg off。
-A/--pause：配置流控制和自动协商设置。例如：ethtool -A eth0 rx on tx off。
-C/--coalesce：配置中断协调和包合并设置。例如：ethtool -C eth0 adaptive-rx off。
-i/--driver：显示接口的驱动程序信息。例如：ethtool -i eth0。
-l/--show-tx/rx-frames：显示接口的发送和接收帧队列长度。例如：ethtool -l eth0。
-r/--show-ring：显示接口的接收和发送环缓冲区设置。例如：ethtool -r eth0。
-S/--statistics：显示接口的统计信息。例如：ethtool -S eth0。
-t/--test：运行内置的自检测试。例如：ethtool -t eth0 offline。
```



# F 

# G

# H

# I 

# J 

# K

# L 

## ldd

用于查看可执行文件或共享库所依赖的动态链接库

```bash
ldd /bin/cat

        linux-vdso.so.1 =>  (0x00007ffe3f3bd000)
        libc.so.6 => /lib64/libc.so.6 (0x00007f92af0da000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f92af4a8000)
```



# M

# N

# O 

## Openssl

 OpenSSL是一个开源的加密库，提供了一系列的加密算法，包括对称加密和非对称加密。

### 生成RSA私钥

```bash
openssl genrsa -out private.pem 2048
```

### 生成RSA公钥

```bash
openssl rsa -in private.pem -out public.pem -pubout
```

### 加密文件

```bash
openssl enc -aes-256-cbc -salt -in file.txt -out file.txt.enc
```

### 解密文件

```bash
openssl enc -aes-256-cbc -d -in file.txt.enc -out file.txt
```

### 生成签名证书

```bash
openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt
```

### 查看证书信息

```bash
openssl x509 -in server.crt -noout -text
# -noout：表示不输出证书本身，而是输出证书的详细信息
# -text：以文本形式输出
```



# P

# Q

# R 

## route

用于管理和操作网络路由表的命令行工具

### 显示路由表

```bash
route -n
```

### 添加路由

```bash
route add -net 10.0.0.0/24 gw 192.168.0.1 dev eth0
```

### 删除路由

```bash
route del -net 10.0.0.0/24
```

### 修改默认网关

```bash
route add default gw 192.168.0.1
```

![](D://i/2023/06/23/xia19r-0.png)



## Rsync

![image-20230702112651769](D://i/2023/07/02/in1497-0.png)



# S 

## SHC

一个Shell脚本编译器工具，将Shell脚本编译为二进制文件

- 编译为二进制：`shc -f script.sh`

- 编译为二进制，并重命名输出文件：`shc -f script.sh -o binary_file`



## SCP

![image-20230702112231239](D://i/2023/07/02/ikbmhs-0.png)



# T 

## tcpdump

是一个网络报文抓取工具，可以在计算机网络上捕获和分析网络数据包。它可以用于诊断和故障排除网络问题、监视网络流量以及进行安全分析

```bash
tcpdump -i ens33 -nn icmp
-i：指定需要监听的网络接口。
-n：以数字形式显示IP地址和端口号。
-s：指定捕获数据包的长度。
-w：将捕获的数据包保存为文件。
host：根据主机或IP地址过滤数据包。
port：根据端口号过滤数据包。

tcpdump -i ens33 -nn icmp and host 192.168.1.100
```



## tracepath

一个用于追踪网络路径的命令行工具，它类似于`traceroute`命令

### 追踪到主机的路径

```bash
tracepath 192.168.1.1
# 选项与traceroute一样
-n：使用IP地址而不是主机名显示路由器的信息。
-p <端口号>：指定追踪的目标端口号，默认为80。
-m <最大跳数>：设置允许的最大跳数。
-w <等待时间>：设置每个路由器的超时时间。

traceroute通常会显示每个跳跃的IP地址、主机名以及每个跳跃的延迟时间。而tracepath通常较为简洁，只显示每个跳跃的IP地址和一个数字，表示该跳跃的延迟时间。
```





# U 

## uuidgen

生成一个uuid



# V 

# W

## w

显示已经登录的用户以及他们在做什么



## watch

是一个 Linux 命令，它可以用来在固定时间间隔内重复执行任意命令，并在终端窗口中显示命令的输出

### 每 5 秒显示一次系统时间和日期

```bash
# watch -n [interval in seconds] [command]
watch -n 5 date
# -n 或 --interval：允许您指定更新输出之间的时间间隔。
# 默认间隔2s
```

### 监控系统正常运行时间并突出显示变化

```bash
# watch -d [command]
watch -d uptime
# -d 或 --differences：突出显示输出更新之间的差异。
```

### 监控系统正常运行时间并删除标题

```bash
# watch -t [command]
watch -t uptime
# -t 或 --no-title：删除显示时间间隔、命令和当前时间和日期的标题。
```

### 监控系统正常运行时间并在输出发生变化时退出 `watch` 命令

```bash
# watch -g [command]
watch -g uptime
# -g 或 --chgexit：当用户定义命令的输出发生变化时退出 watch 命令。
```



# X

# Y

# Z

# #

## 触发 SCSI 主机（host）的扫描过程

```bash
echo '- - -' > /sys/class/scsi_host/host0/scan
```

