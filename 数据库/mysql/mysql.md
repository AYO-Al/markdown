## 1、什么是数据库？

- 数据库：英文单词Database,简称DB。按照一定格式存储数据的一些文件的组合。实际上就是一堆文件。这些文件中存储了具有特定格式的数据
- 数据库管理系统：DataBaseManagement，简称DBMS。专门用来管理数据库中的数据的，数据库管理系统可以对数据库当中的数据进行增删改查
- 数据库管理员：DataBaseAdministrator，简称DBA
- 常见的数据库管理系统：MySQL、Oracle、MS、SqlServer、DB2、sybase等
- SQL：结构化查询语句，程序员通过SQL语句，然后DBMS负责执行SQL语句，最终完成对数据库中数据的增删改查
- 三者关系：DBMS--执行-->SQL语句--操作-->DB
- mysql数据库启动的时候，这个服务占有的默认端口号为3306
### 2、通过命令启动或停止mySQL服务
- net stop 服务名：停止服务
- net start 服务名：开始服务
### 3、登录mysql
- cmd中输入：mysql -u账号 -p密码，登录
- 不显示密码：mysql -u账号 -p直接回车再输入密码，密码则为不可见
- 如果是连接另外的机器则再加一个参数-h机器ip
### 4、数据库的基本知识

- 注释：
  1. \# 注释内容
  2. /*  注释内容  */
  3. -- 注释内容

- 数据库当中最基本的单元是表：table
- 数据库中都是以表格的形式表示数据的，因为表比较直观
- 任何一张表都有行和列
```
# 行（row）：被称为数据/记录
# 列（column）：被称为字段
# 每一个字段都有：字段名、数据类型、约束等属性
姓名    年龄（列：字段）
-----------------------
张三    20   （行：数据/记录）
```
- 数据库标识符命名规范：全部小写，单词与单词之间使用下划线衔接
- 数据库的增删改查：CRUD
- SQL语句的分类：

类别|具体
-|-
DQL|数据查询语言（凡是带有select关键字的都是查询语言）
DML|数据操作语言（凡是对表中数据进行增删改的都是DML）
DDL|数据定义语言（主要操纵的是表的结构。不是表中的数据）
TCL|事务控制语言（事物提交、事物回滚....）
DCL|数据控制语言（授权、撤销权限....）
- 导入sql文件：source 文件路径，注意路径中不要有中文
  - sql文件为数据库脚本文件
  - 执行sql文件的时候该文件中所有的sql语句会全被执行
- 在所有数据库当中，字符串同一用单引号，单引号是标准，双引号在oracle中不能使用，mysql中可以
- 数据库当中null不能使用等号进行衡量。需要使用is null，因为数据库中的null代表什么也没有，不是一个值
- 数据库中只要有null参与运算最后结果都为空

### 5、mysql常用命令
命令|作用|具体说明
-|-|-
\c|终止命令的输入|
exit|退出mysql|
select version();|查看mysql数据库版本号|
select database();|查看当前使用的数据库|
show databases;|查看所有数据库|
use 数据库名称|使用数据库|
create database 数据库名称;|创建数据库|
drop database 数据库名称;|删除数据库|
show tables;|查看数据库全部表|
select * from car;|查看表中数据|从car表中查询所有数据，*代表全部
desc 表名;|查看表的结构|
show create table 表名;|显示创建表时的语句|
select @@transaction_isolation;|查看隔离级别|
select @@配置|查看mysql配置|
set @@配置|设置mysql配置|
<span style="color:red">以上命令不区分大小写</span>||

### 6、查询操作
- 如果select后接字面值，查询的结果会借助表结构得到的查询结果会全是字面值

```
select 'abc' from emp;
+-----+
| abc |
+-----+
| abc |
| abc |
| abc |
| abc |
| abc |
| abc |
| abc |
| abc |
| abc |
| abc |
| abc |
| abc |
| abc |
| abc |
+-----+
```
#### 6.1、简单查询
- 查询一个字段
  - select 字段名 from 表名;
  - select和from都是关键字
  - 字段名和表名都是标识符
- 查询多个字段
  - select 字段名,字段名 from 表名;
- 查询所有字段
  - select * from 表名;
  - 效率低，可读性差，实际开发中不建议使用
- 给查询列取别名
  - select 字段名 as 别名 from car;
  - 只会更改查询结果字段名，数据库中不会更改
  - select 字段名 别名 from car;as关键字可以省略
  - 当别名里面有空格，可以把别名用''或""括取来，不然会报错
  - 别名可以使用中文
- 字段可以使用数学表达式
#### 6.2、条件查询
- 语法格式：select 字段 from 表名 where 条件;
- 支持的运算符

符号|作用|实例
-|-|-
=|等于
<>或!=|不等于
<|小于
<=|小于等于
\> |大于
\>=|大于等于
between...and...|两值之间(>=and<=)
is null|为空（is not null 不为空）
and|并且
or|或者
in|包含，相当于多个or（not in不包含）|select * from car where car_ID in ('CA001','CA006');
not|非
like|为模糊查询，支持%或下划线匹配（%匹配任意个字符，_一个下划线只匹配一个字符）
<span style="color:red">and优先级比or高</span>
```sql
# 模糊查询
# 查询中间字符
select * from car where car_ID like '%00%'
# 查询某开头
select * from car where car_ID like 'CA%'
# 查询某结尾
select * from car where car_ID like '%001'

```

