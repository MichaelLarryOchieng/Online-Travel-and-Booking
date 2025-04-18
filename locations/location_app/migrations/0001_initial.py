# Generated by Django 5.1.7 on 2025-03-26 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Locations',
            fields=[
                ('location_id', models.AutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('airport_code', models.CharField(blank=True, max_length=3, null=True)),
            ],
        ),
    ]
