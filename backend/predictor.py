import joblib
import numpy as np
import pandas as pd
import shap
import os

#Features
FEATURES = [
    'gas_price_lag1',
    'gas_price_volatility',
    'vix',
    'co2_change',
    'days_to_next_cop',
    'cop_urgency',
    'is_cop_week',
    'recent_volatility',
    'momentum_4w',
    'momentum_12w',
    'regime'
]

BASE_VALUE = 0.7904   # From SHAP TreeExplainer on test set


class CarbonPredictor:
    """
    Loads xgb_tuned.pkl and scaler.pkl once at startup.
    Exposes predict() and shap_summary() methods.
    Thread-safe for FastAPI async context.
    """

    def __init__(self, models_dir: str):
        model_path  = os.path.join(models_dir, "xgb_tuned.pkl")
        scaler_path = os.path.join(models_dir, "scaler.pkl")

        # Validate files exist before loading
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                f"Copy xgb_tuned.pkl into backend/models/"
            )
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(
                f"Scaler not found at {scaler_path}. "
                f"Copy scaler.pkl into backend/models/"
            )

        print(f"[predictor] Loading model from {model_path}")
        self.model  = joblib.load(model_path)
        print(f"[predictor] Loading scaler from {scaler_path}")
        self.scaler = joblib.load(scaler_path)

        print("[predictor] Building SHAP TreeExplainer...")
        self.explainer  = shap.TreeExplainer(self.model)
        self.base_value = float(self.explainer.expected_value)
        print(f"[predictor] Ready. SHAP base value: {self.base_value:.4f}%")

        self._global_shap = {
            'momentum_4w'          : {'mean_abs': 0.9193, 'mean': -0.3755},
            'momentum_12w'         : {'mean_abs': 0.2649, 'mean': -0.1917},
            'recent_volatility'    : {'mean_abs': 0.1694, 'mean': -0.1694},
            'gas_price_volatility' : {'mean_abs': 0.1601, 'mean': -0.1007},
            'gas_price_lag1'       : {'mean_abs': 0.0707, 'mean': -0.0245},
            'vix'                  : {'mean_abs': 0.0575, 'mean': -0.0447},
            'co2_change'           : {'mean_abs': 0.0414, 'mean':  0.0106},
            'days_to_next_cop'     : {'mean_abs': 0.0259, 'mean':  0.0029},
            'cop_urgency'          : {'mean_abs': 0.0051, 'mean': -0.0009},
            'regime'               : {'mean_abs': 0.0034, 'mean':  0.0034},
            'is_cop_week'          : {'mean_abs': 0.0000, 'mean':  0.0000},
        }

    def _calculate_cop_urgency(self, days_to_next_cop: int) -> float:
        """
        Non-linear urgency score.
        Returns a value from 0 to 1 as COP approaches within 60 days.
        Beyond 60 days = 0 (no urgency).
        """
        if days_to_next_cop <= 60:
            return round(max(0.0, (60 - days_to_next_cop) / 60), 4)
        return 0.0

    def _build_feature_row(self, request_data: dict) -> pd.DataFrame:
        """
        Assembles a single-row DataFrame in the exact feature order
        the model was trained on. Calculates cop_urgency server-side.
        """
        cop_urgency = self._calculate_cop_urgency(
            request_data["days_to_next_cop"]
        )

        row = {
            "gas_price_lag1"       : request_data["gas_price_lag1"],
            "gas_price_volatility" : request_data["gas_price_volatility"],
            "vix"                  : request_data["vix"],
            "co2_change"           : request_data["co2_change"],
            "days_to_next_cop"     : float(request_data["days_to_next_cop"]),
            "cop_urgency"          : cop_urgency,
            "is_cop_week"          : float(request_data["is_cop_week"]),
            "recent_volatility"    : request_data["recent_volatility"],
            "momentum_4w"          : request_data["momentum_4w"],
            "momentum_12w"         : request_data["momentum_12w"],
            "regime"               : float(request_data["regime"]),
        }

        return pd.DataFrame([row], columns=FEATURES), cop_urgency

    def predict(self, request_data: dict) -> dict:
        """
        Full prediction pipeline:
        1. Build feature row
        2. Scale using fitted scaler
        3. XGBoost prediction
        4. SHAP values for this specific prediction
        5. Return structured result
        """
        X_raw, cop_urgency = self._build_feature_row(request_data)

        X_scaled = pd.DataFrame(
            self.scaler.transform(X_raw),
            columns=FEATURES
        )

        prediction = float(self.model.predict(X_scaled)[0])

        shap_vals_raw = self.explainer.shap_values(X_scaled)
        shap_row = shap_vals_raw[0]

        shap_dict = {
            feat: round(float(val), 6)
            for feat, val in zip(FEATURES, shap_row)
        }

        reconstructed = self.base_value + sum(shap_row)
        if abs(reconstructed - prediction) > 0.01:
            print(f"[predictor] SHAP sanity check warning: "
                  f"reconstructed={reconstructed:.4f} "
                  f"predicted={prediction:.4f}")

        return {
            "prediction_pct"   : round(prediction, 4),
            "direction"        : "UP" if prediction >= 0 else "DOWN",
            "base_value"       : round(self.base_value, 4),
            "shap_values"      : shap_dict,
            "cop_urgency_used" : cop_urgency,
            "feature_order"    : FEATURES,
        }

    def shap_summary(self) -> dict:
        return {
            "features"      : FEATURES,
            "mean_abs_shap" : {k: v['mean_abs']
                               for k, v in self._global_shap.items()},
            "mean_shap"     : {k: v['mean']
                               for k, v in self._global_shap.items()},
        }
