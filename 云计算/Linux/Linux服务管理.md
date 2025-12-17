# Linux服务管理

## 1.Linux的进程

**守护进程**就是一直在后台运行的程序

一般来说，Linux的进程分为**前台进程、后台进程、守护进程**

**前台进程**：是在终端中运行的命令，该终端就为进程的控制终端。一旦这个终端关闭，这个进程也随之消失

**后台进程**：是运行在后台的一种特殊进程，不受终端控制。它可以在后台运行，不会占用控制终端，而且可以在用户退出登录后继续运行。

**守护进程**：是一种特殊的后台进程，它独立于控制终端并且周期性地执行某种任务或等待处理某些发生的事件

![image-20230610132216515](../../.gitbook/assets/lvango-0.png)

![image-20230610133545238](../../.gitbook/assets/m33n0d-0.png)

![image-20230610134636345](../../.gitbook/assets/m9nu63-0.png)

![image-20230610134848629](../../.gitbook/assets/mauzs2-0.png)

![image-20230610135301491](../../.gitbook/assets/mdk2s5-0.png)

![image-20230610135245878](../../.gitbook/assets/md7ygy-0.png)

![image-20230610135734655](../../.gitbook/assets/mg78ex-0.png)

![](../../.gitbook/assets/n5um7f-0.png)

![image-20230610140732814](../../.gitbook/assets/n9yhq8-0.png)

![image-20230610141403628](../../.gitbook/assets/ndvvv2-0.png)

```bash
# 可以使用renice命令调整优先级
renice -n -20 23422
```

![image-20230610141432109](../../.gitbook/assets/ne46xw-0.png)

> 在 Linux 系统中，进程可以分为非实时进程和实时进程。它们主要的区别在于调度上的优先级和调度策略的不同。
>
> 非实时进程是系统中最常见的进程类型，它的调度优先级较低，调度策略是时间片轮转调度算法。在时间片轮转调度算法下，每个进程被分配一个固定长度的时间片，当时间片用完后，就会释放 CPU 资源，给其他进程使用。在该算法下，进程的执行时间无法保证，也无法保证实时性要求严格的任务能够得到及时执行。
>
> 而实时进程则是需要满足更严格实时性要求的进程。实时进程的调度策略需要支持实时处理，能够保证在规定时间内完成任务，所以调度策略是优先级调度。系统必须在规定时间内分配足够的 CPU 时间给它，否则就会导致系统不稳定或发生错误。
>
> 实时进程被分为了两个优先级，一个是实时优先级，一个是普通优先级。实时进程的实时优先级值越小，其拥有的调度优先级越高。调度算法通过不断比较实时进程的实时优先级和进程在进入队列前断定的优先级来确定下一个执行的进程。
>
> 实时进程要比非实时进程具有更快的响应时间和更可靠的执行时间。因此，它们通常应用于满足实时需求的任务，如控制系统、信号处理、数据采集和音频/视频处理等。当实时进程运行时，实时性要求高的进程优先完成，从而保证了系统的稳定性和准确性。

![image-20230610141622175](../../.gitbook/assets/nf96k3-0.png)

## 2.前台进程与后台进程

有时候我们不想把程序在前台运行，我们可以把前台进程转换为后台进程

```bash
yum makecache &
```

只要在命令的尾部加上符号`&`，启动的进程就会变成"后台进程"。如果要让正在运行的"前台任务"变为"后台任务"，可以先按`ctrl + z`，然后执行`bg`命令（让最近一个暂停的"后台任务"继续执行）。

"后台任务"有两个特点：

> 1. 继承当前session的标准输出(stdout)和标准错误(stderr)。因此，后台任务的所有输出依然会同步地在命令行下显示。
> 2. 不再继承当前session的标准输入(stdin)。你无法向这个任务输入指令了。如果它试图读取标准输入，就会暂停执行(halt)

所以。后台进程和前台进程的本质区别只有一个：**是否继承标准输入**。所以，执行后台任务的同时，用户还可以输入其他命令

## 3.SIGHUP信号

当用户退出session以后，后台进程是否还会继续执行？

Linux进程退出流程：

> 1. 用户准备退出session
> 2. 系统向该session发出SIGHUP信号
> 3. session将SIGHUP信号发给所有子进程
> 4. 子进程收到SIGHUP信号后，自动退出

所以，一个进程退出是因为收到了`SIGHUP`信号。

那么，后台进程是否也会收到`SIGHUP`信号呢？

这就由Shell中的`huponexit`参数决定的

```bash
shopt | grep huponexit
```

一般来说，这个参数默认是关闭的，因此，session退出的时候，不会把`SIGHUP`信号发给后台进程。所以，一般来说，后台程序不会随着session一起退出