#### 6.3、排序
- 升序排序：select 字段名 from 表名 order by 字段名 asc;
- 降序：select 字段名 from 表名 order by 字段名 desc;
- 默认为升序
- 多字段排序
  - select 字段名 from 表名 order by 字段名，字段名 desc;
  - 先按前一个字段升序排序如果有相等的，再按后一个字段进行降序排序
- 排序语句总是在最后才执行

### 7、函数
- 条件语句：
  - case...when...then...when...then...else...end
```
# 当员工的岗位为MANAGER的时候工资上调10%，当为SALESMAN的时候上调50%，其他正常
 select
    ename,
    job,
    sal  oldsal,
    (case job when 'MANAGER' then sal *1.1 when 'SALESMAN' then sal*1.5 else sal end) newsal
    from emp;
+--------+-----------+---------+---------+
| ename  | job       | oldsal  | newsal  |
+--------+-----------+---------+---------+
| SMITH  | CLERK     |  800.00 |  800.00 |
| ALLEN  | SALESMAN  | 1600.00 | 2400.00 |
| WARD   | SALESMAN  | 1250.00 | 1875.00 |
| JONES  | MANAGER   | 2975.00 | 3272.50 |
| MARTIN | SALESMAN  | 1250.00 | 1875.00 |
| BLAKE  | MANAGER   | 2850.00 | 3135.00 |
| CLARK  | MANAGER   | 2450.00 | 2695.00 |
| SCOTT  | ANALYST   | 3000.00 | 3000.00 |
| KING   | PRESIDENT | 5000.00 | 5000.00 |
| TURNER | SALESMAN  | 1500.00 | 2250.00 |
| ADAMS  | CLERK     | 1100.00 | 1100.00 |
| JAMES  | CLERK     |  950.00 |  950.00 |
| FORD   | ANALYST   | 3000.00 | 3000.00 |
| MILLER | CLERK     | 1300.00 | 1300.00 |
+--------+-----------+---------+---------+
```
#### 7.1、数据处理函数/单行处理函数
- 特点：一个输入对应一个输出

函数|作用
-|-
Lower|转换小写
upper|转换大写
substr|取子串（substr（被截取的字符串，起始下标（从1开始），截取的长度），不写长度默认截到最后一个字符
length|取长度
trim|去空格
str_to_date|将字符串转换成日期
date——format|格式化日期
format|设置千分位
round|四舍五入
rand()|生成0-1随机数
ifnull|将null转换为一个具体值
concat|拼接字符串（concat(字符串1，字符串2)）
now|获取当前系统时间，为datetime类型
```
# 四舍五入函数，第二个参数为保留几位小数
select round(123.54,3);
+-----------------+
| round(123.54,3) |
+-----------------+
|         123.540 |
+-----------------+

select round(123.54,-2);
+------------------+
| round(123.54,-2) |
+------------------+
|              100 |
+------------------+

# null转换函数
# 把null当成为0
select ename,ifnull(comm,0) from emp;
+--------+----------------+
| ename  | ifnull(comm,0) |
+--------+----------------+
| SMITH  |           0.00 |
| ALLEN  |         300.00 |
| WARD   |         500.00 |
| JONES  |           0.00 |
| MARTIN |        1400.00 |
| BLAKE  |           0.00 |
| CLARK  |           0.00 |
| SCOTT  |           0.00 |
| KING   |           0.00 |
| TURNER |           0.00 |
| ADAMS  |           0.00 |
| JAMES  |           0.00 |
| FORD   |           0.00 |
| MILLER |           0.00 |
+--------+----------------+

# 数字格式化：fromat(数字,'格式')
select format(sal,'$999,999') from emp;
+------------------------+
| format(sal,'$999,999') |
+------------------------+
| 800                    |
| 1,600                  |
| 1,250                  |
| 2,975                  |
| 1,250                  |
| 2,850                  |
| 2,450                  |
| 3,000                  |
| 5,000                  |
| 1,500                  |
| 1,100                  |
| 950                    |
| 3,000                  |
| 1,300                  |
+------------------------+

# str_to_date:将字符串varchar类型转换成date类型
# 如果刚好是年月日格式就可以省略不写
insert into t_user values(1,'san',str_to_date('10-11-1997','%d-%m-%Y'));
# %Y 年
# %m 月
# %d 日
# %h 时
# %i 分
# %s 秒
# date_format:将date类型转换成具有一定格式的varchar字符串类型
select no,name,date_format(birth,'%m/%d/%Y') from t_user;
+------+------+-------------------------------+
| no   | name | date_format(birth,'%m/%d/%Y') |
+------+------+-------------------------------+
|    1 | san  | 10/11/1997                    |
|    1 | san  | 11/10/1997                    |
+------+------+-------------------------------+
```



#### 7.2、分组函数/聚合函数/多行处理函数
- 特点：多个输入对应一个输出
- 分组函数在使用时必须先分组，然后才能使用，没有分组默认一张表为一组
- 分组函数自动忽略null
- 分组函数不能直接用在where语句
```
select * from emp where sal>min(sal);
ERROR 1111 (HY000): Invalid use of group function
```
函数|作用
-|-
count|计数
sum|求和
avg|平均值
max|最大值
min|最小值

