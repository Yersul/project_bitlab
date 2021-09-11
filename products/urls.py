from django.urls import path, re_path
from rest_framework_nested.routers import DefaultRouter
from .views import ProductViewSet


router = DefaultRouter()
router.register('', ProductViewSet)

urlpatterns = [
    re_path('delete_attachments', ProductViewSet.as_view({'delete': 'delete_attachments'})),
] + router.urls