## 4.disown命令

其实，通过后台进程启动守护进程并不保险，因为有的系统huponexit参数时打开的

更保险的方法是使用`disown`命令。它可以将指定任务从后台任务列表中移除，将它变成孤儿进程。一个后台任务只要不在这个后台任务列表中，session就肯定不会向它发出`SIGHUP`信号

`disown`命令用法如下：

```bash
# 移出最近一个正在执行的后台任务
disown

# 移出所有正在执行
disown -r

# 移出所有
disown -a

# 不移出任务，但是让它们不收到信号
disown -h

# 指定后台任务
disown %2
disown -h %2
```

## 5.nohup命令

如果是不想让后台进程接收`SIGHUP`信号，还有一个命令可以实现。那就是`nohup`命令

> 1. 阻止SIGHUP信号发送到这个进程
> 2. 关闭标准输入。该进程不再能接收任何输入，即使是前台程序
> 3. 重定向标准输出和标准错误到文件nohup.out

也就是说，`nohub`命令将子进程与它所在的session分离了

但是，`nohub`不会自动把进程变成后台进程，所以还是得使用`&`

## 6.进程管理工具

![](../../.gitbook/assets/nivllc-0.png)

![image-20230610142808022](../../.gitbook/assets/nm8rgo-0.png)

![image-20230610143715363](../../.gitbook/assets/nrps31-0.png)

![image-20230610144148387](../../.gitbook/assets/nuj3x7-0.png)

![image-20230610144628683](../../.gitbook/assets/nx5i3g-0.png)

![image-20230610144747251](../../.gitbook/assets/nxuyf2-0.png)

```bash
# pidof查看命令进程的pid
# taskset 命令用于将进程绑定到指定的 CPU 或 CPU 核心上运行，以优化 CPU 的利用率和效率
taskset -cp 0,4 `pidof dd`
# -c，--cpu-list：指定 CPU 列表。
# -p，--pid：绑定已有进程到指定的 CPU 上。
```

![image-20230610150737985](../../.gitbook/assets/oxirjp-0.png)

![image-20230610171841268](../../.gitbook/assets/sf66l2-0.png)

![image-20230610172854619](../../.gitbook/assets/slfsld-0.png)

![image-20230610173312954](../../.gitbook/assets/snxdps-0.png)

![image-20230610173822679](../../.gitbook/assets/sqys04-0.png)

![image-20230610174003124](../../.gitbook/assets/ss1khr-0.png)

![image-20230610174409354](../../.gitbook/assets/sugiqs-0.png)

![image-20230610174457970](../../.gitbook/assets/suzi4z-0.png)

![image-20230610175449700](../../.gitbook/assets/t0vzpe-0.png)

![image-20230610175506345](../../.gitbook/assets/t0xfar-0.png)

![image-20230610175522452](../../.gitbook/assets/t10pyv-0.png)

![image-20230610175642535](../../.gitbook/assets/t1qk9s-0.png)

![image-20230610175750372](../../.gitbook/assets/t2do2q-0.png)

![image-20230610175736399](../../.gitbook/assets/t2ap37-0.png)

![image-20230610180101112](../../.gitbook/assets/tsci39-0.png)

![image-20230610180233777](../../.gitbook/assets/tt4twi-0.png)

```bash
# 0信号可以检查进程是否存在
[root@cloud ~]# killall -0 ping
[root@cloud ~]# echo $?
0
```

![image-20230610195806853](../../.gitbook/assets/wdscke-0.png)

## 7.系统启动流程

> LInux组成

* Linux：kernel+rootfs
  * kernel：进程管理、内存管理、网络管理、驱动程序、文件系统、安全功能
  * rootfs：程序和glic
  * 库：函数集合，function，调用接口(头文件负责描述)
  * 程序：二进制执行文件
* 内核设计流派：
  * 单内核(monolithic kernel)：Linux
    * 把所有功能集成与同一程序，分层实现不同功能，系统庞大复杂
  * 微内核(micro kernel)：Windows，Solaris
    * 每种功能使一个单独子系统实现，将内核功能移到用户空间，性能差

![image-20230611172240919](../../.gitbook/assets/shjuqf-0.png)

![image-20230621143129514](../../.gitbook/assets/no5uns-0.png)

![image-20230611172529419](../../.gitbook/assets/sja2tn-0.png)

![image-20230611173350785](../../.gitbook/assets/soejjz-0.png)

![image-20230611175536421](../../.gitbook/assets/t16jwl-0.png)

![image-20230611181057635](../../.gitbook/assets/tyaehg-0.png)

