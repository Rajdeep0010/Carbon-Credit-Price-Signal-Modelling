import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
import os


st.set_page_config(
    page_title="Carbon Signal",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)


BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Barlow+Condensed:wght@300;400;600;700;900&family=Barlow:wght@300;400;500&display=swap');

/* ── Root variables ─────────────────────────────────── */
:root {
    --bg-void:      #06080F;
    --bg-deep:      #0C1018;
    --bg-card:      #111520;
    --bg-raised:    #181D2A;
    --border:       #1E2535;
    --border-glow:  #2A3550;
    --green:        #00D084;
    --green-dim:    #00A86820;
    --green-mid:    #00D08440;
    --red:          #FF4757;
    --red-dim:      #FF475720;
    --amber:        #FFB020;
    --amber-dim:    #FFB02020;
    --blue:         #4DA6FF;
    --blue-dim:     #4DA6FF15;
    --text-bright:  #F0F4FF;
    --text-main:    #A8B2CC;
    --text-muted:   #4A5470;
    --text-ghost:   #2A3050;
    --mono:         'JetBrains Mono', monospace;
    --display:      'Barlow Condensed', sans-serif;
    --body:         'Barlow', sans-serif;
}

/* ── Base reset ─────────────────────────────────────── */
.stApp {
    background-color: var(--bg-void) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, #0D2A1A 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 80%, #0A1A2A 0%, transparent 50%);
    font-family: var(--body);
    color: var(--text-main);
}

.main .block-container {
    padding: 1.5rem 3rem 4rem 3rem;
    max-width: 1400px;
}

/* ── Hide Streamlit chrome ──────────────────────────── */
#MainMenu, footer, header, .stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
.viewerBadge_container__r5tak { display: none !important; }

/* ── Scrollbar ──────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-void); }
::-webkit-scrollbar-thumb { background: var(--border-glow); border-radius: 2px; }

/* ── Typography ─────────────────────────────────────── */
h1, h2, h3 { font-family: var(--display) !important; }

/* ── Tabs ───────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    color: var(--green) !important;
    border-bottom: 2px solid var(--green) !important;
    background: var(--green-dim) !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-main) !important;
    background: var(--blue-dim) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 2rem 0 0 0 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Sliders ────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] {
    padding: 0.2rem 0 !important;
}
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--green) !important;
    border: 2px solid var(--bg-card) !important;
    box-shadow: 0 0 8px var(--green-mid) !important;
    width: 14px !important;
    height: 14px !important;
}
.stSlider [data-baseweb="slider"] div[class*="thumb"] {
    background: var(--green) !important;
}
.stSlider [data-baseweb="slider"] div[class*="track"] div:first-child {
    background: var(--border) !important;
}
.stSlider [data-baseweb="slider"] div[class*="track"] div:nth-child(2) {
    background: var(--green) !important;
}
.stSlider label {
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}
.stSlider [data-testid="stTickBar"] { display: none !important; }

/* ── Number inputs ──────────────────────────────────── */
.stNumberInput input {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--text-bright) !important;
    font-family: var(--mono) !important;
    font-size: 0.85rem !important;
}
.stNumberInput input:focus {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 2px var(--green-mid) !important;
}

/* ── Selectbox ──────────────────────────────────────── */
.stSelectbox > div > div {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-bright) !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
}
.stSelectbox label {
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* ── Toggle / Checkbox ──────────────────────────────── */
.stCheckbox label {
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
    color: var(--text-main) !important;
}

/* ── Buttons ────────────────────────────────────────── */
.stButton > button {
    font-family: var(--display) !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--bg-void) !important;
    background: var(--green) !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    box-shadow: 0 0 20px var(--green-mid) !important;
}
.stButton > button:hover {
    background: #00E891 !important;
    box-shadow: 0 0 35px var(--green-mid) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Metrics ────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}
[data-testid="stMetricLabel"] {
    font-family: var(--mono) !important;
    font-size: 0.65rem !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--mono) !important;
    font-size: 1.4rem !important;
    color: var(--text-bright) !important;
    font-weight: 700 !important;
}

