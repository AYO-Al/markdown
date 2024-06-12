在Linux中编写Shell脚本，当脚本中有命令执行失败，我们又没有写相对于的判断条件时，脚本并不会向其他语言一样自动退出，而是忽略执行失败的命令继续向下执行，这可能会导致很多错误，增加我们排错的难度、浪费我们的时间。

那是不是我们就只能对每一条可能执行出错的命令使用`$?`进行条件判断呢？当然不是，在脚本编写中。我们可以在文件开头写上

```bash
set -e
```

这代表着在脚本中有命令执行失败时退出程序，避免继续执行错误的操作。例如：

```bash
$ cat test.sh
#!/bin/bash

set -e # 开启退出模式

cp /tmp/foo /tmp/bar # 假设/tmp/foo不存在，这个命令会失败

echo "Copy successful" # 这个语句不会执行，因为上一个命令已经退出了

$ bash test.sh 
cp: cannot stat '/tmp/foo': No such file or directory 
```



set命令是Linux系统中的一个内置变量，用来设置和取消设置shell变量和选项，。它通常用在shell脚本中，用来配置环境和控制脚本的行为。常见的用法除了上述的`set -e`外，还有以下几点：

- `-x`选项可以显示每一行脚本执行时的命令和参数，跟`sh -x`相同，用于调试脚本。例如：

  ```bash
  $ cat test.sh
  #!/bin/bash
  
  echo "Hello World"
  $ bash -x test.sh
  + echo 'Hello World'
  Hello World
  ```

  

set也能定义变量，跟export类似，但不同的是set只定义当前shell的变量，而export是定义环境变量。例如：

```bash
$ set foo=bar
$ echo $foo
bar
$ bash # 开启一个子shell
$ echo $foo

$ exit # 退出子shell
$ export foo=bar # 用export指令定义变量
$ bash # 开启一个子shell
$ echo $foo
bar
```

