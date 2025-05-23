# Generated by Django 5.1.7 on 2025-04-22 14:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flight', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('seats_booked', models.IntegerField(default=0)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('flight', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flight.flight')),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('seats', models.ManyToManyField(related_name='bookings', to='flight.seat')),
            ],
        ),
    ]
