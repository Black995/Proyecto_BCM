# Generated by Django 3.2.8 on 2022-02-01 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceOffered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('type', models.SmallIntegerField(choices=[(1, 'Producto'), (2, 'Servicio')])),
                ('profit', models.FloatField()),
                ('recovery_time', models.DurationField()),
                ('criticality', models.SmallIntegerField(null=True)),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='area_service_offered', to='configuration.area')),
                ('headquarters', models.ManyToManyField(related_name='headquarter_service_offered', to='configuration.Headquarter')),
                ('scale', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scale_service_offered', to='configuration.scale')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceUsed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('spending', models.FloatField()),
                ('recovery_time', models.DurationField()),
                ('criticality', models.SmallIntegerField(null=True)),
                ('headquarters', models.ManyToManyField(related_name='headquarter_service_used', to='configuration.Headquarter')),
                ('scale', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scale_service_used', to='configuration.scale')),
                ('services_offered', models.ManyToManyField(related_name='service_offered_service_offered', to='bcm_phase2.ServiceOffered')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=200)),
                ('cost', models.FloatField()),
                ('recovery_time', models.DurationField()),
                ('criticality', models.SmallIntegerField(null=True)),
                ('headquarters', models.ManyToManyField(related_name='headquarter_organization_activity', to='configuration.Headquarter')),
                ('scale', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scale_organization_activity', to='configuration.scale')),
                ('services_offered', models.ManyToManyField(related_name='service_offered_organizacion_activity', to='bcm_phase2.ServiceOffered')),
            ],
        ),
        migrations.CreateModel(
            name='InterestedParty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('type', models.SmallIntegerField(choices=[(1, 'Proveedor'), (2, 'Inversionista'), (3, 'Cliente'), (3, 'Accionista')])),
                ('description', models.CharField(max_length=200)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_interested_party', to='configuration.organization')),
            ],
        ),
    ]