# 第六章：ConfigMap和Secret-配置应用程序

> 本章内容包括：
>
> * 更改容器的主进程
> * 将命令行选项传递给应用程序
> * 设置暴露给应用程序的环境变量
> * 通过ConfigMap配置应用程序
> * 通过Secret传递敏感配置信息

到目前为止，没有传递过任何配置数据给应用程序。几乎所有的应用程序都需要配置信息，并且这些配置数据不应该被嵌入应用本身。

向容器传递配置数据一般可以采用一下几种方法：

* 向容器传递命令行参数
* 为每个容器设置自定义环境变量
* 通过特殊类型的卷将配置文件挂载到容器中

## 1 向命令行传递命令行参数

迄今为止所有使用的容器运行的都是镜像中默认定义的。Kubernetes可以在pod容器中定义并覆盖命令以满足运行不同的可执行程序，或者是以不同的命令行参数集运行。

### 1.1 在Docker中定义命令与参数

在Docker中运行完整的指令需要同时指定命令与参数。

**ENTRYPOINT与CMD**

Dockerfile中的两种指令分别定义命令与参数这两部分：

* ENTRYPOINT定义容器启动时被调用的可执行程序。
* CMD指定传递给ENTRYPOINT的参数。\
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

* shell形式：如`ENTRYPOINT node app.js`
* exec形式：如`ENTRYPOINT ["node","app.js"]`\
  两者的区别在于指定的命令是否在shell中被调用，使用exec形式指令是直接运行node进程，而并非在shell中执行。如果使用shell形式，容器的1号进程会是`/bin/sh -c node app.js`。所以推荐使用exec形式的指令。

### 1.2 在Kubernetes中覆盖命令和参数

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

## 2 为容器设置环境变量

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

> **注意：不要忘记在每个容器中，Kubernetes会自动暴露相同命名空间下每个service对应的环境。这些环境变量基本上可以被看做自动注入的配置。**

在环境变量中，后面定义的环境变量可以引用前面定义的环境变量

```yaml
env:    # 设置环境变量
    - name: INTERVAL
      value: "foo"
    - name: sec
      value: "$(INTERVAL)bar"  # foobar
```

pod定义硬编码意味着需要有效区分生产环境与开发过程中的pod定义。为了能在多个环境下复用pod定义，需要将配置从pod定义描述中解耦出来。可以使用ConfigMap资源对象完成解耦，用`valueFrom`字段替代`value`字段使ConfigMap成为环境变量值的来源。

## 3 利用ConfigMap解耦配置

应用配置的关键在于能够在多个环境中区分配置选项，将配置从应用程序源码中分离，可频繁变更配置值。Kubernetes允许将配置选项分离到单独的资源对象ConfigMap中，本质上就是一个键值对映射，值可以是短字面量，也可以是完整的配置文件。

应用无需读取ConfigMap，甚至不需要知道它的存在。映射的内容通过环境变量或者卷文件的形式传递给容器，而非直接传递给容器。命令行参数的定义中可以通过$(ENV\_VAR)语法引用环境变量，因此可以达到将ConfigMap的条目当做命令行参数传递给进程的效果。

当然，应用程序同样可以通过Kubernetes Rest API按需直接读取ConfigMap的内容。不过除非需求如此，否则不建议这么做，应尽量使应用保持对Kubernetes的无感知。

不管应用是如何使用ConfigMap的，将配置存放在独立的资源对象中有助于在不同的环境下拥有多份同名配置清单。pod是通过名称引用ConfigMap的，因此可以在多环境下使用相应的pod定义描述，同时保持不同的配置值以适应不同环境。

### 3.1 创建ConfigMap

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
  1.txt: |  # 表示后续的条目值是多行字面量
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

### 3.2 给容器传递ConfigMap作为环境变量

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: fortune-env-from-configmap
spec:
  containers:
  - image: luksa/fortune:env
    env:
    - name: INTERVAL
      valueFrom:   
        configMapKeyRef:
          name: fortune-config # 引用ConfigMap名称
          key: sleep-interval  # 环境变量值被设置为ConfigMap下对应键的值
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

这里定义了一个环境变量INTERVAL，并将其设置为`fortune-config`ConfigMap中键名为sleep-interval对应的值。如果在容器中引用了不存在的ConfigMap，容器会启动失败，其他容器会启动成功，这个启动失败的容器会在ConfigMap创建后自动启动，无需重新创建pod。

