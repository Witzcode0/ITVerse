from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, "dashboard/login.html")
def register(request):
    return render(request, "dashboard/register.html")
def forgot_password(request):
    return render(request, "dashboard/forgot_password.html")
def reset_password(request):
    return render(request, "dashboard/reset_password.html")

def index(request):
    return render(request, "dashboard/index.html")

def blog(request):
    return render(request, "dashboard/blog.html")

def about(request):
    return render(request, "dashboard/about.html")

def contact(request):
    return render(request, "dashboard/contact.html")