```
# 计数
select count(ename) from emp;
+--------------+
| count(ename) |
+--------------+
|           14 |
+--------------+
```
### 8、分组查询
- group by 字段名
- 在select语句中，如果有group by语句的话，select后面只能跟参加分组的字段以及分组函数，其他字段无意义
- 单独分组
```
# 按岗位分组算各个岗位的平均工资
select job,avg(sal) from emp group by job;
+-----------+-------------+
| job       | avg(sal)    |
+-----------+-------------+
| ANALYST   | 3000.000000 |
| CLERK     | 1037.500000 |
| MANAGER   | 2758.333333 |
| PRESIDENT | 5000.000000 |
| SALESMAN  | 1400.000000 |
+-----------+-------------+
```
- 联合分组

```
# 在同一部门中找不同岗位的最高工资
select deptno,job,max(sal) from emp group by deptno,job;
+--------+-----------+----------+
| deptno | job       | max(sal) |
+--------+-----------+----------+
|     10 | CLERK     |  1300.00 |
|     10 | MANAGER   |  2450.00 |
|     10 | PRESIDENT |  5000.00 |
|     20 | ANALYST   |  3000.00 |
|     20 | CLERK     |  1100.00 |
|     20 | MANAGER   |  2975.00 |
|     30 | CLERK     |   950.00 |
|     30 | MANAGER   |  2850.00 |
|     30 | SALESMAN  |  1600.00 |
+--------+-----------+----------+
```
- 筛选分组后的数据
  - having关键字可以筛选分组后的数据
  - <span style="color:red">where和having，优先选择where，where不能完成再选having，比如筛选平均值时，where就不能完成</span>
```
select deptno,max(sal) from emp group by deptno having max(sal)>3000;
+--------+----------+
| deptno | max(sal) |
+--------+----------+
|     10 |  5000.00 |
+--------+----------+
```
#### 8.1.关于分组查询时出现ONLY_FULL_GROUP_BY错误解决方法

提示错误：which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
在命令行中执行‘select @@sql_mode’查看自己的sql_mode设置

> sql_mode参数说明

- ONLY_FULL_GROUP_BY

对于GROUP BY聚合操作，如果在SELECT中的列，没有在GROUP BY中出现，那么这个SQL是不合法的，因为列不在GROUP BY从句中。简而言之，就是SELECT后面接的列必须被GROUP BY后面接的列所包含。如：
select a,b from table group by a,b,c; (正确)
select a,b,c from table group by a,b; (错误)
这个配置会使得GROUP BY语句环境变得十分狭窄，所以一般都不加这个配置

- NO_AUTO_VALUE_ON_ZERO

该值影响自增长列的插入。默认设置下，插入0或NULL代表生成下一个自增长值。（不信的可以试试，默认的sql_mode你在自增主键列设置为0，该字段会自动变为最新的自增值，效果和null一样），如果用户希望插入的值为0（不改变），该列又是自增长的，那么这个选项就有用了。

- STRICT_TRANS_TABLES

在该模式下，如果一个值不能插入到一个事务表中，则中断当前的操作，对非事务表不做限制。（InnoDB默认事务表，MyISAM默认非事务表；MySQL事务表支持将批处理当做一个完整的任务统一提交或回滚，即对包含在事务中的多条语句要么全执行，要么全部不执行。非事务表则不支持此种操作，批处理中的语句如果遇到错误，在错误前的语句执行成功，之后的则不执行；MySQL事务表有表锁与行锁非事务表则只有表锁）

- NO_ZERO_IN_DATE

在严格模式下，不允许日期和月份为零

- NO_ZERO_DATE

设置该值，mysql数据库不允许插入零日期，插入零日期会抛出错误而不是警告。

ERROR_FOR_DIVISION_BY_ZERO

在INSERT或UPDATE过程中，如果数据被零除，则产生错误而非警告。如 果未给出该模式，那么数据被零除时MySQL返回NULL

- NO_AUTO_CREATE_USER

禁止GRANT创建密码为空的用户

- NO_ENGINE_SUBSTITUTION

如果需要的存储引擎被禁用或未编译，那么抛出错误。不设置此值时，用默认的存储引擎替代，并抛出一个异常

- PIPES_AS_CONCAT

将”||”视为字符串的连接操作符而非或运算符，这和Oracle数据库是一样的，也和字符串的拼接函数Concat相类似

- ANSI_QUOTES

启用ANSI_QUOTES后，不能用双引号来引用字符串，因为它被解释为识别符

> ##### 解决办法

1. 在命令行中执行，临时更改：set @@sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';

2. 去my.ini文件中配置，永久更改

   ```sql
   [mysqld]
   sql_mode=’STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION’
   ```

### 9、去除重复记录

- distinct关键字
- distinct关键字只能出现在所有字段的前面
- 单去重
```
select distinct job from emp;
+-----------+
| job       |
+-----------+
| CLERK     |
| SALESMAN  |
| MANAGER   |
| ANALYST   |
| PRESIDENT |
+-----------+
```
- 联合去重
```
select distinct deptno,job from emp;
+--------+-----------+
| deptno | job       |
+--------+-----------+
|     20 | CLERK     |
|     30 | SALESMAN  |
|     20 | MANAGER   |
|     30 | MANAGER   |
|     10 | MANAGER   |
|     20 | ANALYST   |
|     10 | PRESIDENT |
|     30 | CLERK     |
|     10 | CLERK     |
+--------+-----------+
```
- 可以出现在分组函数中
```
select count(distinct job) from emp;
+---------------------+
| count(distinct job) |
+---------------------+
|                   5 |
+---------------------+
```
### 10、连接查询
- 连接查询就是多张表联合起来查询数据。比如从empty中取员工名字，从dept表中取部门名字。
- 连接查询分类：
  - 根据语法年代：
    - SQL92：1992年出现的语法
    - SQL99：1999年出现的语法
  - 根据表连接的方式：
    - 内连接：
      - 等值连接
      - 非等值连接
      - 子连接
    - 外连接：
      - 左外连接（左连接）
      - 右外连接（右链接）
    - 全连接（很少用）：全都是主表
