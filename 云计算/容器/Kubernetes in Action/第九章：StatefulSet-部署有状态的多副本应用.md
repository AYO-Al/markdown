> 本章内容包括：
> - 部署有状态集群应用
> - 为每个副本pod实例提供独立存储
> - 保证pod副本有固定的名字和主机名
> - 按预期顺序启停pod副本
> - 通过DNS SRV记录查询伙伴节点

经过前面的介绍已经知道了如何运行一个单实例pod和使用Deployment部署无状态的多副本，还有如何通过持久化存储运行一个有状态pod。
# 1 复制有状态pod

ReplicaSet通过一个pod模板创建多个pod副本。这些pod除了名字和IP地址不同外，没有别的差异。如果pod模板里描述了一个关联到特定持久卷申领的数据卷，那么ReplicaSet的所有副本都将共享这个持久卷申领，也就是绑定到同一个持久卷申领，也就是绑定到同一个申领的持久卷。

因为是在pod模板里关联申领的，又会根据pod模板创建多个pod副本，则不能对每个副本都指定独立的持久卷申领。所以也不能通过一个ReplicaSet来运行一个每个实例都需要独立存储的分布式数据存储服务。在此之前学的所有的资源对象都不能做到这个事情，所以需要一个新的对象。
## 1.1 运行每个实例都有单独存储的多副本

**手动创建pod**

可以手动创建多个pod，然后在每个pod中指定单个存储，但这种方法不好管理，pod宕机后需要手动重启，比较麻烦，不推荐使用。

**创建多个ReplicaSet**

还可以创建多个ReplicaSet，让一个ReplicaSet管理一个pod，这样在pod宕机后会被ReplicaSet自动拉起。但这种方法相较于单个ReplicaSet来说还是比较笨重，且在需要扩容的场景下需要一直创建新的ReplicaSet来承担扩容任务。

## 1.2 每个pod都提供稳定的标识

除了上面说的存储需求，集群应用也会要求每一个实例拥有生命周期内唯一标识。pod可以随时被删掉，然后被新的pod代替。当一个pod被代替时，尽管新的pod也可能使用被删掉pod数据卷中的数据，但它确实拥有全新主机名和IP的崭新pod。在一些应用中，当启动的实例拥有完全崭新的网络标识，但还使用旧实例的数据时，很可能会引起问题。

为什么一些应用需要维护一个稳定的网络标识呢？这个需求在有状态的分布式应用中很普遍。这类应用要求管理者在每个集群成员的配置文件中列出所有其他集群成员和它们的IP(或主机名)。但是在Kubernetes中，每次重新调度一个pod，这个新的pod就会有一个新的主机名和IP地址，这样就要求当集群中任何一个成员被重新调度后，整个应用集群都需要重新配置。
# 2 StatefulSet

可以创建一个StatefulSet资源替代ReplicaSet来运行这类pod。它是专门定制的一类应用，这类应用中的每一个实例都是不可代替的个体，都拥有稳定的名字和状态。
## 2.1 对比StatefulSet和ReplicaSet

要很好的理解StatefulSet的用途，最好先与ReplicaSet对比一下。

**通过宠物与牛的类比来理解状态**

你可以已经听说过宠物与牛的类比。如果没有，先简单介绍一下，可以把我们的应用看做宠物或牛。
> Statefulset最初被称为PetSet，这个名字来源于宠物与牛的类比。

对于无状态的应用来说，行为非常像农场里的牛。一个实力挂掉后并没有什么影响，可以创建一个新实例，而让用户完全无感知。

而有状态应用更像一个宠物。若一只宠物死掉，不能买到一只完全一样的，而不让用户感知到。若要替换掉这只宠物，需要找到一只行为举止与之完全一致的宠物。对应用来说，意味着新的实例需要拥有跟旧实例完全一致的状态和标识。

**StatefulSet与ReplicaSet对比**

