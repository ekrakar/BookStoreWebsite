# Generated by Django 2.2 on 2019-08-05 23:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('register', '0002_auto_20190805_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='credit_Card_Type',
            field=models.CharField(blank=True, choices=[('D', 'Discover'), ('V', 'Visa'), ('M', 'MasterCard'), ('A', 'American Express')], max_length=1),
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.BookInstance')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Order')),
            ],
        ),
    ]
