from django.urls import path
from . import views
from .views import initiate_payment, callback

urlpatterns = [
    path('index', views.index, name='index'),
    path('apbook',views.apbook,name='apbook'),
    path('u-register/',views.u_register,name='u-register'),
    path('uotp/', views.uotp, name='uotp'),
    path('login/', views.u_login, name='u-login'),
    path('u-logout/', views.u_logout, name='u-logout'),
    path('viewtdetails/', views.view_testdetails, name='viewtdetails'),
    path('', views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),
]