from django.db import models
from apps.master.models import BaseClass
from apps.users.models import User
# Create your models here.

class Contact(BaseClass):
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False)
    mobile = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField()

def blog_image_upload_path(instance, filename):
    # uploads to MEDIA_ROOT/blogs/<category>/<filename>
    return f"blogs/{filename}"

class Blog(BaseClass):
    author =  models.ForeignKey(User, related_name="blogs", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=blog_image_upload_path, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        ordering = ["-id"]   # latest first

    def __str__(self):
        return self.title
    
class Task(BaseClass):
    title = models.CharField(max_length=255)
    content = models.TextField()
    