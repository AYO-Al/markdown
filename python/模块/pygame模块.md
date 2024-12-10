## 快速入门pygame
### 安装pygame模块
```
pip install pygame
```
### 游戏的初始化和退出
- 初始化
  ```
  pygame.init()
  # 导入并初始化所有pygame模块，使用其他pygame模块之前必须先调用init方法
  ```
- 退出
  ```
  pygame.quit()
  # 卸载所有的pygame模块，在游戏结束之前调用，清空内存
  ```
- 实例
  ```python
  import pygame
  pygame.init()
  pygame.quit()
  ```



### 游戏中的坐标系

- 左上角顶点为原点
- x轴水平向右，逐渐增加
- y轴垂直向下，逐渐增加
- 在游戏中，所有的可见元素全部都是以矩形区域来描述位置，主要参数有（x,y,(width,height)）
### 矩形区域
- pygame.Rect

```python
# 使用Surface对象的get_rect()方法创建一个Rect对象
ball=pygame.image.load('qiu.png')
ball=pygame.transform.scale(ball,(130,130))
ballrect=ball.get_rect()

# Rect对象的属性
x,y
top, left, bottom, right
topleft, bottomleft, topright, bottomright
midtop, midleft, midbottom, midright
center, centerx, centery
size, width, height
w,h
# 这些都可以分配给：
rect1.right = 10
rect2.center = (20,30)
```
- pygame.Rect.move([x,y])
  - 移动矩形区域

### 显示函数
- pygame.display

- pygame.display.set_mode()
  - 初始化窗口或屏幕以进行显示
  ```python
  # set_mode(size=(0, 0), flags=0, depth=0)
  ## size表示一对表示宽度和高度的数字
  # flag是附加选项的集合，可以控制所需要的显示类型
  '''
  FULLSCREEN 创建一个全屏窗口
  RESIZABLE 创建一个可以改变大小的窗口
  NOFRAME 创建一个没有边框的窗口
  
  screen=pygame.display.set_mode((640,640),pygame.FULLSCREEN)
  '''
  # depth表示要用于颜色的位数
  ```
  
- pygame.display.get_surface()->Surface
  
  - 获取对当前设置的显示Surface的引用
  
- pygame.display.flip()

  - 更新完整屏幕

- pygame.display.update()
  - 更新部分屏幕

- pygame.display.get_desktop_sizes()
  - 获取活动桌面的大小

- pygame.display.toggle_fullscreen()
  - 切换全屏与窗口状态

- pygame.display.set_caption(标题)
  - 更改窗口标题

- pygame.display.set_icon(文件路径)
  - 更改窗口图标
### 事件处理方法
- pygame.event
- pygame.event.get()
  - 从队列获取事件
- pygame.event.wait()
  - 等待队列中的单个事件，默认为任意事件
- event.type
  - 获取事件的类型
#### 键盘事件
- pygame.key
- pygame.pygame.KEYDOWN
  - 键盘按下事件
- pygame.KEYUP
  - 键盘弹起事件
```
这两个事件均包含key属性，是一个整数id，代表键盘上具体的某个按键
```
- key常量

