from rest_framework import serializers
from master.models import (
    Location, Master, Congregation, Family,Gallery, ServantOfGod
)
from rest_framework.pagination import PageNumberPagination
from management.models import ManagementOfWorship  
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth.models import User

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']

class WorshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementOfWorship
        fields = ['id', 'name'] 

class CongregationSerializer(serializers.ModelSerializer):
    worship = WorshipSerializer()

    class Meta:
        model = Congregation
        fields = ['id', 'member_number', 'alias_name', 'chinese_name', 'is_congregation', 'worship']

class FamilySerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(source="id")  
    id = serializers.UUIDField(source="family.id") 
    full_name = serializers.CharField(source='family.full_name')
    gender = serializers.CharField(source='family.get_gender_display')
    address = serializers.CharField(source='family.address')
    personal_identity = serializers.IntegerField(source='family.personal_identity')
    blood_type = serializers.CharField(source='family.get_blood_type_display')
    marital_status = serializers.CharField(source='family.get_marital_status_display')
    profile_photo = serializers.ImageField(source='family.profile_photo')
    location = LocationSerializer(source='family.location')  
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Family
        fields = ['uuid', 'id', 'full_name', 'gender', 'address', 'personal_identity',
                  'blood_type', 'marital_status', 'profile_photo', 'location', 'status']

class MasterSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    congregation = serializers.SerializerMethodField()
    families = serializers.SerializerMethodField()
    blood_type = serializers.CharField(source='get_blood_type_display')
    gender = serializers.CharField(source='get_gender_display')
    marital_status = serializers.CharField(source='get_marital_status_display')
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Master
        fields = ['id', 'full_name', 'gender','date_of_birth','phone_number' , 'address', 'personal_identity',
                  'blood_type', 'marital_status', 'profile_photo', 'location',
                  'congregation', 'families', ]
        

    def get_congregation(self, obj):
        congregation = Congregation.objects.filter(masteruser=obj).first()
        return CongregationSerializer(congregation).data if congregation else None

    def get_families(self, obj):
        families = Family.objects.filter(masteruser=obj)
        return FamilySerializer(families, many=True).data

    def get_profile_photo(self, obj):
        if obj.profile_photo:
            return obj.profile_photo.url
        return None
    
class UserSerializer(serializers.ModelSerializer):
    master = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(source='master.created_at')
    updated_at = serializers.DateTimeField(source='master.updated_at')
    
    class Meta:
        model = User
        fields= ('id', 'email', 'master', 'created_at', 'updated_at')
        
    def get_master(self, obj):
        try:
            master = Master.objects.get(user=obj)
            return MasterSerializer(master, context=self.context).data 
        except Master.DoesNotExist:
            return None
    
 
class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = ['id', 'photo']

class PhotoProfileSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(required=True)  

    class Meta:
        model = Master
        fields = ['profile_photo']

class GalleryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class ServantPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class ServantSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='masteruser.full_name')
    profile_photo = serializers.SerializerMethodField()
    phone_number = serializers.CharField(source='masteruser.phone_number')

    class Meta:
        model = ServantOfGod
        fields = ['id', 'full_name', 'phone_number', 'profile_photo']
    
    def get_profile_photo(self, obj):
        if obj.masteruser.profile_photo:
            return obj.masteruser.profile_photo.url
        return None
    
class GetTokenViewSerializer(TokenObtainPairSerializer):
    pass

class GetRefreshTokenViewSerializer(TokenRefreshSerializer):
    pass