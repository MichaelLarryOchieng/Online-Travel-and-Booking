# Generated by Django 5.1.7 on 2025-04-22 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('city', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeatClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price_multiplier', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(default='XXX', max_length=3)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='city.city')),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_number', models.CharField(max_length=10)),
                ('slug', models.SlugField()),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('airline', models.CharField(blank=True, max_length=100, null=True)),
                ('arrival_airport', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arriving_flights', to='flight.airport')),
                ('arrival_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arriving_flights', to='city.city')),
                ('departure_airport', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departing_flights', to='flight.airport')),
                ('departure_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departing_flights', to='city.city')),
            ],
            options={
                'ordering': ['departure_time'],
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.CharField(max_length=10)),
                ('is_available', models.BooleanField(default=True)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seats', to='flight.flight')),
                ('seat_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight.seatclass')),
            ],
        ),
    ]
