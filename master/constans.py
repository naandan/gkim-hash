from django.db import models

class Gender(models.IntegerChoices):
    MAN = 1, "Laki-laki"
    WOMAN = 2, "Perempuan"

class BloodType(models.IntegerChoices):
    A_POSITIVE = 1, 'A+'
    B_POSITIVE = 2, 'B+'
    AB_POSITIVE = 3, 'AB+'
    O_POSITIVE = 4, 'O+'
    A_NEGATIVE = 5, 'A-'
    B_NEGATIVE = 6, 'B-'
    AB_NEGATIVE = 7, 'AB-'
    O_NEGATIVE = 8, 'O-'

class MaritalStatus(models.IntegerChoices):
    SINGLE = 1, 'Belum Menikah'
    MARRIED = 2, 'Menikah'
    WINDOWWINDOWER = 3, 'Janda/Duda'

class FamilyStatus(models.IntegerChoices):
    FATHER = 1, 'Ayah'
    MOTHER = 2, 'Ibu'
    HUSBAND = 3, 'Suami'
    WIFE = 4, 'Istri'
    CHILD = 5, 'Anak'
    BROTHER = 6, 'Kakak'
    SISTER = 7, 'Adik'
    RELATIVES = 8, 'Kerabat'

class BaptisStatus(models.IntegerChoices):
    BAPTISM_CILD = 1, 'Anak'
    BAPTISM_ADULT = 2, 'Dewasa'
    BAPTISM_ATESTASI_MASUK = 3, 'Atestasi Masuk'
    BAPTISM_ATESTASI_KELUAR = 4, 'Atestasi Keluar'
    BAPTISM_SIDI = 5, 'Sidi'

class AgamaStatus(models.IntegerChoices):
    ISLAM = 1, 'Islam'
    KRISTEN = 2, 'Kristen'
    KATHOLIK = 3, 'Katholik'
    HINDU = 4, 'Hindu'
    BUDHA = 5, 'Budha'
    KONGHUCU = 6, 'Konghucu'

class TypeOfWorship(models.IntegerChoices):
    ONLINE = 1, 'Online'
    OFFLINE = 2, 'Offline'
    HYBRID = 3, 'Hybrid'

class SourcePresence(models.IntegerChoices):
    FINGERPRINT = 1, 'Fingerprint'
    QR_CODE = 2, 'QR Code'
    RFID = 3, 'RFID'

class Role(models.IntegerChoices):
    CONGREGATION = 1, 'Congregation'
    SERVANTOFGOD = 2, 'Servant Of God'
    EMPLOYEE = 3, 'Employee'

class DaysOfWeek(models.IntegerChoices):
    MONDAY = 1, 'Senin'
    TUESDAY = 2, 'Selasa'
    WEDNESDAY = 3, 'Rabu'
    THURSDAY = 4, 'Kamis'
    FRIDAY = 5, 'Jumat'
    SATURDAY = 6, 'Sabtu'
    SUNDAY = 7, 'Minggu'