# 欢迎使用 django4blog 手册
 本项目参考CSDN李威威wiwi教程 [传送门](https://blog.csdn.net/agelee/category_11969257.html)。
## 本地部署
### 修改settings.py文件

先在数据库创建数据库，填写以下对应信息
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'django4blog',  # 数据库名称
        'HOST': '127.0.0.1',  # 数据库地址
        'PORT': 3306,  # 端口
        'USER': 'root',  # 用户名
        'PASSWORD': '',  # 数据库密码
    }
}
```
### 数据库迁移
完成模型的定义后，接着在目标数据库中创建相应的数据表，这个步骤在Django中叫做数据迁移。

**注意，每当对数据库进行了更改（添加、修改、删除等）操作，都需要进行数据迁移。**

jango的迁移代码是由模型文件自动生成的，它本质上只是个历史记录，Django可以用它来进行数据库的滚动更新，通过这种方式使其能够和当前的模型匹配。
在目标数据库中创建表（数据迁移）可以通过Django的管理工具使用特定的代码指令完成。
在目标数据库中创建数据表需要执行两次指令，分别是makemigrations和migrate指令。
在终端运行以下指令
```
python manage.py makemigrations
python manage.py migrate
```
### 创建超级用户
在Pycharm的终端输入框输入如下命令：
```
python manage.py createsuperuser
```
最后启动即可。

## 准备服务器
现在我们开始部署到服务器，
我准备了一台AWS的服务器练手。

## 安装Xshell和Xftp

### Xshell和Xftp都是 NetSarang 开发的远程工具。
 
```gantt
Xshell可以远程连接并控制服务器
Xftp可以远程传输文件到服务器
```

## 服务器软件安装

### 安装之前，我们先升级下系统内库的版本，防止系统版本过旧导致问题。
```gantt
apt update
apt upgrade
```

### 安装必要的软件：Nginx，Python，PIP，同时 PIP 安装了Python虚拟环境virtualenv库。
```gantt
apt install nginx
apt install python3
apt install python3-pip
pip3 install virtualenv
```

## 安装Mysql
```gantt
apt install mysql-server
```
检查运行状态
```gantt
systemctl status mysql
```
安装完成后使用命令直接root用户登录
```gantt
mysql
```
（在MySQL 8.0上，root 用户默认通过auth_socket插件授权，无法使用密码登录，修改密码后才能启用密码登录。）

然后在mysql命令界面输入下面两条命令修改root用户的密码为你的最新密码：
```gantt
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'newpassword';
 
mysql> FLUSH PRIVILEGES;
```

退出mysql
```gantt
mysql> exit
```
然后检查下使用root密码登录是否成功：
```gantt
mysql -u root -p
```
我们把数据库也一起创建了（名字和我们本地创建的一样就好了）：
```gantt
mysql> CREATE DATABASE IF NOT EXISTS django_blog DEFAULT CHARSET utf8mb4;
```

## 修改Django项目配置文件
回到本地项目，修改下配置文件django4blog/settings.py。
```gantt
DEBUG = False
 
ALLOWED_HOSTS = ['*']
 
# 静态文件收集目录
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
```
### 主要涉及3点：

* 部署时要关闭调试模式，避免安全性问题（此时 Django 就不再处理静态资源了）。
* ALLOWED_HOSTS指明了允许访问的服务器名称或 IP，星号表示允许所有的请求。实际部署时请改成你的域名或 IP，比如ALLOWED_HOSTS = [ '127.0.0.1']。
* 项目中有很多静态文件，部署时需要找一个地方统一收集起来，也就是STATIC_ROOT指定的地址了，指定了这个地址后，Django在部署的时候可以通过命令将所有的（包括Django自带的Admin页面相关）静态资源（css，js等）全部收集到指定文件夹，便于我们在部署的时候统一加载。

### 接着我们需要修改下配置解决在线部署的跨域问题：
* 先PIP安装一下包django-cors-headers：
* pip install django-cors-headers

### 然后修改下配置文件django4blog/settings.py
```gantt
INSTALLED_APPS = [
    ......
    'corsheaders',  #解决浏览器跨域问题
    ......
]
 
MIDDLEWARE = [
    ......
    'corsheaders.middleware.CorsMiddleware',  #解决浏览器跨域问题
    'django.middleware.common.CommonMiddleware', #解决浏览器跨域问题
    ......
]
 
