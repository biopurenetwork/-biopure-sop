import streamlit as st

# Set up page styling with a real visual reactor tank graphics layout
st.set_page_config(page_title="Biopure Process Validation", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    
    /* Industrial Reactor Vessel Layout and Styling */
    .reactor-vessel {
        width: 180px;
        height: 240px;
        background: linear-gradient(135deg, #dae3f3 0%, #b4c6e7 100%);
        border: 4px solid #4472c4;
        border-radius: 20px 20px 60px 60px;
        position: relative;
        margin: 30px auto;
        box-shadow: inset -10px -10px 20px rgba(0,0,0,0.1), 5px 10px 15px rgba(0,0,0,0.15);
    }
    
    /* Fluid level indicator inside the tank */
    .reactor-fluid {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 65%;
        background: linear-gradient(to top, rgba(91, 155, 213, 0.8), rgba(157, 195, 230, 0.6));
        border-radius: 0 0 55px 55px;
        transition: height 0.5s ease;
    }
    
    /* Agitator Motor Shaft Assembly */
    .reactor-shaft {
        width: 8px;
        height: 160px;
        background-color: #7f7f7f;
        position: absolute;
        top: -10px;
        left: calc(50% - 4px);
        z-index: 2;
    }
    
    /* Continuous Spinning Animation Keyframes for the Blade */
    @keyframes spin-blade {
        0% { transform: rotateX(70deg) rotateZ(0deg); }
        100% { transform: rotateX(70deg) rotateZ(360deg); }
    }
    
    /* Active Rotating Mixing Blades */
    .spinning-blade {
        width: 100px;
        height: 20px;
        background: #595959;
        position: absolute;
        bottom: 40px;
        left: calc(50% - 50px);
        border-radius: 50%;
        transform: rotateX(70deg);
        animation: spin-blade 0.8s linear infinite;
        z-index: 3;
        box-shadow: 0 4px 5px rgba(0,0,0,0.3);
    }
    
    /* Static Idle Blades state */
    .stopped-blade {
        width: 100px;
        height: 20px;
        background: #a6a6a6;
        position: absolute;
        bottom: 40px;
        left: calc(50% - 50px);
        border-radius: 50%;
        transform: rotateX(70deg);
        z-index: 3;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧪 BIOPURE S.A. — SOP Process Validation Tool")
st.caption("Windows 64-Bit Simulation Environment Core / Native CODESYS V3.5 SP20 Logic")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.header("🎛️ Process Inputs")
    stage = st.selectbox("Select Active Fractionation Stage", 
                        ["Fraction I (Target: 8%)", "Fraction II+III (Target: 21%)", "Fraction IV (Target: 41%)", "Fraction V (Target: 41%)"])
    
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
    st.header("📊 Automated Control Outputs")
    
    if target_pct > manual_et:
        needed_et_kg = (weight * (target_pct - manual_et)) / (0.96 - target_pct)
    else:
        needed_et_kg = 0.0
        
    temp_safe = t_low <= temp <= t_high
    
    m1, m2 = st.columns(2)
    m1.metric("Required 96% Loop Injection", f"{needed_et_kg:.2f} kg")
    m2.metric("Target Phase Concentration", f"{target_pct*100:.1f} %")
    
    st.subheader("🛡️ Safety Interlock Status")
    if temp_safe:
        st.success(f"TEMPERATURE INTERLOCK OK: {temp}°C is within safe limits")
        valve_open = needed_et_kg > 0.0
    else:
        st.error(f"TEMPERATURE INTERLOCK BREACHED: Temp is outside safe limits")
        valve_open = False
        
    # --- VISUAL REACTOR VESSEL AND MECHANICAL AGITATOR RENDERING ---
    st.subheader("🏭 Live Process Vessel Animation")
    
    if valve_open:
        st.warning("🔄 SUPPLY LOOP VALVE OPEN: Mixing process running.")
        # Render Tank with custom CSS classes for active rotating mixing actions
        st.markdown('''
            <div class="reactor-vessel">
                <div class="reactor-fluid"></div>
                <div class="reactor-shaft"></div>
                <div class="spinning-blade"></div>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.info("⏸️ VALVE CLOSED: Agitator system idle.")
        # Render Tank with flat static styling
        st.markdown('''
            <div class="reactor-vessel">
                <div class="reactor-fluid"></div>
                <div class="reactor-shaft"></div>
                <div class="stopped-blade"></div>
            </div>
        ''', unsafe_allow_html=True)
