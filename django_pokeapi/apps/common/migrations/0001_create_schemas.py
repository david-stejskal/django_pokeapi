from django.db import migrations

from django_pokeapi.utils import load_db_sql_migration


class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.RunSQL(
            load_db_sql_migration("common", "2025.5.26_1__create_schemes.sql")
        ),
    ]
