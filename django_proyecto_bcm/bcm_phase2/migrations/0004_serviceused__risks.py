# Generated by Django 3.2.8 on 2022-06-14 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcm_phase1', '0003_remove_risk_services_used'),
        ('bcm_phase2', '0003_auto_20220613_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceused',
            name='_risks',
            field=models.ManyToManyField(related_name='risk_service_used', to='bcm_phase1.Risk'),
        ),
    ]
