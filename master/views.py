import os
from django.shortcuts import get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.template import loader
from master.models import Gallery, Congregation, ServantOfGod, Employee
from management.proxy_model import ManagementPresenceCongregationProxy, ManagementPresenceServantOfGodProxy, ManagementPresenceEmployeeProxy
from management.models import ManagementOfWorship
from datetime import datetime, timedelta
from babel.dates import format_datetime
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def gallery(request, masteruser):
    template = loader.get_template('views/gallery.html')
    context = {
        'images': Gallery.objects.filter(masteruser=masteruser).order_by('-created_at'),
        'masteruser': masteruser
    }
    return HttpResponse(template.render(context, request))

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
@require_POST
def gallery_delete(request, id):
    try:
        gallery = get_object_or_404(Gallery, id=id)
        image_name = str(gallery.photo)
        gallery.delete()
        os.remove(os.path.join('media', image_name))
        return JsonResponse({'success': True, 'message': 'Gambar berhasil dihapus ', 'image_name': image_name})
    except Exception as e: 
        return JsonResponse({'success': False, 'message': f'Gagal menghapus gambar: {e}'}) 


@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def home(request):
    template = loader.get_template('admin/home.html')
    
    today = datetime.now().date()
    totals = {
        'Jumlah Jemaat': Congregation.objects.all(),
        'Jumlah Hamba Tuhan': ServantOfGod.objects.all(),
        'Jumlah Karyawan': Employee.objects.all(),
    }

    daily_presences = {}
    for delta in range(7):
        date = today - timedelta(days=delta)
        formatted_date = format_datetime(datetime.combine(date, datetime.min.time()), 'EEEE, dd MMMM yyyy', locale='id_ID')
        daily_presences[formatted_date] = {
            'Hamba Tuhan': ManagementPresenceServantOfGodProxy.objects.filter(created_at__date=date).count(),
            'Karyawan': ManagementPresenceEmployeeProxy.objects.filter(created_at__date=date).count(),
        }

    presences = []
    worships = ManagementOfWorship.objects.all()
    if today.weekday() == 6:
        weekend = today
    else:
        sunday = today.weekday() + 1 
        weekend = today - timedelta(days=sunday)
    
    start_date = today - timedelta(days=6) 
    end_date = today + timedelta(days=1) 
    for worship in worships:
        presence_count = ManagementPresenceCongregationProxy.objects.filter(
            worship=worship, created_at__range=(start_date, end_date)
        ).count()
        formatted_weekend = format_datetime(datetime.combine(weekend, datetime.min.time()), 'EEEE, dd MMMM yyyy', locale='id_ID')
        presences.append((worship.name, formatted_weekend, 'jemaat', presence_count))

    context = {
        'contents': totals, 
        'daily_presences': daily_presences,
        'presences': presences,
        'categories': ['Hamba Tuhan', 'Karyawan']
    } 

    return HttpResponse(template.render(context, request))
