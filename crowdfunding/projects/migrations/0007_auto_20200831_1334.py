# Generated by Django 3.0.8 on 2020-08-31 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20200831_1331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='project',
        ),
    ]