CORS_ORIGIN_ALLOW_ALL = True #解决浏览器跨域问题
CORS_ALLOW_CREDENTIALS = True #解决浏览器跨域问题
 
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'None'  #Django4 特定解决浏览器跨域问题
```
另外，如果我们服务器数据库密码和本地的数据库密码不一致，我们可以提前修改下配置文件的参数：
```gantt
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',    # 数据库引擎
        'NAME': 'django_blog', # 数据库名称
        'HOST': '127.0.0.1', # 数据库地址，本机 ip 地址 127.0.0.1
        'PORT': 3306, # 端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'newpassword', # 数据库密码 修改为服务器数据库密码
    }
}
```
最后我们将我们本地项目需要用到的库列一个清单，以便在服务器上统一安装。

在本地虚拟环境中输入命令： pip freeze > requirements.txt

得到库清单文件requirements.txt。

## 传输Django项目到服务器
本地项目参数修订好之后，我们登陆Xftp，直接将本地项目文件夹django_project复制到服务器

传输完成后回到Xshell的服务器操作界面，进入我们的项目文件夹django_project
```
cd django_project
```
接着在服务器生成虚拟环境：
```
#选择自己的版本
virtualenv --python=python3.10 myenv
```
进入虚拟环境：
```
source myenv/bin/activate
```
进入到django4blog项目文件夹：
```
cd django4blog
```
输入如下命令安装项目必要的Python库。
```
pip3 install -r requirements.txt
```
接着分别输入如下命令完成静态资源收集和数据迁移。
```
python3 manage.py collectstatic
python3 manage.py migrate
```
至此，我们部署针对开发和代码这部分的工作已经结束了。

## Nginx配置
接下来就是启用Nginx并配置相关代理。

首先我们把Nginx的默认配置和连接文件default先删除。

分别进入/etc/nginx/sites-available，/etc/nginx/sites-enabled两个文件夹输入命令：

sudo rm -r default删除default文件。
```
cd /etc/nginx/sites-available
rm -f default

/etc/nginx/sites-enabled
rm -f default
```
然后我们进入/etc/nginx/sites-available新建一个我们自己的配置文件：django4blog
```
cd /etc/nginx/sites-available
vim django4blog
```
输入如下配置内容：
```
server {
  charset utf-8;
  listen 80;
  server_name 39.107.240.223;  # 改成你的 IP
 
  location /static {
    #注意，这个路径是前面执行python3 manage.py collectstatic时提示的路径
    alias /root/django_project/django4blog/collected_static;
  }
 
  location / {
    proxy_set_header Host $host;
    proxy_pass http://unix:/tmp/39.107.240.223.socket;  # 改成你的 IP
  }
}
```
:wq 保存退出后执行下面命令
```
sudo ln -s /etc/nginx/sites-available/django4blog /etc/nginx/sites-enabled
```
进入nginx配置文件
```
cd /etc/nginx
vim nginx.conf
```
将第一行的 user www-data; 修改成 user root;

最后刷新下Nginx配置信息：
```
service nginx reload
```

## 准备后台用户以及启用Gunicorn
先回到项目所在的目录cd django_project/django4blog，并且进入虚拟环境，输入命令创建一个超级账户：
```
python manage.py createsuperuser
```
然后安装gunicorn：
```
pip3 install gunicorn
```
启动gunicorn，注意修改为自己的公网地址和自己的项目名称。
```
gunicorn --bind unix:/tmp/39.107.240.223.socket django4blog.wsgi:application
```

## 测试及运行
回到本地系统中，在浏览器输入地址：服务器IP地址。39.107.240.223

接着我们登录后台 39.107.240.223/admin 添加几条数据。

## 文件说明
### 项目的每个文件说明如下：
    manage.py：命令行工具，内置多种方式与项目进行交互。在命令提示符窗口下，将路径切换到django4blog项目并输入python manage.py help，可以查看该工具的指令信息。
    __init__.py：初始化文件，一般情况下无须修改。
    asgi.py：用于启动异步通信服务，比如实现在线聊天等异步通信功能。
    settings.py：项目的配置文件，项目的所有功能都需要在该文件中进行配置。
    urls.py：项目的路由设置，设置网站的具体网址内容。
    wsgi.py：全称为Python Web Server Gateway Interface，即Python服务器网关接口，是Python应用与Web服务器之间的接口，用于Django项目在服务器上的部署和上线，一般不需要修改。
### article文件夹下又包含5个.py文件。每个文件说明如下：
    __init__.py：初始化文件，一般情况下无须修改。
    admin.py：后台管理的配置文件 , 后期我们的可以通过他管理我们的model和数据库。
    apps.py：django菜单文件。
    models.py：模型文件，用于创建模型和数据库表的映射关系，用于项目和数据库之间的数据处理。
    views.py：视图文件，用于实现我们具体的Web请求和返回响应。
    tests.py：测试文件
