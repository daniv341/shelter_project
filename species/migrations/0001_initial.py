# Generado por create_objects.py -- revisar con `manage.py makemigrations --check`
# antes de aplicar; este archivo es un punto de partida, no reemplaza a
# makemigrations si el modelo tiene relaciones (FK/M2M) con otras apps.

import species.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.CharField(default=species.models.generate_ulid, editable=False, max_length=26, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[("active", "Activo"), ("blocked", "Bloqueado")], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Species',
                'verbose_name_plural': 'Species',
                'ordering': ['-created_at'],
            },
        ),
    ]
