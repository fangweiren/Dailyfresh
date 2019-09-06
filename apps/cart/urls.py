from django.urls import path
from .views import CartAddView, CartInfoView, CartUpdateView

urlpatterns = [
    path('add', CartAddView.as_view(), name='add'),  # 购物车记录添加
    path('update', CartUpdateView.as_view(), name='update'),  # 购物车记录更新
    path('', CartInfoView.as_view(), name='show'),  # 购物车页面显示
]