```bash
# /boot/initramfs-3.10.0-1160.90.1.el7.x86_64.img
# 因为有关根挂载的文件系统模块，内核文件没有加载，所以无法挂载根目录
# 所以把相关模块放在/boot/initramfs-3.10.0-1160.90.1.el7.x86_64.img，以便启动时能挂载根目录
# 如果删除这个文件，系统无法启动
# 使用mkinitrd命令生成
mkinitrd /boot/initramfs-`uname -r`.img `uname -r`
```

![image-20230611181902371](../../.gitbook/assets/u30p5c-0.png)

![image-20230620165749377](../../.gitbook/assets/revcl8-0.png)

![image-20230621144245440](../../.gitbook/assets/nusyxg-0.png)

> grub修复

![image-20230620171626732](../../.gitbook/assets/sdtr7m-0.png)

第二种方法必须保证grub目录下的文件完整性，grub2可以使用`grub2-makeconfig -o /boot/grub2/grub.cfg`依赖`/etc/default/grub`生成配置文件

![image-20230620180012562](../../.gitbook/assets/trr2fm-0.png)

![](../../.gitbook/assets/ttofzk-0.png)

![image-20230620180446147](../../.gitbook/assets/tuby38-0.png)

![image-20230620180509770](../../.gitbook/assets/tupqbz-0.png)

![image-20230620180528466](../../.gitbook/assets/tutlfm-0.png)

## 8./proc

![image-20230620224135129](../../.gitbook/assets/112fztn-0.png)

![image-20230620224411649](../../.gitbook/assets/1143gjt-0.png)

命令修改或者在/proc/sys里面修改都只能临时修改，如果要永久修改，要到配置文件中修改，格式参照`sysctl -a`

## 9.编译内核

![image-20230620225632617](../../.gitbook/assets/11bd60u-0.png)

```bash
# 使用可视化菜单来编译模块
make menuconfig
# 可以把/boot/config-3.10.0-1160.90.1.el7.x86_64复制为本文件夹的.config，让基于这个文件的模块修改
```

![image-20230620225646674](../../.gitbook/assets/11bg4cf-0.png)

![image-20230620230739279](../../.gitbook/assets/125roty-0.png)

![image-20230621130804218](../../.gitbook/assets/lmtdh0-0.png)

![image-20230621131052254](../../.gitbook/assets/lo93bq-0.png)

## 6.Systemd

除了上述的几种方法外，Linux系统有自己专门的守护进程管理工具Systemd。它是操作系统的一部分，直接与内核交互，性能出色，功能强大。我们完全可以将程序交给 Systemd ，让系统统一管理，成为真正意义上的系统服务。

![image-20230621134537387](../../.gitbook/assets/m905aq-0.png)

![image-20230621135052768](../../.gitbook/assets/mc2mo8-0.png)

### 6.1.由来

一直以来，Linux的启动一直采用`init`进程

使用service来启动服务

```bahs
service httpd start
```

但是，这种方法有两个缺点

一是启动时间长。`init`进程是串行启动，只有前一个进程启动完，才回启动下一个进程

二是启动脚本复杂。`init`进程只是执行启动脚本，不管其他事情。脚本需要自己处理各种情况，这往往使得脚本变得很长

### 6.2.Systemd概述

Systemd 就是为了解决这些问题而诞生的。它的设计目标是，为系统的启动和管理提供一套完整的解决方案。

根据 Linux 惯例，字母`d`是守护进程（daemon）的缩写。 Systemd 这个名字的含义，就是它要守护整个系统。

使用了Systemd，就不需要再用init了。CentOS7中，Systemd取代了init，称为了系统第一个进程(PID=1)，其他进程都是它的子进程，可以用以下命令查看进程树

```
pstree
```

Systemd的功能强大，使用方便，但是体系庞大，非常复杂。

![img](../../.gitbook/assets/ifjhs1-0.png)

### 6.3.系统管理

Systemd并不是一个命令，而是一组命令，涉及到系统管理的方方面面

#### 6.3.1.systemctl

`systemctl`是Systemd的主命令，用于管理系统

```bash
# 重启系统
$ sudo systemctl reboot

# 关闭系统，切断电源
$ sudo systemctl poweroff

# CPU停止工作
$ sudo systemctl halt

# 暂停系统
$ sudo systemctl suspend

# 让系统进入冬眠状态
$ sudo systemctl hibernate

# 让系统进入交互式休眠状态
$ sudo systemctl hybrid-sleep

# 启动进入救援状态（单用户状态）
$ sudo systemctl rescue
```

#### 6.3.2.systemd-analyze

`systemd-analyze`命令用于查看启动耗时

```bash
# 查看启动耗时
$ systemd-analyze                                                                                       

# 查看每个服务的启动耗时
$ systemd-analyze blame

# 显示瀑布状的启动过程流
$ systemd-analyze critical-chain

# 显示指定服务的启动流
$ systemd-analyze critical-chain atd.service
```

