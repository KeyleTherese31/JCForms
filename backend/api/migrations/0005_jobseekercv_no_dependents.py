# Generated by Django 5.2.1 on 2025-05-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_jobseekercv_education_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseekercv',
            name='no_dependents',
            field=models.CharField(blank=True, max_length=3),
        ),
    ]