- 如果表连接时不做条件限制，表就会做笛卡尔积
```
# 不做条件限制
 select ename,dname from emp,dept;
 56 rows in set (0.01 sec)

# 条件限制
# 当两个表的字段名相等时，可以加上表名.的形式进行区分
# 加条件只会减少查询结果，不会减少匹配次数
 select ename,dname from emp e,dept d where e.deptno=d.deptno;
 # 92语法
+--------+------------+
| ename  | dname      |
+--------+------------+
| SMITH  | RESEARCH   |
| ALLEN  | SALES      |
| WARD   | SALES      |
| JONES  | RESEARCH   |
| MARTIN | SALES      |
| BLAKE  | SALES      |
| CLARK  | ACCOUNTING |
| SCOTT  | RESEARCH   |
| KING   | ACCOUNTING |
| TURNER | SALES      |
| ADAMS  | RESEARCH   |
| JAMES  | SALES      |
| FORD   | RESEARCH   |
| MILLER | ACCOUNTING |
+--------+------------+
14 rows in set (0.00 sec)
```

#### 10.1、内连接
- 特点：符合条件的数据查询出来
- 内连接值之等值连接
  - 条件是等量关系，所以被称为等值连接
```
# 92语法
# 缺点：结构不够清晰，表的连接条件和后期进一步筛选条件都烦在where后面
select 
    ename,dname 
from 
    emp e,dept d 
where 
    e.deptno=d.deptno;

# 99语法
# 优点：表连接的条件与后续筛选的条件分离
select 
    ename,dname 
from 
    emp e
inner join # inner可以省略，带inner可读性更高 
    dept d 
on
    e.deptno=d.deptno;
```
- 内连接之非等值连接
  - 条件不是一个等量关系，称为非等值连接
```
select
    e.ename,e.sal,s.grade
from
    emp e
inner join 
    salgrade s
on
    e.sal between s.losal and s.hisal;
+--------+---------+-------+
| ename  | sal     | grade |
+--------+---------+-------+
| SMITH  |  800.00 |     1 |
| ALLEN  | 1600.00 |     3 |
| WARD   | 1250.00 |     2 |
| JONES  | 2975.00 |     4 |
| MARTIN | 1250.00 |     2 |
| BLAKE  | 2850.00 |     4 |
| CLARK  | 2450.00 |     4 |
| SCOTT  | 3000.00 |     4 |
| KING   | 5000.00 |     5 |
| TURNER | 1500.00 |     3 |
| ADAMS  | 1100.00 |     1 |
| JAMES  |  950.00 |     1 |
| FORD   | 3000.00 |     4 |
| MILLER | 1300.00 |     2 |
+--------+---------+-------+
14 rows in set (0.00 sec)
```
- 内连接之自连接
  - 一张表看成两张表
  - 自己与自己连接
```
select 
    a.ename 员工名,a.ename 领导名
from
    emp a
join 
    emp b
on
    a.mgr=b.empno;
+--------+--------+
| 员工名 | 领导名 |
+--------+--------+
| SMITH  | SMITH  |
| ALLEN  | ALLEN  |
| WARD   | WARD   |
| JONES  | JONES  |
| MARTIN | MARTIN |
| BLAKE  | BLAKE  |
| CLARK  | CLARK  |
| SCOTT  | SCOTT  |
| TURNER | TURNER |
| ADAMS  | ADAMS  |
| JAMES  | JAMES  |
| FORD   | FORD   |
| MILLER | MILLER |
+--------+--------+
13 rows in set (0.01 sec)
```
#### 10.2、外连接
- 外连接有主次关系
- 外连接之右连接
  - right表示右边的表看成主表，把主表的数据全部查出，稍带着关联查左边的表
