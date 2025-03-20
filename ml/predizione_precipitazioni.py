import pandas as pd
import glob
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import os

# Percorso ai file CSV
path = "dataset/csv/climate_precipitation/*.csv"
files = sorted(glob.glob(path)) 

# Leggiamo e uniamo i dati
df_list = [pd.read_csv(file) for file in files]
df = pd.concat(df_list, ignore_index=True)

# Creiamo una lista di pixel unici
unique_pixels = df.groupby(["lon", "lat"]).size().reset_index()[["lon", "lat"]]

# Percorso di output
output_path = "ml/climate_predictions/"
os.makedirs(output_path, exist_ok=True)

# Solo l'anno 2028
future_years = [2028]
predictions_dict = {year: [] for year in future_years}

for _, pixel in unique_pixels.iterrows():
    lon, lat = pixel["lon"], pixel["lat"]
    
    # Creiamo una copia indipendente per evitare il warning
    df_pixel = df[(df["lon"] == lon) & (df["lat"] == lat)].copy()

    # Creiamo un indice temporale con frequenza annuale
    df_pixel["year"] = pd.date_range(start="2010", periods=len(df_pixel), freq="YE")

    # Ordiniamo per anno
    df_pixel = df_pixel.sort_values(by="year").reset_index(drop=True)

    if len(df_pixel) < 5:
        continue

    # Selezioniamo solo anno e precipitazione
    train = df_pixel[["year", "precipitation"]].set_index("year")
    train.index.freq = "YE"  # Imposta la frequenza esplicitamente

    # Definizione del modello ARIMA
    try:
        model = ARIMA(train, order=(5,1,0))
        model_fit = model.fit()

        # Previsione per il 2028
        future_date = pd.date_range(start="2028", periods=1, freq="YE")
        forecast = model_fit.forecast(steps=1)

        predictions_dict[2028].append({
            "lon": lon,
            "lat": lat,
            "precipitation": forecast.iloc[0]
        })

    except Exception as e:
        print(f"Errore per il pixel ({lon}, {lat}): {e}")

        # Usa la media delle precipitazioni storiche come previsione
        historical_mean = df_pixel["precipitation"].mean()
        predictions_dict[2028].append({
            "lon": lon,
            "lat": lat,
            "precipitation": historical_mean
        })

# Salviamo il file CSV solo per il 2028
df_pred = pd.DataFrame(predictions_dict[2028])
df_pred.to_csv(f"{output_path}2028.csv", index=False)

print("Previsione per il 2028 completata e salvata!")