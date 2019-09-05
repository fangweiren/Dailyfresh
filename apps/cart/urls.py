from django.urls import path
from .views import CartAddView, CartInfoView

urlpatterns = [
    path('add', CartAddView.as_view(), name='add'),  # 购物车记录添加
    path('', CartInfoView.as_view(), name='show'),  # 购物车页面显示
]
