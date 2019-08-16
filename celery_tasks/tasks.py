# -*- coding: utf-8 -*-
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import time
import os
import django

# django环境初始化(在任务处理者一端加)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()

# 创建celery类的实例对象
app = Celery('celery_tasks.tasks', broker='redis://192.168.37.133:6379/8')


# 定义任务函数
@app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email, sender]
    html_message = '<h1>%s，欢迎你成为天天生鲜注册会员。</h1><br/>请点击下面链接激活您的账户<a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
        username, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)
