# ============================================================================
# MAIN.PY
# ============================================================================
# Minimalna appka FastAPI z jednym endpointem, który robi realny INSERT
# do bazy — celowo prosta, bo jej jedynym zadaniem w tym labie jest
# udowodnić że: (1) migracja Alembika faktycznie utworzyła tabelę,
# (2) appka może z tą tabelą operować.
#
# WAŻNE: appka NIE odpala migracji sama z siebie (nie ma tu
# `alembic upgrade head` wewnątrz kodu Pythona) — to jest CELOWE.
# Migracje ma wykonywać osobny Job (PreSync hook w Argo), appka
# tylko zakłada że schema JUŻ istnieje, gdy startuje.
# ============================================================================
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from sample_alembic_app.db import get_db
from sample_alembic_app.models import Item

app = FastAPI(title="alembic-lab-app")


class ItemCreate(BaseModel):
    name: str


@app.get("/health")
def health():
    """Prosty healthcheck — przydatny później do readinessProbe/livenessProbe."""
    return {"status": "ok"}


@app.post("/items")
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    """Tworzy nowy rekord w tabeli items — dowód że migracja zadziałała."""
    item = Item(name=payload.name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name, "created_at": item.created_at}


@app.get("/items")
def list_items(db: Session = Depends(get_db)):
    """Lista wszystkich rekordów — do szybkiej weryfikacji że dane się zapisały."""
    items = db.query(Item).all()
    return [{"id": i.id, "name": i.name, "created_at": i.created_at} for i in items]
