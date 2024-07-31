from django.http import HttpRequest
import nested_admin

from django import forms
from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from rangefilter.filters import DateRangeFilter
from django.contrib.admin import DateFieldListFilter
from django.conf import settings
from django_reverse_admin import ReverseModelAdmin

from management.admin import ExportAdminMixin
from master.forms import BaptismFilterForm, RoleFilterForm, DummyForm, FormExportRole, FormExportBaptism
from master.adminInline import FamilyInline, CongregationInline, BaptismInline, ServantOfGodInline, EmployeeInline, UserInline
from master.models import Location, Master, Congregation, Family, Baptism,ServantOfGod, Employee, Gallery
from master.filter import FullNameFilter , PhoneNumberFilterMaster, MasterFullNameFilter, AddressFilter, ChineseNameFilter, MemberNumberFilter, AliasNameFilter, MasterAddressFilter, MasterGenderFilter, PhoneNumberFilter, EmployeeNIKFilter2
from master.resources_export import MasterResource, CongregationResource, BaptismResource, ServantOfGodResource, EmployeeResource
from django.db.models.functions import ExtractYear, ExtractMonth
from master.utils import date_hierarchy_drilldown
from core.widgets import DateInput
from django.db import models


class LocationAdmin(nested_admin.NestedModelAdmin):    
    list_per_page = settings.LIST_PER_PAGE
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', )
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {'fields': (('name', 'created_at', 'updated_at'),)}),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'name':
            field.widget.attrs['class'] = 'form-control w-100'
        return field
    
    def render_change_form(self, request, context, *args, **kwargs):
        context.update({
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, *args, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.name = obj.name.upper()
        super().save_model(request, obj, form, change)

admin.site.register(Location, LocationAdmin)

class MasterAdmin(FormExportRole, ReverseModelAdmin):
    form = DummyForm    
    list_per_page = settings.LIST_PER_PAGE
    list_display = ('full_name', 'gender', 'phone_number', 'address',)
    date_hierarchy = 'created_at'
    search_fields = ('full_name', 'phone_number', 'address',)
    autocomplete_fields = ('location', 'user', 'nonstructural') 
    inlines = [FamilyInline, CongregationInline,  BaptismInline, ServantOfGodInline, EmployeeInline]
    list_filter = (
        FullNameFilter,
        PhoneNumberFilterMaster,
        AddressFilter,
        ("date_of_birth", DateFieldListFilter),
    )
    resource_class = MasterResource
    inline_type = 'stacked'
    inline_reverse = [
        {
            'field_name': 'user',
            'admin_class': UserInline
        }
    ]
    export_form_class = RoleFilterForm
    ordering = ('-created_at',)
   
    fieldsets = (
        ('Main', {
            'fields': (
                ('full_name', 
                'gender'), 
                ('address',
                'personal_identity'),
                ('blood_type',
                'marital_status'),
                'profile_photo',    
                ('location', "phone_number"
                ),
                ('date_of_birth', 'date_of_death'),
            ),
            'classes': ( 
                'baton-tabs-init',
                'baton-tab-group-fs-Congregation--inline-Congregation',
                'baton-tab-group-ServantOfGod--inline-ServantOfGod',
                'baton-tab-group-Employee--inline-Employee',
                'baton-tab-fs-nonstructural',
                'baton-tab-group-fs-Family--inline-Family',
                'baton-tab-group-Baptism--inline-Baptism',
                'baton-tab-fs-content',
                ),
        }),
        ('Gallery', {
            'fields': ('dummy_field',),
            'classes': ('tab-fs-content', ),
        }),
        ('Non Structural', {
            'fields': ('nonstructural',),
            'classes': ('tab-fs-nonstructural', ),
        })
    )
    formfield_overrides = {
        models.DateField: {'widget': DateInput},
    }
    baton_form_includes = [
        ('views/htmx.html', 'dummy_field', 'bottom'),
    ]
    date_hierarchy_drilldown = False

    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = Master.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)

    def get_form(self, request, obj=None, **kwargs):
        form = super(MasterAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['dummy_field'].widget = forms.HiddenInput()
        form.base_fields['dummy_field'].label = ''  
        return form
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['full_name', 'gender', 'blood_type', 'marital_status', 'address', 'personal_identity', 'phone_number']:
            field.widget.attrs['class'] = 'form-control w-100'
        if db_field.name in ['date_of_birth', 'date_of_death']:
            attributes_to_remove = ['size']
            for attr in attributes_to_remove:
                field.widget.attrs.pop(attr, None)
            field.widget.attrs['class'] = 'vDateField w-100'
        return field

    def render_change_form(self, request, context, *args, **kwargs):
        context.update({
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, *args, **kwargs)
    
    def save_model(self , request, obj, form, change):
        if change:
            if obj.profile_photo and obj.profile_photo.name:
                previous_obj = Master.objects.get(pk=obj.pk)
                print(previous_obj.profile_photo)
                if previous_obj.profile_photo != obj.profile_photo:
                    if previous_obj.profile_photo: 
                        Gallery.objects.create(masteruser=obj, photo=previous_obj.profile_photo)
                    else:
                        pass
        super().save_model(request, obj, form, change)

admin.site.register(Master, MasterAdmin)

class CongregationProxyAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ( 'number_member','masteruser' ,'alias_name', 'chinese_name', 'address' )
    date_hierarchy = 'created_at'
    list_filter = (
        MasterFullNameFilter,
        AliasNameFilter,
        ChineseNameFilter,
        MemberNumberFilter,
        MasterAddressFilter,
    )
    resource_class = CongregationResource
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('masteruser__full_name',)
    date_hierarchy_drilldown = False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request ):
        return False
    
    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data =  Congregation.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)
    
    @admin.display(ordering='member_number', description='Nomor Anggota Jemaat')
    def number_member(self, obj):
        url = reverse_lazy('admin:master_master_change', args=[obj.masteruser_id])
        full_url = f"{url}#group-fs-Congregation--inline-Congregation"
        obj = obj.member_number
        return mark_safe(u'<a href="%s">%s</a>' % (full_url, obj))

    @admin.display(ordering='masteruser__address', description='Alamat')
    def address(self, obj):
        return obj.masteruser.address
    
    admin_add_url = reverse_lazy('admin:master_master_add')
    
admin.site.register(Congregation, CongregationProxyAdmin)

class FamilyProxyAdmin(nested_admin.NestedModelAdmin):
    list_display = ('full_name', 'status', 'family')
    list_per_page = settings.LIST_PER_PAGE
    date_hierarchy = 'created_at'
    search_fields = ('masteruser__full_name',)
    date_hierarchy_drilldown = False

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request ):
        return False
    
    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = Family.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)

    @admin.display(ordering='masteruser__full_name', description='Nama Lengkap')
    def full_name(self, obj):
        url = reverse_lazy('admin:master_master_change', args=[obj.masteruser_id])
        full_url = f"{url}#group-fs-Family--inline-Family"
        return mark_safe(u'<a href="%s" class="fw-bold">%s</a>' % (full_url, obj.masteruser.full_name))

    admin_add_url = reverse_lazy('admin:master_master_add')

