from django import forms
from import_export import resources
from import_export.admin import ExportForm
from management.models import ManagementOfWorship, ManagementPresence
from management.proxy_model import ManagementPresenceCongregationProxy, ManagementPresenceServantOfGodProxy, ManagementPresenceEmployeeProxy
class FromExport(ExportForm):
    start_date = forms.DateTimeField( label='Start Date',  widget=forms.DateInput(attrs={'type': 'date'}), required=False,)
    end_date = forms.DateTimeField( label='End Date',  widget=forms.DateInput(attrs={'type': 'date'}), required=False,)
    
    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date cannot be earlier than start date.")

        return cleaned_data

class PresenceResource(resources.ModelResource):
    class Meta:
        model = ManagementPresence
        fields = ('created_at', 'masteruser__full_name', 'worship__name', 'check_in', 'check_out', 'source')
        export_order = fields
        
    def get_export_headers(self):
        return ["Tanggal", 'Nama Lengkap', 'Ibadah', 'Check In', 'Check Out', 'Sumber']
    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    def dehydrate_source(self, obj):
        return obj.get_source_display()
    
class ManagementOfWorshipResource(resources.ModelResource):
    class Meta:
        model = ManagementOfWorship
        fields = ('created_at', 'name', 'start_time', 'end_time', 'location__name', 'type', 'status')
        export_order = fields
        
    def get_export_headers(self):
        return ["Tanggal", "Ibadah", 'Waktu Mulai', 'Waktu Selesai', 'Lokasi', 'Tipe', 'Status']
    def dehydrate_start_time(self, obj):
        return obj.start_time.strftime('%H:%M')
    def dehydrate_end_time(self, obj):
        return obj.end_time.strftime('%H:%M')
    def dehydrate_type(self, obj):
        return obj.get_type_display()
    def dehydrate_status(self, obj):
        status = obj.status
        if status:
            return "Aktif"
        else:
            return "Tidak Aktif"
    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    
class ManagementPresenceCongregationResource(resources.ModelResource):
    class Meta:
        model = ManagementPresenceCongregationProxy
        fields = ('created_at', 'masteruser__full_name', 'worship__name', 'check_in', 'check_out', 'source')
        export_order = fields
        
    def get_export_headers(self):
        return ["Tanggal", 'Pengurus Ibadah', 'Ibadah', 'Check In', 'Check Out', 'Sumber']
    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    def dehydrate_source(self, obj):
        return obj.get_source_display()

class ManagementPresenceServantOfGodResource(resources.ModelResource):
    class Meta:
        model = ManagementPresenceServantOfGodProxy
        fields = ('created_at', 'masteruser__full_name', 'worship__name', 'check_in', 'check_out', 'source')
        export_order = fields
        
    def get_export_headers(self):
        return ["Tanggal", 'Pengurus Ibadah', 'Ibadah', 'Check In', 'Check Out', 'Sumber']
    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    def dehydrate_source(self, obj):
        return obj.get_source_display()
    
class ManagementPresenceEmployeeResource(resources.ModelResource):
    class Meta:
        model = ManagementPresenceEmployeeProxy
        fields = ('created_at', 'masteruser__full_name', 'check_in', 'check_out', 'source', 'length_of_work')
        export_order = fields
        
    def get_export_headers(self):
        return ["Tanggal", 'Karyawan', 'Check In', 'Check Out', 'Sumber', 'Lama Kerja']
    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    def dehydrate_source(self, obj):
        return obj.get_source_display()