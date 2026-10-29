import streamlit as st
import time

# Set up page styling
st.set_page_config(page_title="Biopure Process Validation", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stButton>button { width: 100%; background-color: #004B87; color: white; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .spinning-prop { animation: spin 2s linear infinite; display: inline-block; font-size: 50px; }
    .stopped-prop { display: inline-block; font-size: 50px; color: #888888; }
    </style>
""", unsafe_allow_html=True)

st.title("🧪 BIOPURE S.A. — SOP Process Validation Tool")
st.caption("Windows 64-Bit Simulation Environment Core / Native CODESYS V3.5 SP20 Logic")

# Setup layout columns
col1, col2 = st.columns([1, 2])

with col1:
    st.header("🎛️ Process Inputs")
    stage = st.selectbox("Select Active Fractionation Stage", 
                        ["Fraction I (Target: 8%)", "Fraction II+III (Target: 21%)", "Fraction IV (Target: 41%)", "Fraction V (Target: 41%)"])
    
    # Map limits based on stage selection
    if "Fraction I" in stage:
        target_pct, t_low, t_high, prev_et = 0.08, -3.0, -2.0, 0.0
    elif "Fraction II+III" in stage:
        target_pct, t_low, t_high, prev_et = 0.21, -6.0, -4.0, 0.08
    elif "Fraction IV" in stage:
        target_pct, t_low, t_high, prev_et = 0.41, -6.0, -4.0, 0.21
    else:
        target_pct, t_low, t_high, prev_et = 0.41, -8.0, -6.0, 0.41

    weight = st.number_input("Real-Time Load Cell Weight (kg)", min_value=0.0, value=2000.0, step=50.0)
    temp = st.number_input("Inline PT100 Temperature (°C)", min_value=-20.0, max_value=25.0, value=-5.0, step=0.1)
    
    st.subheader("🔬 Lab Assay Hand Entries")
    manual_ph = st.number_input("Measured pH Assay", min_value=0.0, max_value=14.0, value=6.8, step=0.05)
    manual_et = st.number_input("Measured Current Ethanol %", min_value=0.0, max_value=100.0, value=float(prev_et*100), step=0.5) / 100.0

with col2:
    st.header("📊 Automated Mass-Balance & Control Outputs")
    
    # Perform math calculations identical to the PLC logic
    if target_pct > manual_et:
        needed_et_kg = (weight * (target_pct - manual_et)) / (0.96 - target_pct)
    else:
        needed_et_kg = 0.0
        
    temp_safe = t_low <= temp <= t_high
    
    # Display instrumentation statuses
    m1, m2 = st.columns(2)
    m1.metric("Required 96% Loop Injection", f"{needed_et_kg:.2f} kg")
    m2.metric("Target Phase Concentration", f"{target_pct*100:.1f} %")
    
    # Interlock status readouts
    st.subheader("🛡️ Safety Interlock Status")
    if temp_safe:
        st.success(f"TEMPERATURE INTERLOCK OK: {temp}°C falls within safe bounds ({t_low}°C to {t_high}°C)")
        valve_open = needed_et_kg > 0.0
    else:
        st.error(f"TEMPERATURE INTERLOCK BREACHED: {temp}°C is outside safe bounds ({t_low}°C to {t_high}°C)")
        valve_open = False
        
    if valve_open:
        st.warning("🔄 SUPPLY LOOP VALVE COMMANDED OPEN: Dosing process running.")
        # Animated agitator via html injection
        st.markdown('### Reactor Agitator Status: Running <br><span class="spinning-prop">🌀</span>', unsafe_allow_html=True)
    else:
        st.info("⏸️ VALVE COMMANDED CLOSED: System holding or waiting for thermal setpoint.")
        st.markdown('### Reactor Agitator Status: Idle <br><span class="stopped-prop">🌀</span>', unsafe_allow_html=True)
