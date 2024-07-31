from django.db import models
from management.models import ManagementPresence

class ManagementPresenceCongregationManager(models.Manager):
    def get_queryset(self):
       return super().get_queryset().filter(masteruser__Congregation__is_congregation=True).defer()

class ManagementPresenceServantOfGodManager(models.Manager):
    def get_queryset(self):
       return super().get_queryset().filter(masteruser__ServantOfGod__is_servant_of_god=True).defer()
    
class ManagementPresenceEmployeeManager(models.Manager):
    def get_queryset(self):
       return super().get_queryset().filter(masteruser__Employee__is_employee=True).defer()
    

class ManagementPresenceCongregationProxy(ManagementPresence):
    objects = ManagementPresenceCongregationManager()
    class Meta:
        proxy = True
        verbose_name = 'Detail Data Absensi Jemaat'
        verbose_name_plural = 'Detail Data Absensi Jemaat'

class ManagementPresenceServantOfGodProxy(ManagementPresence):
    objects = ManagementPresenceServantOfGodManager()
    class Meta:
        proxy = True
        verbose_name = 'Detail Data Absensi Hamba Tuhan'
        verbose_name_plural = 'Detail Data Absensi Hamba Tuhan'
    
class ManagementPresenceEmployeeProxy(ManagementPresence):
    objects = ManagementPresenceEmployeeManager()
    class Meta:
        proxy = True
        verbose_name = 'Detail Data Absensi Karyawan'
        verbose_name_plural = 'Detail Data Absensi Karyawan'