> **注意：可以设置对ConfigMap的引用是可选的，设置configMapKeyRef.optional: true。这样即使ConfigMap不存在，容器也能正常启动。**

### 3.3 一次性传递所有ConfigMap的内容作为环境变量

如果ConfigMap包含很多内容，把每个键单独列出来是很容易出错且耗时比较长的过程，在Kubernetes1.6版本之后，提供了暴露ConfigMap所有条目作为环境变量的手段。

```yaml
spec:
  containers:
  - image: luksa/fortune:env
    envFrom: # 使用envFrom字段，而不是env
    - prefix: CONFIG_ # 所有环境变量包含CONFIG_前缀
      configMapRef: 
        name: my-config-map # 指定ConfigMap名
```

容器中所有的环境变量都为"CONFIG\_keyname"，可以不指定前缀，这样环境变量的名称就和ConfigMap中的键名一致。

> **注意：当ConfigMap中的键名不是合法的环境变量名的话，创建环境变量的时候会忽略掉对应的条目，如键名包含破折号。**

### 3.4 传递ConfigMap作为命令行参数

如何将ConfigMap中的值作为参数传递到运行在容器中的主进程。在字段pod.spec.containers.args中无法直接引用ConfigMap中的内容，但是可以利用ConfigMap内容初始化某个环境变量，然后再在参数 字段中引用该环境变量。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: fortune-args-from-configmap
spec:
  containers:
  - image: luksa/fortune:args
    env:
    - name: INTERVAL
      valueFrom: 
        configMapKeyRef:
          name: fortune-config
          key: sleep-interval
    args: ["$(INTERVAL)"]
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

环境变量的定义与之前相同，需要通过$(INTERVAL)将环境变量的值注入到参数值。

### 3.5 使用ConfigMap卷将条目暴露为文件

环境变量或命令行参数作为配置值通常适用于变量值较短的创建。由于ConfigMap中可以包含完整的配置文件内容，当想要把文件完整暴露给容器的时候，可以借助前面提到的一种称为ConfigMap卷的特殊卷格式。

创建包含ConfigMap条目内容的卷只需要创建一个引用ConfigMap名称的卷并挂载到容器中即可。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: fortune-configmap-volume
spec:
  containers:
  - image: luksa/fortune:env
    env:
    - name: INTERVAL
      valueFrom:
        configMapKeyRef:
          name: fortune-config
          key: sleep-interval
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
    - name: config
      mountPath: /etc/nginx/conf.d
      readOnly: true
    - name: config
      mountPath: /tmp/whole-fortune-config-volume
      readOnly: true
    ports:
      - containerPort: 80
        name: http
        protocol: TCP
  volumes:
  - name: html
    emptyDir: {}
  - name: config
    configMap:   # configMap类型的卷
      name: fortune-config
      items:  # 可选，不设置则传递整个ConfigMap值
      - key: my-nginx.conf  # 指定单个条目
        path: gzip.conf # 条目的值被存储在该文件中
```

在指定单个条目时需同时设置条目的键名以及对应的文件名。**configMap卷一般以readOnly模式挂载**

如果通过上面的方法挂载到容器中的某个目录中，那么该目录下之前存在的文件会被隐藏，可能会导致容器出问题。这时候就需要用到volumeMount中的subPath字段了，这个字段可以被用作挂载卷中的某个独立文件或者是文件夹，无需挂载完整卷。

```yaml
spec:
  containers:
  - image: image
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html.someconfig.conf # 挂载到容器某一文件
      subPath: myconfig.conf  # 仅挂载卷中指定的条目，而非完整的卷
```

挂载任一种卷时均可以使用subPath属性。可以选择挂载部分卷而不是挂载完整的卷。不过这种独立文件的挂载方式会带来文件更新上的缺陷，在后面会了解到。

**为ConfigMap卷中文件设置权限**

ConfigMap卷中的所有文件的权限默认被设置为644.可以通过卷规格定义中的defaultMode属性改变默认权限。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: fortune-configmap-volume
spec:
  containers:
  - image: luksa/fortune:env
    env:
    - name: INTERVAL
      valueFrom:
        configMapKeyRef:
          name: fortune-config
          key: sleep-interval
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
    - name: config
      mountPath: /etc/nginx/conf.d
      readOnly: true
    - name: config
      mountPath: /tmp/whole-fortune-config-volume
      readOnly: true
  volumes:
  - name: html
    emptyDir: {}
  - name: config
    configMap:
      name: fortune-config
      defaultMode: 0660  # 设置权限
```

