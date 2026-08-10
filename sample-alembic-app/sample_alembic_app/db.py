# ============================================================================
# DB.PY
# ============================================================================
# Konfiguracja połączenia z bazą — jedno miejsce, z którego korzysta
# zarówno appka (main.py), jak i Alembic (alembic/env.py), żeby nie
# duplikować connection stringa w dwóch miejscach.
#
# DATABASE_URL czytany ze zmiennej środowiskowej — w K8s wstrzykniesz go
# przez Deployment appki (env / envFrom), w Compose lokalnie analogicznie.
# Fallback (wartość po "or") to dane developerskie, gdybyś odpalał appkę
# całkiem lokalnie bez żadnego env — dopasuj do swojego lokalnego Postgresa
# jeśli będziesz testować poza K8s.
# ============================================================================
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://labuser:labpassword@localhost:5432/labdb",
)

# echo=False żeby nie zalewać logów całym SQL-em; ustaw True do debugowania
engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base — z niego dziedziczą wszystkie modele (models.py); Alembic też
# go używa (przez target_metadata w env.py) żeby wiedzieć jaki schema
# POWINIEN istnieć i porównać go z tym co faktycznie jest w bazie.
Base = declarative_base()


def get_db():
    """Dependency dla FastAPI — otwiera sesję na czas requestu, zamyka po."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
