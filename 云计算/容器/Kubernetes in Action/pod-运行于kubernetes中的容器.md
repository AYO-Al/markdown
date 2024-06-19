> 本章内容包括
> - 创建、启动和停止pod
> - 使用标签组织pod和其他资源
> - 使用特定标签对所有pod执行操作
> - 使用命名空间将多个pod分到不重叠的组中
> - 调度pod到指定类型的工作节点
> 
> pod是kubernetes中最为重要的核心概念，其他对象仅仅为管理、暴露pod或被pod使用。

# pod是什么
pod是一组并置的容器，代表了kubernetes中最基本构建模块。在实际应用中不会单独部署容器，更多的是针对一组pod的容器进行部署和操作。但这并不意味这一个pod要包含多个容器，kubernetes以pod为基本单位，所以即使一个pod中包含了多个容器，但这多个容器实际上是运行在一个node中。
## 为什么需要pod
为什么kubernetes需要pod？而不是直接使用容器？为什么需要同时运行多个容器？不能把所有进程都放在一个容器里面嘛？
### 为什么运行多个容器？
容器被设计为每个容器只运行一个进程(除非进程本身产生子进程)，这样能保证容器和服务具有相同的生命周期，这样才能最好的应用容器编排来管理好容器和服务。如果一个容器内运行多个不相干的进程，那么kubernetes将无法很好的管理这些进程。设计每个容器只允许一个进程有以下好处：
- 简化管理和伸缩：每个容器只运行一个应用程序，使得水平伸缩变得容易。当需要更多资源时，可以快速创建新的容器，而无需担心多个应用程序之间的相互影响。
- 提高服用性：单个容器只运行一个应用程序，可以方便地将容器重新用于其他项目或目的，从而提高容器的复用性。
- 简化故障排查：当容器出现故障时，开发人员可以专注于排查特定应用程序的问题，而无需对整个系统的各个部分进行排查。这有助于提高容器的可移植性和可预测性。
- 提高应用持续生命周期管理的灵活性：升级程序时，可以将影响范围控制在更小的粒度。这有助于避免在升级某个服务时中断相同容器中的其他进程。
- 提高安全性和隔离性：每个容器只运行一个应用程序，有助于提供更安全的服务和应用程序间的隔离。这有助于保持强大的安全状态，或遵守PCI之类的规定。
## 了解pod
由于不能将多个进程聚集在一个单独的容器中，所以需要一种更高级的结构来将容器绑定在一起，并将它们作为一个单元进行管理，这就是请问什么需要pod的原因。

在包含容器的pod下，我们可以同时运行一些具有超亲密度的进程，并为它们提供相同的环境。此时这些进程就好像全部运行在单个容器中一样，同时又保持着一定的隔离。这样一来就能全面利用容器所提供的特性，同时对这些进程来说它们就像运行在一个机器上一样。
### 同一pod中的部分隔离
容器与容器之间是完全隔离的，但当一组容器具有超亲密度关系的时候，我们会期望它们之间是部分隔离，而不是完全隔离。也就是隔离容器组，让每个容器组内的容器共享一些资源，而不是全部。kubernetes使用pod来使一组容器共享相同的命名空间。如以下几个命名空间：
- UTS
- IPC
- NET
新版的kubernetes也支持共享PID命名空间，但并不是默认开启的，可以通过设置pod的`shareProcessNamespace`的值为true来开启这个功能。

但当涉及到文件系统时，情况就变的有点不一样了。因为容器的文件系统来自容器镜像，因此在默认情况下，每个容器的文件系统与其他容器完全隔离，所以需要使用kubenetes中的volumn资源来共享文件目录。
### pod网络
由于一个pod中的容器运行于相同的Network空间，所以一个pod中的容器共享相同的IP和端口端口空间，所以在同一个pod中运行的多个进程注意别绑定到相同的端口。

kubernetes集群中所有的pod都在同一个共享网络地址空间中，所以每个pod都可以通过其他pod的IP地址来实现相互访问。同一个集群下的pod通信是没有net(网络地址转换)的。这是通过网络插件实现的，所以不同的网络插件有不同的实现方式，但目的都是为了给pod提供一个统一的网络环境，使pod可以直接通信。
## 通过pod合理管理容器
由于pod比较轻量，可以让我们在几乎没有任何额外开销的情况下拥有尽可能多的pod，所以我们应该将应用持续组织到多个pod中，每个pod只保存具有超亲密度关系的容器。
### 将多层应用分散到多个pod中
在云原生架构中，我们应该尽可能的把不同的组件放到不同的pod中，并且把pod调度到不同的工作节点中，这样才能最大的利用不同节点的计算资源，提高基础架构的利用率。

