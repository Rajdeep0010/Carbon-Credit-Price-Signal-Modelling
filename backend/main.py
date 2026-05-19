import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schema import (PredictRequest, PredictResponse,
                        HealthResponse, ModelInfoResponse,
                        ShapSummaryResponse)
from predictor import CarbonPredictor

# ── Models directory ────────────────────────────────────────────────────────
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")


# ── Lifespan — load model once at startup ───────────────────────────────────
# WHY lifespan instead of global variable:
# FastAPI's lifespan context manager guarantees the model is loaded
# before the first request arrives and cleaned up on shutdown.
# A plain global would initialise at import time which causes issues
# with some deployment environments.

predictor: CarbonPredictor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global predictor
    print("[startup] Loading CarbonPredictor...")
    start = time.time()
    predictor = CarbonPredictor(models_dir=MODELS_DIR)
    print(f"[startup] Ready in {time.time() - start:.2f}s")
    yield
    print("[shutdown] CarbonPredictor released")
    predictor = None


# ── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title       = "Carbon Signal API",
    description = (
        "EU ETS weekly carbon price movement predictor. "
        "XGBoost + SHAP · Trained 2015–2022 · Tested 2023–2026."
    ),
    version     = "1.0.0",
    lifespan    = lifespan,
    docs_url    = "/docs",
    redoc_url   = "/redoc",
)


# ── CORS — allow Streamlit Cloud and localhost ────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],   # tighten to your Streamlit URL in production
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["System"])
def health():
    """
    Health check endpoint.
    Called by Streamlit frontend on startup to verify backend is alive.
    Returns model name and SHAP base value.
    """
    if predictor is None:
        raise HTTPException(status_code=503,
                            detail="Model not loaded yet. Try again shortly.")
    return {
        "status"     : "ok",
        "model"      : "xgb_tuned",
        "version"    : "1.0.0",
        "base_value" : predictor.base_value,
    }


@app.post("/predict", response_model=PredictResponse, tags=["Prediction"])
def predict(request: PredictRequest):
    """
    Main prediction endpoint.

    Accepts 10 market input features.
    Returns predicted weekly % change, direction, SHAP values per feature.
    cop_urgency is calculated server-side from days_to_next_cop.
    """
    if predictor is None:
        raise HTTPException(status_code=503,
                            detail="Model not loaded. Please retry.")

    try:
        result = predictor.predict(request.model_dump())
        return result

    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Input error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Prediction failed: {str(e)}")


@app.get("/model-info", response_model=ModelInfoResponse, tags=["Model"])
def model_info():
    """
    Returns metadata about the trained model.
    Used by the About tab in the Streamlit frontend.
    """
    return {
        "model_name"    : "XGBoost Regressor (xgb_tuned)",
        "target"        : "carbon_price_change_pct — weekly % change in EU ETS futures",
        "features"      : [
            "gas_price_lag1", "gas_price_volatility", "vix", "co2_change",
            "days_to_next_cop", "cop_urgency", "is_cop_week",
            "recent_volatility", "momentum_4w", "momentum_12w", "regime"
        ],
        "train_period"  : "April 2015 — December 2022",
        "test_period"   : "January 2023 — April 2026",
        "n_train_weeks" : 404,
        "n_test_weeks"  : 173,
        "best_params"   : {
            "n_estimators"     : 400,
            "max_depth"        : 3,
            "learning_rate"    : 0.005,
            "subsample"        : 0.9,
            "colsample_bytree" : 0.7,
            "min_child_weight" : 3,
            "gamma"            : 1.0,
            "reg_alpha"        : 2.0,
            "reg_lambda"       : 1.0,
        }
    }

@app.get("/metrics", tags=["Model"])
def get_metrics():
    """
    Returns test set evaluation metrics.
    Update these values from your 05_model_training.ipynb output.
    """
    return {
        "r2"                  : 0.0,    # ← paste your actual value here
        "mae"                 : 0.0,    # ← paste your actual value here
        "rmse"                : 0.0,    # ← paste your actual value here
        "directional_accuracy": 0.0,    # ← paste your actual value here
        "test_period"         : "January 2023 — April 2026",
        "n_test_weeks"        : 173,
    }
@app.get("/shap-summary", response_model=ShapSummaryResponse, tags=["Model"])
def shap_summary():
    """
    Returns global SHAP statistics computed on the test set (2023–2026).
    Used by the Model Performance tab to render the feature importance chart.
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")

    return predictor.shap_summary()


@app.get("/", tags=["System"])
def root():
    return {
        "message"   : "Carbon Signal API is running.",
        "docs"      : "/docs",
        "endpoints" : ["/health", "/predict", "/model-info", "/shap-summary"]
    }