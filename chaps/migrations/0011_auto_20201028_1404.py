# Generated by Django 3.1.1 on 2020-10-28 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaps', '0010_auto_20201024_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chap',
            name='toCallNum1',
        ),
        migrations.RemoveField(
            model_name='chap',
            name='toCallNum2',
        ),
    ]