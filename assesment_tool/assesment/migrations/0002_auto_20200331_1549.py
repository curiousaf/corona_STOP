# Generated by Django 3.0.4 on 2020-03-31 15:49

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('assesment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='output',
            name='region',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
