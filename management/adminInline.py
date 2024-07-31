from django.contrib import admin
from management.models import ManagementPresenceDetail

class ManagementPresenceDetailInline(admin.TabularInline):
    model = ManagementPresenceDetail
    extra = 0
    
    def worship_name(self, obj):
        return obj.presence.worship.name
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['check_in', 'check_out']:
            field.widget.attrs['class'] = 'InlineDateFlatpickrInput form-control w-100'
        return field
    