### 3.6 更新配置而不是重启pod

使用环境变量或者命令行参数作为配置源的缺陷在于无法再应用程序运行时更新配置。将ConfigMap暴露为卷可以达到热更新的效果，无需重新创建pod。

ConfigMap被更新后，卷中引用它的所有文件也会相应的更新，进程发现文件被改变之后进行重载。Kubernetes同样支持文件更新之后手动通知容器。但请注意，更新ConfigMap之后对应文件的更新耗时可能会有数分钟，不是立即就能同步更新完成的。

**文件自动更新**

被挂载到ConfigMap卷中的文件是`..data`文件夹中文件的符号链接，而`..data`文件夹同样是另一个文件夹的符号链接，可以在ConfigMap挂载的目录下查看。每当ConfigMap被更新之后，Kubernetes会创建这样一个文件夹，写入所有文件并重新被符号`..data`链接到新文件夹，通过这样的方式可以一次性修改所有文件。

**挂载至已存在文件夹的文件不会被更新**

涉及到更新ConfigMap卷需要提出一个警告：如果挂载的是容器中的单个文件，而不是完整的卷，ConfigMap更新之后对应的文件不会被更新。

**注意**

因为挂载整个ConfigMap卷，在ConfigMap更新的时候，挂载在容器内的文件也会更新(虽然不是立即的)，所以如果不是容器中的应用程序支持自动重载，那么更新ConfigMap不是一个很好的注意。而且在多个pod挂载同一个ConfigMap的情况下更新，可能会在较长的时间内导致各个pod中的文件不一致。

## 4 使用Secret给容器传递敏感数据

到目前为止，所有传递给容器的信息都是表常规的非敏感信息。然而，在配置中通常会包含一些敏感数据，如证书和私钥，需要确保其安全性。

### 4.1 介绍Secret

为了存储和分发敏感信息，Kubernetes提供了`Secret`的单独资源对象。Secret结构与ConfigMap类似，都是键值对的映射。Secret的使用方法也与ConfigMap相同。

* 将Secret条目作为环境变量传递给容器。
* 将Secret条目暴露为卷中文件。\
  Kubernetes通过仅仅将Secret分到到需要访问Secret的pod所在的机器节点来保障其安全性。另外，Secret只会存在节点的内存中，永不写入物理存储中，这样从节点上删除Secret的时候就不需要擦除磁盘了。

对于主节点本身(尤其是etcd)，Secret通常以非加密方式存储，这就需要保障主节点的安全从而确保存储在Secret中的敏感数据的安全性。这种保障不仅仅是对etcd存储的安全性保障，同样包括防止未授权用户对API服务器的访问，这是因为任何人都能通过创建pod并将Secret挂载来获取此类敏感信息。从Kubernetes1.7开始，etcd会以加密的形式存储Secret。

* 采用ConfigMap存储非敏感的文本配置数据。
* 采用Secret存储敏感的数据，通过键来引用。如果一个配置文件同时包含敏感和非敏感信息，该文件应该被存储在Secret中。

### 4.2 默认令牌Secret介绍

首先来介绍一种被默认挂载到所有容器的Secret，对任意一个pod使用命令`kubectl describe pod`

```bash
volume:
  default-token-lch48:
    TYPE: Secret
    SecretName: default-token-lch48

[root@master ~]# kubectl get secret
NAME                  TYPE                                  DATA   AGE
default-token-lch48   kubernetes.io/service-account-token   3      19d
```

可以查看一下这个Secret的详细信息

```bash
[root@master ~]# kubectl describe secret/default-token-lch48
Name:         default-token-lch48
Namespace:    default
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: default
              kubernetes.io/service-account.uid: 322faf17-27aa-4c1c-b7d8-705538d40811

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1025 bytes
namespace:  7 bytes
token: eyJhbGciOiJSUzI1NiIsImtpZCI6InVpZnRrdVUzNTVRJWa
```

可以看出这个Secret包含三个条目--ca.crt、namespace、token，包含了从pod内部安全访问Kubernetes API服务器所需的全部信息。

> **注意：这个Secret默认会被挂载到每个容器。可以通过设置pod定义中的automountServiceAccountToken:false或这只pod使用的服务账户中相同字段为false来关闭这种默认行为。**

