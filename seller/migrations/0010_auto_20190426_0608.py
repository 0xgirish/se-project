# Generated by Django 2.2 on 2019-04-26 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0009_shopprofile_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopitem',
            name='priority',
        ),
        migrations.AddField(
            model_name='shopitem',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
