from admin_auto_filters.filters import AutocompleteFilter, AutocompleteSelect
from baton.admin import InputFilter, MultipleChoiceListFilter
from master.constans import Gender, TypeOfWorship

class FullNameFilter(InputFilter):
   parameter_name = 'full_name'
   title = 'Nama Lengkap'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter(full_name__icontains=self.value())
       return queryset
class PhoneNumberFilterMaster(InputFilter):
   parameter_name = 'phone_number'
   title = 'No HP'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter(phone_number__icontains=self.value())
       return queryset
   
class PhoneNumberFilter(InputFilter):
   parameter_name = 'phone_number'
   title = 'No HP'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter(masteruser__phone_number__icontains=self.value())
       return queryset

class AddressFilter(InputFilter):
   parameter_name = 'address'
   title = 'Alamat'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter(address__icontains=self.value())
       return queryset

class MasterFullNameFilter(InputFilter) :
  title = 'Nama Lengkap'
  parameter_name = "masteruser.full_name"

  def queryset(self, request, queryset):
      if self.value() is not None:
          return queryset.filter(masteruser__full_name__icontains=self.value())
      return queryset

class CongregationFullNameFilter(InputFilter):
    title = 'Nama Lengkap'
    parameter_name = "masteruser.masteruser.full_name"

    def queryset(self, request, queryset):
      if self.value() is not None:
          return queryset.filter(masteruser__masteruser__full_name__icontains=self.value())
      return queryset

class MasterAddressFilter(InputFilter):
    title = 'Alamat'
    parameter_name = 'masteruser.address' 

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(masteruser__address__icontains=self.value())
        return queryset

class MemberNumberFilter(InputFilter):
   parameter_name = 'member_number'
   title = 'Nomor anggota'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter(member_number__icontains=self.value())
       return queryset

class AliasNameFilter(InputFilter):
   parameter_name = 'alias_name'
   title = 'Nama Alias'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter(alias_name__icontains=self.value())
       return queryset

class ChineseNameFilter(InputFilter):
   parameter_name = 'chinese_name'
   title = 'Nama Cina'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter(chinese_name__icontains=self.value())
       return queryset

class MasterGenderFilter(MultipleChoiceListFilter):
   title = 'Jenis kelamin'
   parameter_name = 'masteruser.gender'

   def lookups(self, request, model_admin):
        return Gender.choices
   
   def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(masteruser__gender=value)
        return queryset

# for management

class ManagementOfWorshipFilter(InputFilter):
   parameter_name = 'name'
   title = 'Nama'


   def queryset(self, request, queryset):
        if self.value() is not None:
            search_term = self.value()
            return queryset.filter(
                name__icontains=search_term
            )
   
class LocationFilter(AutocompleteFilter):
   field_name = 'location'
   title = 'Lokasi Gereja'

class TypeManagementOfWorshipFilter(MultipleChoiceListFilter):
   title = 'Tipe Ibadah'
   parameter_name = 'type'

   def lookups(self, request, model_admin):
        return TypeOfWorship.choices
   def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(type=value)
        return queryset

class CongregationAliasNameFilter(InputFilter):
   parameter_name = 'alias_name'
   title = 'Nama Alias'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter(masteruser__Congregation__alias_name__icontains=self.value())
       return queryset
   
class CongregationMemberNumberFilter(InputFilter):
   parameter_name = 'member_number'
   title = 'Nomor Anggota'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter(masteruser__Congregation__member_number__icontains=self.value())
       return queryset

class CongregationChineseNameFilter(InputFilter):
   parameter_name = 'chinese_name'
   title = 'Nama Cina'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter(masteruser__Congregation__chinese_name__icontains=self.value())
       return queryset

class WorshipNameFilter(InputFilter):
   parameter_name = 'worship.name'
   title = 'Ibadah'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter(worship__name__icontains=self.value())
       return queryset

class ServantMemberNumberFilter(InputFilter):
   parameter_name = 'member_number'
   title = 'Member Number'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter( masteruser__ServantOfGod__member_number__icontains=self.value())
       return queryset
   
from django.contrib import admin

class ServantMembershipStatusFilter(admin.SimpleListFilter):
    title = 'Status Member'
    parameter_name = 'membership_status'

    def lookups(self, request, model_admin):
        return (
            ('True', 'Aktif'),
            ('False', 'Tidak Aktif'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value is not None:
            if value == 'True':
                return queryset.filter(masteruser__ServantOfGod__membership_status=True)
            elif value == 'False':
                return queryset.filter(masteruser__ServantOfGod__membership_status=False)
        return queryset
    
class EmployeeNIKFilter(InputFilter):
   parameter_name = 'masteruser.nik'
   title = 'NIK/Passport'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter(masteruser__nik__icontains=self.value())
       return queryset
class EmployeeNIKFilter2(InputFilter):
   parameter_name = 'masteruser.nik'
   title = 'NIK/Passport'

   def queryset(self, request, queryset):
       if self.value() is not None:
           return queryset.filter(nik__icontains=self.value())
       return queryset