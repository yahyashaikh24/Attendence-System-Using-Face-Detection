# Generated by Django 4.0.4 on 2022-05-25 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendence', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacherslogininfo',
            old_name='teacher_id',
            new_name='teacher',
        ),
    ]
