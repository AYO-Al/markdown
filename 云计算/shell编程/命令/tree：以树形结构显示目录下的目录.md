`tree`在中文中的意思是树，功能是以树状图列出指定目录下的所有内容，包括所有文件、子目录及子目录中的目录和文件。

- 语法格式

  ```bash
  tree [option] [directory]
  ```

如果命令不带任何选项和目录，那么默认会显示当前目录的目录结构。

- 常用选项

| 选项 | 说明                                                         |
| ---- | ------------------------------------------------------------ |
| -a   | 显示所有目录，包括隐藏文件                                   |
| -d   | 只显示目录                                                   |
| -f   | 全部显示全路径                                               |
| -i   | 不显示树枝                                                   |
| -L   | 设置显示的层级                                               |
| -F   | 在执行文件，目录，Socket，符号连接，管道名称名称，各自加上"*","/","=","@"," |

- 使用案例

`-f`选项有个有意思的地方，那就是如果命令后不带目录，使用`-f`选项后目录会以`.`开头，如果带了目录，那么会以后面的目录替换这个`.`

```bash
# 不带目录
[root@192 test]# tree -f
.
├── ./a.sh
├── ./dump.sh
└── ./tt
    └── ./tt/c.sh
# 带目录
[root@192 test]# tree -f $PWD
/root/test
├── /root/test/a.sh
├── /root/test/dump.sh
└── /root/test/tt
    └── /root/test/tt/c.sh
```

`-f`选项一般和`-i`选项一起使用，用来获取目录下所有完整路径

```bash
[root@192 test]# tree -fi $PWD
/root/test
/root/test/a.sh
/root/test/dump.sh
/root/test/tt
/root/test/tt/c.sh
```

也可以加上`-F`选项，用来区分文件和目录

```bash
[root@192 test]# tree -fiF $PWD
/root/test
/root/test/a.sh
/root/test/dump.sh
/root/test/tt/
/root/test/tt/c.sh
```

