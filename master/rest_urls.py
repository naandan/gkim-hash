from rest_framework import routers
from django.urls import path, include
from master import rest_views
from management import rest_views as management_rest_views

from warta.rest_urls import router as warta_router
from management.rest_urls import router as management_router

router = routers.DefaultRouter()
router.register(r'users/me', rest_views.UserMeViewSet, basename='userme')

router.registry.extend(warta_router.registry)
router.registry.extend(management_router.registry)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/', include([
        path('', include(router.urls)),
        path('auth/token', rest_views.GetTokenView.as_view(), name='token_obtain_pair'),
        path('auth/token/refresh', rest_views.RefreshTokenView.as_view(), name='token_refresh'),
        path('presence/scan', management_rest_views.PresenceRFIDFingerprintViewSet.as_view(), name='presence_scan'),
        path('servants/', rest_views.ServantViewSet.as_view(), name='presence_scan'),
    ])),
]   