ReplicaSet管理的pod副本比较像牛，这是因为它们都是无状态的，任何时候它们都可以被一个全新的pod替换。然而有状态的pod需要不同的方法，当一个有状态的pod挂掉后(或者它所在的节点故障)，这个pod实例需要在其他节点重新创建，但是新的实例必须与之前被替换的实例拥有完全相同的名称、网络标识和状态，这就是StatefulSet管理pod的特点。

StatefulSet保证了pod在重新调度后保留它们的标识和状态。它让你方便的扩容、缩容。与ReplicaSet类似，StatefulSet也会指定期望副本数，它决定了在同一时间运行的宠物的数量。与ReplicaSet类似，pod也是根据StatefulSet的pod模板进行创建的。与ReplicaSet不同的是，StatefulSet创建的pod副本并不是完全一样的。每个pod都可以拥有一组独立的数据卷而有所区别。另外，宠物pod的名字都是有规律的，而不是每个新pod都随机获取一个名字。
## 2.2 提供稳定的网络标识

一个StatefulSet创建的每个pod都会有一个从零开始的顺序索引，**这个会体现在pod的名称和主机名上，同样还会体现在pod对应的固定存储上**。这些pod的名称是可以预支的，因为它是由StatefulSet的名称加该实例的顺序索引值组成的。不同于pod随机生成的一个名称，这样有规则的pod名称是很方便管理的。

**控制服务介绍**

让pod拥有可预知的名称和主机名并不是全部，与普通的pod不一样的是，有状态的pod有时候需要通过其主机名来定位，而无状态的pod则不需要，因为每个无状态的pod都是一样的，在有需要的时候随便选择一个即可。但对于有状态的pod来说，因为它们都是彼此不同的，通常希望操作的是其中特定的一个。

基于以上原因，一个StatefulSet通常要求你创建一个用来记录每个pod网络标记的headless Service。通过这个Service，每个pod都拥有独立的DNS记录，这样集群里它的伙伴或者客户端可以通过主机名方便的找到它。比如说在default命名空间中，有一个名为foo的服务，它的一个pod为a-0，那么可以通过`a-0.foo.default.svc.cluster.local`来访问这个pod，而这在ReplicaSet是不行的。

另外，也可以通过DNS服务，查找域名`foo.default.svc.cluster.local`对应的所有SVC记录，获取一个StatefulSet中所有的pod名称。这将在后面介绍。

**替换消失的宠物**

当一个StatefulSet管理的一个pod实例消失后(pod所在节点发生故障，或有人手动删除pod)，StatefulSet会保证重启一个新的pod实例替换它，这与ReplicaSet类似，但与ReplicaSet不同的是，新的pod会拥有与之前pod完全一致的名称和主机名。

新的pod不一定会调度到同一个节点，即使新的pod被调度到其他节点，也可以通过主机名来访问。主机名就是pod名称。

**扩缩容StatefulSet**

扩容一个StatefulSet会使用下一个还没用到的顺序索引值创建一个新的pod实例。当缩容一个StatefulSet时，比较好的是很明确哪个pod将要被删除，会先删除最高索引值的实例，所以缩容的结果是可预知的，但ReplicaSet不行。

因为有状态应用缩容在任何时候只会操作一个pod实例，所以有状态应用的缩容不会很迅速。比如说一个数据项副本设置为2的数据存储应用，若同时有两个节点下线，一份数据记录就会丢失，若缩容是线性的，则分布式存储应用就有时间吧丢失的副本复制到其他节点，保证数据不会丢失。

基于以上原因，StatefulSet在有实例不健康的情况下是不允许做缩容操作的。若一个实例是不健康的，而这时再缩容一个实例的话，也就意味着你实际上同时失去了两个集群成员。
## 2.3 为每个有状态实例提供稳定的专属存储

上面介绍了StatefulSet如何保证一个有状态的pod拥有稳定的标识，那存储呢？一个有状态的pod需要拥有自己的存储，即使该有状态的pod被重新调度。新的实例也必须挂载着相同的存储。

