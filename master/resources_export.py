from import_export import resources
from master.models import Master, Congregation, Baptism, ServantOfGod, Employee

class MasterResource(resources.ModelResource):
    class Meta:
        model = Master
        fields = ( 'created_at', 'full_name', 'gender', 'address', 'personal_identity', 'blood_type', 'marital_status', 'profile_photo', 'location__name', 'user__username',)
        export_order = fields

    def get_export_headers(self):
        return ['Tanggal', 'Nama Lengkap', 'Jenis Kelamin', 'Alamat', 'NIK', 'Golongan Darah', 'Status Perkawinan', 'Foto Profil', 'Lokasi', 'Username']

    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    def dehydrate_gender(self, obj):
        return obj.get_gender_display()
    def dehydrate_blood_type(self, obj):
        return obj.get_blood_type_display()
    def dehydrate_marital_status(self, obj):
        return obj.get_marital_status_display()

class CongregationResource(resources.ModelResource):
    class Meta:
        model = Congregation
        fields = ('created_at', 'masteruser__full_name', 'member_number', 'alias_name', 'chinese_name', 'worship__name',)
        export_order = fields

    def get_export_headers(self):
        return ['Created At', 'Master User', 'Member Number', 'Alias Name', 'Chinese Name', 'Worship',]
    
    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    
    
class BaptismResource(resources.ModelResource):
    class Meta:
        model = Baptism
        fields = ('created_at', 'masteruser__full_name', 'baptism_date', 'status', 'location__name',)
        export_order = fields
    
    def get_export_headers(self):
        return ['Created At', 'Master User', 'Member Number', 'Baptism Date', 'Status',]
    
    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    def dehydrate_status(self, obj):
        return obj.get_status_display()
    
class ServantOfGodResource(resources.ModelResource):
    class Meta:
        model = ServantOfGod
        fields = ('created_at', 'masteruser__full_name', 'member_number', 'ordination', 'pastor', 'church', 'membership_status',)
        export_order = fields

    def get_export_headers(self):
        return ['Created At', 'Master User', 'Member Number', 'Tanggal Bapstis', 'Pendeta', 'Gereja', 'Membership Status',]
    
    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    def dehydrate_membership_status(self, obj):
        return 'Aktif' if obj.membership_status else 'Tidak Aktif'
    
class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = ('created_at','masteruser__full_name', 'nik', 'religion', 'bpjs_employment', 'bpjs_health', 'account_number', 'employee_position', 'start_date',)
        export_order = fields

    def get_export_headers(self):
        return ['Tanggal', 'Master User', 'NIK', 'Agama', 'BPJS Kesehatan', 'BPJS Ketenagakerjaan', 'Nomor Rekening', 'Jabatan', 'Tanggal Mulai',]
    
    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d')
    
    def dehydrate_start_date(self, obj):
        return obj.start_date.strftime('%Y-%m-%d')
    
    def dehydrate_religion(self, obj):
        return obj.get_religion_display()