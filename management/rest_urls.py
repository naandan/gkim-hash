from rest_framework import routers
from management import rest_views

router = routers.DefaultRouter()
router.register(r'worships', rest_views.ManagementOfWorshipViewSet, basename="worships")
router.register(r'presences', rest_views.ManagementPresenceViewSet, basename="presences")
router.register(r'presence/qr', rest_views.QRCodeViewSet, basename="qrcodes")