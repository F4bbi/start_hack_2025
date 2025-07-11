import os
import rasterio
import pandas as pd
import numpy as np
from affine import Affine
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.widgets import Slider

def read_tfw(tfw_file):
    """Legge i parametri di trasformazione da un file TFW."""
    with open(tfw_file, 'r') as f:
        values = [float(line.strip()) for line in f.readlines()]
    
    # Creazione della trasformazione affine
    transform = Affine(values[0], values[1], values[4], 
                       values[2], values[3], values[5])
    
    return transform

def extract_climate_data(tiff_file, tfw_file=None):
    """Estrae i dati di densità di popolazione da un file TIFF usando i parametri di un file TFW o direttamente dal TIFF."""

    with rasterio.open(tiff_file) as src:
        # Se il file TFW esiste, leggiamo la trasformazione da lì, altrimenti usiamo quella del TIFF
        transform = read_tfw(tfw_file) if tfw_file and os.path.exists(tfw_file) else src.transform

        # Leggi i dati raster
        data = src.read(1)  # Prima banda (densità di popolazione)

        # Verifica se c'è un valore NoData
        nodata_value = src.nodata

        # Ottieni la dimensione dell'immagine
        rows, cols = np.indices(data.shape)

        # Applica la trasformazione per ottenere le coordinate reali
        xs, ys = rasterio.transform.xy(transform, rows, cols)

        # Creazione del DataFrame
        df = pd.DataFrame({
            'lon': np.array(xs).flatten(),
            'lat': np.array(ys).flatten(),
            'value': data.flatten()
        })

        # Se c'è un valore NoData, rimuoviamo le righe corrispondenti
        if nodata_value is not None:
            df = df[df['value'] != nodata_value]

        return df

def process_climate_data(input_folder, output_folder):
    """Elabora tutti i file di densità di popolazione e salva i CSV in cartelle per anno."""

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for year in range(2010, 2025):
        tiff_file = os.path.join(input_folder, f"{year}R.tif")
        tfw_file = None

        if os.path.exists(tiff_file):
            print(f"Elaborazione: {tiff_file}")

            df = extract_climate_data(tiff_file, tfw_file)

            # Salva il CSV
            csv_path = os.path.join(output_folder, f"{year}.csv")
            df.to_csv(csv_path, index=False)
            print(f"Salvato: {csv_path}")

def plot_climate():
    # Define years and file paths
    years = list(range(2011, 2025))  # From 2011 to 2023
    file_paths = {year: f"data/climate_precipitation/{year}.csv" for year in years}
    
    # Load initial data
    year_init = 2011
    df = pd.read_csv(file_paths[year_init])

    # Create figure and axis
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Add map features
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=":")
    ax.add_feature(cfeature.LAND, edgecolor="black")
    ax.add_feature(cfeature.OCEAN)

    # Plot initial precipitation data
    scatter = ax.scatter(
        df["lon"], df["lat"], c=df["value"], cmap="viridis", s=50, transform=ccrs.PlateCarree()
    )

    # Add colorbar
    cbar = plt.colorbar(scatter, orientation="horizontal", pad=0.05)
    cbar.set_label("Precipitation (mm)")

    # Set title and labels
    ax.set_title(f"Precipitation Data ({year_init})")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Create slider axis and widget
    ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])
    slider = Slider(ax_slider, "Year", years[0], years[-1], valinit=year_init, valstep=1)

    # Update function
    def update(val):
        year = int(slider.val)  # Get the selected year
        df = pd.read_csv(file_paths[year])  # Load new data
        scatter.set_offsets(df[['lon', 'lat']].values)  # Update coordinates
        scatter.set_array(df["value"].values)  # Update colors
        ax.set_title(f"Precipitation Data ({year})")  # Update title
        fig.canvas.draw_idle()

    # Connect slider to update function
    slider.on_changed(update)

    # Show the plot
    plt.show()

input_folder = output_folder = "data/climate_precipitation"

process_climate_data(input_folder, output_folder)
plot_climate()