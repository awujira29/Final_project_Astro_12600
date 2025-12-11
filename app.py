import streamlit as st
import math

# --- Physical constants (from class) ---
G = 6.67430e-11          # gravitational constant, m^3 / (kg s^2)
C = 2.99792458e8         # speed of light, m / s
M_SUN = 1.98847e30       # mass of the Sun in kg
G_EARTH = 9.80665        # approx Earth surface gravity, m/s^2
SECONDS_PER_DAY = 86400.0
SECONDS_PER_YEAR = 365.25 * SECONDS_PER_DAY

# --- Known black holes (masses in solar masses) ---
KNOWN_BLACK_HOLES = {
    "Cygnus X-1": 21.0,          # ~21 M_sun
    "Sagittarius A*": 4.3e6,     # ~4.3 million M_sun
    "M87*": 6.5e9,               # ~6.5 billion M_sun
    "GW150914 remnant": 62.0,    # ~62 M_sun
}


# =================================================================
# --- PHYSICS FUNCTIONS (Your core logic) ---
# =================================================================

def solar_mass_to_kg(m_solar: float) -> float:
    """Convert mass from solar masses to kg."""
    return m_solar * M_SUN

def schwarzschild_radius(m_kg: float) -> float:
    """r_s = 2GM / c^2"""
    return 2 * G * m_kg / (C ** 2)

def gravity_at_radius(m_kg: float, r_m: float) -> float:
    """g(r) = GM / r^2"""
    return G * m_kg / (r_m ** 2)

def tidal_acceleration(m_kg: float, r_m: float, height_m: float) -> float:
    """Approximate tidal acceleration Δg ≈ | g(r) - g(r + h) |"""
    g_near = gravity_at_radius(m_kg, r_m)
    g_far = gravity_at_radius(m_kg, r_m + height_m)
    return abs(g_near - g_far)

def classify_spaghettification(delta_g: float) -> str:
    """Give a rough qualitative classification based on Δg compared to Earth gravity."""
    ratio = delta_g / G_EARTH

    # Note: Using triple quotes and careful formatting to ensure
    # the output is readable within Streamlit's st.info() box.

    if ratio < 0.1:
        return (
            f"**Qualitative Assessment: Negligible (Δg ≈ {ratio:.3f} g_earth)**\n\n"
            "The difference in gravity between your head and feet is tiny. "
            "You would not feel stretched by the black hole at this distance. "
            "This regime applies to distances far from any black hole or even moderately far "
            "from supermassive black holes (like Sgr A*)."
        )
    elif ratio < 1.0:
        return (
            f"**Qualitative Assessment: Noticeable (Δg ≈ {ratio:.2f} g_earth)**\n\n"
            "Tidal forces are stronger than on Earth, and you would feel a clear "
            "difference in pull between your head and feet. You would experience "
            "significant discomfort, but this is not yet the 'instant spaghetti' regime."
        )
    elif ratio < 10.0:
        return (
            f"**Qualitative Assessment: Very Strong (Δg ≈ {ratio:.1f} g_earth)**\n\n"
            "Gravity at your feet is much stronger than at your head. Your body "
            "would be under intense structural stress. The onset of "
            "'spaghettification' would be serious and likely fatal over time, "
            "causing irreparable damage."
        )
    else:
        return (
            f"**Qualitative Assessment: EXTREME SPAGHETTIFICATION (Δg ≈ {ratio:.1f} g_earth)**\n\n"
            "This is deep in the spaghettification regime. The difference in gravitational "
            "pull across your body is so huge that no human (or spacecraft) could "
            "structurally survive it. The stretching would be virtually instantaneous and fatal. "
        )

def kepler_orbital_period(m_kg: float, r_m: float) -> float:
    """P = 2π * sqrt(r^3 / (G M))"""
    return 2.0 * math.pi * math.sqrt(r_m**3 / (G * m_kg))


# =================================================================
# --- STREAMLIT FRONT END ---
# =================================================================

# Set up the main page title and introductory text
st.set_page_config(layout="wide", page_title="Black Hole Calculator")
st.title("🌌 Black Hole Spaghettification & Orbital Calculator")
st.markdown(
    # Using 'r' at the start of the string prevents backslash errors
    r"""
    An interactive calculator for ASTR/PHSC 12600 concepts:
    - **Schwarzschild Radius** ($r_s = 2GM/c^2$)
    - **Newtonian Gravity** ($g(r) = GM/r^2$)
    - **Tidal Forces** (Spaghettification)
    - **Kepler Orbital Period** ($P = 2\pi \sqrt{r^3/(GM)}$)
    ---
    """
)


# --- SIDEBAR FOR USER INPUTS ---
st.sidebar.header("Parameters")

# 1. Black Hole Mass Selection
bh_options = list(KNOWN_BLACK_HOLES.keys())
bh_choice = st.sidebar.selectbox("1. Select Black Hole Mass:", bh_options + ["--- Custom Mass ---"])

