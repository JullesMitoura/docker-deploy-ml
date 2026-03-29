"""
inference.py — dois modos de uso:

  Modo 1 — prever eficiência para uma data:
    python src/inference.py --date 2025-06-15

  Modo 2 — estimar a data para uma eficiência alvo:
    python src/inference.py --efficiency 80.0
    python src/inference.py --efficiency 60.0    (extrapolação futura)
"""

import os
import argparse
import pickle
import pandas as pd

from utils.logger import get_logger

# --- Configuração via variáveis de ambiente ----------------------------------
MODEL_DIR  = os.getenv("MODEL_DIR", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

logger = get_logger(__name__)


def load_artifacts():
    logger.info("Carregando modelo: %s", MODEL_PATH)
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Modelo não encontrado em: {MODEL_PATH}\n"
            "Monte o volume com o modelo treinado:\n"
            "  docker run -v $(pwd)/models:/app/models heat-exchanger-inference ..."
        )
    with open(MODEL_PATH, "rb") as f:
        artifact = pickle.load(f)
    logger.debug(
        "Artefato carregado — origem: %s  última data: %s",
        artifact["origin_date"].date(),
        artifact["last_date"].date(),
    )
    return artifact["model"], artifact["origin_date"], artifact["last_date"]


def predict_efficiency(model, origin_date, date_str: str) -> dict:
    target_date = pd.to_datetime(date_str)
    day_index   = (target_date - origin_date).days

    if day_index < 0:
        raise ValueError(f"Data anterior ao início do dataset ({origin_date.date()}).")

    efficiency = model.predict([[day_index]])[0]
    logger.debug("day_index=%d  eficiência prevista=%.4f%%", day_index, efficiency)

    return {
        "input_date":           date_str,
        "predicted_efficiency": round(float(efficiency), 4),
    }


def find_date_for_efficiency(model, origin_date, last_date, target_efficiency: float) -> dict:
    # Regressão inversa: y = a·x + b  →  x = (y − b) / a
    a             = model.coef_[0]
    b             = model.intercept_
    predicted_day = (target_efficiency - b) / a
    predicted_date = origin_date + pd.Timedelta(days=round(predicted_day))
    in_history    = predicted_date.date() <= last_date.date()

    logger.debug(
        "Regressão inversa — a=%.6f  b=%.4f  day=%.1f  data=%s  histórico=%s",
        a, b, predicted_day, predicted_date.date(), in_history,
    )

    return {
        "target_efficiency": target_efficiency,
        "predicted_date":    str(predicted_date.date()),
        "in_history":        in_history,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inferência — Trocador de Calor")
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--date",       type=str,   help="Data para prever eficiência (YYYY-MM-DD)")
    group.add_argument("--efficiency", type=float, help="Eficiência alvo para estimar a data")
    args = parser.parse_args()

    model, origin_date, last_date = load_artifacts()

    if args.date:
        result = predict_efficiency(model, origin_date, args.date)
        logger.info("Data informada      : %s", result["input_date"])
        logger.info("Eficiência prevista : %.4f%%", result["predicted_efficiency"])
    else:
        result = find_date_for_efficiency(model, origin_date, last_date, args.efficiency)
        logger.info("Eficiência alvo     : %.4f%%", result["target_efficiency"])
        logger.info("Data estimada       : %s", result["predicted_date"])
        logger.info(
            "Status              : %s",
            "histórico" if result["in_history"] else "extrapolação futura",
        )
