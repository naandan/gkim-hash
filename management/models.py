import uuid
from django.db import models
from django.db.models import Min, Max
from django.utils import timezone
from master.constans import TypeOfWorship, SourcePresence, DaysOfWeek
from django.utils.translation import gettext_lazy as _

class ManagementOfWorship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name=_('Nama Ibadah'), help_text="wajib diisi")
    start_time = models.TimeField(default=timezone.now, verbose_name=_('Waktu Mulai Ibadah'), help_text="wajib diisi")
    end_time = models.TimeField(default=timezone.now, verbose_name=_('Waktu Selesai Ibadah'), help_text="wajib diisi")
    pendeta = models.ForeignKey(
        'master.Master',
        verbose_name='Pembimbing Ibadah',
        on_delete=models.CASCADE,
        related_name="ManagementOfWorship",
        help_text="wajib diisi", null=True
    )
    type = models.PositiveIntegerField( choices=TypeOfWorship.choices, verbose_name=_('Jenis Ibadah'), help_text="wajib diisi")
    status = models.BooleanField(default=True, help_text="Checklis jika ingin menggunakan ibadah yang berbeda di waktu yang sama.")
    location = models.ForeignKey(
        'master.Location',
        verbose_name='Lokasi Pelaksanaan Ibadah',
        on_delete=models.CASCADE,
        related_name="ManagementOfWorship",
        help_text="wajib diisi"
    )
    qrcode = models.CharField(max_length=255, null=True, blank=True)
    day_worship = models.PositiveIntegerField(default=0, choices=DaysOfWeek.choices, verbose_name=_('Hari'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True , verbose_name=_('Tanggal Diubah'))

    class Meta:
        verbose_name = 'Data Ibadah Gereja'
        verbose_name_plural = 'Data Ibadah Gereja'

    def __str__(self):
        return self.name

class ManagementPresence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    masteruser = models.ForeignKey(
        'master.Master',
        verbose_name=' Data Master',
        on_delete=models.CASCADE,
        related_name="ManagementPresence",
        help_text="wajib diisi"
    )
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    source = models.PositiveIntegerField( choices=SourcePresence.choices, null=True, blank=True)
    worship = models.ForeignKey(
        ManagementOfWorship,
        verbose_name='Ibadah Gereja',
        on_delete=models.CASCADE,
        related_name="ManagementPresence",
        null=True, blank=True
    )
    length_of_work = models.TimeField(null=True, blank=True, verbose_name=_('Lama Kerja'))
    tag = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Tag (Id Perangkat Presensi)")) 
    present = models.BooleanField(default=True, verbose_name=_('Hadir'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True , verbose_name=_('Tanggal Diubah'))

    def save(self, *args, **kwargs):
        if self.check_in is not None :
            worship = ManagementOfWorship.objects.filter(status=True, start_time__lte=self.check_in, end_time__gte=self.check_in).first()
            if hasattr(self.masteruser, 'Congregation') and self.masteruser.pk is not None:
                if self.masteruser.Congregation.worship.start_time <= self.check_in.time() <= self.masteruser.Congregation.worship.end_time and self.masteruser.Congregation.worship.status == True :
                    self.worship = self.masteruser.Congregation.worship
                else:
                    self.worship = worship
            elif hasattr(self.masteruser, 'ServantOfGod') and self.masteruser.pk is not None:
                self.worship = worship


            if self.check_in is not None and self.check_out is not None:
                timedelta = self.check_out - self.check_in
                totalsecond = int(timedelta.total_seconds())
                hours, remainder = divmod(totalsecond, 3600)
                minutes, seconds = divmod(remainder, 60)
                self.length_of_work = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Data Absensi'
        verbose_name_plural = 'Data Absensi'

    def __str__(self):
        return self.masteruser.full_name

class ManagementPresenceDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    presence = models.ForeignKey(
        ManagementPresence,
        verbose_name='Data Absensi',
        on_delete=models.CASCADE,
        related_name="ManagementPresenceDetail",
        help_text="wajib diisi"
    )
    check_in = models.DateTimeField( null=True, blank=True)
    check_out = models.DateTimeField( null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True , verbose_name=_('Tanggal Diubah'))

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        check_in_out = self.presence.ManagementPresenceDetail.exclude(pk=self.pk if not is_new else None).aggregate(
            first_check_in=Min('check_in'),
            last_check_out=Max('check_out')
        )
        self.presence.check_in = min(filter(None, (check_in_out['first_check_in'], self.check_in)), default=None)
        self.presence.check_out = max(filter(None, (check_in_out['last_check_out'], self.check_out)), default=None)

        self.presence.save()
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Detail Data Absensi'
        verbose_name_plural = 'Detail Data Absensi'

    def __str__(self):
        return self.presence.masteruser.full_name
    
class RFIDCard (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_rfid = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Nomor RFID'), unique=True)
    masteruser = models.OneToOneField(
        'master.Congregation',
        verbose_name="Data Jemaat",
        on_delete=models.CASCADE,
        related_name="RFIDCard",
        help_text="wajib diisi"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True , verbose_name=_('Tanggal Diubah'))

    class Meta:
        verbose_name = 'RFID Card'
        verbose_name_plural = 'RFID Card'

    def __str__(self):
        return self.masteruser.masteruser.full_name