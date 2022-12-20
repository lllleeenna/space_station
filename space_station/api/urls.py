from django.urls import include, path
from rest_framework import routers

from .views import StationViewSet

app_name = 'api'
router_v1 = routers.DefaultRouter()

router_v1.register(r'stations', StationViewSet, basename='stations')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
]