有状态的pod的存储必须是持久的，并且与pod解耦。可以在每个pod中关联不同的持久卷申领，就可以保证每个pod都使用不同的持久化存储，但所有的pod都是由一份pod模板创建出来的，它们是如何关联到不同的持久卷申领的呢，并且是有谁来创建这些持久卷的呢？

**在pod模板中添加卷申领模板**

可以把持久卷申领也交给StatefulSet创建，所以一个StatefulSet可以拥有一个或多个卷申领模板，这些持久卷申领会在创建pod前创建出来，绑定到一个pod实例上。

申领的持久卷可以通过用户自己手动创建出来，也可以使用持久卷动态配置来自动创建。

**持久卷的创建和删除**

扩容StatefulSet增加一个副本数时，会创建两个或更多的API对象(一个pod和与之关联的一个或多个持久卷申领)。但是对缩容来说，则只会删除一个pod，而遗留之前创建的申领，保存了这个pod上的数据，让你手动做决定该怎么处理这些数据。

因为有状态pod是用来运行有状态应用的，所以其在数据卷上存储的数据非常重要，在StatefulSet缩容时删除这个申领将是灾难性的。

**重新挂载持久卷申领到相同的pod新实例上**

因为缩容StatefulSet时会保留持久卷申领，所以在随后的扩容操作中，新的pod实例会使用绑定在持久卷上的相同申领和其上的数据。当你因为误操作而缩容一个StatefulSet后，可以做一次扩容来弥补自己的损失，新的pod实例会运行到与之前完全一致的状态。
## 2.4 StatefulSet的保障

通常来说，无状态的pod是可以替代的，而有状态pod则不行。我们之前已经描述了一个有状态的pod总是会被一个完全一致的pod替换(两者有相同的名称、主机名和存储等)。这个替换发生在Kubernetes发现旧的pod不存在时。

那么当Kubernetes不能确定一个pod的状态呢？如果它创建一个完全一致的pod，那么系统中就会 有两个完全一致的pod在同时运行。这两个pod会绑定同一个持久卷申领，所以这两个相同标记的进程会同时写相同的文件。对于ReplicaSet的pod来说，这不是问题，因为应用本来就是设计为在相同文件上工作的。并且ReplicaSet会以一个随机的标识来创建pod，所以不可能存在两个相同标识的进程同时运行。

**介绍StatefulSet的at-most-one语义**

Kubernetes必须保证两个拥有相同标记和绑定相同持久卷申领的有状态pod实例不会同时运行。一个StatefulSet必须保证有状态的pod实例的`at-most-one`语义。

也就是说一个StatefulSet必须在准确确认一个pod不再运行后，才会去创建它的替换pod。
# 3 使用StatefulSet

先把StatefulSet需要的三个pv创建出来，如果你的集群使用了StorageClass，也可以不创建。
```yaml
kind: List
apiVersion: v1
items:
- apiVersion: v1
  kind: PersistentVolume
  metadata:
    name: pv-a
  spec:
    capacity:
      storage: 1Mi
    accessModes:
      - ReadWriteOnce
    persistentVolumeReclaimPolicy: Recycle
    hostPath:
      path: /tmp/pv-a
- apiVersion: v1
  kind: PersistentVolume
  metadata:
    name: pv-b
  spec:
    capacity:
      storage: 1Mi
    accessModes:
      - ReadWriteOnce
    persistentVolumeReclaimPolicy: Recycle
    hostPath:
      path: /tmp/pv-b
- apiVersion: v1
  kind: PersistentVolume
  metadata:
    name: pv-c
  spec:
    capacity:
      storage: 1Mi
    accessModes:
      - ReadWriteOnce
    persistentVolumeReclaimPolicy: Recycle
    hostPath:
      path: /tmp/pv-c

```
Kubernetes中可以通过`---`来定义多个资源，也可以定义一个List对象，然后把各个资源作为 List对象的各个项目，这两个方法是等价的。

