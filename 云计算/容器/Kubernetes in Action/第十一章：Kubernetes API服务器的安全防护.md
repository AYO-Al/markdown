> 本章内容包括：
> - 了解认证机制
> - ServiceAccounts是什么及使用的原因
> - 了解基于角色(RBAC)的权限控制插件
> - 使用角色和角色绑定
> - 使用集群角色和集群角色绑定
> - 了解默认角色及其绑定
# 1 了解认证机制

在前面的内容中，我们说到API服务器可以配置一个到多个认证的插件(授权插件同样可以)。API服务器接收到的请求会经过一个认证插件的列表，列表中的每个插件都可以检查这个请求和尝试确定谁在发送这个请求。列表中的第一个插件可以提取请求中客户端的用户名、用户ID和组信息，并返回给API服务器。API服务器会停止调用剩余的认证插件并直接进入授权阶段。

目前有几个认证插件是直接可用的。它们使用以下方法获取客户端的身份认证：
- 客户端证书
- 传入在HTTP头重的认证token
- 基础的HTTP认证
- 其他
启动API服务器时，通过命令行选项可以开启认证插件。
## 1.1 用户和组

认证插件会返回已经认证过用户的用户名和用户组。kubernetes不会在任何地方存储这些信息，这些信息被用来验证用户是否被授权执行某个操作。

**了解用户**

kubernetes区分了两种连接到API服务器的客户端：
- 真实的人
- pod(pod中运行的应用)
这两类客户端都使用上述的认证插件进行认证。用户应该被管理在外部系统中，例如单点登录系统(SSO)，但是pod使用一种`service accounts`的机制，该机制被创建和存储在集群中作为`ServiceAccount`资源。没有资源代表用户账户，这也就意味着不能通过API服务器来创建、更新或删除用户。但可以通过RBAC（基于角色的访问控制）来管理用户的权限。

**了解组**

正常用户和serviceAccount都可以属于一个或多个组。我们已经将过认证插件会连同用户名和用户ID返回组。组可以一次给多个用户赋予权限，而不是必须单独给用户赋予权限。

由插件返回的组仅仅是表示组名称的字符串，但是系统内置的组会有一些特殊的含义。
- system:unauthenticated 组⽤于所有认证插件都不会认证客户端⾝份的请求
- system:authenticated 组会⾃动分配给⼀个成功通过认证的⽤户。
- system:serviceaccounts 组包含所有在系统中的ServiceAccount。
- system:serviceaccounts 组包含所有在系统中的ServiceAccount。
## 1.2 ServiceAccount介绍

现在已经了解到了API服务器要求客户端在服务器上执行操作之前对自己进行身份验证，了 解 了 是 怎 么 通 过 发 送pod/var/run/secrets/kubernetes.io/serviceaccount/token ⽂件内容来进⾏⾝份认证的。这个⽂件通过加密卷挂载进每个容器的⽂件系统中。

但是这个文件代表了什么呢？每个pod上都与一个ServiceAccount相关联，它代表了运行在pod中应用程序的身份证明。token文件持有ServiceAccount的认证token。

应用程序使用这个token连接API服务器时，身份认证插件会对ServiceAccount进行身份认证，并将ServiceAccount的用户名传回API服务器内部。ServiceAccount用户名格式像这样`system:serviceaccount:<namespace>:<service account name>`。

API服务器将这个用户名传给已配置好的授权插件，这决定该应用程序所尝试执行的操作是否被ServiceAccount允许执行。

ServiceAccount只不过是一种运行在pod中的应用程序和API服务器身份认证的一种方式。如前所述，应用程序通过在请求中传递ServiceAccount token来实现这一点。

**了解ServiceAccount资源**

ServiceAccount就像Pod、Secret、Configmap等一样都是资源，它们作用在单独的命名空间，为每个命名空间自动创建一个默认的ServiceAccount。可以像其他资源一样查看ServiceAccount
```bash
kubectl get sa
NAME      SECRETS   AGE
default   1         1d
```

当前命名空间只包含default ServiceAccount，其他额外的ServiceAccount可以在需要时添加。每个pod都与一个ServiceAccount相关联，但是多个pod可以使用相同的一个sa，且只能使用相同命名空间的sa。

**ServiceAccount如何和授权进行绑定**

