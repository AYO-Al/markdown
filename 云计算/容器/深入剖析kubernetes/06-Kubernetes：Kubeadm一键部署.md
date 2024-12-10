> 本质内容包括：

通过前面几篇文章的内容，其实阐述了这样一个思想：**要真正发挥容器技术的实力，你就不能仅仅局限于对Linux容器本身的钻研和使用**。

这些知识更适合作为技术储备，以便在需要的时候可以帮你更快的定位问题，并解决问题。

而深入的学习学习容器技术的关键在于，如何使用这些技术来"容器化"你的应用。

比如，我们的应用既可能是Java Web和MySQL这样的组合，也可能是Cassandra这样的分布式系统。而要使用容器把后者运行起来，你单单通过Docker把一个Cassandra镜像跑起来是没用的。

要把Cassandra应用容器化的关键，在于如何处理好这些Cassandra容器之间的编排关系。比如，哪些Cassandra容器是主，哪些是从？主从容器如何区分？它们之间又如何进行自动发现和通信？Cassandra容器的持久化数据又如何保持，等等。

这也是为什么我们要反复强调Kubernetes项目的主要原因：这个项目体现出来的容器化"表达能力"，具有独有的先进性和完备性。这就使得它不仅能运行Java Web与MySQL这样的常规组合，还能够处理Cassandra容器集群等复杂编排问题。

作为一个典型的分布式项目，Kubernetes的部署一直以来都是挡在初学者前面的一只“拦路虎”​。尤其是在Kubernetes项目发布初期，它的部署完全要依靠一堆由社区维护的脚本。

其实，Kubernetes作为一个Golang项目，已经免去了很多类似于Python项目要安装语言级别依赖的麻烦。但是，除了将各个组件编译成二进制文件外，用户还要负责为这些二进制文件编写对应的配置文件、配置自启动脚本，以及为kube-apiserver配置授权文件等等诸多运维工作。

这个问题，在Kubernetes社区里一直没有得到足够重视。直到2017年，在志愿者的推动下，社区才终于发起了一个独立的部署工具，名叫：kubeadm。

这个项目的目的，就是要让用户能够通过这样两条指令完成一个Kubernetes集群的部署：
```bash
# 创建一个Master节点 
$ kubeadm init 

# 将一个Node节点加入到当前集群中 
$ kubeadm join <Master节点的IP和端口>
```
是不是非常方便呢？

不过，你可能也会有所顾虑：**Kubernetes的功能那么多，这样一键部署出来的集群，能用于生产环境吗**？
# kubeadm的工作原理

在上一篇文章中，已经详细介绍了Kubernetes的架构和它的组件。在部署时，它的每一个组件都是一个需要被执行的、单独的二进制文件。所以不难想象，SaltStack这样的运维工具或者由社区维护的脚本的功能，就是要把这些二进制文件传输到指定的机器当中，然后编写控制脚本来启停这些组件。

不过，在理解了容器技术之后，你可能已经萌生出了这样一个想法，为什么不用容器部署Kubernetes呢？

这样，我只要给每个Kubernetes组件做一个容器镜像，然后在每台宿主机上用docker run指令启动这些组件容器，部署不就完成了吗？

事实上，在Kubernetes早期的部署脚本里，确实有一个脚本就是用Docker部署Kubernetes项目的，这个脚本相比于SaltStack等的部署方式，也的确简单了不少。

事实上，在Kubernetes早期的部署脚本里，确实有一个脚本就是用Docker部署Kubernetes项目的，这个脚本相比于SaltStack等的部署方式，也的确简单了不少。

但是，这样做会带来一个很麻烦的问题，即：**如何容器化kubelet**。

在上一篇文章中，已经提到**kubelet是Kubernetes项目用来操作Docker等容器运行时的核心组件。可是，除了跟容器运行时打交道外，kubelet在配置容器网络、管理容器数据卷时，都需要直接操作宿主机**。

而如果现在kubelet本身就运行在一个容器里，那么直接操作宿主机就会变得很麻烦。对于网络配置来说还好，kubelet容器可以通过不开启Network Namespace（即Docker的host network模式）的方式，直接共享宿主机的网络栈。可是，**要让kubelet隔着容器的Mount Namespace和文件系统，操作宿主机的文件系统，就有点儿困难了**。

