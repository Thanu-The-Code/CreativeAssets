# Generated by Django 4.2.14 on 2025-01-19 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laviapp', '0003_alter_order_payment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=15)),
                ('otp', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
