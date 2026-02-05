from django.contrib import admin
from apps.users.models import User, Service, Company, socialLinks
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_filter = ["is_active"]

admin.site.register(User, UserAdmin)

admin.site.register(Service)
admin.site.register(Company)
admin.site.register(socialLinks)