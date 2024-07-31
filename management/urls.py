from django.urls import path, re_path as url
from . import views

from management.forms import MasterCongregation, MasterEmployee, MasterServant

urlpatterns = [
    url(
        r'^master-autocomplete/$',
        MasterCongregation.as_view(),
        name='master-autocomplete',
    ),
    url(
        r'^master-autocomplete2/$',
        MasterServant.as_view(),
        name='master-autocomplete2',
    ),
    url(
        r'^master-autocomplete3/$',
        MasterEmployee.as_view(),
        name='master-autocomplete3',
    ),
    path('qr-code/<str:uuid>', views.QrCode, name='qrcode'),
    path('qr-code/<str:uuid>/regenerate', views.RegenerateQrCode, name='qrcode_regenerate'),
    path('rfidcard/register/', views.add_rfid_card, name='register_rfid_card'),
]