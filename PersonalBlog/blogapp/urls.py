from django.urls import path
from . import views

urlpatterns = [
    path('',views.Dashboard,name='dashboard'),
    path('login/',views.LoginView,name='login')
   
]