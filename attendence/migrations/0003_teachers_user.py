# Generated by Django 4.0.4 on 2022-05-25 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendence', '0002_rename_teacher_id_teacherslogininfo_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachers',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
