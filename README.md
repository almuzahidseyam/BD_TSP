# Bangladesh 64-District TSP Optimizer 🇧🇩🗺️

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![OSRM](https://img.shields.io/badge/Routing-OSRM_API-green.svg)
![Folium](https://img.shields.io/badge/Map-Folium-orange.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)

This project calculates the **absolute shortest driving route** to visit all 64 district headquarters in Bangladesh. It solves the classic Traveling Salesperson Problem (TSP) using real-world road distances and road network geometries.

## ✨ Features
* **Real Road Distances:** Unlike standard Euclidean (straight-line) TSP solvers that plot lines across rivers and oceans, this project queries the **OSRM (Open Source Routing Machine) API** to get real driving distances and durations.
* **2-Opt Optimization Algorithm:** Uses a heuristic algorithm to heavily optimize the travel path, removing crossed paths and shrinking total travel distance.
* **Interactive Maps:** Renders fully interactive, zoomable HTML maps using olium. The final map (angladesh_ultimate_optimized_route.html) plots the exact road curvature connecting all 64 districts.

## 📂 Repository Contents
* 	sp_solver.py - Basic straight-line TSP calculator.
* plot_user_route.py - Evaluates a manual, human-planned route.
* plot_real_roads.py - Queries the OSRM /route/ API to draw the actual road geometries for a given sequence.
* plot_ultimate_tsp.py - **The main script.** Queries the OSRM 64x64 distance matrix, runs the 2-opt optimizer, fetches the exact road geometries, and generates the final interactive map.
* *.html - The generated interactive Folium maps.

## 🚀 How to Run Locally

### 1. Install Dependencies
`ash
python -m venv venv
venv\Scripts\activate
pip install folium requests polyline
`

### 2. Generate the Ultimate Route
`ash
python plot_ultimate_tsp.py
`
*This will fetch the data and generate angladesh_ultimate_optimized_route.html in your directory.*

## 📄 License
This project is licensed under the MIT License.


## 🚀 NEW: Real-Life Logistics DP Solver (C++ & Python)
Standard TSP for 64 districts uses a 2-opt heuristic because an exact calculation using Dynamic Programming takes O(N^2 * 2^N) time (mathematically impossible for N=64).

To demonstrate a **real-life competitive programming / logistics solution**, we created a C++ Dynamic Programming engine (cpp_solver/tsp_dp.cpp) based on the **Held-Karp Algorithm**.

It calculates the absolute perfect delivery route for **15 Major Commercial Hubs** in Bangladesh (Dhaka, Chattogram, Sylhet, etc.).
1. The Python script (cpp_solver/real_life_delivery.py) fetches the real OSRM driving matrix.
2. It compiles and feeds the matrix to the C++ DP engine.
3. The C++ engine uses Bitmask DP to find the exact shortest path in milliseconds.
4. Python generates the final map (d_logistics_real_life_route.html).

**Run the Real-Life Hub Solver:**
`ash
cd cpp_solver
python real_life_delivery.py
`