#### 6.3.3.hostnamectl

`hostnamectl`用于查看当前主机的信息

```bash
# 显示当前主机的信息
$ hostnamectl

# 设置主机名。
$ sudo hostnamectl set-hostname rhel7
```

#### 6.3.4.localetcl

`localectl`命令用于查看本地化设置。

```bash
# 查看本地化设置
 $ localectl

# 设置本地化参数。
$ sudo localectl set-locale LANG=en_GB.utf8
$ sudo localectl set-keymap en_GB
```

#### 6.3.5.timedatectl

`timedatectl`命令用于查看当前时区设置。

```bash
# 查看当前时区设置
$ timedatectl

# 显示所有可用的时区
$ timedatectl list-timezones                                                                                   

# 设置当前时区
$ sudo timedatectl set-timezone America/New_York
$ sudo timedatectl set-time YYYY-MM-DD
$ sudo timedatectl set-time HH:MM:SS
```

#### 6.3.6.loginctl

`loginctl`命令用于查看当前登录的用户。

```bash
# 列出当前session
$ loginctl list-sessions

# 列出当前登录用户
$ loginctl list-users

# 列出显示指定用户的信息
$ loginctl show-user ruanyf
```

### 6.4.Unit

Systemd可以管理所有系统资源，不同的资源统称为Unit(单位)

![image-20230621134759429](../../.gitbook/assets/makgtu-0.png)

Unit 一共分成12种。

> * Service unit：系统服务
> * Target unit：多个 Unit 构成的一个组
> * Device Unit：硬件设备
> * Mount Unit：文件系统的挂载点
> * Automount Unit：自动挂载点
> * Path Unit：文件或路径
> * Scope Unit：不是由 Systemd 启动的外部进程
> * Slice Unit：进程组
> * Snapshot Unit：Systemd 快照，可以切回某个快照
> * Socket Unit：进程间通信的 socket
> * Swap Unit：swap 文件
> * Timer Unit：定时器

`systemctl list-units`命令可以查看当前系统的所有 Unit 。

```bash
# 列出正在运行的 Unit
$ systemctl list-units

# 列出所有Unit，包括没有找到配置文件的或者启动失败的
$ systemctl list-units --all

# 列出所有没有运行的 Unit
$ systemctl list-units --all --state=inactive

# 列出所有加载失败的 Unit
$ systemctl list-units --failed

# 列出所有正在运行的、类型为 service 的 Unit
$ systemctl list-units --type=service

# 查看所有自启的服务
systemctl list-unit-files --type=service | grep enabled

```

#### 6.4.1.Unit状态

`systemctl status`命令用于查看系统状态和单个 Unit 的状态。

```bash
# 显示系统状态
$ systemctl status

# 显示单个 Unit 的状态
$ sysystemctl status bluetooth.service

# 显示远程主机的某个 Unit 的状态
$ systemctl -H root@rhel7.example.com status httpd.service
```

读取服务状态时，系统会返回以下信息

```bash
$ sudo systemctl status httpd

httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled)
   Active: active (running) since 金 2014-12-05 12:18:22 JST; 7min ago
 Main PID: 4349 (httpd)
   Status: "Total requests: 1; Current requests/sec: 0; Current traffic:   0 B/sec"
   CGroup: /system.slice/httpd.service
           ├─4349 /usr/sbin/httpd -DFOREGROUND
           ├─4350 /usr/sbin/httpd -DFOREGROUND
           ├─4351 /usr/sbin/httpd -DFOREGROUND
           ├─4352 /usr/sbin/httpd -DFOREGROUND
           ├─4353 /usr/sbin/httpd -DFOREGROUND
           └─4354 /usr/sbin/httpd -DFOREGROUND

12月 05 12:18:22 localhost.localdomain systemd[1]: Starting The Apache HTTP Server...
12月 05 12:18:22 localhost.localdomain systemd[1]: Started The Apache HTTP Server.
12月 05 12:22:40 localhost.localdomain systemd[1]: Started The Apache HTTP Server.
```

上面的输出结果含义如下：

```bash
Loaded行：配置文件的位置，是否设为开机启动
Active行：表示正在运行
Main PID行：主进程ID
Status行：由应用本身（这里是 httpd ）提供的软件当前状态
CGroup块：应用的所有子进程
日志块：应用的日志
```

除了`status`命令，`systemctl`还提供了三个查询状态的简单方法，主要供脚本内部的判断语句使用。

