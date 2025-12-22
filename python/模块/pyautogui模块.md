# pyautogui模块概述

## 安装pyauto库

```
pip install pyautogui
```

## 基础功能

*   报错机制

    ```
    pyautogui.FAILSAFE=False

    # 默认为True，当鼠标的指针在屏幕的最上方程序会报错
    ```
*   停顿功能

    ```
    pyautogui.PAUSE=1

    # 每条pyauto指令会暂停一秒，其他指令不会停止
    ```

## 鼠标功能

*   获取屏幕分辨率

    ```
    x,y=pyautogui.size()
    # 获取屏幕的分辨率
    ```
*   获取鼠标当前位置

    ```
    pyautogui.position()
    # 获取鼠标当前位置
    ```
*   移动鼠标

    ```
    pyautogui.moveTo(x=300,y=300,duration=1)
    # 鼠标移动到x=300，y=300的位置，耗时1秒
    # moveRel()移动的是相对位置
    # 所有的pyautogui指令都有duration参数，控制速度
    ```
*   拖拽鼠标

    ```
    pyautogui.dragTo()
    pyautogui.dragRel()
    # 按住鼠标移动，参数与用法与moveTo/moveRel用法一样
    ```
*   按住与松开鼠标

    ```
      pyautogui.mouseDown()
      # 按下
      pyautogui.mouseUp()
      # 松开
    ```
*   单击鼠标

    ```
    pyautogui.click(x=300,y=300,button='right')
    # 在x=300，y=300的位置点击右键，默认为左键，middle为中键

    pyautogui.click(clicks=2,interval=0.25)
    #clicks参数设置点击次数 interval参数设置间隔时间
    ```
*   双击鼠标

    ```
    pyautogui.doubleClick(x=300,y=300,button='right')
    # 双击鼠标，参数与click()一致
    ```
*   控制鼠标滚轮滚动

    ```
    pyautogui.scroll(300)
    # 向上滚动300像素，负数为向下
    ```

## 屏幕处理

*   截取屏幕

    ```
    img=pyautogui.screenshot()
    # 没有参数则截取整个屏幕

    img=pyautogui.screenshot((20,20,20,20))
    img=pyautogui.screenshot(region=(20,20,20,20))
    # 截取左上顶点坐标为(20,20),宽为20，长为20的一个图像
    ```
*   保存截图

    ```
    img.save('pm1.jpg')
    # 保存为pm.jpg

    img=pyautogui.screenshot('pm2.jpg')
    # 截取并保存为pm2.jpg
    ```
*   获取某位置像素色彩

    ```
    img=pyautogui.screenshot()
    print(img.getpixel(300,300))
    # 输出截图的x=300,y=300位置的像素色彩的RGB三原色组
    ```
*   色彩对比

    ```
    pyautogui.getpixelMatchesColor(200,200,(255,0,0))
    # 对比(200，200)位置的像素色彩与(255,0,0)色彩，返回布尔值
    ```
*   匹配图像

    ```
    pyautogui.locateOnScreen('zan.png')
    # 匹配当个图像，返回匹配图像左上顶点坐标和长宽,可以加grayscale=True打开灰度匹配，提升匹配速度

    pyautogui.locateAllOnScreen('zan.png')
    # 匹配多个图像位置
    ```
*   获取图像中心位置

    ```
    pyautogui.center(200,200,200,200)
    # 得到(200,200)位置,宽200，长200图像的中心位置

    pyautogui.locateCenterOnScreen('zang.png')
    # 找到匹配图像，返回图像中心坐标
    ```

## 键盘

*   按住松开键

    ```
    pyautogui.keyDown('shift')
    # 按住shift

    pyautogui.Up('shift')
    # 松开shift
    ```
*   按下键

    ```
    pyautogui.press('shift')
    # 按下shift
    ```
*   按下组合键

    ```
    pyautogui.hotkey('win','r')
    # 按下win+r
    ```
*   输出内容

    ```
    pyautogui.typewrite(message='hello python',interval=1)
    # 输出hello python 用时1s，输出不了中文
    ```
*   输出中文

    ```
    import pyperclip
    pyperclip.copy()
    # 复制内容在粘贴板
    pyperclip.paste()
    # 提取粘贴板内容
    # 可以使用ctrl+v输出中文
    ```
*   上下文管理器

    ```
    with pyautogui.hold('shift'):
      pyautogui.press(['r','w'])

    相当于
     pyautogui.keyDown('shift')
     pyautogui.press('r')    
     pyautogui.press('w')   
     pyautogui.keyUp('shift')    
    ```

## 键盘映射

| 键盘字符串                          | 键盘按键              |
| ------------------------------ | ----------------- |
| enter(return\|\n)              | 回车                |
| esc                            | ESC键              |
| shiftleft,shiftright           | 左右SHIFT键          |
| altleft,altright               | 左右ALT键            |
| ctrlleft,ctrlright             | 左右CTRL键           |
| tab,                           | TAB键              |
| backspace,delete               | BACKSPACE、DELETE键 |
| pageuo,pagedown                | PAGEUP和PAGEDOWN键  |
| home,end                       | HOME和END键         |
| up,down,left,right             | 箭头键               |
| f1,f2,f3....f12                | F1到F12键           |
| volumemute,volumedown,volumeuo | 声音变大变小建（有的键盘没有）   |
| pause                          | PAUSE键（暂停键）       |
| capslock                       | CAPSLOCK键         |
| numlock                        | NUMLOCK键          |
| scrolllock                     | SCROLLLOCK键       |
| insert                         | INSERT键           |
| printscreen                    | PRINTSCREEN键      |
| winleft,winright               | 左右win键            |

## 框内容

*   提示框

    ```
    pyautogui.alert(text='hello',title='alert')
    ```
*   选择框

    ```
    pyautogui.confirm(text='死鬼，来了？',title='你的选择',buttons=['滚！','死鬼！'])
    # buttons参数为自己设置按钮
    ```
*   密码输入框

    ```
    p.password('请输入密码！','密码',default='110',mask='*')
    # 第三个参数为默认值,第四个参数为输入表现形式
    ```
*   普通输入框

    ```
    pyautogui.prompt('请输入')
    ```