在pod的manifest文件中，可以用指定账户名称的方式指定一个ServiceAccount。如果不显式的指定，pod会使用命名空间中默认的ServiceAccount。`spec.serviceAccountName: default`。

可以通过将不同的ServiceAccount赋值给pod来控制每个pod可以访问的资源。当API服务器接收到一个带有认证token的请求时，服务器会用这个token来验证发送请求的客户端所关联的Service Account是否允许执行请求的操作。API服务器通过管理员配置好的系统级别认证插件来获取这些信息。其中一个现成的授权插件是基于角色控制的插件(RBAC)。
## 1.3 创建ServiceAccount

我们已经知道了可以自定义ServiceAccount，但是为什么要自定义呢，使用默认的不就好了吗？其中一个显而易见的原因就是集群安全性。不需要读取任何集群元数据的pod应该运行在一个受限制的账户下，这个账户不允许它们检索或修改部署在集群中的任何资源。需要检索元数据的pod应该运行在只允许读取这些对象元数据的ServiceAccount下。反之，需要修改这些对象的pod应该在它们自己的ServiceAccount下运行，这些Service Account允许修改API对象。

下面让我们来看下如何使用ServiceAccount。
```bash
$ kubectl describe sa 
Name:                crc
Namespace:           default
Labels:              <none>
Annotations:         <none>
Image pull secrets:  crc-public  # 这些会被自动的添加到使用这个ServiceAccount的所有pod中
                     crc-vpc
Mountable secrets:   crc-token-pcg46 # 如果强制使用挂载在密钥，那么使用这个ServiceAccount的pod只能挂载这些密钥
Tokens:              crc-token-pcg46  # 认证token，第一个token挂载在容器内


$ kubectl describe secret crc
Name:         crc
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
当创建好ServiceAccount之后，查看token secret，会发现其中包含的东西与默认的secret是一致的，但内容肯定有所不同。ServiceAccount中使用额身份认证token使用的是`JWT token`（JSON Web Token）。

**了解ServiceAccount上的可挂载密钥**

通过`kubectl describe`命令查看ServiceAccount时，token会显示在可挂载列表中。在之前我们了解了如何创建密钥并且把它们挂载进一个pod里。在默认情况下，pod可以挂载任何它需要的密钥。但是我们通过对ServiceAccount进行配置，让pod只允许挂载ServiceAccount中列出的可挂载密钥。
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  annotations:
    kubernetes.io/enforce-mountable-secrets: "true"
  name: my-serviceaccount
  namespace: my-namespace
```

如 果 ServiceAccount 被 加 上 了 这 个 注 解 ， 任 何 使 ⽤这 个ServiceAccount的pod只能挂载进ServiceAccount的可挂载密钥——这些 pod不能使⽤其他的密钥。

**了解ServiceAccount的镜像拉取密钥**

Service也可以包含镜像拉取密钥的list。还记得在第六章时所使用的镜像拉取密钥吗？
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

ServiceAccount的镜像拉取密钥和它的可挂载密钥表现有些轻微不同。和可挂载密钥不同的是，ServiceAccount中的镜像拉取密钥不是⽤来确定⼀个pod可以使⽤哪些镜像拉取密钥的。添加到ServiceAccount中的镜像拉取密钥会⾃动添加到所有使⽤这个ServiceAccount的pod中。向ServiceAccount中添加镜像拉取密钥可以不必对每个pod都单独进⾏镜像拉取密钥的添加操作。

**请注意：如果没有设置RBAC授权插件的话，默认给了ServiceAccount全部的权限。**

如果集群没有使⽤合适的授权，创建和使⽤额外的ServiceAccount并没有多⼤意义，因为即使默认的ServiceAccount也允许执⾏任何操作。在这种情况下，使⽤ServiceAccount的唯⼀原因就是前⾯讲过的加强可挂载密钥，或者通过ServiceAccount提供镜像拉取密钥。如果使⽤RBAC授权插件，创建额外的ServiceAccount实际上是必要的，我们会在后⾯讨论RBAC授权插件的使⽤。
# 2 通过基于角色的权限控制加强集群安全

