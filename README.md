# L2TP-OVER-IPSEC-Manager-Web
**l2tp over ipsec 账户管理系统**
**说明: 该软件为管理l2tp服务在使用前请先自行安装好l2tp over ipsec服务，直接读取你l2tp和ipsec的配置文件，在使用时需要安装python3.7环境具体看下面步骤:**

```
#秘钥配置文件
/etc/ppp/chap-secrets
/etc/ipsec.d/passwd
```

安装L2TP over IPSEC 参考 [这里](https://github.com/hwdsl2/setup-ipsec-vpn)

1、安装python环境；

2、安装Django；

```
pip3 install django
#django版本
D:\>python
Python 3.7.1 (v3.7.1:260ec2c36a, Oct 20 2018, 14:57:15) [MSC v.1915 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import django
>>> print(django.VERSION)
(3, 0, 6, 'final', 0)
```



3、下载代码



4、服务器部署



5、添加账户

本系统中data目录下的userinfo下一行行添加账户与密码信息

6、系统效果展示

![image](https://raw.githubusercontent.com/cuijianzhe/L2TP-OVER-IPSEC-Manager-Web/master/images/shouye.png)

![images](https://raw.githubusercontent.com/cuijianzhe/L2TP-OVER-IPSEC-Manager-Web/master/images/index.png)



![images](https://raw.githubusercontent.com/cuijianzhe/L2TP-OVER-IPSEC-Manager-Web/master/images/add.png)

![](https://raw.githubusercontent.com/cuijianzhe/L2TP-OVER-IPSEC-Manager-Web/master/images/change.png)