from django.contrib import admin
from Home.models import Organization, EmployeeSignup, Query, RFIDCard

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')
    search_fields = ('name', 'email')
    list_filter = ('name',)
    ordering = ('id',)
    actions = ['custom_delete_selected']

    def custom_delete_selected(self, request, queryset):
        # Delete objects without creating deletion LogEntry records.
        queryset.delete()
    custom_delete_selected.short_description = "Delete selected Organizations (without logging)"

@admin.register(EmployeeSignup)
class EmployeeSignupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'date_joined', 'get_unique_id')
    search_fields = ('name', 'email', 'unique_id', 'date_joined')
    list_filter = ('date_joined',)
    ordering = ('-date_joined',)
    date_hierarchy = 'date_joined'
    actions = ['custom_delete_selected']

    def get_unique_id(self, obj):
        return obj.unique_id  
    get_unique_id.short_description = 'Unique ID'

    def custom_delete_selected(self, request, queryset):
        queryset.delete()
    custom_delete_selected.short_description = "Delete selected EmployeeSignups (without logging)"

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'query', 'visibility', 'created_at')
    search_fields = ('query', 'visibility')
    list_filter = ('visibility', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    actions = ['custom_delete_selected']

    def custom_delete_selected(self, request, queryset):
        queryset.delete()
    custom_delete_selected.short_description = "Delete selected Queries (without logging)"

@admin.register(RFIDCard)
class RFIDCardAdmin(admin.ModelAdmin):
    list_display = ("card_uid", "scanned_at")
    search_fields = ("card_uid",)