另一个将不同组件放到不同pod上的考虑是kubernetes的扩缩容是基于pod的，如果将多个组件放到同一个pod中，那么扩缩容时也将把多个组件同时进行，所以当一个组件有单独扩缩容的需求时，应该把它放到一个单独的pod中。
### 何时在pod中使用多个容器
一般将具有超亲密度关系的容器放在一个pod中，例如，部署一个web应用和其日志收集器，这个时候就需要把这两个容器放在一个pod中。这也是kubernetes中常用的边车模式(siedecar)。

当需要决定多个容器是否需要存放在一个pod中时，可以根据以下问题决定：
- 它们需要一起运行还是可以运行在不同的主机上？
- 它们代表的时一个整体还是相互独立的组件？
- 它们必须一起扩缩容还是可以分别进行？

基本上，除了具有超亲密度的容器，一般倾向于在单独的pod中运行单独的容器。
# 用YAML创建pod
pod和其他kubernetes资源通常时通过向kubernetes REST API提供JSON或YAML描述文件来创建的。一般来说，pod的yaml文件会包含以下几个部分：
- apiVersion：YAMl描述文件所使用的Kubernetes API版本
- kind：kubernetes对象资源类型
- metadata：pod元数据，包括名称、标签、注解、命名空间等
- spec：pod规格/内容说明，包括pod的容器列表、volume等
- status：只读的运行时数据，pod及其内部容器的详细状态，如pod所处的条件，每个容器的描述和状态，以及内部IP和其他基本信息。一般创建时不需要指定
```yaml
# kubia-manual.yaml
apiVersion: v1  # 使用v1版本的API
kind: Pod       # 描述一个pod
metadata:
  name: kubia-manual # 名字为kubia-manual
spec:
  containers:       # pod容器列表
  - image: luksa/kubia  # 镜像的名称
    name: kubia   # 容器的名称
    ports:         # 应用监听端口
    - containerPort: 8080
      protocol: TCP
```
在pod定义中指定端口纯粹是展示性的(informational)。忽略它们对于客户端是否可以通过端口连接到pod不会带来任何影响。但明确定义端口任然是有意义的，在端口定义下，每个使用集群的人都可以快速查看每个pod对外暴露的端口，还可以为每个端口定义一个名称，方便我们使用。
> 在编写定义文件时，如果不清楚对应的API对象都支持什么属性，可以在https://kubernetes.io/zh-cn/docs/reference/kubernetes-api/对对应API属性进行查找。
> 
> 也可以使用explain命令查看对应API资源的字段帮助，如：
> 
> kubectl explain pods。
>
> 这将打印出对象的解释并列出对象可以包含的属性，并且可以深入查看各个属性的更多信息，如这样可以查看spec属性：
>
> kubectl explain pods.spec
## 创建pod
在编写好yaml描述文件后，就需要使用这个描述文件把具体的资源对象创建出来，可以使用以下两个命令进行创建
```bash
kubectl create -f kubia-manual.yaml
kubectl apply -f kubia-manual.yaml
```
`create`和`apply`命令都能对资源进行创建，两者又有一些不同：
- `create`创建时如果资源已经存在它会报错并停止执行，意味着不能使用`create`来更新现有资源的配置。
- `apply`使用声明式的方式来更新资源，它会比较yaml文件中的配置和集群中现有的资源配置，然后应用差异，意味着可以使用`apply`来更新资源的配置，而不需要手动删除和重新创建资源。

