# Generated by Django 3.1.1 on 2020-09-24 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chaps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('textL', models.CharField(max_length=200)),
                ('textR', models.CharField(max_length=200)),
                ('status', models.IntegerField(default=0)),
                ('color', models.CharField(default='color:black;', max_length=20)),
                ('chap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chaps.chap')),
            ],
        ),
    ]