/* ── Divider ────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Expander ───────────────────────────────────────── */
.streamlit-expanderHeader {
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
    color: var(--text-muted) !important;
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
}

/* ── Spinner ────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: var(--green) !important;
}

/* ── DataFrame / Table ──────────────────────────────── */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div style="
        display: flex;
        align-items: center;
        gap: 1.5rem;
        padding: 2rem 0 1.5rem 0;
        border-bottom: 1px solid #1E2535;
        margin-bottom: 1.5rem;
    ">
        <div style="
            width: 52px; height: 52px;
            background: linear-gradient(135deg, #00D084, #006B44);
            border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.6rem;
            box-shadow: 0 0 24px #00D08440;
            flex-shrink: 0;
        ">🌿</div>
        <div>
            <div style="
                font-family: 'Barlow Condensed', sans-serif;
                font-size: 2.4rem;
                font-weight: 900;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #F0F4FF;
                line-height: 1;
            ">Carbon Signal</div>
            <div style="
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.68rem;
                color: #4A5470;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                margin-top: 0.25rem;
            ">EU ETS · Weekly Price Movement · XGBoost + SHAP</div>
        </div>
        <div style="margin-left: auto; text-align: right;">
            <div style="
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.6rem;
                color: #4A5470;
                text-transform: uppercase;
                letter-spacing: 0.1em;
            ">Model</div>
            <div style="
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.75rem;
                color: #00D084;
                margin-top: 0.1rem;
            ">xgb_tuned · v1.0</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_label(text):
    st.markdown(f"""
    <div style="
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        color: #4A5470;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        border-left: 2px solid #2A3550;
        padding-left: 0.6rem;
        margin: 1.4rem 0 0.8rem 0;
    ">{text}</div>
    """, unsafe_allow_html=True)


def render_prediction_card(pred_pct, direction):
    is_up     = direction == "UP"
    color     = "#00D084" if is_up else "#FF4757"
    bg_color  = "#00D08408" if is_up else "#FF475708"
    border_c  = "#00D08430" if is_up else "#FF475730"
    arrow     = "↑" if is_up else "↓"
    label     = "EXPECTED TO RISE" if is_up else "EXPECTED TO FALL"
    sign      = "+" if is_up else ""

    st.markdown(f"""
    <div style="
        background: {bg_color};
        border: 1px solid {border_c};
        border-radius: 12px;
        padding: 2rem 2.5rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 1.5rem;
    ">
        <div style="
            position: absolute; top: 0; left: 0; right: 0; height: 2px;
            background: linear-gradient(90deg, transparent, {color}, transparent);
        "></div>

        <div style="
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.62rem;
            color: {color};
            text-transform: uppercase;
            letter-spacing: 0.18em;
            margin-bottom: 0.75rem;
            opacity: 0.7;
        ">Predicted Weekly Movement</div>

        <div style="
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 5.5rem;
            font-weight: 900;
            color: {color};
            line-height: 1;
            letter-spacing: -0.02em;
        ">{sign}{pred_pct:.2f}%</div>

        <div style="
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 1.6rem;
            font-weight: 700;
            color: {color};
            letter-spacing: 0.2em;
            text-transform: uppercase;
            margin-top: 0.25rem;
            opacity: 0.85;
        ">{arrow} {label}</div>

        <div style="
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            color: #4A5470;
            margin-top: 1rem;
            letter-spacing: 0.08em;
        ">Base rate: +0.79% &nbsp;|&nbsp; Model confidence: directional</div>
    </div>
    """, unsafe_allow_html=True)


def render_shap_waterfall(shap_dict, base_value, final_pred):
    """Build a custom Plotly waterfall chart from SHAP values."""

    sorted_shap = sorted(shap_dict.items(), key=lambda x: abs(x[1]), reverse=True)
    features    = [s[0] for s in sorted_shap]
    values      = [s[1] for s in sorted_shap]

    colors = ["#00D084" if v >= 0 else "#FF4757" for v in values]

    feature_labels = {
        'momentum_4w'          : 'Momentum 4W',
        'momentum_12w'         : 'Momentum 12W',
        'recent_volatility'    : 'Recent Volatility',
        'gas_price_volatility' : 'Gas Price Volatility',
        'gas_price_lag1'       : 'Gas Price (lag)',
        'vix'                  : 'VIX Index',
        'co2_change'           : 'CO₂ Change',
        'days_to_next_cop'     : 'Days to COP',
        'cop_urgency'          : 'COP Urgency',
        'regime'               : 'Market Regime',
        'is_cop_week'          : 'COP Week',
    }

    labels   = [feature_labels.get(f, f) for f in features]
    measures = ['relative'] * len(values) + ['total']
    x_vals   = values + [None]
    y_labels = labels + ['Prediction']

    fig = go.Figure(go.Waterfall(
        orientation = "h",
        measure     = measures,
        x           = x_vals,
        y           = y_labels,
        base        = base_value,
        connector   = {"line": {"color": "#1E2535", "width": 1, "dash": "dot"}},
        decreasing  = {"marker": {"color": "#FF4757", "line": {"width": 0}}},
        increasing  = {"marker": {"color": "#00D084", "line": {"width": 0}}},
        totals      = {"marker": {"color": "#4DA6FF",
                                  "line": {"color": "#4DA6FF80", "width": 1}}},
        textposition = "outside",
        text        = [f"{'+' if v>0 else ''}{v:.3f}" for v in values] + [
                       f"{'+' if final_pred>0 else ''}{final_pred:.2f}%"],
        textfont    = {"family": "JetBrains Mono", "size": 10, "color": "#A8B2CC"},
    ))

    fig.add_vline(
        x=base_value, line_dash="dash",
        line_color="#FFB020", line_width=1, opacity=0.5
    )

    fig.add_annotation(
        x=base_value, y=len(y_labels) - 0.5,
        text=f"Base: {base_value:.2f}%",
        showarrow=False,
        font={"family": "JetBrains Mono", "size": 9, "color": "#FFB020"},
        bgcolor="#06080F", borderpad=3
    )

    fig.update_layout(
        title=dict(
            text="SHAP Contribution — What Drove This Prediction",
            font=dict(family="Barlow Condensed", size=16,
                      color="#A8B2CC"),
            x=0
        ),
        paper_bgcolor = "#06080F",
        plot_bgcolor  = "#06080F",
        font          = dict(family="JetBrains Mono", color="#A8B2CC"),
        height        = 440,
        margin        = dict(l=0, r=80, t=50, b=20),
        xaxis = dict(
            showgrid     = True,
            gridcolor    = "#1E2535",
            gridwidth    = 1,
            zeroline     = True,
            zerolinecolor= "#2A3550",
            tickfont     = dict(family="JetBrains Mono", size=9,
                                color="#4A5470"),
            title        = dict(text="SHAP Value (percentage points)",
                                font=dict(size=9, color="#4A5470")),
        ),
        yaxis = dict(
            showgrid  = False,
            tickfont  = dict(family="JetBrains Mono", size=10,
                             color="#A8B2CC"),
            autorange = "reversed",
        ),
        showlegend = False,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_scenario_context(inputs):
    """Generate plain-language context cards from input values."""

    gas   = inputs['gas_price_lag1']
    vix   = inputs['vix']
    days  = inputs['days_to_next_cop']
    m4    = inputs['momentum_4w']
    rv    = inputs['recent_volatility']

    gas_text  = "Below average — low energy pressure" if gas < 3 \
                else "Elevated — energy costs adding carbon demand" if gas > 6 \
                else "Moderate energy market conditions"
    gas_icon  = "🟢" if gas < 3 else "🔴" if gas > 6 else "🟡"

    vix_text  = "High fear — risk assets under pressure" if vix > 30 \
                else "Low anxiety — risk-on environment" if vix < 15 \
                else "Moderate market anxiety"
    vix_icon  = "🔴" if vix > 30 else "🟢" if vix < 15 else "🟡"

    cop_text  = "Summit imminent — urgency building" if days <= 30 \
                else "Approaching — pre-COP positioning" if days <= 60 \
                else "Distant — no immediate COP pressure"
    cop_icon  = "🔴" if days <= 30 else "🟡" if days <= 60 else "⚪"

    mom_text  = f"Strong upward momentum ({m4:+.1f}%)" if m4 > 5 \
                else f"Strong downward momentum ({m4:+.1f}%)" if m4 < -5 \
                else f"Neutral momentum ({m4:+.1f}%)"
    mom_icon  = "🟢" if m4 > 5 else "🔴" if m4 < -5 else "🟡"

    vol_text  = f"High volatility regime ({rv:.1f}%) — uncertain market" if rv > 8 \
                else f"Calm market ({rv:.1f}%) — stable conditions"
    vol_icon  = "🔴" if rv > 8 else "🟢"

    rows = [
        (gas_icon,  "Energy",     gas_text),
        (vix_icon,  "Sentiment",  vix_text),
        (cop_icon,  "COP",        cop_text),
        (mom_icon,  "Momentum",   mom_text),
        (vol_icon,  "Volatility", vol_text),
    ]

    html = """<div style="
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.6rem;
        margin-top: 0.5rem;
    ">"""
    for icon, label, text in rows:
        html += f"""
        <div style="
            background: #111520;
            border: 1px solid #1E2535;
            border-radius: 8px;
            padding: 0.75rem 1rem;
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
        ">
            <span style="font-size: 1.1rem; flex-shrink: 0;">{icon}</span>
            <div>
                <div style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.6rem;
                    color: #4A5470;
                    text-transform: uppercase;
                    letter-spacing: 0.1em;
                    margin-bottom: 0.2rem;
                ">{label}</div>
                <div style="
                    font-family: 'Barlow', sans-serif;
                    font-size: 0.78rem;
                    color: #A8B2CC;
                    line-height: 1.3;
                ">{text}</div>
            </div>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_feature_importance_chart():
    """Static SHAP summary from explainability notebook."""

    data = {
        'Feature'    : ['momentum_4w', 'momentum_12w', 'recent_volatility',
                         'gas_price_volatility', 'gas_price_lag1', 'vix',
                         'co2_change', 'days_to_next_cop', 'cop_urgency',
                         'regime', 'is_cop_week'],
        'Mean|SHAP|' : [0.9193, 0.2649, 0.1694, 0.1601, 0.0707,
                         0.0575, 0.0414, 0.0259, 0.0051, 0.0034, 0.0000],
        'Mean SHAP'  : [-0.3755, -0.1917, -0.1694, -0.1007, -0.0245,
                         -0.0447,  0.0106,  0.0029, -0.0009,  0.0034, 0.0000],
    }
    df = pd.DataFrame(data).sort_values('Mean|SHAP|')

    labels = {
        'momentum_4w'         : 'Momentum 4W',
        'momentum_12w'        : 'Momentum 12W',
        'recent_volatility'   : 'Recent Volatility',
        'gas_price_volatility': 'Gas Price Volatility',
        'gas_price_lag1'      : 'Gas Price (lag 1w)',
        'vix'                 : 'VIX Index',
        'co2_change'          : 'CO₂ Weekly Change',
        'days_to_next_cop'    : 'Days to Next COP',
        'cop_urgency'         : 'COP Urgency Score',
        'regime'              : 'Market Regime',
        'is_cop_week'         : 'Is COP Week',
    }
    df['Label'] = df['Feature'].map(labels)

    bar_colors = [
        "#00D084" if v > 0.05 else
        "#FFB020" if v > 0.01 else
        "#2A3550"
        for v in df['Mean|SHAP|']
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x             = df['Mean|SHAP|'],
        y             = df['Label'],
        orientation   = 'h',
        marker_color  = bar_colors,
        marker_line_width = 0,
        text          = [f"{v:.4f}" for v in df['Mean|SHAP|']],
        textposition  = 'outside',
        textfont      = dict(family="JetBrains Mono", size=9, color="#6B7280"),
    ))

    fig.update_layout(
        title=dict(
            text="Global Feature Importance — Mean |SHAP| on Test Set (2023–2026)",
            font=dict(family="Barlow Condensed", size=16, color="#A8B2CC"),
            x=0
        ),
        paper_bgcolor = "#06080F",
        plot_bgcolor  = "#06080F",
        height        = 400,
        margin        = dict(l=0, r=80, t=50, b=20),
        xaxis=dict(
            showgrid    = True,
            gridcolor   = "#1E2535",
            zeroline    = True,
            zerolinecolor= "#2A3550",
            tickfont    = dict(family="JetBrains Mono", size=9, color="#4A5470"),
            title       = dict(text="Mean |SHAP Value|",
                               font=dict(size=9, color="#4A5470")),
        ),
        yaxis=dict(
            showgrid = False,
            tickfont = dict(family="JetBrains Mono", size=10, color="#A8B2CC"),
        ),
        showlegend=False,
        bargap=0.35,
    )
    st.plotly_chart(fig, use_container_width=True)


def check_backend():
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=8)
        return r.status_code == 200
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════════════════════
#  RENDER
# ═══════════════════════════════════════════════════════════════════════════

render_header()

tab_predict, tab_performance, tab_about = st.tabs([
    "🎯  Predict",
    "📊  Model Performance",
    "ℹ️   About",
])


#Prediction
with tab_predict:

    col_inputs, col_gap, col_results = st.columns([4, 0.2, 6])

    with col_inputs:
        st.markdown("""
        <div style="
            background: #0C1018;
            border: 1px solid #1E2535;
            border-radius: 12px;
            padding: 1.5rem;
        ">
        <div style="
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 1.1rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #F0F4FF;
            margin-bottom: 0.25rem;
        ">Input Parameters</div>
        <div style="
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.62rem;
            color: #4A5470;
            margin-bottom: 1rem;
        ">Set market conditions for this week's scenario</div>
        </div>
        """, unsafe_allow_html=True)

        section_label("⚡  Energy Market")

        gas_price_lag1 = st.slider(
            "Gas Price Last Week ($/MMBtu)",
            min_value=1.0, max_value=15.0, value=3.5, step=0.1
        )
        gas_price_volatility = st.slider(
            "Gas Price Volatility — 4w % std",
            min_value=0.0, max_value=30.0, value=8.2, step=0.1
        )

        section_label("😰  Market Sentiment")

        vix = st.slider(
            "VIX — Market Fear Index",
            min_value=9.0, max_value=80.0, value=22.5, step=0.5
        )

        section_label("🌍  Climate Signal")

        co2_change = st.slider(
            "Weekly CO₂ Change (ppm)",
            min_value=-0.50, max_value=0.85, value=0.08, step=0.01
        )

        section_label("📅  COP Summit")

        days_to_next_cop = st.slider(
            "Days to Next COP Summit",
            min_value=0, max_value=365, value=45, step=1
        )
        is_cop_week = st.checkbox("This week IS a COP summit week", value=False)

        # Auto-calculate cop_urgency
        cop_urgency = max(0.0, (60 - days_to_next_cop) / 60) \
                      if days_to_next_cop <= 60 else 0.0

        st.markdown(f"""
        <div style="
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            color: #FFB020;
            background: #FFB02010;
            border: 1px solid #FFB02030;
            border-radius: 6px;
            padding: 0.5rem 0.75rem;
            margin: 0.3rem 0 0.8rem 0;
        ">
            ↳ COP urgency auto-calculated:
            <strong style="color: #FFD070;">{cop_urgency:.3f}</strong>
        </div>
        """, unsafe_allow_html=True)

        section_label("📈  Carbon Market Memory")

        recent_volatility = st.slider(
            "Recent Volatility — 12w rolling std (%)",
            min_value=0.0, max_value=20.0, value=6.8, step=0.1
        )
        momentum_4w = st.slider(
            "4-Week Momentum (%)",
            min_value=-30.0, max_value=30.0, value=5.2, step=0.1
        )
        momentum_12w = st.slider(
            "12-Week Momentum (%)",
            min_value=-50.0, max_value=50.0, value=12.4, step=0.1
        )

        section_label("🔵  Market Regime")

        regime_label = st.selectbox(
            "Current market phase",
            options=[
                "Phase 0 — Pre-2018 · Low price · Dormant",
                "Phase 1 — 2018–2020 · Reform era · Awakening",
                "Phase 2 — Post-2021 · High price · Energy crisis"
            ],
            index=2
        )
        regime = int(regime_label.split("Phase ")[1][0])

        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("🔮  GENERATE PREDICTION")

    with col_results:

        if not predict_btn:
            st.markdown("""
            <div style="
                height: 420px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                border: 1px dashed #1E2535;
                border-radius: 12px;
                color: #2A3550;
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;">🌿</div>
                <div style="
                    font-family: 'Barlow Condensed', sans-serif;
                    font-size: 1.3rem;
                    font-weight: 600;
                    letter-spacing: 0.1em;
                    text-transform: uppercase;
                    margin-bottom: 0.5rem;
                ">Awaiting Signal</div>
                <div style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.65rem;
                    letter-spacing: 0.08em;
                ">Set parameters → click Predict</div>
            </div>
            """, unsafe_allow_html=True)

        else:
            payload = {
                "gas_price_lag1"       : gas_price_lag1,
                "gas_price_volatility" : gas_price_volatility,
                "vix"                  : vix,
                "co2_change"           : co2_change,
                "days_to_next_cop"     : days_to_next_cop,
                "cop_urgency"          : cop_urgency,
                "is_cop_week"          : int(is_cop_week),
                "recent_volatility"    : recent_volatility,
                "momentum_4w"          : momentum_4w,
                "momentum_12w"         : momentum_12w,
                "regime"               : regime
            }

            # ── Call FastAPI backend ───────────────────────────────────
            with st.spinner("Running model inference..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/predict",
                        json=payload,
                        timeout=15
                    )
                    response.raise_for_status()
                    result = response.json()

                    pred_pct   = result["prediction_pct"]
                    direction  = result["direction"]
                    base_value = result["base_value"]
                    shap_dict  = result["shap_values"]

                    render_prediction_card(pred_pct, direction)

                    render_shap_waterfall(shap_dict, base_value, pred_pct)

                    section_label("🗺️  Scenario Context")
                    render_scenario_context(payload)

                except requests.exceptions.ConnectionError:
                    st.markdown("""
                    <div style="
                        background: #FF475708;
                        border: 1px solid #FF475730;
                        border-radius: 12px;
                        padding: 2rem;
                        text-align: center;
                    ">
                        <div style="font-size: 2rem; margin-bottom: 1rem;">⚡</div>
                        <div style="
                            font-family: 'Barlow Condensed', sans-serif;
                            font-size: 1.2rem;
                            font-weight: 700;
                            color: #FF4757;
                            letter-spacing: 0.1em;
                            text-transform: uppercase;
                            margin-bottom: 0.5rem;
                        ">Backend Waking Up</div>
                        <div style="
                            font-family: 'JetBrains Mono', monospace;
                            font-size: 0.68rem;
                            color: #6B7280;
                            line-height: 1.6;
                        ">
                            The prediction server is cold-starting.<br>
                            This takes 10–15 seconds on Railway free tier.<br>
                            Please wait a moment and try again.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                except requests.exceptions.HTTPError as e:
                    st.error(f"Backend error: {e}")

                except Exception as e:
                    st.error(f"Unexpected error: {e}")


# ──────────────────────────────────────────────────────────────────────────
#  TAB 2 — MODEL PERFORMANCE
# ──────────────────────────────────────────────────────────────────────────
with tab_performance:

    st.markdown("""
    <div style="
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #F0F4FF;
        margin-bottom: 0.25rem;
    ">Model Performance Report</div>
    <div style="
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: #4A5470;
        margin-bottom: 1.5rem;
    ">XGBoost · Test period: January 2023 — April 2026 · 173 weekly observations</div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4_col = st.columns(4)
    with m1:
        st.metric("R² Score", "—",
                  help="Proportion of variance explained by the model")
    with m2:
        st.metric("MAE", "— %",
                  help="Mean absolute error on weekly % change")
    with m3:
        st.metric("RMSE", "— %",
                  help="Root mean squared error on weekly % change")
    with m4_col:
        st.metric("Directional Acc.", "— %",
                  help="% of weeks where UP/DOWN direction was correct")

    st.markdown("""
    <div style="
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        color: #FFB020;
        background: #FFB02010;
        border: 1px solid #FFB02020;
        border-radius: 6px;
        padding: 0.5rem 0.75rem;
        margin: 0.5rem 0 1.5rem 0;
    ">
        ⚠ Run the backend API (GET /model-info) to populate live metrics
        from the trained model. Values shown as — until connected.
    </div>
    """, unsafe_allow_html=True)

    render_feature_importance_chart()

    section_label("🔬  Key SHAP Findings")

    findings = [
        ("momentum_4w dominates",
         "4-week carbon price momentum has 3.5× more predictive power than any other feature. "
         "Mean |SHAP| of 0.9193 — carbon markets have strong short-term memory."),
        ("is_cop_week is dead",
         "SHAP value of exactly 0.000 across all 173 test weeks. The binary COP week flag "
         "adds zero information once momentum and volatility are accounted for."),
        ("Energy is secondary",
         "gas_price_lag1 and gas_price_volatility together contribute less than momentum_4w alone. "
         "This challenges the conventional energy-carbon narrative for recent post-2023 prices."),
        ("VIX matters modestly",
         "Mean SHAP of -0.0447 shows VIX exerts a consistent downward drag — market fear "
         "suppresses carbon prices. But the effect is small relative to momentum."),
    ]

    cols = st.columns(2)
    for i, (title, body) in enumerate(findings):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="
                background: #111520;
                border: 1px solid #1E2535;
                border-left: 3px solid #00D084;
                border-radius: 8px;
                padding: 1rem 1.2rem;
                margin-bottom: 0.8rem;
            ">
                <div style="
                    font-family: 'Barlow Condensed', sans-serif;
                    font-size: 0.95rem;
                    font-weight: 700;
                    color: #F0F4FF;
                    letter-spacing: 0.05em;
                    margin-bottom: 0.4rem;
                ">{title}</div>
                <div style="
                    font-family: 'Barlow', sans-serif;
                    font-size: 0.78rem;
                    color: #6B7280;
                    line-height: 1.5;
                ">{body}</div>
            </div>
            """, unsafe_allow_html=True)

with tab_about:

    col_about1, col_about2 = st.columns([5, 5])

    with col_about1:
        st.markdown("""
        <div style="
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: #F0F4FF;
            margin-bottom: 1rem;
        ">About This System</div>
        """, unsafe_allow_html=True)

        about_items = [
            ("Model",         "XGBoost Regressor (xgb_tuned)"),
            ("Target",        "Weekly % change in EU ETS carbon futures"),
            ("Train period",  "April 2015 — December 2022 · 404 weeks"),
            ("Test period",   "January 2023 — April 2026 · 173 weeks"),
            ("Features",      "11 engineered predictors"),
            ("Explainability","SHAP TreeExplainer"),
            ("Architecture",  "Streamlit + FastAPI + Railway"),
        ]

        for label, value in about_items:
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: baseline;
                gap: 1rem;
                padding: 0.6rem 0;
                border-bottom: 1px solid #1E2535;
            ">
                <div style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.65rem;
                    color: #4A5470;
                    text-transform: uppercase;
                    letter-spacing: 0.1em;
                    min-width: 120px;
                ">{label}</div>
                <div style="
                    font-family: 'Barlow', sans-serif;
                    font-size: 0.83rem;
                    color: #A8B2CC;
                ">{value}</div>
            </div>
            """, unsafe_allow_html=True)

        section_label("📚  Data Sources")
        sources = [
            ("EU ETS Carbon Futures", "Investing.com — weekly OHLC"),
            ("Henry Hub Gas Price",   "EIA.gov — weekly spot price"),
            ("VIX Index",             "Yahoo Finance via yfinance"),
            ("CO₂ Concentration",     "NOAA Mauna Loa Observatory"),
            ("COP Summit Dates",      "UNFCCC — engineered proximity features"),
        ]
        for name, src in sources:
            st.markdown(f"""
            <div style="
                display: flex; align-items: baseline; gap: 0.75rem;
                padding: 0.45rem 0;
                border-bottom: 1px solid #1A2030;
            ">
                <div style="color: #00D084; font-size: 0.7rem;">▸</div>
                <div>
                    <div style="
                        font-family: 'Barlow', sans-serif;
                        font-size: 0.8rem; color: #A8B2CC;
                    ">{name}</div>
                    <div style="
                        font-family: 'JetBrains Mono', monospace;
                        font-size: 0.6rem; color: #4A5470;
                    ">{src}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_about2:
        section_label("🧬  Feature Dictionary")
        features_info = [
            ("gas_price_lag1",       "$/MMBtu", "Henry Hub spot price — previous week"),
            ("gas_price_volatility", "%",       "4-week rolling std of gas price % change"),
            ("vix",                  "index",   "CBOE Volatility Index — market fear"),
            ("co2_change",           "ppm",     "Weekly change in Mauna Loa CO₂ reading"),
            ("days_to_next_cop",     "days",    "Calendar days until next COP summit"),
            ("cop_urgency",          "0–1",     "Non-linear urgency score — peaks at 0 days"),
            ("is_cop_week",          "0/1",     "Binary flag — 1 if COP occurs this week"),
            ("recent_volatility",    "%",       "12-week rolling std of carbon % change"),
            ("momentum_4w",          "%",       "Carbon price % change over 4 weeks"),
            ("momentum_12w",         "%",       "Carbon price % change over 12 weeks"),
            ("regime",               "0/1/2",   "Market phase — pre-2018 / 2018-20 / post-21"),
        ]
        for feat, unit, desc in features_info:
            st.markdown(f"""
            <div style="
                background: #0C1018;
                border: 1px solid #1E2535;
                border-radius: 6px;
                padding: 0.6rem 0.9rem;
                margin-bottom: 0.4rem;
                display: flex;
                align-items: center;
                gap: 0.75rem;
            ">
                <div style="min-width: 165px;">
                    <div style="
                        font-family: 'JetBrains Mono', monospace;
                        font-size: 0.68rem; color: #00D084;
                    ">{feat}</div>
                    <div style="
                        font-family: 'JetBrains Mono', monospace;
                        font-size: 0.58rem; color: #4A5470;
                    ">{unit}</div>
                </div>
                <div style="
                    font-family: 'Barlow', sans-serif;
                    font-size: 0.75rem; color: #6B7280;
                    line-height: 1.4;
                ">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        section_label("⚙️  XGBoost Best Parameters")
        params = {
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
        params_html = ""
        for k, v in params.items():
            params_html += f"""
            <div style="
                display: flex; justify-content: space-between;
                padding: 0.35rem 0;
                border-bottom: 1px solid #1A2030;
            ">
                <span style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.68rem; color: #6B7280;
                ">{k}</span>
                <span style="
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.68rem; color: #00D084;
                ">{v}</span>
            </div>"""

        st.markdown(f"""
        <div style="
            background: #0C1018;
            border: 1px solid #1E2535;
            border-radius: 8px;
            padding: 0.75rem 1rem;
        ">{params_html}</div>
        """, unsafe_allow_html=True)


st.markdown("""
<div style="
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid #1E2535;
    display: flex;
    justify-content: space-between;
    align-items: center;
">
    <div style="
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        color: #2A3550;
        letter-spacing: 0.08em;
    ">Carbon Signal · EU ETS Prediction · XGBoost + SHAP · 2026</div>
    <div style="
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        color: #2A3550;
    ">Not financial advice · Research purposes only</div>
</div>
""", unsafe_allow_html=True)
