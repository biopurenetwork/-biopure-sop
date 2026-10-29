import streamlit as st

st.set_page_config(page_title="Biopure Process Validation", layout="wide")

# Custom injection styling to clean up Streamlit's default card spacing
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    h1, h3, p, span { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important; }
    div[data-testid="stSlider"] { margin-bottom: -10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧪 BIOPURE — SOP Process Validation Tool")
st.caption("Windows 64-Bit Simulation Environment Core / Native CODESYS V3.5 SP20 Logic")

st.markdown("""
<p style="color: #555; font-size: 14px;">To help you simulate and test these calculations directly inside your Windows 64-bit environment without being connected to live plant hardware, you can use this simulation module to verify how changing target weights or assay percentages impacts your loop valve output.</p>
""", unsafe_allow_html=True)

st.subheader("SOP Operator Stage Target Selection")
stage = st.selectbox(
    "Select Active Fractionation Stage", 
    ["Batch Phase (Low Initial Intake)", "Fraction I (Target: 8%)", "Fraction II+III (Target: 21%)", "Fraction IV (Target: 41%)", "Fraction V (Target: 41%)"],
    label_visibility="collapsed"
)

# Configuration mapping based on process step selection
if "Batch Phase" in stage:
    target_pct, t_low, t_high, default_w, default_t, default_a = 0.0, 15.0, 30.0, 116.0, 27.0, 43.0
elif "Fraction I" in stage:
    target_pct, t_low, t_high, default_w, default_t, default_a = 0.08, -3.0, -2.0, 2000.0, -2.5, 0.0
elif "Fraction II+III" in stage:
    target_pct, t_low, t_high, default_w, default_t, default_a = 0.21, -6.0, -4.0, 2900.0, -5.0, 8.0
elif "Fraction IV" in stage:
    target_pct, t_low, t_high, default_w, default_t, default_a = 0.41, -6.0, -4.0, 4000.0, -5.0, 21.0
else:
    target_pct, t_low, t_high, default_w, default_t, default_a = 0.41, -8.0, -6.0, 2200.0, -7.0, 41.0

# 3 Horizontal Layout Sliders matching user screenshot
col_w, col_t, col_a = st.columns(3)
with col_w:
    weight = st.slider("Current Reactor Weight", min_value=0, max_value=5000, value=int(default_w), step=10, format="%d kg")
with col_t:
    temp = st.slider("Reactor Temperature", min_value=-20.0, max_value=40.0, value=float(default_t), step=0.5, format="%.1f °C")
with col_a:
    assay = st.slider("Laboratory Assay Verification", min_value=0, max_value=100, value=int(default_a), step=1, format="%d mg/L")

# System State Evaluation Math
temp_safe = t_low <= temp <= t_high
manual_et = assay / 100.0

if target_pct > manual_et:
    needed_et_kg = (weight * (target_pct - manual_et)) / (0.96 - target_pct)
else:
    needed_et_kg = 0.0

valve_open = needed_et_kg > 0.0 and (temp_safe or "Batch Phase" in stage)

# Calculate parameters for high resolution SVG level tracking maps
fluid_y_axis = min(260, max(100, 260 - int((weight / 5000.0) * 160)))
dosing_flow = f"{needed_et_kg/60.0:.2f} mL/m" if valve_open else "0.00 mL/m"

if temp > 20:
    jacket_color = "#e74c3c"
    jacket_status = "Heating Range"
elif temp_safe:
    jacket_color = "#2ecc71"
    jacket_status = "Optimal Range"
else:
    jacket_color = "#3498db"
    jacket_status = "Cooling Range"

pipe_color = "#3498db" if valve_open else "#2c3e50"
blade_class = "spinning-propeller" if valve_open else "idle-propeller"
cooling_flow_str = "1.8 mL/m" if temp > target_pct else "0.0 mL/m"

# Render Layout splitting text sections from formatting variables safely
canvas_html = f"""
<div style="background-color: #0b132b; border-radius: 12px; padding: 24px; color: #ffffff; font-family: monospace; max-width: 700px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
    
    <style>
        @keyframes industrial-spin {{
            0% {{ transform: scaleX(1); opacity: 1; }}
            25% {{ transform: scaleX(0.1); opacity: 0.8; }}
            50% {{ transform: scaleX(-1); opacity: 1; }}
            75% {{ transform: scaleX(-0.1); opacity: 0.8; }}
            100% {{ transform: scaleX(1); opacity: 1; }}
        }}
        .spinning-propeller {{
            animation: industrial-spin 1.2s linear infinite;
            transform-origin: 300px 240px;
        }}
        .idle-propeller {{
            transform-origin: 300px 240px;
        }}
    </style>

    <div style="width: 100%; display: flex; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px solid #1c2541; padding-bottom: 8px;">
        <span style="color: #5bc0be; font-weight: bold; font-family: sans-serif;">SOP: Run Mode</span>
        <span style="background-color: #1c2541; padding: 2px 8px; border-radius: 4px; font-size: 11px;">⏸ II</span>
    </div>

    <svg viewBox="0 0 600 380" width="100%" height="100%" xmlns="http://w3.org">
        <path d="M 40 100 L 260 100 L 260 120" fill="none" stroke="{pipe_color}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" />
        
        <text x="40" y="65" fill="#8b9bb4" font-size="10" font-family="sans-serif">CODESYS CASCADE LOOP</text>
        <text x="40" y="85" fill="#ffffff" font-size="15" font-weight="bold" font-family="sans-serif">{dosing_flow}</text>

        <rect x="190" y="110" width="220" height="190" rx="30" ry="30" fill="none" stroke="{jacket_color}" stroke-width="12" opacity="0.3" />
        <rect x="190" y="110" width="220" height="190" rx="30" ry="30" fill="none" stroke="{jacket_color}" stroke-width="3" />

        <rect x="200" y="120" width="200" height="170" rx="20" ry="20" fill="#0b132b" stroke="#34495e" stroke-width="2" />
        
        <svg x="200" y="120" width="200" height="170" viewBox="200 120 200 170">
            <rect x="200" y="{fluid_y_axis}" width="200" height="300" fill="url(#fluid-grad)" opacity="0.85" />
        </svg>

        <!-- INDUSTRIAL VERTICAL SHAFT AND ANCHOR-PADDLE AGITATOR DESIGN -->
        <line x1="300" y1="90" x2="300" y2="235" stroke="#95a5a6" stroke-width="6" stroke-linecap="round" />

        <g class="{blade_class}">
            <!-- Crossbar support hub -->
            <rect x="250" y="232" width="100" height="8" rx="2" fill="#7f8c8d" stroke="#bdc3c7" stroke-width="1" />
            <!-- Left Paddle Blade -->
            <path d="M 250 215 L 258 215 L 258 245 L 250 245 Z" fill="#7f8c8d" stroke="#ffffff" stroke-width="1" />
            <!-- Right Paddle Blade -->
            <path d="M 342 215 L 350 215 L 350 245 L 342 245 Z" fill="#7f8c8d" stroke="#ffffff" stroke-width="1" />
        </g>

        <g transform="translate(420, 110)">
            <rect width="140" height="75" rx="6" fill="#1c2541" stroke="#3a506b" stroke-width="1" />
            <line x1="0" y1="0" x2="0" y2="75" stroke="{jacket_color}" stroke-width="4" />
            <text x="12" y="22" fill="#8b9bb4" font-size="10" font-family="sans-serif">THERMAL JACKET</text>
            <text x="12" y="44" fill="#ffffff" font-size="16" font-weight="bold" font-family="sans-serif">{temp:.1f} °C</text>
            <text x="12" y="62" fill="{jacket_color}" font-size="11" font-family="sans-serif">● {jacket_status}</text>
        </g>

        <text x="300" y="325" fill="#8b9bb4" font-size="12" text-anchor="middle" font-family="sans-serif">
            Current Mass: <tspan fill="#5bc0be" font-weight="bold">{weight} Kg</tspan> / 5000 Kg
        </text>

        <defs>
            <linearGradient id="fluid-grad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#1aa6b7" />
                <stop offset="100%" stop-color="#116979" />
            </linearGradient>
        </defs>
    </svg>

    <div style="width: 100%; display: flex; justify-content: space-around; margin-top: 10px; border-top: 1px solid #1c2541; padding-top: 15px; font-size: 12px; text-align: center;">
        <div>
            <div style="color: #8b9bb4; font-size: 10px; margin-bottom: 2px;">Cooling Loop</div>
            <div style="font-weight: bold; color: #ffffff;">{cooling_flow_str}</div>
        </div>
        <div>
            <div style="color: #8b9bb4; font-size: 10px; margin-bottom: 2px;">Thermal State</div>
            <div style="font-weight: bold; color: #e74c3c;">{temp:.1f} °C</div>
        </div>
        <div>
            <div style="color: #8b9bb4; font-size: 10px; margin-bottom: 2px;">Assay Target</div>
            <div style="font-weight: bold; color: #2ecc71;">{assay} mg/L</div>
        </div>
    </div>
</div>
"""

st.components.v1.html(canvas_html, height=480)
