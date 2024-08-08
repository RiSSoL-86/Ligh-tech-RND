from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, BalancesViewSet, OperationsViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('balances', BalancesViewSet, basename='balances')
router.register('operations', OperationsViewSet, basename='operations')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