在平时创建资源时推荐使用`apply`方式进行创建。当资源创建完成后，可以使用以下命令拿到资源的详细信息：
```txt
使用get命令可以简单查看pod是否在正常运行
kubectl get pods
json：以 JSON 格式输出资源的详细信息。
kubectl get pods -o json
yaml：以 YAML 格式输出资源的详细信息。
kubectl get pods -o yaml / describe
name：以简短的资源名称格式输出资源。这种格式仅显示资源的名称，不包括其他信息。
kubectl get pods -o name
wide：以表格格式输出资源的详细信息，包括额外的信息，如节点名称、IP 地址等。
kubectl get pods -o wide
custom-columns：以表格格式输出资源的自定义列。您可以使用此选项自定义要显示的列和列标题。
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase
jsonpath：以 JSONPath 表达式输出资源的自定义信息。您可以使用此选项自定义要显示的信息。
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
go-template：以 Go 模板输出资源的自定义信息。您可以使用此选项自定义要显示的信息。
kubectl get pods -o go-template='{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'
```
## 查看应用程序日志
容器化的应用程序通常会将日志记录到标准输出和标准错误输出流，而不是将其写入文件，但容器运行时将这些流重定向到文件，并使用相关命令来查看日志`docker logs <container id>`，也可以使用kubernetes提供的命令`kubectl logs <pod_name>`
```bash
kubectl logs <pod_name> #获取单个pod日志
kubectl logs <pod_name> -c<container_name> # 多容器pod指定获取容器日志
kubectl logs -f <pod_name> # 实时查看日志
kubectl logs --tail=<number_of_lines> <pod_name> # 限制显示日志行数
kubectl logs --timestamps <pod_name> # 显示时间戳
kubectl logs --previous <pod_name> # 如果容器已经重启，可以使用previous获取以前容器日志
```
每天或每次日志文件达到10M的时候，容器日志会自动轮替，`logs`命令仅显示最后一次轮替后的日志条目。可以在docker配置文件`/etc/docker/daemon.json`中设置
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "1"
  }
}
```
当pod删除后，pod中的日志也会随之删除，除非配置设置中心化的、集群范围的日志系统，将所有日志存储到中心存储中。
## 使用标签组织pod
一般来说，kubernetes集群中会有很多资源对象实例，如果没有一种有效的方式对大规模的实例进行分组管理，那kubernetes架构就会显的非常混乱，所以也就有了标签。

标签是一种简单却功能强大的kubernetes特性，不仅可以组织pod，也可以组织其他kubernetes资源。准确来说，标签是可以附加到资源上的任意键值对，用以选择/过滤具有确切标签的资源(用标签选择器完成)。在同一个资源对象上，标签的键必须是唯一的。通常在编写描述文件时就会将标签附加到资源上，但也可以在资源创建后对标签进行设置，且无需重新创建资源。

标签是一个键值对，其中键和值都是字符串。键和值都必须是有效的 DNS 标签，即它们必须符合以下规则：
- 键和值的长度必须在 1 到 63 个字符之间。
- 键和值只能包含字母（大写或小写）、数字、连字符（-）和下划线（_）。
- 键必须以字母或数字开头和结尾。
```yaml
# kubia-manual-with-labels.yaml
apiVersion: v1
kind: Pod
metadata:
  name: kubia-manual-v2
  labels:  # 设置标签
    creation_method: manual
    env: prod
spec:
  containers:
  - image: luksa/kubia
    name: kubia
    ports:
    - containerPort: 8080
      protocol: TCP
```
在上面这个描述文件中，我们给`kubia-manual-v2`这个pod打上了两个标签，在成功创建了这个pod实例后，可以使用`kubectl get po --show-labels`进行查看标签，也可以使用`-L creation_method,env`过滤感兴趣的标签。常用的标签操作如下：
```bash
kubectl label pods <pod_name> <key>=<value> # 添加标签
kubectl label pods <pod_name> <key>=<new_value> --overwrite # 修改标签
kubectl label pods <pod_name> <key>- # 删除标签
kubectl get pods -l <key>=<value> # 选择标签
# -l <key>=<value>：选择对应标签资源
# -l <key>：选择具有标签的资源
# -l '!<key>'：选择不包含对应标签资源
# -l <key>!=<value>
# -l app in (gem-account)
# -l app notin (gem-account)
```
如果想要过滤多个条件，可以使用逗号分隔条件。`-l 'app notin (gem-account),app=gem-battle-blue'`

## 使用标签和选择器来约束pod调度
在目前未知，我们使用yaml描述文件创建出来的pod都被随机的调度到工作节点上，这正是kubernetes集群中工作的正确方式，由于kubernetes将所有工作节点抽象为一个整体的大型部署平台，所以pod实际被调度到哪个节点是无关紧要的。但实际上由于硬件资源的不同，我们有时候可能会想要把需要某些硬件特点的pod调度到某个具体的节点。
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kubia-gpu
spec:
  nodeSelector:  # 节点选择器
    gpu: "true"
  containers:
  - image: luksa/kubia
    name: kubia
```
添加节点选择器后，这个pod指挥调度到具有`gpu："true"`标签的节点上。每个节点上都会有一个`kubernetes.io/hostname`标签，所以我们也可以指定一个具体的节点调度，但不推荐这么做，如果这个节点宕机会导致pod不可调度。