```
select 
    e.ename,d.dname
from 
    emp e 
right outer join # outer可以省略
    dept d
on 
    e.deptno=d.deptno;
+--------+------------+
| ename  | dname      |
+--------+------------+
| SMITH  | RESEARCH   |
| ALLEN  | SALES      |
| WARD   | SALES      |
| JONES  | RESEARCH   |
| MARTIN | SALES      |
| BLAKE  | SALES      |
| CLARK  | ACCOUNTING |
| SCOTT  | RESEARCH   |
| KING   | ACCOUNTING |
| TURNER | SALES      |
| ADAMS  | RESEARCH   |
| JAMES  | SALES      |
| FORD   | RESEARCH   |
| MILLER | ACCOUNTING |
| NULL   | OPERATIONS |
+--------+------------+
15 rows in set (0.00 sec)
```
#### 多表连接
- 内连接和外连接可以混合
- 语法：
```
select
    ...
from 
    a
join
    b
on 
    a和b的连接条件
join
    c
on
    a和c的连接条件
......

select 
    e.ename,e.sal,d.dname,s.grade
from 
    emp e
join 
    dept d
on 
    e.deptno =d.deptno
join 
    salgrade s
on 
    e.sal between s.losal and s.hisal;
+--------+---------+------------+-------+
| ename  | sal     | dname      | grade |
+--------+---------+------------+-------+
| SMITH  |  800.00 | RESEARCH   |     1 |
| ALLEN  | 1600.00 | SALES      |     3 |
| WARD   | 1250.00 | SALES      |     2 |
| JONES  | 2975.00 | RESEARCH   |     4 |
| MARTIN | 1250.00 | SALES      |     2 |
| BLAKE  | 2850.00 | SALES      |     4 |
| CLARK  | 2450.00 | ACCOUNTING |     4 |
| SCOTT  | 3000.00 | RESEARCH   |     4 |
| KING   | 5000.00 | ACCOUNTING |     5 |
| TURNER | 1500.00 | SALES      |     3 |
| ADAMS  | 1100.00 | RESEARCH   |     1 |
| JAMES  |  950.00 | SALES      |     1 |
| FORD   | 3000.00 | RESEARCH   |     4 |
| MILLER | 1300.00 | ACCOUNTING |     2 |
+--------+---------+------------+-------+
14 rows in set (0.00 sec)
```
### 11、子查询
- select语句中嵌套select语句，被嵌套的select语句称为子查询
- 子查询可以出现的位置：
```
select 
  ..(select)
from
  ..(select)
where
  ..(select)

# where中的子查询
select 
  ename,sal
from 
  emp
where
sal>(select min(sal) from emp);
+--------+---------+
| ename  | sal     |
+--------+---------+
| ALLEN  | 1600.00 |
| WARD   | 1250.00 |
| JONES  | 2975.00 |
| MARTIN | 1250.00 |
| BLAKE  | 2850.00 |
| CLARK  | 2450.00 |
| SCOTT  | 3000.00 |
| KING   | 5000.00 |
| TURNER | 1500.00 |
| ADAMS  | 1100.00 |
| JAMES  |  950.00 |
| FORD   | 3000.00 |
| MILLER | 1300.00 |
+--------+---------+
13 rows in set (0.00 sec)

# from中的子查询
# from中的子查询，可以将查询结果看做一张临时表，每个临时表必须要有自己的别名
select t.*,s.grade
from 
(select job,avg(sal) as avgsal from emp group by job) t
join 
salgrade s
on 
t.avgsal between s.losal and s.hisal;
+-----------+-------------+-------+
| job       | avgsal      | grade |
+-----------+-------------+-------+
| ANALYST   | 3000.000000 |     4 |
| CLERK     | 1037.500000 |     1 |
| MANAGER   | 2758.333333 |     4 |
| PRESIDENT | 5000.000000 |     5 |
| SALESMAN  | 1400.000000 |     2 |
+-----------+-------------+-------+
5 rows in set (0.01 sec)
```
### 12、union关键字
- union在进行结果集的合并的时候要求列数相同
- union可以减少匹配次数
- 结果集合并
```
select ename,job from emp where job ='MANAGER'
union
select ename,job from emp where job ='SALESMAN';
+--------+----------+
| ename  | job      |
+--------+----------+
| JONES  | MANAGER  |
| BLAKE  | MANAGER  |
| CLARK  | MANAGER  |
| ALLEN  | SALESMAN |
| WARD   | SALESMAN |
| MARTIN | SALESMAN |
| TURNER | SALESMAN |
+--------+----------+
7 rows in set (0.00 sec)
```
### 13.limit关键字
- 取出结果集的一部分
- 用法：
  - limit startIndex，length
  - 起始下标从0开始，缺省的话默认从0开始
```
# 取出工资前五的人
select 
    ename,sal
from 
    emp
order by
    sal desc
limit 5;
+-------+---------+
| ename | sal     |
+-------+---------+
| KING  | 5000.00 |
| FORD  | 3000.00 |
| SCOTT | 3000.00 |
| JONES | 2975.00 |
| BLAKE | 2850.00 |
+-------+---------+
5 rows in set (0.00 sec)
```

### 12、DQL语句关键字顺序
```
select 5
...
from 1
...
where 2
...
group by 3
...
having 4
...
order by 6
...
limit ... 7
# 以上顺序不可颠倒
```

### 13、表操作
- 表的创建格式：create table
```
create table 表名(
  字段名1 数据类型，
  字段名2 数据类型，
  字段名3 数据类型...
  );
# 表名建议以t_或者tbl_开始，可读性强，见名知意
# 字段名见名知意

create table t_student(
no int,
name varchar(32),
age int(3),
email varchar(255)
);

```
- 删除表：drop
```sql
drop table 表名;
# 表不存在时会报错

drop table if exists 表名;
# 如果表存在就删除
```
- 插入数据：insert
```
insert into 表名(字段名1，字段名2···) values(值1，值2····);
# 字段与值要一一对应
# 字段可以省略，省略后默认都写上了

# 插入多条记录
 insert into t_student values
 (1,'1',3,'1'),
 (1,'1',3,'1');

# 将一个查询结果插入表
# 查询结果需要符合被插入的表结构
insert into dept select * from emp;
```
- 默认值：default关键字
```
create table 表名(
  字段名1 数据类型 default 默认值，
  字段名2 数据类型，
  字段名3 数据类型...
  );
```
- 修改数据：update
```
# 格式:update 表名 set 字段名1=值1，字段名2=值2....where 条件;
# 没有条件限制会导致所有数据全部更新
```
- 删除数据：delete
```
# 语法格式：delete from 表名 where 条件;
# 没有条件限制会导致所有数据全部删除
# 表中数据被删除，内存不会被释放，效率比较低，但是数据可以被回复


# truncate语句删除
# 效率较高但是不支持回滚
truncate table dept;
```
- 表的复制：as
```
# 将一个查询结果当做一张表新建
# 可以完成表的快速复制
# 表中的数据也会存在
 create table emp2 as select * from emp;
```

