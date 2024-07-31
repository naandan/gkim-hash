import uuid
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _

class PriodeStructural(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name=_('Nama Priode'))
    start_date = models.DateField(verbose_name=_('Tanggal Mulai'))
    end_date = models.DateField(verbose_name=_('Tanggal Selesai'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True , verbose_name=_('Tanggal Diubah'))

    class Meta:
        verbose_name = 'Periode Struktural'
        verbose_name_plural = 'Periode Struktural'

    def __str__(self):
        return self.name   

class Structural(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name=_('Nama Structural'))
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    masteruser = models.ForeignKey(
        'master.Master',
        verbose_name='Data Master',
        on_delete=models.CASCADE,
        related_name="Struktural",
        null=True, blank=True
    )
    periode = models.ForeignKey(
        'PriodeStructural',
        verbose_name='Periode',
        on_delete=models.CASCADE,
        related_name="Structural",
        null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True , verbose_name=_('Tanggal Diubah'))
    class Meta:
        verbose_name = 'Struktural'
        verbose_name_plural = 'Struktural'

    def __str__(self):
        return self.name

class NonStructural(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=255, verbose_name=_('Nama Role'), blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True , verbose_name=_('Tanggal Diubah'))
    class Meta:
        verbose_name = 'Non Struktural'
        verbose_name_plural = 'Non Struktural'

    def __str__(self):
        return self.role
    