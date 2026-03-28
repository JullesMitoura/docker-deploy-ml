import os
import pickle
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

# --- Configuração via variáveis de ambiente ----------------------------------
DB_PATH    = os.getenv("DB_PATH",   "data/heat_exchanger.db")
MODEL_DIR  = os.getenv("MODEL_DIR", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")


def load_data(db_path: str) -> pd.DataFrame:
    print(f"Carregando dados de: {db_path}")
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
        print(f"Removidos {dropped} registro(s) com valores ausentes.")

    print(
        f"Registros: {len(df)} | Período: "
        f"{df['timestamp'].min().date()} \u2192 {df['timestamp'].max().date()}"
    )
    return df


def train(X: np.ndarray, y: np.ndarray) -> LinearRegression:
    model = LinearRegression()
    model.fit(X, y)
    return model


def evaluate(model: LinearRegression, X: np.ndarray, y: np.ndarray):
    cv_scores = cross_val_score(model, X, y, cv=5, scoring="r2")
    y_pred = model.predict(X)

    return {
        "mae": mean_absolute_error(y, y_pred),
        "rmse": root_mean_squared_error(y, y_pred),
        "r2": r2_score(y, y_pred),
        "r2_cv_mean": cv_scores.mean(),
        "r2_cv_std": cv_scores.std(),
        "trend": model.coef_[0],
    }


def save_artifacts(model: LinearRegression, df: pd.DataFrame):
    os.makedirs(MODEL_DIR, exist_ok=True)
    artifact = {
        "model": model,
        "origin_date": df["timestamp"].min(),
        "last_date": df["timestamp"].max(),
    }
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(artifact, f)


if __name__ == "__main__":
    df = load_data(DB_PATH)
    print(
        "Eficiência: "
        f"min={df['heat_efficiency'].min():.2f}%  "
        f"max={df['heat_efficiency'].max():.2f}%"
    )

    X = df[["day_index"]].values
    y = df["heat_efficiency"].values

    print("\nTreinando modelo de regressão linear temporal...\n")
    model = train(X, y)
    metrics = evaluate(model, X, y)
    print("=== Métricas de Avaliação ===")
    print(f"  MAE       : {metrics['mae']:.4f}%")
    print(f"  RMSE      : {metrics['rmse']:.4f}%")
    print(f"  R²        : {metrics['r2']:.4f}")
    print(f"  R² CV (5) : {metrics['r2_cv_mean']:.4f} ± {metrics['r2_cv_std']:.4f}")
    print(f"  Tendência : {metrics['trend']:.4f}% por dia\n")

    save_artifacts(model, df)
    print(f"Modelo salvo em: {MODEL_PATH}")