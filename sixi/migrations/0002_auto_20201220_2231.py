# Generated by Django 3.1.2 on 2020-12-20 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sixi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='ctime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]