比如，如果用户想要使用NFS做容器的持久化数据卷，那么kubelet就需要在容器进行绑定挂载前，在宿主机的指定目录上，先挂载NFS的远程目录。

可是，这时候问题来了。由于现在kubelet是运行在容器里的，这就意味着它要做的这个“mount -F nfs”命令，被隔离在了一个单独的Mount Namespace中。即，kubelet做的挂载操作，不能被“传播”到宿主机上。

对于这个问题，有人说，可以使用setns()系统调用，在宿主机的Mount Namespace中执行这些挂载操作；也有人说，应该让Docker支持一个–mnt=host的参数。

但是，到目前为止，在容器里运行kubelet，依然没有很好的解决办法，我也不推荐你用容器去部署kubelet。

正因为如此，kubeadm选择了一种妥协方案：**把kubelet直接运行在宿主机上，然后使用容器部署其他的Kubernetes组件。**

所以，你使用kubeadm的第一步，是在机器上手动安装kubeadm、kubelet和kubectl这三个二进制文件。当然，kubeadm的作者已经为各个发行版的Linux准备好了安装包，所以你只需要执行：
```bash
$ yum install kubeadm
```
接下来，你就可以使用“kubeadm init”部署Master节点了。
# kubeadm init的工作流程

当你执行kubeadm init指令后，**kubeadm首先要做的，是一系列的检查工作，以确定这台机器可以用来部署Kubernetes**。这一步检查，我们称为“Preflight Checks”​，它可以为你省掉很多后续的麻烦。

其实，Preflight Checks包括了很多方面，比如：
- Linux内核的版本必须是否是3.10以上？
- Linux Cgroups模块是否可用？
- 机器的hostname是否标准？
- 在Kubernetes项目里，机器的名字以及一切存储在Etcd中的API对象，都必须使用标准的DNS命名（RFC 1123）​。用户安装的kubeadm和kubelet的版本是否匹配？
- 机器上是不是已经安装了Kubernetes的二进制文件？
- Kubernetes的工作端口10250/10251/10252端口是不是已经被占用？
- ip、mount等Linux指令是否存在？Docker是否已经安装？
**在通过了Preflight Checks之后，kubeadm要为你做的，是生成Kubernetes对外提供服务所需的各种证书和对应的目录**。

**Kubernetes对外提供服务时，除非专门开启“不安全模式”​，否则都要通过HTTPS才能访问kube-apiserver。这就需要为Kubernetes集群配置好证书文件。**

kubeadm为**Kubernetes项目生成的证书文件都放在Master节点的/etc/kubernetes/pki目录下。在这个目录下，最主要的证书文件是ca.crt和对应的私钥ca.key**。

此外，**用户使用kubectl获取容器日志等streaming操作时，需要通过kube-apiserver向kubelet发起请求，这个连接也必须是安全的。kubeadm为这一步生成的是apiserver-kubelet-client.crt文件，对应的私钥是apiserver-kubelet-client.key**。

除此之外，Kubernetes集群中还有Aggregate APIServer等特性，也需要用到专门的证书，这里我就不再一一列举了。需要指出的是，你可以选择不让kubeadm为你生成这些证书，而是拷贝现有的证书到如下证书的目录里：
```bash
/etc/kubernetes/pki/ca.{crt,key}
```
这时，kubeadm就会跳过证书生成的步骤，把它完全交给用户处理。

证书生成后，kubeadm接下来会为其他组件生成访问kube-apiserver所需的配置文件。这些文件的路径是：/etc/kubernetes/xxx.conf：
```bash
ls /etc/kubernetes/ 
admin.conf controller-manager.conf kubelet.conf scheduler.conf
```
这些文件里面记录的是，当前这个Master节点的服务器地址、监听端口、证书目录等信息。这样，对应的客户端（比如scheduler，kubelet等）​，可以直接加载相应的文件，使用里面的信息与kube-apiserver建立安全连接。