**创建Service**

还需要创建一个headless service，用于在有状态的pod之间提供网络标识。
```yaml
apiVersion: v1
kind: Service
metadata:
  name: kubia
spec:
  clusterIP: None
  selector:
    app: kubia
  ports:
  - name: http
    port: 80
```

**创建StatefulSet**

在创建好上面两个资源后，就可以创建StatefulSet了
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: kubia
spec:
  serviceName: kubia
  replicas: 2
  selector:
    matchLabels:
      app: kubia # has to match .spec.template.metadata.labels
  template:
    metadata:
      labels:
        app: kubia
    spec:
      containers:
      - name: kubia
        image: luksa/kubia-pet
        ports:
        - name: http
          containerPort: 8080
        volumeMounts:
        - name: data
          mountPath: /var/data
  volumeClaimTemplates:   # 持久卷申领模板
  - metadata:
      name: data
    spec:
      resources:
        requests:
          storage: 1Mi
      accessModes:
      - ReadWriteOnce
```
这个StatefulSet和之前创建的ReplicaSet和Deployment的声明文件并没有多大的区别，这里使用了一个`volumeClaimTemplates`卷申领模板，只定义了一个叫data的卷申领模板，StatefulSet会根据这个模板为每个pod都创建一个持久卷申领。

创建好StatefulSet之后，会发现StatefulSet只创建了一个pod，而我们声明文件中的期望副本数是两个pod，**这是为什么？这是StatefulSet创建pod是按顺序创建的，等第一个pod运行并处于就绪状态的时候，第二个pod就会开始创建了。** StatefulSet这样做是因为状态明确的集群应用对同时有两个集群成员启动引起的竞争情况是十分敏感的。所以依次启动每个成员是比较安全可靠的。

**与其他资源不同的是，删除一个StatefulSet，不能保证pod全部被删除，为了实现StatefulSet中的pod可以有序且体面的终止，可以在删除之前将StatefulSet缩容到0。**
> `--cascade` 选项用于指定删除资源时的级联删除策略：
> - `background`：默认策略，立即删除资源对象，依赖资源在后台异步删除。
> - `foreground`：先删除所有依赖资源，然后再删除资源对象，删除过程是同步的。
> - `orphan`：只删除资源对象，不删除其依赖资源，依赖资源将被孤立。
## 3.1 使用pod

现在数据存储集群的节点都已经运行，可以开始使用了。因为之前创建的service处于headless模式，所以不能通过这个服务来访问你的pod。需要连接单独的pod来访问。

**通过API服务器与pod通信**

API服务器的一个很有用的功能就是通过代理直接连接到指定pod。如果向请求当前的kubia-0的pod，可以使用这个URL进行访问`<apiserverHost>:<port>/v1/namespaces/default/pods/kubia-0/proxy/<path>`。因为api访问是加密的，所以通过API服务器发送请求到pod是很麻烦的。可以使用之前学习过的`kubectl proxy`方法。

# 4 在StatefulSet中发现伙伴节点

集群应用中一个很重要的点是伙伴节点能够彼此发现，这样才可以找到集群中的其他成员。一个StatefulSet中的成员需要很容器找到其他的所有成员。当然它可以通过与API服务器通信来获取，但Kubernetes的一个目标是设计功能来帮助应用完全感觉不到Kubernetes的存储。

那如何使得pod不通过API与其他伙伴通信呢？可以使用DNS来达到目的，使用SRV记录可以达到这个目的。

**介绍SRV记录**

SRV记录用来指向提供指定服务的服务器的主机名和端口号。Kubernetes通过一个headless service创建SRV记录来指向pod的主机名。

可以在一个临时的pod里运行DNS查询工具--dig命令，列出所有有状态pod的SRV记录，命令如下：
```
kubectl run -it srvlookup --image=dnsutils --rm --restart=Nerver -- dig SRV kubia.default.svc.cluster.local
```
上面这个容器创建了一个使用`dig SRV kubia.default.svc.cluster.local`命令的临时容器，这个命令会输出提供服务的pod的SRV记录，所以当一个pod想获取集群中其他pod列表时，需要做的就是触发一次SRV DNS查询。
>**注意：SRV记录顺序是随机的，不是按照pod名称进行排序的。**
## 4.1 更新StatefulSet

可以使用`edit`/`patch`命令来更新StatefulSet。
```bash
kubectl edit statefulset kubia
```
上面的命令会使用默认的编辑器打开StatefulSet的定义，在定义中修改StatefulSet的定义即可触发更新，如副本数和镜像之类的。

更新退出之后，就可以看到修改的内容已经开始被更新了。新创建的pod会使用更新的镜像，而老的pod则不会更新，这个因为StatefulSet的行为更像ReplicaSet，而不是Deployment。
> 从Kubernetes 1.7版本开始，StatefulSet支持与Deployment和DaemonSet一样的滚动升级。通过设置updateStrategy相关文档来获取更多信息。

## 4.2 StatefulSet如何处理节点失效

在前面我们知道Kubernetes必须完全保证，一个有状态pod在创建它的代替者之前已经不再运行，当一个节点突然失效，Kubernetes并不知道节点或者它上面pod的状态。它并不知道这些pod是否还在运行，或者它们是否还存在，甚至是否还能被客户端访问到，或者仅仅是kubelet停止向主节点上报节点状态。

因为一个StatefulSet要保证不会有两个拥有相同标记和存储的pod同时运行，当一个节点似乎失效后，StatefulSet在明确知道一个pod不再运行之前，它不能或者不应该创建一个替换pod。

**模拟一个网络断开**

可以在一个节点上使用以下命令来关闭网络接口
```bash
sudo ifconfig eth0 down
```
当关闭网络接口后，在控制节点上使用`kubectl get node`会观察到一个节点的状态变成了`NotReady`，在这个节点上运行的pod状态都变成了`Unknow`。

**当一个pod状态为Unknow时会发生什么**

若该节点过一段时间后，网络恢复正常，节点数据正常上报，那么pod的状态又会变成`Runing`。但如果这个pod的未知状态持续几分钟后(可以配置)，这个pod就会自动从节点上驱逐。这是由主节点处理的，它通过删除pod的资源来把它从节点上驱逐。

当kubelet发现这个pod被标记为删除状态后，它开始终止运行该pod。在 上面的节点中，因为kubelet已经不能与主节点通信，所以这个pod会一直运行。

**手动删除pod**

当你明确这个节点不会再回来，但是所有客户端请求的三个pod都必须是正常运行的。所以需要把kubia-0重新调度到一个健康的节点上。所以要手动删除这个pod。

当我们正常删除pod
```bash
kubectl delete po kubia-0
```
kubectl返回说这个pod已经被删除了，但在控制节点查看运行的pod时却发现旧的pod仍然存在。这是为什么？在删除pod之前，这个pod已经被标记为珊瑚了。这是因为控制组件已经删除了它(把它从节点驱逐)。如果在这是使用`kubectl describe po kubia-0`就会发现这个pod的状态为`Terminating`。这个pod之前已经被标记为删除，只要它节点上的kubelet通知API服务器说这个pod容器已经终止，那么它就会被清除掉。但是因为这个节点上的网络断开了，所以上述情况永远不会发生。

**强制删除pod**

现在要做的就是告诉ApiServer服务器不用等待kubelet来确定这个pod已经不再运行，而是直接删除它。
```bash
kubectl delete po kubia-0 --force --grace-period 0
```
这样就能把pod强制删除了，这是你就会发现一个新的pod被创建出来了。
## 4.3 驱逐策略

可以通过设置`kube-controller-manager`的`--pod-eviction-timeout`来设置驱逐时间，默认是5分钟。
```bash
kube-controller-manager --pod-eviction-timeout=5m
```

