# ============================================================================
# ALEMBIC/ENV.PY
# ============================================================================
# Ten plik Alembic odpala przy KAŻDYM `alembic upgrade`/`downgrade`/`revision`.
# Dwie kluczowe rzeczy które tu robimy inaczej niż domyślny szkielet Alembika:
#
# 1. Nadpisujemy sqlalchemy.url wartością z DATABASE_URL (env var) zamiast
#    trzymać connection string w alembic.ini — żeby jeden i ten sam obraz
#    Dockera działał identycznie w Compose, w K8s Jobie, wszędzie, tylko
#    zmieniając env var, bez przebudowywania obrazu.
#
# 2. target_metadata wskazuje na Base.metadata z naszych modeli — to
#    umożliwia `alembic revision --autogenerate` (Alembic porówna modele
#    z aktualnym stanem bazy i sam zaproponuje migrację).
# ============================================================================
import os
from logging.config import fileConfig

from alembic import context
from sample_alembic_app.db import Base
from sample_alembic_app.models import (
    Item,  # noqa: F401 — import wymagany, żeby model zarejestrował się w Base.metadata
)
from sqlalchemy import engine_from_config, pool

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Nadpisanie URL-a z env var — to jest ten kluczowy trik z komentarza wyżej
database_url = os.environ.get("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Tryb offline — generuje SQL bez faktycznego połączenia z bazą (nieużywany w tym labie)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Tryb online — faktyczne połączenie z bazą i wykonanie migracji. Tego używamy."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
