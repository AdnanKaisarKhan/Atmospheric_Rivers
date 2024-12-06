# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 11:09:25 2024

@author: Dell
"""

import xarray as xr
import datetime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib.ticker as ticker

# Opening netcdf file
dataset = xr.open_dataset('D:/Nepal/Reflectivity/g4.subsetted.OMTO3e_003_RadiativeCloudFraction.20240930.65E_17N_91E_40N.nc', decode_times = False)

# Check for variables and dimentions
print(dataset)

# Enter date and time (Format: YYYY, MM, DD) [omit zeros in the begining]
date_time = datetime.datetime(2024, 9, 30, tzinfo=datetime.timezone.utc)

# Format the date in title
date_title_f = date_time.strftime('%Y-%m-%d')

# Format for date
date_f = date_time.strftime('%Y_%m_%d')

# In seconds since 1970-01-01
time_step = int(date_time.timestamp())
print(time_step)

# Accessing Dataset
Reflectivity = dataset['OMTO3e_003_RadiativeCloudFraction'].sel(time = time_step)

# Plotting Reflectivity
fig = plt.figure(figsize=(11, 11))

ax = plt.axes(projection=ccrs.PlateCarree())

# For Reflectivity
levels = np.linspace(0.1,1,11)
IVT_plot = ax.contourf(dataset['lon'], dataset['lat'], Reflectivity, cmap='gray', transform=ccrs.PlateCarree(), levels=levels)

# Additional details
ax.coastlines(resolution='10m')
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.OCEAN)

# Add latitude and longitude gridlines
gridlines = ax.gridlines(draw_labels=True, alpha=0.5, color='gray', linewidth=0.5)

# Set locators for gridlines every 5 degrees
gridlines.xlocator = ticker.MultipleLocator(5)  # For longitude
gridlines.ylocator = ticker.MultipleLocator(5)  # For latitude

# Adding color bar
cbar = plt.colorbar(IVT_plot, ax=ax, orientation='vertical', shrink=0.7, pad = 0.06)
cbar.set_label('Reflectivity')

# Manually set the color bar limits
#cbar.set_ticks([400, 500, 600, 700, 800, 900, 1000, 1100])

print('Done!')
print('Reflectivity Plot:')    

plt.title(f'Reflectivity on {date_title_f}', pad =30)

plt.savefig(f'D:/Nepal/Reflectivity/Reflectivity_{date_f}.png', dpi = 600)
print(f"Image saved as 'Reflectivity_{date_f}.png")

plt.show()