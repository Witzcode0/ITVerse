from django.db import models
from django.conf import settings
from apps.master.models import BaseClass
import os

# Create your models here.

def pancard_upload_path(instance, filename):
    ext = filename.split('.')[-1]  
    filename = f"{instance.id}.{ext}"
    return os.path.join("users_pancards", filename)

def profile_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"user_{instance.id}.{ext}"
    return os.path.join("user-profiles", filename)


class User(BaseClass):
    USER_TYPE_CHOICES = (
        ("buyer", "Buyer"),
        ("seller", "Seller"),
    )
    user_type = models.CharField(max_length=50, null=False, blank=False, choices=USER_TYPE_CHOICES)
    profile = models.ImageField(upload_to=profile_upload_path, default="defaults/user.png")
    fullname = models.CharField(max_length=200, null=True, blank=True, default="-")
    email = models.EmailField(max_length=100, null=False, blank=False, unique=True)
    mobile = models.CharField(max_length=100, null=False, blank=False, unique=True)
    pancard = models.FileField(upload_to=pancard_upload_path, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        # delete old image
        if self.pk:
            try:
                old_user = User.objects.get(pk=self.pk)

                if old_user.profile != self.profile:

                    # NEVER delete default
                    if (
                        old_user.profile and
                        "defaults/user.png" not in old_user.profile.name and
                        os.path.isfile(old_user.profile.path)
                    ):
                        os.remove(old_user.profile.path)

            except User.DoesNotExist:
                pass


        super().save(*args, **kwargs)  # FIRST SAVE


        # ✅ SKIP DEFAULT IMAGE
        if not self.profile:
            return

        if "defaults/user.png" in self.profile.name:
            return


        # rename only if needed
        ext = self.profile.name.split('.')[-1]
        new_filename = f"user-profiles/user_{self.id}.{ext}"
        new_filepath = os.path.join(settings.MEDIA_ROOT, new_filename)

        # avoid renaming again
        if self.profile.path == new_filepath:
            return

        # ensure folder exists
        os.makedirs(os.path.dirname(new_filepath), exist_ok=True)

        # rename
        if os.path.exists(self.profile.path):
            os.rename(self.profile.path, new_filepath)

            self.profile.name = new_filename
            super().save(update_fields=['profile'])

class Services(BaseClass):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)

def company_logo_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"company_{instance.id}.{ext}"
    return os.path.join("company-logos", filename)

class companyProfile(BaseClass):
    contact_person = models.ForeignKey(User, on_delete=models.CASCADE)
    services = models.ForeignKey(Services, on_delete=models.CASCADE)

    logo = models.ImageField(
        upload_to=company_logo_upload_path,
        default="default/company.png"
    )

    name = models.CharField(max_length=255)
    content = models.TextField()
    address = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):

        # Get old logo before saving
        try:
            old_logo = companyProfile.objects.get(pk=self.pk).logo
        except companyProfile.DoesNotExist:
            old_logo = None

        super().save(*args, **kwargs)  # Save first to get ID

        # Rename file AFTER ID exists
        if self.logo and not self.logo.name.startswith(f"company-logos/company_{self.id}"):

            ext = self.logo.name.split('.')[-1]
            new_name = f"company-logos/company_{self.id}.{ext}"
            new_path = os.path.join(settings.MEDIA_ROOT, new_name)

            # Delete if file already exists
            if os.path.exists(new_path):
                os.remove(new_path)

            os.rename(self.logo.path, new_path)

            self.logo.name = new_name
            super().save(update_fields=['logo'])

        # Delete old logo
        if old_logo and old_logo.name != self.logo.name:
            if old_logo.name != "default/company.png":
                old_path = os.path.join(settings.MEDIA_ROOT, old_logo.name)
                if os.path.exists(old_path):
                    os.remove(old_path)
    
class socialLinks(BaseClass):
    company = models.ForeignKey(companyProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    url = models.URLField()
    

