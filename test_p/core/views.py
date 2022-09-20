from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest

# Create your views here.

@login_required(login_url="signin")
def index(request):
    return render(request, "index.html")
    
def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user=user)
            return redirect('index')
        
        messages.info(request, "user not found")
    
    return render(request, "signin.html")
    
@login_required(login_url="signin")
def signout(request):
    logout(request)
    return render(request, "signout.html")
    
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        
        if not get_user_model().objects.filter(email=email).exists():
            user = get_user_model().objects.create_user(
                    username=username, 
                    password=password, 
                    email=email)
            user.save()
        
            login(request, user=user)
            return redirect('index')
        
        messages.info(request, "username already taken")
        return redirect('register')
    
    return render(request, "register.html")
    
def invite(request: HttpRequest, code):
    return HttpResponse(code)
