# ============================================================================
# MODELS.PY
# ============================================================================
# Definicja tabeli jako klasy SQLAlchemy (ORM). To jest "źródło prawdy"
# o strukturze — Alembic generuje/porównuje migracje na podstawie TEGO
# pliku (przez Base.metadata), a nie odwrotnie. W realnym projekcie
# tu rozrastałby się cały schemat; do laba jedna prosta tabela wystarczy.
# ============================================================================
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from sample_alembic_app.db import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
