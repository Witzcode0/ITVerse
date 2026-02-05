from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from apps.users.models import User, Company, socialLinks, Service
from apps.master.utils.inputValidator import *
# Create your views here.

def login_required(view_func):
    def wrapper(request, *args, **kwargs):

        user_id = request.session.get("user_id")

        if not user_id:
            messages.error(request, "Please login first.")
            return redirect("login")

        return view_func(request, *args, **kwargs)

    return wrapper

def login(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        password_ = request.POST['password']

        if not is_valid_email(email_):
            messages.error(request, "Invalid email")
            return redirect("login")
        
        if not User.objects.filter(email=email_).exists():
            messages.error(request, "Email or Password dose not match")
            return redirect("login")
        
        get_user = User.objects.get(email=email_)
        user_password = check_password(password_, get_user.password)

        if not (user_password):
            messages.error(request, "Email or Password dose not match")
            return redirect("login")
        
        if not get_user.is_active:
            messages.error(request, "Your account is currently inactive. Please contact the administrator for activation.")
            return redirect("login")
        
        request.session["user_id"] = str(get_user.id)
        return redirect("index")
        
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
            password=make_password(password_)
        )
        new_user.save()
        messages.success(
            request,
            "Registration successful! Your application is under review. We will notify you once it is approved."
        )
        return redirect("login")

    return render(request, "dashboard/register.html")

def forgot_password(request):
    if request.method == "POST":
        email_ = request.POST['email']

        if not is_valid_email(email_):
            messages.error(request, "Invalid email")
            return redirect("forgot_password")
        
        if not User.objects.filter(email=email_).exists():
            messages.error(request, "Email does not exist.")
            return redirect("forgot_password")
        
        get_user = User.objects.get(email=email_)
        
        domain = get_current_site(request).domain
        reset_link = f"http://{domain}/reset-password/{get_user.id}/"
        
        subject = "Reset Your Password - ITVERSE"
        message = f"""
        Hello User,

        We received a request to reset your password for your ITVERSE account.

        Click the link below to reset your password:
        {reset_link}

        If you did not request this, please ignore this email.

        ⚠️ This link will expire soon for security reasons.

        Regards,  
        ITVERSE Team
        """
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [f"{email_}"]
        send_mail(subject, message, from_email, recipient_list)
        
        get_user = User.objects.get(email=email_)



    return render(request, "dashboard/forgot_password.html")

def reset_password(request, user_id):
    context = {
        "user_id":user_id
    }
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Invalid reset link.")
        return redirect("login")
    else:
        if request.method == "POST":
            new_password_ = request.POST["new_password"]
            confirm_password_ = request.POST["confirm_password"]
          
            if not match_password(new_password_, confirm_password_)[0]:
                messages.error(request, f"{match_password(new_password_, confirm_password_)[1]}")
                return render(request, "dashboard/reset_password.html", context)
            
            if not validate_password(new_password_)[0]:
                messages.error(request, f"{validate_password(new_password_)[1]}")
                return render(request, "dashboard/reset_password.html", context)
        
            user.password = make_password(new_password_)
            user.save()
            messages.success(request, "Password reset successfully.")
            return redirect("login")
    
    return render(request, "dashboard/reset_password.html", context)

@login_required
def profile(request):
    user_id_ = request.session["user_id"]
    get_user = User.objects.get(id=user_id_)
    # Get company (if exists)
    company = Company.objects.filter(contact_person=user_id_).first()

    # All services for dropdown
    services = Service.objects.filter(is_approved=True, created_by_company=company)
    print(company.services.filter(is_approved=True))

    # print(services)
    # Social links
    social_links = socialLinks.objects.filter(user=user_id_)

    context = {
        "user": get_user,
        "company": company,
        "services": services,
        "social_links": social_links,
    }

    return render(request, "dashboard/profile.html", context)

@login_required
def update_profile(request):
     if request.method == "POST":

        user_id_ = request.session["user_id"]
        get_user = User.objects.get(id=user_id_)

        fullname_ = request.POST.get("fullname")
        email_ = request.POST.get("email")
        mobile_ = request.POST.get("mobile")
        profile_ = request.FILES.get("profile")  # SAFE

        # update fields
        get_user.fullname = fullname_
        get_user.email = email_
        get_user.mobile = mobile_

        # only update image if new uploaded
        if profile_:
            get_user.profile = profile_

        get_user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile")
def logout(request):
    del request.session["user_id"]
    messages.success(request, "Now, you are logged Out.")
    return redirect("login")

@login_required
def add_company(request):
    user = request.session["user_id"]
    get_user = User.objects.get(id=user)
    company, created = Company.objects.get_or_create(
        contact_person=get_user
    )

    if request.method == "POST":

        company.name = request.POST.get("name", "").strip()
        company.address = request.POST.get("address", "").strip()
        company.content = request.POST.get("content", "").strip()

        if request.FILES.get("logo"):
            company.logo = request.FILES["logo"]

        company.save()

        """
        ✅ SERVICES (Handles both existing + new automatically)
        """

        service_names = request.POST.getlist("services[]")

        service_objects = []

        for name in service_names:

            name = name.strip().title()

            if not name:
                continue

            service, created = Service.objects.get_or_create(
                name=name,
                defaults={
                    "created_by_company": company,
                    "is_approved": False
                }
            )

            service_objects.append(service)

        # Replace old services safely
        company.services.set(service_objects)

        messages.success(request, "Company profile updated successfully 🚀")

        return redirect("profile")

    # ✅ Only approved services for suggestions
    services = Service.objects.filter(is_approved=True).order_by("name")

    context = {
        "user":get_user,
        "company": company,
        "services": services,
        "company_services": company.services.all()  # preselected chips
    }

    return render(request, "dashboard/profile.html", context)

@login_required
def add_social_link(request):
    user_id_ = request.session["user_id"]
    if request.method == "POST":

        name = request.POST.get("name")
        url = request.POST.get("url")

        socialLinks.objects.create(
            user=user_id_,
            name=name,
            url=url
        )

        messages.success(request, "Social link added ✅")

        return redirect("profile")

    return redirect("profile")

def index(request):
    return render(request, "dashboard/index.html")

def blog(request):
    return render(request, "dashboard/blog.html")

def about(request):
    return render(request, "dashboard/about.html")

def contact(request):
    return render(request, "dashboard/contact.html")