|KeyASCII|ASCII|描述|
|-|-|-|
|K_BACKSPACE|	\b	|退格键（Backspace）|
K_TAB|	\t|	制表键（Tab）
K_CLEAR|		|清除键（Clear）
K_RETURN|	\r|	回车键（Enter）
K_PAUSE|		|暂停键（Pause）
K_ESCAPE|	^[	|退出键（Escape）
K_SPACE|		|空格键（Space）
K_EXCLAIM|	!	|感叹号（exclaim）
K_QUOTEDBL|	"	|双引号（quotedbl）
K_HASH|	#	|井号（hash）
K_DOLLAR|	$	|美元符号（dollar）
K_AMPERSAND|	&	|and 符号（ampersand）
K_QUOTE|	’	|单引号（quote）
K_LEFTPAREN|	(	|左小括号（left parenthesis）
K_RIGHTPAREN|	)	|右小括号（right parenthesis）
K_ASTERISK|	*	|星号（asterisk）
K_PLUS|	+	|加号（plus sign）
K_COMMA|	,	|逗号（comma）
K_MINUS|	-	|减号（minus sign）
K_PERIOD|	.	|句号（period）
K_SLASH|	/	|正斜杠（forward slash）
K_0|	0|	0
K_1|	1|	1
K_2|	2|	2
K_3|	3|	3
K_4|	4|	4
K_5|	5|	5
K_6|	6|	6
K_7|	7|	7
K_8|	8|	8
K_9|	9|	9
K_COLON|	:	|冒号（colon）
K_SEMICOLON|	;	|分号（semicolon）
K_LESS|	<	|小于号（less-than sign）
K_EQUALS|	=	|等于号（equals sign）
K_GREATER|	>	|大于号（greater-than sign）
K_QUESTION|	?	|问号（question mark）
K_AT|	@	|at 符号（at）
K_LEFTBRACKET|	[	|左中括号（left bracket）
K_BACKSLASH|	\	|反斜杠（backslash）
K_RIGHTBRACKET|	]	|右中括号（right bracket）
K_CARET|	^	|脱字符（caret）
K_UNDERSCORE|	_	|下划线（underscore）
K_BACKQUOTE|	`	|重音符（grave）
K_a|	a|	a
K_b|	b|	b
K_c|	c|	c
K_d	|d|	d
K_e	|e|	e
K_f	|f|	f
K_g	|g|	g
K_h	|h|	h
K_i	|i|	i
K_j	|j|	j
K_k	|k|	k
K_l	|l|	l
K_m	|m|	m
K_n	|n|	n
K_o	|o|	o
K_p	|p|	p
K_q	|q|	q
K_r	|r|	r
K_s	|s|	s
K_t	|t|	t
K_u	|u|	u
K_v	|v|	v
K_w	|w|	w
K_x	|x|	x
K_y	|y|	y
K_z|	z|	z
K_DELETE|		|删除键（delete）
K_KP0|		|0（小键盘）
K_KP1|	|	1（小键盘）
K_KP2|	|	2（小键盘）
K_KP3|	|	3（小键盘）
K_KP4	|	|4（小键盘）
K_KP5	|	|5（小键盘）
K_KP6	|	|6（小键盘）
K_KP7	|	|7（小键盘）
K_KP8	|	|8（小键盘）
K_KP9	|	|9（小键盘）
K_KP_PERIOD|	.	|句号（小键盘）
K_KP_DIVIDE|	/	|除号（小键盘）
K_KP_MULTIPLY|	*	|乘号（小键盘）
K_KP_MINUS|	-	|减号（小键盘）
K_KP_PLUS|	+	|加号（小键盘）
K_KP_ENTER|	\r	|回车键（小键盘）
K_KP_EQUALS|	=	|等于号（小键盘）
K_UP|		|向上箭头（up arrow）
K_DOWN|		|向下箭头（down arrow）
K_RIGHT|		|向右箭头（right arrow）
K_LEFT|		|向左箭头（left arrow）
K_INSERT|		|插入符（insert）
K_HOME|		|Home 键（home）
K_END|	|	End 键（end）
K_PAGEUP|		|上一页（page up）
K_PAGEDOWN|		|下一页（page down）
K_F1|		|F1
K_F2|		|F2
K_F3|		|F3
K_F4|		|F4
K_F5|		|F5
K_F6|		|F6
K_F7|		|F7
K_F8|		|F8
K_F9|		|F9
K_F10|	|	F10
K_F11|	|	F11
K_F12	|	|F12
K_F13||		F13
K_F14	||	F14
K_F15	||	F15
K_NUMLOCK||		数字键盘锁定键（numlock）
K_CAPSLOCK||		大写字母锁定键（capslock）
K_SCROLLOCK	||	滚动锁定键（scrollock）
K_RSHIFT	||	右边的 shift 键（right shift）
K_LSHIFT	||	左边的 shift 键（left shift）
K_RCTRL	||	右边的 ctrl 键（right ctrl）
K_LCTRL	||	左边的 ctrl 键（left ctrl）
K_RALT	||	右边的 alt 键（right alt）
K_LALT	||	左边的 alt 键（left alt）
K_RMETA	||	右边的元键（right meta）
K_LMETA	||	左边的元键（left meta）
K_LSUPER||		左边的 Window 键（left windows key）
K_RSUPER	||	右边的 Window 键（right windows key）
K_MODE	||	模式转换键（mode shift）
K_HELP	||	帮助键（help）
K_PRINT	||	打印屏幕键（print screen）
K_SYSREQ	||	魔术键（sysrq）
K_BREAK	||	中断键（break）
K_MENU		||菜单键（menu）
K_POWER		||电源键（power）
K_EURO		||欧元符号（euro）

```
# 按下a键退出
  if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_a:
          pygame.quit()
```


- 组合键的常量定义

|KeyASCII|	描述|
|-|-|
|KMOD_NONE|	木有同时按下组合键|
KMOD_LSHIFT|	同时按下左边的 shift 键
KMOD_RSHIFT|	同时按下右边的 shift 键
KMOD_SHIFT|	同时按下 shift 键
KMOD_CAPS|	同时按下大写字母锁定键
KMOD_LCTRL|	同时按下左边的 ctrl 键
KMOD_RCTRL|	同时按下右边的 ctrl 键
KMOD_CTRL	|同时按下 ctrl 键
KMOD_LALT	|同时按下左边的 alt 键
KMOD_RALT	|同时按下右边的 alt 键
KMOD_ALT	|同时按下 alt 键
KMOD_LMETA|	同时按下左边的元键
KMOD_RMETA|	同时按下右边的元键
KMOD_META	|同时按下元键
KMOD_NUM	|同时按下数字键盘锁定键
KMOD_MODE	|同时按下模式转换键

- pygame.key.get_pressed()
  - 获取键盘上所有按键的状态
  - 返回一个由布尔值组成的序列
```
# 按下a键退出
  if event.type == pygame.KEYDOWN:
      keys=pygame.key.get_pressed()
      if keys[pygame.K_a]:
          pygame.quit()
```
- pygame.key.get_mods()
  - 检测是否有组合键被按下
```
# 按下Ctrl键退出
  if event.type == pygame.KEYDOWN:
      keys=pygame.key.get_pressed()
      if pygame.key.get_mods() & pygame.KMOD_CTRL:
              pygame.quit()
```
- pygame.key.set_repeat()
  - 控制重复响应持续按下按键的时间
```
# delay参数(毫秒)控制按下多久后开始发送第一个pygame.KEYDOWN事件
# interval参数设置发送两个事件之间的间隔
```
#### 鼠标事件
- pygame.mouse
- pygame.MOUSEBUTTONDOWN
  - 鼠标按下事件
- pygame.MOUSEBUTTONUP
  - 鼠标松开事件
```
# 都有一个按键属性
# 鼠标滑轮滚动时也会触发这两个事件，向上滚动时按键会被设置为4，向下滚动时会被设置为5

  if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 4:
          print(1)
```

- pygame.MOUSEMOTION
  - 鼠标移动事件
- pygame.mouse.set_visible(False)
  - 设置界面鼠标是否可见，False为不可见
- pygame.mouse.get_pos() 
  - 获取光标位置


### 字体对象
- pygame.font
- pygame.font.get_fonts()
  - 获取所有可用字体名
- pygame.font.get_default_font()
  - 获取默认字体的文件名
- pygame.font.SysFont()
  - 创建系统文字对象
  ```
  # SysFont(name, size, bold=False, italic=False)
  ## name为系统文字名字
  ## size为字体大小
  # bold为是否为粗体
  # italic为是否为斜体
  ```
- pygame.font.Font()
  - 创建自定义字体对象

### 图像处理方法
- pygame.image
- 图像作为Surface对象加载
- pygame.image.load(文件名)
  - 从文件中加载图像

- pygame.Surface.set_colorkey()
  - 设置当前Surface对象的colorkeys，当绘制Surface对象时，将所有与colorkeys相同的颜色值绘制为透明

### 声音处理
- pygame.mixer
  - 控制声音的模块

- pygame.mixer.Sound(文件名)
  - 从文件或缓冲区对象创建一个新的Sound对象

方法|作用
-|-
pygame.mixer.Sound.play | 开始播放声音
pygame.mixer.Sound.stop | 停止声音播放
pygame.mixer.Sound.fadeout | 淡出后停止声音播放
pygame.mixer.Sound.set_volume | 设置此声音的播放音量[0.0-1.0]
pygame.mixer.Sound.get_volume | 获取播放音量
pygame.mixer.Sound.get_num_channels | 计算此声音播放的次数
pygame.mixer.Sound.get_length | 获取Sound的长度
pygame.mixer.Sound.get_raw | 返回Sound样本的字节串副本。

- pygame.mixer.music
  - 控制音乐的模块
- pygame.mixer.music.load(filename)
  - 载入一个音乐文件用于播放
  - 如果已经有音乐在播放，那么前一个音乐会被停止
- pygame.mixer.music.play() 
  - 开始播放音乐
- pygame.mixer.music.rewind()
  - 从新开始播放
- pygame.mixer.music.stop()
  - 结束音乐播放
- pygame.mixer.music.pause()
  - 暂停音乐播放
- pygame.mixer.music.unpause()
  - 回复音乐播放
- pygame.mixer.music.set_endevent(type)
  - 在播放结束后发出一个事件
```
# 结束播放后退出界面
pygame.mixer.music.set_endevent(pygame.QUIT)
```


### Surface对象
- pygame.Surface
- pygame中用于表示图像的对象
- pygame.Surface.blit()
  - 将一个Surface对象绘制到另一个Surface对象上
```
# blit(source, dest, area=None, special_flags = 0) -> Rect
# 将source指定的对象会知道该对象上，dest指定绘制的位置，area是一个Rect对象，表示限定source指定的Surface对象的范围
# 将ball Surface对象绘制到screen对象上的ballrect位置上，如果传入的是Surface对象，后一个参数会默认为对象的左上角坐标
screen.blit(ball,ballrect)
```
- pygame.Surface.blits()
```
# 绘制多个图像到对象上
screen.blits([(ball,ballrect),(ball,(300,300))])
```
- pygame.Surface.convert()
  - 修改图像的格式
  - 如果原来包含alpha通道，转换后不会保留
- pygame.Surface.convert_alpha()
  - 修改图像的格式
  - 会保留alpha通道
### 时间模块
- pygame.time
- pygame.time.get_ticks()
  - 以毫秒为单位获取时间
- pygame.time.wait() 
  - 暂停一段时间
- pygame.time.delay()
  - 暂停一段时间，使用处理器而不是休眠，所以比上一个要准确
- pygame.time.set_timer()
  - 在实践中队列上重复创建一个事件
- pygame.time.Clock()
  - 创建一个对象来帮助跟踪事件
- pygame.time.Clock.tick()
  - 更新clock对象
  - 用来控制帧率
### transform模块
- pygame.transform
- 移动像素或调整像素大小的操作，返回新的Surface
- 一些变换是破坏性的，会丢失像素数据，例如调整大小和旋转
- pygame.transform.flip()
  - 使垂直和水平翻转
```
# flip(Surface, xbool, ybool) -> Surface
# Surface为需要翻转的图像
# xbool为水平翻转
# ybool为垂直翻转
```
- pygame.transform.scale()
  - 调整大小到新的分标率
```
# scale(Surface, (width, height), DestSurface = None) -> Surface
# surface为要调整的对象
# (width, height)为要调整的大小
```
- pygame.transform.rotate()
  - 旋转图像
```
# rotate(Surface, angle) -> Surface
```
### 精灵对象
- pygame.sprite
- 用作游戏中不同类型对象的基类
- 在对Sprite进行子类化时，请务必在Sprite添加到Groups之前调用基本初始值设定项。 例如：
```
class Block(pygame.sprite.Sprite):

    #构建函数 传入颜色和它的x、y坐标
    def __init__(self, color, width, height):

       #调用父类（Sprite）的构建函数
       pygame.sprite.Sprite.__init__(self)

       #创建一个图像，用某个颜色填充
       #这也可以是从磁盘加载的图像
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       ＃获取具有图像尺寸的矩形对象
       ＃通过设置rect.x和rect.y的值来更新该对象的位置
       self.rect = self.image.get_rect()

```
- pygame.sprite.Sprite.update()
  - 控制精灵行为的方法，默认不执行任何操作，可以重写此方法
- pygame.sprite.Sprite.add()
  - 将精灵添加到组中
```
# add(*groups) -> None
# 可以将任意数量的Group实例作为参数传递，Sprite将被添加到它还不是其成员的组中
```
- pygame.sprite.Sprite.remove()
  - 从组中删除精灵
```
# remove(*groups) -> None
# 可以将任意数量的Group实例作为参数传递。 Sprite将从其当前所属的组中删除
```
- pygame.sprite.Group()
  - 用于保存和管理多个Sprite对象的容器类

方法|作用|解释
-|-|-
pygame.sprite.Group.sprites | 此组包含的Sprite列表|您也可以从组中获取迭代器，但在修改它时不能对组进行迭代。
pygame.sprite.Group.copy | 复制组
pygame.sprite.Group.add | 将Sprite添加到此组
pygame.sprite.Group.remove | 从组中删除Sprite
pygame.sprite.Group.has | 测试一个Group是否包含Sprite
pygame.sprite.Group.update | 在包含的Sprite上调用update方法|没有返回值
pygame.sprite.Group.draw | blit Sprite的图像
pygame.sprite.Group.clear | 在Sprites上绘制背景
pygame.sprite.Group.empty | 删除所有Sprite
- pygame.sprite.collide_rect_ratio() 
  - 使用rects检测两个精灵直接的碰撞
```
# collide_rect(left, right) -> bool
result = pygame.sprite.collide_rect_ratio( 0.5 )(sprite_1,sprite_2)
```
### 摄像头对象
- pygame.camera
- pygame.camera.list_cameras()
  - 返回一个可用的摄像头列表
```
# list_cameras() -> [cameras]

```
- pygame.camera.Camera()
  - 加载一个摄像头
```
# Camera(device, (width, height), format) -> Camera
# 加载一个V4L2摄像头，默认高宽为640x480，默认格式为RBG
# ca=pygame.camera.Camera(c[0],(640,640),'RGB')
```
方法|作用
-|-
pygame.camera.Camera.start | 打开摄像头、初始化然后开始捕捉画面
pygame.camera.Camera.stop | 结束摄像头工作，还原并关闭摄像头
pygame.camera.Camera.get_controls | 获得当前用户设定的值
pygame.camera.Camera.set_controls | 修改当前摄像头设置（如果摄像头支持的话）
pygame.camera.Camera.get_size | 返回被记录的图像的尺寸
pygame.camera.Camera.query_image | 确认一帧图像是否准备好
pygame.camera.Camera.get_image | 捕获一张图像并转换为一个 Surface 对象
pygame.camera.Camera.get_raw | 以字符串的形式返回一张未修改的图像
- pygame.camera.Camera.set_controls()
```
# set_controls(hflip = bool, vflip = bool, brightness) -> (hflip = bool, vflip = bool, brightness)
# 三个参数分别设置图像是否水平、垂直翻转，用整数值表示的图像亮度
```