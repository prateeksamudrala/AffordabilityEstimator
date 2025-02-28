# Generated by Django 5.1.6 on 2025-02-28 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AffordabilityInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('income', models.FloatField()),
                ('down_payment', models.FloatField()),
                ('loan_term', models.IntegerField()),
                ('interest_rate', models.FloatField()),
            ],
        ),
    ]
