# Generated by Django 4.2.7 on 2023-11-22 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('m_venta', '0030_alter_direcciondespacho_direccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direcciondespacho',
            name='ciudad',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='direcciondespacho',
            name='comuna',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='direcciondespacho',
            name='direccion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
