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

请自行安装 Python3.7环境+Django环境，可用nginx代理

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



3、L2TP  IPSEC 配置文件

```
filedata_dir = os.path.join(BASE_DIR,"data")  #读取L2TP文件目录
ipsecpwd_dir = os.path.join(BASE_DIR,"ipsec") #读取ipsec passwd文件

filedata_path=os.path.join(filedata_dir,"chap-secrets")  # 配置文件
ipsecpwd_path = os.path.join(ipsecpwd_dir,"passwd")
filedata_path_bak = os.path.join(filedata_dir,"chap-secrets.bak")  # 备份配置文件 (修改的时候需要使用请一定要与配置文件名称一样)
ipsecpwd_path_bak = os.path.join(ipsecpwd_dir,"passwd.bak")
userinfo_path = os.path.join(filedata_dir,"userinfo")  # 用户文件
```



4、服务器部署

```
pip3 install django
nohub python3 manage.py runserver 0.0.0.0:8000 >>/var/log/web_l2tp.log 2<&1 &
```



5、添加账户

本系统中data目录下的userinfo下一行添加账户与密码信息(加盐处理)

6、系统效果展示

![shouye.png](https://kyun.ltyuanfang.cn/tc/2020/05/30/abd487eca6676.png)



![index.png](https://kyun.ltyuanfang.cn/tc/2020/05/30/862e897a97d9c.png)

![add.png](https://kyun.ltyuanfang.cn/tc/2020/05/30/d57fa19fae049.png)

![change.png](https://kyun.ltyuanfang.cn/tc/2020/05/30/6149d8c141a31.png)