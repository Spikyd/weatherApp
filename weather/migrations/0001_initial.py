# Generated by Django 5.0.2 on 2024-02-27 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('city', models.CharField(max_length=100)),
                ('max_temp', models.FloatField()),
                ('min_temp', models.FloatField()),
                ('total_precip', models.FloatField()),
                ('sunrise', models.TimeField()),
                ('sunset', models.TimeField()),
                ('condition', models.CharField(max_length=255)),
                ('wind_speed', models.FloatField()),
                ('humidity', models.IntegerField()),
                ('uv', models.FloatField()),
            ],
            options={
                'unique_together': {('date', 'city')},
            },
        ),
    ]
