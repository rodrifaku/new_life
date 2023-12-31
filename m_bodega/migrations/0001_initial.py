# Generated by Django 4.2.7 on 2023-11-21 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('m_venta', '0030_alter_direcciondespacho_direccion'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenDespacho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_orden', models.CharField(max_length=20, unique=True)),
                ('despachado', models.BooleanField(default=False)),
                ('boleta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='m_venta.venta')),
            ],
        ),
    ]