从1.6版本开始，集群安全性显著提高。在早期版本中，如果你设法从集群中的⼀个pod获得了⾝份认证token，就可以使⽤这个token在集群中执⾏任何你想要的操作。如果在⾕歌上搜索，可以找到演⽰如何使⽤ pathtraversal（或者directory traversal）攻击的例⼦（客户端可以检索位于We b服务器的We b根⽬录之外的⽂件）。通过这种⽅式可以获取token，并⽤这个token在不安全的 Kubernetes集群中运⾏恶意的pod。

但是在1.8版本中，RBAC授权插件升级为GA(通用可用性)，并且默认在集群上开启。RBAC会阻止未授权的用户查看和修改集群状态。除非授予默认的ServiceAccount额外的特权，否则默认的ServiceAccount不允许查看集群状态，更不用说以任何方式取修改集群状态。
> 注意 除了RBAC插件，Kubernetes也包含其他的授权插件，⽐如基于属性的访问控制插件（ABAC）、WebHook插件和⾃定义插件实现。但是，RBAC插件是标准的。

## 2.1 介绍RBAC授权插件

Kubernetes API服务器可以配置使用一个授权插件来检查是否允许用户请求的动作执行。因为API服务器对外暴露了REST接口，用户可以通过向服务器发送HTTP请求来执行动作，通过在请求汇总包含认证凭证来进行认证(认证token、用户名和密码或者客户端证书)。

**了解动作**

但是有什么动作？如你所了解的，REST客户端发送GET、POST、PUT、DELETE和其他类型的HTTP请求到特定的URL路径上，这些路径表⽰特定的REST资源。在Kubernetes中，这些资源是Pod、Service、Secret，等等。以下是Kubernetes请求动作的⼀些例⼦：
- 获取pod创建服务
- 创建服务
- 更新密钥

这些⽰例中的动词（get、create、update）映射到客户端请求的 HTTP⽅法（GET、POST、PUT）上。名词（Pod、Service、Secret）显然是映射到Kubernetes上的资源。

例如RBAC这样的授权插件运⾏在API服务器中，它会决定⼀个客户端是否允许在请求的资源上执⾏请求的动词。

| HTTP方法   | 单一资源动词           | 集合的动词            |
| -------- | ---------------- | ---------------- |
| GET、HEAD | get(以及watch用于监听) | list(以及watch)    |
| POST     | create           | n/a              |
| PUT      | uodate           | n/a              |
| PATCH    | patch            | n/a              |
| DELETE   | delete           | deletecollection |
除了可以对全部资源类型应⽤安全权限，RBAC规则还可以应⽤于特定的资源实例（例如，⼀个名为myservice的服务），并且后⾯你会看到权限也可以应⽤于non-resource（⾮资源）URL路径，因为并不是 API服务器对外暴露的每个路径都映射到⼀个资源（例如 /api路径本⾝或服务器健康信息在的路径/healthz）。

**了解RBAC插件**

顾名思义，RBAC授权插件将用户角色作为决定用户能否执行操作的关键因素。主体(一个人、一个Service或一组用户或ServiceAccount)和一个或多个角色相关联，每个角色被允许在特定的资源上执行特定的动词。

通过RBAC插件管理授权是简单的，这⼀切都是通过创建四种RBAC特定的Kubernetes资源来完成的，我们会在下⾯学习这个过程。
## 2.2 介绍RBAC资源

Role（⾓⾊）和ClusterRole（集群⾓⾊），它们指定了在资源上可以执⾏哪些动词。RoleBinding （ ⾓ ⾊ 绑 定 ） 和 ClusterRoleBinding （ 集群 ⾓ ⾊ 绑定），它们将上述⾓⾊绑定到特定的⽤户、组或ServiceAccounts上。⾓⾊定义了可以做什么操作，⽽绑定定义了谁可以做这些操作。
![](image/第十一章：Kubernetes%20API服务器的安全防护_time_1.png)

角色和集群角色，或者角色绑定和集群角色绑定之间的区别在于角色和角色绑定是命名空间的资源，而集群角色和集群角色绑定时集群级别的资源。

