from django.urls import path
from apps.dashboard.api import *

urlpatterns = [
    path("contacts/", contactListAPI, name="contactListAPI"),
    path("contact/<uuid:contact_id>", contactDetailAPI, name="contactDetailAPI"),
]