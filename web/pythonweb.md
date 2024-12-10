[toc]

## #概述

> 常见的项目类型

1. B/S
   - 浏览器/服务器模式
2. C/S
   - 客户端/服务器模式

> 项目不同组成

- 前端	
  - HTML：web网页的内容和框架
  - CSS：样式，修饰网页内容
  - JavaScript：通过改变HTML和CSS形成页面动态效果或者用户交互操作

- 后台
  - 和前端数据交互
  - 业务处理-处理数据
  - 对数据存储的操作

- 数据存储

## 1.HTML和CSS基础

### 1.1.什么是Web

web，全称为World Wide Web，也叫作www，中文译为万维网。万维网是一个通过互联网访问的、由许多互相链接的超文本组成的庞大文档系统



Web开发主要分为前端和后端，前端是指用户直接交互的部分，包括Web页面结构(**HTML**)，Web的外观视觉表现(**CSS**)以及Web层面的交互实现(**JavaScript**)，后端更多的是指与数据库进行交互并处理相应的业务逻辑，需要考虑的是如何实现业务功能、数据存取、平台的稳定性与性能等



网页主要由格式化文本文件和超文本标记语言(**HTML**)组成，除此之外，网页还可能包括图片、影片、声音等组件

> 互联网和万维网这两个词通常没有多少区别，但本质上两者并不相同。互联网是一个全球互相连接的计算机网络系统，相比之下，万维网只是通过超链接和同一资源标识符连接的全球收集的文本和其他资源系统。万维网通常使用HTTP协议访问，该协议是互联网通信协议中非常关键的一环

### 1.2.Web应用程序的工作环境

需要访问万维网上的某个网页或网络资源时，需要在浏览器上输入待访问网页的统一资源定位符(**URL**)，或者通过超链接跳转。



工作流程如下：

1. URL的服务器名部分，被分布于全球的因特网数据库所解析(域名系统)
2. 根据解析结果进入IP地址
3. 向该IP地址所在的服务器发送一个HTTP请求
4. 服务器响应并逐一发送构成该网页的文件

