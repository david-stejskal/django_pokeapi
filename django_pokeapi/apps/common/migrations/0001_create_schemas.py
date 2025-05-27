from django.db import migrations

from django_pokeapi.utils import load_db_migration


class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.RunSQL(
            load_db_migration("common", "2025.3.23_1__create_schemes.sql")
        ),
    ]
