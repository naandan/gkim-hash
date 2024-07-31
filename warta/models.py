import uuid
from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _

class Warta (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name=_('Nama Warta'))
    file = models.FileField(upload_to='warta/file', null=True, blank=True, verbose_name=_('File Warta'))
    status = models.BooleanField(default=False, verbose_name=_('Status Warta'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True , verbose_name=_('Tanggal Diubah'))
    order = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Urutan'), unique=True)

    class Meta:
        verbose_name = 'Warta'
        verbose_name_plural = 'Warta'

    def __str__(self):
        return self.name

class Announcement (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name=_('Nama Pengumuman'))
    file = models.FileField(upload_to='Announcement/file', null=True, blank=True, verbose_name=_('File Pengumuman'))
    order = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name=_('Urutan'), unique=True)
    contents = HTMLField(verbose_name=_('Konten Pengunguman'), help_text=_('html is supported'))
    status = models.BooleanField(default=False, verbose_name=_('Status Pengumuman'))
    url = models.URLField(max_length=255, null=True, blank=True, verbose_name=_('Url Pengumuman'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Dibuat'))
    updated_at = models.DateTimeField(auto_now=True , verbose_name=_('Tanggal Diubah'))
    class Meta:
        verbose_name = 'Pengumuman'
        verbose_name_plural = 'Pengumuman'
        ordering = ('-order',)

    def __str__(self):
        return self.name
