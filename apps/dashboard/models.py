from django.db import models
from apps.master.models import BaseClass
# Create your models here.

class Contact(BaseClass):
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False)
    mobile = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField()
