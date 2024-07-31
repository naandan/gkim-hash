from .models import Structural, PriodeStructural
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def TreeStructural(request, pk):
    trees = Structural.objects.filter(periode=pk)
    priode = PriodeStructural.objects.filter(id=pk).first()
    return render(request, 'views/tree.html', {'trees': trees, 'priode': priode})