admin.site.register(Family, FamilyProxyAdmin)

class BaptismProxyAdmin(FormExportBaptism, admin.ModelAdmin):
    list_display = ('full_name', 'baptism_date' ,'status')
    date_hierarchy = 'created_at'
    list_per_page = settings.LIST_PER_PAGE
    export_form_class = BaptismFilterForm
    list_filter = (
        MasterFullNameFilter,
        MasterAddressFilter,
        MasterGenderFilter,
        ('baptism_date', DateRangeFilter),
    )
    search_fields = ('masteruser__full_name',)
    resource_class = BaptismResource
    date_hierarchy_drilldown = False

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request ):
        return False

    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = Baptism.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)

    @admin.display(ordering='masteruser__full_name', description='Nama Lengkap') 
    def full_name(self, obj):
        url = reverse_lazy('admin:master_master_change', args=[obj.masteruser_id])
        full_url = f"{url}#group-Baptism--inline-Baptism"
        return mark_safe(u'<a href="%s" class="fw-bold">%s</a>' % (full_url, obj))
    
    admin_add_url = reverse_lazy('admin:master_master_add')

admin.site.register(Baptism, BaptismProxyAdmin)

class ServantOfGodProxyAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('number_member', 'masteruser', 'ordination', 'pastor', 'church', )
    date_hierarchy = 'created_at'
    list_filter = (
        MasterFullNameFilter,
        MasterAddressFilter,
    )
    search_fields = ('masteruser__full_name',)
    list_per_page = settings.LIST_PER_PAGE
    resource_class = ServantOfGodResource
    date_hierarchy_drilldown = False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request ):
        return False
    
    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = ServantOfGod.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)

    @admin.display(ordering='member_number', description='Nomor Anggota Jemaat')
    def number_member(self, obj):
        url = reverse_lazy('admin:master_master_change', args=[obj.masteruser_id])
        full_url = f"{url}#group-ServantOfGod--inline-ServantOfGod"
        return mark_safe(u'<a href="%s" class="fw-bold">%s</a>' % (full_url, obj.member_number))
    
    admin_add_url = reverse_lazy('admin:master_master_add')
    
