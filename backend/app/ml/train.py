import os
import pandas as pd

from sklearn.ensemble import IsolationForest


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "security_events.csv"
)

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "anomaly_model.pkl"
)


def train_model():

    print("Loading dataset...")

    data = pd.read_csv(DATA_PATH)

    features = [
        "failed_logins",
        "request_count",
        "connection_count",
        "bytes_transferred"
    ]

    X = data[features]

    print("Training Isolation Forest...")

    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42
    )

    model.fit(X)

    import joblib

    joblib.dump(
        model,
        MODEL_PATH
    )

    print("Model trained successfully.")
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()