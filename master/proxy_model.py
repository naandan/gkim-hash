from django.db import models
from master.models import Congregation, Family, Baptism, ServantOfGod, Employee, Gallery

class CongregationManage(models.Manager):
    def get_queryset(self):
        return super(CongregationManage, self).get_queryset().filter( is_congregation=True )
class CongregationProxy(Congregation):
    objects = CongregationManage()
    class Meta:
        proxy = True
        verbose_name = 'Data Jemaat'
        verbose_name_plural = 'Data Jemaat'

class FamilyManage(models.Manager):
    def get_queryset(self):
        return super(FamilyManage, self).get_queryset()

class FamilyProxy(Family):
    objects = FamilyManage()
    class Meta:
        proxy = True
        verbose_name = 'Data Keluarga'
        verbose_name_plural = 'Data Keluarga'

class BaptismManage(models.Manager):
    def get_queryset(self):
        return super(BaptismManage, self).get_queryset()


class BaptismProxy(Baptism):
    objects = BaptismManage()
    class Meta:
        proxy = True
        verbose_name = 'Data Baptis'
        verbose_name_plural = 'Data Baptis'


class ServantOfGodManage(models.Manager):
    def get_queryset(self):
        return super(ServantOfGodManage, self).get_queryset().filter(  is_servant_of_god=True )

class ServantOfGodProxy(ServantOfGod):
    objects = ServantOfGodManage()
    class Meta:
        proxy = True
        verbose_name = 'Data Hamba Tuhan'
        verbose_name_plural = 'Data Hamba Tuhan'

class EmployeeManage(models.Manager):
    def get_queryset(self):
        return super(EmployeeManage, self).get_queryset().filter(  is_employee=True )

class EmployeeProxy(Employee):
    objects = EmployeeManage()
    class Meta:
        proxy = True
        verbose_name = 'Data Karyawan'
        verbose_name_plural = 'Data Karyawan'

class GalleryManage(models.Manager):
    def get_queryset(self):
        return super(GalleryManage, self).get_queryset()
    
class GalleryProxy(Gallery):
    objects = GalleryManage()
    class Meta:
        proxy = True
        verbose_name = 'Data Gallery'
        verbose_name_plural = 'Data Gallery'


# NOTE RED: KEMUNGKINAN FILE INI AKAN DI HAPUS KARENA TIDAK MENGGUNAKAN PROXY JUGA SUDAH BISA.