admin.site.register(ServantOfGod, ServantOfGodProxyAdmin)

class EmployeeProxyAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('no' ,'masteruser','phone_number', 'start_date', 'employee_position')
    date_hierarchy = 'created_at'
    list_filter = (
        MasterFullNameFilter,
        EmployeeNIKFilter2,
        ('start_date', DateRangeFilter),
        PhoneNumberFilter,
    )
    search_fields = ('masteruser__full_name',)
    list_per_page = settings.LIST_PER_PAGE
    resource_class = EmployeeResource
    date_hierarchy_drilldown = False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request ):
        return False

    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = Employee.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)
    
    @admin.display(ordering='masteruser__phone_number', description='No HP')
    def phone_number(self, obj):
        return obj.masteruser.phone_number

    @admin.display(ordering='nik', description='Nomor ID Karyawan')
    def no(self, obj):
        url = reverse_lazy('admin:master_master_change', args=[obj.masteruser_id])
        full_url = f"{url}#group-Employee--inline-Employee"
        return mark_safe(u'<a href="%s" class="fw-bold">%s</a>' % (full_url, obj.nik))


    admin_add_url = reverse_lazy('admin:master_master_add')
    
admin.site.register(Employee, EmployeeProxyAdmin)

class GalleryProxyAdmin(nested_admin.NestedModelAdmin):
    list_display = ('full_name',  'photo_thumbnail' )
    date_hierarchy = 'created_at'
    date_hierarchy_drilldown = False
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('masteruser__full_name',)

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request ):
        return False
    
    def get_date_hierarchy_drilldown(self, year_lookup, month_lookup):
        years_with_data = Gallery.objects.annotate(
            year_created=ExtractYear('created_at'),
            month_created=ExtractMonth('created_at')
        ).values('year_created', 'month_created').distinct()

        return date_hierarchy_drilldown(years_with_data, year_lookup, month_lookup)

    @admin.display(ordering='masteruser__full_name', description='Nama Lengkap')
    def full_name(self, obj):
        url = reverse_lazy('admin:master_master_change', args=[obj.masteruser_id])
        full_url = f"{url}#fs-content"
        return mark_safe(u'<a href="%s" class="fw-bold">%s</a>' % (full_url, obj))
    
    @admin.display(ordering='photo', description='Foto')
    def photo_thumbnail(self, obj):
        base_url = settings.MEDIA_URL
        url = base_url + obj.photo
        if obj.photo:
            return mark_safe(f'<a href="{url}">{url}</a>')
        return "No Photo"

    
    admin_add_url = reverse_lazy('admin:master_master_add')

admin.site.register(Gallery, GalleryProxyAdmin)
