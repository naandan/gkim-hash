import random

from django.db import models
from core.widgets import TimeInput
from django.contrib import admin
from django.conf import settings
from master.constans import TypeOfWorship
from master.utils import date_hierarchy_drilldown

from management.adminInline import ManagementPresenceDetailInline
from django.db.models.functions import ExtractYear, ExtractMonth
from rangefilter.filters import DateRangeFilter,DateTimeRangeFilter
from management.models import ManagementOfWorship, ManagementPresence, RFIDCard
from management.proxy_model import ManagementPresenceCongregationProxy, ManagementPresenceServantOfGodProxy, ManagementPresenceEmployeeProxy
from management.forms import MasterAutocomplatedCongregation, MasterAutocomplatedEmployee, MasterAutocomplatedServant, ManagementOfWorshipForm, ExportAdminMixin, FormExportAdminMixin
from management.resources_export import PresenceResource, FromExport, ManagementOfWorshipResource, ManagementPresenceCongregationResource, ManagementPresenceServantOfGodResource, ManagementPresenceEmployeeResource
from master.filter import LocationFilter, TypeManagementOfWorshipFilter, ManagementOfWorshipFilter, MasterFullNameFilter,CongregationAliasNameFilter, CongregationMemberNumberFilter, CongregationChineseNameFilter, WorshipNameFilter, MasterGenderFilter, ServantMemberNumberFilter, ServantMembershipStatusFilter, EmployeeNIKFilter, CongregationFullNameFilter

class ManagementOfWorshipAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'type', 'day_worship')
    list_filter = (TypeManagementOfWorshipFilter, ManagementOfWorshipFilter, ('start_time', DateRangeFilter), LocationFilter)
    search_fields = ('name',"location__name",)
    autocomplete_fields = ('location', 'pendeta')
    date_hierarchy = 'created_at'
    list_per_page = settings.LIST_PER_PAGE
    form = ManagementOfWorshipForm
    resource_class = ManagementOfWorshipResource
    date_hierarchy_drilldown = False
    formfield_overrides = {
        models.TimeField: {'widget': TimeInput},
    }

    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = ManagementOfWorship.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)

    def get_fieldsets(self, request, obj=None):
        fields = (('name','pendeta'), ('start_time', 'end_time'), ('location',  'type'), ('status', 'day_worship'))
        if obj is not None and obj.type != TypeOfWorship.OFFLINE:
            fields += ('qrcode',) 
        return ((None, {'fields': fields}),)

    def start_time(self, obj):
        return obj.start_time.strftime("%H:%M:%S")

    def end_time(self, obj):
        return obj.end_time.strftime("%H:%M:%S")

    start_time.short_description = 'Start Time'
    end_time.short_description = 'End Time'

    def save_model(self, request, obj, form, change):
        if not obj.qrcode:
            obj.qrcode = ''.join(str(random.randint(0, 9)) for _ in range(8))
        super().save_model(request, obj, form, change)
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['name', 'type', 'day_worship']:
            field.widget.attrs['class'] = 'form-control w-100'
        return field 

    def render_change_form(self, request, context, *args, **kwargs):
        context.update({
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, *args, **kwargs)

admin.site.register(ManagementOfWorship, ManagementOfWorshipAdmin)


class ManagementPresenceCongregationProxyAdmin(FormExportAdminMixin, admin.ModelAdmin):
    list_display = ('masteruser', 'created_at', 'worship',  'check_in','tag', "keterangan")
    date_hierarchy = 'created_at'
    autocomplete_fields = ('worship',)
    form = MasterAutocomplatedCongregation
    export_form_class = FromExport
    resource_class = ManagementPresenceCongregationResource
    list_per_page = settings.LIST_PER_PAGE
    ordering = ('-created_at',)
    list_filter = (
        CongregationMemberNumberFilter,
        MasterFullNameFilter,
        CongregationAliasNameFilter,
        CongregationChineseNameFilter,
        WorshipNameFilter,
        ('created_at', DateTimeRangeFilter)
    )   
    fieldsets = (
        ("", {
            "fields": (
                ('masteruser','worship',),
                ('check_in',
                'check_out'),
                ('source', 'present')
                
            ),
        }),
    )
    date_hierarchy_drilldown = False

    @admin.display(ordering='present')
    def keterangan(self, obj):
        if obj.present:
            return 'Hadir'
        else:
            return 'Tidak Hadir'

    keterangan.short_description = 'Keterangan'
        

    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = ManagementPresenceCongregationProxy.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['check_in', 'check_out']:
            field.widget.attrs['class'] = 'DateFlatpickrInput form-control w-100'
        if db_field.name in ['source']:
            field.widget.attrs['class'] = 'responsive-field'
        return field 
    
    def render_change_form(self, request, context, *args, **kwargs):
        context.update({
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, *args, **kwargs)
admin.site.register(ManagementPresenceCongregationProxy, ManagementPresenceCongregationProxyAdmin)

class MangementPresenceServantOfGodProxyAdmin(FormExportAdminMixin, admin.ModelAdmin):
    list_display = ('masteruser', 'created_at', 'worship', 'check_in', 'check_out')
    date_hierarchy = 'created_at'
    autocomplete_fields = ('worship',)
    form = MasterAutocomplatedServant
    export_form_class = FromExport
    resource_class = ManagementPresenceServantOfGodResource
    list_per_page = settings.LIST_PER_PAGE
    ordering = ('-created_at',)
    list_filter = (
        MasterFullNameFilter,
        ServantMemberNumberFilter,
        MasterGenderFilter,
        ServantMembershipStatusFilter,
        ('created_at', DateTimeRangeFilter)
    )
    fieldsets = (
        ("", {
            "fields": (
                ('masteruser','worship',),
                ('check_in',
                'check_out'),
                'source',
            ),
        }),
    )
    date_hierarchy_drilldown = False

    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = ManagementPresenceServantOfGodProxy.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['check_in', 'check_out']:
            field.widget.attrs['class'] = 'DateFlatpickrInput form-control w-100'
        if db_field.name in ['source']:
            field.widget.attrs['class'] = 'responsive-field'
        return field
    
    def render_change_form(self, request, context, *args, **kwargs):
        context.update({
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, *args, **kwargs)
    
admin.site.register(ManagementPresenceServantOfGodProxy, MangementPresenceServantOfGodProxyAdmin)

class ManagementPresenceEmployeeProxyAdmin(FormExportAdminMixin, admin.ModelAdmin):
    list_display = ('masteruser','check_in', 'check_out', 'long_work')
    date_hierarchy = 'created_at'
    autocomplete_fields = ('worship',)
    form = MasterAutocomplatedEmployee
    export_form_class = FromExport
    resource_class = ManagementPresenceEmployeeResource
    inlines = [ManagementPresenceDetailInline]
    list_per_page = settings.LIST_PER_PAGE
    ordering = ('-created_at',)
    list_filter = (
        EmployeeNIKFilter,
        MasterFullNameFilter,
        MasterGenderFilter,
        ('created_at', DateTimeRangeFilter)
    )
    fieldsets = (
        ("Main", {
            "fields": (
                ('masteruser','source'),
                ('check_in',
                'check_out'),
            ),
             "classes": ('baton-tabs-init', 'baton-tab-inline-ManagementPresenceDetail',),
        }),
    )
    date_hierarchy_drilldown = False

    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = ManagementPresenceEmployeeProxy.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['check_in', 'check_out']:
            field.widget.attrs['class'] = 'DateFlatpickrInput form-control w-100'
        if db_field.name in ['source']:
            field.widget.attrs['class'] = 'form-control w-100'
        return field
    
    def render_change_form(self, request, context, *args, **kwargs):
        context.update({
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, *args, **kwargs)

    @admin.display( description='Lama Kerja', ordering='length_of_work')
    def long_work(self, obj):
        return f"{obj.length_of_work} jam"
    
admin.site.register(ManagementPresenceEmployeeProxy, ManagementPresenceEmployeeProxyAdmin)

class ManagementPresenceAdmin(FormExportAdminMixin, admin.ModelAdmin):
    list_display = ('masteruser', 'worship', 'check_in', 'check_out', 'created_at')
    date_hierarchy = 'created_at'
    autocomplete_fields = ('masteruser', 'worship',)
    search_fields = ('masteruser__full_name', )
    list_per_page = settings.LIST_PER_PAGE
    list_filter = (
        MasterFullNameFilter,
        ('created_at', DateTimeRangeFilter)
    )
    ordering = ('-created_at',)
    fieldsets = (
        ("", {
            "fields": (
                ('masteruser','worship',),
                ('check_in',
                'check_out'),
                'source',
            ),
        }),
    )
    date_hierarchy_drilldown = False

    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = ManagementPresence.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)

    resource_class = PresenceResource
    export_form_class = FromExport
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['check_in', 'check_out']:
            field.widget.attrs['class'] = 'DateFlatpickrInput form-control w-100'
        if db_field.name in ['source']:
            field.widget.attrs['class'] = 'responsive-field'
        return field
    
    def render_change_form(self, request, context, *args, **kwargs):
        context.update({
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, *args, **kwargs)
    
admin.site.register(ManagementPresence, ManagementPresenceAdmin)

class RFIDCardAdmin(admin.ModelAdmin):
    list_display = ('masteruser','id_rfid', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    search_fields = ('masteruser__masteruser__full_name', )
    autocomplete_fields = ('masteruser',)
    list_filter = (
        CongregationFullNameFilter,
        ('created_at', DateTimeRangeFilter)
    )
    custom_button = [
            {'link': '#', 'name': 'Registrasi RFID', },
        ]
    date_hierarchy_drilldown = False

    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = RFIDCard.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)

admin.site.register(RFIDCard, RFIDCardAdmin)