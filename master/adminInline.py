from django.db import models
from django.contrib import admin
from core.widgets import DateInput

from django.contrib.auth.models import User
from master.forms import FormPassword
from master.models import Congregation, Family, Baptism, ServantOfGod, Employee

class FamilyInline(admin.TabularInline):    
    model = Family
    extra = 0
    fk_name = 'masteruser'
    autocomplete_fields = ('family',)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ["status", "family"]:
            field.widget.attrs['class'] = 'form-control w-100'
        return field

class CongregationInline(admin.StackedInline):
    model = Congregation
    autocomplete_fields = ('worship',)
    fieldsets = (
        (None, {
            "fields": (
                ('member_number', 'alias_name'),
                ('chinese_name', 'worship'),
                ('is_congregation', ),
            ),
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['member_number', 'alias_name', 'chinese_name']:
            field.widget.attrs['class'] = 'form-control w-100'
        return field

class BaptismInline(admin.StackedInline):
    model = Baptism
    extra = 0
    fk_name = 'masteruser'
    autocomplete_fields = ('congregation', 'location')
    fieldsets = (
        (None, {
            "fields": (
                ('congregation', 'status'), ('baptism_date', 'location'),
            ),
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['baptism_date']:
            attributes_to_remove = ['size']
            for attr in attributes_to_remove:
                field.widget.attrs.pop(attr, None)
            field.widget.attrs['class'] = 'dateFlatpickrInput w-100'
        if db_field.name in ['pendeta', 'status']:
            field.widget.attrs['class'] = 'form-control w-100'
        return field

class ServantOfGodInline(admin.StackedInline):
    model = ServantOfGod
    fk_name = 'masteruser'
    autocomplete_fields = ('pastor',)
    fieldsets = (
        (None, {
            "fields": (
                ('member_number', 'church',),
                ('pastor',  'ordination'),
                ('membership_status', 'is_servant_of_god'),
            ),
        }),
    )


    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['ordination']:
            attributes_to_remove = ['size']
            for attr in attributes_to_remove:
                field.widget.attrs.pop(attr, None)
            field.widget.attrs['class'] = 'dateFlatpickrInput w-100'
        if db_field.name in ['member_number', 'church', 'pastor']:
            field.widget.attrs['class'] = 'form-control w-100'
        return field

class EmployeeInline(admin.StackedInline):
    model = Employee

    fieldsets = (
        (None, {
            "fields": (
                ('nik', 'religion'), 
                ('bpjs_employment', 'bpjs_health'),
                ('account_number', 'employee_position'),
                ('start_date',"out_of_work" )
                ,'is_employee',
            ),
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['start_date', 'out_of_work']:
            attributes_to_remove = ['size']
            for attr in attributes_to_remove:
                field.widget.attrs.pop(attr, None)
            field.widget.attrs['class'] = 'dateFlatpickrInput w-100'
        if db_field.name in ['nik', 'religion', 'bpjs_employment', 'bpjs_health', 'account_number', 'employee_position']:
            field.widget.attrs['class'] = 'form-control w-100'
        return field

class UserInline(admin.StackedInline):
    model = User
    form = FormPassword
    fieldsets = (
        (None, {
            "fields": (
                ('username', 'email'), ('password', 'groups'), ('is_staff', 'is_active', 'is_superuser'), 
            ),
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['username', 'email', 'groups']:
            field.widget.attrs['class'] = 'form-control w-100'
        return field