#### 13.1、数据类型
数据类型|含义|限制
-|-|-
varchar|可变长度的字符串，会根据实际的数据长度动态分配空间|最长255
char|定长字符串，不管实际的数据长度，分配固定的空间|最长255
int|数字整数型|最长11
bigint|数字长整型|
float|单精度浮点型
double|双精度浮点型
date|短日期，包括年月日
datetime|长日期，包括年月日时分秒
clob|字符大对象，最多可以存储4G的字符串
blob|二进制大对象，专门用来存储图片，声音，视频等流媒体数据|插入数据必须使用IO流

#### 13.2、约束
- 约束：在创建表的时候可以给表中的字段加上一些约束，来保证这个表中数据的完整性和有效性
- 添加在列后面的为列级约束，没有添加在列后面的为表级约束，一般用来联合约束
- 非空约束：not null
```
# 非空约束的字段不能为NULL
# 只有列级约束
create table emp3(
  no int not null
);
```

- 唯一性约束：unique
```
# 唯一性约束的字段不能重复
 create table t_vip(
id int,
name varchar(255) unique
);

# 多字段联合起来唯一
 create table t_vip(
  id int,
  name varchar(255)，
  unique(id,name)
);
```
- 主键约束：primary key(简称PK)
  - 主键约束：一种约束
  - 主键字段：字段加了主键约束
  - 主键值：主键字段里的每一个值都为主键值
```
# 主键约束：一种约束
# 主键字段：字段加了主键约束
# 主键值：主键字段里的每一个值都为主键值
# 主键值是每一行记录的唯一标识
# 任何一张表都应该有主键，否则是无效的
# 主键不能重复不能为空
# 分为单一主键与复合主键（多个字段联合），不建议使用复合主键
# 主键只能有一个
# 主键建议使用int，bigint，char等定长类型
# 还可以分为自然主键和业务主键
# 自然主键(使用较多)：主键值是一个自然数，和业务没关系
# 业务主键：和业务紧密关联
# 在mysql中可以使用auto_increment自增来维护主键,默认从1开始以1递增
create table t_vip(
  id int primary key auto_increment,
  name varchar(255)
);
```
- 外键约束：foreign key(简称FK)
```
# 外键约束：一种约束
# 外键字段：字段加了外键约束
# 外键值：外键字段里的每一个值都为外键值
# 如果把全部数据都放在一张表里，数据冗余，空间浪费，可以设计两张表来节省空间，这时候就需要添加外键约束，确保两表链接数据正确
# 被外键引用的表为父表，删除表的时候要先删子表，创建表的时候先创父表，删除数据时先删子表，插入数据时先插父表
# 被外键引用的字段必须有unique约束，外键值可以为null
# 从表的外键一般为主表的主键
# 从表外键的数据类型必须与主表的主键类型一致
CREATE table t_class(
	classno int primary key,
	classname varchar(255)
);
CREATE TABLE t_student(
	no int primary key auto_increment,
	name varchar(255),
	cno int ,
  foreign key(cno) references t_class(classno)
	);
```
- 检查约束：mysql不支持，oracle支持

### 14、存储引擎
- mysql特有术语，就是一个表存储/组织数据的方式
- 给表指定引擎
```
CREATE TABLE `emp` (
  `EMPNO` int(4) NOT NULL,
  `ENAME` varchar(10) DEFAULT NULL,
  `JOB` varchar(9) DEFAULT NULL,
  `MGR` int(4) DEFAULT NULL,
  `HIREDATE` date DEFAULT NULL,
  `SAL` double(7,2) DEFAULT NULL,
  `COMM` double(7,2) DEFAULT NULL,
  `DEPTNO` int(2) DEFAULT NULL,
  PRIMARY KEY (`EMPNO`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 auto_increment=100
# 指定存储引擎和字符集,指定自增从100开始
```
- 常用存储引擎
  - MyISAM
    - 不支持事物，安全性底
    ![](./image/303)
  - InnoDB
    - 表空间存储索引和数据
      ![](./image/305)
  - MEMORY
    ![](./image/307)

### 15、事务

- 事务命令：
  - 查看隔离级别：select @@transaction_isolation;
  - 设置隔离级别：set global transaction isolation level 事务等级;

- 一个事务起始就是一个完整的业务逻辑

> 事务（transaction）：最小的不可再分的工作单元；通常一个事务对应一个完整的业务(例如银行账户转账业务，该业务就是一个最小的工作单元)
>
> 什么是一个完整的业务逻辑？
> 假设转账，从A账户向B账户转账10000
> 将A账户的钱减去10000(update语句)
> 将B账户的钱加上10000(update语句)
> 这就是一个完整的业务逻辑
>
> 只有DML语句才有事物这一说，其他语句和事物无关
> insert、delete、update才有关，其他没有关系
>
> 正是因为做某件事需要多条DML语句共同联合起来才能完成，所以才需要事务的存在
>
> 事务本质就是多条DML语句同时成功或同时失败
>
> 在事物进行过程中，未结束之前，DML语句不会更改底层数据，它只是将历史操作记录一下，在内存中完成记录。只有在事物结束的时候，而且是成功的结束的时候，才会修改底层硬盘文件中的数据。

