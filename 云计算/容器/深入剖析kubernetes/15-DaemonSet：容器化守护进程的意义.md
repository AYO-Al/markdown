> 本章内容包括：
> - StatefulSet如何控制更新策略
> - DaemonSet工作原理
> - DaemonSet版本控制

# 1 StatefulSet更新策略

在上一篇文章中，我和你详细分享了使用StatefulSet编排“有状态应用”的过程。从中不难看出，StatefulSet其实就是对现有典型运维业务的容器化抽象。也就是说，你一定有方法在不使用Kubernetes、甚至不使用容器的情况下，自己DIY一个类似的方案出来。但是，一旦涉及到升级、版本管理等更工程化的能力，Kubernetes的好处，才会更加凸现。

这样，StatefulSet Controller就会按照与Pod编号相反的顺序，从最后一个Pod开始，逐一更新这个StatefulSet管理的每个Pod。而如果更新发生了错误，这次“滚动更新”就会停止。此外，StatefulSet的“滚动更新”还允许我们进行更精细的控制，比如金丝雀发布（Canary Deploy）或者灰度发布，这意味着应用的多个实例中被指定的一部分不会被更新到最新的版本。

这个字段，正是StatefulSet的spec.updateStrategy.rollingUpdate的partition字段。

比如，现在我将前面这个StatefulSet的partition字段设置为2：
```bash
$ kubectl patch statefulset mysql -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":2}}}}'
statefulset.apps/mysql patched
```

其中，kubectl patch命令后面的参数（JSON格式的），就是partition字段在API对象里的路径。所以，上述操作等同于直接使用 kubectl edit命令，打开这个对象，把partition字段修改为2。

这样，我就指定了当Pod模板发生变化的时候，比如MySQL镜像更新到5.7.23，那么只有序号大于或者等于2的Pod会被更新到这个版本。并且，如果你删除或者重启了序号小于2的Pod，等它再次启动后，也会保持原先的5.7.2版本，绝不会被升级到5.7.23版本。
# 2 DaemonSet

话说回到今天的主角--DaedonSet。

顾名思义，DaemonSet的主要作用，是让你在Kubernetes集群里，运行一个Daemon Pod。 所以，这个Pod有如下三个特征：

1.  这个Pod运行在Kubernetes集群里的每一个节点（Node）上；

2.  每个节点上只有一个这样的Pod实例；

3.  当有新的节点加入Kubernetes集群后，该Pod会自动地在新节点上被创建出来；而当旧节点被删除后，它上面的Pod也相应地会被回收掉。

这个机制听起来很简单，但Daemon Pod的意义确实是非常重要的。我随便给你列举几个例子：

1.  各种网络插件的Agent组件，都必须运行在每一个节点上，用来处理这个节点上的容器网络；

2.  各种存储插件的Agent组件，也必须运行在每一个节点上，用来在这个节点上挂载远程存储目录，操作容器的Volume目录；

3.  各种监控组件和日志组件，也必须运行在每一个节点上，负责这个节点上的监控信息和日志搜集。

更重要的是，跟其他编排对象不一样，DaemonSet开始运行的时机，很多时候比整个Kubernetes集群出现的时机都要早。

这个乍一听起来可能有点儿奇怪。但其实你来想一下：如果这个DaemonSet正是一个网络插件的Agent组件呢？

这个时候，整个Kubernetes集群里还没有可用的容器网络，所有Worker节点的状态都是NotReady（NetworkReady=false）。这种情况下，普通的Pod肯定不能运行在这个集群上。所以，这也就意味着DaemonSet的设计，必须要有某种“过人之处”才行。
# 3 DaemonSet工作原理

为了弄清楚DaemonSet的工作原理，我们还是按照老规矩，先从它的API对象的定义说起。
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-elasticsearch
  namespace: kube-system
  labels:
    k8s-app: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd-elasticsearch
  template:
    metadata:
      labels:
        name: fluentd-elasticsearch
    spec:
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: fluentd-elasticsearch
        image: k8s.gcr.io/fluentd-elasticsearch:1.20
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

可以看到，DaemonSet跟Deployment其实非常相似，只不过是没有replicas字段；它也使用selector选择管理所有携带了name=fluentd-elasticsearch标签的Pod。

而这些Pod的模板，也是用template字段定义的。在这个字段中，我们定义了一个使用 fluentd-elasticsearch:1.20镜像的容器，而且这个容器挂载了两个hostPath类型的Volume，分别对应宿主机的/var/log目录和/var/lib/docker/containers目录。

