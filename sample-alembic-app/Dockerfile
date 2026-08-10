# ============================================================================
# DOCKERFILE
# ============================================================================
# Obraz budowany przez uv (szybszy niż pip). CMD odpala tylko serwer appki —
# CELOWO NIE robimy tu `alembic upgrade head && uvicorn ...` (tak jak w Compose
# wcześniej) — bo w K8s migracja ma być odpowiedzialnością OSOBNEGO Joba,
# nie tego samego kontenera co appka. Ten sam obraz jest używany zarówno
# przez Job (z command nadpisanym na `alembic upgrade head`), jak i przez
# Deployment appki (z domyślnym CMD poniżej) — stąd oba w jednym obrazie.
# ============================================================================
FROM python:3.12-slim

# uv jako statyczny binarek, kopiowany z oficjalnego obrazu uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

# Kopiujemy najpierw tylko pliki zależności — warstwa Dockera z zależnościami
# będzie cache'owana dopóki pyproject.toml się nie zmieni (szybsze rebuildy)
COPY pyproject.toml ./
RUN uv sync --no-dev

# Reszta kodu — ta warstwa zmienia się często, więc jest na końcu
COPY sample_alembic_app ./sample_alembic_app
COPY alembic ./alembic
COPY alembic.ini ./

# Domyślna komenda: odpala serwer appki. Job w K8s nadpisze to komendą
# `alembic upgrade head` (patrz: migration-job.yaml, który zrobimy dalej)
CMD ["uv", "run", "uvicorn", "sample_alembic_app.main:app", "--host", "0.0.0.0", "--port", "8000"]