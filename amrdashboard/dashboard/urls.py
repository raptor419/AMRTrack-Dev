from django.conf.urls import url, include
from django.urls import path

from dashboard import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
	path('active/', views.index, name='active'),    
]