# Final_project_Astro_12600

# 🌌 Black Hole Spaghettification & Orbital Dynamics Simulator
**ASTR/PHSC 12600 Final Project – University of Chicago**

This project is a computational and **Streamlit web application** that models tidal forces (“spaghettification”) and orbital periods near astrophysical black holes, using physics concepts directly from the course lectures.

The project includes:
* A Python scientific backend that computes gravitational acceleration, tidal stretching, Schwarzschild radius, and Keplerian orbital periods.
* A **single-file Streamlit application (`app.py`)** that hosts the physics calculations and creates the interactive frontend interface.
* A complete quantitative analysis component, satisfying the final project expectations.
* An accompanying explanation that synthesizes three key course lectures.

## 🚀 Live Application

You can access and interact with the deployed simulator immediately via the Streamlit Community Cloud:

**[Live Simulator Link](https://finalprojectastro12600-m7oypjvuupepgknjuhnier.streamlit.app/)**

---
---

## 📌 Project Motivation

Tidal forces around black holes are among the most extreme gravitational phenomena in the universe. As an object approaches a black hole, the gravitational pull on the side closer to the black hole becomes significantly stronger than on the far side, producing intense stretching forces—the so-called **spaghettification effect**. 

At the same time, orbital motion near black holes remains governed, at moderate radii, by Kepler’s Third Law. By combining these ideas, the project demonstrates how Newtonian gravity still provides valuable intuition even in relativistic environments.

---

## 📘 Synthesis of Lecture Material

This project explicitly synthesizes material from at least three course lectures, satisfying the requirement described in the Final Project Checklist Form and the Final Project Rubric.

* **Lecture 7–8: Newtonian Gravity**
    * Used to compute gravitational acceleration: $g(r)=\frac{GM}{r^2}$
    * Used to compute tidal forces by comparing gravitational pull at two distances ($\Delta g = |g(r) - g(r+h)|$).

* **Lecture 11: Black Holes**
    * Used the Schwarzschild radius formula: $r_s = \frac{2GM}{c^2}$
    * Used course intuition that ($r_s \approx 3 \text{ km}$) per solar mass.
    * Distinguishes between being outside vs. inside the event horizon.

* **Lecture 6: on Kepler’s 3rd Law**
    * Applied the Newtonian orbital period formula: $P = 2\pi\sqrt{\frac{r^3}{GM}}$
    * Used to compute how orbital periods dramatically shorten near compact objects.

---

## 🔢 Quantitative Analysis Component

The project includes multiple quantitative components, fully satisfying the requirement in the project instructions:

* Schwarzschild Radius Calculation
* Newtonian Gravitational Acceleration at a given radius
* Tidal Acceleration (Spaghettification Strength): $\Delta g = |g(r) - g(r+h)|$
* Keplerian Orbital Period Calculation: $P = 2\pi \sqrt{\frac{r^3}{GM}}$
* Unit conversions (solar masses → kg; meters → kilometers).

All results are displayed numerically, with clear units and qualitative interpretation for the user.

---

## 🧠 What the Simulator Does

The interactive application lets the user enter:

* Black hole mass (choose from known astrophysical BHs or enter custom)
* Distance from the black hole (in $\text{km}$ or multiples of $r_s$)
* Personal height (for tidal calculations, default $2.0 \text{ m}$)

The program then computes and explains:

* **✔ Schwarzschild Radius:** Shows whether the user is outside or inside the event horizon.
* **✔ Gravitational Acceleration:** Displays both $\text{m/s}^2$ and Earth-gravity multiples (“$g_{\oplus}$”).
* **✔ Tidal Acceleration:** Displays the $\Delta g$ value and the qualitative level of stretching (e.g., "Negligible" vs. "Extreme Spaghettification").
* **✔ Keplerian Orbital Period:** Shows the orbital period at that radius.

---

## 🖥 Technology Stack

This project uses a minimalist, Python-only stack for simplicity and rapid deployment:

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend/Frontend** | **Python 3 + Streamlit** | Single-file application for both physics logic and web interface. |
| **Deployment** | **GitHub + Streamlit Community Cloud** | Hosted directly from the main branch. |

---

## 📁 Repository Structure

black-hole-spaghetti/ ├── app.py # Single file containing all Streamlit UI and physics logic └── requirements.txt # Lists required libraries (only 'streamlit')

---

## ▶️ How to Run the Project Locally

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/awujira29/Final_project_Astro_12600](https://github.com/awujira29/Final_project_Astro_12600)
    cd Final_project_Astro_12600
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Web App:**
    ```bash
    streamlit run app.py
    ```

The application will automatically open in your web browser, typically at `http://localhost:8501`.

---

## 🌠 Scientific Interpretation Included in the Frontend

The front end shows:

* **✔ Why tidal forces increase as you approach a black hole:** Explains differential gravity and stretching.
* **✔ Why supermassive black holes have weaker tidal forces at the horizon:** Demonstrates the surprising course idea that big black holes are “gentler.”
* **✔ Why Kepler’s Third Law works surprisingly well even near compact objects:** Relates orbital motion to Newtonian intuition and the $r^3$ dependence.
* **✔ Why being inside the Schwarzschild radius means no stable orbit or escape:** Connects to the concept of “no escape even at light speed.”

These conceptual explanations appear directly below the numerical outputs so users understand not only the numbers but also the science.
