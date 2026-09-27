import os
import joblib
import numpy as np


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "anomaly_model.pkl"
)


class AnomalyDetector:

    def __init__(self):

        if not os.path.exists(MODEL_PATH):

            raise FileNotFoundError(
                "ML model not found. "
                "Run: python -m app.ml.train"
            )

        self.model = joblib.load(
            MODEL_PATH
        )

    def predict(
        self,
        failed_logins: int,
        request_count: int,
        connection_count: int,
        bytes_transferred: int
    ):

        data = np.array([[
            failed_logins,
            request_count,
            connection_count,
            bytes_transferred
        ]])

        prediction = self.model.predict(data)

        # Isolation Forest:
        #  1  = normal
        # -1  = anomaly

        return prediction[0] == -1


def calculate_risk_score(
    severity: str,
    anomaly: bool
):

    severity_scores = {
        "Low": 20,
        "Medium": 50,
        "High": 80,
        "Critical": 95
    }

    score = severity_scores.get(
        severity,
        20
    )

    if anomaly:
        score += 10

    return min(score, 100)