from django.shortcuts import HttpResponse,render,redirect
from l2tp_web import settings
from functools import wraps
import os
import json
import subprocess
import hashlib
# Create your views here.

print(settings.userinfo_path)
print(os.path.exists(settings.userinfo_path))
def auth(username, password):
    with open(settings.userinfo_path, encoding='utf-8', ) as f1:
        for line in f1:
            line = line.strip()
            if not line == '':
                user, pwd = line.split("|")
                if username == user and password == pwd:
                    return True

def login(request):
    msg = ""
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get("user",None)
        pwd = request.POST.get('pwd',None)
        md5 = hashlib.md5()
        md5.update(bytes(pwd,encoding='utf-8'))
        md5_pwd = md5.hexdigest()
        print(user,md5_pwd)
    res = auth(user,md5_pwd)
    #做是否登陆成功的判断
    if res:
        request.session.set_expiry(10) #session认证时间为10s，10s之后session认证失效
        request.session["is_login"] = "1"
        request.session["username"] = user
        request.session.set_expiry(0)  #session在关闭浏览器后失效
        return redirect("/index/")
    else:
        msg = "用户名或者密码错误"
    return render(request,"login.html",{"error": msg})

# 装饰器函数，用来判断是否登录
def check_login(func):
    @wraps(func)  # 装饰器修复技术
    def inner(request, *args, **kwargs):
        ret = request.session.get("is_login")
        print(ret)
        # 1. 获取cookie中的随机字符串
        # 2. 根据随机字符串去文件取 session_data --> 解密 --> 反序列化成字典
        # 3. 在字典里面 根据 is_login 取具体的数据
        if ret == "1":
            # 已经登录，继续执行
            return func(request, *args, **kwargs)
        # 没有登录过
        else:
            # ** 即使登录成功也只能跳转到index页面，现在通过在URL中加上next指定跳转的页面
            # 获取当前访问的URL
            next_url = request.path_info
            print(next_url)
            return redirect("/login/?next={}".format(next_url))
    return inner

@check_login
def test(request):
    if request.session["is_login"]:
        return HttpResponse(request.session["username"])
    else:
        return HttpResponse("gun")

@check_login
def index(request):
    lt_list=[]
    with open(settings.filedata_path, encoding='utf-8') as f1:
        for line in f1:
            dic = {}
            user, l2tp, pwd, all = line.split(' ')
            dic = {"user":json.loads(user),"pwd":json.loads(pwd)}
            lt_list.append(dic)
    return render(request,"index.html",{"lt_list":lt_list})

@check_login
def delete(request):
    print('===========================')
    print(request.GET)
    name = request.GET.get("username",None)
    if name:
        with open(settings.filedata_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(settings.filedata_path, "w", encoding="utf-8") as f_w:
            for line in lines:
                username, l2tp, password, all = line.split(' ')
                if name in username:
                    continue
                f_w.write(line)
        with open(settings.ipsecpwd_path, "r", encoding="utf-8") as i:
            lines = i.readlines()
        with open(settings.ipsecpwd_path, "w", encoding="utf-8") as i_w:
            for line in lines:
                username,pwd,psk = line.split(':')
                if name in username:
                    continue                 #删除ipsec passwd文件内容
                i_w.write(line)
    return redirect('/index/')



@check_login
def edit(request):
    if request.method == "GET":
        name = request.GET.get("username",None)
        if name:
            with open(settings.filedata_path, "r", encoding="utf-8") as f:
                for line in f:
                    username, l2tp, password, all = line.split(' ')
                    dic = {}
                    dic['user'] = json.loads(username)
                    dic['password'] = json.loads(password)
                    if name in username:
                        return render(request,"edit.html",{"row":dic})
    if request.method == "POST":
        print(request.POST)
        old_user = request.GET.get("username")
        print(old_user)
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        CMD = "openssl passwd -1 %s" % pwd
        pwd_str = subprocess.getoutput(CMD)
        if old_user:
            with open(settings.filedata_path, encoding='utf-8') as f1, \
                    open(settings.filedata_path_bak, encoding='utf-8', mode='w') as f2:
                for line in f1:
                    username, l2tp, password, all = line.split(' ')
                    if old_user in username:
                        line = '"{}" {} "{}" {}\n'.format(user, 'l2tpd', pwd, '*')
                    f2.write(line)
            os.remove(settings.filedata_path)
            os.rename(settings.filedata_path_bak, settings.filedata_path)
            with open(settings.ipsecpwd_path, encoding='utf-8') as p1, \
                    open(settings.ipsecpwd_path_bak, encoding='utf-8', mode='w') as p2:
                for line in p1:
                    username, password, psk = line.split(':')
                    if old_user in username:
                        line = '{}:{}:{}\n'.format(user,pwd_str,'xauth-psk')
                    p2.write(line)
            os.remove(settings.ipsecpwd_path)
            os.rename(settings.ipsecpwd_path_bak, settings.ipsecpwd_path)
            return redirect("/index/")
    return redirect('/index/')

@check_login
def add(request):
    if request.method == "GET":
        return render(request,"add.html")

    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
    CMD = "openssl passwd -1 %s"%pwd
    pwd_str = subprocess.getoutput(CMD)
    try:
        with open(settings.ipsecpwd_path, encoding='utf-8') as p1, \
                open(settings.ipsecpwd_path, encoding='utf-8', mode='a') as p2:
             for line in p1:
                 username,password,psk = line.split(':')
                 if not user == username:
                    print(username,user)
             p2.write('{}:{}:{}\n'.format(user,pwd_str,'xauth-psk'))
        with open(settings.filedata_path, encoding='utf-8') as f1, \
                open(settings.filedata_path, encoding='utf-8', mode='a') as f2:
              for line in f1:
                   username, l2tp, password, all = line.split(' ')
                   if not user == username:
                      print(username,user)
              f2.write('"{}" {} "{}" {}\n'.format(user,'l2tpd',pwd,'*'))
        return redirect("/index")
    except Exception as e:
        hint = '<script>alert("添加失败！");window.location.href="/index/"</script>'
    return hint

@check_login
def logout(request):
    request.session.get("is_login")
    request.session.clear() #清除所有session
    return redirect('/login')


