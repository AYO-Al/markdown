# 什么是redis-trib.rb?

redis-trib.rb是Redis官方提供的Redis Cluster的管理工具，无序额外下载。但是由于该工具用ruby开发，所有需要配置ruby环境



# 准备运行环境

```bash
yum install -y ruby

wget http://rubygems.org/downloads/redis-3.3.0.gem
gem install -l redis-3.3.0.gem
gem list --check redis gem

cp ${REDIS_HOME}/src/redis-trib.rb /usr/local/bin

```



# Redis-trib.rb命令

```bash
# redis-trib.rb help
Usage: redis-trib <command> <options> <arguments ...>

  create          host1:port1 ... hostN:portN
                  --replicas <arg>
  check           host:port
  info            host:port
  fix             host:port
                  --timeout <arg>
  reshard         host:port
                  --from <arg>
                  --to <arg>
                  --slots <arg>
                  --yes
                  --timeout <arg>
                  --pipeline <arg>
  rebalance       host:port
                  --weight <arg>
                  --auto-weights
                  --use-empty-masters
                  --timeout <arg>
                  --simulate
                  --pipeline <arg>
                  --threshold <arg>
  add-node        new_host:new_port existing_host:existing_port
                  --slave
                  --master-id <arg>
  del-node        host:port node_id
  set-timeout     host:port milliseconds
  call            host:port command arg arg .. arg
  import          host:port
                  --from <arg>
                  --copy
                  --replace
  help            (show this help)

For check, fix, reshard, del-node, set-timeout you can specify the host and port of any working node in the cluster.
```

支持的操作如下：

1. create：创建集群

2. check：检查集群

3. info：查看集群信息

 4. fix：修复集群

 5. reshard：在线迁移slot

 6. rebalance：平衡集群节点slot数量

 7. add-node：添加新节点

 8. del-node：删除节点

 9. set-timeout：设置节点的超时时间

 10. call：在集群所有节点上执行命令

 11. import：将外部redis数据导入集群



# 创建集群

```bash
redis-trib.rb create --replicas 1 127.0.0.1:6379 127.0.0.1:6380 127.0.0.1:6381 127.0.0.1:6382 127.0.0.1:6383 127.0.0.1:6384
# --replicas参数指定集群中每个主节点配备几个从节点，这里设置为1。
```

```bash
>>> Creating cluster
/usr/local/ruby/lib/ruby/gems/2.5.0/gems/redis-3.3.0/lib/redis/client.rb:459: warning: constant ::Fixnum is deprecated
>>> Performing hash slots allocation on 6 nodes...
Using 3 masters:
127.0.0.1:6379
127.0.0.1:6380
127.0.0.1:6381
Adding replica 127.0.0.1:6383 to 127.0.0.1:6379
Adding replica 127.0.0.1:6384 to 127.0.0.1:6380
Adding replica 127.0.0.1:6382 to 127.0.0.1:6381
>>> Trying to optimize slaves allocation for anti-affinity
[WARNING] Some slaves are in the same host as their master
M: bc775f9c4dea40820b82c9451778b1fcd42f92bc 127.0.0.1:6379
   slots:0-5460 (5461 slots) master
M: 3b27d00d13706a032a92ff6b0a914af272dcaaf2 127.0.0.1:6380
   slots:5461-10922 (5462 slots) master
M: d874f003257f1fb036bbd856ca605172a1741232 127.0.0.1:6381
   slots:10923-16383 (5461 slots) master
S: 648eb314863b82aaa676380be7db2ec307f5547d 127.0.0.1:6382
   replicates bc775f9c4dea40820b82c9451778b1fcd42f92bc
S: 65a6efb441ac44c348f7da8c62e26b888cda7c48 127.0.0.1:6383
   replicates 3b27d00d13706a032a92ff6b0a914af272dcaaf2
S: 57bda956485109552547aef6c77fba43d2124abf 127.0.0.1:6384
   replicates d874f003257f1fb036bbd856ca605172a1741232
Can I set the above configuration? (type 'yes' to accept): yes
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join...
>>> Performing Cluster Check (using node 127.0.0.1:6379)
M: bc775f9c4dea40820b82c9451778b1fcd42f92bc 127.0.0.1:6379
   slots:0-5460 (5461 slots) master
   1 additional replica(s)
S: 648eb314863b82aaa676380be7db2ec307f5547d 127.0.0.1:6382
   slots: (0 slots) slave
   replicates bc775f9c4dea40820b82c9451778b1fcd42f92bc
M: 3b27d00d13706a032a92ff6b0a914af272dcaaf2 127.0.0.1:6380
   slots:5461-10922 (5462 slots) master
   1 additional replica(s)
S: 57bda956485109552547aef6c77fba43d2124abf 127.0.0.1:6384
   slots: (0 slots) slave
   replicates d874f003257f1fb036bbd856ca605172a1741232
S: 65a6efb441ac44c348f7da8c62e26b888cda7c48 127.0.0.1:6383
   slots: (0 slots) slave
   replicates 3b27d00d13706a032a92ff6b0a914af272dcaaf2
M: d874f003257f1fb036bbd856ca605172a1741232 127.0.0.1:6381
   slots:10923-16383 (5461 slots) master
   1 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```

