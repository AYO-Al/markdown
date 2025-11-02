代码变成可执行文件，叫做[编译](https://www.ruanyifeng.com/blog/2014/11/compiler.html)（compile）；先编译这个，还是先编译那个（即编译的安排），叫做[构建](https://en.wikipedia.org/wiki/Software_build)（build）。

[Make](https://en.wikipedia.org/wiki/Make_%28software%29)是最常用的构建工具，诞生于1977年，主要用于C语言的项目。但是实际上 ，任何只要某个文件有变化，就要重新构建的项目，都可以用Make构建。
# 1 什么是 make

Make这个词，英语的意思是"制作"。Make命令直接用了这个意思，就是要做出某个文件。比如，要做出文件a.txt，就可以执行下面的命令。

```bash
$ make a.txt
```

但是，如果你真的输入这条命令，它并不会起作用。因为Make命令本身并不知道，如何做出a.txt，需要有人告诉它，如何调用其他命令完成这个目标。

比如，假设文件 a.txt 依赖于 b.txt 和 c.txt ，是后面两个文件连接（cat命令）的产物。那么，make 需要知道下面的规则。

```bash
a.txt: b.txt c.txt
    cat b.txt c.txt > a.txt
```

也就是说，make a.txt 这条命令的背后，实际上分成两步：第一步，确认 b.txt 和 c.txt 必须已经存在，第二步使用 cat 命令 将这个两个文件合并，输出为新文件。

像这样的规则，都写在一个叫做Makefile的文件中，Make命令依赖这个文件进行构建。Makefile文件也可以写为makefile， 或者用命令行参数指定为其他文件名。

```bash
$ make -f rules.txt
# 或者
$ make --file=rules.txt
```

总之，make只是一个根据指定的Shell命令进行构建的工具。它的规则很简单，你规定要构建哪个文件、它依赖哪些源文件，当那些文件有变动时，如何重新构建它。
# 2 makefile文件格式

Makefile文件由一系列规则（rules）构成。且规则是可以无序编写的。每条规则的形式如下。

```bash
<target> : <prerequisites> 
[tab]  <commands>
```

上面第一行冒号前面的部分，叫做"目标"（target），冒号后面的部分叫做"前置条件"（prerequisites）；第二行必须由一个tab键起首，后面跟着"命令"（commands）。

"目标"是必需的，不可省略；"前置条件"和"命令"都是可选的，但是两者之中必须至少存在一个。

每条规则就明确两件事：构建目标的前置条件是什么，以及如何构建。
## 2.1 目标(target)

一个目标（target）就构成一条规则。目标通常是文件名，指明Make命令所要构建的对象，比如上文的 a.txt 。目标可以是一个文件名，也可以是多个文件名，之间用空格分隔。

除了文件名，目标还可以是某个操作的名字，这称为"伪目标"（phony target）。

```bash
clean:
      rm *.o
```

上面代码的目标是clean，它不是文件名，而是一个操作的名字，属于"伪目标 "，作用是删除对象文件。

声明clean是"伪目标"之后，make就不会去检查是否存在一个叫做clean的文件，而是每次运行都执行对应的命令。像.PHONY这样的内置目标名还有不少，可以查看[手册](http://www.gnu.org/software/make/manual/html_node/Special-Targets.html#Special-Targets)。

如果Make命令运行时没有指定目标，默认会执行Makefile文件的第一个目标。

```bash
.PHONY: clean
clean:
        rm *.o temp
```
## 2.2 前置条件(prerequisites)

前置条件通常是一组文件名，之间用空格分隔，也可以是操作名。它指定了"目标"是否重新构建的判断标准：只要有一个前置文件不存在，或者有过更新（前置文件的last-modification时间戳比目标的时间戳新），"目标"就需要重新构建。

```bash
result.txt: source.txt
    cp source.txt result.txt
```

上面代码中，构建 result.txt 的前置条件是 source.txt 。如果当前目录中，source.txt 已经存在，那么`make result.txt`可以正常运行，否则必须再写一条规则，来生成 source.txt 。

```bash
source.txt:
    echo "this is the source" > source.txt
```

上面代码中，source.txt后面没有前置条件，就意味着它跟其他文件都无关，只要这个文件还不存在，每次调用`make source.txt`，它都会生成。

```bash
$ make result.txt
$ make result.txt
```

上面命令连续执行两次`make result.txt`。第一次执行会先新建 source.txt，然后再新建 result.txt。第二次执行，Make发现 source.txt 没有变动（时间戳晚于 result.txt），就不会执行任何操作，result.txt 也不会重新生成。

如果需要生成多个文件，往往采用下面的写法。

```bash 
source: file1 file2 file3
```

上面代码中，source 是一个伪目标，只有三个前置文件，没有任何对应的命令。然后编写对应的文件生成规则即可。

 ```bash
 '''
source: 
        touch 1.txt 2.txt 3.txt
clear: source
        rm 1.txt
'''

$ make source
```

执行`make source`命令后，就会一次性生成 file1，file2，file3 三个文件。这比下面的写法要方便很多。

```bash
$ make file1
$ make file2
$ make file3
```
## 2.3 命令(commands)

命令（commands）表示如何更新目标文件，由一行或多行的Shell命令组成。它是构建"目标"的具体指令，它的运行结果通常就是生成目标文件。

每行命令之前必须有一个tab键。如果想用其他键，可以用内置变量.RECIPEPREFIX声明。

需要注意的是，每行命令在一个单独的shell中执行。这些Shell之间没有继承关系。

需要注意的是，每行命令在一个单独的shell中执行。这些Shell之间没有继承关系。

```bash
var-lost:
    export foo=bar
    echo "foo=[$$foo]"
```

上面代码执行后（`make var-lost`），取不到foo的值。因为两行命令在两个不同的进程执行。一个解决办法是将两行命令写在一行，中间用分号分隔。

```bash
var-kept:
    export foo=bar; echo "foo=[$$foo]"
```

另一个解决办法是在换行符前加反斜杠转义。

```bash
var-kept:
    export foo=bar; \
    echo "foo=[$$foo]"
```

最后一个方法是加上`.ONESHELL:`命令。

```bash
.ONESHELL:
var-kept:
    export foo=bar; 
    echo "foo=[$$foo]"
```
# 3 makefile文件语法

## 3.1 注释

井号（#）在Makefile中表示注释。

## 3.2 回声（echoing）

正常情况下，make会打印每条命令，然后再执行，这就叫做回声（echoing）。

```bash
test:
    # 这是测试
```

执行上面的规则，会得到下面的结果。

```bash
test:
    @# 这是测试
```

在命令的前面加上@，就可以关闭回声。

现在再执行`make test`，就不会有任何输出。

由于在构建过程中，需要了解当前在执行哪条命令，所以通常只在注释和纯显示的echo命令前面加上@。
## 3.3 容错模式

默认情况下，如果一条命令执行失败（返回非零的退出状态码），Make 就会​**​立即停止​**​构建。`-`前缀的作用是告诉 Make：“执行这个命令，即使它失败了也继续往下执行，不要停止”。
## 3.4 通配符

通配符（wildcard）用来指定一组符合条件的文件名。Makefile 的通配符与 Bash 一致，主要有星号（*）、问号（？）和 \[...] 。比如， *.o 表示所有后缀名为o的文件。

- `*`：匹配任意长度的字符串（包括空字符串），但不匹配以点开头的文件（隐藏文件），除非明确指定。
    
- `?`：匹配任意单个字符。
    
- `[...]`：匹配括号内的任意一个字符。
## 3.5 模式匹配

Make命令允许对文件名，进行类似正则运算的匹配，主要用到的匹配符是%。比如，假定当前目录下有 f1.c 和 f2.c 两个源码文件，需要将它们编译为对应的对象文件。

**注意：模式匹配匹配的是当前上下文中的规则，而不是去扫目录中的文件，模式规则本身不会触发，除非有目标匹配这个模式。**

Make命令允许对文件名，进行类似正则运算的匹配，主要用到的匹配符是%。比如，假定当前目录下有 f1.c 和 f2.c 两个源码文件，需要将它们编译为对应的对象文件。

```bash

%.o: %.c
```

等同于下面的写法。

```bash

f1.o: f1.c
f2.o: f2.c
```

使用匹配符%，可以将大量同类型的文件，只用一条规则就完成构建。
## 3.6 变量和赋值符

Makefile 允许使用等号自定义变量。

```bash

txt = Hello World
test:
    @echo $(txt)
```

上面代码中，变量 txt 等于 Hello World。调用时，变量需要放在 $( ) 之中。

调用Shell变量，需要在美元符号前，再加一个美元符号，这是因为Make命令会对美元符号转义。

```bash
a="hello world"
echo:
        @ echo $(a)
        @ echo $$PATH
```

有时，变量的值可能指向另一个变量。

```bash
v1 = $(v2)
```

上面代码中，变量 v1 的值是另一个变量 v2。这时会产生一个问题，v1 的值到底在定义时扩展（静态扩展），还是在运行时扩展（动态扩展）？如果 v2 的值是动态的，这两种扩展方式的结果可能会差异很大。

为了解决类似问题，Makefile一共提供了四个赋值运算符 （=、:=、？=、+=），它们的区别如下

```bash
VARIABLE = value
# 在执行时扩展，允许递归扩展。

VARIABLE := value
# 在定义时扩展。

VARIABLE ?= value
# 只有在该变量为空时才设置值。

VARIABLE += value
# 将值追加到变量的尾端。+=会继承原始变量的展开方式
```
## 3.7 内置变量

Make命令提供一系列内置变量，比如，$(CC) 指向当前使用的编译器，$(MAKE) 指向当前使用的Make工具。这主要是为了跨平台的兼容性，详细的内置变量清单见[手册](https://www.gnu.org/software/make/manual/html_node/Implicit-Variables.html)。

```bash
output:
    $(CC) -o output input.c
```
## 3.8 自动变量

Make命令还提供一些自动变量，它们的值与当前规则有关。主要有以下几个。

- $@

$@指代当前目标，就是Make命令当前构建的那个目标。比如，make foo的 $@ 就指代foo。

```bash
a.txt b.txt: 
    touch $@
```

等同于下面的写法。

```bash
a.txt:
    touch a.txt
b.txt:
    touch b.txt
```

- $<

$< 指代第一个前置条件。比如，规则为 t: p1 p2，那么$< 就指代p1。

```bash
a.txt: b.txt c.txt
    cp $< $@ 
```

等同于下面的写法。

```bash
a.txt: b.txt c.txt
    cp b.txt a.txt 
```

- \$?:  \$? 指代比目标更新的所有前置条件，之间以空格分隔。比如，规则为 t: p1 p2，其中 p2 的时间戳比 t 新，$?就指代p2。

- $^: $^ 指代所有前置条件，之间以空格分隔。比如，规则为 t: p1 p2，那么 $^ 就指代 p1 p2 。

- \$\*:  \$* 指代匹配符 % 匹配的部分， 比如% 匹配 f1.txt 中的f1 ，$* 就表示 f1。

- \$(\@D) / \$(\@F): \$(\@D) 和 \$(\@F) 分别指向 \$@ 的目录名和文件名。比如，\$\@是 src/input.c，那么\$(\@D) 的值为 src ,\$(\@F) 的值为 input.c。

- $(<D) / $(<F): $(<D) 和 $(<F) 分别指向 $< 的目录名和文件名。

所有的自动变量清单，请看[手册](https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html)。下面是自动变量的一个例子。
## 3.9 判断和循环

Makefile使用 Bash 语法，完成判断和循环。

```bash
### `ifeq`/ `ifneq`- 判断相等/不等
# 判断两个值是否相等
ifeq ($(CC),gcc)
    CFLAGS = -O2
else
    CFLAGS = -O1
endif

# 判断是否为空
ifeq ($(DEBUG),)
    CFLAGS += -DNDEBUG
else
    CFLAGS += -g -DDEBUG
endif

# ifneq 用法类似
ifneq ($(OS),Windows_NT)
    RM = rm -f
else ifeq ($(OS),Windows_NT)
    RM = del
endif


### `ifdef`/ `ifndef`- 判断变量是否定义

# 判断变量是否定义（非空）
ifdef VERBOSE
    Q =  # 空，显示完整命令
else
    Q = @  # 不显示命令
endif

# 判断变量是否未定义或为空
ifndef PREFIX
    PREFIX = /usr/local
endif
```

- 循环

```bash
LIST = one two three
all:
    for i in $(LIST); do \
        echo $$i; \
    done

# 等同于

all:
    for i in one two three; do \
        echo $i; \
    done
```
# 4 函数

Makefile 还可以使用函数，格式如下。

```bash
$(function arguments)
# 或者
${function arguments}
```

Makefile提供了许多[内置函数](http://www.gnu.org/software/make/manual/html_node/Functions.html)，可供调用。下面是几个常用的内置函数。

## 4.1 字符串处理函数

|函数|定义|作用|实例|注意事项|
|---|---|---|---|---|
|​**​subst​**​|`$(subst from,to,text)`|字符串替换|`$(subst ee,EE,feet)`→ `fEEt`|不支持模式匹配，仅简单替换|
|​**​patsubst​**​|`$(patsubst pattern,replacement,text)`|模式替换|`$(patsubst %.c,%.o,foo.c)`→ `foo.o`|支持 `%`通配符，比 subst 更强大|
|​**​strip​**​|`$(strip string)`|去除多余空格|`$(strip a b )`→ `a b`|只去除开头结尾空格，合并中间空格|
|​**​findstring​**​|`$(findstring find,in)`|查找子串|`$(findstring a,abc)`→ `a`|找到返回子串，否则返回空|
|​**​filter​**​|`$(filter pattern...,text)`|过滤匹配项|`$(filter %.c,foo.c bar.h)`→ `foo.c`|支持多个模式，空格分隔|
|​**​filter-out​**​|`$(filter-out pattern...,text)`|过滤不匹配项|`$(filter-out %.c,foo.c bar.h)`→ `bar.h`|与 filter 相反|
|​**​sort​**​|`$(sort list)`|排序并去重|`$(sort b a c a)`→ `a b c`|按字典序排序，自动去重|
|​**​word​**​|`$(word n,text)`|取第n个单词|`$(word 2,foo bar baz)`→ `bar`|从1开始计数，越界返回空|
|​**​wordlist​**​|`$(wordlist s,e,text)`|取单词子列表|`$(wordlist 2,3,a b c d)`→ `b c`|包含起始和结束位置|
|​**​words​**​|`$(words text)`|统计单词数|`$(words a b c)`→ `3`|空字符串返回0|
|​**​firstword​**​|`$(firstword text)`|取第一个单词|`$(firstword a b c)`→ `a`|等价于 `$(word 1,text)`|

## 4.2 文件名函数

|函数|定义|作用|实例|注意事项|
|---|---|---|---|---|
|​**​dir​**​|`$(dir names...)`|提取目录部分|`$(dir src/foo.c)`→ `src/`|总是以斜杠结尾|
|​**​notdir​**​|`$(notdir names...)`|提取文件名部分|`$(notdir src/foo.c)`→ `foo.c`|去掉目录路径|
|​**​suffix​**​|`$(suffix names...)`|提取文件后缀|`$(suffix foo.c)`→ `.c`|包含点号，无后缀返回空|
|​**​basename​**​|`$(basename names...)`|提取文件前缀|`$(basename foo.c)`→ `foo`|去掉后缀部分|
|​**​addsuffix​**​|`$(addsuffix suffix,names...)`|添加后缀|`$(addsuffix .c,foo)`→ `foo.c`|直接拼接，不检查重复|
|​**​addprefix​**​|`$(addprefix prefix,names...)`|添加前缀|`$(addprefix src/,foo.c)`→ `src/foo.c`|直接拼接|
|​**​wildcard​**​|`$(wildcard pattern)`|通配符展开|`$(wildcard *.c)`→ 文件列表|在变量赋值时必须使用|
|​**​realpath​**​|`$(realpath names...)`|获取绝对路径|`$(realpath ./foo)`→ 绝对路径|解析所有符号链接|
|​**​abspath​**​|`$(abspath names...)`|获取绝对路径|`$(abspath ./foo)`→ 绝对路径|不解析符号链接|

## 4.3 条件判断函数

|函数|定义|作用|实例|注意事项|
|---|---|---|---|---|
|​**​if​**​|`$(if condition,then-part[,else-part])`|条件判断|`$(if foo,then,else)`→ `then`|condition 非空为真|
|​**​or​**​|`$(or condition1,condition2,...)`|逻辑或|`$(or ,foo,)`→ `foo`|返回第一个非空参数|
|​**​and​**​|`$(and condition1,condition2,...)`|逻辑与|`$(and foo,bar)`→ `bar`|全部非空返回最后一个|

## 4.4 循环和控制函数

|函数|定义|作用|实例|注意事项|
|---|---|---|---|---|
|​**​foreach​**​|`$(foreach var,list,text)`|循环处理|`$(foreach f,a b,$(f).c)`→ `a.c b.c`|var 是临时变量|
|​**​eval​**​|`$(eval text)`|动态解析代码|`$(eval VAR := value)`|将文本作为 Makefile 代码执行|
|​**​value​**​|`$(value var)`|获取变量原始值|`$(value VAR)`→ 未展开的值|用于查看变量定义|
|​**​call​**​|`$(call variable,param,...)`|调用自定义函数|`$(call func,arg)`|配合 define 使用|

## 4.5 文件和shell函数

|函数|定义|作用|实例|注意事项|
|---|---|---|---|---|
|​**​shell​**​|`$(shell command)`|执行shell命令|`$(shell ls)`→ 命令输出|每调用一次执行一次命令|
|​**​file​**​|`$(file op filename,text)`|文件操作|`$(file > out.txt,text)`|GNU make 4.0+ 支持|
|​**​info​**​|`$(info text)`|输出信息|`$(info Building...)`|不停止执行，仅输出|
|​**​warning​**​|`$(warning text)`|输出警告|`$(warning Deprecated)`|不停止执行，显示警告|
|​**​error​**​|`$(error text)`|输出错误并停止|`$(error Fatal)`|立即停止make执行|

## 4.6 自定义函数

|功能|定义方式|调用方式|实例|注意事项|
|---|---|---|---|---|
|​**​自定义函数​**​|使用 `define...endef`|`$(call func,args)`|见下方详细示例|参数通过 `$(1)`, `$(2)`访问|
```bash
# 彩色输出函数
define ColorInfo
@echo -e "\033[36m[INFO] $(1)\033[0m"
endef

define ColorSuccess
@echo -e "\033[32m[SUCCESS] $(1)\033[0m"
endef

define ColorError
@echo -e "\033[31m[ERROR] $(1)\033[0m"
endef

# 使用示例
deploy:
	$(call ColorInfo,"开始部署...")
	$(call ColorSuccess,"部署完成!")
	$(call ColorError,"部署失败!")

```

| 元素               | 正确语法                        | 错误示例                | 说明             |
| ---------------- | --------------------------- | ------------------- | -------------- |
| ​**​函数定义​**​     | `define Name`或 `Name = ...` | `define Add echo:`  | 不需要冒号          |
| ​**​参数引用​**​     | `$(1)`, `$(2)`              | `$1`, `$2`          | 需要括号           |
| ​**​函数调用​**​     | `$(call Name,arg1,arg2)`    | `$(call,Name,arg1)` | 函数名在 call 后直接跟 |
| ​**​多行函数​**​     | 使用 `define...endef`         | 直接写多行               | 需要 define 包装   |
| ​**​Shell 命令​**​ | 使用 `@`或 `-`前缀               | 直接写命令               | 控制命令显示和错误处理    |