if bh_choice == "--- Custom Mass ---":
    m_sun = st.sidebar.number_input(
        r"Enter Mass in Solar Masses ($M_{\odot}$):",
        min_value=0.01,
        value=10.0,
        format="%.3g"
    )
else:
    m_sun = KNOWN_BLACK_HOLES[bh_choice]
    st.sidebar.markdown(rf"**Mass:** {m_sun:.4g} $M_{{\odot}}$")


# 2. Distance from Center
distance_type = st.sidebar.radio(
    "2. Specify Distance:",
    ["Multiple of $r_s$", "Kilometers (km)"]
)

# Initialize m_kg and r_s for calculating default km value
m_kg_temp = solar_mass_to_kg(m_sun)
r_s_km_temp = schwarzschild_radius(m_kg_temp) / 1000.0

# 2b. Conditional Input Field for Distance
if distance_type == "Multiple of $r_s$":
    distance_input_value = st.sidebar.number_input(
        "Factor ($\times r_s$):",
        min_value=0.001, # Allows exploring distances inside r_s
        value=2.0,
        key='factor_input'
    )
else: # Kilometers (km)
    distance_input_value = st.sidebar.number_input(
        "Distance in km:",
        min_value=0.001, # FIXED: Allows entering very small distances (1 meter is 0.001 km)
        value=r_s_km_temp * 2.0,
        format="%.3f",
        key='km_input'
    )


# 3. Body Height
h_m = st.sidebar.number_input(
    "3. Body/Object Height (m):",
    min_value=0.1,
    value=2.0,
    format="%.2f"
)

# --- CALCULATE BUTTON AND LOGIC ---
st.sidebar.markdown("---")
if st.sidebar.button("Calculate Physics"):
    
    # 1. Calculate Mass and Schwarzschild Radius
    m_kg = solar_mass_to_kg(m_sun)
    r_s = schwarzschild_radius(m_kg)
    r_s_km = r_s / 1000.0
    
    # 2. Convert the user's input value to radius in meters (r_m)
    if distance_type == "Multiple of $r_s$":
        r_m = distance_input_value * r_s
        factor = distance_input_value
    else: # Kilometers (km)
        r_m = distance_input_value * 1000.0
        factor = r_m / r_s if r_s > 0 else float("inf")
        
    r_km = r_m / 1000.0

    # --- Perform the Core Calculations ---
    g_here = gravity_at_radius(m_kg, r_m)
    delta_g = tidal_acceleration(m_kg, r_m, h_m)

    # Kepler period check
    period_s = None
    if r_m > r_s:
        period_s = kepler_orbital_period(m_kg, r_m)

    # --- Display Results ---
    st.header(rf"Results for a {m_sun:.4g} $M_{{\odot}}$ Black Hole")

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Schwarzschild Radius ($r_s$)", f"{r_s_km:.4g} km")
    col2.metric("Distance from Center ($r$)", f"{r_km:.4g} km", delta=f"{factor:.3g} × $r_s$")
    col3.metric("Acceleration ($g(r)$)", f"{g_here:.4e} m/s²", delta=f"{g_here / G_EARTH:.3g} × $g_{{\oplus}}$")

    st.subheader("1. Spaghettification / Tidal Forces")
    
    # Display Tidal Metric and Classification
    st.metric(
        "Tidal Acceleration ($\Delta g$)",
        f"{delta_g:.4e} m/s²",
        delta=f"Ratio: {delta_g / G_EARTH:.3g} × $g_{{\oplus}}$ over {h_m:.2f} m"
    )
    
    st.markdown("---")
    classification_text = classify_spaghettification(delta_g)
    # The classification text now includes detailed, formatted explanation
    st.info(classification_text)
    
    st.subheader("2. Kepler Orbital Period (Newtonian)")

    if factor <= 1.0:
        st.warning(
            "⚠️ You are at or inside the event horizon ($r \le r_s$). "
            "A classical circular orbit is not physically meaningful here. "
            "General Relativity predicts inevitable inward freefall (geodesic)."
        )
    elif period_s is not None:
        period_hours = period_s / 3600.0
        period_days = period_s / SECONDS_PER_DAY
        period_years = period_s / SECONDS_PER_YEAR

        st.markdown(
            r"The Newtonian formula $P = 2\pi \sqrt{r^3 / (GM)}$ gives an estimated period of:"
        )

        colA, colB, colC, colD = st.columns(4)
        colA.metric("Period (Seconds)", f"{period_s:.4e} s")
        colB.metric("Period (Hours)", f"{period_hours:.3g} hrs")
        colC.metric("Period (Days)", f"{period_days:.3g} days")
        colD.metric("Period (Years)", f"{period_years:.3g} yrs")
    
    st.markdown("---")
    st.caption("Note: Calculations are based on Newtonian approximations and the Schwarzschild radius.")