**注意：给redis-trib.rb的节点地址必须是不包含任何槽/数据的节点，否则会拒绝创建集群。**

关于主从节点的选择及槽的分配，其算法如下：

1> 把节点按照host分类，这样保证master节点能分配到更多的主机中。

2> 遍历host列表，从每个host列表中弹出一个节点，放入interleaved数组。直到所有的节点都弹出为止。

3> 将interleaved数组中前master个数量的节点保存到masters数组中。

4> 计算每个master节点负责的slot数量，16384除以master数量取整，这里记为N。

5> 遍历masters数组，每个master分配N个slot，最后一个master，分配剩下的slot。

6> 接下来为master分配slave，分配算法会尽量保证master和slave节点不在同一台主机上。对于分配完指定slave数量的节点，还有多余的节点，也会为这些节点寻找master。分配算法会遍历两次masters数组。

7> 第一次遍历master数组，在余下的节点列表找到replicas数量个slave。每个slave为第一个和master节点host不一样的节点，如果没有不一样的节点，则直接取出余下列表的第一个节点。

8> 第二次遍历是分配节点数除以replicas不为整数而多出的一部分节点。

 

# 检查集群状态

```bash
redis-trib.rb check 127.0.0.1:6379
```



# 查看集群信息

```bash
redis-trib.rb info 127.0.0.1:6383
```

```bash
/usr/local/ruby/lib/ruby/gems/2.5.0/gems/redis-3.3.0/lib/redis/client.rb:459: warning: constant ::Fixnum is deprecated
127.0.0.1:6380 (3b27d00d...) -> 0 keys | 5462 slots | 1 slaves.
127.0.0.1:6381 (d874f003...) -> 1 keys | 5461 slots | 1 slaves.
127.0.0.1:6379 (bc775f9c...) -> 0 keys | 5461 slots | 1 slaves.
[OK] 1 keys in 3 masters.
0.00 keys per slot on average.
```



# 修复集群

目前fix命令能修复两种异常，

 1. 节点中存在处于迁移中（importing或migrating状态）的slot。

 2. 节点中存在未分配的slot。

其它异常不能通过fix命令修复。

```bash
[root@slowtech conf]# redis-trib.rb fix 127.0.0.1:6379
/usr/local/ruby/lib/ruby/gems/2.5.0/gems/redis-3.3.0/lib/redis/client.rb:459: warning: constant ::Fixnum is deprecated
>>> Performing Cluster Check (using node 127.0.0.1:6379)
S: d826c5fd98efa8a17a880e9a90a25f06c88e6ae9 127.0.0.1:6379
   slots: (0 slots) slave
   replicates a8b3d0f9b12d63dab3b7337d602245d96dd55844
S: 55c05d5b0dfea0d52f88548717ddf24975268de6 127.0.0.1:6383
   slots: (0 slots) slave
   replicates a8b3d0f9b12d63dab3b7337d602245d96dd55844
M: f413fb7e6460308b17cdb71442798e1341b56cbc 127.0.0.1:6381
   slots:50-16383 (16334 slots) master
   2 additional replica(s)
S: beba753c5a63607fa66d9ec7427ed9a511ea136e 127.0.0.1:6382
   slots: (0 slots) slave
   replicates f413fb7e6460308b17cdb71442798e1341b56cbc
S: 83797d518e56c235272402611477f576973e9d34 127.0.0.1:6384
   slots: (0 slots) slave
   replicates f413fb7e6460308b17cdb71442798e1341b56cbc
M: a8b3d0f9b12d63dab3b7337d602245d96dd55844 127.0.0.1:6380
   slots:0-49 (50 slots) master
   2 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```