```bash
# 显示某个 Unit 是否正在运行
$ systemctl is-active application.service

# 显示某个 Unit 是否处于启动失败状态
$ systemctl is-failed application.service

# 显示某个 Unit 服务是否建立了启动链接
$ systemctl is-enabled application.service
```

![image-20230621141950519](../../.gitbook/assets/nh52xg-0.png)

#### 6.4.2.Unit管理

对于用户来说，最常用的是下面这些命令，用于启动和停止 Unit（主要是 service）。

```bash
# 立即启动一个服务
$ sudo systemctl start apache.service

# 立即停止一个服务
$ sudo systemctl stop apache.service

# 重启一个服务
$ sudo systemctl restart apache.service

# 杀死一个服务的所有子进程
$ sudo systemctl kill apache.service

# 重新加载一个服务的配置文件
$ sudo systemctl reload apache.service

# 重载所有修改过的配置文件
$ sudo systemctl daemon-reload

# 显示某个 Unit 的所有底层参数
$ systemctl show httpd.service

# 显示某个 Unit 的指定属性的值
$ systemctl show -p CPUShares httpd.service

# 设置某个 Unit 的指定属性
$ sudo systemctl set-property httpd.service CPUShares=500

# 禁止启动服务
$ systemctl mask(unmask) name
```

#### 6.4.3.依赖关系

Unit 之间存在依赖关系：A 依赖于 B，就意味着 Systemd 在启动 A 的时候，同时会去启动 B。

`systemctl list-dependencies`命令列出一个 Unit 的所有依赖。

```bash
$ systemctl list-dependencies nginx.service
```

上面命令的输出结果之中，有些依赖是 Target 类型（详见下文），默认不会展开显示。如果要展开 Target，就需要使用`--all`参数。

```bash
$ systemctl list-dependencies --all nginx.service
```

### 6.5.Unit配置文件

#### 6.5.1.概述

每一个Unit都有一个配置文件，告诉Systemd怎么启动这个Unit

Systemd 默认从目录`/etc/systemd/system/`读取配置文件。但是，里面存放的大部分文件都是符号链接，指向目录`/usr/lib/systemd/system/`，真正的配置文件存放在那个目录。

`systemctl enable`命令用于在上面两个目录之间，建立符号链接关系。

```bash
$ sudo systemctl enable clamd@scan.service
# 等同于
$ sudo ln -s '/usr/lib/systemd/system/clamd@scan.service' '/etc/systemd/system/multi-user.target.wants/clamd@scan.service'
```

如果配置文件里面设置了开机启动，`systemctl enable`命令相当于激活开机启动。

与之对应的，`systemctl disable`命令用于在两个目录之间，撤销符号链接关系，相当于撤销开机启动。

```bash
$ sudo systemctl disable clamd@scan.service
```

配置文件的后缀名，就是该 Unit 的种类，比如`sshd.socket`。如果省略，Systemd 默认后缀名为`.service`，所以`sshd`会被理解成`sshd.service`。

#### 6.5.2.配置文件状态

`systemctl list-unit-files`命令用于列出所有配置文件。

```bash
# 列出所有配置文件
$ systemctl list-unit-files

# 列出指定类型的配置文件
$ systemctl list-unit-files --type=service
```

这个命令会输出一个列表。

```bash
$ systemctl list-unit-files

UNIT FILE              STATE
chronyd.service        enabled
clamd@.service         static
clamd@scan.service     disabled
```

这个列表显示每个配置文件的状态，一共有四种。

> * enabled：已建立启动链接
> * disabled：没建立启动链接
> * static：该配置文件没有`[Install]`部分（无法执行），只能作为其他配置文件的依赖
> * masked：该配置文件被禁止建立启动链接

注意，从配置文件的状态无法看出，该 Unit 是否正在运行。这必须执行前面提到的`systemctl status`命令。

```bash
$ systemctl status bluetooth.service
```

一旦修改配置文件，就要让 SystemD 重新加载配置文件，然后重新启动，否则修改不会生效。

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl restart httpd.service
```

#### 6.5.3.配置文件格式

* \[Unit]：描述服务的元数据，如服务名称、描述、依赖关系等。
* \[Service]：描述服务的具体行为，如要运行的命令、环境变量、工作目录等。
* \[Install]：描述如何安装服务，如安装路径、安装类型等。

`systemctl cat`命令可以查看配置文件内容

```bash
$ systemctl cat named.service

# /usr/lib/systemd/system/named.service
[Unit]
Description=Berkeley Internet Name Domain (DNS)
Wants=nss-lookup.target
Wants=named-setup-rndc.service
Before=nss-lookup.target
After=network.target
After=named-setup-rndc.service

[Service]
Type=forking
Environment=NAMEDCONF=/etc/named.conf
EnvironmentFile=-/etc/sysconfig/named
Environment=KRB5_KTNAME=/etc/named.keytab
PIDFile=/run/named/named.pid

