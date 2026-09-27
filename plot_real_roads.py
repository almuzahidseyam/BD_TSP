import folium
import requests
import time

user_ordered_districts = [
    "Chandpur", "Cumilla", "Feni", "Noakhali", "Lakshmipur", "Chattogram", "Cox's Bazar", "Bandarban", "Rangamati", "Khagrachari", "Brahmanbaria",
    "Habiganj", "Moulvibazar", "Sylhet", "Sunamganj", "Netrokona", "Mymensingh", "Jamalpur", "Sherpur",
    "Tangail", "Kishoreganj", "Narsingdi", "Gazipur", "Narayanganj", "Dhaka", "Munshiganj", "Manikganj", "Rajbari", "Faridpur", "Madaripur", "Shariatpur", "Gopalganj",
    "Pirojpur", "Barishal", "Jhalokati", "Bhola", "Patuakhali", "Barguna",
    "Bagerhat", "Khulna", "Satkhira", "Jashore", "Narail", "Magura", "Jhenaidah", "Chuadanga", "Meherpur", "Kushtia",
    "Pabna", "Natore", "Rajshahi", "Chapainawabganj", "Naogaon", "Joypurhat", "Bogura", "Sirajganj",
    "Gaibandha", "Rangpur", "Nilphamari", "Panchagarh", "Thakurgaon", "Dinajpur", "Lalmonirhat", "Kurigram"
]

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

m = folium.Map(location=[23.6850, 90.3563], zoom_start=7, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', attr='Esri')

def get_driving_route(lat1, lon1, lat2, lon2):
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('code') == 'Ok':
            # OSRM returns [lon, lat], folium needs [lat, lon]
            coords = data['routes'][0]['geometry']['coordinates']
            return [[lat, lon] for lon, lat in coords]
    except Exception as e:
        print(f"Routing failed for {lat1},{lon1} to {lat2},{lon2}: {e}")
    return [[lat1, lon1], [lat2, lon2]] # Fallback to straight line if API fails

print("Calculating actual road routes using OSRM Navigation Engine...")

# Include the return trip back to Chandpur
route_sequence = user_ordered_districts + ["Chandpur"]

for i in range(len(route_sequence) - 1):
    start_city = route_sequence[i]
    end_city = route_sequence[i+1]
    
    start_coords = coords_dict[start_city]
    end_coords = coords_dict[end_city]
    
    print(f"Routing: {start_city} -> {end_city}")
    road_path = get_driving_route(start_coords[0], start_coords[1], end_coords[0], end_coords[1])
    
    folium.PolyLine(road_path, weight=4, color='blue', opacity=0.8).add_to(m)
    time.sleep(0.5) # Prevent rate-limiting from OSRM

# Add numbered markers
for step, dist_name in enumerate(user_ordered_districts):
    coord = coords_dict[dist_name]
    color = 'green' if step == 0 else 'red'
    folium.Marker(
        location=coord,
        popup=f"Stop {step+1}: {dist_name}",
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

m.save('bangladesh_real_road_route.html')
print("Successfully generated bangladesh_real_road_route.html")
