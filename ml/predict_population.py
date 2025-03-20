import pandas as pd
import glob
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import os

# Percorso ai file CSV
path = "../dataset/csv/population_density/*.csv"
files = sorted(glob.glob(path)) 

# Leggiamo e uniamo i dati
df_list = [pd.read_csv(file) for file in files]
print(f"Numero di file letti: {len(df_list)}")
df = pd.concat(df_list, ignore_index=True)

# Creiamo una lista di pixel unici
unique_pixels = df.groupby(["lon", "lat"]).size().reset_index()[["lon", "lat"]]

# Percorso di output
output_path = "ml/population_predictions/"
os.makedirs(output_path, exist_ok=True)

# Anni disponibili nel dataset
available_years = [2010, 2015, 2020, 2025, 2030]
future_year = 2035  # L'anno che vogliamo prevedere

# Dizionario per salvare le previsioni
predictions_dict = []

for _, pixel in unique_pixels.iterrows():
    lon, lat = pixel["lon"], pixel["lat"]
    
    # Selezioniamo i dati del pixel
    df_pixel = df[(df["lon"] == lon) & (df["lat"] == lat)].copy()

    # Creiamo la colonna "year" e impostiamo come indice
    df_pixel["year"] = available_years[:len(df_pixel)]
    df_pixel = df_pixel.sort_values(by="year").set_index("year")

    if len(df_pixel) < 3:  # Abbiamo bisogno almeno di 3 punti per ARIMA
        continue

    train = df_pixel["value"]

    # Modello ARIMA
    try:
        model = ARIMA(train, order=(2,1,0))  # ARIMA più semplice per pochi dati
        model_fit = model.fit()

        # Previsione per il 2025
        forecast = model_fit.forecast(steps=1)

        # Se la previsione è zero o fallisce, usa la media storica
        predicted_value = forecast.iloc[0] if forecast.iloc[0] != 0.0 else df_pixel["value"].mean()

    except Exception as e:
        print(f"Errore per il pixel ({lon}, {lat}): {e}")
        predicted_value = df_pixel["value"].mean()

    predictions_dict.append({
        "lon": lon,
        "lat": lat,
        "value": predicted_value
    })

# Salviamo il file CSV con le previsioni per il 2025
df_pred = pd.DataFrame(predictions_dict)
df_pred.to_csv(f"{output_path}2035.csv", index=False)

print("Previsione per il 2035 completata e salvata!")