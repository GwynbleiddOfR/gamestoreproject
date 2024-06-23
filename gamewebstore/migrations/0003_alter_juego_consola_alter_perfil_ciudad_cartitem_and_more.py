# Generated by Django 5.0.6 on 2024-06-23 05:03

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamewebstore', '0002_alter_juego_consola_perfil'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='juego',
            name='consola',
            field=models.CharField(choices=[('PS2', 'PLAYSTATION 2'), ('PS3', 'PLAYSTATION 3'), ('PS5', 'PLAYSTATION 5'), ('PS1', 'PLAYSTATION 1'), ('PS4', 'PLAYSTATION 4')], max_length=3),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='ciudad',
            field=models.CharField(choices=[('Santiago', 'Santiago'), ('Valparaíso', 'Valparaíso'), ('Concepción', 'Concepción')], max_length=15),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('precio_por_item', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('juego', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamewebstore.juego', verbose_name='Juego')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('items', models.ManyToManyField(related_name='carts', to='gamewebstore.cartitem', verbose_name='Ítems')),
            ],
        ),
    ]