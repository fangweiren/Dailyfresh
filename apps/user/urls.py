from django.urls import path, re_path
from apps.user.views import RegisterView, ActiveView, LoginView

app_name = 'user'
urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),  # 注册
    path('login', LoginView.as_view(), name='login'),  # 登录
    re_path('active/(?P<token>.*)', ActiveView.as_view(), name='active'),  # 用户激活
]