ExecStartPre=/bin/bash -c 'if [ ! "$DISABLE_ZONE_CHECKING" == "yes" ]; then /usr/sbin/named-checkconf -z "$NAMEDCONF"; else echo "Checking of zone fi
ExecStart=/usr/sbin/named -u named -c ${NAMEDCONF} $OPTIONS

ExecReload=/bin/sh -c '/usr/sbin/rndc reload > /dev/null 2>&1 || /bin/kill -HUP $MAINPID'

ExecStop=/bin/sh -c '/usr/sbin/rndc stop > /dev/null 2>&1 || /bin/kill -TERM $MAINPID'

PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

从上面的输出可以看到，配置文件分成几个区块。每个区块的第一行，是用方括号表示的区别名，比如`[Unit]`。注意，配置文件的区块名和字段名，都是大小写敏感的。

每个区块内部是一些等号连接的键值对。且键值对的等号两侧不能有空格

#### 6.5.4.配置文件的区块

`[Unit]`区块通常是配置文件的第一个区块，用来定义 Unit 的元数据，以及配置与其他 Unit 的关系。它的主要字段如下。

> * `Description`：简短描述
> * `Documentation`：文档地址
> * `Requires`：当前 Unit 依赖的其他 Unit，如果它们没有运行，当前 Unit 会启动失败
> * `Wants`：与当前 Unit 配合的其他 Unit，如果它们没有运行，当前 Unit 不会启动失败
> * `BindsTo`：与`Requires`类似，它指定的 Unit 如果退出，会导致当前 Unit 停止运行
> * `Before`：如果该字段指定的 Unit 也要启动，那么必须在当前 Unit 之后启动
> * `After`：如果该字段指定的 Unit 也要启动，那么必须在当前 Unit 之前启动
> * `Conflicts`：这里指定的 Unit 不能与当前 Unit 同时运行
> * `Condition...`：当前 Unit 运行必须满足的条件，否则不会运行
> * `Assert...`：当前 Unit 运行必须满足的条件，否则会报启动失败

注意：`After`和`Before`字段只涉及启动顺序，不涉及依赖关系。

​ `Wants`定义弱依赖关系，即设定的依赖出了问题，不影响服务继续执行

​ `Requires`定义强依赖关系，即如果定义的依赖除了文件，此服务也不能运行

```
	   `Wants`和`Requires`字段致设计依赖关系，与启动顺序无关，默认同时启动
```

`[Install]`通常是配置文件的最后一个区块，用来定义如何启动，以及是否开机启动。它的主要字段如下。

> * `WantedBy`：它的值是一个或多个 Target，当前 Unit 激活时（enable）符号链接会放入`/etc/systemd/system`目录下面以 Target 名 + `.wants`后缀构成的子目录中
> * `RequiredBy`：它的值是一个或多个 Target，当前 Unit 激活时，符号链接会放入`/etc/systemd/system`目录下面以 Target 名 + `.required`后缀构成的子目录中
> * `Alias`：当前 Unit 可用于启动的别名
> * `Also`：当前 Unit 激活（enable）时，会被同时激活的其他 Unit

`Target`的含义是服务组，表示一组服务。`WantedBy=multi-user.target`指的是，sshd 所在的 Target 是`multi-user.target`。

这个设置非常重要，因为执行`systemctl enable sshd.service`命令时，`sshd.service`的一个符号链接，就会放在`/etc/systemd/system`目录下面的`multi-user.target.wants`子目录之中。

`[Service]`区块用来 Service 的配置，只有 Service 类型的 Unit 才有这个区块。它的主要字段如下。

