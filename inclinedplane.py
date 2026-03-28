import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Inclined Plane Ball Model", layout="wide")

st.title("Inclined Plane Ball Motion Model")
st.write("Study how angle, mass, surface smoothness, size, and ramp length affect a ball rolling or sliding down an inclined plane.")

g = 9.81

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Input Parameters")

angle_deg = st.sidebar.slider("Angle of Incline (degrees)", 1, 89, 30)
mass = st.sidebar.number_input("Mass of Ball (kg)", min_value=0.01, value=1.0, step=0.1)
radius = st.sidebar.number_input("Radius of Ball (m)", min_value=0.01, value=0.05, step=0.01)
mu = st.sidebar.slider("Surface Friction Coefficient (μ)", 0.0, 1.0, 0.10, 0.01)
length = st.sidebar.number_input("Ramp Length (m)", min_value=0.1, value=2.0, step=0.1)

motion_type = st.sidebar.radio("Motion Type", ["Rolling (Solid Sphere)", "Sliding"])

theta = np.radians(angle_deg)

# -----------------------------
# Physics Calculations
# -----------------------------
force_parallel = mass * g * np.sin(theta)
normal_force = mass * g * np.cos(theta)

if motion_type == "Rolling (Solid Sphere)":
    # Solid sphere rolling without slipping
    acceleration = (5/7) * g * np.sin(theta)
else:
    # Sliding with friction
    acceleration = g * (np.sin(theta) - mu * np.cos(theta))
    if acceleration < 0:
        acceleration = 0

if acceleration > 0:
    time_to_bottom = np.sqrt((2 * length) / acceleration)
    final_velocity = np.sqrt(2 * acceleration * length)
else:
    time_to_bottom = np.nan
    final_velocity = 0

# -----------------------------
# Summary
# -----------------------------
st.subheader("Simulation Summary")

c1, c2, c3 = st.columns(3)
c1.metric("Acceleration (m/s²)", f"{acceleration:.3f}")
c2.metric("Time to Bottom (s)", f"{time_to_bottom:.3f}" if not np.isnan(time_to_bottom) else "Does not move")
c3.metric("Final Velocity (m/s)", f"{final_velocity:.3f}")

c4, c5 = st.columns(2)
c4.metric("Force Along Slope (N)", f"{force_parallel:.3f}")
c5.metric("Normal Force (N)", f"{normal_force:.3f}")

# -----------------------------
# Interpretation
# -----------------------------
st.subheader("Interpretation")

if motion_type == "Rolling (Solid Sphere)":
    st.info("In ideal rolling motion, mass and size do not strongly affect acceleration for a solid sphere. The angle is the main factor.")
else:
    st.info("In sliding motion, friction and angle strongly affect acceleration. If friction is too high, the ball may not move.")

# -----------------------------
# Time Series Simulation
# -----------------------------
st.subheader("Motion Plots")

if acceleration > 0:
    t = np.linspace(0, time_to_bottom, 200)
    position = 0.5 * acceleration * t**2
    velocity = acceleration * t

    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.plot(t, position)
    ax1.set_title("Position vs Time")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Position along slope (m)")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(t, velocity)
    ax2.set_title("Velocity vs Time")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Velocity (m/s)")
    st.pyplot(fig2)
else:
    st.warning("The ball does not move under the current conditions.")

# -----------------------------
# Sensitivity Analysis
# -----------------------------
st.subheader("Effect of Angle on Acceleration")

angles = np.arange(1, 90)

if motion_type == "Rolling (Solid Sphere)":
    acc_values = (5/7) * g * np.sin(np.radians(angles))
else:
    acc_values = g * (np.sin(np.radians(angles)) - mu * np.cos(np.radians(angles)))
    acc_values = np.maximum(acc_values, 0)

fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.plot(angles, acc_values)
ax3.set_title("Acceleration vs Angle")
ax3.set_xlabel("Angle (degrees)")
ax3.set_ylabel("Acceleration (m/s²)")
st.pyplot(fig3)

# -----------------------------
# Data Table
# -----------------------------
st.subheader("Computed Results Table")

results_df = pd.DataFrame({
    "Parameter": [
        "Angle (degrees)",
        "Mass (kg)",
        "Radius (m)",
        "Friction Coefficient (μ)",
        "Ramp Length (m)",
        "Acceleration (m/s²)",
        "Time to Bottom (s)",
        "Final Velocity (m/s)",
        "Force Along Slope (N)",
        "Normal Force (N)"
    ],
    "Value": [
        angle_deg,
        mass,
        radius,
        mu,
        length,
        acceleration,
        time_to_bottom if not np.isnan(time_to_bottom) else "Does not move",
        final_velocity,
        force_parallel,
        normal_force
    ]
})

st.dataframe(results_df, use_container_width=True)

# -----------------------------
# Download Results
# -----------------------------
csv = results_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Results as CSV",
    data=csv,
    file_name="inclined_plane_results.csv",
    mime="text/csv"
)