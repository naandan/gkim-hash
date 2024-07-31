import uuid
from django.db import models
from django.core.exceptions import ValidationError

class Setting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    allow_edit = models.BooleanField(default=False, verbose_name='Bisa di edit')

    def __str__(self):
        return u"Konfigurasi Umum"
    
    class Meta:
        verbose_name = "Konfigurasi Umum"
        verbose_name_plural = "Konfigurasi Umum"

    def save(self, *args, **kwargs):
        if Setting.objects.exists() and not self.pk:
            raise ValidationError("Hanya boleh ada satu pengaturan umum.")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if Setting.objects.count() == 1:
            raise ValidationError("Hanya boleh ada satu pengaturan umum.")
        super().delete(*args, **kwargs)