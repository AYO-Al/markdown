# HTTPD

## 1.httpd基础知识

![image-20230704192137636](../../.gitbook/assets/w0dfbp-0.png)

![image-20230704192225824](../../.gitbook/assets/w0skx7-0.png)

![image-20230704192242635](../../.gitbook/assets/w0pvsp-0.png)

![image-20230704192430791](../../.gitbook/assets/w0z25f-0.png)

![image-20230704192621874](../../.gitbook/assets/w1d0ky-0.png)

![image-20230704193330484](../../.gitbook/assets/w1jqgg-0.png)

## 2.HTTPD工作模型

![image-20230704194710308](../../.gitbook/assets/w7coev-0.png)

![image-20230704194934684](../../.gitbook/assets/w8n88i-0.png)

![image-20230704195445430](../../.gitbook/assets/wbpasb-0.png)

![image-20230704200608340](../../.gitbook/assets/x6h917-0.png)

![image-20230704200658548](../../.gitbook/assets/x6xj48-0.png)

![image-20230704200749193](../../.gitbook/assets/x780lo-0.png)

![image-20230704201134362](../../.gitbook/assets/x9ihzh-0.png)

![image-20230704201333134](../../.gitbook/assets/xapuxw-0.png)

![image-20230704201410965](../../.gitbook/assets/xb6ajq-0.png)

![image-20230704201507403](../../.gitbook/assets/xbrdsu-0.png)

![image-20230704201436965](../../.gitbook/assets/xbc4k5-0.png)

![image-20230704202433909](../../.gitbook/assets/xhc1zc-0.png)

## 3.HTTPD

### 1.MPM

![image-20230704202800317](../../.gitbook/assets/xjhm19-0.png)