## 注解
除注解外，pod和其他对象还可以包含注解。注解也是键值对，但与标签不同，注解并不是为了保存标识信息而存在的，也没有注解选择器这样的东西。

注解可以容纳更多的信息，且主要用于工具使用。向kubernetes引入新特性时，通常会使用注解。一旦所需的API更改变得清晰并得到所有相关人员的认可，就会引入新字段并废弃相关注解。注解是一组键值对，其中键是字符串，值可以是字符串、布尔值、整数等类型。注解的键必须是唯一的，且不能包含空格、制表符等特殊字符。注解的值可以是任意字符串，但不能包含换行符。注解的大小限制为 256KB。这意味着不能在注解中存储大量数据。
```yaml
apiVersion: v1
kind: pod
metadata:
  annotations:
    deployment.kubernetes.io/revision: '1'
```
大量使用注解可以为每个pod或其他API对象添加说明，以便每个使用该集群的人都可以快速查找有关每个单独对象的信息。例如，指定创建对象的人员姓名的注解可以使在集群工作的人员之间的协作更加便利。常用注解操作如下：
```bash
kubectl annotate pod my-pod my-annotation=my-value # 新增
kubectl describe pod my-pod # 查看
kubectl annotate pod my-pod my-annotation=new-value --overwrite # 修改
kubectl annotate pod my-pod my-annotation- # 删除
```

## 命名空间
前面我们介绍过标签，标签可以给资源分组，但如果没有明确对标签进行选择，那么我们还是默认可以看到所有资源的，如果想将资源分为完全独立且不重叠的组时，可以使用命名空间，在不同的命名空间内，我们可以使用相同的资源名称。资源名称只需要在命名空间内保持唯一即可。
### 为什么需要命名空间
在使用多个namespace前提下，我们可以将包含大量组件的复杂系统拆分为更小的不同组，这些不同组也可以用于在多租户环境中分配资源，将资源分配为生产、开发和QA环境，或者以其他任何你需要的方式分配资源。可以使用`kubectl get ns`查看所有命名空间。默认情况下，我们一直在操作`default`命名空间下的资源，如果想查看其他命名空间下的资源，可以使用`-n namespace`指定。除了隔离资源，命名空间限制某些用户访问某些资源，还能限制单个用户可用的计算资源数量。
### 命名空间常用操作
命名空间是和其他资源一样的kubernetes资源，所以可以通过将yaml文件提交到kubernetes API服务器来创建该资源。
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: custom-namespace
```
由于namespace资源属性比较简单，所以我们可以直接使用`kubectl create namespace name`来进行创建，使用以上yaml文件只是为了强化kubernetes中的所有内容都是一个API对象这一概念。可以通过向API服务器提交`YAML manifest`来实现创建、删除、更新和读取。
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kubia-manual
  namespace: custom-namespace # 指定命名空间
spec:
  containers:
  - image: luksa/kubia
    name: kubia
    ports:
    - containerPort: 8080
      protocol: TCP
```
我们在custom-namespace命名空间中创建了一个pod。但值得注意的是，命名空间实际上不提供对正在运行的对象的任何隔离。不同命名空间的pod是否能通信取决于kubernetes所使用的网络解决方案。
## pod常用操作
- 按名称删除pod：`kubectl delete po po_name[ pod_name1....]`
  - 指示k8s终止pod中所有容器，向进程发送`SIGTERM`信号并等待30s，如果没有正常关闭则发送`SIGKILL`终止进程。
- 按标签删除pod：`kubectl delete po -l key=value`
- 通过删除命名空间来删除pod：`kubectl delete ns ns_name`
- 删除命名空间下所有pod/资源：`kubectl delete po/all --all`
  - 有些资源并不包括在all中，需要明确指定出来，如srcret