显然，fluentd启动之后，它会从这两个目录里搜集日志信息，并转发给ElasticSearch保存。这样，我们通过ElasticSearch就可以很方便地检索这些日志了。

**需要注意的是，Docker容器里应用的日志，默认会保存在宿主机的/var/lib/docker/containers/{{.容器ID}}/{{.容器ID}}-json.log文件里，所以这个目录正是fluentd的搜集目标。**

那么，**DaemonSet又是如何保证每个Node上有且只有一个被管理的Pod呢**？

显然，这是一个典型的“控制器模型”能够处理的问题。

DaemonSet Controller，首先从Etcd里获取所有的Node列表，然后遍历所有的Node。这时，它就可以很容易地去检查，当前这个Node上是不是有一个携带了name=fluentd-elasticsearch标签的Pod在运行。

而检查的结果，可能有这么三种情况：

1.  没有这种Pod，那么就意味着要在这个Node上创建这样一个Pod；

2.  有这种Pod，但是数量大于1，那就说明要把多余的Pod从这个Node上删除掉；

3.  正好只有一个这种Pod，那说明这个节点是正常的。

在创建Pod时候，可以指定节点亲和性调度pod到目标节点。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: with-node-affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: metadata.name
            operator: In
            values:
            - node-geektime
```

而在这里，我定义的nodeAffinity的含义是：

1.  requiredDuringSchedulingIgnoredDuringExecution：它的意思是说，这个nodeAffinity必须在每次调度的时候予以考虑。同时，这也意味着你可以设置在某些情况下不考虑这个nodeAffinity；

2.  这个Pod，将来只允许运行在“metadata.name”是“node-geektime”的节点上。

在这里，你应该注意到nodeAffinity的定义，可以支持更加丰富的语法，比如operator: In（即：部分匹配；如果你定义operator: Equal，就是完全匹配），这也正是nodeAffinity会取代nodeSelector的原因之一。

所以，我们的DaemonSet Controller会在创建Pod的时候，自动在这个Pod的API对象里，加上这样一个nodeAffinity定义。其中，需要绑定的节点名字，正是当前正在遍历的这个Node。

当然，DaemonSet并不需要修改用户提交的YAML文件里的Pod模板，而是在向Kubernetes发起请求之前，直接修改根据模板生成的Pod对象。这个思路，也正是我在前面讲解Pod对象时介绍过的。

此外，DaemonSet还会给这个Pod自动加上另外一个与调度相关的字段，叫作tolerations。这个字段意味着这个Pod，会“容忍”（Toleration）某些Node的“污点”（Taint）。

而DaemonSet自动加上的tolerations字段，格式如下所示：
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: with-toleration
spec:
  tolerations:
  - key: node.kubernetes.io/unschedulable
    operator: Exists
    effect: NoSchedule
```

这个Toleration的含义是：“容忍”所有被标记为unschedulable“污点”的Node；“容忍”的效果是允许调度。

而在正常情况下，被标记了unschedulable“污点”的Node，是不会有任何Pod被调度上去的（effect: NoSchedule）。可是，DaemonSet自动地给被管理的Pod加上了这个特殊的Toleration，就使得这些Pod可以忽略这个限制，继而保证每个节点上都会被调度一个Pod。当然，如果这个节点有故障的话，这个Pod可能会启动失败，而DaemonSet则会始终尝试下去，直到Pod启动成功。

这时，你应该可以猜到，我在前面介绍到的DaemonSet的“过人之处”，**其实就是依靠Toleration实现的**。

这种机制，正是我们在部署Kubernetes集群的时候，能够先部署Kubernetes本身、再部署网络插件的根本原因：因为当时我们所创建的Weave的YAML，实际上就是一个DaemonSet。

至此，通过上面这些内容，你应该能够明白，DaemonSet其实是一个非常简单的控制器。在它的控制循环中，只需要遍历所有节点，然后根据节点上是否有被管理Pod的情况，来决定是否要创建或者删除一个Pod。

只不过，在创建每个Pod的时候，DaemonSet会自动给这个Pod加上一个nodeAffinity，从而保证这个Pod只会在指定节点上启动。同时，它还会自动给这个Pod加上一个Toleration，从而忽略节点的unschedulable“污点”。

当然，**你也可以在Pod模板里加上更多种类的Toleration，从而利用DaemonSet达到自己的目的**。
# 4 DaemonSet版本控制

