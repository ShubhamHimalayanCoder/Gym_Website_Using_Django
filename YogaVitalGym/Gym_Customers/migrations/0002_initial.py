# Generated by Django 5.0.6 on 2024-06-23 16:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Gym_Customers', '0001_initial'),
        ('Gym_Staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Gym_Staff.gym_staff_data'),
        ),
    ]
