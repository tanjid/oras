# Generated by Django 4.0.5 on 2022-08-23 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_supplier_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='category',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
