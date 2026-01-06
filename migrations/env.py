
import asyncio
import importlib
import os
import pkgutil
import re
import sys
from logging.config import fileConfig
from pathlib import Path
import app.infrastructure.models
from alembic import context

# Ajuste mínimo de sys.path (idealmente no lo necesitarías si instalas el paquete)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Importa Base y el engine Async desde tu app
from app.infrastructure.core.database import Base, engine  # noqa: E402

config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# --- Cargar modelos automáticamente para poblar Base.metadata ---
def _import_all_models(package_name: str = "app.infrastructure.models") -> None:
    """
    Importa todos los submódulos del paquete de modelos para asegurar
    que se registren en Base.metadata.
    """
    try:
        pkg = importlib.import_module(package_name)
    except Exception:
        # Si el paquete no existe o falla, no rompemos aquí;
        # Alembic fallará más adelante si no encuentra metadata.
        return

    for m in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
        try:
            importlib.import_module(m.name)
        except Exception:
            # Si un modelo revienta al importarse, mejor fallar explícitamente
            # en vez de migrar con metadata incompleta.
            raise


_import_all_models()

target_metadata = Base.metadata


# --- Alinear sqlalchemy.url (offline y tooling) con el engine real ---
def _set_sqlalchemy_url_from_engine() -> None:
    """
    Mantiene consistente la URL usada por Alembic.
    - Prioridad:
      1) Si engine expone .url, úsala.
      2) Si no, respeta el alembic.ini (sqlalchemy.url).
    """
    try:
        url = str(engine.url)  # AsyncEngine normalmente expone .url
        if url:
            config.set_main_option("sqlalchemy.url", url)
    except Exception:
        pass


_set_sqlalchemy_url_from_engine()


# --- Excluir tablas vía alembic.ini ---
_raw_exclude = config.get_main_option("exclude", "") or ""
exclude_tables = [t for t in re.sub(r"\s+", "", _raw_exclude).split(",") if t]


def include_object(object_, name, type_, reflected, compare_to):
    """
    Filtro para autogenerate.

    Como estás trabajando en schema public (por defecto), ignoramos cualquier
    tabla en schemas distintos. Esto reduce ruido si existieran schemas extras.
    """
    if type_ == "table":
        # Schema del objeto (None equivale al default schema)
        schema = getattr(object_, "schema", None)
        if schema not in (None, "public"):
            return False

        if name in exclude_tables or name in ("alembic_version", "spatial_ref_sys"):
            return False

    return True


def run_migrations_offline() -> None:
    """
    Modo offline: genera SQL sin conectarse a la DB.
    Importante: mantener flags consistentes con online.
    """
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        raise RuntimeError(
            "sqlalchemy.url está vacío. Configúralo o expón engine.url correctamente.")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        compare_type=True,
        # Actívalo si de verdad lo necesitas (puede generar falsos positivos):
        # compare_server_default=True,
        include_schemas=False,          # trabajas en public
        version_table_schema="public",  # alembic_version en public
    )

    with context.begin_transaction():
        context.run_migrations()


def _do_run_migrations(connection) -> None:
    """
    Configuración central (reutilizada por online).
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
        compare_type=True,
        # Actívalo si de verdad lo necesitas (puede generar falsos positivos):
        # compare_server_default=True,
        include_schemas=False,          # trabajas en public
        version_table_schema="public",  # alembic_version en public
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Modo online: conecta a la DB (AsyncEngine) y ejecuta migraciones.
    """
    async with engine.connect() as connection:
        await connection.run_sync(_do_run_migrations)

    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
