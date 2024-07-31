from rest_framework import routers
from warta import rest_views

router = routers.DefaultRouter()
router.register(r'news', rest_views.WartaViewSet, basename="warta")
router.register(r'announcements', rest_views.AnnouncementViewSet, basename="announcement")