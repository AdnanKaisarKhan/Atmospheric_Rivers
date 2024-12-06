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
    # - IMPORTANT - Change the 'time_index' as required.
    # - netCDF data downloaded from: https://apps.ecmwf.int/datasets/data/tigge/levtype=pl/type=cf/

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset, num2date
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as ticker

# Open the NetCDF file
file_path = 'D:/Temp/Temp_03_Sep_2014.nc'
nc_file = Dataset(file_path, 'r')

# Temperature
t2m = nc_file.variables['t2m'][:]

# Convert tp from K to C
t2m_c = t2m - 273.15

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
    
# Select the desired time index
time_index = 13  # In this case: 0-23

# Mask zero values
t2m_c_masked = np.ma.masked_where(t2m_c[time_index, :, :] == 0, t2m_c[time_index, :, :])

# Create a meshgrid
lon, lat = np.meshgrid(lon, lat)

plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

# Add other features
ax.coastlines(resolution = '10m')
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.OCEAN)

# Plot the data
levels = np.linspace(-20, 40, 11)
Temp_plot = ax.contourf(lon, lat, t2m_c_masked, cmap='RdYlBu_r', transform=ccrs.PlateCarree(), levels=levels, extend='both')

# Add contour lines
contours = ax.contour(lon, lat, t2m_c_masked, colors='black', linewidths=0.5, transform=ccrs.PlateCarree(), levels=levels)

# Add latitude and longitude gridlines
gridlines = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linewidth=0.5)

gridlines.xlocator = ticker.MultipleLocator(9)  # For longitude
gridlines.ylocator = ticker.MultipleLocator(9)  # For latitude

# Add colorbar
plt.colorbar(Temp_plot, label='Temperature (°C)', extend='both', shrink=0.9, pad=0.06)

plt.title(f'Temperature at 2m (ERA5) ({time_converted[time_index].strftime('Date: ' "%Y-%m-%d" '  Time: ' "%H:%M:%S")})', pad = 20)

plt.savefig('D:/Temp/Plot_Temp_2014_09_03.png', dpi = 600)
print("Image saved as 'Plot_Temp_2014_09_03.png")

plt.show()