![](https://note.youdao.com/yws/public/resource/92933d878935240680c00793fc3e404c/xmlnote/WEBRESOURCE39c46921fdb054ef959a82e3abe732a5/414)

## 2.网络编程基础

### 2.1.TCP/IP协议

当计算机为了联网时，就必须约定通信协议。

网络协议三要素为：语法、语义、时序

互联网协议包含了上百种协议标准，最重要的是TCP协议和IP协议，所以习惯上把互联网的协议简称为TCP/IP协议。TCP/IP协议包含四个概念层，分别是应用层、传输层、网络层、链路层

1. 应用层：规范不同计算机之间的服务需求，为用户提供所需要的各种服务。该层主要协议有FTP(文件传输协议)、Telnet(远程登录协议)、DNS(域名系统协议)、SMTP(电子邮件传输的协议)等
2. 传输层：规范不同计算机之间交流沟通的语言，为应用层实体提供端到端的通信功能，保证了数据包的顺序传送及数据的完整性。传输层中最常见的两个协议分别是传输控制协议(TCP)和用户数据报协议(UDP)
3. 网络层：解决不同计算机之间链接问题，主要解决主机到主机的通信问题。该层有三个主要协议：网络协议(IP)、互联网组管理协议(IGMP)、互联网控制报文协议(ICMP)
4. 链路层：解决计算机和互联网络链接和数据传输问题，负责监视数据在主机和网络之间的交换。事实上，TCP/IP协议本身并未定义该层的协议，而由参与互连的各网络使用自己的物理层和数据链路层协议，然后与TCP/IP的网络接入层进行连接

![](https://note.youdao.com/yws/public/resource/92933d878935240680c00793fc3e404c/xmlnote/WEBRESOURCE212e32f9e5ce2a54e32079b9f9e03bbd/416)

### 2.2.IP协议

在通信时，通信双方必须知道对方的唯一标识(IP)。

IP：IP实际上是一个32位整数(称为IPv4)，以字符串表示。

> 例如：172.16.254.1
>
> 实际上就是把32位整数按8位分组后的数字表示，目的是便于阅读
>
> IP协议负责把数据从一台计算机通过网络发送到另一台计算机。
>
> 数据被分为一小块一小块，然后通过IP包发送出去。
>
> 由于互联网链路复杂，两台计算机直接经常有多条线路，因此路由器复杂决定如何把一个IP包转发出去。
>
> IP包的特点就是按块发送，途径多个路由，但不保证都能到达，也不保证顺利到达

### 基于传输协议的套接字编程

套接字就是一套用c语义协程的应用程序开发库，主要用于实现进程间通信和网络编程。

实际开发中使用的套接字可以分为三类：流套接字(TCP套接字)、数据报套接字和原始套接字

### 2.3.TCP协议

> TCP协议建立在IP协议基础之上。
>
> TCP负责在两台计算机之间建立可靠连接，保证数据包按顺序到达
>
> **TCP通过三次握手建立可靠连接**，**四次挥手断开连接**
>
> ![](https://note.youdao.com/yws/public/resource/92933d878935240680c00793fc3e404c/xmlnote/WEBRESOURCEe2a4bd56f9ff032dcfdccf6ac3e34f32/418)
>
> **TCP协议对每个IP包编号，确保对方按顺序收到，如果包丢了就重发**
>
> ![](https://note.youdao.com/yws/public/resource/92933d878935240680c00793fc3e404c/xmlnote/WEBRESOURCEb25ceed4107868707e120241d4aff853/420)
>
> 
>
> 许多常用的更高级协议都是建立在TCP协议基础上的，如用于浏览器的HTTP协议、发送邮件的SMTP协议等
>
> 一个TCP报文除了包含要传输的数据外，**还包含源IP地址和目标IP地址，源端口和目标端口**
>
> 端口：每个网络程序都向操作系统申请唯一的端口号，标识唯一的程序
>
> 但是每个线程可能同时与很多计算机进行链接，所以会申请很多端口号。端口号是按照一定的规定进行分配的，如：80端口给HTTP服务，21端口给FTP服务

### 2.4.UDP简介

不同于TCP协议，UDP协议是面向无连接的协议。使用UDP协议时，不需要建立连接，只需要指定对方的IP地址和端口号，就可以直接发送数据包。但是数据无法保证一定到达。

虽然不可靠，但是速度比TCP协议快，对于不要求可靠到达的数据就可以使用UDP协议

![](https://note.youdao.com/yws/public/resource/92933d878935240680c00793fc3e404c/xmlnote/WEBRESOURCE2ccc9e5e2c2382827be6996339f17484/422)

### 2.5.Socket简介

为了让两个程序使用网络进行通信，二者均必须使用Socket套接字，用于描述IP地址和端口，是一个通信链的句柄，可以用来实现不同虚拟机或不同计算机之间的通信。

在python中使用socket模块的socket函数创建一个socket套接字对象

```python
# 语法格式：
s = socket.socket(socket.ADDressFamily,socket.Type)

''''''
该函数带有两个参数：
ADDressFamily：可以选择AF_INET(用于Internet进程间通信)或者AF_UNIX(用于同一台机器进程间通信)
Type：套接字类型，可以是SOCK_STREAM(流式套接字，主要用于TCP协议)或者SOCK_DGRAM(数据套接字，主要用于UDP协议)
''''''

# 创建TCP/IP套接字
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 创建UDP/IP套接字
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
```

主要方法有：

| 方法         | 描述                                                         |
| ------------ | ------------------------------------------------------------ |
| s.bind()     | 绑定地址(host,port)到套接字，在AF_INET下以元组(host,port)的形式表示地址 |
| s.listen()   | 开始TCP监听。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5 |
| s.accept()   | 被动接受TCP客户端连接，(阻塞式)等待连接的到来                |
| s.connect()  | 主动初始化TCP服务器连接，一般address的格式为元组(host,port)，如果连接出错，返回socket.error错误 |
| s.recv()     | 接受TCP数据，以字符串形式返回。bufsize指定要接受的最大数据量；flag提供有关消息的其他信息，通常可以忽略 |
| s.send()     | 发送TCP数据，将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string大小 |
| s.sendall()  | 完整发送TCP数据。。将string中的数据发送到连接的套接字，但在返回之前会尝试发送所有数据。成功则返回None，失败则抛出异常 |
| s.recvfrom() | 接受UDP数据。与recv()类似，但返回值是(data,address)元组。其中data是包含接收数据的字符串，address是发送数据的套接字地址 |
| s.sendto()   | 发送UDP数据，将数据发送到套接字。address是形式为(ipaddr,port)的元组，指定远程地址。返回值是发送的字节数 |
| s.close()    | 关闭套接字                                                   |

### 2.6.TCP编程

因为TCP连接具有安全可靠的特性所以TCP应用更加广泛。创建TCP连接时，主动发起连接的叫做客户端，被动响应连接的叫做服务器。

**创建TCP服务器：**

1. 使用socket创建一个套接字
2. 使用bind绑定IP地址
3. 使用listen使套接字变为可以被动连接
4. 使用accept等待客户端的连接
5. 使用recv/send接收发送数据

```python
import socket
host = '127.0.0.1'
port = 8080
web = socket.socket()
web.bind((host,port))
web.listen(5)
print('服务器等待客户端连接..')
while 1:
    conn,addr = web.accept()
    data = conn.recv(1024)
    print(data)
    # 字符串前面的b代表字符串为bytes对象
    # 常用在如网络编程中，服务器和浏览器只认bytes类型数据
    # HTTP/1.1 200 ok为HTTP的响应报文中的响应行，分别为HTTP协议版本 状态码 状态描述
    conn.sendall(b'HTTP/1.1 200 ok\r\n\r\nHELLO World')
    conn.close()
    
# 运行后再浏览器中输入127.0.0.1:8080连接服务器后网页就会显示HELLO World
```

**创建TCP客户端**

```python
import socket
host = '127.0.0.1'
port = 8080
s = socket.socket()
s.connect((host,port))
send_data = input('请输入要发送的数据：')
s.send(send_data.encode())
recvData = s.recv(1024).decode()
print('接收到的数据为：',recvData)
s.close()

# 先创建一个服务器，在创建一个客户端
# 按顺序运行后，客户端发送信息给服务器，服务器返回数据给客户端
```

#### 2.6.1.TCP总结(建立简易聊天室)

![](https://note.youdao.com/yws/public/resource/92933d878935240680c00793fc3e404c/xmlnote/WEBRESOURCE75d0420b65b4ceac5ec72bbb623b806d/429)

**建立聊天室**

```python
# 服务端
import socket
host = socket.gethostname()
port = 12345
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen(1)
sock,addr = s.accept()
print('连接已经建立')
info = sock.recv(1024).decode()
while info != 'byebye':
    if info:
        print('接收到的内容为：'+info)
    send_data = input('输入发送的内容：')
    sock.send(send_data.encode())
    if send_data == 'byebye':
        break
    info = sock.recv(1024).decode()
sock.close()
s.close()
```

```python
# 客户端
import socket
s = socket.socket()
host = socket.gethostname()
port = 12345
s.connect((host,port))
print('已连接')
info = ''
while info!= 'byebye':
    send_data = input('输入要发送的内容：')
    s.send(send_data.encode())
    if send_data == 'byebye':
        break
    info = s.recv(1024).decode()
    print('接收到的内容：'+info)
s.close()
```

> 按顺序打开服务器和客户端，就可以分别发送消息了

### 2.7.UDP编程

UDP是面向消息的协议，通信时不需要建立连接，数据的传输不可靠。UDP一般用于多点通信和实时的数据业务。如：

1. 语音广播
2. 视频
3. 聊天软件
4. TFTP(简单文件传送)
5. SNMP(简单网络管理协议)
6. RIP(路由信息协议，如报告股票市场，航空消息)
7. DNS(域名解析)

**创建UDP服务器**

```python
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('127.0.0.1',8888))
print('绑定UDP到8888端口')
data,addr = s.recvfrom(1024)
data = float(data)*1.8+32
send_data = '转换后的温度：'+str(data)
print('Received from %s:%s.' % addr)
s.sendto(send_data.encode(),addr)
s.close()
```

**创建UDP客户端**

```python
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
data = input('请输入要转换的温度:')
s.sendto(data.encode(),('127.0.0.1',8888))
print(s.recv(1024).decode())
s.close()
```

#### 2.7.1.UDP模型

![](https://note.youdao.com/yws/public/resource/92933d878935240680c00793fc3e404c/xmlnote/WEBRESOURCE80520a3dcdde67fe608917c3ad00f357/432)

## 3.web基础

### 3.1.HTTP协议

**HTTP协议(超文本传输协议)是互联网上应用最为广泛的一种网络协议。利用TCP在两台计算机(通常是Web服务器和客户端)之间传输信息。**

### 3.2.Web服务器

当浏览器输入URL后，浏览器会先请求DNS服务器，获得请求站点的IP地址(根据http后面的URL获取)，然后发送一个HTTPRequest给拥有该IP的主机，接着就会接收到服务器返回的HTTPResponse

具体过程：

1. 建立连接：客户端通过TCP/IP协议建立到服务器的TCP连接
2. 请求过程：客户端想服务器发送HTTP协议请求包，请求服务器里的资源文档
3. 应答过程：服务器想客户端发送HTTP协议应答包，如果请求的资源包含动态语言内容，服务器会调用解释引擎处理动态内容，并将处理后得到的数据返回给客户端。由客户端解释HTML文档，最终在用户屏幕上渲染显示图形结果
4. 关闭连接：客户端和服务器断开连接

​																**HTTP常用请求方法**

| 方法    | 描述                                                         |
| ------- | ------------------------------------------------------------ |
| GET     | 请求指定的页面信息，并返回实体主体                           |
| POST    | 向指定资源提交数据(如提交表单或者上传文件)，进行处理请求。数据被包含在请求体中，POST请求会导致新资源的建立或已有资源的修改 |
| HEAD    | 类似于GET请求，只不过返回的响应中没有具体的内容，仅用于获取报头 |
| PUT     | 从客户端向服务器传送的数据取代指定的文档内容                 |
| DELETE  | 请求服务器删除指定的页面                                     |
| OPTIONS | 允许客户端查看服务器端的性能                                 |

​														**HTTP状态码**

| 状态码  | 说明                                                         |
| ------- | ------------------------------------------------------------ |
| **1xx** | 表示信息请求收到，继续处理                                   |
| 100     | 继续                                                         |
| 101     | 切换协议                                                     |
| **2xx** | 表示成功返回响应，即行为呗菜狗的接收、理解、采纳             |
| 200     | 确定。客户端已经请求成功                                     |
| 201     | 已创建                                                       |
| 202     | 已接受                                                       |
| 203     | 非权威性信息                                                 |
| 204     | 无内容                                                       |
| 205     | 重置内容                                                     |
| 206     | 部分内容。表明已部分下载一个文件，可以续传损坏的下载，或者将下载拆分为多个并发的流 |
| 207     | 多状态。                                                     |
| **3xx** | 表示重新定向，为了完成请求，必须进一步执行的动作             |
| 301     | 已永久移动。此请求和之后所有的请求都应该转到指定的URL        |
| 302     | 对应移动。对于基于表单的身份验证，此消息通常表示为‘对象已移动’。请求的资源临时驻留在不同的URL。由于重定向有事可能会改变，客户端将来在请求时应该继续使用RequestURL。只有在CacheControl或Expires标题字段中只是，此响应才能够缓存 |
| 304     | 未修改。客户端请求的文档已在其缓存中，文档自缓存依赖尚未被修改过。客户端使用文档的缓存副本，而不从服务器下载文档 |
| 307     | 临时重定向                                                   |
| **4xx** | 表示客户端错误，如请求包含语法错误或者请求无法实现           |
| 400     | 错误的请求                                                   |
| 401     | 访问被拒绝                                                   |
| 403     | 服务器拒绝请求                                               |
| 404     | 服务器找不到指定请求                                         |
| 405     | 用来访问本页面的HTTP谓词不背允许                             |
| 414     | 请求URL太长                                                  |
| 417     | 执行失败                                                     |
| **5xx** | 表示服务器错误，如服务器不能实现一种明显无效的请求           |
| 500     | 内部服务器错误                                               |
| 502     | Web服务器作为网关或代理服务器时，从上游服务器收到了无效响应  |

**[更多状态码可以去菜鸟教程观看](https://www.runoob.com/http/http-status-codes.html)**

### 3.3.WSGI接口

FastCGI使用进程/线程池来处理一连串的请求，这些进程/线程池由FastCGI服务器管理，而不是Web服务器管理

WSGI(服务器网关接口)是Web服务器和Web应用程序或框架之间的一种简单而通用的接口

WSGI中有两种角色：

1. 接受请求的Server(服务器)
2. 处理请求的Application(应用)
3. 它们底层是通过FastCGI沟通的。

> 当服务器收到一个请求后，可以通过Socket把环境变量和一个Callback回调函数传给后端应用，应用在完成页面组装后通过Callback把内容返回给Server，最后Server再将响应返回给Client

#### 3.3.1.定义WSGI接口

WSGI接口只要求Web开发者实现一个函数，就可以响应HTTP请求

```python
def application(environ,start_response):
    start_response('200 ok',[('Content-Type'),'text/html'])
    return [b'<h1>Hello,World!</h1>']

# environ:一个包含了所有HTTP请求信息的字典对象
# start_response:一个发送HTTP响应的函数

'''
整个函数本身并没有涉及任何解析HTTP部分，所以底层Web服务器的解析部分和应用程序逻辑部分进行分离
所以函数本身必须由WSGI服务器来调用，现在很多服务器都符合WSGI规范，如：Apache服务器和Nginx服务器等，Python内部还内置了wsgiref模块，但是只是WSGI的参考实现，也就是不考虑运行效率
'''
```

#### 3.3.2.运行WSGI服务

```python
# 创建一个Views目录
# 创建course.html
<!DOCTYPE html>
<html lang="UTF-8">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>
    明日科技
</title>
<!-- Bootstrap core CSS -->
<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" 
<!-- Documentation extras -->
<style>
body {
    position: relative; /* For scrollspy */
}

/* Keep code small in tables on account of limited space */
.table code {
  font-size: 13px;
  font-weight: normal;
}

/* Inline code within headings retain the heading's background-color */
h2 code,
h3 code,
h4 code {
  background-color: inherit;
}

/* Outline button for use within the docs */
.btn-outline {
  color: #563d7c;
  background-color: transparent;
  border-color: #563d7c;
}
.btn-outline:hover,
.btn-outline:focus,
.btn-outline:active {
  color: #fff;
  background-color: #563d7c;
  border-color: #563d7c;
}

/* Inverted outline button (white on dark) */
.btn-outline-inverse {
  color: #fff;
  background-color: transparent;
  border-color: #cdbfe3;
}
.btn-outline-inverse:hover,
.btn-outline-inverse:focus,
.btn-outline-inverse:active {
  color: #563d7c;
  text-shadow: none;
  background-color: #fff;
  border-color: #fff;
}

/* Bootstrap "B" icon */
.bs-docs-booticon {
  display: block;
  font-weight: 500;
  color: #fff;
  text-align: center;
  cursor: default;
  background-color: #563d7c;
  border-radius: 15%;
}
.bs-docs-booticon-sm {
  width: 30px;
  height: 30px;
  font-size: 20px;
  line-height: 28px;
}
.bs-docs-booticon-lg {
  width: 144px;
  height: 144px;
  font-size: 90px;
  line-height: 140px;
}
.bs-docs-booticon-inverse {
  color: #563d7c;
  background-color: #fff;
}
.bs-docs-booticon-outline {
  background-color: transparent;
  border: 1px solid #cdbfe3;
}

/*
 * Main navigation
 *
 * Turn the `.navbar` at the top of the docs purple.
 */

.bs-docs-nav {
  margin-bottom: 0;
  background-color: #fff;
  border-bottom: 0;
}
.bs-home-nav .bs-nav-b {
  display: none;
}
.bs-docs-nav .navbar-brand,
.bs-docs-nav .navbar-nav > li > a {
  font-weight: 500;
  color: #563d7c;
}
.bs-docs-nav .navbar-nav > li > a:hover,
.bs-docs-nav .navbar-nav > .active > a,
.bs-docs-nav .navbar-nav > .active > a:hover {
  color: #463265;
  background-color: #f9f9f9;
}
.bs-docs-nav .navbar-toggle .icon-bar {
  background-color: #563d7c;
}
.bs-docs-nav .navbar-header .navbar-toggle {
  border-color: #fff;
}
.bs-docs-nav .navbar-header .navbar-toggle:hover,
.bs-docs-nav .navbar-header .navbar-toggle:focus {
  background-color: #f9f9f9;
  border-color: #f9f9f9;
}

/*
 * Homepage
 *
 * Tweaks to the custom homepage and the masthead (main jumbotron).
 */

/* Share masthead with page headers */
.bs-docs-masthead,
.bs-docs-header {
  position: relative;
  padding: 30px 0;
  color: #cdbfe3;
  text-align: center;
  text-shadow: 0 1px 0 rgba(0,0,0,.1);
  background-color: #6f5499;
  background-image: -webkit-gradient(linear, left top, left bottom, from(#563d7c), to(#6f5499));
  background-image: -webkit-linear-gradient(top, #563d7c 0%, #6f5499 100%);
  background-image:      -o-linear-gradient(top, #563d7c 0%, #6f5499 100%);
  background-image:         linear-gradient(to bottom, #563d7c 0%, #6f5499 100%);
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#563d7c', endColorstr='#6F5499', GradientType=0);
  background-repeat: repeat-x;
}

/* Masthead (headings and download button) */
.bs-docs-masthead .bs-docs-booticon {
  margin: 0 auto 30px;
}
.bs-docs-masthead h1 {
  font-weight: 300;
  line-height: 1;
  color: #fff;
}
.bs-docs-masthead .lead {
  margin: 0 auto 30px;
  font-size: 20px;
  color: #fff;
}
.bs-docs-masthead .version {
  margin-top: -15px;
  margin-bottom: 30px;
  color: #9783b9;
}
.bs-docs-masthead .btn {
  width: 100%;
  padding: 15px 30px;
  font-size: 20px;
}

@media (min-width: 480px) {
  .bs-docs-masthead .btn {
    width: auto;
  }
}

@media (min-width: 768px) {
  .bs-docs-masthead {
    padding: 80px 0;
  }
  .bs-docs-masthead h1 {
    font-size: 60px;
  }
  .bs-docs-masthead .lead {
    font-size: 24px;
  }
}
</style>

<!-- Analytics
================================================== -->
</head>
  <body class="bs-docs-home">
    <!-- Docs master nav -->
  <header class="navbar navbar-static-top bs-docs-nav" id="top">
  <div class="container">
    <div class="navbar-header">
      <a href="/" class="navbar-brand">明日学院</a>
    </div>
    <nav id="bs-navbar" class="collapse navbar-collapse">
      <ul class="nav navbar-nav">
        <li>
          <a href="/course.html" >课程</a>
        </li>
        <li>
          <a href="http://www.mingrisoft.com/book.html">读书</a>
        </li>
        <li>
          <a href="http://www.mingrisoft.com/bbs.html">社区</a>
        </li>
        <li>
          <a href="http://www.mingrisoft.com/servicecenter.html">服务</a>
        </li>
        <li>
          <a href="/contact.html">联系我们</a>
        </li>
      </ul>
    </nav>
  </div>
</header>
      <!-- Page content of course! -->
      <main class="bs-docs-masthead" id="content" tabindex="-1">
    <div class="container">
      <div class="jumbotron">
        <h1 style="color: #573e7d">明日课程</h1>
        <p style="color: #573e7d">海量课程，随时随地，想学就学。有多名专业讲师精心打造精品课程，让学习创造属于你的生活</p>
        <p><a class="btn btn-primary btn-lg" href="http://www.mingrisoft.com/selfCourse.html" role="button">开始学习</a></p>
      </div>
    </div>
</main>
</body>
</html>
                                            
# 创建application
def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])     # 响应信息
    file_name = environ['PATH_INFO'][1:] or 'index.html'        # 获取url参数
    HTML_ROOT_DIR = './Views/'  # 设置HTML文件目录
    try:
        file = open(HTML_ROOT_DIR + file_name, "rb")  # 打开文件
    except IOError:
        response = "The file is not found!"     # 如果异常，返回404
    else:
        file_data = file.read() # 读取文件内容
        file.close()            # 关闭文件
        response = file_data.decode("utf-8") # 构造响应数据

    return [response.encode('utf-8')] # 返回数据
# 创建web_server
from wsgiref.simple_server import make_server
from application import app

# 创建一个服务器,ip为空，端口为8000，处理函数为app
httpd = make_server('', 8000, app)
print('Serving HTTP on port 8000...')
# 开始监听HTTP请求
httpd.serve_forever()

                                            

# 运行web_server文件，在浏览器输入127.0.0.1:8000                                            
                                            
```

### 3.4.ORM编程

ORM(对象关系映射)是一种程序设计技术，用于实现面向对象编程语言里不同类型系统的数据直接的转换。

面向对象是在软件工程(耦合、聚合、封装)的基础上发展起来的，而关系数据库是从数学理论发展而来的

数据库和对象的映射如下：

1. 数据库->类
2. 数据行->对象
3. 字段->对象的属性

```python
sql = 'select * from books order by price'
cursor.execute(sql)
data = cursor.fetchall()

# 上面的语句可以替换为

data = BOOK.query.all()
```

**ORM优缺点：**

优点：

1. 数据模型都在一个地方定义，便于更新和维护，也利于重用代码
2. 有很多现成工具，很多功能可以自动完成
3. 业务代码更加简洁
4. 不会写出性能不佳的sql语句

缺点：

1. 不是轻量级的，要花费很多时间学习与设置
2. 不利于复杂查询
3. 开发者无法了解数据库底层，无法定制sql语句

## 4.Web框架基础

### 4.1.什么是Web框架？

Web框架是用来简化Web开发的软件框架，是一些能实现常用功能的Python文件，框架就是一系列工具的集合。

一个典型的框架通常会提供：

1. 管理路由
2. 支持数据库
3. 支持MVC
4. 支持ORM
5. 支持模块引擎
6. 管理会话和Cooies

> ==MVC==是Smalltalk的一种设计模式。Model(模型)用于封装和业务逻辑相关的数据和数据处理的方法，View(视图)是数据的HTML体现，Controller(控制器)负责响应请求
>
> ==MTV==，`M-model`数据模式，`T-template`负责将页面展示给用户，`V-view`业务处理，更新模板中的数据库

> 
>
> ==模板引擎==是为了使用户界面与业务数据分离而产生的，它可以生成特定格式的文档，用于网站的模板引擎一般生成一个标准的HTML文档。
>
> 如：在{{}}中的变量会被替换为变量值，这就可以更好的实现界面与数据分离
>
> ```html
><html>
> <head>
> <title>{{title}}</title>
> </head>
> <body>
>  <h1>Hello,{{username}}!</h1>
> </body>
>    </html>
> ```

### 4.2.常用的Python Web框架

1. Django

   > 拥有世界上最大的社区，最多的包。文档非常完善，而且提供一站式的解决方案，包括缓存、ORM、管理后台、验证、表单处理等，使得开发复杂的由数据库驱动的网站变得简单。但是，Django系统耦合度较高，替换掉内置功能比较复杂，学习比较困难

2. Flask

   > 是一个轻量级别的Web框架。它把Werkzeug和Jinja合在一起，所以很容易被扩展。

3. Tornado

   > 不单单是个框架还是个Web服务器。是为了解决实时服务而诞生的，使用了异步非阻塞IO，所以运行速度非常快

4. FastApI

   > 是一个现代的高性能框架，能够自动生成API

## 5.Flask框架

1. 下载安装Flask框架

```python
pip install flask

'''
当安装 Flask 时，以下配套软件会被自动安装。

Werkzeug 用于实现 WSGI ，应用和服务之间的标准 Python 接口。

Jinja 用于渲染页面的模板语言。

MarkupSafe 与 Jinja 共用，在渲染页面时用于避免不可信的输入，防止注入攻击。

ItsDangerous 保证数据完整性的安全标志数据，用于保护 Flask 的 session cookie.

Click 是一个命令行应用的框架。用于提供 flask 命令，并允许添加自定义 管理命令。
'''
```

2. 默认环境

> 刚开始的时候Flask有许多带有合理缺省值的配置值和惯例。按照惯例，模板和静态文件凡在应用Python源代码树的子目录中，名称分别为==templates==和==static==，可以改变

### 5.1.第一个Flask应用

```python
# 导入Flask类，该类的实例会成为我们的WSGI应用
from flask import Flask
'''
创建该类的一个实例
第一个参数是引用模块或者包的名称，如果使用单一模块，名称为__name__。
模块的名称将会因其作为单独应用启动还是作为模块导入而有不同
这样flask才知道到哪去找模板、静态文件等
'''
app = Flask(__name__)

# 使用route装饰器告诉Flask什么样的URL能触法执行被装饰的函数
# 函数返回需要在用户浏览器中显示的信息。默认内容类型是HTML
@app.route('/')
def index():
    return 'Hello World!'

if  __name__ == '__main__':
    app.run()
    
'''
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
  打开浏览器输入网址就能看见网站内容
'''
```

### 5.2.开启调试模式

```python
# 在Flask对象的run方法里可以设置参数
app.run(
	debug=True, # 开启调试模式，这样更改代码后就不需要重启服务了
	port = 8000,
    host='0.0.0.0' #当运行服务后，你会发现只有自己的电脑能运行，如果您关闭了调试器或信任您网络中的用户，那么可以让服务器被公开访问。 只要在run方法上简单的加上 host='0.0.0.0' 即可:
)
```

### 5.3.HTML转义

> 当返回HTML时，为了防止注入攻击，所有用户提供的值在输出渲染前必须被转义。

```python
# 使用escape()可以手动转义
from markupsafe import escape

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"
```



### 5.4.路由

> 客户端把请求发送给Web服务器后，Web服务器会把请求发送给Flask程序实例。程序实例需要知道对每个URL请求运行那些代码，所以保存了一个URL到Python函数的映射关系。处理URL和函数之间关系的程序称为路由
>
> ![](https://note.youdao.com/yws/public/resource/92933d878935240680c00793fc3e404c/xmlnote/WEBRESOURCE398a19eeada41bf456312baf2fd737b0/437)

```python
# 使用装饰器声明路由
@app.route('/')
def index():
    return 'Hello World!'
```

### 5.5.变量规则

通过把URL的一部分编辑为`<variable_name>`就可以在URL中添加变量标记的 部分会作为关键字参数传递给函数。通过使用 `<converter:variable_name>` ，可以 选择性的加上一个转换器，为变量指定规则。

```python
from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/user/<username>')
def show_user_profile(username):
    # 显示该用户名的用户信息
    return f'用户名是:{username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # 根据ID显示文章，ID是整型数据
    return f'ID是:{post_id}'

if __name__ == '__main__':
    app.run(debug = True)
```

| 转换器类型 | 描述                       |
| ---------- | -------------------------- |
| string     | (默认)接收不包含斜杆的文本 |
| int        | 接受正整数                 |
| float      | 接受征浮点数               |
| path       | 类似于默认。但可以包含斜杆 |
| uuid       | 接受UUID字符串             |

### 5.6.唯一的URL/重定向行为

```python
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
```

`projects` 的 URL 是中规中矩的，尾部有一个斜杠，看起来就如同一个文件 夹。访问一个没有斜杠结尾的 URL （ `/projects` ）时 Flask 会自动进行重 定向，帮您在尾部加上一个斜杠（ `/projects/` ）。

`about` 的 URL 没有尾部斜杠，因此其行为表现与一个文件类似。如果访问这 个 URL 时添加了尾部斜杠（`` /about/ `` ）就会得到一个 404 “未找到” 错 误。这样可以保持 URL 唯一，并有助于搜索引擎重复索引同一页面。

### 5.7.构造URL

url_for()函数用于构建指定函数的URL。它把函数名称作为第一个参数。它可以接受任意个关键字参数，每个关键字参数对应URL中的变量。未知变量将添加到URL中作为查询参数

为什么不在把 URL 写死在模板中，而要使用反转函数 `url_for()`动态构建？

1. 反转通常比硬编码 URL 的描述性更好。
2. 您可以只在一个地方改变 URL ，而不用到处乱找。
3. URL 创建会为您处理特殊字符的转义，比较直观。
4. 生产的路径总是绝对路径，可以避免相对路径产生副作用。
5. 如果您的应用是放在 URL 根路径之外的地方（如在 `/myapplication` 中，不在 `/` 中）， `url_for()` 会为您妥善处理。

```python
'''
url_for(endpoint,values)->str
endpoint (str) – 函数名称
values (Any) – URL规则的变量参数
return type str

重定向函数redirect(location)
location ->一条URL，可以与反转函数一起使用，也可以填入视图函数路径
redirect('/')转到index页面

'''

from flask import Flask,url_for,redirect

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/user/<username>')
def show_user_profile(username):
    # 显示该用户名的用户信息
    return f'用户名是:{username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # 根据ID显示文章，ID是整型数据
    return f'ID是:{post_id}'

@app.route('/login')
def login():
    # 模拟登录流程
    flag = ''
    # 如果登录成功，跳转到首页
    if flag:
        return redirect(url_for('index'))
    return "登录页面"

# 告诉 Flask 正在处理一个请求，其实只是运行了服务器而已
with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('show_post', post_id=2))
    print(url_for('index', username='John  Doe'))

if __name__ == '__main__':
    app.run(debug = True)

```

### 5.8.HTTP方法

缺省情况下，一个路由只回应`GET`请求，可以使用route()装饰器的`methods`参数来处理不同的HTTP方法

```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
```

### 5.9.静态文件

当web需要调用静态文件(一般是 CSS 和 JavaScript 文件)时，可以用反转函数来生成文件路径

```python
url_for('static', filename='style.css')

# /static/style.css
# style.css文件应该在static文件下
```

### 5.11.渲染模板

一般来说HTML模板默认在templates文件夹下，所以在Flask中使用`render_template`函数渲染模板

```python
render_template('temp_name.html',temp_variable=name)

# 第一个参数为渲染的模板名称，第二个参数为模板中变量的值
# 在模板内部可以像使用 url_for() 和 get_flashed_messages() 函数一样访问 config 、 request 、 session 和 g 对象。
```

- 模板变量

  > 在模板中使用{{}}表示一个变量，它是一种特殊的占位符，告诉模板引擎这个位置的值从渲染模板时使用的数据中获取。Jinja2能识别所有类型的变量
  >
  > 如：{{mydict['key']}}

- 过滤器

  > 过滤器是一些可以用来修改和过滤变量值得特殊函数，过滤器和变量用一个|隔开，需要参数的过滤器可以像函数一样使用括号传递
  >
  > 如：Hello,{{name|capitalize}} //变量首字母会大写

  |                    常用过滤器                    |                             说明                             |
  | :----------------------------------------------: | :----------------------------------------------------------: |
  |                       safe                       |                         渲染时不转义                         |
  |                    capitalize                    |           把值得首字母转换为大写，其他字母转为小写           |
  |                      lower                       |                      把值转换成小写形式                      |
  |                      upper                       |                     把值转换为 大写形式                      |
  |                      title                       |               把值每个单词的首字母都转换为大写               |
  |                       trim                       |                      把值的首尾空格去掉                      |
  |                    striptags                     |              渲染之前把值中所有的HTML标签都删掉              |
  | truncate(s,length=255,killwords=False,end='...') | 截取字符串，常用于显示文章摘要。length参数设置截取的长度，killwords参数设置是否截取单词，end参数设置结尾符号 |

- 自定义过滤器

  ```python
  # 先写好一个函数
  def count_length(arg):
  		return len(arg)
  # 再用add_template_filter把函数注册为过滤器
  # 第一个参数为函数名，第二个参数为注册的过滤器名
  app.add_template_filter(count_length,'1')
  
  # 还可以用template_filter()装饰器定义过滤器
  @app.template_filter()
  def count_length(arg):
  		return len(arg)
  ```

  

- 控制结构

  Jinja2提供了很多种控制结构，用来改变模板的渲染流程

  - `{% ... %}`对于语句

  - `{{ ... }}`用于变量打印到模板输出

  - `{# ... #}`对于模板输出中未包含的注释

```python
# 常见的模板
# if控制结构
{% if user %}
Hello,{{user}}
{% else %}
{{user}}
{% endif %} #表示结束

# for控制结构，能跟python一样使用序列的相关函数
<ul>
{% for comment in comments %}
<li>{{comment}}</li>
{% endfor %}
</ul>

# Jinja2还支持宏(类似于函数)
{% macro render_comment(comment) %}
<li>{{comment}}</li>
<% endmacro %> # 定义一个宏
{% for comment in comments %}
{{render_comment(comment)}} # 调用宏
{% endfor %}

# 还支持导入
{% import 'macros.html' as macros %}
<ul>
{% for comment in comments %}
{{macros.render_comment(comment)}}
{% endfor %}
</ul>

# 模板继承，类似于类继承
# 创建base.html文件
<!DOCTYPE html>
<html lang="en">
<head>
   {% block head %}
    <meta charset="UTF-8">
    <title>{% block title %}{% endblock %}Title</title>
    {% endblock %}
</head>
<body>
    {% block body %}
    {% endblock %}
</body>
</html>

# 创建子模块
{% extends 'base.html' %} # 继承父模块内容
{% block title %}index{% endblock %} # 网页标题为indexTitle
{% block head %}
{{super()}}  # 获取父模块内容
{% endblock %}
{% block body %}
<h1>Hello</h1>  # 网页主体内容为Hello
{% endblock %}

# 局部模板
# 当各个独立模板中使用同一块HTML时，可以把这部分代码抽离出来，存储到局部模板中
# 为了和普通模板分开，局部模板的命名通常是以下划线开始的
# 导入局部模板
{% include '_banner.html' %}
```

### 5.12.Web表单

> 表单是用户跟Web应用实现交互的基本元素，Flask不会自己处理表单，但Flask-WTF扩展允许用户在Flask应用中使用WTFForms包，从而使得表单和处理表单变得非常轻松

```python
# 安装WTForms
pip install flask-wtf
```

- CSRF保护和验证

  > CSRF全称为Cross Site Resquest Forgery,即跨站请求伪造。CSRF通过第三方伪造表单数据，POST到服务器上。WTForms在渲染表单时会生成一个独一无二的token，该taken将在POST请求中随表单数据一起传递，并且在表单被接受前进行验证。taken的值取决于存储在用户对话(cookies)中的一个值，该值会在30分钟后过时
  >
  > 为了更好的实现CSRF保护，Flask-WTF需要程序设置一个密钥，通过密钥生成加密令牌，再用令牌验证请求中表单数据的真伪

  ```python
  # 设置密钥
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'mrsoft'
  
  # config方法可用来存储框架，扩展和程序本身的配置变量
  # SECRET_KEY配置变量时通用密钥
  ```

- 表单类

  ```python
  from flask_wtf import FlaskForm
  from wtforms import StringField,PasswordField,SubmitField
  from wtforms.validators import InputRequired
  
  class NameFrom(FlaskForm):
      name = StringField('请输入姓名',validators=[InputRequired()])
      password = PasswordField('请输入密码',validators=[InputRequired()])
      submit = SubmitField('Submit')
  ```

  ​													**WTForms支持的HTML标准字段**

  |      字段类型       |                说明                 |
  | :-----------------: | :---------------------------------: |
  |     StringField     |              文本字段               |
  |    TextAreaField    |            多行文本字段             |
  |    PasswordField    |            密码文本字段             |
  |     HiddenField     |            隐藏文本字段             |
  |      DateField      |   文本字段，值为datetime.date格式   |
  |    DateTimeField    | 文本字段，值为datetime.datetime格式 |
  |    IntegerField     |         文本字段，值为整数          |
  |    DecimalField     | 文本字段，值为datetime.Decimal格式  |
  |     FloatField      |         文本字段,值为浮点数         |
  |    BooleanField     |       复选框，值为True和False       |
  |     RadioField      |            一组单选按钮             |
  |     SelectField     |              下拉列表               |
  | SelectMultipleField |        下拉列表，可选多个值         |
  |      FileField      |            文件上传按钮             |
  |     SubmitField     |            表单提交按钮             |
  |      FormField      |   把表单作为字段嵌入另一个表单内    |
  |      FieldList      |         一组指定类型的字段          |

​																**WTForms内置的验证函数**

|  字段类型   |                       说明                       |
| :---------: | :----------------------------------------------: |
|    Email    |                 验证电子邮件地址                 |
|   EqualTo   | 比较两个字段的值，常用于要求输入两次密码进行确定 |
|  IPAddress  |                 验证IPv4网络地址                 |
|   Length    |               验证输入字符串的长度               |
| NumberRange |             验证输入的值在数字范围内             |
|  Optional   |            无输入值时跳过其他验证函数            |
|  Required   |                 确保字段中有数据                 |
|   Regexp    |             使用正则表达式验证输入值             |
|     URL     |                     验证URL                      |
|    AnyOf    |              确保输入值在可选列表中              |

- **实例**

  ```python
  # 创建HTML模板
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <link rel="stylesheet" href="/static/css/bootstrap.css">
      <script src="/static/js/jquery.js"></script>
      <script src="/static/js/bootstrap.js"></script>
  </head>
  <body>
  <nav class="navbar navbar-expand-sm bg-primary navbar-dark">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link" href="#">首页</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">明日学院</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">明日图书</a>
      </li>
      <!-- Dropdown -->
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#"
            id="navbardrop" data-toggle="dropdown">
          关于我们
        </a>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#">公司简介</a>
          <a class="dropdown-item" href="#">企业文化</a>
          <a class="dropdown-item" href="#">联系我们</a>
        </div>
      </li>
    </ul>
  </nav>
  
  <div class="jumbotron">
    <form action="" method="post">
        <div class="form-group">
        {{ form.name.label }}
        {{ form.name(class="form-control")}}
        {% for err in form.name.errors %}
            <p style="color: red">{{ err }}</p>
        {% endfor %}
        </div>
        <div class="form-group">
        {{ form.password.label }}
        {{ form.password(class="form-control") }}
        {% for err in form.password.errors %}
           <p style="color: red">{{ err }}</p>
        {% endfor %}
        </div>
        {{ form.csrf_token }}
        {{ form.submit(class="btn btn-primary") }}
    </form>
  </div>
  </body>
  </html>
  
  # 创建表单类
  from flask_wtf import FlaskForm
  from wtforms import StringField, PasswordField,SubmitField
  from wtforms.validators import DataRequired,Length
  
  class LoginForm(FlaskForm):
      """
      登录表单类
      """
      name = StringField(label='用户名', validators=[
          DataRequired("用户名不能为空"),
          Length(max=8,min=3,message="用户名长度必须大于3且小于8")
      ])
      password = PasswordField(label='密码', validators=[
          DataRequired("密码不能为空"),
          Length(max=10, min=6, message="用户名长度必须大于6且小于10")
      ])
      submit = SubmitField(label="提交")
      
      
  # 创建主函数
  from flask import Flask ,url_for,redirect, render_template
  from models import LoginForm
  
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'mrsoft'
  
  
  @app.route('/login', methods=['GET', 'POST'])
  def login():
      """
      登录页面
      """
      form = LoginForm()  # 实例化表单对象
      if form.validate_on_submit():
          username = form.name.data
          password = form.password.data
          if username== "andy" and password == "mrsoft":
              return redirect(url_for('index'))
      return render_template('login.html',form=form) # 渲染页面和表单
  
  @app.route('/')
  def index():
      """
      首页
      """
      name = "明日学院"
      message = """
          明日学院，是吉林省明日科技有限公司倾力打造的在线实用技能学习平台，该平台于2016年正式
          上线，主要为学习者提供海量、优质的课程，课程结构严谨，用户可以根据自身的学习程度，自主安
          排学习进度。我们的宗旨是，为编程学习者提供一站式服务，培养用户的编程思维。
      """
      return render_template("index.html",name=name,message=message)
  
  if __name__ == '__main__':
      app.run(debug=True)
  
  ```

### 5.13.蓝图

蓝图是一个存储操作方法的容器，当它被注册到一个应用后，这些操作方法就可以被调用。蓝图很好的简化了大型应用的工作方式，并给Flask扩展提供了在应用上注册操作的核心方法。蓝图对象不能独立运行，必须将他注册到一个应用对象上

使用蓝图的原因：

1. 一个应用可以分解为多个蓝图的集合。这对大型应用是理想的，一个项目可以实例化一个应用对象，初始化几个扩展，并注册多个蓝图
2. 对URL前缀/子域名，可以在应用上注册一个蓝图。URL前缀/子域名中的参数即成为这个蓝图下所有视图函数的共同视图参数(默认情况下)
3. 在一个应用中，用不同的URL规则可以多次注册一个蓝图
4. 通过蓝图可提供模板过滤器、静态文件、模板和其他功能。一个蓝图不一定要实现应用或者视图函数
5. 初始化一个Flask扩展时，需要注册一个蓝图

> 视图相关联的名称亦称为 *端点* ，缺省情况下，端点名称与视图函数名称相同。
>
> 前文被加入应用工厂的 `hello()` 视图端点为 `'hello'` ，可以使用 `url_for('hello')` 来连接。如果视图有参数，后文会看到，那么可使用 `url_for('hello', who='World')` 连接。
>
> 当使用蓝图的时候，蓝图的名称会添加到函数名称的前面。上面的 `login` 函数 的端点为 `'auth.login'` ，因为它已被加入 `'auth'` 蓝图中。

```python
# 蓝图在python包下的__init__文件里面创建
# 创建home蓝图，hone文件夹下的__init__文件
from flask import Blueprint

# home = Blueprint('home', __name__, url_prefix='/auth')
# 也可以直接在创建时加入URL
home = Blueprint("home",__name__)

# 创建蓝图
@home.route('/')
def index():
   return  '<h1>Hello Home!</h1>'

# 创建admin蓝图，admin文件夹下的__init__文件
from flask import Blueprint

# 创建蓝图，第一个参数为蓝图名，第二个为蓝图所在的模块名
admin = Blueprint("admin",__name__)

@admin.route('/')
def index():
   return  '<h1>Hello Admin!</h1>'

# 绑定蓝图，在与上两文件夹同级下创建run.py文件
from flask import Flask
from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app = Flask(__name__)
# 注册蓝图
app.register_blueprint(home_blueprint, url_prefix='/home')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
# 第一个参数为蓝图名称，第二个参数为蓝图的URL前缀

if __name__ == '__main__':
    app.run(debug=True)

```

### 5.14.重定向和错误

```python
from flask import abort, redirect, url_for,Flask

app = Flask(__name__)
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    # 使用 abort() 可以 更早退出请求，并返回错误代码
    abort(404)

if __name__ == '__main__':
    app.run(debug=True)
    

# 使用 errorhandler() 装饰器可以定制出错页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
```



## 6.Flask框架进阶

进阶知识包括Flask的请求和响应、高级模板技术以及和数据库相关的操作

### 6.1.Flask请求

使用Request请求对象可以获取请求中各个字段的值

​																		**Request对象的常用属性和方法**

|  属性或方法  |                          说明                          |
| :----------: | :----------------------------------------------------: |
|     form     |          一个字典，存储请求提交的所有表单字段          |
|     args     |     一个字典，存储通过URL查询字符串传递的所有参数      |
|    values    |               一个字典，form和args的合集               |
|   cookies    |            一个字典，存储所有请求的cookies             |
|   headers    |          一个字典，存储所有请求的所有HTTP首部          |
|    files     |            一个字典，存储请求上传的所有文件            |
|  get_data()  |                 返回请求主体缓冲的数据                 |
|  get_json()  |    返回一个Python字典，包含解析请求主体后得到的JSON    |
|  blueprint   |               处理请求的Flask蓝本的名称                |
|   endpoint   |               处理请求的Flask的端点名称                |
|    method    |             HTTP请求方法，可以是GET或POST              |
|    scheme    |                 URL方案（http或https）                 |
| is_secure()  |       通过安全的连接(https)发送请求时，返回True        |
|     host     | 请求定义的主机名，如果客户端定义了端口号，还包括端口号 |
|     path     |                     URL的路径部分                      |
| query_string |         URL的查询字符串部分，返回原始二进制值          |
|  full_path   |               URL的路径和查询字符串部分                |
|     url      |                  客户端请求的完整URL                   |
|   base_url   |              同url，但没有查询字符串部分               |
| remote_addr  |                     客户端的IP地址                     |
|   environ    |                 请求的元素WSGI环境字典                 |

#### 6.1.1.获取get请求参数

```python
# 获取http://127.0.0.1:5000/?name=ande&age=18的name与age值

from flask import Flask,request

app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get('name')
    age = request.args.get('age')
    message = f'姓名：{name}\n 年龄：{age}'
    return message

if __name__ == "__main__":
    app.run(debug=True)
```

#### 6.1.2.获取POST请求参数

```python
# 获取表单提交数据
from flask import Flask,request,render_template

app = Flask(__name__)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        message = f'用户名是:{username}</br>密码是:{password}'
        return message

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

    
# 获取表单提交的文件
import os
import uuid

from flask import send_from_directory
from flask import Flask,request,render_template,redirect,url_for

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path,'uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """
    判断上传文件类型是否允许
    :param filename: 文件名
    :return: 布尔值True或False
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def random_file(filename):
    """
    生成随机文件
    :param filename: 文件名
    :return: 随机文件名
    """
    # 获取文件后缀
    ext = os.path.splitext(filename)[1]
    # 使用uuid生成随机字符
    new_filename = uuid.uuid4().hex+ext
    return new_filename

@app.route('/upload',methods=['GET','POST'])
def upload():
    """
    头像上传表单页面
    :return:
    """
    if request.method == 'POST':
        # 接受头像字段
        avatar = request.files['avatar']
        # 判断文件是否上传，已经上传文件类型是否正确
        if avatar and allowed_file(avatar.filename):
            # 生成一个随机文件名
            filename = random_file(avatar.filename)
            # 保存文件
            avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename))

    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    显示上传头像
    :param filename: 文件名
    :return: 真实文件路径
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == '__main__':
    app.run(debug=True)

```

#### 6.1.3.请求钩子

有时需要对请求进行预处理(preprocessing)和后处理(postprocessing),这时可以使用Flask提供的请求钩子(Hook),以注册在请求处理的不同阶段执行的处理函数(或称为回调函数，即Callback)

请求钩子：在执行视图函数前后执行的一些函数，用户可以在这些函数里面做一些操作

Flask利用装饰器提供钩子：

1. before_first_request:在处理第一个请求前执行，如链接数据库操作
2. before_request:在每次请求前执行，如权限校验
3. after_request:每次请求之后调用，前提是没有未处理的异常抛出
4. teardown_request:在每次请求之后调用，即使有未处理的异常抛出

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    print('视图执行中')
    return 'index page'

@app.before_first_request
def before_first_request():
    print('before_first_request')

@app.before_request
def before_request():
    print('before_request')

@app.after_request
def after_request(response):
    print('after_request')
    return response

@app.teardown_request
def teardown_request(error):
    print('teardown_request:error %s'%error)

if __name__ == '__main__':
    app.run(debug=True)
```

### 6.2.Flask响应

#### 6.2.1.Response响应对象

响应在Flask中使用Response对象表示，响应报文大部分内容由服务器处理，大多数情况下只负责返回主体内容。

当你在浏览器输入一个网址时，Flask会先判断是否可以找到与请求URL相匹配的路由，如果没有则返回404响应。如果找到，则调用相应的视图函数。视图函数的返回值构成了响应报文的主体内容，当请求成功时，返回状态码默认为200.

视图函数可以返回最多由三个元素构成的元组：响应主体、状态码和首部字段。

1. 最常见的响应只包含主体内容

   ```python
   @app.route('/index')
   def index():
   	return render_template('index.html')
   ```

2. 还可以返回带状态码的形式

   ```python
   @app.errorhandler(404)
   def index(e):
   	return render_template('404.html')
   ```

3. 有时需要附加或修改某个首部字段

   ```python
   # 生成状态码为3xx的重定向响应，需要将首部中的Location字段设置为重定向的目标URL
   @app.route('/index')
   def index():
   	return '',302,{'Location','http://www.mingrisoft.com'}
   ```

#### 6.2.2.响应格式

在HTTP响应中，数据可以通过多种格式传输。大多数情况下使用HTML格式，这也是Flask中的默认设置。不同的响应数据需要设置不同的MIME类型，MIME类型在首部的Content-Type字段中定义。

```python
# 默认的HTML类型
Content-Type:text/html;charset=utf8
```

当需要使用其他格式时，可以通过使用Flask提供的make_response()方法生成响应对象，传入响应主体作为参数，然后使用响应对象的mimetype属性设置MIME类型

```python
from flask import Flask,make_response

app = Flask(__name__)

@app.route('/index')
def index():
	response = make_response('Hello,World')
	response.mimetype = 'text/plain'
	return response
```

常用的数据格式有：

- [x] 纯文本：text/plain
- [x] HTML：text/html
- [x] XML：application/xml
- [x] JSON：application/json

#### 6.2.3.Cookie和Session

**1. Cookies对象**

​		HTTP是无状态协议。一次请求响应结束后，服务器不会留下任何关于对方状态的信息。所以就有了Cookie技术，Cookie技术通过在请求和响应报文中添加Cookie数据来保护客户端的状态

​		Cookie指Web服务器为了存储某些数据(如用户信息)而保存在浏览器上的小型文本数据。浏览器会在一定时间内保存它，并在下一次向同一个服务器发送请求时附带这些数据。Cookie通常被用来进行用户会话管理

​		在Flask中，使用Response类提供的set_cookie()方法可以在响应中添加一个cookie，首先使用make_response方法手动生成一个响应对象，传入响应主体作为参数。

​															**内置的Response类的常用属性和方法**

| 属性或方法  |                            说明                             |
| :---------: | :---------------------------------------------------------: |
|   headers   | 一个Werkzeug的headers对象，表示响应首部，可以像字典一样操作 |
|   status    |                            状态                             |
| status_code |                      状态码，文本类型                       |
|  mimetype   |                          MIME类型                           |
| set_cookie  |                       用来设置cookie                        |
|  get_json   |                     解析是否为JSON数据                      |
|   is_json   |                     判断是否为JSON数据                      |

​													**Cookie选项的常用属性说明**

|   属性   |                             说明                             |
| :------: | :----------------------------------------------------------: |
|   key    |                         cookie的名称                         |
|  value   |                          cookie的值                          |
| max_age  | cookie被保存的世界，单位为秒。默认在用户会话结束(关闭浏览器)过期 |
| expires  |         具体的过期时间，一个datetime对象或UNIX时间戳         |
|   path   |        下载cookie时只有给定的路径可用，默认为整个域名        |
|  domain  |                     设置cookie可用的域名                     |
|  secure  |             如果为True，只有通过HTTPS才可以使用              |
| httponly |          如果为True，禁止客户端javaScript获取cookie          |

```python
from flask import Flask,request,render_template,make_response

app = Flask(__name__)

@app.route('/')
def index():
    # 判断Cookie是否存在
    if request.cookies.get('username'):
        return '欢迎来到首页!'
    else:
        return '请先登录!'

@app.route('/login',methods=['GET','POST'])
def login():
    # 验证表单数据
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'mrsoft' and password == 'mrsoft':
            # 如果用户名和密码正确，将用户名写入Cookie
            response = make_response(('登录成功!'))    # 获取response对象
            response.set_cookie('username', username) # 将用户名写入Cookie
            return response # 返回response对象
    return render_template('login.html') # 渲染表单页面


@app.route('/logout')
def logout():
    response = make_response(('退出登录!'))
    # 设置Cookie过期时间为0，即删除Cookie
    response.set_cookie('username', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)

```

**2. Session对象**

​	因为在浏览器中手动添加和修改cookie很容易，所处Flask提供了Session对象以对Cookie数据加密存储

​	Session指用户会话，又称对话，即服务器和客户端/浏览器之间或桌面程序和用户之间建立的交互活动

​	Session是一种持久网络协议，通过在用户端和服务器端之间创建关联，起到交换数据包的作用机制。Session在不包含会话层(UDP)或者是无法长时间驻留会话层(http)的传输协议中，会话的维持需要依靠数据参数中的高级别程序

​	在Flask中，Session对象用来加密Cookie。默认情况下，它会把数据存储在浏览器上一个名为Session的cookie李。Session通过密钥对数据进行签名以加密数据，因此需要先设置一个密钥。

```python
# 设置密钥
app.secret_key = 'asjoaisjdas45as6d4a8sd7'
```

```python
# 使用session判断用户是否登录(在上面代码基础上修改)
from flask import Flask,request,render_template,make_response,session,redirect,url_for

app = Flask(__name__)
app.secret_key = 'mrsoft12345678' # 设置秘钥

@app.route('/')
def index():
    if session.get('logged_in'):
        return '欢迎来到首页!'
    else:
        return '请先登录!'

@app.route('/login',methods=['GET','POST'])
def login():
    # 验证表单数据
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'mrsoft' and password == 'mrsoft':
            session['logged_in'] = True  # 写入session
            return redirect(url_for('index'))
    return render_template('login.html') # 渲染表单页面

@app.route('/logout')
def logout():
    session.pop('logged_in')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

```

### 6.3.消息闪现

在开发过程中，经常需要提示用户操作成功或操作失败，针对这种需求，Flask提供了一个非常有用的flask()函数，可以用来闪现需要显示给用户的信息

```python
# 语法格式
flask(message,category)

'''
message：消息内容
category：消息类型，用于对不同的消息内容分类处理

通过flash函数发送的信息会存储在session对象中，所以需要为程序设置密钥
可以通过secret_key属性或配置变量SECRET_KEY进行设置
'''

# 创建login.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
    	# 定义不同消息类型的格式
        .error { color: red }
        .success { color: blue}
    </style>
</head>
<body>
    <div style="padding:20px">
    	# 使用get_flashed_messages(with_categories=true)获取消息列表
        # 用with限制messages变量的作用域
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            <ul class=flashes>
            {% for category, message in messages %}
              <li class="{{ category }}">{{ message }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
        <form action="" method="post">
            <div>
                <label for="username">用户名</label>
                <input type="text" id="username" name="username" value="">
            </div>
            <div>
                <label for="password">密&nbsp;&nbsp;&nbsp;码</label>
                <input type="password" id="password" name="password" value="">
            </div>
            <button type="submit" class="btn btn-primary">提交</button>
        </form>
    </div>
</body>
</html>

# 创建run.py
from flask import Flask,request,render_template,redirect,url_for,flash

app = Flask(__name__)
app.secret_key = 'mrsoft12345678' # 设置秘钥

@app.route('/login',methods=['GET','POST'])
def login():
    # 验证表单数据
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'mrsoft' and password == 'mrsoft':
            flash('恭喜您登录成功','success')
        else:
            flash('用户名或密码错误', 'error')
        return redirect(url_for('login'))
    return render_template('login.html') # 渲染表单页面

if __name__ == '__main__':
    app.run(debug=True)

```





