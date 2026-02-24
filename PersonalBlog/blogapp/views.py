from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseForbidden

# Create your views here.
def Dashboard(request):
    return render(request,"dashboard.html")

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('passoword')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "You logged in")
            return redirect('dashboard')
        else:
            messages.error(request,"Invalid username and password")
            return redirect('login')
    return render(request,"login.html")

def add_user(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You are not authorized to access this page")

