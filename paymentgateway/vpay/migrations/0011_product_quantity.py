# Generated by Django 4.1.2 on 2022-11-10 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpay', '0010_totalnumber_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
