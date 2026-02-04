from django.contrib import admin
from apps.users.models import User, Services, companyProfile, socialLinks
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_filter = ["is_active"]

admin.site.register(User, UserAdmin)

admin.site.register(Services)
admin.site.register(companyProfile)
admin.site.register(socialLinks)