from django.urls import path
from .views import OrderPlaceView

urlpatterns = [
    path('place', OrderPlaceView.as_view(), name='place'),  # 提交订单页面显示
]
