from django.urls import path
from structural import views

urlpatterns = [
    path('structural/tree-structural/<str:pk>/', views.TreeStructural, name='tree'),
]