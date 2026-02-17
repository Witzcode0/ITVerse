from django.urls import path
from apps.dashboard.views import *
from apps.dashboard.api import *

urlpatterns = [
    path('', index, name='index'),
    path("crud", crud, name="crud"),
    path("crud-record-delete/<uuid:record_id>", crud_record_delete, name="crud_record_delete"),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<uuid:user_id>/', reset_password, name='reset_password'),
    path('profile/', profile, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path("add-company", add_company, name="add_company"),
    path("remove_service/<uuid:service_id>/", remove_service, name="remove_service"),
    path("add_social_link/", add_social_link, name="add_social_link"),
     path("connections/", connections_view, name="connections"),
    path("connect/<uuid:receiver_id>/", send_request_view, name="send_request_view"),
    path("accept/<uuid:sender_id>/", accept_request_view, name="accept-request"),
    path("search_connections/", search_connections, name='search_connections'),
    path('logout/', logout, name='logout'),
    path('blog/', blog, name='blog'),
    path("blog-detail/<uuid:blog_id>", blog_detail, name="blog_detail"),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]