"""
Fuel Price Transmission Effect: India 2019–2025
Interactive Dashboard (Upgraded Version)
Author: Om Dadhe
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import f as f_dist
import warnings
warnings.filterwarnings("ignore")

# PAGE CONFIG
st.set_page_config(
    page_title="Fuel Price Transmission | India",
    layout="wide"
)

# COLORS
C_PETROL = "#C0392B"
C_DIESEL = "#1A5276"
C_BRENT = "#D35400"
C_CPI = "#117A65"

# LOAD DATA (SAFE)
@st.cache_data
def load_data():
    df = pd.read_csv("outputs/master_dataset.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df

try:
    master = load_data()
except:
    st.error("Master dataset not found. Run analysis script first.")
    st.stop()

# SIDEBAR
with st.sidebar:
    st.title("Fuel Price Transmission")
    page = st.radio("Navigation", [
        "Overview",
        "VAR Impulse Response",
        "Ridge vs ARIMA",
        "Regime Analysis",
        "Data"
    ])

# =========================================================
# OVERVIEW
# =========================================================
if page == "Overview":

    st.title("Fuel Price Transmission System")

    c1, c2, c3 = st.columns(3)

    petrol_chg = master["Petrol_RSP"].iloc[-1] / master["Petrol_RSP"].iloc[0] - 1
    diesel_chg = master["Diesel_RSP"].iloc[-1] / master["Diesel_RSP"].iloc[0] - 1
    cpi_chg = master["CPI_General"].iloc[-1] / master["CPI_General"].iloc[0] - 1

    c1.metric("Petrol Change", f"{petrol_chg*100:.1f}%")
    c2.metric("Diesel Change", f"{diesel_chg*100:.1f}%")
    c3.metric("CPI Change", f"{cpi_chg*100:.1f}%")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=master["date"], y=master["Petrol_RSP"], name="Petrol", line=dict(color=C_PETROL)))
    fig.add_trace(go.Scatter(x=master["date"], y=master["Diesel_RSP"], name="Diesel", line=dict(color=C_DIESEL)))
    fig.update_layout(title="Retail Fuel Prices")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# VAR IRF
# =========================================================
elif page == "VAR Impulse Response":

    st.title("VAR Impulse Response: Crude Shock to CPI")

    df = master[["Brent_USD", "CPI_General"]].dropna()

    # SIMPLE VAR(1)
    Y = df.values
    Y_lag = Y[:-1]
    Y_curr = Y[1:]

    X = np.column_stack([np.ones(len(Y_lag)), Y_lag])
    B = np.linalg.lstsq(X, Y_curr, rcond=None)[0]

    A = B[1:].T

    steps = 12
    irf = np.zeros((steps, 2))

    shock = np.array([1, 0])  # crude shock
    irf[0] = shock

    for t in range(1, steps):
        irf[t] = A @ irf[t-1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=irf[:,1], mode="lines+markers", name="CPI Response"))

    fig.update_layout(
        title="Impulse Response (Crude → CPI)",
        xaxis_title="Months",
        yaxis_title="Impact"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# RIDGE VS ARIMA
# =========================================================
elif page == "Ridge vs ARIMA":

    st.title("Model Comparison: Ridge vs ARIMA")

    df = master.dropna().copy()

    # FEATURES
    df["Brent_lag1"] = df["Brent_USD"].shift(1)
    df["Excise_lag1"] = df["Excise_Petrol"].shift(1)
    df["FX_lag1"] = df["USD_INR"].shift(1)

    df = df.dropna()

    X = df[["Brent_lag1", "Excise_lag1", "FX_lag1"]].values
    y = df["Petrol_RSP"].values

    # RIDGE
    lam = 0.5
    I = np.eye(X.shape[1])
    beta = np.linalg.inv(X.T @ X + lam*I) @ X.T @ y

    y_pred = X @ beta

    rmse = np.sqrt(np.mean((y - y_pred)**2))

    st.metric("Ridge RMSE", f"{rmse:.3f}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y, name="Actual"))
    fig.add_trace(go.Scatter(y=y_pred, name="Ridge Predicted"))

    fig.update_layout(title="Ridge Fit vs Actual")

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# REGIME SWITCHING
# =========================================================
elif page == "Regime Analysis":

    st.title("Regime Switching Elasticity")

    df = master.dropna().copy()

    df["regime"] = np.where(df["date"] < "2022-01-01", "Pre-Shock", "Post-Shock")

    results = {}

    for regime in df["regime"].unique():
        sub = df[df["regime"] == regime]

        X = np.column_stack([np.ones(len(sub)), sub["Brent_USD"]])
        y = sub["CPI_General"]

        beta = np.linalg.lstsq(X, y, rcond=None)[0]

        results[regime] = beta[1]

    res_df = pd.DataFrame(results.items(), columns=["Regime", "Elasticity"])

    fig = go.Figure()
    fig.add_trace(go.Bar(x=res_df["Regime"], y=res_df["Elasticity"]))

    fig.update_layout(title="Crude → CPI Elasticity by Regime")

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# DATA
# =========================================================
elif page == "Data":

    st.title("Dataset")

    st.dataframe(master, use_container_width=True)

    st.download_button(
        "Download CSV",
        master.to_csv(index=False),
        "dataset.csv"
    )