从图中可以看到，多个⾓⾊绑定可以存在于单个命名空间中（对于⾓⾊也是如此）。同样地，可以创建多个集群绑定和集群⾓⾊。图中显⽰的另外⼀件事情是，尽管⾓⾊绑定是在命名空间下的，但它们也可以引⽤不在命名空间下的集群⾓⾊，但不可用绑定其他命名空间下的角色。
![](image/第十一章：Kubernetes%20API服务器的安全防护_time_2.png)
可以在APIServer启动选项中使用`--authorization-mode=RBAC,Node`开启RABC及node授权插件，node授权插件专门为Kubernetes节点设计的授权机制，确保节点只能访问和修改与其自身相关的资源。
## 2.3 使用Role和RoleBinding

Role资源定义了哪些操作可以在哪些资源上执行。下⾯的代码清单定义了⼀个Role，它允许⽤户获取并列出foo命名空间中的服务。
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadate:
  namespace: foo
  name: service-reader
rules:
- apiGroups: [""]   # Service是核心apiGroup的资源，所有没有apiGroup名
  verbs: ["get","list"]  # 获取独立的Service并且列出所有允许的服务
  resources: ["services"] # 这条规则和服务有关，必须使用复数形式
```
这个Role资源会在foo命名空间中创建出来。在第8章中，你了解到每个资源类型属于⼀个API组，在资源清单（manifest）的apiVersion字段中指定API组（以及版本）。在⾓⾊定义中，需要为定义包含的每个规则涉及的资源指定apiGroup。如果你允许访问属于不同API组的资源，可以使⽤多种规则。

**绑定角色到ServiceAccount**

⾓⾊定义了哪些操作可以执⾏，但没有指定谁可以执⾏这些操作。要做到这⼀点，必须将⾓⾊绑定⼀个到主体，它可以是⼀个 user（⽤户）、⼀个ServiceAccount或⼀个组（⽤户或ServiceAccount的组）。
```yaml
apiVersion: rbac.authorization.k8s.io/v1 
kind: RoleBinding 
metadata: 
  name: read-nodes 
roleRef: 
  apiGroup: rbac.authorization.k8s.io 
  kind: ClusterRole 
  name: service-reader
  subjects: 
  - kind: ServiceAccount 
    name: my-service-account n
    amespace: default
  - kind: ServiceAccount 
    name: sa2 
    namespace: default
```
## 2.4 使用ClusterRole和ClusterRoleBinding

除了这些命名空间⾥的资源，还存在两个集群级别的RBAC资源：ClusterRole和ClusterRoleBinding，它们不在命名空间⾥。让我们看看为什么需要它们。

⼀个常规的⾓⾊只允许访问和⾓⾊在同⼀命名空间中的资源。如果你希望允许跨不同命名空间访问资源，就必须要在每个命名空间中创建⼀个Role和RoleBinding。如果你想将这种⾏为扩展到所有的命名空间（集群管理员可能需要），需要在每个命名空间中创建相同的 Role和RoleBinding。当创建⼀个新的命名空间时，必须记住也要在新的命名空间中创建这两个资源。

正如前面所了解到的，一些特定的资源完全不在命名空间中。API服务器也会对外暴露一些不表示资源的URL路径(例如/healthz)。常规角色不能对这些资源或非资源型URL进行授权，但是ClusterRole可以。

ClusterRole是⼀种集群级资源，它允许访问没有命名空间的资源和⾮资源型的URL，或者作为单个命名空间内部绑定的公共⾓⾊，从⽽避免必须在每个命名空间中重新定义相同的⾓⾊。

**允许访问集群级别的资源**

可以使⽤ClusterRole来允许集群级别的资源访问。让我们来了解⼀下如何允许pod列出集群中的PersistentVolume。
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadate:
  name: service-reader
rules:
- apiGroups: [""]   
  verbs: ["get","list"]  
  resources: ["persistentvolumes"] 
```
需要将ClusterRole绑定到ServiceAccount来允许它这样做。ClusterRole可以通过常规的RoleBinding（⾓⾊绑定）来和主体绑定，但绑定后不能访问非命名空间资源。尽管你可以创建⼀个RoleBinding并在你想开启命名空间资源的访问时引⽤⼀个ClusterRole，但是不能对集群级别（没有命名空间的）资源使⽤相同的⽅法。必须始终使⽤ClusterRoleBinding来对集群级别的资源进⾏授权访问。
```yaml
apiVersion: rbac.authorization.k8s.io/v1 
kind: ClusterRoleBinding 
metadata: 
  name: read-nodes 
roleRef: 
  apiGroup: rbac.authorization.k8s.io 
  kind: ClusterRole 
  name: service-reader
  subjects: 
  - kind: ServiceAccount 
    name: my-service-account 
    amespace: foo
```
![](image/第十一章：Kubernetes%20API服务器的安全防护_time_3.png)
> **记住⼀个RoleBinding不能授予集群级别的资源访问权限，即使它引⽤了⼀个ClusterRoleBinding。**

