## openpyxl

### 安装openpyxl

```
pip install openpyxl
```

### openpyxl基本操作

- 创建工作簿

  ```
  # 创建出来就会自带一个表
  wb = Workbook()
  ```

- 获取第一个工作表

  ```
  wb.active
  ```


- 获取全部表对象

  ```
  wb.worksheets
  ```

- 创建一个新工作表

  ```
  # 新建一个name表，插入到第零个位置
  ws=wb.create_sgeet('name',0)
  ```

- 修改表名

  ```
  ws.title='New Title'
  ```

- 创建表对象

  ```
   ws3 = wb["New Title"]
  ```

  

- 修改选项卡的颜色

  ```
  ws.sheet_properties.tabColor = "1072BA"
  ```

- 查看所有表的名字

  ```
  wb.sheetnames
  ```

- 遍历工作表

  ```
  for i in wb:
  	print(i.title)
  ```

- 创建工作表的副本

  ```
  source = wb.active
  target = wb.copy_worksheet(source)
  ```

- 修改单元格的值

  ```
  ws['A4']=4
  或者
  d = ws.cell(row=4, column=2, value=10)
  ```

- 访问多个单元格

  ```python
  # 使用切片访问单元格
   cell_range = ws['A1':'C2']
  # 获取多行数据
  for row in ws.iter_rows(min_row=1, max_col=3, max_row=2):
   	for cell in row:
        print(cell)
  # 获取多列数据
  for col in ws.iter_cols(min_row=1, max_col=3, max_row=2):
  ...     for cell in col:
  ...         print(cell)
  ```

- 写入多个值

  ```
  date1=['小梦'，25，‘广东]
  ws.append(data1)
  ```

- 访问文件所有行与列与值

  ```python
  # 行
  ws.rows
  # 列
  ws.columns
  # 值
  ws.values
  ```

- 保存文件

  ```
  wb.save('文件路径')
  ```

- 加载文件

  ```
  from openpyxl import load_workbook
  wb2 = load_workbook('test.xlsx')
  ```

- 使用公式

  ```
  ws['A1']='=SUM(1,1)'
  ```

- 合并单元格

  ```python
  from openpyxl.workbook import Workbook
  >>>
  >>> wb = Workbook()
  >>> ws = wb.active
  >>>
  >>> ws.merge_cells('A2:D2')
  >>> ws.unmerge_cells('A2:D2')
  >>>
  >>> # or equivalently
  >>> ws.merge_cells(start_row=2, start_column=1, end_row=4, end_column=4)
  >>> ws.unmerge_cells(start_row=2, start_column=1, end_row=4, end_column=4)
  ```

- 查看表中内容范围

  ```
  print(sheet.dimensions)
  ```

- 在某行或某列插入或删除多行多列

  ```
  # 在idx行上插入4行
  ws.insert_rows(idx=2,amount=4)
  
  # 在idx行开始删除4行，包括idx
  ws.delete_rows(idx=2,amount=4)
  
  # 在idx列左边插入4列
  ws.insert_cols(idx=2,amount=4)
  
  # 在idx列开始删除4列，包括idx
  ws.delete_cols(idx=2,amount=4)
  ```

- 移动范围数据

  ```
  # 数字为正向下或向右
  ws.move_range('C1:D2',rows=3,clos=-2)
  ```

- 设置字体样式

  ```python
  from openpyxl.styles import Font
  # name字体名称，size大小，bold粗体，italic斜体，color颜色
  font = Font(name,size,bold,italic,color)
  ws['A4'].font=font
  ```

- 设置对齐样式

  ```python
  from openpyxl.styles import Alignment
  # 水平对齐，垂直对齐，字体倾斜度，自动换行
  alignment=Alignment(horizontal,vertical,text_rotation,wrap_text)
  ws['A4'].alignment=alignment
  ```

- 设置边框样式

  ```python
  from openpyxl.styles import Side,Border
  # 边线样式，边线颜色
  side=Side(style,color)
  # 左右上下
  border=Border(left,right,top,bottom)
  ```

- 设置单元格填充样式

  ```
  from openpyxl.styles import PatternFill,GradientFill
  # 单色填充
  pattern_fill=PatternFill(fill_type,fgColor)
  # 渐变填充
  gradient_fill=GradientFill(stop=('FFFFFF','99ccff','000000'))
  ```

- 设置行高和列宽

  ```python
  # 设置一行的高度
  ws.row_dimensions[1].height=50
  # 设置一列的宽度
  ws.column_dimensions['C']=20
  ```

  















