import uuid
from django.db import models
from master.constans import Gender, BloodType, MaritalStatus, FamilyStatus, BaptisStatus, AgamaStatus
from django.utils.translation import gettext_lazy as _
from master.validates import validate_number_length, isValidPhoneNumber, isMemberNumberValid
from structural.models import NonStructural

class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name=_('Nama Lokasi'), help_text='Wajib diisi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True , verbose_name=_('Tanggal Diubah'))

    class Meta:
        verbose_name =  'Lokasi Gereja'
        verbose_name_plural = 'Lokasi Gereja'

    def __str__(self):
        return self.name
    
class Master(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255, verbose_name=_('Nama Lengkap'), help_text='Wajib diisi')
    gender = models.PositiveIntegerField(choices=Gender.choices, verbose_name=_('Jenis Kelamin'), help_text='Wajib diisi', null=True)
    address = models.CharField(max_length=255, verbose_name=_('Alamat'), help_text='Wajib diisi')
    personal_identity = models.CharField(verbose_name=_('NIK/PASPOR'), validators=[validate_number_length], unique=True, max_length=16, help_text='Wajib diisi')
    blood_type = models.PositiveIntegerField(choices=BloodType.choices, verbose_name=_('Golongan Darah'), help_text='Wajib diisi')
    marital_status = models.PositiveIntegerField(choices=MaritalStatus.choices, verbose_name=_('Status Perkawinan'), help_text='Wajib diisi')
    profile_photo =  models.ImageField(upload_to='profile_photo/img', null=True, blank=True, verbose_name=_('Foto Profil'), help_text='Wajib diisi')
    location =  models.ForeignKey(
        Location,
        verbose_name=_('Lokasi Gereja'),
        on_delete=models.CASCADE,
        related_name='Masters',
        help_text='Wajib diisi'
    )
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='master'
    )
    nonstructural = models.ForeignKey(
        NonStructural,
        verbose_name=_('Non Structural'),
        on_delete=models.CASCADE,
        related_name='NonStructural',
        blank=True, null=True
    )
    phone_number = models.CharField(max_length=255 , null=True, blank=True, verbose_name=_('Nomor Telepon'), validators=[isValidPhoneNumber] ,unique=True)
    date_of_birth = models.DateField(verbose_name=_('Tanggal Lahir'), blank=True, null=True)
    date_of_death = models.DateField(verbose_name=_('Tanggal Kematian'), blank=True, null=True, help_text='Isi jika sudah meninggal')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True , verbose_name=_('Tanggal Diubah'))

    class Meta:
        verbose_name = 'Data Master'
        verbose_name_plural = 'Data Master'

    def __str__(self):
        return self.full_name

class Congregation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    masteruser = models.OneToOneField(
        Master,
        verbose_name='Nama Lengkap',
        on_delete=models.CASCADE,
        related_name='Congregation',
    )
    member_number = models.CharField(verbose_name=_('Nomor Anggota Jemaat'), unique=True, max_length=16, help_text=(
            "<ul> <li>Wajib diisi</li>"
            "<li> Awalan (S), untuk simpatisan, contoh = S001 </li>"
            "<li> Untuk Anggota hanya terdiri dari angka, contoh = 001</li>"
            "<li> Jika mengisi no anggota Hamba Tuhan maka pada nomor anggota Jemaat akan berubah sesuai dengan yang di isi.</li> </ul>"
        ), validators=[isMemberNumberValid])
    alias_name = models.CharField(max_length=255, verbose_name=_('Nama Alias'), null=True, blank=True)
    chinese_name = models.CharField(max_length=255, verbose_name=_('Nama Mandarin'), null=True, blank=True)
    is_congregation = models.BooleanField(default=False, verbose_name=_('Dia Jemaat?'))
    worship = models.ForeignKey(
        'management.ManagementOfWorship',
        verbose_name='Ibadah Gereja',
        on_delete=models.CASCADE,
        related_name='Congregation',
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=_('Tanggal Diubah'))

    class Meta:
        verbose_name = 'Data Jemaat'
        verbose_name_plural = 'Data Jemaat'
    
    def save(self, *args, **kwargs):
        if hasattr(self.masteruser, 'ServantOfGod') and self.masteruser.ServantOfGod.is_servant_of_god==True:
            if self.member_number:
                ServantOfGod.objects.filter(id=self.masteruser.ServantOfGod.id).update(member_number=self.member_number)       
        super(Congregation, self).save(*args, **kwargs)

    def __str__(self):
        return self.masteruser.full_name