> * `Type`：定义启动时的进程行为。它有以下几种值。
>   * `Type=simple`：默认值，执行`ExecStart`指定的命令，启动主进程
>   * `Type=forking`：以 fork 方式从父进程创建子进程，创建后父进程会立即退出
>   * `Type=oneshot`：一次性进程，Systemd 会等当前服务退出，再继续往下执行
>   * `Type=dbus`：当前服务通过D-Bus启动
>   * `Type=notify`：当前服务启动完毕，会通知`Systemd`，再继续往下执行
>   * `Type=idle`：若有其他任务执行完毕，当前服务才会运行
> * `ExecStart`：启动当前服务的命令
> * `ExecStartPre`：启动当前服务之前执行的命令
> * `ExecStartPost`：启动当前服务之后执行的命令
> * `ExecReload`：重启当前服务时执行的命令
> * `ExecStop`：停止当前服务时执行的命令
> * `ExecStopPost`：停止当其服务之后执行的命令
> * `RestartSec`：自动重启当前服务间隔的秒数
> * `Restart`：定义何种情况 Systemd 会自动重启当前服务
>   * no（默认值）：退出后不会重启
>   * on-success：只有正常退出时（退出状态码为0），才会重启
>   * on-failure：非正常退出时（退出状态码非0），包括被信号终止和超时，才会重启
>   * on-abnormal：只有被信号终止和超时，才会重启
>   * on-abort：只有在收到没有捕捉到的信号终止时，才会重启
>   * on-watchdog：超时退出，才会重启
>   * always：不管是什么退出原因，总是重启
>   * 对于守护进程，推荐设为`on-failure`。对于那些允许发生错误退出的服务，可以设为`on-abnormal`
> * `KillMode`：定义Systemd如何停止sshd服务
>   * control-group（默认值）：当前控制组里面的所有子进程，都会被杀掉
>   * process：只杀主进程
>   * mixed：主进程将收到 SIGTERM 信号，子进程收到 SIGKILL 信号
>   * none：没有进程会被杀掉，只是执行服务的 stop 命令。
> * `TimeoutSec`：定义 Systemd 停止当前服务之前等待的秒数
> * `Environment`：指定环境变量

注意：所有的启动设置之前，都可以加上一个连词号（`-`），表示"抑制错误"，即发生错误的时候，不影响其他命令的执行。比如，`EnvironmentFile=-/etc/sysconfig/sshd`（注意等号后面的那个连词号），就表示即使`/etc/sysconfig/sshd`文件不存在，也不会抛出错误。

下面是一个`oneshot`的例子，笔记本电脑启动时，要把触摸板关掉，配置文件可以这样写。

```bash
[Unit]
Description=Switch-off Touchpad

[Service]
Type=oneshot
ExecStart=/usr/bin/touchpad-off

[Install]
WantedBy=multi-user.target
```

上面的配置文件，启动类型设为`oneshot`，就表明这个服务只要运行一次就够了，不需要长期运行。

如果关闭以后，将来某个时候还想打开，配置文件修改如下。

```bash
[Unit]
Description=Switch-off Touchpad

[Service]
Type=oneshot
ExecStart=/usr/bin/touchpad-off start
ExecStop=/usr/bin/touchpad-off stop
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

上面配置文件中，`RemainAfterExit`字段设为`yes`，表示进程退出以后，服务仍然保持执行。这样的话，一旦使用`systemctl stop`命令停止服务，`ExecStop`指定的命令就会执行，从而重新开启触摸板。

Unit 配置文件的完整字段清单，请参考[官方文档](https://www.freedesktop.org/software/systemd/man/systemd.unit.html)。

### 6.6.Target

启动计算机的时候，需要启动大量的 Unit。如果每一次启动，都要一一写明本次启动需要哪些 Unit，显然非常不方便。Systemd 的解决方案就是 Target。

简单说，Target 就是一个 Unit 组，包含许多相关的 Unit 。启动某个 Target 的时候，Systemd 就会启动里面所有的 Unit。从这个意义上说，Target 这个概念类似于"状态点"，启动某个 Target 就好比启动到某种状态。

传统的`init`启动模式里面，有 RunLevel 的概念，跟 Target 的作用很类似。不同的是，RunLevel 是互斥的，不可能多个 RunLevel 同时启动，但是多个 Target 可以同时启动。

```bash
# 查看当前系统的所有 Target
$ systemctl list-unit-files --type=target

# 查看一个 Target 包含的所有 Unit
$ systemctl list-dependencies multi-user.target

# 查看启动时的默认 Target
$ systemctl get-default

# 设置启动时的默认 Target
$ sudo systemctl set-default multi-user.target

# 切换 Target 时，默认不关闭前一个 Target 启动的进程，
# systemctl isolate 命令改变这种行为，
# 关闭前一个 Target 里面所有不属于后一个 Target 的进程
$ sudo systemctl isolate multi-user.target
```

Target 与 传统 RunLevel 的对应关系如下。

```bash
Traditional runlevel      New target name     Symbolically linked to...

