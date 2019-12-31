# Django2.2.4 实战 - 天天生鲜项目

## 前言
本项目采用django2.2.4版本，因为原项目采用框架版本为django1.8，所以踩了很多坑，特别是django1.x和2.x版本之间的坑，特此记录，希望对各位有所帮助。
同时，该项目包含了实际开发电商项目大部分的功能和知识点，是一个非常不错的django练手项目。

## 开发环境
```
python: 3.5
django: 2.2.4
celery: 4.3.0
django-haystack: 2.8.1
django-redis: 4.10.0
django-tinymce: 2.6.0
itsdangerous: 1.1.0
jieba: 0.39
Pillow: 6.1.0
PyMySQL: 0.9.3
redis: 3.3.7
requests: 2.22.0
Whoosh: 2.7.4
```

## 实现的功能
- [x] 用户模块
  - [x] 注册
  - [x] 登录
  - [x] 激活(celery)
  - [x] 退出
  - [x] 个人中心
  - [x] 地址管理
- [x] 商品模块
  - [x] 首页(celery)
  - [x] 商品详情
  - [x] 商品列表
  - [x] 搜索功能(haystack+whoosh)
- [x] 购物车模块(redis)
  - [x] 增加
  - [x] 删除
  - [x] 修改
  - [x] 查询
- [x] 订单模块
  - [x] 确认订单页面
  - [x] 订单创建
  - [x] 请求支付(支付宝)
  - [x] 查询支付结果
  - [x] 评论
  
## 踩过的坑
### 项目框架搭建
- [Django报错 __init__() missing 1 required positional argument 'on_delete'](https://blog.csdn.net/jiangxunzhi123/article/details/86160146)
- [Django2.0异常：Specifying a namespace in include() without providing an app_name is not supported.](https://blog.csdn.net/zoulonglong/article/details/79612973)
- [天天生鲜 (fields.E210) Cannot use ImageField because Pillow is not installed.](http://www.iamnancy.top/post/247/)
- [天天生鲜 ?: (2_0.W001) Your URL pattern '^' has a route that contains '(?P<', begins with a '^', or ends](http://www.iamnancy.top/post/248/)
- [Django2.2报错——AttributeError: ''str'' object has no attribute ''decode''](https://blog.csdn.net/qq_36274515/article/details/89043481)

### 注册基本逻辑
- [django2.x报错No module named 'django.core.urlresolvers'](https://blog.csdn.net/weixin_35757704/article/details/78977753)
- [天天生鲜 The included URLconf 'dailyfresh.urls' does not appear to have any patterns in it.](http://www.iamnancy.top/admin/blog/post/250/)

### django内置函数发送激活邮件
- [天天生鲜 smtplib.SMTPDataError: (554, b'DT:SPM 163 smtp13](http://www.iamnancy.top/admin/blog/post/251/)

### 登录基本逻辑
- [天天生鲜 用户登录逻辑 user = authenticate(username=username, password=password)一直返回None](http://www.iamnancy.top/admin/blog/post/252/)

### FastDFS的安装和配置
- [Failed to start fdfs_trackerd.service: Unit fdfs_trackerd.service not found.](https://blog.csdn.net/u014179267/article/details/87970521)
- [Django出现Error: 111 connect to 192.168.158.141:22122. Connection refused](https://blog.csdn.net/chenhua1125/article/details/80112716)

### Nginx配合FastDFS使用的安装和配置
- [ubuntu下安装nginx错误error: the HTTP rewrite module requires the PCRE library 解决方法](https://blog.csdn.net/u014723529/article/details/45874705)

### python和FastDFS交互
```
ImportError: No module named 'mutagen'
ImportError: No module named 'requests'
```
解决：
```
（venv） $ pip install mutagen
（venv） $ pip install requests
```

### 首页获取购物车商品数目
- [TypeError: 'bool' object is not callable](https://www.cnblogs.com/weixuqin/p/9298746.html)

### 其他
- [AttributeError: 'QuerySet' object has no attribute 'total_price'](https://www.cnblogs.com/niuli1987/p/10186239.html)
