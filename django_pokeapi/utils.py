from pathlib import Path

from django.apps import apps


def _load_sql_file(
    app_label: str, resource_file: str, resource_location: tuple[str, str]
) -> str:
    file = (
        Path(apps.get_app_config(app_label).path)
        .joinpath(*resource_location)
        .joinpath(resource_file)
    )

    with file.open("r", encoding="utf-8") as fd:
        return fd.read()


def load_db_sql_migration(
    app_label: str,
    migration_file: str,
    migration_loc: tuple[str, str] = ("resources", "migrations"),
) -> str:
    return _load_sql_file(app_label, migration_file, migration_loc)
