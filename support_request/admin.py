from django.contrib import admin
from .models import ClientList, SectorRegionList, MyRequest


class MyRequestAdmin(admin.ModelAdmin):
    list_display = ( 'first_name', 'last_name', 'request_category', 'directorate', 'client', 'other_client', 'requested_date_from', 'requested_date_to', 'date_request_submitted')
    list_display_links = ('first_name', 'last_name', 'request_category', 'directorate', 'client',)
    readonly_fields = ()
    ordering = ('-requested_date_from',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class ClientListAdmin(admin.ModelAdmin):
    list_display = ('name', 'regional_office')
    list_display_links = ('name',)
    readonly_fields = ()
    ordering = ('-regional_office',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(ClientList, ClientListAdmin)
admin.site.register(SectorRegionList)
admin.site.register(MyRequest, MyRequestAdmin)