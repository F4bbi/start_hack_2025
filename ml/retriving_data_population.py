import os
import rasterio
import pandas as pd
import numpy as np
from affine import Affine

def read_tfw(tfw_file):
    """Legge i parametri di trasformazione da un file TFW."""
    with open(tfw_file, 'r') as f:
        values = [float(line.strip()) for line in f.readlines()]
    
    # Creazione della trasformazione affine
    transform = Affine(values[0], values[1], values[4], 
                       values[2], values[3], values[5])
    
    return transform

def extract_population_data(tiff_file, tfw_file=None):
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
            'population_density': data.flatten()
        })

        # Se c'è un valore NoData, rimuoviamo le righe corrispondenti
        if nodata_value is not None:
            df = df[df['population_density'] != nodata_value]

        return df

def process_population_data(input_folder, output_folder):
    """Elabora tutti i file di densità di popolazione e salva i CSV in cartelle per anno."""

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for year in [2010, 2015, 2020]:
        for resolution in ["", "_1km"]:
            if resolution == "":
                tiff_file = os.path.join(input_folder, f"Assaba_Pop_{year}.tif")
                tfw_file = os.path.join(input_folder, f"Assaba_Pop_{year}.tfw")
            else:
                tiff_file = os.path.join(input_folder, f"mrt_pd_{year}{resolution}.tif")
                tfw_file = None  # Nessun TFW per i file _1km

            if os.path.exists(tiff_file):
                print(f"Elaborazione: {tiff_file}")

                df = extract_population_data(tiff_file, tfw_file)

                # Salva il CSV
                csv_path = os.path.join(output_folder, f"{year}{resolution}_population.csv")
                df.to_csv(csv_path, index=False)
                print(f"Salvato: {csv_path}")

# Imposta le cartelle
input_folder = "dati_popolazione"  # Sostituisci con il nome della cartella dei dati
output_folder = "output_population"

# Esegui il processo
process_population_data(input_folder, output_folder)
