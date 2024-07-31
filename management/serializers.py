from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from django.utils import timezone

from management.models import ManagementOfWorship, ManagementPresence, ManagementPresenceDetail

class ManagementOfWorshipSerializer(serializers.ModelSerializer):
    day_worship = serializers.CharField(source='get_day_worship_display')
    type = serializers.CharField(source='get_type_display')
    class Meta:
        model = ManagementOfWorship
        fields = ['id', 'name','start_time', 'end_time' , 'day_worship', 'type', 'status', ]

class ManagementOfWorshipPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class ManagementPresenceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementPresenceDetail
        fields = ('id', 'check_in', 'check_out')

class ManagementPresenceSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='masteruser.full_name')
    details = serializers.SerializerMethodField()
    source = serializers.CharField(source='get_source_display')
    worship_id = serializers.SerializerMethodField()

    class Meta:
        model = ManagementPresence
        fields = ('id', 'user',  'check_in', 'check_out', 'source', 'worship_id', 'tag' ,'details')

    def get_worship_id(self, obj):
        if obj.worship is not None:
            return obj.worship.id
        return None

    def get_details(self, obj):
        return ManagementPresenceDetailSerializer(obj.ManagementPresenceDetail.all(), many=True).data 
    
class ManagementPresencePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class QRCodeSerializer(serializers.Serializer):
    qr_id = serializers.CharField(max_length=255)

class PresenceRFIDFingerprintSerializer(serializers.Serializer):
    id = serializers.CharField(style={'input_type': 'text'})
    type = serializers.ChoiceField(choices=[(1, 'Fingerprint'), (2, 'RFID')])
    tag = serializers.IntegerField(required=False)
    time = serializers.DateTimeField(default=timezone.now)
    mode = serializers.ChoiceField(choices=[(1, 'In'), (2, 'Out'),], default=0)
