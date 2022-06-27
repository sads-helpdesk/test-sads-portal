from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    list_display = ('full_name', 'email', 'username', 'phone_number', 'regional_office_sector', 'unit', 'date_joined', 'is_superadmin', 'is_active')
    list_display_links = ('email', 'full_name', 'regional_office_sector', 'unit')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)