**允许访问非资源型URL**

我们已经提过，API服务器也会对外暴露⾮资源型的URL。访问这些URL也必须要显式地授予权限；否则，API服务器会拒绝客户端的请求 。 通 常 ， 这 个 会 通 过 system:discoveryClusterRole 和 相 同 命 名 的ClusterRoleBinding帮你⾃动完成，它出现在其他预定义的ClusterRoles和ClusterRoleBindings中
```yaml
$ kubectl get clusterrole system:discovery -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  name: system:discovery
rules:
- nonResourceURLs:   # 指向非资源型URL为不是资源
  - /api
  - /api/*
  - /apis
  - /apis/*
  - /healthz
  - /livez
  - /openapi
  - /openapi/*
  - /readyz
  - /version
  - /version/
  verbs:
  - get
```
> **对于⾮资源型URL，使⽤普通的HTTP动词，如post、put和 patch，⽽不是create或update。动词需要使⽤⼩写的形式指定。**

同样有一个ClusterRoleBinding绑定ClusterRole
```yaml
root:~$ kubectl get clusterrolebinding system:discovery -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  name: system:discovery
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:discovery
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: system:authenticated   # 绑定到认证用户，说明认证过后的用户都能访问
```
## 2.5 使用ClusterRole来授权访问指定命名空间中的资源

ClusterRole不是必须⼀直和集群级别的ClusterRoleBinding捆绑使⽤。它们也可以和常规的有命名空间的RoleBinding进⾏捆绑。
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadate:
  name: service-reader
rules:
- apiGroups: [""]   
  verbs: ["get","list"]  
  resources: ["persistentvolumes"] 
