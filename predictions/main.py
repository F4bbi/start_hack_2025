import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.widgets import Slider

# for every file in climate_precipitation folder, change name to year.csv and year starts from 2010
def clear_csv(directory: str):
    import os
    import glob

    files = glob.glob('data/' + directory + '/*.csv')
    for f in files:
        os.remove(f)

clear_csv('land_cover')