import os
import pickle
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

from utils.logger import get_logger

# --- Configuração via variáveis de ambiente ----------------------------------
DB_PATH    = os.getenv("DB_PATH",   "data/heat_exchanger.db")
MODEL_DIR  = os.getenv("MODEL_DIR", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

logger = get_logger(__name__)


def load_data(db_path: str) -> pd.DataFrame:
    logger.info("Conectando ao banco: %s", db_path)
    engine = create_engine(f"sqlite:///{db_path}")
    df = pd.read_sql_query(
        "SELECT timestamp, heat_efficiency FROM heat_exchanger ORDER BY timestamp",
        engine,
    )

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["day_index"] = (df["timestamp"] - df["timestamp"].min()).dt.days

    before = len(df)
    df = df.dropna(subset=["timestamp", "heat_efficiency"])
    dropped = before - len(df)
    if dropped:
        logger.warning("Removidos %d registro(s) com valores ausentes.", dropped)

    logger.info(
        "Dados carregados: %d registros | período: %s → %s",
        len(df),
        df["timestamp"].min().date(),
        df["timestamp"].max().date(),
    )
    return df


def train(X: np.ndarray, y: np.ndarray) -> LinearRegression:
    logger.info("Iniciando treino  modelo: LinearRegression")
    model = LinearRegression()
    model.fit(X, y)
    logger.info(
        "Treino concluído  coef=%.6f  intercept=%.4f",
        model.coef_[0],
        model.intercept_,
    )
    return model


def evaluate(model: LinearRegression, X: np.ndarray, y: np.ndarray) -> dict:
    cv_scores = cross_val_score(model, X, y, cv=5, scoring="r2")
    y_pred = model.predict(X)

    return {
        "mae":        mean_absolute_error(y, y_pred),
        "rmse":       root_mean_squared_error(y, y_pred),
        "r2":         r2_score(y, y_pred),
        "r2_cv_mean": cv_scores.mean(),
        "r2_cv_std":  cv_scores.std(),
        "trend":      model.coef_[0],
    }


def save_artifacts(model: LinearRegression, df: pd.DataFrame):
    os.makedirs(MODEL_DIR, exist_ok=True)
    artifact = {
        "model":       model,
        "origin_date": df["timestamp"].min(),
        "last_date":   df["timestamp"].max(),
    }
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(artifact, f)
    logger.info("Modelo salvo: %s", MODEL_PATH)


if __name__ == "__main__":
    df = load_data(DB_PATH)
    logger.debug(
        "Eficiência: min=%.2f%%  max=%.2f%%",
        df["heat_efficiency"].min(),
        df["heat_efficiency"].max(),
    )

    X = df[["day_index"]].values
    y = df["heat_efficiency"].values

    model   = train(X, y)
    metrics = evaluate(model, X, y)

    logger.info(
        "MAE=%.4f%%  RMSE=%.4f%%  R²=%.4f  R²_CV=%.4f±%.4f  Tendência=%.4f%%/dia",
        metrics["mae"],
        metrics["rmse"],
        metrics["r2"],
        metrics["r2_cv_mean"],
        metrics["r2_cv_std"],
        metrics["trend"],
    )

    save_artifacts(model, df)
