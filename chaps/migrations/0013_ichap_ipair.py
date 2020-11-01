# Generated by Django 3.1.1 on 2020-10-29 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chaps', '0012_remove_pair_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='IChap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IPair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('textL', models.CharField(max_length=200)),
                ('textR', models.CharField(max_length=200)),
                ('status', models.IntegerField(blank=True, default=0)),
                ('chap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Ipairs', to='chaps.ichap')),
            ],
        ),
    ]