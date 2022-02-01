# Generated by Django 3.2.8 on 2022-01-28 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Headquarter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('type', models.SmallIntegerField(choices=[(1, 'País'), (2, 'Estado'), (3, 'Ciudad')])),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('legal_id', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(max_length=350)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='organization_logo')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('relevant', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Scale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('min_value', models.SmallIntegerField()),
                ('max_value', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_number', models.IntegerField(null=True)),
                ('names', models.CharField(max_length=100)),
                ('surnames', models.CharField(max_length=100)),
                ('earnings', models.IntegerField()),
                ('Headquarter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='headquarter_staff', to='configuration.headquarter')),
                ('area', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='area_staff', to='configuration.area')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_staff', to='configuration.position')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_staff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ScaleView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('scale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scale_view', to='configuration.scale')),
            ],
        ),
        migrations.AddField(
            model_name='headquarter',
            name='location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_headquarter', to='configuration.location'),
        ),
    ]
