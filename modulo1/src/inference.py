"""
inference.py — dois modos de uso:

  Modo 1 — prever eficiência para uma data:
    python src/inference.py --date 2022-04-15

  Modo 2 — estimar a data para uma eficiência alvo:
    python src/inference.py --efficiency 94.5
    python src/inference.py --efficiency 82      (extrapolação futura)
"""
import os
import argparse
import pickle
import pandas as pd

# --- Configuração via variáveis de ambiente ----------------------------------
MODEL_DIR  = os.getenv("MODEL_DIR", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
REFERENCE_PATH = os.path.join(MODEL_DIR, "reference_data.pkl")


def load_artifacts():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Modelo não encontrado em: {MODEL_PATH}\n"
            "Execute 'python src/train.py' primeiro."
        )
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    if not os.path.exists(REFERENCE_PATH):
        raise FileNotFoundError(
            f"Referência não encontrada em: {REFERENCE_PATH}\n"
            "Execute 'python src/train.py' para gerar os artefatos."
        )
    with open(REFERENCE_PATH, "rb") as f:
        df = pickle.load(f)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return model, df


def predict_efficiency(model, df: pd.DataFrame, date_str: str) -> dict:
    target_date = pd.to_datetime(date_str)
    origin      = df["timestamp"].min()
    day_index   = (target_date - origin).days

    if day_index < 0:
        raise ValueError(f"Data anterior ao início do dataset ({origin.date()}).")

    efficiency = model.predict([[day_index]])[0]
    closest    = df.iloc[(df["day_index"] - day_index).abs().argsort()[:1]]

    return {
        "input_date": date_str,
        "predicted_efficiency": round(float(efficiency), 4),
        "closest_historical_date": str(closest["timestamp"].iloc[0].date()),
        "closest_historical_efficiency": round(float(closest["heat_efficiency"].iloc[0]), 4),
    }


def find_date_for_efficiency(model, df: pd.DataFrame, target_efficiency: float, top_k: int = 3) -> dict:
    # Regressão inversa: y = a·x + b  →  x = (y − b) / a
    a              = model.coef_[0]
    b              = model.intercept_
    predicted_day  = (target_efficiency - b) / a
    origin         = df["timestamp"].min()
    predicted_date = origin + pd.Timedelta(days=round(predicted_day))
    in_history     = predicted_date.date() <= df["timestamp"].max().date()

    df = df.copy()
    df["diff"] = (df["heat_efficiency"] - target_efficiency).abs()
    historical = df.nsmallest(top_k, "diff")

    return {
        "target_efficiency": target_efficiency,
        "predicted_date": str(predicted_date.date()),
        "in_history": in_history,
        "historical_matches": [
            {
                "date": str(row["timestamp"].date()),
                "recorded_efficiency": round(float(row["heat_efficiency"]), 4),
                "delta": round(float(row["diff"]), 4),
            }
            for _, row in historical.iterrows()
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inferência — Trocador de Calor")
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--date",       type=str,   help="Data para prever eficiência (YYYY-MM-DD)")
    group.add_argument("--efficiency", type=float, help="Eficiência alvo para estimar a data")
    parser.add_argument("--top",       type=int, default=3, help="Número de registros históricos")
    args = parser.parse_args()

    model, df = load_artifacts()

    if args.date:
        result = predict_efficiency(model, df, args.date)
        print(f"Data informada        : {result['input_date']}")
        print(f"Eficiência prevista   : {result['predicted_efficiency']:.4f}%")
        print(
            "Referência histórica  : "
            f"{result['closest_historical_date']} "
            f"({result['closest_historical_efficiency']:.4f}%)"
        )
    else:
        result = find_date_for_efficiency(model, df, args.efficiency, top_k=args.top)
        print(f"Eficiência alvo       : {result['target_efficiency']:.4f}%")
        print(f"Data estimada         : {result['predicted_date']}")
        print(
            "Status                : "
            f"{'histórico' if result['in_history'] else 'extrapolação futura'}"
        )
        print("\nTop matches históricos:")
        for i, row in enumerate(result["historical_matches"], 1):
            print(
                f"  {i}. {row['date']} | "
                f"eficiência={row['recorded_efficiency']:.4f}% | "
                f"delta={row['delta']:.4f}%"
            )