# PYQT5

## 1.GUI入口套路

```python
import sys
from PyQt5.Qtwidgets import QApplication,QMainWindow
from function import partial

if __name__ == "__main__":
    # 创建应用
    # argv:当别人通过命令行启动这个程序的时候，可以设定一种功能(接收命令行传递的参数来执行不同的业务逻辑)
    app = QApplication(sys,argv)
    
    # 创建窗口
    MainWindow = QMainWindow()
    
    # 创建组件对象
    ui = Ui_MainWindow()
    
    # 把组件加载到窗口上
    ui.setupUi(MainWindow)
    
    # 窗口显示
    MainWindow.show()
    
    # 为组件设置槽
    ui1.pushButton.clicked.connect(partial(函数, 参数))
    
   # 让整个程序开始执行，并且进入到消息循环	(无限循环)
   # 监测整个程序所接收到的用户交互信息
   # exit(退出码)，正常退出是0，程序内部错误是其他的错误码，通过传递不同的错误码，可以知道怎么退出的。
    sys.exit(app.exec_())
```

## 2.常用的pyqt库

1. QtWidgets:包含一整套的UI元素控件，用于建立符合系统风格的界面
2. QtGui:涵盖多种基本图像功能的类（字体，图形，图标，颜色）
3. QtCore:涵盖了包的核心的非GUI界面的功能(时间，文件，目录，数据类型，文本流，链接，线程进程等)
4. QtWebKit:显示网页
5. QtTest:对Qt应用程序和库进行单元测试的类
6. QtSql:提供对SQL数据库支持的基本模块
7. QtMultimedia:多媒体，比如音频，视频
8. QtMultimediaWidgets:多媒体，比如音频，视频

## 3.Qt Designer的使用

**Qt Designer是专门用来制作PyQt程序中UI界面的可视化工具**

它会生成一个后缀为ui的文件，符合MVC设计模式，做到了显示和业务逻辑的分离。

### 3.1.Qt Designer界面认识

1. 最左侧的**Widget Box为工具箱**，提供多种控件，可以直接拖曳安放，ctrl+r可以预览效果
   2. 中间的**MainWindow就是主窗口**
   3. 右侧最上方的**Object Inspector为对象查看器**，可以查看主窗口放置的对象列表
   4. 右侧中间的**Property Editor为属性编辑器**，其中提供了对窗口、控件、不具的属性编辑功能
   5. 最下方的**Signal/Slot/Editor 信号/槽编辑器、动作编辑器和资源浏览器**\
      1\. 在信号/槽编辑器中，可以为控件添加自定义的信号和槽函数\
      2\. 在资源浏览器中，可以为控件添加资源，如Label的背景图片

![](https://note.youdao.com/yws/public/resource/92933d878935240680c00793fc3e404c/xmlnote/WEBRESOURCE67d96a0104eb75789de7f834b52d51d2/410)

### 3.2.Qt Designer布局方式

Qt Designer提供了四种窗口布局：

```
1. Vertical Layout(垂直布局)
2. Horizontal Layout(水平布局)
3. Grid Layout(栅格布局)
4. Form Layout(表单布局)
5. 以及隐藏的-绝对布局
 - 绝对布局是最简单的一种布局，就是在右侧的属性编辑器中更改，设置geometry属性，X,Y分别代表这个控件左上角距离主窗口左侧多
```

一般进行布局有两种方式：**一是通过布局管理器进行布局，而是通过容器控件进行布局**

### 3.3.关于分割线

工具箱中的Spacers栏中有水平分隔线和垂直分割线，用来给控件分隔

### 3.4.关于Qt Designer的控件尺寸策略

#### 3.4.1.控件的最大值与最小值

**一个控件拖到主窗口后可以随意放大或缩小，但是也是有限制的，位置在属性编辑器，属性名为`minimumSize`,`maximumSize`。**

#### 3.4.2.期望尺寸

*   sizeHint(期望尺寸)

    * 每个控件的期望尺寸是不同的，在未设置控件最大值最小值之前，控件推荐到某个尺寸，像默认尺寸一样。但对大多数控件来说，期望尺寸是只读的。

    ```python
    self.控件名.sizeHint.width()
    self.控件名.sizeHint.height()
    ```
*   minisizeHInt

    ```python
    self.控件名.minimumSizeHint().width()
    self.控件名.minimumSizeHint().height()

    ```

#### 3.4.3.尺寸策略

* 尺寸策略在属性编辑器中的Horizontal Policy属性中设置
* 分为水平策略和垂直策略
* 水平策略
  * `Fixed`：窗口控件具有其sizeHint所提示的尺寸且尺寸不会再改变
  * `Minimum`：窗口控件的sizeHint所提示的尺寸就是它的最小尺寸，该控件不能压缩的比这个值小
  * `Maximum`：窗口控件的sizeHint所提示的尺寸就是它的最大尺寸，该窗口控件不能变得比这个值大，但它可以被压缩到minisizeHint给定的尺寸大小；
  * `Preferred`：窗口控件的sizeHint所提示的尺寸就是它的期望尺寸，该窗口控件可以缩小到minisizeHint所提示的尺寸，也可以变得比sizeHint所提示的尺寸还大；
  * `Expanding`：窗口控件可以缩小到minisizeHint所提示的尺寸，也可以变得比sizeHint所提示的尺寸大，但它希望能变得更大；
  * `MinimumExpanding`：窗口控件的sizeHint所提示的尺寸就是它的最小尺寸，该窗口控件不能被压缩得比这个值还小，但它希望能够变得更大；
  * `Ignored`：无视窗口控件的sizeHint和minisizeHint所提示的尺寸，按照默认来设置。

### 3.5.设置控件之间的伙伴关系

* 伙伴关系：伙伴关系就是指在界面上有一个Label标签和一个组件相关联，它的作用就是为了在程序运行的时候，在窗体上使用`快捷键`快速的将输入焦点切换到某个组件上。
  1. 在Label的文本内容中加入&+快捷键内容
  2. 在菜单中设置伙伴关系
  3. 设置成功后就可以用alt+快捷键内容来快速切换焦点
