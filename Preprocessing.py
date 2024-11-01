import matplotlib.pyplot as plt
import pandas as pd

vehicle_data = pd.read_csv("/kaggle/input/vehicular-movements-datasets/vehicle path (Day).csv")
geo_data = pd.read_csv("/kaggle/input/vehicular-movements-datasets/geo1.csv")

# Display the first few rows of each dataset to understand their structure
print("Vehicle Path Data:")
print(vehicle_data.head())

print("\nGeo1 Data:")
print(geo_data.head())

# Display basic info and statistics
print("\nVehicle Path Data Info:")
print(vehicle_data.info())

print("\nGeo1 Data Info:")
print(geo_data.info())

print("\nVehicle Path Data Statistics:")
print(vehicle_data.describe())

print("\nGeo1 Data Statistics:")
print(geo_data.describe())

print("\nMissing values in Vehicle Path Data:")
print(vehicle_data.isnull().sum())

print("\nMissing values in Geo1 Data:")
print(geo_data.isnull().sum())

# Drop or fill missing values as needed
vehicle_data = vehicle_data.dropna()  # or fillna() depending on the dataset characteristics
geo_data = geo_data.dropna()  # or fillna()

# Ensure correct data types
vehicle_data['timestep_time'] = pd.to_datetime(vehicle_data['timestep_time'])
# Similarly, convert other columns to their appropriate types if necessary

# Preview the cleaned data
print("\nCleaned Vehicle Path Data:")
print(vehicle_data.head())

print("\nCleaned Geo1 Data:")
print(geo_data.head())

# Initialize the Transformer for UTM Zone 14N to WGS84 (latitude/longitude)
transformer = Transformer.from_crs("epsg:32614", "epsg:4326", always_xy=True)

# Function to convert x-y to lat-long using the new Transformer class
def convert_xy_to_latlong(x, y):
    longitude, latitude = transformer.transform(x, y)
    return latitude, longitude

# Display the updated vehicle data with lat-long
print(vehicle_data[['vehicle_x', 'vehicle_y', 'latitude', 'longitude']].head())

data1=pd.read_csv("/kaggle/input/vehicular-movements-datasets/vehicle path (Day).csv")
# Scatter plot of vehicle positions
plt.scatter(data1['vehicle_x'], data1['vehicle_y'], c=data1['vehicle_speed'], cmap='viridis')
plt.colorbar(label='Speed')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Vehicle Positions and Speeds')
plt.show()
