#!/usr/bin/env python3
"""
Black Hole Tide & Spaghettification + Kepler Orbital Period Calculator
ASTR/PHSC 12600 – Final Project (Python version)

This script uses ONLY standard Python and physics concepts
from the course:

- Newtonian gravity (Lessons 6–7):
    g(r) = GM / r^2

- Schwarzschild radius (Lesson 11: black holes):
    r_s = 2GM / c^2
  which matches the ~3 km per solar mass rule discussed in class.

- Kepler's Third Law (from planetary orbits, adapted here to orbits
  around compact objects like black holes):
    P^2 ∝ a^3  →  for a small test particle in circular orbit:
    P = 2π * sqrt(r^3 / (G M))

We apply Kepler’s law in a Newtonian way to estimate the orbital period
of a small object at your chosen radius around the black hole.
"""

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


def solar_mass_to_kg(m_solar: float) -> float:
    """Convert mass from solar masses to kg."""
    return m_solar * M_SUN


def schwarzschild_radius(m_kg: float) -> float:
    """
    Compute Schwarzschild radius in meters:
        r_s = 2GM / c^2
    This is the exact version of the ~3 km per solar mass rule
    discussed in the black hole lecture (Lesson 11).
    """
    return 2 * G * m_kg / (C ** 2)


def gravity_at_radius(m_kg: float, r_m: float) -> float:
    """
    Compute gravitational acceleration g(r) = GM / r^2 in m/s^2.
    This is just Newton's law of gravity, as in Lessons 6–7.
    """
    return G * m_kg / (r_m ** 2)


def tidal_acceleration(m_kg: float, r_m: float, height_m: float) -> float:
    """
    Approximate tidal acceleration across a body of height 'height_m'
    by the difference in g between r and r + height:

        Δg ≈ | g(r) - g(r + h) |

    Physically, this is what stretches the body ("spaghettification").
    """
    g_near = gravity_at_radius(m_kg, r_m)
    g_far = gravity_at_radius(m_kg, r_m + height_m)
    return abs(g_near - g_far)


def classify_spaghettification(delta_g: float) -> str:
    """
    Give a rough qualitative classification based on Δg compared to Earth gravity.
    These thresholds are heuristic, just to make the output more intuitive.
    """
    ratio = delta_g / G_EARTH

    if ratio < 0.1:
        return (
            f"Negligible tidal forces (Δg ≈ {ratio:.3f} g_earth):\n"
            "  The difference in gravity between your head and feet is tiny.\n"
            "  You would not really feel stretched by the black hole at this distance."
        )
    elif ratio < 1.0:
        return (
            f"Noticeable but not immediately lethal (Δg ≈ {ratio:.2f} g_earth):\n"
            "  Tidal forces are stronger than on Earth, and you would feel\n"
            "  a clear difference in pull between your head and feet, but\n"
            '  this is not yet the “instant spaghetti” regime.'
        )
    elif ratio < 10.0:
        return (
            f"Very strong (Δg ≈ {ratio:.1f} g_earth):\n"
            "  Gravity at your feet is much stronger than at your head.\n"
            "  Your body would be under intense stress, and the onset of\n"
            '  “spaghettification” would be serious and likely fatal over time.'
        )
    else:
        return (
            f"Extreme tidal forces (Δg ≈ {ratio:.1f} g_earth):\n"
            "  This is deep in the spaghettification regime. The difference\n"
            "  in gravitational pull across your body is so huge that no\n"
            "  human (or spacecraft) could structurally survive it."
        )


def kepler_orbital_period(m_kg: float, r_m: float) -> float:
    """
    Kepler's Third Law (Newtonian form) for a small object in circular orbit
    around a mass M:

        P = 2π * sqrt(r^3 / (G M))

    Here:
      - P is the orbital period (seconds),
      - r is the orbital radius (meters),
      - M is the mass of the central object (kg).

    In the original Kepler context, this described planets orbiting the Sun.
    In this project, we apply the same idea to orbits around black holes.
    """
    return 2.0 * math.pi * math.sqrt(r_m**3 / (G * m_kg))


