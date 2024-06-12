## 介绍

Pillow库是一个Python的用于图像处理的第三方库。

## 安装Pillow模块

pillow和PIL不能在同一环境共存，在安装之前请卸载PIL模块

```python
pip install pillow

# 安装成功后，导包时要用PIL进行导包
from PIL import Image
```

## Image模块

在Pillow中，最常用的就是Image模块中的Image类

```python
# 导入Image模块
from PIL import Image
# 创建Image对象
im = Image.open('donation6.png')
print(im)
# 调用图片显示软件打开图片
# 打开后程序会堵塞
im.show()
'''
格式属性标识图像的源。如果未从文件中读取图像，则将其设置为“无”。size 属性是包含宽度和高度（以像素为单位）的 2 元组。mode 属性定义影像中波段的数量和名称，以及像素类型和深度。常见模式包括“L”（(luminance)）用于灰度图像，“RGB”用于真彩色图像，“CMYK”用于印前图像。
'''
print(im.format, im.size, im.mode)

'''
输出Image对象
<PIL.PngImagePlugin.PngImageFile image mode=RGBA size=1300x720 at 0x244FBA27FA0>
PNG (1300, 720) RGBA
'''
```

### 读取和写入图像