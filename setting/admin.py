from django.contrib import admin
from django.http import HttpRequest
from django.urls.resolvers import URLPattern
from setting.models import Setting
from django.db.models import Model
from django.urls import path

class SettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj: Model | None = None) -> bool:
        return False
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(self.change_view), name='setting_change'),
        ]
        return custom_urls + urls

    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        obj = Setting.objects.first()  
        if not extra_context:
            extra_context = dict()
        extra_context['skip_object_list_page'] = True
        extra_context['show_save_and_continue'] = False 
        return super().change_view(request, str(obj.id), form_url, extra_context)

admin.site.register(Setting, SettingAdmin)