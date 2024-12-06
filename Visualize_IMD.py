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
    # - IMPORTANT - Change the 'plt.savefig' path and file name as desired.
    # - IMPORTANT - Change the 'data_ret' to either 'day' or 'year' as per the requirement.
    # - IMPORTANT - If 'day' is selected, change the 'time_index' as required.
    # - 'day' gives us daily precipitation map.
    # - 'year'  gives us annual precipitation map.
    # - netCDF data downloaded from: https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_NetCDF.html

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset, num2date
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as ticker

# Open the NetCDF file
file_path = 'D:/Nepal/IMD_Rainfall/RF25_ind2023_rfp25.nc'
nc_file = Dataset(file_path, 'r')

# Total precipitation
rainfall_mm = nc_file.variables['RAINFALL'][:]

# Extract latitude, longitude, and time
lat = nc_file.variables['LATITUDE'][:]
lon = nc_file.variables['LONGITUDE'][:]
time = nc_file.variables['TIME'][:]  # Time in seconds since 1970-01-01

# Get the units of the time variable
time_units = nc_file.variables['TIME'].units

# Convert time from seconds since 1970-01-01 to datetime
time_converted = num2date(time, units=time_units)

# Close the NetCDF file
nc_file.close()

# Select data to be retrieved
data_ret = 'year'  # 'day' or 'year'

if data_ret == 'day':
    
    # Select the desired time index
    time_index = 200  # In this case: 0-364/365
    
    # Mask zero values
    rainfall_masked = np.ma.masked_where(rainfall_mm[time_index, :, :] == 0, rainfall_mm[time_index, :, :])
    
    # Create a meshgrid
    lon, lat = np.meshgrid(lon, lat)
    
    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Add other features
    ax.coastlines(resolution = '10m')
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.OCEAN)
    
    # Plot the data
    levels = np.linspace(10, 100, 5)
    rainfall_plot = ax.contourf(lon, lat, rainfall_masked, cmap='viridis_r', transform=ccrs.PlateCarree(), levels=levels, extend='max')
    
    # Add contour lines
    contours = ax.contour(lon, lat, rainfall_masked, colors='black', linewidths=0.5, transform=ccrs.PlateCarree(), levels=levels)

    # Add latitude and longitude gridlines
    gridlines = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linewidth=0.5)

    gridlines.xlocator = ticker.MultipleLocator(7)  # For longitude
    gridlines.ylocator = ticker.MultipleLocator(7)  # For latitude
    
    # Add colorbar
    plt.colorbar(rainfall_plot, label='Total Precipitation (mm)', extend='max', pad=0.06)
    
    plt.title(f'Total Precipitation (IMD) (Date: {time_converted[time_index].strftime("%Y-%m-%d")})', pad=20)
    
    plt.savefig(f'D:/Nepal/IMD_Rainfall/Plot_Rainfall_{time_converted[time_index].strftime("%Y_%m_%d")}.png', dpi = 600)
    print(f"Image saved as 'Plot_Rainfall_{time_converted[time_index].strftime("%Y_%m_%d")}.png")
    
    plt.show()

elif data_ret == 'year':
    
    # Sum the precipitation data
    total_rainfall = np.sum(rainfall_mm, axis=0)
    
    # Create a meshgrid
    lon, lat = np.meshgrid(lon, lat)
    
    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Add other features
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.OCEAN)
    
    # Plot the data
    levels = np.linspace(50, 2000, 4)
    rainfall_plot = ax.contourf(lon, lat, total_rainfall, cmap='viridis_r', transform=ccrs.PlateCarree(), levels=levels, extend='max')
    
    # Add contour lines
    contours = ax.contour(lon, lat, total_rainfall, colors='black', linewidths=0.5, transform=ccrs.PlateCarree(), levels=levels)

    # Add latitude and longitude gridlines
    gridlines = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linewidth=0.5)
    
    gridlines.xlocator = ticker.MultipleLocator(7)  # For longitude
    gridlines.ylocator = ticker.MultipleLocator(7)  # For latitude
    
    # Add colorbar
    plt.colorbar(rainfall_plot, label='Total Precipitation (mm)', extend='max', pad=0.06)
    
    plt.title(f'Total Precipitation (IMD) (Year: {time_converted[0].strftime("%Y")})', pad = 20)
    
    plt.savefig(f'D:/Nepal/IMD_Rainfall/Plot_Rainfall_Total_{time_converted[0].strftime("%Y")}.png', dpi = 600)
    print(f"Image saved as 'Plot_Rainfall_Total_{time_converted[0].strftime("%Y")}.png")
    
    plt.show()

else:
    print('Invalid selection!')