# 迁移数据与槽

```bash
redis-trib.rb reshard 127.0.0.1:6379
# 指定任意一个节点即可
```

```bash
/usr/local/ruby/lib/ruby/gems/2.5.0/gems/redis-3.3.0/lib/redis/client.rb:459: warning: constant ::Fixnum is deprecated
>>> Performing Cluster Check (using node 127.0.0.1:6379)
M: bc775f9c4dea40820b82c9451778b1fcd42f92bc 127.0.0.1:6379
   slots:3225-5460 (2236 slots) master
   1 additional replica(s)
S: 648eb314863b82aaa676380be7db2ec307f5547d 127.0.0.1:6382
   slots: (0 slots) slave
   replicates bc775f9c4dea40820b82c9451778b1fcd42f92bc
M: 3b27d00d13706a032a92ff6b0a914af272dcaaf2 127.0.0.1:6380
   slots:0-3224,5461-13958 (11723 slots) master
   1 additional replica(s)
S: 57bda956485109552547aef6c77fba43d2124abf 127.0.0.1:6384
   slots: (0 slots) slave
   replicates d874f003257f1fb036bbd856ca605172a1741232
S: 65a6efb441ac44c348f7da8c62e26b888cda7c48 127.0.0.1:6383
   slots: (0 slots) slave
   replicates 3b27d00d13706a032a92ff6b0a914af272dcaaf2
M: d874f003257f1fb036bbd856ca605172a1741232 127.0.0.1:6381
   slots:13959-16383 (2425 slots) master
   1 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
How many slots do you want to move (from 1 to 16384)? 200
What is the receiving node ID? 3b27d00d13706a032a92ff6b0a914af272dcaaf2
Please enter all the source node IDs.
  Type 'all' to use all the nodes as source nodes for the hash slots.
  Type 'done' once you entered all the source nodes IDs.
Source node #1:
```

它首先会提示需要迁移多个槽，我这里写的是200。

接着它会提示需要将槽迁移到哪个节点，这里必须写节点ID。

紧跟着它会提示槽从哪些节点中迁出。

如果指定为all，则待迁移的槽在剩余节点中平均分配，在这里，127.0.0.1:6379和127.0.0.1:6381各迁移100个槽出来。

也可从指定节点中迁出，这个时候，必须指定源节点的节点ID，最后以done结束

也可以直接使用

```bash
redis-trib.rb reshard host:port --from <arg> --to <arg> --slots <arg> --yes --timeout <arg> --pipeline <arg>
```

- host:port：必传参数，集群内任意节点地址，用来获取整个集群信息。

- --from：源节点id，如果有多个源节点，使用逗号分隔，如果是all，则源节点为集群内出目标节点外的其它所有主节点。

- --to：目标节点id，只能填写一个。

- --slots：需要迁移槽的总数量。

- --yes：迁移无需用户手动确认。

- --timeout：控制每次migrate操作的超时时间，默认为60000毫秒。

- --pipeline：控制每次批量迁移键的数量，默认为10。



# 平衡集群节点槽数量

```bash
rebalance       host:port
                  --weight <arg>
                  --auto-weights
                  --use-empty-masters
                  --timeout <arg>
                  --simulate
                  --pipeline <arg>
                  --threshold <arg>
```