def print_intro() -> None:
    print("=" * 72)
    print(" Black Hole Tide, Spaghettification & Kepler Orbital Period Calculator")
    print(" ASTR/PHSC 12600 – Final Project (Python)")
    print("=" * 72)
    print("This program uses:")
    print("  • Newtonian gravity (Lessons 6–7): g(r) = GM / r^2")
    print("  • The Schwarzschild radius from modern relativity (Lesson 11):")
    print("      r_s = 2GM / c^2  (~3 km per solar mass)")
    print("  • Kepler’s Third Law applied near a black hole to estimate how long")
    print("    it would take a small object to complete one circular orbit at")
    print("    your chosen distance.\n")
    print("The goal is to connect quantitative calculations to intuitive ideas:")
    print("How strong is gravity, how much do tidal forces stretch you, and")
    print("how fast could you orbit near different black holes?\n")


def choose_black_hole() -> float:
    """
    Let the user choose a known black hole or enter a custom mass.
    Returns the mass in solar masses.
    """
    print("Choose a black hole or enter a custom mass:")
    keys = list(KNOWN_BLACK_HOLES.keys())

    for i, name in enumerate(keys, start=1):
        print(f"  {i}. {name} (≈ {KNOWN_BLACK_HOLES[name]:.3g} M_sun)")
    print(f"  {len(keys) + 1}. Custom mass (in solar masses)")

    while True:
        choice = input(f"Enter 1–{len(keys) + 1}: ").strip()
        if not choice.isdigit():
            print("Please enter a number.")
            continue

        idx = int(choice)
        if 1 <= idx <= len(keys):
            name = keys[idx - 1]
            m_sun = KNOWN_BLACK_HOLES[name]
            print(f"\nYou chose: {name} (≈ {m_sun:.3g} M_sun)\n")
            return m_sun
        elif idx == len(keys) + 1:
            while True:
                try:
                    val = float(input("Enter mass in solar masses (e.g., 10, 30, 4.3e6): "))
                    if val <= 0:
                        print("Mass must be positive.")
                    else:
                        print(f"\nYou entered a custom mass: {val:.3g} M_sun\n")
                        return val
                except ValueError:
                    print("Please enter a valid number.")
        else:
            print("Invalid choice, try again.")


def get_distance(m_kg: float) -> float:
    """
    Ask the user for a distance from the center, either:
    - in kilometers, or
    - as a multiple of the Schwarzschild radius.
    Returns the distance in meters.
    """
    r_s = schwarzschild_radius(m_kg)
    r_s_km = r_s / 1000.0

    print("How would you like to specify your distance from the black hole center?")
    print("  1. In kilometers")
    print("  2. As a multiple of the Schwarzschild radius r_s")

    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice == "1":
            while True:
                try:
                    d_km = float(input("Enter distance from center in km (must be > 0): "))
                    if d_km <= 0:
                        print("Distance must be positive.")
                    else:
                        return d_km * 1000.0
                except ValueError:
                    print("Please enter a valid number.")
        elif choice == "2":
            print(f"Note: For this black hole, r_s ≈ {r_s_km:.3g} km.")
            while True:
                try:
                    factor = float(input("Enter distance as a multiple of r_s (e.g., 2, 5, 10): "))
                    if factor <= 0:
                        print("Factor must be positive.")
                    else:
                        return factor * r_s
                except ValueError:
                    print("Please enter a valid number.")
        else:
            print("Please enter 1 or 2.")


def get_body_height() -> float:
    """
    Ask for body height (for tidal calculation). Default is 2 m.
    Returns height in meters.
    """
    print("\nWe will estimate tidal forces across your body height.")
    print("Default is 2.0 m (rough human height).")
    text = input("Enter body height in meters, or press Enter to use 2.0 m: ").strip()

    if text == "":
        return 2.0

    try:
        h = float(text)
        if h <= 0:
            print("Height must be positive. Using default 2.0 m.")
            return 2.0
        return h
    except ValueError:
        print("Invalid input. Using default 2.0 m.")
        return 2.0


