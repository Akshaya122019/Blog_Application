from django.urls import path
from . import views

urlpatterns = [
    path('',views.Dashboard,name='dashboard'),
    
    path('login/',views.LoginView,name='login'),
    path('logout',views.LogoutUser, name='logout'),

    path('Add_User/', views.add_user, name='add_user'),
    path('update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('User/', views.show_user, name='user'),

    path('add_blog',views.Add_Blog, name='add_blog'),
    path('blog_list',views.Blog_list, name='blog_list'),
    path('blogs',views.Blogs, name='blogs'),
   
]