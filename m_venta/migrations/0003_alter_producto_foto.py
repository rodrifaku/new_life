# Generated by Django 4.2.2 on 2023-06-24 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('m_venta', '0002_alter_detalleventa_options_alter_producto_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='foto',
            field=models.ImageField(null=True, upload_to='img/'),
        ),
    ]
