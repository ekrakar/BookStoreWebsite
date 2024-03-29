# Generated by Django 2.2.4 on 2019-08-03 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_ID', models.CharField(max_length=10)),
                ('mailing_Address', models.CharField(blank=True, max_length=200)),
                ('billing_Address', models.CharField(blank=True, max_length=200)),
                ('credit_Card_Type', models.CharField(blank=True, choices=[('1', 'Visa'), ('2', 'MasterCard'), ('3', 'Discover'), ('4', 'American Express')], max_length=50)),
                ('credit_Card_Number', models.CharField(blank=True, max_length=20)),
                ('expiration_Date', models.DateField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
