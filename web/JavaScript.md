# JavaScript

\[toc]

## 1.初识JavaScript

### 1.1什么是JavaScript？

JavaScript是运行在浏览器上的脚本语言。简称js

JavaScript运行在浏览器的内存当中

JavaScript程序不需要我们程序员手动编译，编写完源代码之后，浏览器直接打开解释执行

JavaScript的‘目标程序’以普通文本形式保存，这种语言叫做‘脚本语言’

脚本语言：不需要编译，运行过程中由js解释器逐行来进行解释并执行

现在也可以基于Node.js技术进行服务器编程

**js是一门事件驱动型的编程语言**

> 注意：事件与事件句柄的区别是：事件句柄是在事件单词前加一个on
>
> 1. 事件句柄是以HTML标签的属性存在的
> 2. 当页面打开的时候，js代码并不会执行，只是把js代码注册到对应的事件句柄上，当事件句柄发生后，注册在句柄上的js代码会被浏览器自动调用
> 3. js语句结束可以使用分号也可以不使用

### 1.2 JavaScript的作用

* 表单动态校验(密码强度检测)(js最初的目的)
* 网页特效
* 服务器端开发(Node.js)
* 桌面程序(Electron)
* APP(Cordova)
* 控制硬件-物联网(Ruff)
* 游戏开发(cocos2d-js)

### 1.3 HTML/CSS/JS的关系

> HTML/CSS标记语言-描述类语言

* HTML决定网页结构和内容(决定看到什么)，相当于人的身体
* CSS决定网页呈现给用户的模样(决定好不好看)。相当于衣服

> JS脚本语言-编程类语言

实现业务逻辑和页面控制(决定功能)，相当于人的各种动作

### 1.4 浏览器执行JS

浏览器分为两部分--渲染引擎和JS引擎

* 渲染引擎：用来解析HTML和CSS，俗称内核，比如Chrome的blink
* JS引擎：也称为JS解释器。用来读取网页中的JavaScript代码，对其处理后运行，比如Chrome的V8

浏览器本身并不会执行js代码，而是通过内置JavaScript引擎来执行js代码，。js引擎执行代码时会逐行解释每一句源码，然后由计算机去执行，所以JavaScript语言归为脚本语言

### 1.5 js组成

