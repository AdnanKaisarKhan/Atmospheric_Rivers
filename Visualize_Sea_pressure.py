# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 12:57:31 2024

@author: Dell
"""

# Developed by:
    # Adnan Kaisar Khan & Dr. Munir Ahmad Nayak
    # National Institute of Technology Srinagar
    
# Please read the instructions before using this script:
    # - IMPORTANT - Change the 'file_path' to the desired path. 
    # - IMPORTANT - Change the 'data_ret' to either hour or day as per the requirement.
    # - IMPORTANT - If 'hour' is selected, change the 'time_index' as required.
    # - 'hour' gives us hourly precipitation map.
    # - 'day'  gives us daily  precipitation map.
    # - netCDF data downloaded from: https://apps.ecmwf.int/datasets/data/tigge/levtype=pl/type=cf/

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset, num2date
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as ticker

# Open the NetCDF file
file_path = 'D:/Nepal/Sea_pressure/eec3711ee19f642054031d2a677077c3.nc'
nc_file = Dataset(file_path, 'r')

# Total precipitation
tp = nc_file.variables['msl'][:]

# Convert tp from meters to millimeters
tp_mm = tp / 100

# Extract latitude, longitude, and time
lat = nc_file.variables['latitude'][:]
lon = nc_file.variables['longitude'][:]
time = nc_file.variables['valid_time'][:]  # Time in seconds since 1970-01-01

# Get the units of the time variable
time_units = nc_file.variables['valid_time'].units

# Convert time from seconds since 1970-01-01 to datetime
time_converted = num2date(time, units=time_units)

# Close the NetCDF file
nc_file.close()

# Select data to be retrieved
data_ret = 'hour'  # 'hour' or 'day'

if data_ret == 'hour':
    
    # Select the desired time index
    time_index = 96   # In this case: 0-23
    
    # Mask zero values
    tp_masked = np.ma.masked_where(tp_mm[time_index, :, :] == 0, tp_mm[time_index, :, :])
    
    # Create a meshgrid
    lon, lat = np.meshgrid(lon, lat)
    
    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Add other features
    ax.coastlines(resolution = '10m')
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.OCEAN)
    
    # Plot the data
    levels = np.linspace(1000, 1010, 10)
    precip_plot = ax.contourf(lon, lat, tp_masked, cmap='viridis_r', transform=ccrs.PlateCarree(), levels=levels, extend='both')
    
    # Add contour lines
    contours = ax.contour(lon, lat, tp_masked, colors='black', linewidths=0.5, transform=ccrs.PlateCarree(), levels=levels)
    
    # Add labels to the contours
    ax.clabel(contours, inline=True, fontsize=8, fmt='%1.1f')
    
    # Add latitude and longitude gridlines
    gridlines = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linewidth=0.5)
    
    gridlines.top_labels = gridlines.right_labels = False

    gridlines.xlocator = ticker.MultipleLocator(7)  # For longitude
    gridlines.ylocator = ticker.MultipleLocator(7)  # For latitude
    
    # Add colorbar
    plt.colorbar(precip_plot, label='pressure (mbar)', extend='both', pad=0.01)
    
    plt.title(f'Pressure (ERA5) (Time: {time_converted[time_index].strftime("%Y-%m-%d %H:%M:%S")})')
    
    plt.savefig('D:/Nepal/Sea_pressure/Sea_Pressure_2024_09_29.png', dpi = 600)
    print("Image saved as Sea_Pressure_2024_09_29.png")
    
    plt.show()

elif data_ret == 'day':
    
    # Sum the precipitation data
    total_tp = np.sum(tp_mm, axis=0)
    
    # Create a meshgrid
    lon, lat = np.meshgrid(lon, lat)
    
    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Add other features
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.OCEAN)
    
    # Plot the data
    levels = np.linspace(10, 200, 6)
    precip_plot = ax.contourf(lon, lat, total_tp, cmap='viridis_r', transform=ccrs.PlateCarree(), levels=levels, extend='max')
    
    # Add contour lines
    contours = ax.contour(lon, lat, total_tp, colors='black', linewidths=0.5, transform=ccrs.PlateCarree(), levels=levels)

    # Add latitude and longitude gridlines
    gridlines = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linewidth=0.5)
    
    gridlines.xlocator = ticker.MultipleLocator(7)  # For longitude
    gridlines.ylocator = ticker.MultipleLocator(7)  # For latitude
    
    # Add colorbar
    plt.colorbar(precip_plot, label='Total Precipitation (mm)', extend='max', pad=0.06)
    
    plt.title(f'Total Precipitation (ERA5) (Date: {time_converted[0].strftime("%Y-%m-%d")})', pad = 20)
    
    plt.savefig('D:/Nepal/ERA5/Plot_2014_09_06.png', dpi = 600)
    print("Image saved as 'Plot_2014_09_06.png")
    
    plt.show()

else:
    print('Invalid selection!')

#plt.savefig(f'D:/Flood/ERA5/Plot_{time_index}.png')
#print(f"Image saved as 'Plot_{time_index}.png'")



# - Another Method for day:
'''
elif data_ret == 'daynew':
    # Initialize an empty list
    tp_list = []
    
    # Loop over all time indices
    for index in range(24):
        # Extract precipitation
        tp = nc_file.variables['tp'][index, :, :]
        tp_mm = tp * 1000
        
        # Append the list
        tp_list.append(tp_mm)
    
    # Sum the precipitation 
    total_tp = np.sum(tp_list, axis=0)
    
    # Create a meshgrid
    lon, lat = np.meshgrid(lon, lat)
    
    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Add other features
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.OCEAN)
    
    # Plot the total precipitation   
    levels = np.linspace(5, 400, 10)
    precip_plot = ax.contourf(lon, lat, total_tp, cmap='viridis_r', transform=ccrs.PlateCarree(), levels=levels)
    
    # Adding contour lines
    contours = ax.contour(lon, lat, total_tp, colors='black', linewidths=0.5, transform=ccrs.PlateCarree(), levels=levels)
    
    # Add latitude and longitude gridlines
    gridlines = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linewidth=0.5)
    
    gridlines.xlocator = ticker.MultipleLocator(7)  # For longitude
    gridlines.ylocator = ticker.MultipleLocator(7)  # For latitude
    
    # Add colorbar
    plt.colorbar(precip_plot, label='Total Precipitation (mm)', extend='max', pad=0.06)
    
    plt.title(f'Total Precipitation (Date: {time_converted[0].strftime("%Y-%m-%d")})')
    
    plt.show()
'''


# - For Animation:
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from netCDF4 import Dataset, num2date
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from PIL import Image
import os

# Open the NetCDF file
file_path = 'D:/Flood/ERA5/ERA5_3_Sep_2014.nc'
nc_file = Dataset(file_path, 'r')

# Extract the total precipitation
tp = nc_file.variables['tp'][:]

# Convert tp from meters to millimeters
tp_mm = tp * 1000

# Extract latitude, longitude, and time
lat = nc_file.variables['latitude'][:]
lon = nc_file.variables['longitude'][:]
time = nc_file.variables['valid_time'][:]  # Time in seconds since 1970-01-01

# Get the units of the time variable
time_units = nc_file.variables['valid_time'].units

# Convert time from seconds since 1970-01-01 to datetime
time_converted = num2date(time, units=time_units)

# Close the NetCDF file
nc_file.close()

# Create a directory for images
if not os.path.exists('frames'):
    os.makedirs('frames')

# Create a plot with a base map
def create_frame(index):
    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Add other features
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, edgecolor='black')

    # Mask zero values
    tp_masked = np.ma.masked_where(tp_mm[index, :, :] == 0, tp_mm[index, :, :])

    # Create a meshgrid
    lon_grid, lat_grid = np.meshgrid(lon, lat)

    # Plot the data
    levels = np.linspace(2,40,30)
    precip_plot = ax.contourf(lon_grid, lat_grid, tp_masked, cmap='turbo', transform=ccrs.PlateCarree(),levels=levels)

    # Add colorbar
    plt.colorbar(precip_plot, label='Total Precipitation (mm)')

    # Set title with the selected time
    plt.title(f'Total Precipitation (Time: {time_converted[index].strftime("%Y-%m-%d %H:%M:%S")})')

    # Save the frame
    plt.savefig(f'frames/frame_{index:02d}.png')
    plt.close()

# Generate frames
for i in range(len(time_converted)):
    create_frame(i)

# Create a GIF from the frames
frames = [Image.open(f'frames/frame_{i:02d}.png') for i in range(len(time_converted))]
frames[0].save('D:/Flood/ERA5/Animation_3_Sep.gif', save_all=True, append_images=frames[1:], optimize=False, duration=500, loop=0)

print("GIF saved as 'Animation3.gif'")
'''
