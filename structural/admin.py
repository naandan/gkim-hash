from django.contrib import admin
from django_mptt_admin.django_mptt_admin_mixin import DjangoMpttAdminMixin
from structural.models import Structural, PriodeStructural, NonStructural
from admin_auto_filters.filters import AutocompleteFilter
from django_mptt_admin.admin import DjangoMpttAdmin
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from uuid import UUID
from django.contrib import messages
from django.conf import settings
from management.admin import ExportAdminMixin
from structural.resources_export import NonStructuralResource
from core.widgets import DateInput
from django.db import models
from django.http import HttpResponse

class PriodeFilter(AutocompleteFilter):
    title = 'Periode'
    field_name = 'periode'

class StructuralAdmin(DjangoMpttAdmin):
    list_display = ('name', 'parent', 'masteruser', 'periode',)
    list_display_links = ('name',)
    autocomplete_fields = ('parent', 'masteruser', 'periode')
    search_fields = ('name',)
    list_per_page = settings.LIST_PER_PAGE
    list_filter = ('periode',)
    fieldsets = (
        (None, {
            "fields": (
                ('name', 'parent'), ('masteruser', 'periode'),
            ),
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['name']:
            field.widget.attrs['class'] = 'form-control w-100'
        return field
    
    def _prepare_view(self, request, extra_context=None):
        latest_period = PriodeStructural.objects.order_by('-created_at').first()
        if latest_period is None:
            self.message_user(request, "Belum ada periode yang tersedia.", level=messages.WARNING)
            return super().changelist_view(request, extra_context)

        selected_period_id = request.GET.get('periode__id__exact')
        if isinstance(selected_period_id, list):
            try:
                selected_period_id = UUID(selected_period_id[0]) 
            except (ValueError, TypeError, IndexError):
                selected_period_id = None
        elif isinstance(selected_period_id, str):
            try:
                selected_period_id = UUID(selected_period_id)
            except ValueError:
                selected_period_id = None
        else:
            selected_period_id = None

        if not selected_period_id:
            q = request.GET.copy()
            q['periode__id__exact'] = str(latest_period.id)
            request.GET = q
            request.META['QUERY_STRING'] = request.GET.urlencode()

        empty_periods = PriodeStructural.objects.filter(Structural__isnull=True).exclude(
            id=selected_period_id if selected_period_id else latest_period.id
        )

        self.custom_button = [
            {'link': '', 'name': 'Copy Data', 'childlinks': True, 'periods': empty_periods, 'source_period_id': selected_period_id if selected_period_id else latest_period.id},
            {'link': f'/structural/tree-structural/{selected_period_id if selected_period_id else latest_period.id}/', 'name': 'Lihat Bagan', 'type' : 'htmx', 'target' : '#changelist'},
        ]

        extra_context = extra_context or {}
        extra_context['custom_button'] = self.custom_button

        return extra_context, selected_period_id if selected_period_id else latest_period.id

    def _handle_ajax_post(self, request):
        source_period_id = request.POST.get('source_period_id')
        target_period_id = request.POST.get('target_period_id')

        try:
            source_period = PriodeStructural.objects.get(id=source_period_id)
            target_period = PriodeStructural.objects.get(id=target_period_id)

            structural_objects = Structural.objects.filter(periode=source_period)

            for structural_obj in structural_objects:
                structural_obj.pk = None 
                structural_obj.periode = target_period
                structural_obj.tree_id = structural_obj.tree_id + 1
                structural_obj.save()  

            return JsonResponse({'success': True, 'message': 'Data berhasil disalin'})

        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'message': 'Periode tidak ditemukan'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Terjadi kesalahan: {type(e).__name__}: {e}'})

    def grid_view(self, request, extra_context=None):
        result = self._prepare_view(request, extra_context)
        if isinstance(result, HttpResponse):
            return result
        extra_context, _ = result

        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return self._handle_ajax_post(request)

        return super().grid_view(request, extra_context)

    def changelist_view(self, request, extra_context=None):
        result = self._prepare_view(request, extra_context)
        if isinstance(result, HttpResponse):
            return result
        extra_context, _ = result

        if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return self._handle_ajax_post(request)

        return super().changelist_view(request, extra_context=extra_context)

    def render_change_form(self, request, context, *args, **kwargs):
        context.update({
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, *args, **kwargs)

admin.site.register(Structural, StructuralAdmin)

class PriodeStructuralAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'created_at', 'updated_at')
    search_fields = ('name', )
    list_per_page = settings.LIST_PER_PAGE
    formfield_overrides = {
        models.DateField: {'widget': DateInput},
    }
    fieldsets = (
        (None, {
            "fields": (
                ('name', 'start_date', 'end_date'),
            ),
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name in ['start_date', 'end_date']:
            attributes_to_remove = ['size']
            for attr in attributes_to_remove:
                field.widget.attrs.pop(attr, None)
            field.widget.attrs['class'] = 'vDateField w-100'
        if db_field.name in ['name']:
            field.widget.attrs['class'] = 'w-100'
        return field

    def render_change_form(self, request, context, *args, **kwargs):
        context.update({
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, *args, **kwargs)

admin.site.register(PriodeStructural, PriodeStructuralAdmin)

class NonStructuralAdmin(ExportAdminMixin, admin.ModelAdmin):
    list_display = ('role', 'created_at', 'updated_at')
    resource_class = NonStructuralResource
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('role', )
    fieldsets = (
        (None, {
            "fields": (
                ('role'),
            ),
        }),
    )

    def render_change_form(self, request, context, *args, **kwargs):
        context.update({
            'show_save_and_continue': False
        })
        return super().render_change_form(request, context, *args, **kwargs)

admin.site.register(NonStructural, NonStructuralAdmin)