- 事务是怎么做到多条DML语句同时成功或同时失败的？
  - InnoDB存储引擎：提供一组用来记录事务性活动的日志文件
  - 在事务的执行过程中，每一条DML的操作都会记录到“事务性活动的日志文件中”。在事务的执行过程中，我们既可以提交事务，也可以回滚事务

- 提交事务

  - commit语句
  - 清空事务性活动的日志文件，将数据全部彻底持久化到数据库表中。提交事务标志着事务的结束。并且是一种全部成功的结束

- 回滚事务

  - rollback语句
  - 将之前所有的DML操作全部撤销，并且清空事务性活动的日志文件，回滚事务标志着事务的结束。并且是一种全部失败的结束
  - 永远只能回滚到上一次的提交点

- mysql支持自动提交事务，每执行一次DML语句，则提交一次

  ```sql
  # 查看是否自动提交
  show variables like 'autocommit';
  
  # 开启自动提交
  set automent=1
  
  # 关闭自动提交
  set automent=0
  ```

- 关于事务参数---completion_type

  ```sql
  # 查看变量
  SHOW VARIABLES LIKE 'completion_type';
  
  # 变量值
  completion_type = 0: 默认值，执行 commit 后不会自动开启新的事务。
  completion_type = 1: 执行 commit 时，相当于执行 COMMIT AND CHAIN，自动开启一个相同隔离级别的事务。
  completion_type = 2: 执行 commit 时，相当于执行 COMMIT AND RELEASE，提交事务后自动断开服务器连接。
  ```

  

- 如何开启mysql的事务？

  ```
  start transaction 或  begin #开启事务
  # 执行commit或者rollback结束事务
  ```

- 如何在事务中回退一部分？

  ```sql
  # 当我们在执行复杂的事物时，一般不需要回滚整个操作，而是分批执行，回滚到某个节点就好了，相当于在大事务下嵌套裂开若干个小事务，在mysql中可以使用保留点`savepoint`来实现
  begin;
  insert into t_class value(50,'终极四班');
  savepoint s1;
  insert into t_class value(60,'终极五班');
  rollback to s1;
  ```

  

- 事务的四个特性：

  1. A：原子性
     - 说明事务是最小的工作单位，不可再分
  2. C：一致性
     - 所有事务要求，在用一个事务中，所有操作必须同时成功，或者同时失败，以保证数据的一致性
  3. I：隔离性
     - 两个事务之间都具有一定的隔离
  4. D:持久性
     - 事务最终结束的一个保障。事务提交，就相当于将没有保存到硬盘上的数据保存到硬盘上

- 事务隔离性

```
A教室和B教室中间有一道墙，这道墙越厚，表示隔离的级别就越高

# 事务隔离级别从低到高为：
读未提交：read uncommitted
	事务A可以读取到事务B未提交的数据。
	这种隔离级别的存在的问题就是:
		脏读现象(Dirty Read)
		称为读到了脏数据
	这种级别一般都是理论上的，一般都是从第二级起步
	
读已提交：read committed
	事务A只能读取到事务B提交后的数据
	这种隔离级别解决了脏读现象，但是不可重复读取数据
	这种隔离级别是比较真实的数据，每一次读到的数据是绝对真实
	
可重复读：repeatable read
	事务A开启后，不管多久，每一次在事务A中读取到的数据都是一致的，即使是事务B将数据已经修改，并且提交了。
	解决了不可重复读取数据，但是会出现幻影读。每一次读到的数据都是幻象，不够真实
	mysql默认的隔离级别
	
序列化/串行化:serializable
	效率最低，解决了所有的问题。
	别是事务排队，不能并发
	每一次读取到的数据时最真实的，并且效率是最低的
```

### 16、索引

- 索引是在数据库表的字段上添加，是为了提高查询效率存在的一种机制。一张表的一个字段可以添加一个索引，多个字段联合起来也可以添加。相当于一本书的目录

- 索引可以**提高数据检索的效率**，减低数据库的IO成本。通过索引列队数据进行排序，减低数据排序的成本，减低CPU的消耗(**如果按照索引列的顺序进行排序，对应order by语句来说，效率会提高很多**)

  - 但是索引会占据磁盘空间
  - 而且索引虽然会提高查询效率，但是会减低更新表的效率。因为在更新表的时候，数据库不仅要保存数据，还要保存或者更新对应的索引文件

- 索引是各种数据库进行优化的重要手段。**优化的时候优先考虑的因素就是索引**

- mysql查询主要就是两种方式：

  - 全表扫描
  - 根据索引检索

- 索引的实现原理

  - 在任何数据库中，任何一张表的任何一条记录在硬盘存储上都有一个硬盘的物理存储编号

- mysql会自动在主键上添加索引对象，如果以一个字段上有unique约束的话，也会自动创建索引对象

