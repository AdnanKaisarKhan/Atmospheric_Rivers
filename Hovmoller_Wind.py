

# Developed by:
    # Adnan Kaisar Khan & Dr. Munir Ahmad Nayak
    # National Institute of Technology Srinagar
    
# Please read the instructions before using this script:
    # - IMPORTANT - Change the 'dataset' path to the netcdf file location.
    # - IMPORTANT - Change the 'pressure_level' as required.
    # - IMPORTANT - Change the plot extent according to your dataset.
    # - Also check 'geop' variable before proceeding.
    # - Change 'levels' according to the data.
    # - For more information check the README file.
    # - Data downloaded from: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-pressure-levels?tab=download
    # - Check Status of request from: https://cds.climate.copernicus.eu/requests?tab=all

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
 
# Load dataset
dataset = xr.open_dataset('D:/Nepal/Wind/ff71b8341ab807bf8a07413a798c122a.nc', decode_times=False)

print(dataset)

# Get time data
time_seconds = dataset['valid_time'].values.astype('timedelta64[s]')
time_nanoseconds = time_seconds.astype('timedelta64[ns]')

time = xr.DataArray(np.datetime64('1970-01-01') + time_nanoseconds)

time_str = time.dt.strftime('%d-%b')

# Get unique dates in sorted order
dates = sorted(set(time_str.values))

# Choose the pressure level
pressure_level = 300

# Data selection
geop = dataset['v'].sel(pressure_level=pressure_level, latitude=slice(60, 30))
longitude = dataset['longitude']

geop_mean = dataset['v'].sel(pressure_level=pressure_level, valid_time=slice(338688000, 1727305200), longitude=slice(0, 140), latitude=slice(60, 30))

print('Mean value of Wind is:', geop_mean)

gpf = geop_mean/1080

print('Mean value of Wind 2 is:', gpf)

print(geop.attrs)

# Average over latitude
geop_avg_lat = geop.mean(dim='latitude')

# Convert geopotential to meters
geop_m = geop_avg_lat

print('Plotting Data...')

# Set up the figure
plt.figure(figsize=(15, 22))

# Bottom plot for Hovmöller Diagram
ax = plt.axes()

# Plotting the Hovmöller Diagram
levels = [-25, -20, -15, -10, -5, 0, 5, 10, 15, 20, 25]
cf = ax.contourf(longitude, time, geop_m, cmap='RdBu_r', extend='both', levels=levels)
cs = ax.contour(longitude, time, geop_m, colors='k', linewidths=0.5, alpha=0.5, extend='both', levels=levels)

# Create color bar
cbar = plt.colorbar(cf, orientation='horizontal', pad=0.05, aspect=40, shrink=1.02, extend='both')
cbar.set_label('"v" wind anomaly (m/s)', fontsize=25, labelpad=10)
cbar.ax.tick_params(labelsize=15)

# Set x labels
x_tick_labels = ['0°', '20°E', '40°E', '60°E', '80°E', '100°E', '120°E', '140°E']
ax.set_xticks([0, 20, 40, 60, 80, 100, 120, 140])
ax.set_xticklabels(x_tick_labels, fontsize=15)
for label in ax.get_xticklabels():
    label.set_y(label.get_position()[1] - 0.006)
ax.set_yticklabels(dates, fontsize=15)
ax.grid(linestyle='dotted', linewidth=2)
ax.set_xlabel('Longitude', fontsize=25)
ax.set_ylabel('Date', fontsize=25)

# Set the title for the entire plot
plt.title(f'ERA5 "v" Wind at {pressure_level} hPa', fontsize=25, pad=15)

# Save the plot
plt.savefig(f'D:/Nepal/Wind/Wind_N10_{pressure_level}.png', dpi=600)
print(f"Image saved as 'Wind_N10_{pressure_level}.png'")

plt.show()
