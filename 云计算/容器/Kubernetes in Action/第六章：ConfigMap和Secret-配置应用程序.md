> 本章内容包括：
> - 更改容器的主进程
> - 将命令行选项传递给应用程序
> - 设置暴露给应用程序的环境变量
> - 通过ConfigMap配置应用程序
> - 通过Secret传递敏感配置信息

到目前为止，没有传递过任何配置数据给应用程序。几乎所有的应用程序都需要配置信息，并且这些配置数据不应该被嵌入应用本身。

向容器传递配置数据一般可以采用一下几种方法：
- 向容器传递命令行参数
- 为每个容器设置自定义环境变量
- 通过特殊类型的卷将配置文件挂载到容器中
# 向命令行传递命令行参数

迄今为止所有使用的容器运行的都是镜像中默认定义的。Kubernetes可以在pod容器中定义并覆盖命令以满足运行不同的可执行程序，或者是以不同的命令行参数集运行。
## 在Docker中定义命令与参数

在Docker中运行完整的指令需要同时指定命令与参数。

**ENTRYPOINT与CMD**

Dockerfile中的两种指令分别定义命令与参数这两部分：
- ENTRYPOINT定义容器启动时被调用的可执行程序。
- CMD指定传递给ENTRYPOINT的参数。
可以直接使用CMD指定镜像运行时想要执行的命令，但还是推荐使用ENTRYPOINT。
```
# 可以使用--entrypoint替换ENTRYPOINT命令
# 直接在后面接参数即可覆盖cmd
docker run --entrypoint ls myimage -l

# dockerfile
FROM ubuntu

# 安装curl
RUN apt-get update && apt-get install -y curl

# 设置ENTRYPOINT
ENTRYPOINT ["curl"]

# 设置CMD作为默认参数
CMD ["--help"]

```

**shell与exec形式区别**

上述两条指令均支持以下两种形式：
- shell形式：如`ENTRYPOINT node app.js`
- exec形式：如`ENTRYPOINT ["node","app.js"]`
两者的区别在于指定的命令是否在shell中被调用，使用exec形式指令是直接运行node进程，而并非在shell中执行。如果使用shell形式，容器的1号进程会是`/bin/sh -c node app.js`。所以推荐使用exec形式的指令。
## 在Kubernetes中覆盖命令和参数

在Kubernetes中定义容器时，镜像的ENTRYPOINT和CMD均可以被覆盖，仅需在容器定义中设置属性command和args的值即可
```
kind: Pod
spec:
	containners:
	- image: image
	  command: ["/bin/command"]
	  args: 
	  - arg1
	  - arg2
	  - arg3   # 数值需要用引号标记，字符不需要
```
**这两个属性在pod被创建后无法被修改。**
# 为容器设置环境变量

容器化应用通常会使用环境变量作为配置源。Kubernetes允许为pod中的每个容器都指定自定义的环境变量，但现在还不能在pod层面定义环境变量。
> **注意：环境变量和容器的命令和参数一样，在pod创建后无法修改。**

接下来我们演示一下如何在容器中定义环境变量
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: fortune-env
spec:
  containers:
  - image: luksa/fortune:env
    env:    # 设置环境变量
    - name: INTERVAL
      value: "30"
    name: html-generator
    volumeMounts:
    - name: html
      mountPath: /var/htdocs
  - image: nginx:alpine
    name: web-server
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
      readOnly: true
    ports:
    - containerPort: 80
      protocol: TCP
  volumes:
  - name: html
    emptyDir: {}
```
环境变量被设置在pod的容器定义中，并非是pod级别。
>**注意：不要忘记在每个容器中，Kubernetes会自动暴露相同命名空间下每个service对应的环境。这些环境变量基本上可以被看做自动注入的配置。**

在环境变量中，后面定义的环境变量可以引用前面定义的环境变量
```yaml
env:    # 设置环境变量
    - name: INTERVAL
      value: "foo"
    - name: sec
      value: "$(INTERVAL)bar"  # foobar
```
pod定义硬编码意味着需要有效区分生产环境与开发过程中的pod定义。为了能在多个环境下复用pod定义，需要将配置从pod定义描述中解耦出来。可以使用ConfigMap资源对象完成解耦，用`valueFrom`字段替代`value`字段使ConfigMap成为环境变量值的来源。
# 利用ConfigMap解耦配置

应用配置的关键在于能够在多个环境中区分配置选项，将配置从应用程序源码中分离，可频繁变更配置值。Kubernetes允许将配置选项分离到单独的资源对象ConfigMap中，本质上就是一个键值对映射，值可以是短字面量，也可以是完整的配置文件。

应用无需读取ConfigMap，甚至不需要知道它的存在。映射的内容通过环境变量或者卷文件的形式传递给容器，而非直接传递给容器。命令行参数的定义中可以通过$(ENV_VAR)语法引用环境变量，因此可以达到将ConfigMap的条目当做命令行参数传递给进程的效果。

当然，应用程序同样可以通过Kubernetes Rest API按需直接读取ConfigMap的内容。不过除非需求如此，否则不建议这么做，应尽量使应用保持对Kubernetes的无感知。

不管应用是如何使用ConfigMap的，将配置存放在独立的资源对象中有助于在不同的环境下拥有多份同名配置清单。pod是通过名称引用ConfigMap的，因此可以在多环境下使用相应的pod定义描述，同时保持不同的配置值以适应不同环境。
## 创建ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fortune-config # pod通过名称引用
data:   # 指定数据
  sleep-interval: "25" 
```
ConfigMap中的键名必须是一个合法的DNS子域，仅包括数字、字母、破折号、下划线以及点。首位的圆点是可选的。

ConfigMap不仅可以字面量映射，还可以映射整个文件或者整个文件夹下面的文件
```bash
kubectl create configmap my-config 
--from-file=tt.txt   # 映射文件
--from-file=bar=tt.txt  # 带有键名
--from-file=test/  # 映射文件夹
--from-literal=some=thing # 映射字面量

[root@master ~]# kubectl get cm/my-config -oyaml
apiVersion: v1
data:
  1.txt: |
    1
    2
  2.txt: |
    3
    4
  bar: |
    aa
    bb
  some: thing
  tt.txt: |
    aa
    bb
kind: ConfigMap
metadata:
  creationTimestamp: "2024-07-17T14:51:47Z"
  name: my-config
  namespace: default
  resourceVersion: "156648"
  selfLink: /api/v1/namespaces/default/configmaps/my-config
  uid: 1c01da17-d58d-4a75-9798-35ec7e52c514
```
**注意：同一个ConfigMap中的键名不能一样。**