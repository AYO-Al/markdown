# lower_case_table_names

```text
系统变量lower_case_table_names有三个值：分别是0、1、2.
1. 设置成0(Linux)：表名按你写的SQL大小写存储，大写就大写小写就小写，比较时大小写敏感。
2. 设置成1(Windows)：表名转小写后存储到硬盘，比较时大小写不敏感。 
3. 设置成2(macOS)：表名按你写的SQL大小写存储，大写就大写小写就小写，比较时统一转小写比较。

   数据库名与表名是严格区分大小写的；
   表的别名是严格区分大小写的；
   列名与列的别名在所有的情况下均是忽略大小写的；
   变量名也是严格区分大小写的；
```





# Innoeb_print_all_deadlocks

这个变量是个全局变量，默认关闭，可以动态调整。会在每次发生死锁后，系统会自动将死锁信息输出到错误日志中。输出的内容是`show engine innodb status`中的`LASTER DETECTED DEADLOCK`部分的内容，但`LASTER DETECTED DEADLOCK`只会显示最新的一条，且要手动执行。所以推荐开启`innodb_print_all_deadlocks`



# sql_require_primary_key

`sql_require_primary_key` 是 MySQL 数据库中的一个参数，它控制是否要求每个表都有主键。主键是表中的一列或一组列，其值用于唯一标识表中的每一行。这个参数的值决定了在创建或修改表时是否需要定义主键。

sql_require_primary_key是MySQL 8.0.13版本引入的一个新的参数，这个参数可以在全局或会话级别动态修改，默认值是OFF。



























































































