# Generated by Django 4.2.7 on 2023-11-19 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('m_venta', '0029_alter_direcciondespacho_direccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direcciondespacho',
            name='direccion',
            field=models.CharField(max_length=100),
        ),
    ]
