"""
app.py  API de inferência do trocador de calor (FastAPI)

Endpoints:
  GET  /              → informações da API e versão do modelo carregado
  GET  /health        → health check para load balancers e orquestradores
  POST /predict/date  → prediz eficiência para uma data informada
  POST /predict/efficiency → estima a data para uma eficiência alvo
  GET  /versions      → lista versões disponíveis no registry
"""

import os
import pickle
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from utils.logger import get_logger
from utils.versioning import resolve_model_path, list_versions

# --- Configuração via variáveis de ambiente ----------------------------------
MODEL_DIR     = os.getenv("MODEL_DIR",     "models")
MODEL_VERSION = os.getenv("MODEL_VERSION", "")   # "" → usa latest
PORT          = int(os.getenv("PORT",      "8000"))

logger = get_logger(__name__)

# Estado global  carregado uma única vez na inicialização da API
_model        = None
_origin_date  = None
_last_date    = None
_loaded_version = "desconhecida"


# =============================================================================
# Lifespan  carregamento do modelo na inicialização
#
# O contexto @asynccontextmanager permite rodar código de setup antes de
# a API começar a aceitar requisições e código de teardown ao encerrar.
# =============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    global _model, _origin_date, _last_date, _loaded_version

    model_path = resolve_model_path(MODEL_DIR, MODEL_VERSION or None)
    logger.info("Carregando modelo: %s", model_path)

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Modelo não encontrado em: {model_path}\n"
            "Monte o volume com os artefatos de treino:\n"
            "  docker run -v $(pwd)/models:/app/models heat-exchanger-serve"
        )

    with open(model_path, "rb") as f:
        artifact = pickle.load(f)

    _model         = artifact["model"]
    _origin_date   = artifact["origin_date"]
    _last_date     = artifact["last_date"]
    _loaded_version = artifact.get("version", "desconhecida")

    logger.info(
        "Modelo carregado  versão: %s | período: %s → %s",
        _loaded_version,
        _origin_date.date(),
        _last_date.date(),
    )

    yield  # API fica disponível aqui

    logger.info("Encerrando API")


# =============================================================================
# Instância da aplicação FastAPI
# =============================================================================
app = FastAPI(
    title="Heat Exchanger Inference API",
    description=(
        "API de predição de eficiência térmica do trocador de calor. "
        "Dois modos: prever eficiência por data, ou estimar data por eficiência alvo."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# =============================================================================
# Schemas de entrada (Pydantic valida automaticamente os tipos e formatos)
# =============================================================================
class DateRequest(BaseModel):
    date: str  # formato YYYY-MM-DD


class EfficiencyRequest(BaseModel):
    efficiency: float  # percentual de eficiência térmica


# =============================================================================
# Endpoints
# =============================================================================

@app.get("/")
def root():
    """Informações gerais da API."""
    return {
        "api":            "Heat Exchanger Inference API",
        "version":        "1.0.0",
        "model_version":  _loaded_version,
        "endpoints": {
            "health":              "GET  /health",
            "predict_by_date":     "POST /predict/date",
            "predict_by_efficiency": "POST /predict/efficiency",
            "list_versions":       "GET  /versions",
            "docs":                "GET  /docs",
        },
    }


@app.get("/health")
def health():
    """
    Health check  usado por load balancers, Kubernetes liveness probe, etc.
    Retorna 200 enquanto o modelo estiver carregado.
    """
    return {
        "status":        "ok",
        "model_version": _loaded_version,
        "model_dir":     MODEL_DIR,
    }


@app.post("/predict/date")
def predict_by_date(req: DateRequest):
    """
    Prevê a eficiência térmica para uma data informada.

    Exemplo de requisição:
      {"date": "2022-04-15"}

    Exemplo de resposta:
      {"input_date": "2022-04-15", "predicted_efficiency": 94.2341, "model_version": "..."}
    """
    try:
        target_date = pd.to_datetime(req.date)
    except Exception:
        raise HTTPException(
            status_code=422,
            detail=f"Formato de data inválido: '{req.date}'. Use YYYY-MM-DD.",
        )

    day_index = (target_date - _origin_date).days

    if day_index < 0:
        raise HTTPException(
            status_code=422,
            detail=f"Data anterior ao início do dataset ({_origin_date.date()}).",
        )

    efficiency = _model.predict([[day_index]])[0]
    logger.debug("Predict date → day_index=%d  eficiência=%.4f%%", day_index, efficiency)

    return {
        "input_date":           req.date,
        "predicted_efficiency": round(float(efficiency), 4),
        "model_version":        _loaded_version,
    }


@app.post("/predict/efficiency")
def predict_by_efficiency(req: EfficiencyRequest):
    """
    Estima a data em que o trocador atingirá uma eficiência alvo.

    Usa regressão inversa: y = a·x + b → x = (y − b) / a

    Exemplo de requisição:
      {"efficiency": 94.5}

    Exemplo de resposta:
      {"target_efficiency": 94.5, "predicted_date": "2022-04-03",
       "in_history": true, "model_version": "..."}
    """
    a             = _model.coef_[0]
    b             = _model.intercept_
    predicted_day = (req.efficiency - b) / a
    predicted_date = _origin_date + pd.Timedelta(days=round(predicted_day))
    in_history    = predicted_date.date() <= _last_date.date()

    logger.debug(
        "Predict efficiency → eficiência=%.4f%%  data=%s  histórico=%s",
        req.efficiency,
        predicted_date.date(),
        in_history,
    )

    return {
        "target_efficiency": req.efficiency,
        "predicted_date":    str(predicted_date.date()),
        "in_history":        in_history,
        "model_version":     _loaded_version,
    }


@app.get("/versions")
def get_versions():
    """Lista todas as versões de modelo registradas no registry.json."""
    versions = list_versions(MODEL_DIR)
    if not versions:
        return {"message": "Nenhuma versão registrada.", "versions": []}
    return {"latest": _loaded_version, "versions": versions}