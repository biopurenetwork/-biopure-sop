import streamlit as st
import time

st.set_page_config(page_title="Biopure Process Validation", layout="wide")

# App Header
st.title("🧪 BIOPURE — SOP Process Validation Tool")
st.caption("Windows 64-Bit Simulation Environment Core / Native CODESYS V3.5 SP20 Logic")

st.markdown("""
<p>To help you simulate and test these calculations directly inside your Windows 64-bit environment without being connected to live plant hardware, you can use this simulation module to verify how changing target weights or assay percentages impacts your loop valve output.</p>
""", unsafe_allow_html=True)

# User Controls Panels
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

# Calculate parameters for visual rendering display
fluid_height = min(220, max(20, int((weight / 5000.0) * 200) + 20))
dosing_flow = f"{needed_et_kg/60.0:.2f} mL/m" if valve_open else "0.00 mL/m"
jacket_color = "#e74c3c" if temp > 20 else ("#3498db" if temp < 0 else "#2ecc71")
jacket_status = "Heating Range" if temp > 20 else ("Cooling Range" if temp < 0 else "Optimal Range")

# Core Schematic Generation Script Layout using Embedded HTML Canvas Elements
canvas_html = f"""
<div style="background-color: #0b132b; border-radius: 12px; padding: 24px; color: #ffffff; font-family: monospace; display: flex; flex-direction: column; align-items: center; box-shadow: 0 8px 16px rgba(0,0,0,0.3); max-width: 700px; margin: 0 auto;">
    <div style="width: 100%; display: flex; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px solid #1c2541; padding-bottom: 8px;">
        <span style="color: #5bc0be; font-weight: bold;">SOP: Run Mode</span>
        <span style="background-color: #1c2541; padding: 2px 8px; border-radius: 4px; font-size: 11px;">⏸ II</span>
    </div>
    
    <div style="position: relative; width: 550px; height: 350px; margin-top: 15px;">
        <!-- Dosing Loop Pipeline Stream Graphics -->
        <div style="position: absolute; top: 80px; left: 10px; width: 140px; height: 6px; background-color: {('#3498db' if valve_open else '#1c2541')}; z-index: 1;"></div>
        <div style="position: absolute; top: 86px; left: 144px; width: 6px; height: 34px; background-color: {('#3498db' if valve_open else '#1c2541')}; z-index: 1;"></div>
        
        <!-- Text labels metrics displays on canvas layout -->
        <div style="position: absolute; top: 40px; left: 20px; font-size: 12px;">
            <div style="color: #8b9bb4; font-size: 10px;">DOSING RECONCILE LOOP</div>
            <div style="color: #ffffff; font-weight: bold;">{dosing_flow}</div>
        </div>

        <div style="position: absolute; top: 120px; right: 40px; font-size: 12px; background: rgba(28,37,65,0.6); padding: 8px; border-radius: 6px; border-left: 4px solid {jacket_color};">
            <div style="color: #8b9bb4; font-size: 10px;">THERMAL JACKET</div>
            <div style="color: #ffffff; font-weight: bold; font-size: 14px;">{temp:.1f} °C</div>
            <div style="color: {jacket_color}; font-size: 11px;">● {jacket_status}</div>
        </div>

        <!-- Reactor Vessel Layout Outline Assembly -->
        <div style="position: absolute; top: 100px; left: 180px; width: 180px; height: 220px; border-radius: 20px 20px 40px 40px; border: 4px solid {jacket_color}; background-color: #0b132b; box-shadow: 0 0 15px {jacket_color}44; z-index: 2; overflow: hidden;">
            <!-- Process Fluid Height Tracking Level Display Container -->
            <div style="position: absolute; bottom: 0; left: 0; right: 0; height: {fluid_height}px; background: linear-gradient(to top, #116979, #1aa6b7); opacity: 0.85; transition: height 0.3s ease;"></div>
            
            <!-- Center Motor Mixing Shaft Element Overlay -->
            <div style="position: absolute; top: 0; left: 87px; width: 6px; height: 160px; background-color: #bdc3c7;"></div>
            
            <!-- Custom CSS Continuous Mechanical Spinning Impeller Rotor Blades Component -->
            <div id="blade" style="position: absolute; top: 155px; left: 43px; width: 94px; height: 14px; background-color: #ecf0f1; border-radius: 4px; transform-origin: center;"></div>
        </div>
        
        <div style="position: absolute; bottom: 5px; left: 200px; background-color: #1c2541; padding: 4px 12px; border-radius: 20px; font-size: 11px; border: 1px solid #3a506b;">
            Current Mass: <span style="color: #5bc0be; font-weight: bold;">{weight} Kg</span> / Max: 5000kg
        </div>
    </div>

    <!-- Footnotes Status Cards Alignment Row -->
    <div style="width: 100%; display: flex; justify-content: space-around; margin-top: 15px; border-top: 1px solid #1c2541; padding-top: 15px; font-size: 12px; text-align: center;">
        <div>
            <div style="color: #8b9bb4; font-size: 10px; margin-bottom: 2px;">Cooling Loop</div>
            <div style="font-weight: bold; color: #ffffff;">{('1.8 mL/m' if temp > target_pct else '0.0 mL/m')}</div>
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

    <!-- Active Inline Keyframe Rotation Scripts Driver Injection -->
    <script>
        var angle = 0;
        var isRunning = {str(valve_open).lower()};
        function spin() {{
            if (isRunning) {{
                angle = (angle + 8) % 360;
                var el = document.getElementById('blade');
                if (el) {{
                    el.style.transform = 'rotateX(65deg) rotateZ(' + angle + 'deg)';
                }}
            }} else {{
                var el = document.getElementById('blade');
                if (el) {{
                    el.style.transform = 'rotateX(65deg) rotateZ(0deg)';
                }}
            }}
            requestAnimationFrame(spin);
        }}
        // Small timeout safely anchors DOM availability loading hooks loops execution setup
        setTimeout(spin, 100);
    </script>
</div>
"""

# Render dynamic compiled html module safely inside framework window screen workspace
st.components.v1.html(canvas_html, height=450)
