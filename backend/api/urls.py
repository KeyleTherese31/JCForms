from django.urls import path
from .views import AdminRegisterView, AdminLoginView, JobseekerCVView, JobseekerCVDetailView, mobile_login, BulkQuestionView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('submit-cv/', JobseekerCVView.as_view(), name='submit-cv'),
    path('submit-cv/<int:id>/', JobseekerCVDetailView.as_view(), name='submit-cv-detail'),
    path('jobseeker-login/', mobile_login, name='jobseeker-login'),
    path('questions/bulk/', BulkQuestionView.as_view(), name='bulk-questions'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
