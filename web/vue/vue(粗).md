# node环境搭建
#TODO vue详细学习
使用node.js可以快速的创建出vue-cli的脚手架。使用nvm来安装管理node版本。

#### **1. 安装与管理 Node.js 版本**

|命令|作用|示例|
|---|---|---|
|`nvm install <version>`|安装指定版本 Node.js|`nvm install 18.16.0`|
|`nvm install --lts`|安装最新的 LTS 版本|`nvm install --lts`|
|`nvm uninstall <version>`|卸载指定版本|`nvm uninstall 16.20.1`|
|`nvm use <version>`|临时切换 Node.js 版本|`nvm use 20.5.0`|
|`nvm alias default <version>`|设置默认版本|`nvm alias default 18.16.0`|

#### ​**2. 版本列表与信息查询**

|命令|作用|
|---|---|
|`nvm ls`|查看已安装的所有版本|
|`nvm ls-remote`|列出远程可安装的版本列表|
|`nvm ls-remote --lts`|仅列出远程 LTS 版本|
|`nvm current`|显示当前使用的版本|

#### ​**3. 别名与快捷操作**

|命令|作用|
|---|---|
|`nvm alias <name> <version>`|为版本设置别名（如 `dev`、`prod`）|
|`nvm unalias <name>`|删除别名|
|`nvm run <version> <command>`|用指定版本运行命令|
|`nvm exec <version> <command>`|在指定版本下执行命令|
#### npm

1. 全局安装：安装在node的安装目录
```node
nup install vue -g
```
2. 本地安装：安装在本项目目录
```node
npm install vue
```
**--save参数会将安装的包记录到package.json中**

- 查看版本：npm -v
- 初始化：npm init 进入指定项目目录执行，会生成一个package.json文件，保存本项目中用到的包

- 安装vue-cli：npm install @vue/cli -g

- 创建vue项目：vue creat prijectname

## 项目结构

```
README.md node_modules public

babel.config.js package-lock.json src

jsconfig.json package.json vue.config.js
```

- node_modules：本地安装包的文件夹
- public：项目出口文件
- src：项目源文件
    - App.vue ：入口组件
    - assets ：资源文件
    - components ：组件文件
    - main.js：webpack在打包时候的入口文件
- babel.config.js：es\*转低级js语言的配置文件
- package.json：项目包管理文件

# ant库

https://3x.antdv.com/components/icon-cn

# 服务端和vue交互

vue-router是vue官方的路由管理器

https://v3.router.vuejs.org/zh/installation.html