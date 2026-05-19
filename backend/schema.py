from pydantic import BaseModel, Field
from typing import Dict

# ── Input schema ────────────────────────────────────────────────────────────
class PredictRequest(BaseModel):
    gas_price_lag1       : float = Field(..., ge=1.0,   le=15.0,                                         description="Henry Hub gas price last week $/MMBtu")
    gas_price_volatility : float = Field(..., ge=0.0,   le=30.0,
                                        description="4-week rolling std of gas price % change")
    
    
    vix                  : float = Field(..., ge=9.0,   le=80.0,
                                        description="CBOE VIX market fear index")
    co2_change           : float = Field(..., ge=-0.5,  le=0.85,
                                        description="Weekly CO2 change in ppm")
    days_to_next_cop     : int   = Field(..., ge=0,     le=730,
                                        description="Days until next COP summit")
    is_cop_week          : int   = Field(..., ge=0,     le=1,
                                        description="1 if this week is a COP summit week")
    recent_volatility    : float = Field(..., ge=0.0,   le=20.0,
                                        description="12-week rolling std of carbon % change")
    momentum_4w          : float = Field(..., ge=-30.0, le=30.0,
                                        description="4-week carbon price momentum %")
    momentum_12w         : float = Field(..., ge=-50.0, le=50.0,
                                        description="12-week carbon price momentum %")
    regime               : int   = Field(..., ge=0,     le=2,
                                        description="Market regime: 0=pre-2018, 1=2018-20, 2=post-2021")

    class Config:
        json_schema_extra = {
            "example": {
                "gas_price_lag1"       : 3.50,
                "gas_price_volatility" : 8.20,
                "vix"                  : 22.50,
                "co2_change"           : 0.08,
                "days_to_next_cop"     : 45,
                "is_cop_week"          : 0,
                "recent_volatility"    : 6.80,
                "momentum_4w"          : 5.20,
                "momentum_12w"         : 12.40,
                "regime"               : 2
            }
        }


# ── Output schemas ──────────────────────────────────────────────────────────
class PredictResponse(BaseModel):
    prediction_pct   : float
    direction        : str
    base_value       : float
    shap_values      : Dict[str, float]
    cop_urgency_used : float
    feature_order    : list


class HealthResponse(BaseModel):
    status      : str
    model       : str
    version     : str
    base_value  : float


class ModelInfoResponse(BaseModel):
    model_name      : str
    target          : str
    features        : list
    train_period    : str
    test_period     : str
    n_train_weeks   : int
    n_test_weeks    : int
    best_params     : dict


class ShapSummaryResponse(BaseModel):
    features         : list
    mean_abs_shap    : Dict[str, float]
    mean_shap        : Dict[str, float]