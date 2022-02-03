# Generated by Django 3.2.8 on 2022-02-03 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
        ('bcm_phase2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationactivity',
            name='scale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scale_organization_activity', to='configuration.scale'),
        ),
        migrations.AlterField(
            model_name='serviceoffered',
            name='scale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scale_service_offered', to='configuration.scale'),
        ),
        migrations.AlterField(
            model_name='serviceused',
            name='scale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scale_service_used', to='configuration.scale'),
        ),
    ]
