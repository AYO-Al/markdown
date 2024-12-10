### 1.option_bits

在MySQL中，如果不设置，默认`autocommit`是开启的

```sql
select @@autocommit;
> 1
```

这个参数的作用是开启事务自动提交，也就是将MySQL中的每一条语句当成一个事物，当执行完成后自动提交，如果你没有开启这个功能的话，需要手动执行`commit`执行提交事务。

但在MySQL中可以以语句显式的开启事务

```sql
BEGIN;
SQL;
COMMIT;
```

使用`BEGIN`开启事务后，只要不执行`COMMIT`语句提交事务，在`BEGIN`后面执行的SQL语句都不会刷盘，只要其中任一条语句报错，所执行的SQL语句会全部回滚，这就是MySQL事务的原子性。

但如果我们开启了自动提交，又使用`BEGIN`显式的开启事务呢？有没有可能MySQL在显式开启事务后，自动把`autocommit`参数关闭了？

```sql
mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> select @@autocommit;
+--------------+
| @@autocommit |
+--------------+
|            1 |
+--------------+
1 row in set (0.00 sec)

mysql> COMMIT;
Query OK, 0 rows affected (0.00 sec)
```

看来不是这样的，那开始显式事务后，究竟MySQL是怎么工作的？

在MySQL文档里说，在使用`BEGIN`开启事务后，MySQL会隐性的关闭自动提交。

经过寻找后，我在一篇解说MySQL源码的文章里，找到了答案。简单解释一下：

1. MySQL事务不支持嵌套事务，如果你在`BEGIN`里面再执行一次`BEGIN`，那么上一个事物会自动提交
2. 而MySQL判断的依据是`option_bits`是否包含`OPTION_NOT_AUTOCOMMIT | OPTION_BEGIN`这两个标志位的任何一个，如果包含就是当前连接还有事务还未提交

```c++
inline bool in_multi_stmt_transaction_mode() const {
  return variables.option_bits & 
    (OPTION_NOT_AUTOCOMMIT | OPTION_BEGIN);
}
```

`OPTION_BEGIN`标志位就是执行`BEGIN`语句后带上的

```c
thd->variables.option_bits |= OPTION_BEGIN;
```

`OPTION_NOT_AUTOCOMMIT`标志位是表示当前会话没有开启自动提交功能。

这个标志位很眼熟啊，那会不会有个`OPTION_AUTOCOMMIT`标志位代表的是开启了自动提交功能？上网一查，果然是的。

### 2.OPTION_AUTOCOMMIT标志位

option_bits是MySQL服务器的一个内部位掩码，用于存储一些选项标志，例如是否开启了事务、是否启用了查询缓存等。是一个无符号长整型，是一个32位或64位的二进制数。打上对应的标志，就会对标志位做**按位或运算**

```c
thd->variables.option_bits |= OPTION_BEGIN;
```

MySQL中关于事务的标志位有：

- OPTION_NOT_AUTOCOMMIT的值是0x00000004，也就是二进制的00000100。它表示当前会话使用了SET autocommit=0;语句，或者在服务器启动时使用了–skip-autocommit选项。

- OPTION_BEGIN的值是0x00000001，也就是二进制的00000001。它表示当前会话开始了一个显式的事务，也就是使用了BEGIN或START TRANSACTION语句。

- OPTION_AUTOCOMMIT的值是0x00000002，也就是二进制的00000010。它表示当前会话使用了SET autocommit=1;语句，或者在服务器启动时使用了–autocommit选项。

所以在显式开启事务后，所说的隐式关闭自动提交，其实就是

1. 打上OPTION_BEGIN标志位，将OPTION_AUTOCOMMIT标志位清零
2. 在提交事务后将OPTION_BEGIN标志位清零，将OPTION_AUTOCOMMIT置1

参考文档：[MySQL 中 BEGIN 语句会马上启动事务吗？ - 掘金 (juejin.cn)](https://juejin.cn/post/7322156751818031141)





