from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_number_length(value, min_length=9):
    if len(str(value)) < min_length:
        raise ValidationError(_('Panjang nomor identitas harus minimal {} digit.'.format(min_length)))
    return value

def isValidPhoneNumber(value):
    phone_regex = r'^0\d{7,15}$'
    if not re.match(phone_regex, value):
        raise ValidationError(
            _('%(value)s no telepon tidak valid. harus diawalin dengan 0 dan hanya terdiri dari angka.'),
            params={'value': value},
        )
    return value

def isMemberNumberValid(value):
    if value.startswith('S'):
        if not value[1:].isnumeric():
            raise ValidationError(
                _('%(value)s no anggota tidak valid. harus diawalin dengan S dan hanya terdiri dari angka.'),
                params={'value': value},
            )
    else:
        if not value.isnumeric():
            raise ValidationError(
                _('%(value)s no anggota tidak valid. harus terdiri dari angka.'),
                params={'value': value},
            )
    return value