from io import BytesIO
from django import forms
from dal import autocomplete
from master.models import Master
from openpyxl import load_workbook
from tempfile import NamedTemporaryFile

from import_export.admin import ExportMixin
from django.utils.safestring import mark_safe
from management.models import RFIDCard, ManagementOfWorship
from management.proxy_model import ManagementPresenceCongregationProxy, ManagementPresenceServantOfGodProxy, ManagementPresenceEmployeeProxy

class ManagementOfWorshipForm(forms.ModelForm):
    class Meta:
        model = ManagementOfWorship
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and end_time < start_time:
            raise forms.ValidationError(mark_safe("<p class='alert alert-danger'>Waktu terakhir tidak boleh lebih awal dari waktu pertama.</p>"))
        
        return cleaned_data

class ExportAdminMixin(ExportMixin):
    def export_action(self, request, *args, **kwargs):
        response = super().export_action(request, *args, **kwargs)
        if response.has_header and 'Content-Disposition' in response:
            wb = load_workbook(filename=BytesIO(response.content))
            ws = wb.active
            ws.auto_filter.ref = ws.dimensions
            with NamedTemporaryFile() as tmp:
                wb.save(tmp.name)
                tmp.seek(0)
                response.content = tmp.read()
        return response
    
class FormExportAdminMixin(ExportAdminMixin):
    def get_export_queryset(self, request):
        queryset = super().get_export_queryset(request)

        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date and end_date > start_date:
            try :
                queryset = queryset.filter(created_at__date__range=[start_date, end_date]).order_by('-created_at')
            except ValueError:
                raise forms.ValidationError("Start date must be before end date.")
        

        self.resource_class.export_queryset = queryset
        return queryset
    

class MasterCongregation(autocomplete.Select2QuerySetView):
   def get_queryset(self):
        queryset = Master.objects.all()
        queryset = queryset.filter(Congregation__is_congregation=True)
        return queryset
   
class MasterServant(autocomplete.Select2QuerySetView):
   def get_queryset(self):
        queryset = Master.objects.all()
        queryset = queryset.filter(ServantOfGod__is_servant_of_god=True)
        return queryset
   
class MasterEmployee(autocomplete.Select2QuerySetView):
   def get_queryset(self):
        queryset = Master.objects.all()
        queryset = queryset.filter(Employee__is_employee=True)
        return queryset
   
class MasterAutocomplatedCongregation(forms.ModelForm):
    class Meta:
        model = ManagementPresenceCongregationProxy
        fields = '__all__'
        widgets = {
            'masteruser': autocomplete.ModelSelect2(url='master-autocomplete'),
        }
        labels = {
            'masteruser': 'Pilih Jemaat',
        }

class MasterAutocomplatedServant(forms.ModelForm):
    class Meta:
        model = ManagementPresenceServantOfGodProxy
        fields = '__all__'
        widgets = {
            'masteruser': autocomplete.ModelSelect2(url='master-autocomplete2')
        }
        labels = {
            'masteruser': 'Pilih Hamba Tuhan',
        }

class MasterAutocomplatedEmployee(forms.ModelForm):
    class Meta:
        model = ManagementPresenceEmployeeProxy
        fields = '__all__'
        widgets = {
            'masteruser': autocomplete.ModelSelect2(url='master-autocomplete3')
        }
        labels = {
            'masteruser': 'Pilih Karyawan',
        }

class RFIDCardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['masteruser'].queryset = self.fields['masteruser'].queryset.filter(
            is_congregation=True
        )
        self.fields['masteruser'].widget.attrs.update({'class': 'js-example-basic-single form-control d-none'})

    class Meta:
        model = RFIDCard
        fields = ['id_rfid', 'masteruser']
        widgets = {
            'id_rfid': forms.TextInput(attrs={'class': 'form-control w-100'}),
        }