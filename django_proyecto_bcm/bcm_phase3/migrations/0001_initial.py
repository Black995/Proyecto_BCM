# Generated by Django 3.2.8 on 2022-06-27 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bcm_phase1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncidentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('crisis_scenario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crisis_scenario_indicent_history', to='bcm_phase1.crisisscenario')),
            ],
        ),
    ]
