## 1.uuid是什么？

UUID是Universally Unique IDentifier(普遍唯一的标识)

UUID代表通用唯一标识符，是一个128位的值，用于软件开发的唯一标识

UUID的生成基于当前时间戳和生成UUID的工作站的唯一属性

## 2.UUID的分类

- [ ] uuid1

  ```python
  uuid.uuid1([node[,clock_seq]]):基于时间戳
  """
  使用主机ID，序列号和当前时间来生成UUID，可保证全球范围的唯一性，但由于该方法生成的UUID中包含有主机的网络地址，可能危及隐私
  如果node参数缺省，系统则自动调用getnode()函数获取主机的硬件地址
  如果clock_seq缺省，则随机产生14位序列号代替
  """
  ```

- [ ] uuid4

  ```python
  uuid.uuid4():基于随机数
  '''
  通过随机数来生成uuid，但使用的是伪随机数有一定的重复概率
  '''
  ```

- [ ] uuid3

  ```python
  uuid.uuid3(namespace,name):基于名字的MD5散列值
  '''
  通过计算命名空间和名字的MD5散列值来生成uuid，可以保证同一命名空间中不同名字的唯一性和不同命名空间的唯一性
  '''
  uuid.uuid3(uuid.NAMESPACE_DNS,'456')
  ```

- [ ] uuid5

  ```python
  uuid.uuid3(namespace,name):基于名字的SHA-1散列值
  '''
  通过计算命名空间和名字的SHA-1散列值生成uuid，算法与uuid3相同
  '''
  uuid.uuid5(uuid.NAMESPACE_DNS,'456')
  ```

## 3.什么是Secrets

> secrets是python3.6加入到标准库的,使用secrets模块，可以生成适用于处理机密信息（如密码，帐户身份验证，安全令牌）的`加密`强随机数。

|        常用函数         |                             说明                             |              实例               |
| :---------------------: | :----------------------------------------------------------: | :-----------------------------: |
|    choice(sequence)     |                   从非空序列中选择一个元素                   |   secrets.choice([23,3,5,6])    |
|      randbelow(n)       |                    随机一个取[0,n)的整数                     |      secrets.randbelow(10)      |
|       randbits(n)       |              在n位长度二进制数范围内随机取一位               |      secrets.randbits(10)       |
|     token_bytes(n)      |             随机生成n个字节以内的bytes类型字符串             |     secrets.token_bytes(2)      |
|      token_hex(n)       |                返回n位长16进制随机文本字符串                 |      secrets.token_hex(2)       |
|    taken_urlsafa(n)     | 返回字节为nbytes的URL安全文本字符串。 文本以Base64编码，每个字节平均约为1.3个字符。 |     secrets.token_urlsafe()     |
| compare_digest(str,str) |                   字符串比较，相等返回True                   | secrets.compare_digest('a','a') |

