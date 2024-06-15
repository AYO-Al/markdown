# 1. 简介
- git官方网站：[Git (git-scm.com)](https://git-scm.com/)

# 2.Git入门
## 2.1.Git介绍
自诞生于2005年以来，Git日渐完善，它的速度很快，极其适合管理大型项目，它还有着令人难以置信的非线性分支管理系统，可以应付各种复杂的项目开发需求。
- Git是一个版本控制软件，具有以下几点优点
	- 本地建立版本库
	- 本地版本控制
	- 多主机异地协同工作
	- 重写提交说明
	- 可以进行版本回退
	- 更好的提交列表
	- 更好的差异比较
	- 更完善的分支系统
	- 速度极快
- Github与GitLab都是用于管理版本的服务端软件
- GitLab用于在企业内部管理Git版本库，功能上类似于GitHub
## 2.2.Git工作模式
- 版本库初始化
	- 个人计算机从版本服务器同步
- 操作
	- 90%以上的操作在个人计算机上
	- 添加文件
	- 修改文件
	- 提交变更
	- 查看版本历史等
- 版本库同步
	- 将本地修改推送到版本服务器
	![](image/Git_time_1.png)
- Git文件存储方式：以全量的方式管理文件，直接记录快照，而非差异比较
	![[image/Git_time_2.png]]
- Git文件状态
	- Git文件：已经被版本库管理的文件
	- 已修改：在工作目录修改Git文件
	- 已暂存：对已修改的文件执行Git暂存操作，将文件存入暂存区
	- 已提交：将已暂存的文件执行Git提交操作，将文件存入版本库
	![[image/Git_time_3.png]]
	![[image/Git_time_4.png]]
- 本地版本库与服务器版本库
	![[image/Git_time_5.png]]

## 2.3.Git常用命令
- 获得版本库
	- git init
	- git clone
- 版本管理
	- git add
	- git commit
		- 会对提交内容使用sha1计算出一个commitid
		- `git commit --amend -m 'mesge'`:修正上一条提交的信息
		- `git commit -am`：直接把全部文件添加到暂存区并提交
	- git rm：删除文件，本质和rm命令一致
		- 使用`git rm`后不需要再使用`git add`命令将修改添加在暂存区，使用`rm`的话仍然需要使用使用`git add`命令将修改添加在暂存区
		- 如果想将删除的文件恢复，可以使用`git reset HEAD filename`将文件从暂存区移除，再使用`git checkout -- fielname`将工作区中的修改丢弃
	- git mv
	- git branch：分支操作，不带参数则查看所有分支，带`*`为当前所在分支
	- git checkout
		- git checkout branchname:切换分支
- 查看信息
	- git help
	- git log：查看提交历史
		- -p：展开显示每次提交的内容差异
		- -n：只显示n条
		- --pretty=oneline|format:"%h"：指定格式进行输出
	- git diff
- 远程协作
	- git pull
	- git push
- 设置信息：在提交文件时需要进行设置
	- git config --global user.name "Your Name"
	- git config --global user.email you@example.com
	> 可以在三个地方进行设置
	> 1. /etc/gitconfig(几乎不会使用) git config --system
	> 2. ~/.gitconfig git config --global
	> 3. 针对特定项目 .git/config git config --local

## 2.4.gitignore
在git中可以在.gitigore文件中编写一定的规则，让git管理时忽略一些文件。编写规则的语法如下：
```bash
以#号开始的表示注释
以/结尾表示目录
以*通配多个字符
以?通配单个字符
以[]包含单个字符的匹配列表
以!表示不忽略匹配到的文件或目录
```
.gitigore的规则读取方式是采用从上往下的顺序，所以如果上面的规则范围比较大，下面范围较小的规则则不会生效。

## 2.5.分支
分支是git中一个非常重要的概念。分支其实就是一条commit对象链(一条工作记录线)
![](image/Git_time_6.png)
有常见操作有以下几种：
- git branch \[branchname]: 查看/创建分支，带\*的为当前所在分支。
	- -d/-D：删除分支/如果分支上有未合并的操作
- git checkout \[branchname]：切换分支
	- -b：创建并切换到分支
- git merge branch：合并分支
在git中，使用`HEAD`指向当前分支，信息存储在.git/HEAD中
快进合并：master没有做任何修改，直接就是把master指向最新的提交。
![](image/Git_time_7.png)
分支合并：master和分支都做了操作，如果有冲突需要手动解决冲突再合并。有冲突的文件会变成下面这样。解决完冲突后使用`git add filename`标记解决冲突，再使用`git commit`提交合并。
![](image/Git_time_8.png)
![](image/Git_time_9.png)
如果可能的话，合并分支时Git会使用fast-forward模式，这种模式下，删除分支时会丢掉分支信息。可以在合并时加上`--no-ff`参数会禁用fast-forward，这样会多出一个`commit id`。
由于Git其实就是由一条提交链组成的，所以我们可以回退到任意一个提交上。
- 回退到上一版本
	- git reset --hard HEAD^
	- git reset --hard HEAD~1
	- git reset --hard commit_id
- 回退到某一个版本
	- git reflog