- --weight <arg>：节点的权重，格式为node_id=weight，如果需要为多个节点分配权重的话，需要添加多个--weight <arg>参数，即--weight b31e3a2e=5 --weight 60b8e3a1=5，node_id可为节点名称的前缀，只要保证前缀位数能唯一区分该节点即可。没有传递–weight的节点的权重默认为1。

- --auto-weights：自动将每个节点的权重默认为1。如果--weight和--auto-weights同时指定，则--auto-weights会覆盖前者。

- --threshold <arg>：只有节点需要迁移的slot阈值超过threshold，才会执行rebalance操作。

- --use-empty-masters：默认没有分配slot节点的master是不参与rebalance的。如果要让其参与rebalance，需添加该参数。

- --timeout <arg>：设置migrate命令的超时时间。

- --simulate：设置该参数，只会提示用户会迁移哪些slots，而不会执行真正的迁移操作。

- --pipeline <arg>：定义cluster getkeysinslot命令一次取出的key数量，不传的话使用默认值为10。

```bash
# redis-trib.rb rebalance --weight a8b3d0f9b12d63dab3b7337d602245d96dd55844=3 --weight f413fb7e6460308b17cdb71442798e1341b56cbc=2  --use-empty-masters  127.0.0.1:6379
/usr/local/ruby/lib/ruby/gems/2.5.0/gems/redis-3.3.0/lib/redis/client.rb:459: warning: constant ::Fixnum is deprecated
>>> Performing Cluster Check (using node 127.0.0.1:6379)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
>>> Rebalancing across 2 nodes. Total weight = 5.0
Moving 3824 slots from 127.0.0.1:6380 to 127.0.0.1:6381
#########################################...
```



# 删除节点

```bash
redis-trib.rb del-node host:port node_id
```

在删除节点之前，其对应的槽必须为空，所以，在进行节点删除动作之前，必须使用redis-trib.rb reshard将其迁移出去。

需要注意的是，如果某个节点的槽被完全迁移出去，其对应的slave也会随着更新，指向迁移的目标节点。



# 添加新节点

```bash
redis-trib add-node new_host:new_port existing_host:existing_port --slave --master-id <arg>
```

new_host:new_port：待添加的节点，必须确保其为空或不在其它集群中。否则，会报错

所以，线上建议使用redis-trib.rb添加新节点，因为其会对新节点的状态进行检查。如果手动使用cluster meet命令加入已经存在于其它集群的节点，会造成被加入节点的集群合并到现有集群的情况，从而造成数据丢失和错乱，后果非常严重，线上谨慎操作。

existing_host:existing_port：集群中任意一个节点的地址。

如果添加的是主节点，只需指定源节点和目标节点的地址即可。

```bash
redis-trib.rb add-node 127.0.0.1:6379 127.0.0.1:6384
```

如果是从节点

```bash
redis-trib.rb add-node --slave --master-id f413fb7e6460308b17cdb71442798e1341b56cbc 127.0.0.1:6379 127.0.0.1:6384
```

注意：--slave和--master-id必须写在前面，同样的参数，如果是下面这样写法，会提示错误，

```
# redis-trib.rb add-node 127.0.0.1:6379 127.0.0.1:6384 --slave --master-id f413fb7e6460308b17cdb71442798e1341b56cbc
[ERR] Wrong number of arguments for specified sub command
```



# 设置节点的超时时间

```bash
redis-trib.rb set-timeout host:port milliseconds
```

其实就是批量修改集群各节点的cluster-node-timeout参数。

```bash
# redis-trib.rb set-timeout 127.0.0.1:6379 20000
/usr/local/ruby/lib/ruby/gems/2.5.0/gems/redis-3.3.0/lib/redis/client.rb:459: warning: constant ::Fixnum is deprecated
>>> Reconfiguring node timeout in every cluster node...
*** New timeout set for 127.0.0.1:6379
*** New timeout set for 127.0.0.1:6383
*** New timeout set for 127.0.0.1:6381
*** New timeout set for 127.0.0.1:6382
*** New timeout set for 127.0.0.1:6384
*** New timeout set for 127.0.0.1:6380
>>> New node timeout set. 6 OK, 0 ERR.
```



# 在集群所有节点上执行命令

