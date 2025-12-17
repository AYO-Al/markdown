# functools模块

\[toc]

### python中的functools模块

> functools 模块可以说主要是为[函数式编程](https://so.csdn.net/so/search?q=%E5%87%BD%E6%95%B0%E5%BC%8F%E7%BC%96%E7%A8%8B\&spm=1001.2101.3001.7020)而设计，用于增强函数功能。\
> functools模块用以为可调用对象（callable objects）定义[高阶函数](https://so.csdn.net/so/search?q=%E9%AB%98%E9%98%B6%E5%87%BD%E6%95%B0\&spm=1001.2101.3001.7020)或操作。

#### partial函数

> 用于创建一个偏函数，将默认参数包装一个可调用对象，返回结果也是可调用对象。
>
> 偏函数：可以固定住原函数的部分参数，从而在调用时更简单

```python
from functools import partial

int1 = partial(int, '10', 8)
print(int1())

# 把int1函数设置为专门把10转换为8进制的函数
```

#### update\_wrapper函数

> 使用partial包装的函数是没有\_\_name\_\_\_\_和\_\_doc\_\_\_\_属性的。
>
> update\_wrapper:将被包装的函数的属性拷贝到新函数里去

```python
from functools import partial,update_wrapper


int1 = partial(int, '10', 8)
update_wrapper(int1, int)
print(int1.__name__)
print(int1())

# int
# 8
```

#### wraps装饰器

> 装饰器版的update\_wrapper函数

```python
from functools import wraps

def guanjia(game):
    @wraps(game)
    def inner(*args, **kwargs):
        print('打开外挂1')
        game(*args, **kwargs)
        print('关闭外挂1')

    return inner


@guanjia
def play_lol(user, password, hero):
    print('我要开始玩lol了:', user, password, hero)
    print('德玛西亚')


print(play_lol.__name__)

# play_lol
# 如果不用装饰器，则为inner
```

#### reduce函数

> 语法：reduce(函数，参数)
>
> 作用：将一个序列归纳为一个输出

```python
from functools import reduce

l = range(1,50)
print(reduce(lambda x,y:x+y, l))
# 1225
# 将l中所有元素进行相加
```

#### cmp\_to\_key

> 将函数转换为key函数

```python
from functools import cmp_to_key

nums = [3, 30, 34, 5, 9]
new_nums = sorted(nums, key=cmp_to_key(lambda x, y: y - x))
new_nums2 = sorted(nums, key=cmp_to_key(lambda x, y: x - y))
print(new_nums)
print(new_nums2)
#结果:
#[34, 30, 9, 5, 3]
#[3, 5, 9, 30, 34]

```

#### lru\_cache装饰器

> 允许我们将一个函数的返回值快速的缓存或取消缓存
>
> 该装饰器用于缓存函数的调用结果，对于需要多次调用的函数，而且每次调用参数都相同，则可以用该装饰器缓存调用结果，从而加快程序运行
>
> 该装饰器会将不同的调用结果缓存在内存中，因此需要注意内存占用问题

```python
from functools import lru_cache
import time

now = lambda : time.time()
@lru_cache(maxsize=30)  # maxsize参数告诉lru_cache缓存最近多少个返回值
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
start1 = now()
time.sleep(2)
print([fib(n) for n in range(30)])
print(now() - start1)
fib.cache_clear()   # 清空缓存
start2 = now()
time.sleep(2)
print([fib(n) for n in range(30)])
print(now() - start2)

# 2.0053112506866455
# 2.0083212852478027
```

#### singledispatch

> 单分发器，用于实现泛型函数
>
> 根据单一参数的类型来判断调用那个函数

```python
from functools import singledispatch
@singledispatch
def fun(text):
	print('String：' + text)

@fun.register(int)
def _(text):
	print(text)

@fun.register(list)
def _(text):
	for k, v in enumerate(text):
		print(k, v)

@fun.register(float)
@fun.register(tuple)
def _(text):
	print('float, tuple')
fun('i am is hubo')
fun(123)
fun(['a','b','c'])
fun(1.23)
print(fun.registry)	# 所有的泛型函数
print(fun.registry[int])	# 获取int的泛型函数
# String：i am is hubo
# 123
# 0 a
# 1 b
# 2 c
# float, tuple
# {<class 'object'>: <function fun at 0x106d10f28>, <class 'int'>: <function _ at 0x106f0b9d8>, <class 'list'>: <function _ at 0x106f0ba60>, <class 'tuple'>: <function _ at 0x106f0bb70>, <class 'float'>: <function _ at 0x106f0bb70>}
# <function _ at 0x106f0b9d8>

```
