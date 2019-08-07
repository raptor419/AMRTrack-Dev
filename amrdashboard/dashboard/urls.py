from dashboard import views
from django.conf import settings
from django.views.static import serve
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static



urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('active/', views.active, name='active'),
    path('google_login/', views.google_login, name='active'),
    path('addpath/', views.pathtestcreate, name='addpath'),
    path('viewdata/', views.view_data, name='viewdata'),
    path('viewdataraw/', views.view_data_raw, name='viewdataraw'),
    path('fullabg/', views.complete_antibiogram, name='fullabg'),
    path('explore/', views.exploraotry_analysis, name='explore'),
]
