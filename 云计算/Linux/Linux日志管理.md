# Linux日志管理

## 1.日志

![image-20230703191115825](../../.gitbook/assets/vtntjj-0.png)

![image-20230703191513881](../../.gitbook/assets/vtn77v-0.png)

![image-20230703191733862](../../.gitbook/assets/vtmhhv-0.png)

![image-20230703192407224](../../.gitbook/assets/vtlahz-0.png)

![image-20230703192945723](../../.gitbook/assets/vwr2vc-0.png)

```bash
# 如果想要开启日志远程功能，需要开启以下两个配置，且在target中，一个@表示UDP协议，两个表示TCp协议

# Provides UDP syslog reception
#$ModLoad imudp
#$UDPServerRun 514

# Provides TCP syslog reception
#$ModLoad imtcp
#$InputTCPServerRun 514
```

![image-20230703195646813](../../.gitbook/assets/wd6uk8-0.png)

### 1.journalctl

![image-20230703203229798](../../.gitbook/assets/xm2igz-0.png)

![image-20230703203345595](../../.gitbook/assets/xn19cj-0.png)

![image-20230703203508886](../../.gitbook/assets/xno03a-0.png)

![image-20230703203534493](../../.gitbook/assets/xnund1-0.png)

### 2.将日志存到数据库中

![image-20230703203635225](../../.gitbook/assets/xohavx-0.png)

## 2.loganalyer