```
这个集群角色能做什么，这取决于它是和ClusterRoleBinding还是和RoleBinding绑定（可以和其中的⼀个进⾏绑定）。如果你创建了⼀个ClusterRoleBinding并在它⾥⾯引⽤了ClusterRole，在绑定中列出的主体可以在所有命名空间中查看指定的资源。相反，如果你创建的是⼀个RoleBinding，那么在绑定中列出的主体只能查看在RoleBinding命名空间中的资源。

**使用ClusterRoleBinding**
![](image/第十一章：Kubernetes%20API服务器的安全防护_time_4.png)

**使用RoleBinding**
![](image/第十一章：Kubernetes%20API服务器的安全防护_time_5.png)
## 2.6 总结Role、ClusterRole、Rolebinding和ClusterRoleBinding的组合

我们已经介绍了许多不同的组合，可能很难记住何时去使⽤对应的每个组合。下面这张图可能会帮助你更好的记忆。
![](image/第十一章：Kubernetes%20API服务器的安全防护_time_6.png)

## 2.7 了解默认的ClusterRole和ClusterRoleBinding

Kubernetes提供了⼀组默认的ClusterRole和ClusterRoleBinding，每次API服务器启动时都会更新它们。这保证了在你错误地删除⾓⾊和绑定，或者Kubernetes的新版本使⽤了不同的集群⾓⾊和绑定配置时，所有的默认⾓⾊和绑定都会被重新创建。
![](image/第十一章：Kubernetes%20API服务器的安全防护_time_7.png)
view、edit、admin和cluster-admin ClusterRole是最重要的⾓⾊，它们应该绑定到⽤户定义pod中的ServiceAccount上。

**⽤view ClusterRole允许对资源的只读访问**

默认的view ClusterRole，它允许读取⼀个命名空间中的⼤多数资源，除了Role、RoleBinding和 Secret。你可能会想为什么Secrets不能被读取？因为Secrets中的某⼀个可能包含⼀个认证token，它⽐定义在view ClusterRole中的资源有更⼤的权限，并且允许⽤户伪装成不同的⽤户来获取额外的权限（权限扩散）。

**⽤edit ClusterRole允许对资源的修改**

edit ClusterRole，它允许你修改⼀个命名空间中的资源，同时允许读取和修改Secret。但是，它也不允许查看或修改Role和RoleBinding，这是为了防⽌权限扩散。

**⽤admin ClusterRole赋予⼀个命名空间全部的控制权**

⼀个命名空间中的资源的完全控制权是由admin ClusterRole赋予的。有这个ClusterRole的主体可以读取和修改命名空间中的任何资源，除了ResourceQuota和命名空间资源本⾝。edit和admin ClusterRole之间的主要区别是能否在命名空间中查看和修改Role和RoleBinding。
> **注意 为了防⽌权限扩散，API服务器只允许⽤户在已经拥有⼀个⾓⾊中列出的所有权限（以及相同范围内的所有权限）的情况下，创建和更新这个⾓⾊。**

**⽤cluster-admin ClusterRole得到完全的控制**

通 过 将 cluster-admin ClusterRole 赋 给 主 体 ， 主 体 可以 获 得Kubernetes集群完全控制的权限。正如你前⾯了解那样，adminClusterRole不允许⽤户修改命名空间的ResourceQuota对象或者命名空间资源本⾝。如果你想允许⽤户这样做，需要创建⼀个指向cluster-admin ClusterRole的RoleBinding。这使得RoleBinding中包含的⽤户能够完全控制创建RoleBinding所在命名空间上的所有⽅⾯。

如何授予⽤户⼀个集群中所有命名 空 间 的 完 全 控 制 权 。 就 是 通 过 在ClusterRoleBinding ⽽ 不 是RoleBinding中引⽤clusteradmin ClusterRole。

**了解其他默认的ClusterRole**

默认的ClusterRole列表包含了⼤量其他的ClusterRole，它们以 system：为前缀。这些⾓⾊⽤于各种Kubernetes组件中。在它们之中，可以找到如system:kube-scheduler之类的⾓⾊，它明显是给调度器使⽤的，system:node是给Kubelets组件使⽤的，等等。

虽然Controller Manager作为⼀个独⽴的pod来运⾏，但是在其中运⾏的每个控制器都可以使⽤单独的ClusterRole和ClusterRoleBinding（它们以system：Controller：为前缀）。

这些系统的每个ClusterRole都有⼀个匹配的ClusterRoleBinding，它会 绑 定 到 系 统 组 件 ⽤ 来 ⾝ 份认 证 的 ⽤ 户 上 。 例 如 ， system:kube-schedulerClusterRoleBinding 将 名 称 相 同 的 ClusterRole 分 配 给system:kube-scheduler⽤户，它是调度器作为⾝份认证的⽤户名。
## 2.8 理性地授予授权权限

在默认情况下，命名空间中的默认ServiceAccount除了未经⾝份验证 的 ⽤ 户 没 有 其 他 权 限 （ 你 可 能 记 得 前 ⾯ 的⽰ 例 之 ⼀ ，system:discovery ClusterRole和相关联的绑定 允许任何⼈对⼀些⾮资源型的URL发送GET请求）。因此，在默认情况下，pod甚⾄不能查看集群状态。应该授予它们适当的权限来做这些操作。

显然，将所有的ServiceAccounts赋予cluster-adminClusterRole是⼀个坏主意。和安全问题⼀样，我们最好只给每个⼈提供他们⼯作所需要的权限，⼀个单独权限也不能多（最⼩权限原则）。

**为每个pod创建特定的ServiceAccoun**

⼀个好的想法是为每⼀个pod（或⼀组pod的副本）创建⼀个特定ServiceAccount，并且把它和⼀个定制的Role（或ClusterRole）通过RoleBinding联系起来（不是ClusterRoleBinding，因为这样做会给其他命名空间的pod对资源的访问权限，这可能不是你想要的）。

如果你的⼀个pod（应⽤程序在它内部运⾏）只需要读取pod，⽽其他的pod也需要修改它们，然后创建两个不同的ServiceAccount，并且让这些pod通过指定在pod spec中的serviceAccountName属性来进⾏使⽤，和你在本章的第⼀部分了解的那样。不要将这两个pod所需的所有必要权限添加到命名空间中的默认ServiceAccount上。