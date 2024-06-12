find命令在Linux中常用的用于查找目录和文件，同时也可以调用其他命令执行相应的操作的命令。十分重要

- 语法格式

  ```bash
  find [path] [expression]
  # path为要查找的路径，绝对路径和相对路径都行
  # expression是要执行的操作
  ```

- 常用操作

| 参数选项               | 说明                                                         |
| ---------------------- | ------------------------------------------------------------ |
| -maxdepth levels       | 查找的最大目录级数                                           |
| -mtime [-n\|n\|+n]     | 按照文件的修改时间查找<br>-n：表示文件修改在n天内<br>n：表示距离现在几天<br>+n：表示文件修改在n天以前 |
| -atime                 | 按照文件的访问时间来查找                                     |
| -ctime                 | 按照文件的状态改变时间来查找                                 |
| -mmin                  |                                                              |
| -amin                  |                                                              |
| -cmin                  | 跟上面三个意思一天，但单位为分钟                             |
| -size [+-]size[cwbkMG] | 按文件大小查找，支持使用 `+` 或 `-` 表示大于或小于指定大小，单位可以是 `c`（字节）、`w`（字数）、`b`（块数）、`k`（KB）、`M`（MB）或 `G`（GB）。 |
| -name                  | 按照名字查找，仅支持*、？、[]等特殊通配符。**使用通配符时用双引号引起来，否则会报错** |
| -user                  | 按照所属者进行查找                                           |
| -group                 | 按照所属组进行查找                                           |
| -newer                 | 查找更改时间比指定文件新的文件                               |
| -path pattern          | 指定路径样式，配合-prune排除指定目录                         |
| -type                  | 按文件类型查找，可以是 `f`（普通文件）、`d`（目录）、`l`（符号链接）、s（套接字文件）等。 |
| -regex pattern         | 对路径进行正则                                               |
| -exec                  | 对匹配的文件执行shell命令                                    |
| -prune                 | 指定不在某个目录查找                                         |
| -delete                | 删除匹配文件                                                 |
| ！                     | 取反                                                         |
| -a                     | 交集                                                         |
| -o                     | 并集                                                         |

## 查找文件并删除

```bash
find . -name "1.*" -exec rm -rf {} \;
# {} 指代前面匹配的文件

find . -name "1.*" -delete
```

## 删除全部文件，但排除部分文件

```bash
find . -type f ! -name "10.txt" -exec rm -rf {} \;
# 删除全部文件，但排除10.txt

find . -type f ! \( -name "10.txt" -o -name "9.txt" \) -exec rm -rf {} \;
# 也可以用()括起来，这样就不用使用多个！取反了
# 但()在shell中有特殊意思，所以要使用转义
```

## 删除1分钟前创建大于170字节的文件

```bash
find . -size +170c -cmin +1 |xargs rm -rf {}
```

## 排除某个路径

```bash
[root@192 ~]# find . -path "./a/b" -prune -o -print
.
./.dbus
./.dbus/session-bus
./.local
./.pki
./.pki/nssdb
./.ssh
./ts
./a
./a/1.txt
./9.txt

# -o后必须接-print参数，不然会多输出一个-path匹配的路径
[root@192 ~]# find . -path "./a/b/c" -prune -o -name "1.txt" -print
./a/b/1.txt
./a/1.txt
```

