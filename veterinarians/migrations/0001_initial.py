# Generado por create_objects.py -- revisar con `manage.py makemigrations --check`
# antes de aplicar; este archivo es un punto de partida, no reemplaza a
# makemigrations si el modelo tiene relaciones (FK/M2M) con otras apps.

import veterinarians.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Veterinatian',
            fields=[
                ('id', models.CharField(default=veterinarians.models.generate_ulid, editable=False, max_length=26, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[("active", "Activo"), ("blocked", "Bloqueado")], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Veterinatian',
                'verbose_name_plural': 'Veterinarians',
                'ordering': ['-created_at'],
            },
        ),
    ]
