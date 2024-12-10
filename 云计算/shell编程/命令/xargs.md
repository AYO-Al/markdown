`xargs`命令是将标准输入转换为命令行参数，默认的命令是 echo，这意味着通过管道传递给 xargs 的输入将会包含换行和空白，不过通过 xargs 的处理，换行和空白将被空格取代。

**xargs命令默认执行echo命令**

为什么有了管道还需要这个命令？这是因为很多命令不支持管道，所以需要`xargs`命令来接收命令的输出来当下一个命令的参数。

命令格式：

```bash
xargs [选项]  # xargs命令一般和管道一起使用
```

- 常用参数

| 参数 | 说明                                   |
| ---- | -------------------------------------- |
| -d   | 指定分隔符                             |
| -i   | 将前面的就过用{}代替，一般是一行行传递 |
| -n   | 指定每行的最大参数量                   |

## 多行与单行输出转换

```bash
[root@192 test]# echo {1..3}|xargs
1 2 3
[root@192 test]# echo {1..3}|xargs -n 1
1
2
3

# 多行变单行
xargs < test.txt
```

## 分割字符

```bash
[root@192 test]# echo "asdasxasdhajsdxasda" |xargs -d "x"
asdas asdhajsd asda

```

## 指代变量

```bash
[root@192 test]# echo `seq 10`|xargs -i touch {}
# 因为-i参数{}指代内容是一行一行的
# 所以这条命令会创建一个"1 2 3 4 5 6 7 8 9 10"的文件
```

