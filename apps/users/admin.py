from django.contrib import admin
from apps.users.models import User, Service, Company, socialLinks, Connection
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "fullname", "email", "mobile", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["user_type","fullname", "email", "mobile" ]
    list_editable = ["fullname", "email", "mobile", "is_active"]
    list_per_page = 1

admin.site.register(User, UserAdmin)

admin.site.register(Service)
admin.site.register(Company)
admin.site.register(socialLinks)
admin.site.register(Connection)