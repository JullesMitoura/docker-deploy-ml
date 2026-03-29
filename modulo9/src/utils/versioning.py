"""
versioning.py — Utilitários de versionamento manual de modelos.

Estratégia adotada (sem ferramenta externa):
  - Cada artefato é salvo com tag baseada em timestamp: model_YYYYMMDD_HHMMSS.pkl
  - model_latest.pkl é sempre sobrescrito apontando para a versão mais recente
  - registry.json registra todas as versões com metadados (métricas, data de treino)

Estrutura do models/ após dois treinos:
  models/
  ├── model_20240101_143052.pkl   ← versão 1
  ├── model_20240102_091823.pkl   ← versão 2
  ├── model_latest.pkl             ← cópia da versão mais recente
  └── registry.json                ← índice de todas as versões
"""

import json
import os
import shutil
from datetime import datetime

REGISTRY_FILENAME = "registry.json"


def make_version_tag() -> str:
    """Gera tag de versão com timestamp: YYYYMMDD_HHMMSS."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def model_filename(version_tag: str) -> str:
    return f"model_{version_tag}.pkl"


def _registry_path(model_dir: str) -> str:
    return os.path.join(model_dir, REGISTRY_FILENAME)


def load_registry(model_dir: str) -> dict:
    """Lê o registry.json. Retorna estrutura vazia se não existir."""
    path = _registry_path(model_dir)
    if not os.path.exists(path):
        return {"latest": None, "versions": {}}
    with open(path) as f:
        return json.load(f)


def save_registry(model_dir: str, version_tag: str, metrics: dict) -> None:
    """Registra uma nova versão no registry.json e atualiza o ponteiro 'latest'."""
    registry = load_registry(model_dir)
    registry["latest"] = version_tag
    registry["versions"][version_tag] = {
        "file":       model_filename(version_tag),
        "trained_at": datetime.now().isoformat(timespec="seconds"),
        "metrics":    {k: round(float(v), 6) for k, v in metrics.items()},
    }
    with open(_registry_path(model_dir), "w") as f:
        json.dump(registry, f, indent=2)


def promote_to_latest(model_dir: str, version_tag: str) -> str:
    """Copia o artefato versionado para model_latest.pkl."""
    src  = os.path.join(model_dir, model_filename(version_tag))
    dest = os.path.join(model_dir, "model_latest.pkl")
    shutil.copy2(src, dest)
    return dest


def resolve_model_path(model_dir: str, version_tag: str | None = None) -> str:
    """
    Retorna o caminho do artefato para uma versão específica ou para a mais recente.

    Se version_tag for None, usa o 'latest' do registry.
    Se o registry não existir, cai no model_latest.pkl (compatibilidade com módulos anteriores).
    """
    if version_tag:
        return os.path.join(model_dir, model_filename(version_tag))

    registry = load_registry(model_dir)
    latest = registry.get("latest")
    if latest:
        return os.path.join(model_dir, model_filename(latest))

    # fallback: compatível com módulos 3 e 4
    return os.path.join(model_dir, "model_latest.pkl")


def list_versions(model_dir: str) -> list[dict]:
    """Retorna lista de versões registradas, ordenadas da mais recente para a mais antiga."""
    registry = load_registry(model_dir)
    versions = []
    for tag, meta in registry.get("versions", {}).items():
        versions.append({"version": tag, **meta})
    return sorted(versions, key=lambda v: v["version"], reverse=True)
