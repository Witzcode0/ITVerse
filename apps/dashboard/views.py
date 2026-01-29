from django.shortcuts import render, redirect
from django.contrib import messages
from apps.users.models import User
from apps.master.utils.inputValidator import *
# Create your views here.
def login(request):
    return render(request, "dashboard/login.html")

def register(request):
    if request.method == "POST":
        user_type_ = request.POST['user_type']
        email_ = request.POST['email']
        mobile_ = request.POST['mobile']
        pancard_ = request.FILES['pancard']
        password_ = request.POST['password']
        confirm_password_ = request.POST['confirm_password']
        
        if not is_valid_email(email_):
            messages.error(request, "Invalid email")
            return redirect("register")
        
        if User.objects.filter(email=email_).exists():
            messages.error(request, "Email already exist")
            return redirect("register")
        
        if not is_valid_mobile(mobile_):
            messages.error(request, "Invalid mobile")
            return redirect("register")
        
        if User.objects.filter(mobile=mobile_).exists():
            messages.error(request, "Mobile already exist")
            return redirect("register")

        print("1", match_password(password_, confirm_password_))
        if not match_password(password_, confirm_password_)[0]:
            messages.error(request, f"{match_password(password_, confirm_password_)[1]}")
            return redirect("register")
        
        print("2", validate_password(password_))
        print("3", not validate_password(password_)[0])
        if not validate_password(password_)[0]:
            print("4",not validate_password(password_)[0])
            messages.error(request, f"{validate_password(password_)[1]}")
            return redirect("register")
        
        new_user = User.objects.create(
            user_type=user_type_,
            email=email_,
            mobile=mobile_,
            pancard=pancard_,
            password=password_
        )
        new_user.save()
        return redirect("login")

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