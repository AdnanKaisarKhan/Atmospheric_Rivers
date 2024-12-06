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
import datetime
import matplotlib.ticker as ticker

# Opening netcdf file
#dataset = xr.open_dataset('D:/Nepal/Vorticity/af197a4d6308590e51dd55ce7248547c.nc', decode_times = False)
dataset = xr.open_dataset('D:/Nepal/RWB/27e3f479ade90a0c78065acc15e8b277.nc', decode_times = False)

# Check for variables and dimentions
print(dataset)

# Enter date and time (Format: YYYY, MM, DD, HH, MM, SS) [omit zeros in the begining of month and day]
date_time = datetime.datetime(2024, 9, 29, 0, 0, 0, tzinfo=datetime.timezone.utc)

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

pressure_level = 200

# Dataset Selection (Specific Humidity, U Wind, V Wind)
wind_v = dataset['v'].sel(valid_time = time_step, pressure_level = pressure_level)    # Specific Humidity at different pressure levels

print('Done!')
print('Plotting...')

# Create a meshgrid
#lon, lat = np.meshgrid(lon, lat)

plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

# Add other features
ax.coastlines(resolution = '10m', linewidths=0.3)
ax.add_feature(cfeature.BORDERS, linewidths=0.3)
ax.add_feature(cfeature.OCEAN)

# Plot the data
levels = [-25, -20, -15, -10, -5, 5, 10, 15, 20, 25]
#levels = [-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,3]
Temp_plot = ax.contourf(dataset['longitude'], dataset['latitude'], wind_v, cmap='bwr_r', transform=ccrs.PlateCarree(), levels=levels, extend = 'both')

# Add contour lines
#contours = ax.contour(dataset['longitude'], dataset['latitude'], wind_v, levels=levels, colors='black', linewidths=0.2, alpha=0.5, transform=ccrs.PlateCarree())

# Add latitude and longitude gridlines
gridlines = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linewidth=0.5)

gridlines.xlocator = ticker.MultipleLocator(15)  # For longitude
gridlines.ylocator = ticker.MultipleLocator(15)  # For latitude

# Add colorbar
plt.colorbar(Temp_plot, label='Poleward Wind (v)', extend='both', pad=0.06, orientation='horizontal')

plt.title(f'Poleward Wind at {pressure_level} hpa on {date_time_f} UTC', pad = 20)

plt.savefig(f'D:/Nepal/Wind/Plot_Wind_v_{pressure_level}hpa_{date_f}.png', dpi = 600)
print(f"Image saved as 'Plot_Wind_v_{pressure_level}hpa_{date_f}.png")

plt.show()
