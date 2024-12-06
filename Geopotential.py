# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 12:41:00 2024

@author: Dell
"""

# Developed by:
    # Adnan Kaisar Khan & Dr. Munir Ahmad Nayak
    # National Institute of Technology Srinagar
    
# Please read the instructions before using this script:
    # - IMPORTANT - Change the 'dataset' path to the netcdf file location.
    # - IMPORTANT - Insert date and time in 'date_time' in YYYY-MM-DD HH:MM:SS format according to the file name.
    # - For more information check the README file.
    # - Data downloaded from: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-pressure-levels?tab=download
    # - Check Status of request from: https://cds.climate.copernicus.eu/requests?tab=all

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import datetime
import matplotlib.ticker as ticker

# Opening netcdf file
dataset = xr.open_dataset('D:/Nepal/Geopotential/d57e8a062799268a5ee7042392885b79.nc', decode_times = False)

# Check for variables and dimentions
print(dataset)

# Enter date and time (Format: YYYY, MM, DD, HH, MM, SS) [omit zeros in the begining of month and day]
date_time = datetime.datetime(2024, 9, 30, 0, 0, 0, tzinfo=datetime.timezone.utc)

# Format the datetime
date_time_f = date_time.strftime('%Y-%m-%d %H:%M')

# Format for date
date_f = date_time.strftime('%Y_%m_%d_%H_%M')

# In seconds since 1970-01-01
time_step = int(date_time.timestamp())
print(time_step)

# Pressure levels
#pressure_levels = [1, 2, 3, 5, 7, 10, 20, 30, 50, 70, 100, 125, 150, 175, 200, 225, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000]

print('Selecting Dataset...')

pressure_level=300

# Dataset Selection (Specific Humidity, U Wind, V Wind)
geop = dataset['z'].sel(valid_time = time_step, pressure_level = pressure_level)    # Specific Humidity at different pressure levels

geop_m = geop / 9.80665

print('Done!')
print('Plotting...')

# Plotting IVT
fig = plt.figure(figsize=(40, 10))

ax = plt.axes(projection=ccrs.PlateCarree())

# For IVT
#levels = np.linspace(3000,3200,9) # for 700hpa

#levels = np.linspace(5600,5950,15) # for 500hpa

levels = np.linspace(8900,9800,18) # for 300hpa

IVT_plot = ax.contourf(dataset['longitude'], dataset['latitude'], geop_m, cmap='coolwarm', transform=ccrs.PlateCarree(), levels=levels, extend = 'both')


# Adding contour lines
#contours = ax.contour(dataset['longitude'], dataset['latitude'], geop_m, levels=levels, colors='black', linewidths=0.5, transform=ccrs.PlateCarree())

# Additional details
ax.coastlines(resolution='10m')
ax.add_feature(cfeature.BORDERS)
#ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.OCEAN)

# Add latitude and longitude gridlines
gridlines = ax.gridlines(draw_labels=True, alpha=0.5, color='black', linewidth=0.5)

# Set extent (bounding box) for the plot: [longitude_min, longitude_max, latitude_min, latitude_max]
ax.set_extent([-180, 180, 0, 60.0000001], crs=ccrs.PlateCarree())

gridlines.xlabel_style = {'size': 20}
gridlines.ylabel_style = {'size': 20}

gridlines.top_labels = gridlines.right_labels = False
gridlines.bottom_labels = gridlines.left_labels = True

# Set locators for gridlines every 10 degrees
gridlines.xlocator = ticker.MultipleLocator(20)  # For longitude
gridlines.ylocator = ticker.MultipleLocator(10)  # For latitude

gridlines.x_inline = False  # Show labels at the first and last longitude gridlines
gridlines.y_inline = False  # Show labels at the first and last latitude gridlines

# Adding color bar
cbar = plt.colorbar(IVT_plot, ax=ax, orientation='horizontal', extend = 'both', pad = 0.06, aspect=50, shrink=1.01)
cbar.set_label('Geopotential Height (m)', fontsize=25)
#cbar.ax.xaxis.label.set_size(30)
cbar.ax.tick_params(labelsize=20)

# Manually set the color bar limits
#cbar.set_ticks([3000, 3025, 3050, 3075, 3100, 3125, 3150, 3175, 3200])      #For 700hpa

#cbar.set_ticks([5600, 5625, 5650, 5675, 5700, 5725, 5750, 5775, 5800, 5825, 5850, 5875, 5900, 5925, 5950])      #For 500hpa

cbar.set_ticks([8900, 8950, 9000, 9050, 9100, 9150, 9200, 9250, 9300, 9350, 9400, 9450, 9500, 9550, 9600, 9650, 9700, 9750, 9800])      #For 300hpa

print('Done!')
print('Geopotential Height Plot:')    

plt.title(f'Geopotential Heights at {pressure_level} hpa on {date_time_f} UTC', pad = 20, fontsize=30)

plt.savefig(f'D:/Nepal/Geopotential/Geopotential_{pressure_level}_{date_f}.png', dpi = 600)
print(f"Image saved as 'IVT_ERA5_{date_f}.png")

plt.show()