接下来，kubeadm会为Master组件生成Pod配置文件。已经在上一篇文章中和你介绍过Kubernetes有三个Master组件kube-apiserver、kube-controller-manager、kube-scheduler，而它们都会被使用Pod的方式部署起来。

你可能会有些疑问：这时，Kubernetes集群尚不存在，难道kubeadm会直接执行docker run来启动这些容器吗？

你可能会有些疑问：这时，Kubernetes集群尚不存在，难道kubeadm会直接执行docker run来启动这些容器吗？

在Kubernetes中，**有一种特殊的容器启动方法叫做“Static Pod”​。它允许你把要部署的Pod的YAML文件放在一个指定的目录里。这样，当这台机器上的kubelet启动时，它会自动检查这个目录，加载所有的Pod YAML文件，然后在这台机器上启动它们**。

从这一点也可以看出，**kubelet在Kubernetes项目中的地位非常高，在设计上它就是一个完全独立的组件，而其他Master组件，则更像是辅助性的系统容器**。

在kubeadm中，Master组件的YAML文件会被生成在/etc/kubernetes/manifests路径下。比如，kube-apiserver.yaml：
```yaml
apiVersion: v1 
kind: Pod 
metadata: 
    annotations: 
        scheduler.alpha.kubernetes.io/critical-pod: "" 
        creationTimestamp: null 
    labels: 
        component: kube-apiserver 
        tier: control-plane 
    name: kube-apiserver 
    namespace: kube-system 
spec: 
    containers: 
    - command: 
      - kube-apiserver 
      - --authorization-mode=Node,RBAC 
      - --runtime-config=api/all=true 
      - --advertise-address=10.168.0.2 
      ... 
      - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt 
      - --tls-private-key-file=/etc/kubernetes/pki/apiserver.key 
      image: k8s.gcr.io/kube-apiserver-amd64:v1.11.1 
      imagePullPolicy: IfNotPresent 
      livenessProbe: 
      ... 
      name: kube-apiserver 
      resources: 
          requests: 
              cpu: 250m 
      volumeMounts: 
      - mountPath: /usr/share/ca-certificates 
        name: usr-share-ca-certificates 
        readOnly: true 
        ... 
        hostNetwork: true 
        priorityClassName: system-cluster-critical 
        volumes: 
        - hostPath: 
            path: /etc/ca-certificates 
            type: DirectoryOrCreate 
          name: etc-ca-certificates ...
```
这个Pod里只定义了一个容器，它使用的镜像是：k8s.gcr.io/kube-apiserver-amd64:v1.11.1。这个镜像是Kubernetes官方维护的一个组件镜像。

这个容器的启动命令（commands）是kube-apiserver --authorization-mode=Node,RBAC …，这样一句非常长的命令。其实，它就是容器里kube-apiserver这个二进制文件再加上指定的配置参数而已。

如果你要修改一个已有集群的kube-apiserver的配置，需要修改这个YAML文件。

在这一步完成后，kubeadm还会再生成一个Etcd的Pod YAML文件，用来通过同样的Static Pod的方式启动Etcd。所以，最后Master组件的Pod YAML文件如下所示：
```bash
$ ls /etc/kubernetes/manifests/ 
etcd.yaml kube-apiserver.yaml kube-controller-manager.yaml kube-scheduler.yaml
```
而一旦这些YAML文件出现在被kubelet监视的/etc/kubernetes/manifests目录下，kubelet就会自动创建这些YAML文件中定义的Pod，即Master组件的容器。

**Master容器启动后，kubeadm会通过检查localhost:6443/healthz这个Master组件的健康检查URL，等待Master组件完全运行起来**。

然后，**kubeadm就会为集群生成一个bootstrap token**。在后面，只要持有这个token，任何一个安装了kubelet和kubadm的节点，都可以通过kubeadm join加入到这个集群当中。

这个token的值和使用方法，会在kubeadm init结束后被打印出来。

在token生成之后，**kubeadm会将ca.crt等Master节点的重要信息，通过ConfigMap的方式保存在Etcd当中，供后续部署Node节点使用。这个ConfigMap的名字是cluster-info**。