### 4.3 创建Secret

```bash
[root@master ~]# kubectl create secret generic for --from-file=tt.txt
secret/for created
[root@master ~]# kubectl get secret/for -oyaml
apiVersion: v1
data:
  tt.txt: YWEKYmIK
kind: Secret
metadata:
  creationTimestamp: "2024-07-19T11:58:11Z"
  name: for
  namespace: default
  resourceVersion: "158180"
  selfLink: /api/v1/namespaces/default/secrets/for
  uid: 63ef9e03-f655-4da1-832e-4b52d243d3a9
type: Opaque
```

Secret条目的内容会被以Base64编码格式编码，而ConfigMap直接以纯文本展示。这种却别导致在处理YAML和JSON格式的Secret时有些麻烦，需要在设置和读取相关条目时对内容进行编解码。

**为二进制数据创建Secret**

采用Base64编码的原因很简单。Secret的条目可以涵盖二进制数据而不仅仅是纯文本。Base64编码可以将二进制数据转换为纯文本，以YAML或JSON格式展示。

> Secret甚至可以用来存储非敏感二进制数据。不过Secret的大小限制于1MB。

**stringData字段**

由于并非所有的敏感信息数据都是二进制形式的，Kubernetes允许通过Secret的stringData字段设置条目的纯文本值

```yaml
apiVersion: v1
kind: Secret
stringDate:
  foo: test  # 未被编码
data:
  tt.txt: YWEKYmIK
```

stringData字段是只写的，可以被用来设置条目值。通过`kubectl get -o yaml`获取Secret的YAML格式定义时，不会展示stringData字段，相反，stringData字段中的所有条目会被Base64编码之后展示在data字段下。

**在pod读取Secret条目**

通过Secret卷将Secret暴露给容器之后，Secret条目的值会被解码并以真实形式写入对应文件。通过环境变量暴露Secret也是如此。在这两种情况下，应用程序均无需主动解码，可以直接读取文件内容或者查找环境变量。

### 4.4 在pod使用Secret

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: fortune-https
spec:
  containers:
  - image: luksa/fortune:env
    name: html-generator
    env:
    - name: INTERVAL
      valueFrom: 
        configMapKeyRef:
          name: fortune-config
          key: sleep-interval
    volumeMounts:
    - name: html
      mountPath: /var/htdocs
  - image: nginx:alpine
    name: web-server
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
      readOnly: true
    - name: config
      mountPath: /etc/nginx/conf.d
      readOnly: true
    - name: certs
      mountPath: /etc/nginx/certs/  # 挂载到指定路径下
      readOnly: true
    ports:
    - containerPort: 80
    - containerPort: 443
  volumes:
  - name: html
    emptyDir: {}
  - name: config
    configMap:
      name: fortune-config
      items:
      - key: my-nginx-config.conf
        path: https.conf
  - name: certs   
    secret:    # 挂载Secret
      secretName: fortune-https

```

Secret跟ConfigMap一样，可以通过`defaultModes`属性指定默认权限。

**通过环境变量暴露Secret条目**

除卷之外，Secret独立条目可作为环境变量被暴露

```yaml
env:
- name: foo
  valueFrom:
    secretKeyRef:
      name: fortune-https
      key: foo
```

使用`secretKeyRef`可以将Secret条目传递给环境变量。但一般不建议这么做，因为应用程序通常会在错误报告时转储环境变量，或者是启动时打印在应用日志里，无意会暴露Secret中的敏感信息。

**镜像拉取Secret**

有时pod去拉取私有仓库的镜像时，会需要有拉取镜像所需的证书。

**在Docker Hub上使用私有镜像仓库**

可以在Docker Hub上创建私有仓库。运行一个镜像来源于私有仓库的pod时，需要做以下两件事：

* 创建包含Docker镜像仓库证书的Secret。
* pod定义中的imagePullSecrets字段引用该secret。\
  这里创建secret跟之前一样，但可以创建类型为`docker-registry`类型的secret。

**在pod中使用**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: private-pod
spec:
  imagePullSecrets:
  - name: mydockerhubsecret  # 指定Secret名称
  containers:
  - image: username/private:tag
    name: main
```

在pod中imagePullSecrets引用上面创建的`docker-registry`类型的secret即可拉取私有仓库的镜像。也可以在ServiceAccount中添加secret让所有的pod都能自动添加上镜像拉取Secret。
