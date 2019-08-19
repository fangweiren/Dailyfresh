from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from apps.user.views import RegisterView, ActiveView, LoginView, UserInfoView, UserOrderView, AddressView

app_name = 'user'
urlpatterns = [
    path('register', RegisterView.as_view(), name='register'), # 注册
    path('login', LoginView.as_view(), name='login'), # 登录
    re_path('active/(?P<token>.*)', ActiveView.as_view(), name='active'), # 用户激活

    path('', login_required(UserInfoView.as_view()), name='user'), # 用户中心-信息页
    path('order', login_required(UserOrderView.as_view()), name='order'), # 用户中心-订单页
    path('address', login_required(AddressView.as_view()), name='address'), # 用户中心-地址页
]