**kubeadm init的最后一步，就是安装默认插件**。Kubernetes默认kube-proxy和DNS这两个插件是必须安装的。它们分别用来提供整个集群的服务发现和DNS功能。其实，这两个插件也只是两个容器镜像而已，所以kubeadm只要用Kubernetes客户端创建两个Pod就可以了。
# Kubeadm join的工作流程

这个流程其实非常简单，kubeadm init生成bootstrap token之后，你就可以在任意一台安装了kubelet和kubeadm的机器上执行kubeadm join了。

可是，为什么执行kubeadm join需要这样一个token呢？

因为，任何一台机器想要成为Kubernetes集群中的一个节点，就必须在集群的kube-apiserver上注册。可是，要想跟apiserver打交道，这台机器就必须要获取到相应的证书文件（CA文件）​。可是，为了能够一键安装，我们就不能让用户去Master节点上手动拷贝这些文件。

所以，kubeadm至少需要发起一次“不安全模式”的访问到kube-apiserver，从而拿到保存在ConfigMap中的cluster-info（它保存了APIServer的授权信息）​。而bootstrap token，扮演的就是这个过程中的安全验证的角色。

只要有了cluster-info里的kube-apiserver的地址、端口、证书，kubelet就可以以“安全模式”连接到apiserver上，这样一个新的节点就部署完成了。

只要有了cluster-info里的kube-apiserver的地址、端口、证书，kubelet就可以以“安全模式”连接到apiserver上，这样一个新的节点就部署完成了。

接下来，你只要在其他节点上重复这个指令就可以了。
# 配置kubeadm的部署参数

我在前面讲了kubeadm部署Kubernetes集群最关键的两个步骤，kubeadm init和kubeadm join。相信你一定会有这样的疑问：kubeadm确实简单易用，可是我又该如何定制我的集群组件参数呢？

比如，我要指定kube-apiserver的启动参数，该怎么办？

在这里，我强烈推荐你在使用kubeadm init部署Master节点时，使用下面这条指令：
```bash
$ kubeadm init --config kubeadm.yaml
```
这时，你就可以给kubeadm提供一个YAML文件。

通过制定这样一个部署参数配置文件，你就可以很方便地在这个文件里填写各种自定义的部署参数了。比如，我现在要指定kube-apiserver的参数，那么我只要在这个文件里加上这样一段信息：
```bash
... 
apiServerExtraArgs: 
  advertise-address: 192.168.0.103 
  anonymous-auth: false 
  enable-admission-plugins: AlwaysPullImages,DefaultStorageClass 
  audit-log-path: /home/johndoe/audit.log
```
然后，kubeadm就会使用上面这些信息替换/etc/kubernetes/manifests/kube-apiserver.yaml里的command字段里的参数了。

而这个YAML文件提供的可配置项远不止这些。比如，你还可以修改kubelet和kube-proxy的配置，修改Kubernetes使用的基础镜像的URL（默认的k8s.gcr.io/xxx镜像URL在国内访问是有困难的）​，指定自己的证书文件，指定特殊的容器运行时等等。这些配置项，就留给你在后续实践中探索了。
# 总结

在今天的这次分享中，我重点介绍了kubeadm这个部署工具的工作原理和使用方法。紧接着，我会在下一篇文章中，使用它一步步地部署一个完整的Kubernetes集群。

从今天的分享中，你可以看到，kubeadm的设计非常简洁。并且，它在实现每一步部署功能时，都在最大程度地重用Kubernetes已有的功能，这也就使得我们在使用kubeadm部署Kubernetes项目时，非常有“原生”的感觉，一点都不会感到突兀。

而kubeadm的源代码，直接就在kubernetes/cmd/kubeadm目录下，是Kubernetes项目的一部分。

现在，来回答一下上面那个问题，kubeadm是否能用于生产环境？

这个问题的答案是可以，因为生产环境的kubernetes的集群应该是一个多节点的高可用集群。具体可以参考[利用 kubeadm 创建高可用集群](https://kubernetes.io/zh-cn/docs/setup/production-environment/tools/kubeadm/high-availability/)





