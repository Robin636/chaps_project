# Generated by Django 3.1.1 on 2020-10-28 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chaps', '0011_auto_20201028_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pair',
            name='color',
        ),
    ]