```bash
redis-trib.rb call host:port command arg arg .. arg
```

```bash
[root@slowtech conf]# redis-trib.rb call 127.0.0.1:6379 set hello world
/usr/local/ruby/lib/ruby/gems/2.5.0/gems/redis-3.3.0/lib/redis/client.rb:459: warning: constant ::Fixnum is deprecated
>>> Calling SET hello world
127.0.0.1:6379: MOVED 866 127.0.0.1:6381
127.0.0.1:6383: MOVED 866 127.0.0.1:6381
127.0.0.1:6381: OK
127.0.0.1:6382: MOVED 866 127.0.0.1:6381
127.0.0.1:6384: MOVED 866 127.0.0.1:6381
127.0.0.1:6380: MOVED 866 127.0.0.1:6381

[root@slowtech conf]# redis-trib.rb call 127.0.0.1:6379 get hello
/usr/local/ruby/lib/ruby/gems/2.5.0/gems/redis-3.3.0/lib/redis/client.rb:459: warning: constant ::Fixnum is deprecated
>>> Calling GET hello
127.0.0.1:6379: MOVED 866 127.0.0.1:6381
127.0.0.1:6383: MOVED 866 127.0.0.1:6381
127.0.0.1:6381: world
127.0.0.1:6382: MOVED 866 127.0.0.1:6381
127.0.0.1:6384: MOVED 866 127.0.0.1:6381
127.0.0.1:6380: MOVED 866 127.0.0.1:6381
```



# 将外部redis数据导入集群

```bash
redis-trib.rb import --from 127.0.0.1:6378 127.0.0.1:6379
```

其内部处理流程如下：

1> 通过load_cluster_info_from_node方法加载集群信息，check_cluster方法检查集群是否健康。

2> 连接外部redis节点，如果外部节点开启了cluster_enabled，则提示错误（[ERR] The source node should not be a cluster node.）

3> 通过scan命令遍历外部节点，一次获取1000条数据。

4> 遍历这些key，计算出key对应的slot。

5> 执行migrate命令,源节点是外部节点,目的节点是集群slot对应的节点，如果设置了--copy参数，则传递copy参数，其会保留源节点的key，如果设置了--replace，则传递replace参数。如果目标节点中存在同名key，其值会被覆盖。两个参数可同时指定。

6> 不停执行scan命令，直到遍历完所有key。

7> 迁移完成。

```bash
[root@slowtech conf]# redis-trib.rb import --from 127.0.0.1:6378 --replace  127.0.0.1:6379 
>>> Importing data from 127.0.0.1:6378 to cluster 
/usr/local/ruby/lib/ruby/gems/2.5.0/gems/redis-3.3.0/lib/redis/client.rb:459: warning: constant ::Fixnum is deprecated
>>> Performing Cluster Check (using node 127.0.0.1:6379)
S: d826c5fd98efa8a17a880e9a90a25f06c88e6ae9 127.0.0.1:6379
   slots: (0 slots) slave
   replicates a8b3d0f9b12d63dab3b7337d602245d96dd55844
S: 55c05d5b0dfea0d52f88548717ddf24975268de6 127.0.0.1:6383
   slots: (0 slots) slave
   replicates a8b3d0f9b12d63dab3b7337d602245d96dd55844
M: f413fb7e6460308b17cdb71442798e1341b56cbc 127.0.0.1:6381
   slots:50-16383 (16334 slots) master
   2 additional replica(s)
S: beba753c5a63607fa66d9ec7427ed9a511ea136e 127.0.0.1:6382
   slots: (0 slots) slave
   replicates f413fb7e6460308b17cdb71442798e1341b56cbc
S: 83797d518e56c235272402611477f576973e9d34 127.0.0.1:6384
   slots: (0 slots) slave
   replicates f413fb7e6460308b17cdb71442798e1341b56cbc
M: a8b3d0f9b12d63dab3b7337d602245d96dd55844 127.0.0.1:6380
   slots:0-49 (50 slots) master
   2 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
>>> Connecting to the source Redis instance
*** Importing 1 keys from DB 0
Migrating key5 to 127.0.0.1:6381: OK
```





