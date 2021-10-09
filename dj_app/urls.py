from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('',views.dashboard, name= 'dashboard'),
    path('register/', views.register, name = 'register'),
    path('otp/', views.otp, name='otp'),
    path('logout/',views.logout,name='logout'),
    path('profile', views.profile, name='profile'),
    path('delete1/<int:pk>',views.delete1,name='delete1'),
    path('forgot1/',views.forgot1,name='forgot1'),
    path('forgot2/',views.forgot2,name='forgot2'),
    path('forgot3/',views.forgot3,name='forgot3'),
    path('addtest/',views.addtest,name='addtest'),
    path('managetest/', views.managetest, name='managetest'),
    path('newap/',views.new_appointment, name='newap'),
    path('report/', views.report, name='report'),
    path('viewreguser/', views.viewreg_user, name='viewreguser'),
    path('edittest/<int:pk>', views.edittest, name='edittest'),
]