import pandas as pd
import numpy as np
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# Load datasets
geo_df = pd.read_csv(r"C:\Users\Srinivasa Rao\OneDrive\Desktop\21VV1A1218\DS Project\geo1.csv")  # containing latitude, longitude, address
vehicle_df = pd.read_csv(r"C:\Users\Srinivasa Rao\OneDrive\Desktop\21VV1A1218\DS Project\vehicle path (Day).csv")  # containing vehicle_x, vehicle_y, vehicle_speed, vehicle_direction

# Filter out invalid latitude/longitude values in vehicle_df and geo_df
vehicle_df = vehicle_df[(vehicle_df['vehicle_y'] >= 0) & (vehicle_df['vehicle_y'] <= 90) &
                        (vehicle_df['vehicle_x'] >= 0) & (vehicle_df['vehicle_x'] <= 180)]

geo_df = geo_df[(geo_df['LATITUDE'] >= -90) & (geo_df['LATITUDE'] <= 90) &
                (geo_df['LONGITUDE'] >= -180) & (geo_df['LONGITUDE'] <= 180)]

# Check the range of coordinates in the datasets
print("Vehicle data latitude range:", vehicle_df['vehicle_y'].min(), vehicle_df['vehicle_y'].max())
print("Vehicle data longitude range:", vehicle_df['vehicle_x'].min(), vehicle_df['vehicle_x'].max())

print("Geo data latitude range:", geo_df['LATITUDE'].min(), geo_df['LATITUDE'].max())
print("Geo data longitude range:", geo_df['LONGITUDE'].min(), geo_df['LONGITUDE'].max())

# Sample the datasets for demonstration purposes
vehicle_sample_size = min(100, len(vehicle_df))
geo_sample_size = min(50, len(geo_df))

sampled_vehicle_df = vehicle_df.sample(n=vehicle_sample_size, random_state=42)
sampled_geo_df = geo_df.sample(n=geo_sample_size, random_state=42)

# Function to create a graph from sampled_geo_df
def create_graph(geo_df):
    G = nx.Graph()
    for i in range(len(geo_df) - 1):
        point1 = (geo_df.iloc[i]['LATITUDE'], geo_df.iloc[i]['LONGITUDE'])
        point2 = (geo_df.iloc[i + 1]['LATITUDE'], geo_df.iloc[i + 1]['LONGITUDE'])
        distance = geodesic(point1, point2).meters  # Calculate distance between two points
        G.add_edge(point1, point2, weight=distance)  # Add edge with distance as weight
    return G

# Create the graph based on the sampled geo data
G = create_graph(sampled_geo_df)

# Function to find the closest road segment for a GPS point
def find_closest_road(G, gps_point):
    closest_node = min(G.nodes, key=lambda node: geodesic(gps_point, node).meters)
    return closest_node

# Match each vehicle's GPS trajectory to the road network for the sampled data
matched_points = []
for index, row in sampled_vehicle_df.iterrows():
    gps_point = (row['vehicle_y'], row['vehicle_x'])
    closest_road = find_closest_road(G, gps_point)
    matched_points.append(closest_road)

# Add the matched road points to the sampled_vehicle_df
sampled_vehicle_df['matched_road'] = matched_points

# Visualize the graph and matched points
pos = {node: node for node in G.nodes}
nx.draw(G, pos, with_labels=False, node_size=10, node_color='blue', edge_color='gray')

# Plot the matched points as red dots
for matched_point in matched_points:
    plt.plot(matched_point[1], matched_point[0], 'ro')  # Red points for matched roads

plt.title("Sampled Graph and Matched GPS Points")
plt.show()

# View the results of the sampled vehicle data with matched roads
print(sampled_vehicle_df[['vehicle_x', 'vehicle_y', 'vehicle_speed', 'matched_road']].head())