Runlevel 0           |    runlevel0.target -> poweroff.target
Runlevel 1           |    runlevel1.target -> rescue.target
Runlevel 2           |    runlevel2.target -> multi-user.target
Runlevel 3           |    runlevel3.target -> multi-user.target
Runlevel 4           |    runlevel4.target -> multi-user.target
Runlevel 5           |    runlevel5.target -> graphical.target
Runlevel 6           |    runlevel6.target -> reboot.target
```

它与`init`进程的主要差别如下。

> **（1）默认的 RunLevel**（在`/etc/inittab`文件设置）现在被默认的 Target 取代，位置是`/etc/systemd/system/default.target`，通常符号链接到`graphical.target`（图形界面）或者`multi-user.target`（多用户命令行）。
>
> **（2）启动脚本的位置**，以前是`/etc/init.d`目录，符号链接到不同的 RunLevel 目录 （比如`/etc/rc3.d`、`/etc/rc5.d`等），现在则存放在`/lib/systemd/system`和`/etc/systemd/system`目录。
>
> **（3）配置文件的位置**，以前`init`进程的配置文件是`/etc/inittab`，各种服务的配置文件存放在`/etc/sysconfig`目录。现在的配置文件主要存放在`/lib/systemd`目录，在`/etc/systemd`目录里面的修改可以覆盖原始设置。

Target 也有自己的配置文件。

```bash
$ systemctl cat multi-user.target

[Unit]
Description=Multi-User System
Documentation=man:systemd.special(7)
Requires=basic.target
Conflicts=rescue.service rescue.target
After=basic.target rescue.service rescue.target
AllowIsolate=yes
```

注意，Target 配置文件里面没有启动命令。

上面输出结果中，主要字段含义如下。

> `Requires`字段：要求`basic.target`一起运行。
>
> `Conflicts`字段：冲突字段。如果`rescue.service`或`rescue.target`正在运行，`multi-user.target`就不能运行，反之亦然。
>
> `After`：表示`multi-user.target`在`basic.target` 、 `rescue.service`、 `rescue.target`之后启动，如果它们有启动的话。
>
> `AllowIsolate`：允许使用`systemctl isolate`命令切换到`multi-user.target`。

### 6.7.日志管理

Systemd 统一管理所有 Unit 的启动日志。带来的好处就是，可以只用`journalctl`一个命令，查看所有日志（内核日志和应用日志）。日志的配置文件是`/etc/systemd/journald.conf`。

`journalctl`功能强大，用法非常多。

```bash
# 查看所有日志（默认情况下 ，只保存本次启动的日志）
$ sudo journalctl

# 查看内核日志（不显示应用日志）
$ sudo journalctl -k

# 查看系统本次启动的日志
$ sudo journalctl -b
$ sudo journalctl -b -0

# 查看上一次启动的日志（需更改设置）
$ sudo journalctl -b -1

# 查看指定时间的日志
$ sudo journalctl --since="2012-10-30 18:17:16"
$ sudo journalctl --since "20 min ago"
$ sudo journalctl --since yesterday
$ sudo journalctl --since "2015-01-10" --until "2015-01-11 03:00"
$ sudo journalctl --since 09:00 --until "1 hour ago"

# 显示尾部的最新10行日志
$ sudo journalctl -n

# 显示尾部指定行数的日志
$ sudo journalctl -n 20

# 实时滚动显示最新日志
$ sudo journalctl -f

# 查看指定服务的日志
$ sudo journalctl /usr/lib/systemd/systemd

# 查看指定进程的日志
$ sudo journalctl _PID=1

# 查看某个路径的脚本的日志
$ sudo journalctl /usr/bin/bash

# 查看指定用户的日志
$ sudo journalctl _UID=33 --since today

# 查看某个 Unit 的日志
$ sudo journalctl -u nginx.service
$ sudo journalctl -u nginx.service --since today

# 实时滚动显示某个 Unit 的最新日志
$ sudo journalctl -u nginx.service -f

# 合并显示多个 Unit 的日志
$ journalctl -u nginx.service -u php-fpm.service --since today

# 查看指定优先级（及其以上级别）的日志，共有8级
# 0: emerg
# 1: alert
# 2: crit
# 3: err
# 4: warning
# 5: notice
# 6: info
# 7: debug
$ sudo journalctl -p err -b

# 日志默认分页输出，--no-pager 改为正常的标准输出
$ sudo journalctl --no-pager

# 以 JSON 格式（单行）输出
$ sudo journalctl -b -u nginx.service -o json

# 以 JSON 格式（多行）输出，可读性更好
$ sudo journalctl -b -u nginx.serviceqq
 -o json-pretty

# 显示日志占据的硬盘空间
$ sudo journalctl --disk-usage

# 指定日志文件占据的最大空间
$ sudo journalctl --vacuum-size=1G

# 指定日志文件保存多久
$ sudo journalctl --vacuum-time=1years
```

### 6.8.修改配置文件后重启

如果你修改了配置文件，那么需要重新加载配置文件，如何重新启动相关服务

```bash
# 重新加载配置文件
$ sudo systemctl daemon-reload

# 重启相关服务
$ sudo systemctl restart foobar
```

但是如果你修改了systemd的配置文件，要么重启生效，要么也像服务一样执行

```bash
$ systemctl daemon-reload

$ systemctl restart systemd
```
