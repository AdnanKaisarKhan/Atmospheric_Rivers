# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 15:45:48 2024

@author: Dell
"""

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset, num2date
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as ticker
import glob

data_ret = 'period'

if data_ret == 'day':
    
    # List of NetCDF files
    files = glob.glob('D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.*.65E_17N_91E_40N.nc')
    
    # Initialize arrays
    total_tp_sum = None
    lat, lon, time_converted = None, None, None
    
    # Loop through each NetCDF file
    for file_path in files:
        # Open the NetCDF file
        nc_file = Dataset(file_path, 'r')
        
        # Total precipitation
        tp_mm = nc_file.variables['GPM_3IMERGHHL_07_precipitation'][:]
        
        # Extract latitude, longitude, and time
        lat = nc_file.variables['lat'][:]
        lon = nc_file.variables['lon'][:]
        time = nc_file.variables['time'][:]  # Time in seconds since 1970-01-01 00:00:00
        
        # Get the units of the time variable
        time_units = nc_file.variables['time'].units
        
        # Convert time from seconds since 1970-01-01 to datetime
        time_converted = num2date(time, units=time_units)
        
        # Accumulate the precipitation data
        if total_tp_sum is None:
            total_tp_sum = np.sum(tp_mm, axis=0)
        else:
            total_tp_sum += np.sum(tp_mm, axis=0)
        
        # Close the NetCDF file
        nc_file.close()
    
    # Create a meshgrid
    lon, lat = np.meshgrid(lon, lat)
    
    # Plotting the combined precipitation data
    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Add other features
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.OCEAN)
    
    # Plot the data
    levels = np.linspace(50, 650, 7)
    precip_plot = ax.contourf(lon, lat, total_tp_sum, cmap='viridis_r', transform=ccrs.PlateCarree(), levels=levels, extend='max')
    
    # Add contour lines
    contours = ax.contour(lon, lat, total_tp_sum, colors='black', linewidths=0.5, transform=ccrs.PlateCarree(), levels=levels)
    
    # Add latitude and longitude gridlines
    gridlines = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linewidth=0.5)
    
    gridlines.top_labels = gridlines.right_labels = False
    gridlines.bottom_labels = gridlines.left_labels = True
    
    gridlines.xlocator = ticker.MultipleLocator(7)  # For longitude
    gridlines.ylocator = ticker.MultipleLocator(7)  # For latitude
    
    # Add colorbar
    plt.colorbar(precip_plot, label='Total Precipitation (mm)', extend='max', pad=0.06, shrink = 0.75)
    
    plt.title('Total Precipitation (GPM) from 2024-09-25 to 2024-09-29', pad=20)
    
    # Save the plot
    plt.savefig('D:/Nepal/GPM/GPM_Total_Precipitation.png', dpi=600)
    print("Image saved as 'GPM_Total_Precipitation.png'")
    
    # Show the plot
    plt.show()
    
elif data_ret == 'hour':
    
    # Open the NetCDF file
    file_path = 'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240928030000.65E_17N_91E_40N.nc'
    nc_file = Dataset(file_path, 'r')

    # Total precipitation
    tp_mm = nc_file.variables['GPM_3IMERGHHL_07_precipitation'][:]
    
    # Extract latitude, longitude, and time
    lat = nc_file.variables['lat'][:]
    lon = nc_file.variables['lon'][:]
    time = nc_file.variables['time'][:]  # Time in seconds since 1970-01-01 00:00:00
    
    # Get the units of the time variable
    time_units = nc_file.variables['time'].units
    
    # Convert time from seconds since 1970-01-01 to datetime
    time_converted = num2date(time, units=time_units)
    
    # Close the NetCDF file
    nc_file.close()
    
    # Mask zero values
    tp_time = tp_mm[0, :, :]

    # Create a meshgrid
    lon, lat = np.meshgrid(lon, lat)
    
    # Plotting the combined precipitation data
    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Add other features
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.OCEAN)
    
    # Plot the data
    levels = np.linspace(10, 50, 5)
    precip_plot = ax.contourf(lon, lat, tp_time, cmap='viridis_r', transform=ccrs.PlateCarree(), levels=levels, extend='max')
    
    # Add contour lines
    contours = ax.contour(lon, lat, tp_time, colors='black', linewidths=0.5, transform=ccrs.PlateCarree(), levels=levels)
    
    # Add latitude and longitude gridlines
    gridlines = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linewidth=0.5)
    
    gridlines.top_labels = gridlines.right_labels = False
    gridlines.bottom_labels = gridlines.left_labels = True
    
    gridlines.xlocator = ticker.MultipleLocator(7)  # For longitude
    gridlines.ylocator = ticker.MultipleLocator(7)  # For latitude
    
    # Add colorbar
    plt.colorbar(precip_plot, label='Total Precipitation (mm)', extend='max', pad=0.01, shrink = 0.75)
    
    plt.title('Precipitation (GPM) on 2024-09-28 03:00 UTC', pad=5)
    
    # Save the plot
    plt.savefig('D:/Nepal/GPM/GPM_Precipitation_2024_09_28_03_00_UTC.png', dpi=600)
    print("Image saved as 'GPM_Precipitation_2024_09_28_03_00_UTC.png'")
    
    # Show the plot
    plt.show()
    
elif data_ret == 'period':
    
    # List of NetCDF files
    '''
    files = ['D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240929210000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240929213000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240929220000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240929223000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240929230000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240929233000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240930000000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240930003000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240930010000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240930013000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240930020000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240930023000.65E_17N_91E_40N.nc']
    '''
    files = ['D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240925000000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240925003000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240925010000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240925013000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240925020000.65E_17N_91E_40N.nc',
             'D:/Nepal/GPM/NC/g4.subsetted.GPM_3IMERGHHL_07_precipitation.20240925023000.65E_17N_91E_40N.nc']
    
    # Initialize arrays
    total_tp_sum = None
    lat, lon, time_converted = None, None, None
    
    # Loop through each NetCDF file
    for file_path in files:
        # Open the NetCDF file
        nc_file = Dataset(file_path, 'r')
        
        # Total precipitation
        tp_mm = nc_file.variables['GPM_3IMERGHHL_07_precipitation'][:]
        
        # Extract latitude, longitude, and time
        lat = nc_file.variables['lat'][:]
        lon = nc_file.variables['lon'][:]
        time = nc_file.variables['time'][:]  # Time in seconds since 1970-01-01 00:00:00
        
        # Get the units of the time variable
        time_units = nc_file.variables['time'].units
        
        # Convert time from seconds since 1970-01-01 to datetime
        time_converted = num2date(time, units=time_units)
        
        # Accumulate the precipitation data
        if total_tp_sum is None:
            total_tp_sum = np.sum(tp_mm, axis=0)
        else:
            total_tp_sum += np.sum(tp_mm, axis=0)
        
        # Close the NetCDF file
        nc_file.close()
    
    # Create a meshgrid
    lon, lat = np.meshgrid(lon, lat)
    
    # Plotting the combined precipitation data
    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Add other features
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.OCEAN)
    
    # Plot the data
    #levels = np.linspace(3, 90, 10)
    levels = [10, 30, 50, 70, 90, 110, 130]
    #levels = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]
    precip_plot = ax.contourf(lon, lat, total_tp_sum, cmap='viridis_r', transform=ccrs.PlateCarree(), levels=levels, extend='max')
    
    # Add contour lines
    contours = ax.contour(lon, lat, total_tp_sum, colors='black', linewidths=0.1, transform=ccrs.PlateCarree(), levels=levels)
    
    # Add latitude and longitude gridlines
    gridlines = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linewidth=0.5)
    
    gridlines.top_labels = gridlines.right_labels = False
    gridlines.bottom_labels = gridlines.left_labels = True
    
    gridlines.xlocator = ticker.MultipleLocator(7)  # For longitude
    gridlines.ylocator = ticker.MultipleLocator(7)  # For latitude
    
    # Add colorbar
    cbar = plt.colorbar(precip_plot, label='Total Precipitation (mm)', extend='max', pad=0.01, shrink = 0.77)
    
    cbar.set_ticks([10, 30, 50, 70, 90, 110, 130])
    
    plt.title('Total Precipitation (GPM) on 2024-09-25 00:00 UTC - 03:00 UTC', pad=5)
    
    # Save the plot
    plt.savefig('D:/Nepal/GPM/GPM_Precipitation_2024_09_25_00to03_UTC.png', dpi=600)
    print("Image saved as 'GPM_Precipitation_2024_09_25_00to03_UTC.png'")
    
    # Show the plot
    plt.show()
        
    
else:
    print('Invalid Selection!')