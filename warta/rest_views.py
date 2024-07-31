from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from warta.models import Warta, Announcement
from warta.serializers import WartaSerializer, WartaPagination, AnnouncementSerializer, AnnouncementPagination
    
class WartaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WartaSerializer
    pagination_class = WartaPagination  
    required_group_permission = ['warta.view_warta']

    def get_queryset(self):
        return Warta.objects.all()
    
class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AnnouncementSerializer
    pagination_class = AnnouncementPagination
    required_group_permission = ['warta.view_announcement']
    
    def get_queryset(self):
        return Announcement.objects.all()