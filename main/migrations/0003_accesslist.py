# Generated by Django 4.2.1 on 2023-05-12 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_device'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_type', models.IntegerField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.device')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
