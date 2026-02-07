from django.db import models
from django.conf import settings
from apps.master.models import BaseClass
import os
import uuid

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

class Service(BaseClass):

    name = models.CharField(max_length=150, unique=True)

    # Which company suggested this service
    created_by_company = models.ForeignKey(
        "Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_services"
    )

    # Admin approval
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

def company_logo_upload_path(instance, filename):
    ext = filename.split('.')[-1]

    # temporary unique name (first upload)
    return f"company-logos/temp_{uuid.uuid4()}.{ext}"

class Company(BaseClass):

    contact_person = models.ForeignKey(User, on_delete=models.CASCADE)

    logo = models.ImageField(
        upload_to=company_logo_upload_path,
        default="default/company.png"
    )

    name = models.CharField(max_length=255)
    content = models.TextField()
    address = models.CharField(max_length=255)

    services = models.ManyToManyField(
        Service,
        related_name="companies",
        blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        # Track old logo
        old_logo = None
        if self.pk:
            try:
                old_logo = Company.objects.get(pk=self.pk).logo
            except Company.DoesNotExist:
                pass

        super().save(*args, **kwargs)  
        # Now instance has ID

        # 🔥 Skip if default image
        if not self.logo or "default/company.png" in self.logo.name:
            return

        ext = self.logo.name.split('.')[-1]
        new_name = f"company-logos/company_{self.id}.{ext}"
        new_path = os.path.join(settings.MEDIA_ROOT, new_name)

        # If already renamed → skip
        if self.logo.name == new_name:
            return

        # Delete existing file with same name
        if os.path.exists(new_path):
            os.remove(new_path)

        # Rename temp file
        if os.path.exists(self.logo.path):
            os.rename(self.logo.path, new_path)

        self.logo.name = new_name
        super().save(update_fields=["logo"])

        # Delete old logo (not default)
        if old_logo and old_logo.name != "default/company.png":
            old_path = os.path.join(settings.MEDIA_ROOT, old_logo.name)
            if os.path.exists(old_path):
                os.remove(old_path)
    
class socialLinks(BaseClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False, null=False)
    url = models.URLField()
    

class Connection(BaseClass):
    sender = models.ForeignKey(
        User,
        related_name="sent_requests",
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name="received_requests",
        on_delete=models.CASCADE
    )
    is_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("sender", "receiver")

    def __str__(self):
        return f"{self.sender.id} -> {self.receiver.id}"