![image-20220816094311549](d://i/2023/03/05/image-20220816094311549.png)

ECMAScript是由ECMA国际(原欧洲计算机制造商协会)进行标准化的一门编程语言，这种语言在万维网上应用广泛，往往没称为JavaScript或JScript，但实际上后两者是ECMAScript语言的实现和扩展

![image-20220816094351130](https://d/i/2023/11/19/image-20220816094351130.png)

**DOM-文档对象模型**

**文档对象模型**是W3C组织推荐的处理可扩展标记语言的标准编程接口，通过DOM提供的接口可以对页面上的各种元素进行操作(大小位置等)

**BOM-浏览器对象模型**

浏览器对象模型，它提供了独立于内容的、可以与浏览器窗口进行互动的对象结构。通过BOM可以操作浏览器窗口，比如弹出框、控制浏览器跳转、获取分辨率等

## 2.HTML中怎么嵌入js代码

1.  直接把js代码写入HTML标签属性中

    ```html
    格式：<input type="button" value="hello" onclick="js代码">
    例如：<input type="button" value="hello" onclick="alert('hello js')">
    ```
2.  以脚本块的方式

    ```html
    格式：
    <script type='text/javascript'>
       		js代码
    </script>
    例如：
    <script type='text/javascript'>
       		alert('hello js!')
    </script>

    ```

    > 注意：暴露在脚本块当中的程序，在页面打开的时候执行，并且遵守自上而下的顺序依次逐行执行
    >
    > \==脚本块可以出现在任意位置，且可以出现多次==
    >
    > 注意单双引号的使用：在HTML中推荐使用`双引号`，在js中推荐使用`单引号`
3.  单独js文件，需要时导入

    ```html
    导入格式：
    <script type="text/javascript" src="js/js文件名"></script>
    ```

    > 注意：js代码文件中也会自上而下逐行执行
    >
    > js文件可以被引入多次

## 3.js的注释

1. 单行注释:// 单行注释
2. 多行注释:/\* 多行注释 \*/

## 4.JavaScript输入输出语句

![image-20220816101707208](d://i/2023/03/05/image-20220816101707208.png)

## 5.标识符与关键字

1. 标识符命名规则与规范按照java执行
   1. 命名规则
      1. 由字母、数字、下划线、美元符号组成
      2. 数字不能开头
      3. 严格区分大小写，长度无限制
      4. 不能出现关键字(name变量在某些浏览器中有定义，所以最好别使用)
   2. 标识符命名规范
      1. 包名都小写
      2. 类名、接口名：首字母大写，以后每个单词首字母大写
      3. 变量名、方法名：第一个单词首字母小写，后面每个单词首字母大写
      4. 常量名：字母都大写，多单词直接用下划线连接
2. 关键字不需要刻意去记

## 6.js中的变量

变量就是一个存放数据的容器。我们可以通过`变量名`获取数据，甚至修改数据

变量的本质是程序在内存中申请的一块用来`存放数据的空间`

* 强类型： 强类型语言是一种强制类型定义的语言，一旦某一个变量被定义类型，如果不经过强制转换，则它永远就是该数据类型了，强类型语言包括Java、.net 、C++等语言。
* 弱类型：弱类型语言是一种弱类型定义的语言，某一个变量被定义类型，该变量可以根据环境变化自动进行转换，不需要经过显性强制转换。弱类型语言包括vb 、PHP、javascript、Python等语言。
* JavaScript声明变量
  * var 变量名;
* 怎么给变量赋值
  * 变量名 = 值;
* 同时声明多个变量:多个变量之间用逗号隔开
*   声明变量特殊情况

    ![image-20220816103648530](d://i/2023/03/05/image-20220816103648530.png)

JavaScript是一种弱类型语言，没有编译阶段，一个变量可以随意赋值

> 注意：系统默认赋值为undefined

#### 5.1.全局变量与局部变量

1. 全局变量
   * 在函数体之外声明的变量属于全局变量
   * 全局变量的生命周期：
     * 浏览器打开时声明，浏览器关闭时销毁，尽量少用。因为全局变量会一直在浏览器的内存当中，耗费内存空间，能用局部变量尽量使用局部变量
2. 局部变量
   * 在函数体当中声明的变量，包括一个函数的形参
   * 局部变量的生命周期：
     * 函数开始执行时局部变量的内存空间开辟，函数执行结束之后，局部变量的内存空间释放

> 注意：若一个变量声明时没有加var关键字，则不管此变量在哪声明，都是全局变量

### 6.数据类型

在计算机中，不同的数据所需占用的存储空间是不同的，为了便于把数据分成所需内存大小不同的数据，充分利用存储空间，于是定义了不同的数据类型

1. 原始类型
   1. Undefined
   2. Number
   3. String
   4. Boolean
   5. Null
2. 引用类型
   1. Object以及Object的子类
   2. 数组
3. js中有一个运算符typeof，可以在程序的运行阶段动态的获取变量的数据类型
   1. 格式:typeof a == 'undefined'
   2.  运算符结果全为小写

       1. undefined
       2. number
       3. string
       4. boolean
       5. object
       6. function

       > 注意:当变量赋值为Null时，typeof结果为object

> 注意：ES6(ECMAScript规范)之前只有六种数据类型，之后加了Symbol类型

* Undefined类型
  * 这种类型只有一个undefined值
  * 当一个变量没有手动赋值，系统自动赋值undefined
*   Number类型

    * 包括所有的数字以及NaN(不是数字)，Infinity(无穷大)

    > \==NaN==出现在运算结果本应是一个数字，最后的结果却不是一个数字
    >
    > \==Infinity==当除数为0时，结果为无穷大
    >
    > Number.MAX\_VALUE：数字型的最大值\
    > Number.MIN\_VALUE：最小值

    * isNaN函数
      * 用法isNaN(数据)，返回Boolean，表示是否为一个数字
    * parseInt()
      * parseInt(数据):可以将字符串自动转换为数字，并且取整数位
    * parseFloat()
      * parseFloat(数据):可以将字符串自动转换为数字
    * Math.ceil
      * Math.ceil(数据):向上取整
* Boolean类型
  * 包括true和false
  * Boolean()
    * Boolean(数据):将非布尔类型转换成布尔类型
    * 一般是有就转换为真，没有就转换为假
* Null类型
  * 包括null
* String类型
  *   在js中字符串可以用单引号也可以用双引号

      ```javascript
      // 创建字符串对象
      1. var s = 'asb'
      2. var s = new String('asd')
      /*
      第二种使用了js内置的支持类String，s为object类型
      但两种对象的方法都是一样的
      */
      ```

      ```js
      //String常用的属性
      属性：length  //获取字符串长度
      用法：String对象.length

      //string常用函数
      indexOf 	//获取指定字符串在当前字符串第一次出现的索引
      lastIndexOf	//获取指定字符串在当前字符串最后一次出现的索引
      replace		//替换
      substr		//截取子字符串
      substring	//截取子字符串
      toLowerCase	//转换小写
      toUpperCase	//转换大写
      split		//拆分字符串
      trim		//去除前后空白

      //实例
      x = '123456'
      //索引
      alert(x.indexOf('1')) //0
      alert(x.lastIndexOf('7')) //-1

      //替换
      alert(x.replace('1','2')) //把1换成2，替换一个，想全部替换需要正则表达式

      //截取子字符串
      alert(x.substr(2,4)) //3456
      alert(x.substring(2,4)) //34

      t = " 456 "
      //去除前后空白
      alert(x.trim())	//456
      ```
*   Object类型

    * 是所有类型的超类，自定义的类默认继承Object

    ```js
    //Object常用的属性
    prototype属性//作用是给类动态的扩展属性和函数
    constructor

    //函数
    toString()
    valueOf()
    toLocaleString()
    ```
*   数组类型

    ```js
    // 定义
    1. var h = new Array('1','2','3')
    2. var h = ['1','2','3']
    ```

#### 6.1.null NaN undefined区别

1. **数据类型不一样**
2. **null和undefined可以等同**

> 注意：
>
> \==(等同运算符) 只比较值
>
> \===(全等运算符) 即比较值，也比较数据类型

### 7.js中的函数

函数就是一段完成某个特定功能且可以被重复利用的代码片段

```javascript
格式1：
function 函数名(形式参数列表){
	函数体
}
格式2:
函数名 = function(形式参数列表){
	函数体
}
例如：
function sum(a,b){
	alert(a+b)
}
sum(10,20)

例如:
sayHello = function(username){
	alert('hello' + username)
}
sayHello('zsan')
```

> 注意：js中的形式参数列表相当于python中的默认值参数，若函数调用时不主动传参，则参数使用默认值undefined

* 回调函数
  * 自己写出来一个函数，但是自己不调用这个函数，由其他程序负责调用该函数
  * 例如事件注册的第一种方式

### 8.js的类

* 定义类的方法与new对象

```js
第一种：
function 类名(形参){

}
第二种:
类名 = function(形参){

}
创建对象的语法:
new 构造方法名(实参)//构造方法名与类名一致

例如：
var obj = new sayHello()

//在js中构造函数和类的定义是放在一起来完成的
function User(a,b,c){
    this.sno = a
    this.sname = b
    this.sage = c
}
var u1 = new User(111,'zhangsan',30)

//访问一个类中的属性的方法
1. u1.sno
2. u1['sno']

//在类中定义方法
Product = function(a,b,c){
    this.getPrice = function(){
        return 0
    }
}

var p1 = new function(1,2,3)
alert(p1.getPrice())

//通过prototype属性动态扩展属性以及函数
Product.prototype.getA = function(){
    return a
}
Product.prototype.name = a
```

> 注意：要是没有new就是函数，要是new则把函数看成类

### 9.js事件

| 事件名称      | 事件详情      |
| --------- | --------- |
| blur      | 失去焦点      |
| focus     | 获得焦点      |
| keydown   | 键盘按下      |
| keyup     | 键盘弹起      |
| click     | 鼠标单击      |
| dblclick  | 鼠标双击      |
| mousedown | 鼠标按下      |
| mouseover | 鼠标经过      |
| mousemove | 鼠标移动      |
| mouseout  | 鼠标离开      |
| mouseup   | 鼠标弹起      |
| load      | 页面加载完毕    |
| change    | 下拉列表选择项改变 |
| reset     | 表单重置      |
| submit    | 表单提交      |
| select    | 文本被选定     |

*   注册事件的方式

    ```js
    1. 直接在标签中使用事件句柄
    <input type='button' value="hello" onclick="sayHello()">
       
    2.纯js代码完成事件的注册
    	1. 先拿到按钮对象
        	<input type='button' value="hello" id="mybtn">
        	var btnObj = document.getElementById("mybtn")//document代表整个html页面
    	2. 给按钮onclick属性赋值
    		btnObj.onclick = doSome//注意加小括号是错误的
    ```

### 9.1.js代码执行顺序

**js中可以直接window.onload = 函数名来让函数在页面加载完后在执行，避免因代码执行顺序而导致的获取节点为空的错误**

#### 9.2.js键盘事件

```js
user.onkeydown = function(event){
    //对于键盘事件来说，都有keyCode属性来获取键值
    alert(event.keyCode)
}
```

### 10.js运算符之void

* 格式：void(表达式)
* 执行括号里的表达式但不返回任何结果

```html
<a href="javascript:void(0)">点击链接不跳转</a>
/*
javascript:表示告诉浏览器后面是一段js代码，不能省略
*/
```

### 11.js的控制语句

1. if
2. switch
3. while
4. do.....while...
5. for循环
6. break
7. continue

```js
//创建数组
var arr = [false,true,1,2]
```

### 12.js的DOM，BOM编程

**ECMAScript是EAMA指定的262标准，JavaScript和script都准守这个标准，ECMAScript是JavaScript的核心语法**

*   DMO(文档对象模型)编程是通过JavaScript对HTML中的dom结点进行操作，DOM是有规范的，DOM规范是w3c制定的

    ```js
    var obj = decument.getElementById("id")
    ```
* BMO(浏览器对象模型)编程是对浏览器本身操作，例如：前进。后退、地址栏、关闭窗口、弹窗等。由于浏览器有不同的厂家制造，所以BOM缺少规范，一般只是有一个默认的行业规范
* 两者的区别于联系
  * BOM的顶级对象是：window
  * DOM的顶级对象是：document
  * BOM包括DOM

### 13.innerHTML与innerText

* 相同点
  * 两者都是属性
  * 都是设置元素内部的内容
* 不同点
  * innerHTML会把后面的字符串当做一段HTML代码解释并执行
  * innerText即使后面是一段HTML代码，也只是将其当做普通的字符串

### 14.js的正则表达式

* 什么是正则表达式？有什么用？
  * 正则表达式主要用在字符串格式匹配方面
  * 大部分编程语言都支持正则表达式

| 常见的正则符号   | 用法                    |
| --------- | --------------------- |
| .         | 匹配除换行符以外的任意字符         |
| \w        | 匹配字母或数字或下划线或行子        |
| \s        | 匹配任意的空白符              |
| \d        | 匹配数字                  |
| \b        | 匹配单词的开始或结束            |
| ^         | 匹配字符串的开始              |
| $         | 匹配字符串的结束              |
| \*        | 重复零次或更多次              |
| +         | 重复一次或更多次              |
| ？         | 重复零次或一次               |
| {n}       | 重复n次                  |
| {n，}      | 重复n次或更多次              |
| {n，m}     | 重复n到m次                |
| \W        | 匹配任意不是字母，数字，下划线，汉字的字符 |
| \S        | 匹配任意不是空白字符的字符         |
| \D        | 匹配任意不是数字的字符           |
| \B        | 匹配不是单词开头或结束的位置        |
| \[^x]     | 匹配不是x的任意字符            |
| \[^aeiou] | 匹配不是aeiou这几个字母的任意字符   |
| \[]       | 表示可以出现的字符             |

* 创建正则表达式对象
  1. var regExp = /正则表达式(字符串)/flags
  2. var regExp = new RegExp("正则表达式(字符串)","flags")
  3. flags参数
     1. i：忽略大小写
     2. g：全文查找
     3. m：多行查找(ES规范指定之后才支持m)
        * 若是正则表达式则忽略m参数
* 正则对象的text函数
  * true/false = 正则表达式对象.text(用户填写的字符串)

### 15.内置类-Date

**Date用来获取时间/日期**

*   获取当前系统时间

    ```js
    var nowTime = new Date()
    document.write(nowTime)
    ```
*   把时间转换为本地语言环境的日期格式

    ```js
    nowTime = nowTime.toLocaleString()
    ```
*   自定制时间格式

    ```js
    getFullYear() //获取全部年份
    getMonth()    //获取月份是0-11
    getDay()      //获取一周中的第几天，0-6
    getDate()	  //获取日信息
    getTime()	  //获取从1970年1月1日 00:00:00 000 到当前系统时间的总毫秒数，一般把这个毫秒数当成时间戳

    var t = new Date()

    ```

### 16.周期函数setInterval

```js
// 格式
setInterval(code,millisec)
/*
code:要调用的函数
millisec:周期性调用code的毫秒数

这个方法的返回值可以传递给window.clearInterval()从而取消对code的调用
*/
//例如
<script>
        function up() {
            var time = new Date()
            document.getElementById('1').innerHTML = time.toLocaleString()

          }
        function start() {
            v = window.setInterval("up()",1000)
        }

        function stop() {
          window.clearInterval(v)
          }
  </script>
    <div id="1"></div>
    <input type="button" value="stop" onclick="stop()">
    <input type="button" value="up" onclick="start()">




```

### 17.内置类Array

```js
//创建数组
//数组可以自动扩容
var arr = []
var arr2 = [1,2,false]

//创建数组
var a = new Array(数组长度/数组内容)

//常用函数
join(一个连接元素) //把数组里面的值用连接元素连接
push(多个元素)  //在数组的末尾加一个元素
pop() 			//将末尾元素弹出
reverse()		//将数组反转
//例如
var a=[1,2,3]
alert(a.join('-')) //1-2-3
a.push(1,2,3)
alert(a)   // 1,2,3,1,2,3
alert(a.pop()) //3
alert(a.reverse()) //2,1,3,2,1
```

### 18.BOM编程

**BOM编程中，window对象时顶级对象，代表浏览器窗口**

#### 18.1.window的close(),open()

```js
/*
open(完整url)		打开窗口
close()		关闭窗口
*/

//例如
 <input type="button" value="当前窗口"onclick="window.open('https://www.baidu.com','_self')">
<input type="button" value="新窗口(默认)" onclick="window.open('https://www.baidu.com','_blank')">
<input type="button" value="父窗口" onclick="window.open('https://www.baidu.com','_parent')">
<input type="button" value="顶级窗口" onclick="window.open('https://www.baidu.com','_top')">
<input type="button" value="关闭窗口" onclick="window.close()">
```

#### 18.2.弹窗

```js
alert('文本')			//消息框
confirm('文本')		//确认框，返回true或false
```

#### 18.3.历史记录

```js
window.history.back()       // 页面后退
window.history.go(前进距离)  // 页面前进
```

#### 18.4.设置顶级窗口

```js
<iframe src="004.html"></iframe> 
 
 
 004页面
 <script>
 	function settop(){
 		if(window.top !== window.self){
		 window.top.location = window.self.location
 		}
 }
 </script>
 <input type="button" value="设置顶级窗口" onclick="settop()">
```

#### 18.5.地址栏对象

```js
<script>
    function gobaidu() {
    	var local = window.location //创建对象
        local.href = 'https://www.baidu.com'
    	// document.location.herf 等效
        }
</script>
<input type="button" value="百度" onclick="gobaidu()">
```

* 总结：浏览器往服务器发请求方法：
  1. 表单form的提交
  2. 超链接
  3. document.location
  4. window.location
  5. window.open()
  6. 直接在浏览器地址栏输入url
* **以上方法均可以携带数据给服务器，只有通过表单提交的数据才是动态的**

### 19.json

* 什么是json？
  * JavaScript Object Notation，简称json
  * 一种标准轻量的数据交换格式
  * 主要用于数据交换
* 特点：体积小，易解析
* 市面上流行的数据交换格式一种是json一种是xml
* xml特点：体积大，解析麻烦，但是优点是语法严谨

```json
//语法格式：
var jsonObj = {
    "属性名" : 属性值,
    "属性名" : 属性值,
    .......
    "属性名" : 属性值
};//属性值可以是任意类型

 // json对象
        var jsonObj = {
            "sno" : "110",
            "sname" : "张三",
            "sex" : "男"
        };
        alert(jsonObj.sno+','+jsonObj.sname+','+jsonObj.sex)
        //json数组
        var student = [
            {"sno" : "110", 
             "sname" : "张三", 
             "sex" : "男"},
            {"sno" : "110", 
             "sname" : "王五", 
             "sex" : "男"},
            {"sno" : "110", 
             "sname" : "李四", 
             "sex" : "男"}
        ]
        for(var i=0;i<student.length;i++){
            alert(student[i].sno+','+student[i].sname+','+student[i].sex)
        }
```

* eval函数
  *   **eval函数的作用是把一段字符串当成js代码解释并执行**

      ```js
      window.eval('var i =100')
      alert('i = '+ i)//100
      ```

### 20.简单实战

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
  <script>
    var data = {
      "total" : 4,
        "emp" : [
            {"empno" : 7369,"ename" : "SMITH","sal" : 800.0},
            {"empno" : 7369,"ename" : "SMITH","sal" : 3800.0},
            {"empno" : 7369,"ename" : "SMITH","sal" : 2800.0},
            {"empno" : 7369,"ename" : "SMITH","sal" : 4800.0},
        ]
    }
    window.onload = function () {
        document.getElementById('displaybtn').onclick = function () {
            var emps = data.emp
            var html = ""
            for(var i = 0; i < emps.length; i++){
                var emp = emps[i]
                html += "<tr>"
                html += "<td>"+emps.empno+"</td>"
                html +=  "<td>"+emps.ename+"</td>"
                html +=  "<td>"+emps.sal+"</td>"
                html +=  "</tr>"
            }
            document.getElementById("settbody").innerHTML = html
            document.getElementById('count').innerText = data.total
        }
    }
  </script>
    <!--点击显示表格信息 -->
    <input type="button" value="显示员工信息" id="displaybtn">
    <!-- 希望吧数据展示到table中 -->
    <table border="1px" width="50%">
        <tr>
            <th>员工编号</th>
            <th>员工名字</th>
            <th>员工薪资</th>
        </tr>
        <tbody id="settbody">
        </tbody>
    </table>
  总共<span id="count">0</span>条记录
</body>
</html>
```

### 21.jQuery基础

jQuery是一个轻量级的，写得少、做得多的JavaScript函数库

包含以下功能：

1. HTML元素选取
2. HTML元素操作
3. CSS操作
4. HTML事件函数
5. JavaScript特效和动画
6. HTML DOM遍历和修改
7. Ajax
8. Utilities

**21.1.引入jQuery**

从官方下载jQuery库，jQuery实际是一个JavaScript文件可以用JavaScript方式引入

\[下载地址]\([Download jQuery | jQuery](https://jquery.com/download/))

下载页面中有两个版本：

1. Production version：用于实际网站中，已被精简和压缩
2. Development version：用于测试和开发中(未被压缩，是可读的代码)

**21.2.jQuery基本语法**

1. **查询HTML元素并对它们执行对应的操作**

```javascript
$(selector).action()
/* 
$ 用于定义jQuery
selector选择符用于指明要查询的HTML元素
action()函数用于执行对元素的操作
*/

1. $(this).hide() //当前元素隐藏
2. $('p').hide()	//所有p元素隐藏
3. $('p.test').hide() //class=test的p元素隐藏
4. $('#test').hide() // id=test的元素隐藏 
```

> 大多数情况下，jQuery函数位于document ready函数中

```js
$(document).ready(function(){
    // 开始写jQuery代码
})
// 为了防止文档在加载前运行jQuery代码
// 也可以简化为
$(function(){
    // 写jQuery代码
})
```

2. **jQuery选择器**

元素\
元素

| 语法                         | 描述                                            |
| -------------------------- | --------------------------------------------- |
| $('\*')                    | 选取所有元素                                        |
| $(this)                    | 选取当前HTML元素                                    |
| $('p.intro')               | <p>选取class=intro的</p><p>元素</p>                |
| $('#intro')                | 选取id=intro的元素                                 |
| $('p:first')               | <p>选取第一个</p><p>元素</p>                         |
| $('ul li:frist')           | <p>选取每一个</p><ul><li>的第一个</li><li>元素</li></ul> |
| $('ul li:first-child')     | <p>选取每一个</p><ul><li>的第一个</li><li>元素</li></ul> |
| $('\[href]')               | 选取带有href属性的元素                                 |
| $('a\[target="\_blank"]')  | 选取所有target属性值等于'\_blank'的元素                   |
| $('a\[target!="\_blank"]') | 选取所有target属性值不等于'\_blank'的元素                  |
| $(':button')               | 选取所有type=‘button’的和元素                         |
| $('tr:even')               | 选取偶数位置的                                       |
|                            |                                               |
| $('tr:odd')                | 选取奇数位置的                                       |
|                            |                                               |

3.  **jQuery事件**

    | 鼠标事件       | 键盘事件     | 表单事件   | 文档/窗口事件 |
    | ---------- | -------- | ------ | ------- |
    | click      | keypress | submit | load    |
    | dblclick   | keydown  | change | resize  |
    | mouseenter | keyup    | focus  | scroll  |
    | mouseleave |          | blur   | unload  |
    | hover      |          |        |         |

    ```js
    // 在页面指定一个单击事件
    $('p').click()

    //双函数，移动到元素上时会触发第一个函数，离开时会触发第二个函数
    $(document).ready(function(){
    	$('#p1').hover(
        	function(){
                alert('鼠标已经悬停在p1元素上了')
            }
            function(){
                alert('鼠标已经离开在p1元素上了')
            }
        )
    })
    ```
4. 获取内容和属性
5.  获得内容三方法

    text()：设置或返回所选元素的文本内容

    html():设置或返回所选元素的内容（包括HTML标记）

    val():设置或返回表单字段的值

```js
// text()和html()
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="jquery.js"></script>
    <script>
        $(document).ready(function(){
            $('#btn1').click(function(){
                alert('Text:'+$('#test').text())
            })// 显示：Text:这是段落中的粗体文字

            $('#btn2').click(function(){
                alert('HTML:'+$('#test').html())
            })// 显示：这是段落中的<b>粗体</b>文字
        })
    </script>
</head>
<body>
    <p id='test'>这是段落中的<b>粗体</b>文字 </p>
    <button id='btn1'>显示文本</button>
    <button id='btn2'>显示</button>
</body>
</html>


// val()获取表单数据
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="jquery.js"></script>
</head>
<body>
  <form action="" method="post">
      <div>
          <label for="username">用户名：</label>
          <input type="text" name="username" id="username">
      </div>
      <div>
          <label for="password">用户名：</label>
          <input type="password" name="password" id="password">
      </div>
      <div>
          <button id="btn" type="submit" name="submit">提交</button>
      </div>
  </form>
<script>
    $('#btn').click(function (){
        var username = $('#username').val()
        var password = $('#password').val()
        if (username.length<2){
            alert('用户名长度不能小于2')
            return false
        }
        if (password.length<6){
            alert('密码长度不能小于6')
            return false
        }

    })
</script>
</body>
</html>
```

5.  获得属性

    attr('属性名'): 获取属性

    attr('属性名','属性值'): 设置属性

```js
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="jquery.js"></script>
</head>
<body>
    <div>
        <a id="test" href="https://www.baidu.com"> 大学习</a>
    </div>
    <button id="btn1">获取url</button>
    <button id="btn2">修改url</button>
    <script>
        $('#btn1').click(function (){
            var url = $('#test').attr('href')
            alert(url)
        })
        $('#btn2').click(function (){
            $('#test').attr('href','www.baidu.com')
            var url = $('#test').attr('href')
            alert(url)
        })
    </script>
</body>
</html>
```
