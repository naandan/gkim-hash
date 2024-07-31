from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from warta.models import Announcement, Warta

class WartaSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    
    class Meta:
        model = Warta
        fields = ['id', 'name', 'file', 'status', 'order', 'created_at', 'updated_at']
    
    def get_file(self, obj):
        if obj.file:
            return obj.file.url
        return None

class WartaPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class AnnouncementSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    class Meta:
        model = Announcement
        fields = ['id', 'name', 'url', "file" , 'status', 'contents', 'order', 'created_at', 'updated_at']
    
    def get_file (self, obj):
        return obj.file.url


class AnnouncementPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    