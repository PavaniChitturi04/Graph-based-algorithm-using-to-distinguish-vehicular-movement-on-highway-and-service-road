# Vehicle Path and Road Network Matching

This project implements a map-matching algorithm that matches vehicle GPS trajectory points to the closest road segments using geospatial data. The primary goal is to map vehicle movements onto a known road network and visualize the matched points. The project uses Python, NetworkX, and GeoPy libraries.

## Features

- **Data Cleaning**: Filters out invalid vehicle and geo data points.
- **Graph Construction**: Builds a road network graph based on geographical data.
- **GPS Point Matching**: Matches each vehicle's GPS point to the closest road segment.
- **Visualization**: Displays a graph of the road network and highlights the matched GPS points.

## Prerequisites

Ensure that you have the following libraries installed:

```bash
pip install pandas numpy networkx geopy matplotlib
```
## File Descriptions

- **geo1.csv**: Contains the road network data with columns for `LATITUDE`, `LONGITUDE`, and `ADDRESS`.
- **vehicle path (Day).csv**: Contains vehicle GPS data with columns for `vehicle_x`, `vehicle_y`, `vehicle_speed`, and `vehicle_direction`.

## Code Overview

### Data Loading
First, the vehicle and geo datasets are loaded, and invalid latitude/longitude values are filtered out.

```python
geo_df = pd.read_csv("geo1.csv")
vehicle_df = pd.read_csv("vehicle path (Day).csv")

# Filtering invalid GPS points
vehicle_df = vehicle_df[(vehicle_df['vehicle_y'] >= 0) & (vehicle_df['vehicle_y'] <= 90) &
                        (vehicle_df['vehicle_x'] >= 0) & (vehicle_df['vehicle_x'] <= 180)]
```

### Graph Creation
A graph is created from the geo dataset, where each node represents a point on the map (latitude, longitude), and the edge weights are the geodesic distances between these points.

```python
def create_graph(geo_df):
    G = nx.Graph()
    for i in range(len(geo_df) - 1):
        point1 = (geo_df.iloc[i]['LATITUDE'], geo_df.iloc[i]['LONGITUDE'])
        point2 = (geo_df.iloc[i + 1]['LATITUDE'], geo_df.iloc[i + 1]['LONGITUDE'])
        distance = geodesic(point1, point2).meters
        G.add_edge(point1, point2, weight=distance)
    return G
```

### Finding Closest Road
The script finds the closest road segment for each vehicle's GPS point by comparing the geodesic distance between the vehicle's point and the nodes in the road network graph.

```python
def find_closest_road(G, gps_point):
    closest_node = min(G.nodes, key=lambda node: geodesic(gps_point, node).meters)
    return closest_node
```

### Visualization
After matching the GPS points to the road network, the road graph is plotted in blue, and the matched vehicle points are plotted in red.

```python
nx.draw(G, pos, with_labels=False, node_size=10, node_color='blue', edge_color='gray')

for matched_point in matched_points:
    plt.plot(matched_point[1], matched_point[0], 'ro')

plt.title("Sampled Graph and Matched GPS Points")
plt.show()
```

### Sample Output
The output includes the `vehicle_x`, `vehicle_y`, `vehicle_speed`, and the `matched_road` (closest road segment for each vehicle).

```bash
   vehicle_x   vehicle_y   vehicle_speed   matched_road
0  120.34000   45.12000    60             (45.15000, 120.38000)
1  110.23000   35.21000    50             (35.25000, 110.24000)
```
