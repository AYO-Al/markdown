当我们想在Linux任何一个位置都能直接运行脚本或程序时，就需要设置相对应的环境变量

Linux与Windows一样可以设置环境变量，用来存储一些全局性的配置信息的变量。与Windows不同的是，Linux环境变量时区分大小写的，而Windows是不区分的

#### Linux环境变量的分类

- 按照生命周期，有永久和临时的。永久的需要修改相关的配置文件，临时的可以用export命令在当前终端下声明
- 按照作用域，有全局和局部的。全局的对所有用户有效，局部只对当前用户或当前shell有效



#### Linux环境变量设置

如果你想要设置**临时的**环境变量，你可以在命令行输入：

```bash
export PATH=$PATH:your_path
```

但是这种办法只对当前终端有效，一旦Linux重启或者当前终端关闭，使用这种办法设置的环境变量就会失效。需要重新输入命令才能继续生效

所以你如果不想这么麻烦，可以配置**永久的**环境变量。

我们都知道设置永久生效的配置，一般都需要修改文件，配置环境变量也是这样，不一样的是，跟环境变量相关的

文件挺多的。

- /etc/profile:全局的永久环境变量配置文件，对所有用户有效，只能由root用户修改
- /etc/bashrc:全局的永久环境变量配置文件，对所有用户有效，只对bash shell有效，只能由root用户修改
- \~/.profile或\~/.bash_profile:局部的永久环境变量配置文件，只对当前用户有效，只在登录时执行一次
- ~./bashrc:局部的永久环境变量配置文件，只对当前用户有效，每次打开新终端都会执行一次

配置永久全局变量，需要在配置文件中添加：

```bash
export PATH=$PATH:your_path
```

当你修改了配置文件之后，你需要`重启`或使用`source`来使环境变量生效

当你配置了环境变量之后，如果想知道是否配置成功，你可以输出环境变量值进行查看：

```bash
echo $PATH
```



在Linux中，有两种类型的shell，登录shell和非登录shell。可以使用`echo $0`查看当前shell名称，如果以`-`开头，就是登录shell，反之则是非登录shell不同的shell加载不同的配置文件顺序也是不一样的

- 登录shell：/etc/profile、~/.bashrc、/etc/bashrc
- 非登录shell：~/.bashrc、/etc/bashrc

除了上述说的相关配置文件，Linux还有一个相关的目录`/etc/profile.d`，这是/etc/profile文件的进阶版。当登录shell加载/etc/profile文件时，它会从profile.d目录中读取所有以.sh结尾的脚本文件。这样可以方便地管理不同的环境变量配置，而不用把所有的内容都写在一个文件里。

```bash
$ /etc/profile.d/java.sh
export JAVA_HOME=/root/jdk1.8.0_212
export PATH=$PATH:/root/jave/bin:/root/java/jre/bin
```

