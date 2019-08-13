from django.urls import path
from apps.user import views

app_name = 'user'
urlpatterns = [
    path('register', views.register, name='register'),
]
