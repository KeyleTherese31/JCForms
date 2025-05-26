from django.contrib.auth.models import AbstractUser
from django.db import models

class AdminUser(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Superadmin'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')

    class Meta:
        verbose_name = 'admin user'
        verbose_name_plural = 'admin users'
    
    @property
    def actual_role(self):
        return 'superadmin' if self.is_superuser else self.role

class JobseekerCV(models.Model):
    position = models.CharField(max_length=100)
    date_applied = models.DateField()
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    contact_no = models.CharField(max_length=20, blank=True)
    dob = models.DateField(null=True, blank=True)
    pob = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    national_id = models.CharField(max_length=50, blank=True)
    sss_no = models.CharField(max_length=50, blank=True)
    tin_no = models.CharField(max_length=50, blank=True)
    tin_new = models.BooleanField(default=False)
    pagibig = models.CharField(max_length=50, blank=True)
    philhealth = models.CharField(max_length=50, blank=True)
    civil_status = models.CharField(max_length=100, blank=True)
    no_dependents = models.CharField(max_length=3, blank=True)

    # Nested Sections (stored as serialized JSON strings)
    education = models.TextField(blank=True, null=True)
    scholarships = models.TextField(blank=True, null=True)
    family = models.TextField(blank=True, null=True)
    employment = models.TextField(blank=True, null=True)
    references = models.TextField(blank=True, null=True)

    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)

class Test(models.Model):
    CATEGORY_CHOICES = [
        ('Image Pattern Analysis', 'Image Pattern Analysis'),
        ('Basic Math', 'Basic Math'),
        ('Problem Analysis and Solving', 'Problem Analysis and Solving'),
        ('Reading Comprehension', 'Reading Comprehension'),
        ('Pre Interview Questionnaire', 'Pre Interview Questionnaire'),
        ('Sentence Completion', 'Sentence Completion'),
        ('Other', 'Other'),
    ]

    FORMAT_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True / False'),
        ('short_answer', 'Short Answer'),
        ('long_answer', 'Long Answer'),
        ('checkboxes', 'Checkboxes'),
    ]

    QUESTION_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
    ]

    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    question_format = models.CharField(max_length=50, choices=FORMAT_CHOICES)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    question_text = models.TextField(blank=True, null=True)
    question_image = models.ImageField(upload_to='question_images/', blank=True, null=True)

    has_answer_key = models.BooleanField(default=True)
    answer_key = models.TextField(blank=True, null=True)

    # Store choices as JSON list (for multiple_choice, checkboxes)
    choices = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.question_text or 'Image Question'}"