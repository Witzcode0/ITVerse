from django.urls import path
from apps.dashboard.views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<uuid:user_id>/', reset_password, name='reset_password'),
    path('profile/', profile, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path("add-company", add_company, name="add_company"),
    path('logout/', logout, name='logout'),
    path('blog/', blog, name='blog'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact')
]