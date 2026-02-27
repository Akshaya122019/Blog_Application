from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.
@login_required
def Dashboard(request):
    return render(request,"dashboard.html")


def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "You logged in")
            return redirect('dashboard')
        else:
            messages.error(request,"Invalid username and password")
            return redirect('login')
    return render(request,"login.html")

@login_required
def add_user(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You are not authorized to access this page")
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password']
        confirm = request.POST['confirm']
        role = request.POST['role']

        if password != confirm:
            messages.error(request,"Password do not match")
            return redirect('add_user')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        
        user = User.objects.create_user(username=username, email=email, password=password)

        if role == 'admin':
            group, _ = Group.objects.get_or_create(name='Admin')
        elif role == 'user':
            group, _ = Group.objects.get_or_create(name='User')
        else:
            messages.warning(request, "Invalid role selected")
            return redirect('add_user')
        
        user.groups.add(group)

        messages.success(request, f"Account created successfully as {role.capitalize()}")
        return redirect('user')
    
    return render(request, 'add_user.html')

def show_user(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You are not authorized to access this page")
    
    users = User.objects.all()
    is_admin = request.user.groups.filter(name='Admin').exists()

    return render(request, 'view_user.html', {"users":users, "is_admin":is_admin})

@login_required
def LogoutUser(request):
    logout(request)
    return redirect("login")

@login_required
def update_user(request, user_id):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You are not authorized to access this page")
    
    user = get_object_or_404(User,id=user_id)
    current_role = user.groups.first().name if user.groups.exists() else "User"

    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()

        new_role = request.POST['role']
        user.groups.clear()
        group, _ = Group.objects.get_or_create(name=new_role)
        user.groups.add(group)

        messages.success(request, "User Updated Successfully")
        return redirect('user')
    return render(request, 'update_user.html', {'user': user, 'user_role': current_role})

@login_required
def delete_user(request, user_id):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('user')

@login_required
def Add_Blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog added successfully")
            return redirect('blog_list')
        else:
            messages.error(request,"Something wrong")
    else:
        form = BlogForm()
    return render(request,"add_blog.html", {'form':form})

@login_required
def Blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog_list.html', {'blogs':blogs})

@login_required
def Blogs(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blogs.html', {'blogs':blogs})

@login_required
def blog_detail(request,slug):
    blog = Blog.objects.get(url=slug)
    return render(request, "blog_detail.html", {'blog':blog})
