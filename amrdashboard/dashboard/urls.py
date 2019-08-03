from dashboard import views
from django.urls import path

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('active/', views.active, name='active'),
    path('google_login/', views.google_login, name='active'),
    path('addpath/', views.pathtestcreate, name='addpath'),
    path('viewdata/', views.view_data, name='viewdata'),
    path('viewdataraw/', views.view_data_raw, name='viewdataraw'),
]
