# Generated by Django 4.2.20 on 2025-05-18 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_adminuser_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobseekerCV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100)),
                ('date_applied', models.DateField()),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('address', models.TextField(blank=True)),
                ('contact_no', models.CharField(blank=True, max_length=20)),
                ('dob', models.DateField(blank=True, null=True)),
                ('pob', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('national_id', models.CharField(blank=True, max_length=50)),
                ('sss_no', models.CharField(blank=True, max_length=50)),
                ('tin_no', models.CharField(blank=True, max_length=50)),
                ('tin_new', models.BooleanField(default=False)),
                ('pagibig', models.CharField(blank=True, max_length=50)),
                ('philhealth', models.CharField(blank=True, max_length=50)),
                ('civil_status', models.CharField(blank=True, max_length=100)),
                ('education', models.JSONField(blank=True, null=True)),
                ('scholarships', models.JSONField(blank=True, null=True)),
                ('family', models.JSONField(blank=True, null=True)),
                ('employment', models.JSONField(blank=True, null=True)),
                ('references', models.JSONField(blank=True, null=True)),
                ('signature', models.ImageField(blank=True, null=True, upload_to='signatures/')),
            ],
        ),
    ]
