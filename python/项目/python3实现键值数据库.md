# 1.实验简介

## 1.1.实验来源

本课程核心部分来自[《500 lines or less》](https://github.com/aosabook/500lines/tree/master/data-store)项目，作者是来自 Countermeasure 的合唱歌手 Taavi Burns，也曾在 IBM 以及多家创业公司任职 。项目代码使用 MIT 协议，项目文档使用 http://creativecommons.org/licenses/by/3.0/legalcode 协议。

本实验学习于蓝桥云课[《Python3实现键值数据库》]([Python3 实现键值数据库_Python - 蓝桥云课 (lanqiao.cn)](https://www.lanqiao.cn/courses/614))，感兴趣可以前往学习



## 1.2.实验简介

本实验将通过理解一个操作类似于 Redis ，存储理念来自于 CouchDB 的键值数据库的源代码来学习如何做数据库的数据存储，体会使用不可变数据结构的优点。



## 1.3.实验知识点

本项目完成过程中，我们将学习：

1. 二叉树数据的持久化存储与读取
2. 分层对数据库进行设计
3. 使用Python的内置方法将数据结构的操作封装为键值操作



## 1.4.使用版本

- Xfce终端(Linux)
- python3.5
- portalocker-1.2.1
- nose-1.3.7



# 2.实验环境

进入Linux，选好项目目录，直接通过`wget`获取DBDB源代码，同时为了避免本地环境的影响，需要安装虚拟环境，在虚拟环境中操作本次实验

```bash
$ cd /home/shiyanlou/Code
$ sudo pip3 install virtualenv
$ virtualenv --python=python3.5 env
$ source env/bin/activate
$ git clone https://github.com/aosabook/500lines.git
$ unzip dbdb-code.zip
$ cd dbdb-code
$ pip3 install -r requirements.txt
$ cd ../
$ sudo env/bin/easy_install-3.5 dbdb-code #安装 DBDB
```



# 3.相关简介

键值数据库属于 NoSQL 数据库，Redis 是其中的典型代表。本课程所讲解的数据库，其存储数据的核心理念参照 CouchDB （沙发DB），大概也是出于这个原因，所以它叫狗床DB（Dog Bed Database），可能没沙发那么舒适，但也足够温暖。

狗床DB 针对电脑死机、崩溃、异常等状况下数据没有保存而造成的数据丢失，它同时也避免了在内存中存储过多数据，使得你的程序能够使用超出内存大小的数据。

之后皆以 DBDB 来简称狗床DB。



## 3.1.DBDB诞生背景

Taavi Burns：还记得第一次写程序卡在一个 BUG 上时的情景，那时我正运行自己刚写好的 BASIC 程序，不知道为什么屏幕上有些像素点一闪一闪的，然后程序就中止了。我回过头来查看自己的代码，发现代码最后几行竟然消失了。

正巧我妈妈的一个朋友会编程，交流了一下后就找到问题出在哪了。程序太大以至于占了显存。一旦屏幕清空，我的程序就直接被截断了。

自此之后，我就非常注意内存分配的问题了，我学习了关于指针的知识，知道了如何使用 malloc 分配内存，还学习了数据结构是如何存储在内存上的，你必须非常小心地应对这些内存上的数据，一旦修改了不该修改的地方，你的程序会崩溃而且可能需要花很长时间来调 BUG 。

一些年过去了，我遇到了一门面向并发程序设计的语言 Erlang，原来进程间通信并不一定要复制数据，所有的数据结构都是不可变的。之后我又学习了 Clojure 中的不可变数据结构，渐渐沉迷于此道。

2013 年的时候我阅读了 CouchDB 的源代码，他的设计理念，对于复杂数据的管理机制都让我由衷的认同和欣赏。我认识到使用不可变的数据结构设计系统会是一个不错的主意，所以就有了 DBDB 和这篇文档（500L 上的原文档）。

当我实现可变的二叉树时遇到了不少麻烦，当你对数据的一部分做出改变时你不知道它会不会影响到其它部分，需要考虑的边界情况很多，但是更可怕的是有些情况你自己也想不到，简直是一团乱。但是当我改用不可变的数据结构后，麻烦几乎都消失了，程序不那么容易出 BUG 了。我再一次认识到使用不可变的数据结构会使开发和维护程序更加容易。



# 4.DBDB初体验

DBDB既可以在代码中使用，也可在命令行中使用。

命令行用法如下：

```bash
python -m dbdb.tool DBNAME get KEY          
#获得键值
python -m dbdb.tool DBNAME set KEY VALUE    
#设置键值
python -m dbdb.tool DBNAME delete KEY       
#删除键值
```

