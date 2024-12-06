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
dataset = xr.open_dataset('D:/Nepal/RWB/27e3f479ade90a0c78065acc15e8b277.nc', decode_times = False)

# Check for variables and dimentions
print(dataset)

# Enter date and time (Format: YYYY, MM, DD, HH, MM, SS) [omit zeros in the begining]
date_time = datetime.datetime(2024, 9, 29, 0, 0, 0, tzinfo=datetime.timezone.utc)

# Format the datetime
date_time_f = date_time.strftime('%Y-%m-%d %H:%M')

# Format for date
date_f = date_time.strftime('%Y_%m_%d')

# In seconds since 1970-01-01
time_step = int(date_time.timestamp())
print(time_step)

# Pressure levels
pressure_levels = [300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000]

pressure_level = 200

# Dataset Selection (Specific Humidity, U Wind, V Wind)
pv = dataset['pv'].sel(valid_time = time_step, pressure_level = pressure_level)    # Specific Humidity at different pressure levels

pvu = pv * 10**6

print('Selecting Dataset...')

# Dataset Selection (Specific Humidity, U Wind, V Wind)
spec_hum = {level: dataset['q'].sel(valid_time = time_step, pressure_level = level) for level in pressure_levels}     # Specific Humidity at different pressure levels

wind_u = {level: dataset['u'].sel(valid_time = time_step, pressure_level = level) for level in pressure_levels}       # Wind in East direction at different pressure levels

wind_v = {level: dataset['v'].sel(valid_time = time_step, pressure_level = level) for level in pressure_levels}       # Wind in North direction at different pressure levels

print('Done!')
print('Averaging Specific Humidity...')

# Number of levels for averaging
num_levels = len(pressure_levels) - 1

# Specific humidity averages for each level
spec_hum_levels = {}
for i in range(num_levels):
    spec_hum_levels[f'level_{i + 1}'] = (spec_hum[pressure_levels[i]] + spec_hum[pressure_levels[i + 1]]) / 2

print('Done!')
print('Averaging Wind Velocities...')

# Wind averages for each level
wind_u_levels = {}
wind_v_levels = {}
for i in range(num_levels):
    wind_u_levels[f'level_{i + 1}'] = (wind_u[pressure_levels[i]] + wind_u[pressure_levels[i + 1]]) / 2
    wind_v_levels[f'level_{i + 1}'] = (wind_v[pressure_levels[i]] + wind_v[pressure_levels[i + 1]]) / 2

print('Done!')
print('Multiplying...')

# Products of specific humidity and wind components
qu_levels = {}
qv_levels = {}
for i in range(num_levels):
    qu_levels[f'level_{i + 1}'] = spec_hum_levels[f'level_{i + 1}'] * wind_u_levels[f'level_{i + 1}']
    qv_levels[f'level_{i + 1}'] = spec_hum_levels[f'level_{i + 1}'] * wind_v_levels[f'level_{i + 1}']

print('Done!')
print('Processing Data...')

# Pressure differences
pressure_diffs = [(pressure_levels[i + 1] - pressure_levels[i]) * 100 for i in range(num_levels)]

g = 9.8  # Acceleration due to gravity (m/s**2)

# IVT Calculation
IVT_u = sum(qu_levels[f'level_{i + 1}'] * pressure_diffs[i] for i in range(num_levels)) / g  # IVT in East direction
IVT_v = sum(qv_levels[f'level_{i + 1}'] * pressure_diffs[i] for i in range(num_levels)) / g  # IVT in North direction

IVT = np.sqrt(IVT_u**2 + IVT_v**2)  # Magnitude of IVT

print('Done!')
print('Plotting...')

# Plotting IVT
fig = plt.figure(figsize=(12, 8))

ax = plt.axes(projection=ccrs.PlateCarree())

# For IVT
levels = np.linspace(200,1100,10)
IVT_plot = ax.contourf(dataset['longitude'], dataset['latitude'], IVT, cmap='OrRd', transform=ccrs.PlateCarree(), levels=levels, extend = 'max')

# Reducing the density
step = 15
quiver = ax.quiver(dataset['longitude'][::step], dataset['latitude'][::step], IVT_u[::step, ::step], IVT_v[::step, ::step], transform=ccrs.PlateCarree(), scale=30000)
ax.quiverkey(quiver, X=0.05, Y=1.02, U=500, label='500 m/s', labelpos='E', coordinates='axes', fontproperties={'size': 10})

# Adding contour lines
#contours = ax.contour(dataset['longitude'], dataset['latitude'], IVT, levels=levels, colors='black', linewidths=0.5, transform=ccrs.PlateCarree())
level =[2]
contours = ax.contour(dataset['longitude'], dataset['latitude'], pvu, levels=level, transform=ccrs.PlateCarree(), colors='black', linewidths=1)
ax.clabel(contours, inline=True, fontsize=8, fmt='%1.1f')

# Additional details
ax.coastlines(resolution='10m', linewidths=0.3)
ax.add_feature(cfeature.BORDERS, linewidths=0.2)
#ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.OCEAN)

# Add latitude and longitude gridlines
gridlines = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linewidth=0.5)

gridlines.top_labels = gridlines.right_labels = False
gridlines.bottom_labels = gridlines.left_labels = True

# Set locators for gridlines every 10 degrees
gridlines.xlocator = ticker.MultipleLocator(15)  # For longitude
gridlines.ylocator = ticker.MultipleLocator(15)  # For latitude

# Adding color bar
cbar = plt.colorbar(IVT_plot, ax=ax, orientation='vertical', shrink=0.6, extend = 'max', pad = 0.01)
cbar.set_label('Integrated Vertical Transport (IVT) (kg/ms)')

# Manually set the color bar limits
#cbar.set_ticks([400, 500, 600, 700, 800, 900, 1000, 1100])

print('Done!')
print('Rossby Wave Plot:')    

plt.title(f'Wind, PV and IVT at {pressure_level} hpa on {date_time_f} UTC', pad = 20)

plt.savefig(f'D:/Nepal/RWB/RWB_{pressure_level}_{date_f}.png', dpi = 600)
print(f"Image saved as 'RWB_{pressure_level}_{date_f}.png")

plt.show()