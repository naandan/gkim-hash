from master.serializers import PhotoProfileSerializer, GetTokenViewSerializer, GetRefreshTokenViewSerializer, GallerySerializer, GalleryPagination, ServantSerializer, ServantPagination, UserSerializer
from master.models import Master, Gallery, ServantOfGod

from rest_framework import viewsets, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

class GetTokenView(TokenObtainPairView):
    serializer_class = GetTokenViewSerializer

class RefreshTokenView(TokenObtainPairView):
    serializer_class = GetRefreshTokenViewSerializer
class UserMeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    required_group_permission = ['master.view_master']

    def get_queryset(self):
        user = self.request.user 
        return Master.objects.filter(user=user)  
    def list(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def gallery(self, request):
        gallery = Gallery.objects.all()  
        paginator = GalleryPagination()
        page = paginator.paginate_queryset(gallery, request)

        if page is not None:
            serializer = GallerySerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        serializer = GallerySerializer(gallery, many=True, context={'request': request})
        return Response(serializer.data)

    parser_classes = (MultiPartParser, FormParser,) 
    @action(detail=False, methods=['POST'])
    def update_photo_profile(self, request):
        user = self.request.user
        try:
            master = Master.objects.get(user=user)
        except Master.DoesNotExist:
            return Response({"error": "Master tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PhotoProfileSerializer(master, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ServantViewSet(APIView):
    required_group_permission = ['master.view_servantofgod']  

    def get(self, request):
        queryset = ServantOfGod.objects.all()
        paginator = ServantPagination()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = ServantSerializer(page, many=True , context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        serializer = ServantSerializer(queryset, many=True , context={'request': request})
        return Response(serializer.data)