class Family(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    masteruser = models.ForeignKey(
        Master,
        verbose_name="Master Data",
        on_delete=models.CASCADE,
        related_name="Family"
    )
    family = models.ForeignKey(
        Master,
        verbose_name= _('Data Keluarga'),
        on_delete=models.CASCADE,
        related_name='family',
        null=True, blank=True,
    )
    status = models.PositiveIntegerField(choices=FamilyStatus.choices, help_text='Wajib diisi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Data Keluarga'
        verbose_name_plural = 'Data Keluarga'

    def __str__(self):
        return self.masteruser.full_name


class Baptism(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    congregation = models.ForeignKey(
        Master,
        verbose_name="Pendeta",
        on_delete=models.CASCADE,
        related_name="Pendeta",
        null=True,
        blank=True,
    )
    baptism_date = models.DateField(verbose_name=_('Tanggal Baptis'), help_text='Wajib diisi')
    masteruser = models.ForeignKey(
        Master,
        verbose_name="Master Data",
        on_delete=models.CASCADE,
        related_name="Baptism"
    )
    status = models.PositiveIntegerField(choices=BaptisStatus.choices, help_text='Wajib diisi')
    location = models.ForeignKey(
        Location,
        verbose_name=_('Lokasi Baptis'),
        on_delete=models.CASCADE,
        related_name='Location',
        blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Data Baptis / Atestasi'
        verbose_name_plural = 'Data Baptis / Atestasi'

    def __str__(self):
        return self.masteruser.full_name

class ServantOfGod(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    masteruser = models.OneToOneField(
        Master,
        verbose_name="Nama Lengkap",
        on_delete=models.CASCADE,
        related_name="ServantOfGod"
    )
    member_number = models.CharField(verbose_name=_('Nomor Hamba Tuhan'), unique=True,  max_length=16, help_text=(
            "<li> Awalan (S), untuk simpatisan, contoh = S001 </li>"
            "<li> Untuk Anggota hanya terdiri dari angka, contoh = 001</li>"
            "<li> Jika mengisi no anggota Hamba Tuhan maka pada nomor anggota Jemaat akan berubah sesuai dengan yang di isi.</li> </ul>"
            ), validators=[isMemberNumberValid])

    ordination = models.DateField(verbose_name=_('Tanggal Pengangkatan'), null=True, blank=True)
    pastor = models.ForeignKey(
        Master,
        verbose_name=_('Pendeta yang mengangkat'),
        on_delete=models.CASCADE,
        related_name='Pastor',
        null=True, blank=True,
    )
    church = models.CharField(max_length=255, verbose_name=_('Tempat Pengangkatan'), null=True, blank=True, help_text="Isi jika dari tempat lain.")
    membership_status = models.BooleanField(default=True, verbose_name=_('Status Keanggotaan'), help_text="Checklist jika masih aktif")
    is_servant_of_god = models.BooleanField(default=False, verbose_name=_('Dia Hamba Tuhan?'), help_text="Checklist jika ingin mengisi field hamba tuhan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True , verbose_name=_('Tanggal Diubah'))

    class Meta:
        verbose_name = 'Data Hamba Tuhan'
        verbose_name_plural = 'Data Hamba Tuhan'

    def save(self, *args, **kwargs):
        if hasattr(self.masteruser, 'Congregation') and self.masteruser.Congregation.is_congregation==True:
            if self.member_number is not None:
                Congregation.objects.filter(id=self.masteruser.Congregation.id).update(member_number=self.member_number)       
            if self.masteruser.Congregation.member_number is not None:
                self.member_number = self.masteruser.Congregation.member_number
        super(ServantOfGod, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.masteruser.full_name

class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nik = models.CharField(verbose_name=_('Nomor ID Karyawan'), unique=True, max_length=16, help_text="Wajib diisi")
    religion = models.PositiveIntegerField(choices=AgamaStatus.choices, verbose_name=_('Agama'), help_text="Wajib diisi")
    bpjs_employment = models.IntegerField(verbose_name=_('BPJS Karyawan'), unique=True, help_text="Wajib diisi")
    bpjs_health = models.IntegerField(verbose_name=_('BPJS Kesehatan'), unique=True, help_text="Wajib diisi")
    account_number = models.CharField(max_length=255, verbose_name=_('Nomor Rekening'), unique=True, help_text="Wajib diisi")
    start_date = models.DateField(verbose_name=_('Tanggal Mulai Kerja'), help_text="Wajib diisi")
    employee_position = models.CharField(max_length=255, verbose_name=_('Posisi Karyawan'), help_text="Wajib diisi")
    out_of_work = models.DateField(_("Tanggal Keluar Karyawan"), null=True, blank=True, help_text="Isi jika sudah tidak menjadi karyawan")
    is_employee = models.BooleanField(default=False, verbose_name=_('Dia Karyawan?'), help_text="Checklist jika ingin mengisi field karyawan")
    masteruser = models.OneToOneField(
        Master,
        verbose_name="Nama Lengkap",
        on_delete=models.CASCADE,
        related_name="Employee"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True , verbose_name=_('Tanggal Diubah'))

    class Meta:
        verbose_name = 'Data Karyawan'
        verbose_name_plural = 'Data Karyawan'

    def __str__(self):
        return self.masteruser.full_name

class Gallery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.CharField(max_length=255, null=True, blank=True)
    masteruser = models.ForeignKey(
        Master,
        verbose_name="Master Data",
        on_delete=models.CASCADE,
        related_name= "Gallery"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Gallery'

    def __str__(self):
        return self.masteruser.full_name