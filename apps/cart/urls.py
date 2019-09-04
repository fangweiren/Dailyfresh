from django.urls import path
from .views import CartAddView

urlpatterns = [
    path('add', CartAddView.as_view(), name='add'),  # 购物车记录添加
]
