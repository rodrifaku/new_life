# Generated by Django 4.2.6 on 2023-10-25 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('m_venta', '0019_categoria_producto_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='foto',
            field=models.ImageField(null=True, upload_to='img'),
        ),
    ]
