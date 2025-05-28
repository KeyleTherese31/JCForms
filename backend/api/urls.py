from django.urls import path
from .views import AdminRegisterView, AdminLoginView, JobseekerCVView, JobseekerCVDetailView, mobile_login,BulkQuestionCreateView, QuestionDetailView
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('submit-cv/', JobseekerCVView.as_view(), name='submit-cv'),
    path('submit-cv/<int:id>/', JobseekerCVDetailView.as_view(), name='submit-cv-detail'),
    path('jobseeker-login/', mobile_login, name='jobseeker-login'),
    path('questions/bulk-create/', BulkQuestionCreateView.as_view(), name='bulk-question-create'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),  # PUT, DELETE, GET by id
    path('questions/<str:category>/', views.questions_by_category),  # GET questions by category
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
