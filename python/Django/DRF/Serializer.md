## 一、序列化器是什么？

序列化器相当于 Django 表单在 API 中的​**​高级版本​**​：

- **序列化​**​：将复杂数据（模型实例、查询集）转换为 Python 数据类型 → JSON
    
- ​**​反序列化​**​：将客户端提交的数据（JSON）验证后转换为 Python 对象 → 模型实例
    
- ​**​数据验证​**​：验证传入数据的完整性和安全性
    

## 二、序列化器类型

### 1. Serializer 基础类

- 需手动定义所有字段
    
- 适用于非模型数据或简单需求
    

```
from rest_framework import serializers

class BasicSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    age = serializers.IntegerField(min_value=0)
```

### 2. ModelSerializer（最常用）

- 自动根据模型生成字段
    
- 自动创建create()和update()方法
    

```
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}  # 密码不返回
        }
    
    def create(self, validated_data):
        """创建时加密密码"""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
```

### 3. HyperlinkedModelSerializer

- 包含超链接代替 ID
    

```
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']
        extra_kwargs = {
            'url': {'view_name': 'user-detail'}
        }
```

# 三、序列化器设置

## 1. Meta 类配置（ModelSerializer 核心）

```
class UserSerializer(serializers.ModelSerializer):
    # Meta 配置项决定序列化器的基本行为
    class Meta:
        model = User  # 必须配置：关联的模型类
        fields = ['id', 'username', 'email', 'is_active']  # 显式指定字段
        # fields = '__all__'  # 包含所有字段（开发阶段慎用）
        exclude = ['password', 'last_login']  # 排除特定字段（与fields互斥）
        
        # 高级选项：
        read_only_fields = ['id', 'created_at']  # 只读字段列表
        extra_kwargs = {
            'password': {'write_only': True},  # 字段级配置
            'email': {'required': True}
        }
        depth = 1  # 嵌套关系深度（0-10）
```

|​**​配置项​**​|​**​适用字段类型​**​|​**​说明​**​|​**​示例​**​|​**​默认值​**​|
|---|---|---|---|---|
|​**​**read_only​​|所有字段|设置为只读字段，反序列化时忽略|{'created_at': {'read_only': True}}|False|
|​**​**write_only​​|所有字段|设置为只写字段，序列化时不包含|{'password': {'write_only': True}}|False|
|​**​**required​​|所有字段|字段是否为必填项|{'email': {'required': True}}|根据字段类型|
|​**​**allow_null​​|可为空的字段|是否允许 None 值|{'middle_name': {'allow_null': True}}|False|
|​**​**allow_blank​​|字符串字段|是否允许空字符串 ('')|{'description': {'allow_blank': True}}|False|
|​**​**trim_whitespace​​|CharField|是否在验证前去除字符串两端的空白|{'username': {'trim_whitespace': True}}|True|
|​**​**max_length​​|文本相关字段|最大长度限制|{'title': {'max_length': 100}}|无|
|​**​**min_length​​|文本相关字段|最小长度限制|{'password': {'min_length': 8}}|无|
|​**​**max_value​​|数值字段|最大值限制|{'age': {'max_value': 120}}|无|
|​**​**min_value​​|数值字段|最小值限制|{'rating': {'min_value': 1}}|无|
|​**​**validators​​|所有字段|添加额外的验证器|{'username': {'validators': [validate_username]}}|[]|
|​**​**error_messages​​|所有字段|自定义错误消息|{'age': {'error_messages': {'min_value': '年龄不能小于0'}}}|字段默认|
|​**​**style​​|所有字段|控制渲染时的样式（主要用于API文档）|{'password': {'style': {'input_type': 'password'}}}|无|
|​**​**label​​|所有字段|字段的标签（用于表单渲染）|{'email': {'label': '电子邮箱'}}|字段名|
|​**​**help_text​​|所有字段|字段的帮助文本|{'content': {'help_text': '请输入内容'}}|无|
|​**​**default​​|所有字段|字段的默认值|{'status': {'default': 'draft'}}|无|
|​**​**initial​​|所有字段|字段的初始值|{'category': {'initial': 'tech'}}|无|
|​**​**source​​|所有字段|指定字段的数据来源|{'pub_date': {'source': 'published_date'}}|字段名|
|​**​**format​​|日期时间字段|格式化输出|{'created_at': {'format': '%Y-%m-%d %H:%M'}}|ISO 8601|
|​**​**input_formats​​|日期时间字段|指定反序列化时接受的输入格式|{'birthday': {'input_formats': ['%Y-%m-%d', '%d/%m/%Y']}}|多种格式|
|​**​**lookup_field​​|关系字段|指定关联对象查找的字段|{'author': {'lookup_field': 'username'}}|'pk'|
|​**​**lookup_url_kwarg​​|关系字段|指定URL中的关键字参数名|{'author': {'lookup_url_kwarg': 'username'}}|同 lookup_field|
|​**​**view_name​​|HyperlinkedRelatedField|指定用于生成超链接的视图名称|{'url': {'view_name': 'user-detail'}}|无|
|​**​**queryset​​|关系字段|指定查询集|{'category': {'queryset': Category.objects.active()}}|模型默认|
|​**​**many​​|关系字段|指定是否为多对多关系|{'tags': {'many': True}}|根据关系类型|
|​**​**allow_empty​​|列表字段|是否允许空列表|{'tags': {'allow_empty': True}}|True|
|​**​**child​​|ListField|指定列表元素的字段类型|{'scores': {'child': IntegerField(min_value=0, max_value=100)}}|无|
|​**​**to_representation​​|所有字段|自定义序列化方法|{'full_name': {'to_representation': self.format_name}}|无|
|​**​**to_internal_value​​|所有字段|自定义反序列化方法|{'full_name': {'to_internal_value': self.parse_name}}||

