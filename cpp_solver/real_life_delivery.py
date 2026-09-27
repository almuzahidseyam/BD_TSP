import folium
import requests
import json
import subprocess
import os

# 15 Major Distribution Hubs for real-life logistics problem
hubs = [
    "Dhaka", "Chattogram", "Sylhet", "Rajshahi", "Khulna", 
    "Barishal", "Rangpur", "Mymensingh", "Cumilla", "Gazipur", 
    "Narayanganj", "Bogura", "Jashore", "Faridpur", "Cox's Bazar"
]

coords_dict = {
    "Dhaka": (23.8103, 90.4125), "Chattogram": (22.3569, 91.7832), "Sylhet": (24.8949, 91.8687),
    "Rajshahi": (24.3745, 88.6042), "Khulna": (22.8456, 89.5403), "Barishal": (22.7010, 90.3535),
    "Rangpur": (25.7439, 89.2752), "Mymensingh": (24.7471, 90.4203), "Cumilla": (23.4607, 91.1809),
    "Gazipur": (24.0023, 90.4264), "Narayanganj": (23.6238, 90.5000), "Bogura": (24.8465, 89.3778),
    "Jashore": (23.1661, 89.2083), "Faridpur": (23.6071, 89.8429), "Cox's Bazar": (21.4339, 92.0058)
}

def get_osrm_matrix():
    print("[1/4] Fetching real driving distance matrix from OSRM...")
    coords_string = ";".join([f"{coords_dict[h][1]},{coords_dict[h][0]}" for h in hubs])
    url = f"http://router.project-osrm.org/table/v1/driving/{coords_string}?annotations=distance"
    response = requests.get(url).json()
    return response['distances']

def solve_with_cpp(matrix):
    print("[2/4] Compiling C++ DP Engine...")
    os.system("g++ tsp_dp.cpp -o tsp_dp -O3")
    
    print("[3/4] Running O(N^2 * 2^N) Dynamic Programming on C++...")
    n = len(hubs)
    input_data = f"{n}\n"
    for row in matrix:
        input_data += " ".join(map(str, row)) + "\n"
        
    process = subprocess.Popen(["./tsp_dp"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    out, _ = process.communicate(input_data)
    
    lines = out.strip().split("\n")
    min_dist = float(lines[0]) / 1000.0  # Convert meters to km
    path_indices = list(map(int, lines[1].split()))
    optimal_path = [hubs[i] for i in path_indices]
    
    print(f"      => Exact Optimal Distance: {min_dist:.2f} km")
    print(f"      => Exact Sequence: {' -> '.join(optimal_path)}")
    return optimal_path

def plot_route(optimal_path):
    print("[4/4] Generating Interactive Route Map...")
    coords_string = ";".join([f"{coords_dict[d][1]},{coords_dict[d][0]}" for d in optimal_path])
    url = f"http://router.project-osrm.org/route/v1/driving/{coords_string}?overview=full&geometries=geojson"
    res = requests.get(url).json()
    
    if res["code"] != "Ok":
        print("Error fetching route!")
        return

    geometry = res["routes"][0]["geometry"]["coordinates"]
    route_points = [(lat, lon) for lon, lat in geometry]
    
    m = folium.Map(location=[23.6850, 90.3563], zoom_start=7, tiles='CartoDB Positron')
    
    folium.PolyLine(route_points, weight=5, color="blue", opacity=0.8).add_to(m)
    
    for i, city in enumerate(optimal_path[:-1]):
        icon_color = 'red' if i == 0 else 'green'
        icon_name = 'star' if i == 0 else 'info-sign'
        folium.Marker(
            location=coords_dict[city],
            popup=f"Stop {i}: {city}",
            tooltip=f"{i}. {city}",
            icon=folium.Icon(color=icon_color, icon=icon_name)
        ).add_to(m)
        
    m.save("bd_logistics_real_life_route.html")
    print("Done! Map saved to bd_logistics_real_life_route.html")

if __name__ == '__main__':
    matrix = get_osrm_matrix()
    optimal_path = solve_with_cpp(matrix)
    plot_route(optimal_path)
