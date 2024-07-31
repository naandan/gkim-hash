import random
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from management.models import ManagementOfWorship, RFIDCard
from django.http import JsonResponse
from management.forms import RFIDCardForm
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def QrCode(request, uuid):
    data = get_object_or_404(ManagementOfWorship, id=uuid)
    return JsonResponse({'success': True, 'message': 'QR Code regenerated successfully', 'qrcode': data.qrcode})

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
@require_POST
def RegenerateQrCode(request, uuid):
    data = get_object_or_404(ManagementOfWorship, id=uuid)
    data.qrcode = ''.join(str(random.randint(0, 9)) for _ in range(8))
    data.save()
    return JsonResponse({'success': True, 'message': 'QR Code regenerated successfully', 'qrcode': data.qrcode})

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def add_rfid_card(request):
    if request.method == 'POST':
        form = RFIDCardForm(request.POST)
        if form.is_valid():
            rfid_card = form.save()
            context = {
                'form': RFIDCardForm(),
                'success_message': 'RFID Card Berhasil Ditambahkan!',
                'rfid_card': {'id_rfid': rfid_card.id_rfid, 'masteruser': rfid_card.masteruser.masteruser.full_name}
            }
            return render(request, 'views/add_rfid_card_form.html', context)
        else:
            context = {'form': form, 'errors': form.errors}
        
        return render(request, 'views/add_rfid_card_form.html', context)
    else:
        form = RFIDCardForm()
        return render(request, 'views/add_rfid_card_form.html', {'form': form})