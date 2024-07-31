from django.contrib import admin
from django.conf import settings
from warta.models import Warta, Announcement
from master.utils import date_hierarchy_drilldown
from django.db.models.functions import ExtractYear, ExtractMonth
from warta.resources_export import WartaResource, AnnouncementResource

from django.template.defaultfilters import truncatechars

class WartaAdmin( admin.ModelAdmin):
    list_display = ('created_at', 'truncated_name', 'file', 'status', 'order')  
    date_hierarchy = 'created_at'
    search_fields = ('name', )
    resource_class = WartaResource
    list_per_page = settings.LIST_PER_PAGE
    date_hierarchy_drilldown = False

    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = Warta.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)

    @admin.display(ordering='name', description='Nama Warta')
    def truncated_name(self, obj):
        return truncatechars(obj.name, 50)
    
    def render_change_form(self, request, context, *args, **kwargs):
        context.update({
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, *args, **kwargs)  

admin.site.register(Warta, WartaAdmin)


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('files','name','url', 'status', 'order_display')
    date_hierarchy = 'created_at'
    search_fields = ('name', )
    resource_class = AnnouncementResource
    list_per_page = settings.LIST_PER_PAGE
    date_hierarchy_drilldown = False

    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = Announcement.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)

    def files(self, obj):
        if obj.file:
            return obj.file
        else:
            return obj.name
    files.short_description = 'File'

    def order_display(self, obj):
        return obj.order

    def render_change_form(self, request, context, *args, **kwargs):
        context.update({
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, *args, **kwargs)

admin.site.register(Announcement, AnnouncementAdmin)
