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

def extract_precipitation_data(tiff_file, tfw_file):
    """Estrae i dati di precipitazione da un file TIFF usando i parametri di un file TFW."""

    transform = read_tfw(tfw_file)
    print(transform)

    with rasterio.open(tiff_file) as src:
        # Leggi i dati raster
        data = src.read(1)  # Prima banda (precipitazioni)

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

def process_all_tiff_files(input_folder, output_folder):
    """Elabora tutti i file TIFF nella cartella e salva i CSV nella cartella di output."""

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for year in range(2010, 2024):  # Da 2010 a 2023
        tiff_file = os.path.join(input_folder, f"{year}LCT.tif")
        tfw_file = os.path.join(input_folder, f"{year}LCT.tfw")

        if os.path.exists(tiff_file) and os.path.exists(tfw_file):
            print(f"Elaborazione: {tiff_file}")

            df = extract_precipitation_data(tiff_file, tfw_file)

            # Salva il CSV
            csv_path = os.path.join(output_folder, f"{year}.csv")
            df.to_csv(csv_path, index=False)
            print(f"Salvato: {csv_path}")

# Imposta le cartelle
input_folder = "data/land_cover"  # Sostituisci con il nome della cartella dei dati
output_folder = "output"

# Esegui il processo
process_all_tiff_files(input_folder, output_folder)
