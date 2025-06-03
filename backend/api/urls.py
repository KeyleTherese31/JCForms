from django.urls import path
from .views import AdminRegisterView, AdminLoginView, AdminProfileView, AdminListView, AdminDeactivateView, JobseekerCVView, JobseekerCVDetailView, mobile_login,BulkQuestionCreateView, SubmitTestView, JobseekerScoresView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('admin/profile/', AdminProfileView.as_view(), name='admin-profile'),
    path('admin-users/', AdminListView.as_view()),  # ✅ must match Vue
    path('deactivate-admin/<int:pk>/', AdminDeactivateView.as_view()),
    path('admin/update/', views.admin_update_view, name='admin-update'),
    path('submit-cv/', JobseekerCVView.as_view(), name='submit-cv'),
    path('submit-cv/<int:id>/', JobseekerCVDetailView.as_view(), name='submit-cv-detail'),
    path('jobseeker-login/', mobile_login, name='jobseeker-login'),
    path('questions/bulk-create/', BulkQuestionCreateView.as_view(), name='bulk-question-create'),
    path('questions/<str:category>/', views.questions_by_category),
    path('submit-test/', SubmitTestView.as_view(), name='submit-test'),
    path('jobseeker-scores/<int:jobseeker_id>/', JobseekerScoresView.as_view(), name='jobseeker-scores'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 