当你创建号DaemonSet之后，你会发现它跟Deployment一样，也有DESIRED、CURRENT等多个状态字段。这也就意味着，DaemonSet可以像Deployment那样，进行版本管理。这个版本，可以使用kubectl rollout history看到：
```bash
$ kubectl rollout history daemonset fluentd-elasticsearch -n kube-system
daemonsets "fluentd-elasticsearch"
REVISION  CHANGE-CAUSE
1         <none>
```

接下来，我们来把这个DaemonSet的容器镜像版本到v2.2.0，然后使用`kubectl rollout status`命令来看这个滚动更新的过程
```bash
$ kubectl rollout status ds/fluentd-elasticsearch -n kube-system
Waiting for daemon set "fluentd-elasticsearch" rollout to finish: 0 out of 2 new pods have been updated...
Waiting for daemon set "fluentd-elasticsearch" rollout to finish: 0 out of 2 new pods have been updated...
Waiting for daemon set "fluentd-elasticsearch" rollout to finish: 1 of 2 updated pods are available...
daemon set "fluentd-elasticsearch" successfully rolled ou
```

有了版本号，你也就可以像Deployment一样，将DaemonSet回滚到某个指定的历史版本了。

而我在前面的文章中讲解Deployment对象的时候，曾经提到过，Deployment管理这些版本，靠的是“**一个版本对应一个ReplicaSet对象**”。可是，**DaemonSet控制器操作的直接就是Pod，不可能有ReplicaSet这样的对象参与其中。那么，它的这些版本又是如何维护的呢？**

所谓，一切皆对象！

在Kubernetes项目中，任何你觉得需要记录下来的状态，都可以被用API对象的方式实现。当然，“版本”也不例外。

Kubernetes v1.7之后添加了一个API对象，名叫ControllerRevision，专门用来记录某种Controller对象的版本。比如，你可以通过如下命令查看fluentd-elasticsearch对应的ControllerRevision：
```bash
$ kubectl get controllerrevision -n kube-system -l name=fluentd-elasticsearch
NAME                               CONTROLLER                             REVISION   AGE
fluentd-elasticsearch-64dc6799c9   daemonset.apps/fluentd-elasticsearch   2          1h
```

而如果你使用kubectl describe查看这个ControllerRevision对象：
```bash
$ kubectl describe controllerrevision fluentd-elasticsearch-64dc6799c9 -n kube-system
Name:         fluentd-elasticsearch-64dc6799c9
Namespace:    kube-system
Labels:       controller-revision-hash=2087235575
              name=fluentd-elasticsearch
Annotations:  deprecated.daemonset.template.generation=2
              kubernetes.io/change-cause=kubectl set image ds/fluentd-elasticsearch fluentd-elasticsearch=k8s.gcr.io/fluentd-elasticsearch:v2.2.0 --record=true --namespace=kube-system
API Version:  apps/v1
Data:
  Spec:
    Template:
      $ Patch:  replace
      Metadata:
        Creation Timestamp:  <nil>
        Labels:
          Name:  fluentd-elasticsearch
      Spec:
        Containers:
          Image:              k8s.gcr.io/fluentd-elasticsearch:v2.2.0
          Image Pull Policy:  IfNotPresent
          Name:               fluentd-elasticsearch
...
Revision:                  2
Events:                    <none>
```

会看到，这个ControllerRevision对象，实际上是在Data字段保存了该版本对应的完整的DaemonSet的API对象。并且，在Annotation字段保存了创建这个对象所使用的kubectl命令。

接下来，我们可以尝试将这个DaemonSet回滚到Revision=1时的状态：
```bash
$ kubectl rollout undo daemonset fluentd-elasticsearch --to-revision=1 -n kube-system
daemonset.extensions/fluentd-elasticsearch rolled back
```

这个kubectl rollout undo操作，实际上相当于读取到了Revision=1的ControllerRevision对象保存的Data字段。而这个Data字段里保存的信息，就是Revision=1时这个DaemonSet的完整API对象。

所以，**现在DaemonSet Controller就可以使用这个历史API对象，对现有的DaemonSet做一次PATCH操作（等价于执行一次kubectl apply -f “旧的DaemonSet对象”），从而把这个DaemonSet“更新”到一个旧版本**。

这也是为什么，在执行完这次回滚完成后，你会发现，**DaemonSet的Revision并不会从Revision=2退回到1，而是会增加成Revision=3。这是因为，一个新的ControllerRevision被创建了出来。**