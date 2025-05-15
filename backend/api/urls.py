from django.urls import path
from .views import AdminRegisterView, AdminLoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
