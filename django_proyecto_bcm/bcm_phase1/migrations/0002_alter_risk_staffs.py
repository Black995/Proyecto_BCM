# Generated by Django 3.2.8 on 2022-06-16 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcm_phase2', '0003_auto_20220616_1704'),
        ('bcm_phase1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='risk',
            name='staffs',
            field=models.ManyToManyField(related_name='staff_risk', to='bcm_phase2.Staff'),
        ),
    ]
