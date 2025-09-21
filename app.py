import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Forex Simulation", layout="centered")

# ----------------- Core Functions -----------------
def forex_simulation(budget_inr, inr_to_foreign_direct, inr_to_usd, usd_to_foreign):
    """Compare INR→Foreign vs INR→USD→Foreign and compute break-even. (@spreading.smiles06)"""
    # Option 1: Direct INR → Foreign
    foreign_direct = budget_inr / inr_to_foreign_direct

    # Option 2: INR → USD → Foreign
    usd_amount = budget_inr / inr_to_usd
    foreign_via_usd = usd_amount * usd_to_foreign

    # Break-even INR→Foreign rate
    break_even_inr_to_foreign = budget_inr / foreign_via_usd if foreign_via_usd > 0 else None

    # Break-even USD→Foreign rate
    break_even_usd_to_foreign = inr_to_usd / inr_to_foreign_direct if inr_to_foreign_direct > 0 else None

    return {
        "Foreign via Direct (India)": foreign_direct,
        "Foreign via USD abroad": foreign_via_usd,
        "Break-even INR/Foreign": break_even_inr_to_foreign,
        "Break-even USD/Foreign": break_even_usd_to_foreign
    }


def plot_forex_graph(budget_inr, inr_to_foreign_direct, inr_to_usd, usd_to_foreign_range):
    """Plot comparison of INR→Foreign vs INR→USD→Foreign over a range of USD→Foreign rates."""
    usd_rates = np.linspace(min(usd_to_foreign_range), max(usd_to_foreign_range), 100)

    # Direct INR→Foreign is constant
    foreign_direct = budget_inr / inr_to_foreign_direct

    # Via USD→Foreign varies with USD→Foreign rate
    usd_amount = budget_inr / inr_to_usd
    foreign_via_usd = usd_amount * usd_rates

    # Calculate break-even
    break_even_usd_to_foreign = inr_to_usd / inr_to_foreign_direct

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axhline(y=foreign_direct, color='r', linestyle='--', label=f"Direct INR→Foreign ({foreign_direct:.0f})")
    ax.plot(usd_rates, foreign_via_usd, label="Via USD abroad", color='b')
    ax.axvline(x=break_even_usd_to_foreign, color='g', linestyle=':', 
               label=f"Break-even USD→Foreign: {break_even_usd_to_foreign:.2f}")

    ax.set_xlabel("USD → Foreign exchange rate")
    ax.set_ylabel("Foreign currency obtained")
    ax.set_title("Direct INR vs Via USD Comparison")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# ----------------- Streamlit UI -----------------
st.title("💱 Forex Simulation Tool")
st.markdown("<span style='color:cyan'>(@spreading.smiles06)</span>", unsafe_allow_html=True)

st.markdown("Compare **Direct INR→Foreign** vs **INR→USD→Foreign abroad** and find break-even points. (@spreading.smiles06)")

# Inputs
budget = st.number_input("Budget in INR", min_value=1000, value=100000, step=1000)
inr_to_foreign_direct = st.number_input("Direct INR→Foreign (India)", min_value=0.01, value=1.41, step=0.01, format="%.2f")
inr_to_usd = st.number_input("INR→USD (India)", min_value=0.01, value=89.1, step=0.1, format="%.2f")
usd_to_foreign_min = st.number_input("Min USD→Foreign rate (abroad)", min_value=0.1, value=60.0, step=0.1, format="%.2f")
usd_to_foreign_max = st.number_input("Max USD→Foreign rate (abroad)", min_value=0.1, value=85.0, step=0.1, format="%.2f")

usd_to_foreign_range = (usd_to_foreign_min, usd_to_foreign_max)

# Run Simulation
if st.button("Run Simulation"):
    # Calculate with mid-value for table
    mid_usd_rate = (usd_to_foreign_min + usd_to_foreign_max) / 2
    result = forex_simulation(budget, inr_to_foreign_direct, inr_to_usd, mid_usd_rate)

    # Show results in table
    df = pd.DataFrame(result.items(), columns=["Scenario", "Value"])
    st.subheader("📊 Results")
    st.table(df)

    # Show graph
    st.subheader("📈 Simulation Graph")
    plot_forex_graph(budget, inr_to_foreign_direct, inr_to_usd, usd_to_foreign_range)

st.markdown("---")
st.caption("Built with ❤️ in Streamlit by st.markdown("<span style='color:cyan'>(@spreading.smiles06)</span>", unsafe_allow_html=True)
")