## 2. 字段类型与选项配置

```
username = serializers.CharField(
    max_length=50,  # 最大长度
    min_length=3,   # 最小长度
    allow_blank=False,  # 是否允许空字符串
    error_messages={     # 自定义错误消息
        'blank': "用户名不能为空",
        'max_length': "用户名最多50个字符"
    },
    required=True,   # 是否为必需字段
    trim_whitespace=True  # 自动修剪两端空格
)

email = serializers.EmailField(
    allow_null=False,   # 是否允许None值
    default="noreply@example.com"  # 默认值
)

birth_date = serializers.DateField(
    format="%Y-%m-%d",  # 日期格式化
    input_formats=["%Y-%m-%d", "%Y/%m/%d"]  # 接收的日期格式
)
```

## 3. 自定义验证配置

### 1. 字段级验证

命名规则：validate_<field_name>

- 序列化器会自动识别以validate_开头，后面跟着字段名称的方法。
    
- 在验证过程中，当处理到特定字段时，会自动调用对应的验证函数。
    

```
def validate_username(self, value):
    """用户名不能包含特殊字符"""
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise serializers.ValidationError("用户名只能包含字母、数字和下划线")
    return value
```

### 2. 对象级验证

函数名称：validate

- 序列化器会固定识别名为validate的方法作为对象级验证函数。
    
- 该方法在字段级验证之后执行，用于验证多个字段之间的关系。
    

```
def validate(self, data):
    """对象整体验证"""
    if data['start_date'] > data['end_date']:
        raise serializers.ValidationError("结束日期不能早于开始日期")
        
    # 基于用户角色的验证
    if data['role'] == 'admin' and not self.context['request'].user.is_superuser:
        raise serializers.ValidationError("无权限创建管理员账号")
        
    return data
```

### 3. 验证器配置

```
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

username = serializers.CharField(
    validators=[
        UniqueValidator(
            queryset=User.objects.all(),  # 唯一性验证
            message="该用户名已被使用"
        ),
        validate_username_length  # 自定义验证函数
    ]
)

class Meta:
    # 联合唯一验证
    validators = [
        UniqueTogetherValidator(
            queryset=UserGroup.objects.all(),
            fields=('user', 'group'),
            message="用户已加入该组"
        )
    ]
```

# 四. 示例

```
# serializers.py
class CourseSerializer(serializers.ModelSerializer):

    teacher = serializers.ReadOnlyField(source='teacher.username') # 外键字段，只读

    class Meta:
        model = Course
        # exclude = ('id',)
        fields = '__all__'

    def validate_name(self, value):
        if value != "admin1":
            raise serializers.ValidationError("name can not be admin")
        return value

# views.py
@api_view(["GET","PUT","DELETE"])
def course_detail2(request,pk):
    """
    获取/更新/删除一个课程
    :param request:
    :param pk:
    :return:
    """
    try:
        courses = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(data={"msg":"没有此课程信息"},status=status.HTTP_404_NOT_FOUND)
    else:
        if request.method == "GET":
            s = CourseSerializer(instance=courses)
            return Response(data=s.data,status=status.HTTP_200_OK)
        elif request.method == "PUT":
            s = CourseSerializer(instance=courses,data=request.data)
            if s.is_valid():
                s.save()
                return Response(s.data,status=status.HTTP_201_CREATED)
            return Response(s.errors,status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            courses.delete()
            return Response(courses.name,status=status.HTTP_204_NO_CONTENT)

# urls.py
urlpatterns = [
    path('fbv/list/', views.course_detail,name='fbv-list'),
    path('fbv/list2/<int:pk>/', views.course_detail2,name='fbv-list2'),
      ]
  
'''
使用postman：http://localhost:9091/course/fbv/list2/5/
      {
    "name": "123",
    "introduction": "123",
    "price": "123.00"
	}
      
    报错："detail": "Method \"POST\" not allowed."  
'''
```

|​**​方法名​**​|​**​用途​**​|​**​返回值​**​|​**​示例​**​|
|---|---|---|---|
|is_valid()|验证数据|bool|serializer.is_valid()|
|save()|保存数据|模型实例|course = serializer.save()|
|errors|获取错误|dict|errors = serializer.errors|
|data|序列化数据|dict|json_data = serializer.data|
|validated_data|验证后数据|dict|clean_data = serializer.validated_data|

