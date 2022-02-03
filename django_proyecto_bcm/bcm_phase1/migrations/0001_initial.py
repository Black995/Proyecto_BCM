# Generated by Django 3.2.8 on 2022-02-01 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configuration', '0001_initial'),
        ('bcm_phase2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=200)),
                ('headquarters', models.ManyToManyField(related_name='headquarter_risk', to='configuration.Headquarter')),
                ('organizacion_activities', models.ManyToManyField(related_name='organizacion_activity_risk', to='bcm_phase2.OrganizationActivity')),
                ('services_offered', models.ManyToManyField(related_name='service_used_risk', to='bcm_phase2.ServiceUsed')),
                ('staffs', models.ManyToManyField(related_name='staff_risk', to='configuration.Staff')),
            ],
        ),
        migrations.CreateModel(
            name='CrisisScenario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(max_length=200)),
                ('_risks', models.ManyToManyField(db_column='risks', related_name='crisis_scenario_risk', to='bcm_phase1.Risk')),
                ('headquarters', models.ManyToManyField(related_name='headquarter_crisis_scenario', to='configuration.Headquarter')),
            ],
        ),
    ]