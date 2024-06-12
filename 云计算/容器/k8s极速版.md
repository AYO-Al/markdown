# 1.有了Docker，为什么还用Kubernetes

![image-20230713142558515](./image/nl57nx-0.png)

![image-20230713142907273](./image/nmufjg-0.png)

![image-20230713143212070](./image/noo3ml-0.png)

![image-20230713143617652](./image/nr4zoa-0.png)

![image-20230713202023666](./image/xeysqf-0.png)

![image-20230713202458707](./image/xhe1no-0.png)

![image-20230703085312752](./image/e3zkwd-0.png)

![image-20230703091911708](./image/f7akbb-0.png)

![image-20230703093112688](./image/fefz0u-0.png)

![image-20230703143702589](./image/nrn37k-0.png)

![image-20230703143958984](./image/nt3ls3-0.png)

![image-20230713144251352](./image/nuubll-0.png)



# 2.环境准备三台主机

```bash
# 1.设置主机名和时区
timedatectl set-timezone Asia/Shanghai
hostnamectl set-hostname master # master
hostnamectl set-hostname node1  # node1
hostnamectl set-hostname node2  # node2


# 配置hosts网络配置
vim /etc/hosts
192.168.19.137 master
192.168.19.138 node1
192.168.19.139 node2

# 关闭防火墙
[root@k8s-master ~]# systemctl stop firewalld
[root@k8s-master ~]# systemctl disable firewalld
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

# 安装docker
# step 1: 安装必要的一些系统工具
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
# Step 2: 添加软件源信息
sudo yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
# Step 3
sudo sed -i 's+download.docker.com+mirrors.aliyun.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo
# Step 4: 更新并安装Docker-CE
sudo yum makecache fast
sudo yum -y install docker-ce
# Step 4: 开启Docker服务
sudo service docker start


# 安装kubeadm
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
setenforce 0
yum install -y kubelet kubeadm kubectl
systemctl enable kubelet && systemctl start kubelet

# 关闭交换分区
swapoff -a
vim /etc/fstab
# swap一行注释

# 配置网桥
cat > /etc/sysctl.d/k8s.conf <<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sysctl --system

```



# 3.安装kubuadm

```bash
kubeadm join 192.168.19.137:6443 --token flknyj.dykek2mbjndszk2t \
    --discovery-token-ca-cert-hash sha256:b1ae30f0862edb021ff77901b05c95d2d8914bd5439e7871a1f7148599312b47 
```



![image-20230703144645930](./image/nx6x3t-0.png)

![image-20230713163930774](./image/r40gvn-0.png)



# 4.快速部署一个网站

![image-20230713192301992](./image/vszddr-0.png)

![image-20230713192444792](./image/vtrjft-0.png)

![image-20230713193143839](./image/w4xnlq-0.png)

![image-20230713193340918](./image/vz646w-0.png)

![image-20230713194220937](./image/w4erlo-0.png)

![image-20230713194656909](./image/w783r9-0.png)

```bash
kubectl apply -f deployment.yaml
```

![image-20230713195815304](./image/wduhjn-0.png)



# 5.Deployment

![image-20230713204132465](./image/xrfpzd-0.png)

![image-20230713204221801](./image/xrvz9d-0.png)

![image-20230713204420639](./image/xt3ru4-0.png)

![image-20230713204615894](./image/xuahm6-0.png)

```bash
# 发布
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.16
        ports:
        - containerPort: 80

---
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort
```

```
# 升级
# 修改文件中的镜像
spec:
      containers:
      - name: nginx
        image: nginx
        
# 查看升级过程
kubectl describe deployment web
```

![image-20230713210654495](./image/yu6pls-0.png)

```bash
# 记录更新记录，在更新命令上加
--record=ture # 只能记录更新命令
```

![image-20230713211755831](./image/z104sa-0.png)

![image-20230713212435768](./image/z4sjm7-0.png)

```bash
# 可以直接使用文件
kubectl delete -f deployment.yaml
```



# 6.Pod

![image-20230713212915572](./image/z7nu6c-0.png)

![image-20230713213038072](./image/z8dyuf-0.png)

![](./image/zihm5v-0.png)

> Pod中使用Pause镜像启动Infra container，用来给pod中的容器提供共享卷和网络等功能

![image-20230713215539988](./image/znabg5-0.png)

![image-20230714145055860](./image/nzz3y5-0.png)

# 7.Service

![image-20230713220408974](./image/10gai43-0.png)

![image-20230713221708296](./image/10o07in-0.png)

```bash
# 把service导出为yaml格式
kubectl get service kubernetes -o yaml

# 找到selector中的app
# 查找service绑定的pods
kubectl getpods -l app=pvc
```

![image-20230713222302536](./image/10rjo8w-0.png)

```bash
# 查看pod的标签
kubectl get pods --show-labels

apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort
```

![image-20230714090155282](./image/ex4449-0.png)

![image-20230714090300202](./image/exms3k-0.png)

![image-20230714091108036](./image/f2ivz8-0.png)

![image-20230714092154235](./image/f8zhwi-0.png)

# 8.Ingress

![image-20230714092834464](./image/fcpu9r-0.png)

![image-20230714093107588](./image/fecwto-0.png)

![image-20230714093144381](./image/fekonm-0.png)

![image-20230714093326021](./image/ffq509-0.png)



# 9.实战

![image-20230714110828169](./image/ibxjv0-0.png)