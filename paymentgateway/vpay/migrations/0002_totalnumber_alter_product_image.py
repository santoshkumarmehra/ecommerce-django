# Generated by Django 4.1.2 on 2022-11-03 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpay', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, max_length=5000, null=True, upload_to='images/'),
        ),
    ]
