# 1.httpd基础知识

![image-20230704192137636](./image/w0dfbp-0.png)

![image-20230704192225824](./image/w0skx7-0.png)

![image-20230704192242635](./image/w0pvsp-0.png)

![image-20230704192430791](./image/w0z25f-0.png)

![image-20230704192621874](./image/w1d0ky-0.png)

![image-20230704193330484](./image/w1jqgg-0.png)



# 2.HTTPD工作模型

![image-20230704194710308](./image/w7coev-0.png)

![image-20230704194934684](./image/w8n88i-0.png)

![image-20230704195445430](./image/wbpasb-0.png)

![image-20230704200608340](./image/x6h917-0.png)

![image-20230704200658548](./image/x6xj48-0.png)

![image-20230704200749193](./image/x780lo-0.png)

![image-20230704201134362](./image/x9ihzh-0.png)

![image-20230704201333134](./image/xapuxw-0.png)

![image-20230704201410965](./image/xb6ajq-0.png)

![image-20230704201507403](./image/xbrdsu-0.png)

![image-20230704201436965](./image/xbc4k5-0.png)

![image-20230704202433909](./image/xhc1zc-0.png)



# 3.HTTPD

## 1.MPM

![image-20230704202800317](./image/xjhm19-0.png)

![image-20230707145004107](D://i/2023/07/07/nzc2vn-0.png)

![image-20230704203034385](./image/xkwyqv-0.png)

![image-20230704203755558](./image/xpe1tw-0.png)

![image-20230704203529733](./image/xnugcg-0.png)

![image-20230704203655969](./image/xosow6-0.png)



## 2.安装

![image-20230705084540981](./image/dzp44j-0.png)

![image-20230705084931675](./image/e1oi87-0.png)

![image-20230705084955376](./image/e1tsxw-0.png)



## 3.配置

![image-20230705085159934](./image/e3bq6q-0.png)

![image-20230705085904031](./image/e7lszg-0.png)

![image-20230705090318781](./image/eytz2h-0.png)

![image-20230705090449323](./image/eyk2ay-0.png)

![image-20230705091005060](./image/f1wsbz-0.png)

![image-20230705091236166](./image/f38jc0-0.png)

![image-20230705092219816](./image/f92f2o-0.png)

![image-20230705095204320](./image/fqwl3y-0.png)

![image-20230705095918373](./image/fv5o9r-0.png)

```bash
# 在httpd2.4，设置文档页面之后需要授权
DocumentRoot "/var/www/html"

#
# Relax access to content within /var/www.
#
<Directory "/var/www">
    AllowOverride None #该指令指定不允许在该目录中覆盖 Apache 的默认设置。这可以增加服务器的安全性，因为阻止了用户可能通过 .htaccess 文件来修改服务器的行为。
    # Allow open access:
    Require all granted # 定义了访问控制规则
</Directory>
```

![image-20230705100305545](./image/gl9uam-0.png)

![image-20230705100356564](./image/glimk5-0.png)

![image-20230705100419611](./image/glw6ra-0.png)

![image-20230705100637934](./image/gn8q0s-0.png)

![image-20230705100707218](./image/gnlmnv-0.png)

![image-20230705100944437](./image/gp0fiq-0.png)

![image-20230705101327804](./image/grd9og-0.png)

![image-20230705101429440](./image/grw9j1-0.png)

```bash
ErrorLog "logs/error_log"
# LogLevel: Control the number of messages logged to the error_log.
LogLevel warn
    # a CustomLog directive (see below).
    LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
    LogFormat "%h %l %u %t \"%r\" %>s %b" common
      LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O" combinedio
    # The location and format of the access logfile (Common Logfile Format).
    #CustomLog "logs/access_log" common
    # (Combined Logfile Format) you can use the following directive.
    CustomLog "logs/access_log" combined
```

![image-20230705104036707](./image/h7f8pq-0.png)

![image-20230705104351223](./image/h9apn7-0.png)

![image-20230705104539686](./image/haf6rp-0.png)

![image-20230705105451829](./image/hfumtm-0.png)

> 需要加载`auth_basic`模块

![image-20230705110209305](./image/i86308-0.png)

![image-20230705110220671](./image/i895ig-0.png)

![image-20230705112513705](./image/ilz9dh-0.png)

![image-20230705112806788](./image/innl99-0.png)

![image-20230705112838071](./image/inttv3-0.png)

![image-20230705113734972](./image/it8ibi-0.png)

![image-20230705113800709](./image/itjvyp-0.png)

![image-20230705114351713](./image/iwu75k-0.png)



# 4.多虚拟主机

## 1.基于ip

![image-20230705115310226](./image/j2lqxq-0.png)



## 2.基于port

![image-20230705115441764](./image/j3cebs-0.png)



## 3.基于多主机

![image-20230705144913300](./image/nytw18-0.png)



# 5.mod_deflate模块

![image-20230705145413330](./image/o1unad-0.png)

![image-20230705145841925](./image/o4by4u-0.png)



# 6.https

![image-20230705150244240](./image/ouvkgm-0.png)

```bash
# 安装ssl模块
# 安装之后
 yum install mod_ssl
 
 # 加密配置文件
/etc/httpd/conf.d/ssl.conf
# SSLCertificateFile /etc/pki/tls/certs/localhost.crt 证书
# SSLCertificateKeyFile /etc/pki/tls/private/localhost.key 私钥

#SSLCertificateChainFile /etc/pki/tls/certs/server-chain.crt CA证书
```

![image-20230705160403410](./image/qj0tzf-0.png)

```bash
<VirtualHost *:80>
    #DocumentRoot /var/www/asite
    ServerName www.a.com
    Redirect temp / https://www.a.com/
</VirtualHost>

<VirtualHost *:443>
    DocumentRoot /var/www/asite
    ServerName www.a.com
    SSLEngine on
    SSLCertificateFile /etc/httpd/conf.d/ssl/httpd.crt
    SSLCertificateKeyFile /etc/httpd/conf.d/ssl/httpd.key

    # 添加其他HTTPS相关配置
</VirtualHost>
```



# 7.重定向

![image-20230705160904468](./image/qlzzk4-0.png)

> 如果不在虚拟主机中使用`Redirect`，可能会造成循环重定向问题

![image-20230705201144318](./image/x9x7fi-0.png)





# 8.代理

![image-20230705202910576](./image/xk5pfr-0.png)

![image-20230705203156254](./image/xlwe7r-0.png)



# 9.Sendfile(零复制)

![image-20230705204451380](./image/xtm415-0.png)

![image-20230705204616707](./image/xu9cdc-0.png)



# 10.HTTP协议

![image-20230706092635866](./image/fbl45a-0.png)

![image-20230706092810994](./image/fckxf8-0.png)

![image-20230706093141445](./image/fem5qt-0.png)

![image-20230706093550903](./image/fgzh4j-0.png)

![image-20230706093756512](./image/fiiq48-0.png)

![image-20230706093942965](./image/fjbncw-0.png)

![image-20230706094041561](./image/fjx6vb-0.png)

![image-20230706094245050](./image/fl43zc-0.png)

![image-20230706094528388](./image/fmwy08-0.png)

![image-20230706103652760](./image/h55f2x-0.png)

![image-20230706103909338](./image/h6pvcb-0.png)

![image-20230706104252002](./image/h8pgkk-0.png)

![image-20230706105919181](./image/iartq5-0.png)

![image-20230706110205935](./image/i8vig1-0.png)

![image-20230706110245398](./image/i8yv70-0.png)

![image-20230706110258037](./image/i9gosx-0.png)

![image-20230706110641301](./image/ib5484-0.png)



# 11.HTTPD编译安装

![image-20230706110753894](./image/ica72i-0.png)

![image-20230706111947635](./image/iij4jx-0.png)

![image-20230706112119242](./image/ijk559-0.png)



# 12.LAMP

![image-20230706120420650](./image/jx1qih-0.png)

![image-20230706142834798](./image/nmiiyg-0.png)

![image-20230706143149207](./image/noay7g-0.png)



## 1.PHP

![image-20230706143216985](./image/nospm2-0.png)

![image-20230706143338910](./image/npru48-0.png)

![image-20230706143424350](./image/npzo5w-0.png)

![image-20230706143447550](./image/nq3ytd-0.png)



## 2.Module方式

![image-20230706143751670](./image/nsdw8d-0.png)

![image-20230706144146958](./image/nujkud-0.png)

```bash
# 优先解析index.php
DirectoryIndex index.php index.html
```

![image-20230706144226561](./image/nuq6mv-0.png)

![image-20230706144458512](./image/nwijp6-0.png)

![image-20230706150414684](./image/ovjg8k-0.png)



## 3.LAMP部署应用

![image-20230706151401402](./image/p1indo-0.png)



### 1.phpadmin

![image-20230706154735812](./image/plajm2-0.png)



### 2.wordpress

![image-20230706155232598](./image/poamlk-0.png)

![image-20230706162219608](./image/qtw3p6-0.png)



### 3.powerdns

![image-20230706162243144](./image/qtz5r2-0.png)

![image-20230706164133359](./image/r5cspt-0.png)

![image-20230706164829208](./image/r9e6fu-0.png)

![image-20230706170344289](./image/s6kqyd-0.png)

![image-20230706171401543](./image/scl612-0.png)

![image-20230706172034990](./image/sgdnga-0.png)



## 4.PHP FastCGI方式

![image-20230706190417328](./image/vhq2k7-0.png)

![image-20230706190528159](./image/vih92l-0.png)

![image-20230706191519521](./image/vodmbr-0.png)

![image-20230706191540202](./image/vofh1j-0.png)

```bash
DirectoryIndex index.php
ProxyRequests off
ProxyPassMatch "^/.*\.php(.*)$" "fcgi://127.0.0.1:9000/var/www/html/"
```

![image-20230706204537488](./image/xu5qd1-0.png)

![image-20230706210628038](./image/yu41an-0.png)



## 5.编译PHP

![image-20230706214012849](./image/ze71uq-0.png)

![image-20230706214030247](./image/zeakmx-0.png)

![image-20230706215615982](./image/znqm5s-0.png)
