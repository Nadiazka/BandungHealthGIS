# Generated by Django 3.0.3 on 2020-04-01 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_trialv12', '0008_kasus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasien',
            name='jenis_kelamin',
            field=models.CharField(max_length=10),
        ),
    ]