def main() -> None:
    print_intro()

    # 1. Choose black hole
    m_sun = choose_black_hole()
    m_kg = solar_mass_to_kg(m_sun)

    # 2. Get distance and body height
    r_m = get_distance(m_kg)
    h_m = get_body_height()

    # 3. Compute physics quantities
    r_s = schwarzschild_radius(m_kg)
    g_here = gravity_at_radius(m_kg, r_m)
    delta_g = tidal_acceleration(m_kg, r_m, h_m)

    # Kepler orbital period (only meaningful outside the horizon)
    if r_m > r_s:
        period_s = kepler_orbital_period(m_kg, r_m)
    else:
        period_s = None  # no physical circular orbit here

    # 4. Convert for reporting
    r_s_km = r_s / 1000.0
    r_km = r_m / 1000.0
    multiples_of_rs = r_m / r_s if r_s > 0 else float("inf")

    # 5. Print results
    print("\n" + "=" * 72)
    print(" RESULTS")
    print("=" * 72)
    print(f"Black hole mass:          {m_sun:.4g} M_sun")
    print(f"Schwarzschild radius r_s: {r_s_km:.4g} km")
    print(f"Your distance r:          {r_km:.4g} km")
    print(f"Distance in units of r_s: {multiples_of_rs:.4g} r_s")

    if multiples_of_rs <= 1.0:
        print("\n>>> You are at or inside the event horizon (r ≤ r_s).")
        print("    Classically, not even light can escape here.")

    print("\nGravitational acceleration at your position:")
    print(f"  g(r) = {g_here:.4e} m/s^2")
    print(f"      ≈ {g_here / G_EARTH:.3g} times Earth surface gravity (g_earth).")

    print("\nTidal acceleration across your body:")
    print(f"  Δg ≈ |g(head) − g(feet)| ≈ {delta_g:.4e} m/s^2")
    print(f"      ≈ {delta_g / G_EARTH:.3g} g_earth over a height of {h_m:.2f} m.\n")

    print("Spaghettification assessment:")
    print("  " + classify_spaghettification(delta_g) + "\n")

    # --- Kepler part: orbital period explanation ---
    print("Kepler Orbital Period Near the Black Hole:")
    if period_s is None:
        print("  At your chosen radius, you are at or inside r_s, so a circular")
        print("  orbit in the usual Kepler sense is not physically meaningful.")
        print("  In full general relativity, particle trajectories here are")
        print("  described by geodesics that inevitably fall inward.\n")
    else:
        period_hours = period_s / 3600.0
        period_days = period_s / SECONDS_PER_DAY
        period_years = period_s / SECONDS_PER_YEAR

        print(f"  Using Kepler's Third Law (Newtonian form):")
        print(f"    P = 2π * sqrt(r^3 / (G M))")
        print(f"  we estimate that a small object on a circular orbit at your")
        print(f"  radius would have an orbital period:")
        print(f"    P ≈ {period_s:.4e} seconds")
        print(f"      ≈ {period_hours:.3g} hours")
        print(f"      ≈ {period_days:.3g} days")
        print(f"      ≈ {period_years:.3g} Earth years\n")

        print("  Interpretation:")
        print("    • Far from the black hole, this period behaves like the usual")
        print("      Kepler law you saw for planets: P^2 ∝ a^3.")
        print("    • Close to a black hole, the same formula (still Newtonian)")
        print("      shows how orbits can become very fast: small radii give")
        print("      extremely short orbital periods.")
        print("    • A more precise treatment would use general relativity, but")
        print("      this Newtonian+Schwarzschild picture already shows how")
        print("      gravity, orbital motion, and tidal forces are linked.\n")

    print("Notes:")
    print("  - g(r) = GM / r^2 comes from Newton's law of gravity (Lessons 6–7).")
    print("  - The Schwarzschild radius r_s = 2GM / c^2 is the relativistic")
    print("    radius of the event horizon (Lesson 11: ~3 km per solar mass).")
    print("  - Tidal forces are estimated using the difference in g between")
    print("    your head and feet, which is what would stretch you.")
    print("  - Kepler’s Third Law (originally for planets) is repurposed here")
    print("    to describe orbital periods near compact objects, showing how")
    print("    dramatically orbital timescales shrink near black holes.\n")

    print("Thank you for using the Black Hole Tide, Spaghettification & Kepler Calculator!")
    print("=" * 72)


if __name__ == "__main__":
    main()