![image-20230707145004107](d://i/2023/07/07/nzc2vn-0.png)

![image-20230704203034385](../../.gitbook/assets/xkwyqv-0.png)

![image-20230704203755558](../../.gitbook/assets/xpe1tw-0.png)

![image-20230704203529733](../../.gitbook/assets/xnugcg-0.png)

![image-20230704203655969](../../.gitbook/assets/xosow6-0.png)

### 2.安装

![image-20230705084540981](../../.gitbook/assets/dzp44j-0.png)

![image-20230705084931675](../../.gitbook/assets/e1oi87-0.png)

![image-20230705084955376](../../.gitbook/assets/e1tsxw-0.png)

### 3.配置

![image-20230705085159934](../../.gitbook/assets/e3bq6q-0.png)

![image-20230705085904031](../../.gitbook/assets/e7lszg-0.png)

![image-20230705090318781](../../.gitbook/assets/eytz2h-0.png)

![image-20230705090449323](../../.gitbook/assets/eyk2ay-0.png)

![image-20230705091005060](../../.gitbook/assets/f1wsbz-0.png)

![image-20230705091236166](../../.gitbook/assets/f38jc0-0.png)

![image-20230705092219816](../../.gitbook/assets/f92f2o-0.png)

![image-20230705095204320](../../.gitbook/assets/fqwl3y-0.png)

![image-20230705095918373](../../.gitbook/assets/fv5o9r-0.png)

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

![image-20230705100305545](../../.gitbook/assets/gl9uam-0.png)

![image-20230705100356564](../../.gitbook/assets/glimk5-0.png)

![image-20230705100419611](../../.gitbook/assets/glw6ra-0.png)

![image-20230705100637934](../../.gitbook/assets/gn8q0s-0.png)

![image-20230705100707218](../../.gitbook/assets/gnlmnv-0.png)

![image-20230705100944437](../../.gitbook/assets/gp0fiq-0.png)

![image-20230705101327804](../../.gitbook/assets/grd9og-0.png)

![image-20230705101429440](../../.gitbook/assets/grw9j1-0.png)

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

![image-20230705104036707](../../.gitbook/assets/h7f8pq-0.png)

![image-20230705104351223](../../.gitbook/assets/h9apn7-0.png)

![image-20230705104539686](../../.gitbook/assets/haf6rp-0.png)

![image-20230705105451829](../../.gitbook/assets/hfumtm-0.png)

> 需要加载`auth_basic`模块

![image-20230705110209305](../../.gitbook/assets/i86308-0.png)

![image-20230705110220671](../../.gitbook/assets/i895ig-0.png)

![image-20230705112513705](../../.gitbook/assets/ilz9dh-0.png)

![image-20230705112806788](../../.gitbook/assets/innl99-0.png)

![image-20230705112838071](../../.gitbook/assets/inttv3-0.png)

![image-20230705113734972](../../.gitbook/assets/it8ibi-0.png)

![image-20230705113800709](../../.gitbook/assets/itjvyp-0.png)

![image-20230705114351713](../../.gitbook/assets/iwu75k-0.png)

## 4.多虚拟主机

### 1.基于ip

![image-20230705115310226](../../.gitbook/assets/j2lqxq-0.png)

### 2.基于port

![image-20230705115441764](../../.gitbook/assets/j3cebs-0.png)

### 3.基于多主机

![image-20230705144913300](../../.gitbook/assets/nytw18-0.png)

## 5.mod\_deflate模块

![image-20230705145413330](../../.gitbook/assets/o1unad-0.png)

![image-20230705145841925](../../.gitbook/assets/o4by4u-0.png)

## 6.https

![image-20230705150244240](../../.gitbook/assets/ouvkgm-0.png)

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

![image-20230705160403410](../../.gitbook/assets/qj0tzf-0.png)

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

## 7.重定向

![image-20230705160904468](../../.gitbook/assets/qlzzk4-0.png)

> 如果不在虚拟主机中使用`Redirect`，可能会造成循环重定向问题

![image-20230705201144318](../../.gitbook/assets/x9x7fi-0.png)

## 8.代理

![image-20230705202910576](../../.gitbook/assets/xk5pfr-0.png)

![image-20230705203156254](../../.gitbook/assets/xlwe7r-0.png)

## 9.Sendfile(零复制)

![image-20230705204451380](../../.gitbook/assets/xtm415-0.png)

![image-20230705204616707](../../.gitbook/assets/xu9cdc-0.png)

## 10.HTTP协议

![image-20230706092635866](../../.gitbook/assets/fbl45a-0.png)

![image-20230706092810994](../../.gitbook/assets/fckxf8-0.png)

![image-20230706093141445](../../.gitbook/assets/fem5qt-0.png)

![image-20230706093550903](../../.gitbook/assets/fgzh4j-0.png)

![image-20230706093756512](../../.gitbook/assets/fiiq48-0.png)

![image-20230706093942965](../../.gitbook/assets/fjbncw-0.png)

![image-20230706094041561](../../.gitbook/assets/fjx6vb-0.png)

![image-20230706094245050](../../.gitbook/assets/fl43zc-0.png)

![image-20230706094528388](../../.gitbook/assets/fmwy08-0.png)

![image-20230706103652760](../../.gitbook/assets/h55f2x-0.png)

![image-20230706103909338](../../.gitbook/assets/h6pvcb-0.png)

![image-20230706104252002](../../.gitbook/assets/h8pgkk-0.png)

![image-20230706105919181](../../.gitbook/assets/iartq5-0.png)

![image-20230706110205935](../../.gitbook/assets/i8vig1-0.png)

![image-20230706110245398](../../.gitbook/assets/i8yv70-0.png)

![image-20230706110258037](../../.gitbook/assets/i9gosx-0.png)

![image-20230706110641301](../../.gitbook/assets/ib5484-0.png)

## 11.HTTPD编译安装

![image-20230706110753894](../../.gitbook/assets/ica72i-0.png)

![image-20230706111947635](../../.gitbook/assets/iij4jx-0.png)

![image-20230706112119242](../../.gitbook/assets/ijk559-0.png)

## 12.LAMP

![image-20230706120420650](../../.gitbook/assets/jx1qih-0.png)

![image-20230706142834798](../../.gitbook/assets/nmiiyg-0.png)

![image-20230706143149207](../../.gitbook/assets/noay7g-0.png)

### 1.PHP

![image-20230706143216985](../../.gitbook/assets/nospm2-0.png)

![image-20230706143338910](../../.gitbook/assets/npru48-0.png)

![image-20230706143424350](../../.gitbook/assets/npzo5w-0.png)

![image-20230706143447550](../../.gitbook/assets/nq3ytd-0.png)

### 2.Module方式

![image-20230706143751670](../../.gitbook/assets/nsdw8d-0.png)

![image-20230706144146958](../../.gitbook/assets/nujkud-0.png)

```bash
# 优先解析index.php
DirectoryIndex index.php index.html
```

![image-20230706144226561](../../.gitbook/assets/nuq6mv-0.png)

![image-20230706144458512](../../.gitbook/assets/nwijp6-0.png)

![image-20230706150414684](../../.gitbook/assets/ovjg8k-0.png)

### 3.LAMP部署应用

![image-20230706151401402](../../.gitbook/assets/p1indo-0.png)

#### 1.phpadmin

![image-20230706154735812](../../.gitbook/assets/plajm2-0.png)

#### 2.wordpress

![image-20230706155232598](../../.gitbook/assets/poamlk-0.png)

![image-20230706162219608](../../.gitbook/assets/qtw3p6-0.png)

#### 3.powerdns

![image-20230706162243144](../../.gitbook/assets/qtz5r2-0.png)

![image-20230706164133359](../../.gitbook/assets/r5cspt-0.png)

![image-20230706164829208](../../.gitbook/assets/r9e6fu-0.png)

![image-20230706170344289](../../.gitbook/assets/s6kqyd-0.png)

![image-20230706171401543](../../.gitbook/assets/scl612-0.png)

![image-20230706172034990](../../.gitbook/assets/sgdnga-0.png)

### 4.PHP FastCGI方式

![image-20230706190417328](../../.gitbook/assets/vhq2k7-0.png)

![image-20230706190528159](../../.gitbook/assets/vih92l-0.png)

![image-20230706191519521](../../.gitbook/assets/vodmbr-0.png)

![image-20230706191540202](../../.gitbook/assets/vofh1j-0.png)

```bash
DirectoryIndex index.php
ProxyRequests off
ProxyPassMatch "^/.*\.php(.*)$" "fcgi://127.0.0.1:9000/var/www/html/"
```

![image-20230706204537488](../../.gitbook/assets/xu5qd1-0.png)

![image-20230706210628038](../../.gitbook/assets/yu41an-0.png)

### 5.编译PHP

![image-20230706214012849](../../.gitbook/assets/ze71uq-0.png)

![image-20230706214030247](../../.gitbook/assets/zeakmx-0.png)

![image-20230706215615982](../../.gitbook/assets/znqm5s-0.png)
