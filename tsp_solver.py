import folium
import numpy as np
from scipy.spatial.distance import cdist
from geopy.geocoders import Nominatim
import time

districts = [
    "Chandpur", "Lakshmipur", "Noakhali", "Feni", "Chattogram", "Cox's Bazar", "Bandarban", "Rangamati", "Khagrachari",
    "Cumilla", "Brahmanbaria", "Habiganj", "Moulvibazar", "Sylhet", "Sunamganj",
    "Netrokona", "Mymensingh", "Sherpur", "Jamalpur",
    "Kurigram", "Lalmonirhat", "Nilphamari", "Panchagarh", "Thakurgaon", "Dinajpur", "Rangpur", "Gaibandha",
    "Joypurhat", "Bogura", "Naogaon", "Chapainawabganj", "Rajshahi", "Natore", "Sirajganj", "Pabna",
    "Kushtia", "Meherpur", "Chuadanga", "Jhenaidah", "Magura", "Narail", "Jashore", "Satkhira", "Khulna", "Bagerhat",
    "Pirojpur", "Jhalokati", "Barguna", "Patuakhali", "Bhola", "Barishal",
    "Gopalganj", "Faridpur", "Rajbari", "Manikganj", "Tangail", "Gazipur", "Kishoreganj", "Narsingdi", "Narayanganj", "Dhaka", "Munshiganj", "Madaripur", "Shariatpur"
]

# Hardcoded approximate coordinates for speed and reliability (Lat, Lon)
coords_dict = {
    "Chandpur": (23.2333, 90.6667), "Lakshmipur": (22.9425, 90.8412), "Noakhali": (22.8696, 91.0993), 
    "Feni": (23.0159, 91.3976), "Chattogram": (22.3569, 91.7832), "Cox's Bazar": (21.4339, 92.0058),
    "Bandarban": (22.1953, 92.2184), "Rangamati": (22.6533, 92.1525), "Khagrachari": (23.1193, 91.9847),
    "Cumilla": (23.4607, 91.1809), "Brahmanbaria": (23.9571, 91.1119), "Habiganj": (24.3749, 91.4155),
    "Moulvibazar": (24.4829, 91.7774), "Sylhet": (24.8949, 91.8687), "Sunamganj": (25.0658, 91.4051),
    "Netrokona": (24.8710, 90.7289), "Mymensingh": (24.7471, 90.4203), "Sherpur": (25.0205, 90.0153),
    "Jamalpur": (24.9196, 89.9481), "Kurigram": (25.8054, 89.6362), "Lalmonirhat": (25.9923, 89.2847),
    "Nilphamari": (25.9318, 88.8560), "Panchagarh": (26.3354, 88.5517), "Thakurgaon": (26.0337, 88.4617),
    "Dinajpur": (25.6217, 88.6355), "Rangpur": (25.7439, 89.2752), "Gaibandha": (25.3288, 89.5281),
    "Joypurhat": (25.1012, 89.0270), "Bogura": (24.8465, 89.3778), "Naogaon": (24.8021, 88.9405),
    "Chapainawabganj": (24.5965, 88.2775), "Rajshahi": (24.3745, 88.6042), "Natore": (24.4206, 89.0115),
    "Sirajganj": (24.4534, 89.7007), "Pabna": (24.0041, 89.2425), "Kushtia": (23.9013, 89.1205),
    "Meherpur": (23.7622, 88.6318), "Chuadanga": (23.6402, 88.8418), "Jhenaidah": (23.5450, 89.1726),
    "Magura": (23.4873, 89.4198), "Narail": (23.1725, 89.5126), "Jashore": (23.1661, 89.2083),
    "Satkhira": (22.7185, 89.0705), "Khulna": (22.8456, 89.5403), "Bagerhat": (22.6516, 89.7859),
    "Pirojpur": (22.5841, 89.9720), "Jhalokati": (22.6406, 90.1987), "Barguna": (22.1557, 90.1156),
    "Patuakhali": (22.3596, 90.3188), "Bhola": (22.6859, 90.6480), "Barishal": (22.7010, 90.3535),
    "Gopalganj": (23.0051, 89.8267), "Faridpur": (23.6071, 89.8429), "Rajbari": (23.7574, 89.6445),
    "Manikganj": (23.8644, 90.0047), "Tangail": (24.2478, 89.9175), "Gazipur": (24.0023, 90.4264),
    "Kishoreganj": (24.4449, 90.7765), "Narsingdi": (23.9189, 90.7108), "Narayanganj": (23.6238, 90.5000),
    "Dhaka": (23.8103, 90.4125), "Munshiganj": (23.5422, 90.5305), "Madaripur": (23.1641, 90.1897),
    "Shariatpur": (23.2082, 90.3475)
}

# Ensure all 64 are matched
ordered_names = list(coords_dict.keys())
coords = np.array([coords_dict[name] for name in ordered_names])

# Calculate distance matrix (Euclidean approximation for TSP optimization)
dist_matrix = cdist(coords, coords)

# Greedy Nearest Neighbor TSP Starting from Chandpur (Index 0)
n = len(ordered_names)
unvisited = set(range(1, n))
tour = [0]
current = 0

while unvisited:
    next_node = min(unvisited, key=lambda x: dist_matrix[current][x])
    unvisited.remove(next_node)
    tour.append(next_node)
    current = next_node

tour.append(0) # Return to Chandpur

# Create Folium Map
m = folium.Map(location=[23.6850, 90.3563], zoom_start=7, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', attr='Esri')

# Draw route
route_coords = [coords[i] for i in tour]
folium.PolyLine(route_coords, weight=2, color='blue', opacity=0.8).add_to(m)

# Add markers
for step, idx in enumerate(tour[:-1]):
    name = ordered_names[idx]
    coord = coords[idx]
    color = 'green' if step == 0 else 'red'
    folium.Marker(
        location=coord, 
        popup=f"Step {step+1}: {name}",
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

m.save('bangladesh_tsp_map.html')
print("Map generated: bangladesh_tsp_map.html")


