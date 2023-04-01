# Generated by Django 3.2.7 on 2023-04-01 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodges', '0004_pop_searched'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]