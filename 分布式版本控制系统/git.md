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
	![[image/Pasted image 20240612141046.png]]
- Git文件存储方式：以全量的方式管理文件，直接记录快照，而非差异比较
	![[image/Pasted image 20240612141654.png]]
- Git文件状态
	- Git文件：已经被版本库管理的文件
	- 已修改：在工作目录修改Git文件
	- 已暂存：对已修改的文件执行Git暂存操作，将文件存入暂存区
	- 已提交：将已暂存的文件执行Git提交操作，将文件存入版本库
	![[image/Pasted image 20240612142252.png]]
	![[image/Pasted image 20240612142445.png]]
- 本地版本库与服务器版本库
	![[image/Pasted image 20240612142654.png]]

## 2.3.Git常用命令
- 获得版本库
	- git init
	- git clone
- 版本管理
	- git add
	- git commit
		- 会对提交内容使用sha1计算出一个commitid
	- git rm
- 查看信息
	- git help
	- git log
	- git diff
- 远程协作
	- git pull
	- git push
- 设置信息
	- git config --global user.name "Your Name"
	- git config --global user.email you@example.com
	> 可以在三个地方进行设置
	> 1. /etc/gitconfig(几乎不会使用) git config --system
	> 2. ~/.git config git config --global
	> 3. 针对特定项目 .git/config git config --local

ss









