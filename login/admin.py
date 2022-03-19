from django.contrib import admin
from login.models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'last_login', 'is_admin', )
    readonly_fields = ('date_joined', 'last_login')
    search_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
