# Generated by Django 5.2 on 2025-05-19 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_examquestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(choices=[('text', 'Text'), ('image', 'Image')], max_length=20)),
                ('question_format', models.CharField(choices=[('multiple_choice', 'Multiple Choice'), ('checkboxes', 'Checkboxes'), ('true_false', 'True/False'), ('short_answer', 'Short Answer')], max_length=30)),
                ('question_text', models.TextField(blank=True)),
                ('question_image_url', models.URLField(blank=True)),
                ('choices', models.JSONField(blank=True, default=list)),
                ('answer_key', models.CharField(blank=True, max_length=255)),
                ('category', models.CharField(choices=[('Image Pattern Analysis', 'Image Pattern Analysis'), ('Basic Math', 'Basic Math'), ('Problem Analysis and Solving', 'Problem Analysis and Solving'), ('Reading Comprehension', 'Reading Comprehension'), ('Pre Interview Questionnaire', 'Pre Interview Questionnaire'), ('Sentence Completion', 'Sentence Completion'), ('Other', 'Other')], max_length=100)),
                ('hasAnswerKey', models.BooleanField(default=False)),
            ],
        ),
    ]
