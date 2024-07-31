from rest_framework import viewsets, status, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

import pytz
import django_filters
from django.utils import timezone
from datetime import datetime, timedelta
from master.models import  Employee, Master
from management.models import ManagementOfWorship, ManagementPresence, ManagementPresenceDetail, RFIDCard
from management.serializers import ManagementOfWorshipSerializer, ManagementOfWorshipPagination, ManagementPresenceSerializer, ManagementPresencePagination, QRCodeSerializer, PresenceRFIDFingerprintSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.utils import IntegrityError

class ManagementOfWorshipViewSet(viewsets.ReadOnlyModelViewSet):
    http_method_names = ['get', 'head', 'options']
    serializer_class = ManagementOfWorshipSerializer
    pagination_class = ManagementOfWorshipPagination
    required_group_permission = ['management.view_managementofworship']
    queryset = ManagementOfWorship.objects.all()

class ManagementPresenceFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = ManagementPresence
        fields = ['worship__id', 'start_date', 'end_date']

class ManagementPresenceViewSet(viewsets.ReadOnlyModelViewSet):
    http_method_names = ['get', 'head', 'options']
    serializer_class = ManagementPresenceSerializer 
    pagination_class = ManagementPresencePagination
    required_group_permission = ['management.view_managementpresence']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ManagementPresenceFilter

    def get_queryset(self):
        user = self.request.user
        
        try:
            if hasattr(user.master, 'ServantOfGod'):
                queryset = ManagementPresence.objects.all()

                start_date = self.request.query_params.get('start_date')
                end_date = self.request.query_params.get('end_date')

                if start_date and end_date:
                    queryset = queryset.filter(
                        created_at__date__gte=start_date,
                        created_at__date__lte=end_date
                    )
                elif start_date:
                    queryset = queryset.filter(created_at__date__gte=start_date)
                elif end_date:
                    queryset = queryset.filter(created_at__date__lte=end_date)
                
                return queryset
        except AttributeError:
            pass

        return ManagementPresence.objects.none()
        
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        queryset = ManagementPresence.objects.filter(masteruser__user=request.user)

        worship_id = self.request.query_params.get('worship_id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if worship_id:
            queryset = queryset.filter(worship_id=worship_id)  
            
        if start_date and end_date:
            queryset = queryset.filter(
                created_at__date__gte=start_date,
                created_at__date__lte=end_date
            )
        elif start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)  
    
class QRCodeViewSet(viewsets.ViewSet):
    required_group_permission = ['management.view_managementpresence']

    @action(detail=False, methods=['post'], url_path='add')
    def add_qr(self, request):
        serializer = QRCodeSerializer(data=request.data)
        if serializer.is_valid():
            qr_id = serializer.validated_data['qr_id']
            
            try:
                worship = ManagementOfWorship.objects.get(qrcode=qr_id)
            except ManagementOfWorship.DoesNotExist:
                return Response({"status": "false", "Message": "Ibadah tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)
            user = self.request.user
            master = Master.objects.get(user=user)
            now = timezone.now().astimezone(pytz.timezone('Asia/Jakarta'))

            if not worship.start_time <= now.time() <= worship.end_time:
                return Response({"status": "false", "Message": "Ibadah tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)
            else:
                try:
                    existing_presence = ManagementPresence.objects.get(masteruser=master, worship=worship, check_out__isnull=True)
                    return Response({"status": "false", "Message": "Anda sudah ada di Ibadah"}, status=status.HTTP_404_NOT_FOUND)
                except ManagementPresence.DoesNotExist:
                    presence = ManagementPresence.objects.create(
                        masteruser=master,
                        source=2
                    )
                    ManagementPresenceDetail.objects.create(
                        presence=presence,
                        check_in=timezone.now()
                    )
                    return Response({"status": "true", "Worship_id": worship.id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PresenceRFIDFingerprintViewSet(APIView):
    required_group_permission = ['management.view_managementpresence']
    serializer_class = PresenceRFIDFingerprintSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data['id']
            type = serializer.validated_data['type']

            if type == 1:
                time = serializer.validated_data.get('time')
                mode = serializer.validated_data.get('mode')
                if not time or not mode:
                    return Response({"status": "false", "message": "Field 'time' dan 'mode' wajib diisi"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    employee = Employee.objects.get(nik=id)
                except Employee.DoesNotExist:
                    return Response({"status": "false", "Message": "Karyawan tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)
                master_user = employee.masteruser

            elif type == 2:
                tag = serializer.validated_data.get('tag')
                print(tag)
                if not tag:
                    return Response({"status": "false", "message": "Field 'tag' wajib diisi"}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    rfid = RFIDCard.objects.get(id_rfid=id)
                except RFIDCard.DoesNotExist:
                    return Response({"status": "false", "Message": "Nomor RFIF Card tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)
                master_user = rfid.masteruser.masteruser
                type = 3

            else:
                return Response({"status": "false", "Message": "Tipe tidak valid"}, status=status.HTTP_400_BAD_REQUEST)

            today_start = timezone.now().date()
            today_end = today_start + timedelta(days=1)
            try:
                presence, created = ManagementPresence.objects.get_or_create(
                    masteruser=master_user,
                    created_at__range=(today_start, today_end),
                    defaults={'source': type}
                )

                if type == 1:  # Fingerprint
                    if mode == 1:  # Check-in
                        if presence.ManagementPresenceDetail.filter(check_out__isnull=True).exists():  
                            return Response({"status": "false", "message": "Anda sudah masuk, silahkan pilih mode keluar"}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            ManagementPresenceDetail.objects.create(
                                presence=presence,
                                check_in=time
                            )
                            return Response({"status": "true", "message": "Presensi berhasil diubah (check-in)"}, status=status.HTTP_200_OK)
                    elif mode == 2:  # Check-out
                        presence_detail = presence.ManagementPresenceDetail.filter(check_out__isnull=True).first() 
                        if presence_detail: 
                            presence_detail.check_out = time
                            presence_detail.save()
                            return Response({"status": "true", "message": "Presensi berhasil diubah (check-out)"}, status=status.HTTP_200_OK)
                        else:
                            return Response({"status": "false", "message": "Anda belum masuk"}, status=status.HTTP_400_BAD_REQUEST)

                    else:
                        return Response({"status": "false", "message": "Mode tidak valid"}, status=status.HTTP_400_BAD_REQUEST)
                else: 
                    if not created:
                        return Response({"status": "false", "Message": "Anda sudah melakukan presensi"}, status=status.HTTP_400_BAD_REQUEST)
                presence.check_in = timezone.now()
                presence.tag = tag
                presence.save()

                return Response({"status": "true", "message": "Presensi Berhasil Dibuat"}, status=status.HTTP_200_OK)

            except IntegrityError:
                return Response({"status": "false", "Message": "Sudah ada checkin pada hari ini"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({"status": "false", "Message": {"error": str(e)}}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            