- 什么时候会添加索引？

  1. 数据量庞大

  2. 该字段经常出现在where后面，一条件的形式存在，也就是说这个字段总是被扫描

  3. 该子段很少的DML操作(因为DML后，索引需要重新排序)

     <font color='red' size=4>建议不要随意添加索引，因为索引是需要维护的，太多会降低系统性能，建议通过主键查询，建议通过unique约束的字段进行查询，效率是比较高的</font>

- 索引的创建与删除

  - 索引名可以省略，省略索引名与索引列名相同

  - 创建索引

    ```
    create index 索引名 on 表名(字段);
    ```

  - 删除索引

    ```
    drop index 索引名  on 表名;
    ```

- 在mysql中怎么查看一个sql语句是否使用了索引进行检索

  ```
  # 对sql语句进行解释，可以查看检索的行数，type=all则是全表扫描
  explain select * from emp where ename='king';
  
  # 查看索引信息
  show index from 表名;
  ```

- 索引的失效

  ```sql
  # 在模糊查询时尽量避免以'%'开头
  select * from emp where ename like '%T';
  
  # 使用or的时候要求两边的条件字段都要有索引才会走索引
  
  # 使用复合索引的时候，没有使用左侧的列查找，索引失效
  create index emp_job_sal_index on emp(job,sal);# 复合索引
  explain select * from emp where job='MANAGER';# 使用索引
  explain select * from emp where sal=800;# 索引失效
  
  # 在where当中索引字段参加了运算
  explain select * from emp where sal+1=800;# 索引失效
  
  # 在where当中索引字段使用了函数
  explain select * from emp where lower(ename)='smith';
  ```

- 索引的分类

  - 单一索引：一个字段上添加索引

  - 复合索引：多个字段添加索引

  - 主键索引：主键上添加索引

  - 唯一性索引：在有unique约束字段上添加索引

    <font color="red">唯一性比较弱的字段上添加索引用处不大</font>

### 17、视图

- 什么是视图？

  - 站在不同的角度去看待同一份数据

- 创建视图对象和删除视图对象

  - 创建视图

    ```
    # 用一个查询结果创建视图
    create view 视图名 as select * from emp;
    # 只有DQL语句才能以view的形式创建
    ```

  - 删除视图对象

    ```
    drop view 视图名;
    ```

- 视图可以做什么？

  - 可以面向视图对象进行增删改查操作，对试图对象的增删改查，会导致原表被操作

- 视图的作用

  - 视图是用来简化sql对象

    ```sql
    create view
    	emp_dept_view
    as
    	select 
    		e.ename,e.sal,d.dname
    	from
        	emp e
    	join
    		dept d
    	on 
    		e.deptno=d.deptno;
    
    # 默认把DQL语句简化为emp_dept_view视图
    ```

### 18、DBA命令

- 新建用户

  ```
  # username--你要创建的用户名
  # password--该用户密码
  create user username identified by 'password'
  ```

- 数据导出：

  ```
  # 只能在windows dos命令窗口
  # 导出整个数据库
  mysqldump 数据库名>路径名 -urrot -p123456
  
  # 导出数据库中的某个表
  mysqldump 数据库名 表名>路径名 表名 -urrot -p123456
  ```

- 数据导入

  ```
  source 路径 
  ```

### 19、数据库表的设计范式

- 什么是数据库设计范式？
  - 数据库表的设计依据。教你怎么进行数据库表的设计
  - 安装范式进行表的设计可以避免数据的冗余，空间的浪费

- 第一范式
  - 要求任何一张表必须有主键，每一个字段原子性不可再分
- 第二范式
  - 建立在第一范式至上，要求所有非主键字段完全依赖主键，不要产生部分依赖
- 第三范式
  - 建立在第二范式之上，要求所有非主键字段直接依赖主键，不要产生传递依赖

#### 19.1、范式详解

- 第一范式

  - 最核心，最重要的范式，所有表的设计都需要满足

  - 必须有主键，并且每一个字段都是原子性不可再分

  ```
  学生编号 联系方式
  1001	1213546548
  1002	1354654654
  # 以上不符合第一范式：没有主键，并且联系范式字段可以分为邮箱与联系电话
  ```

- 第二范式

  - 建立在第一范式之上
  - 要求所有非主键字段必须完全依赖主键，不要产生部分依赖

  ```
  学生编号+ 教师编号(pk) 学生姓名 老师姓名
  1001	001			张三		汪老师
  # 不符合第二范式，学生姓名字段依赖学生编号，老师姓名字段依赖教师编号，产生部分依赖
  
  # 多对多，三张表，关系表两个外键
  ```

  

- 第三范式

  - 建立在第二范式之上
  - 要求所有非主键字段必须直接依赖主键，不要产生传递依赖

  ```
  学生编号(pk)	学生姓名	班级编号	班级名称
  1001			张三		01			一年一班
  # 满足第一范式
  # 满足第二范式，主键不是复合主键，没有产生部分依赖
  # 不满足第三范式，一年一班依赖01,01依赖1001，产生传递依赖
  
  # 一对多，两张表，多的表加外键
  ```

#### 19.2、设计表总结

- 一对一：
  - 可能数据庞大，需要拆表
  - 建议拆为两张表
- 多对多：
  - 多对多，三张表，关系表两个外键
- 一对多：
  - 一对多，两张表，多的表加外键

<font color="red">数据库设计三范式是理论上的,实践和理论有偏差,最终的目的都是为了满足客户需求，有时候会拿冗余换执行速度,因为在sql中，表和表之间连接的次数越多，效率越低</font>











