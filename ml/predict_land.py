import pandas as pd
import glob
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import os

# Percorso ai file CSV
path = "../dataset/csv/land_cover/*.csv"
files = sorted(glob.glob(path)) 

# Leggiamo e uniamo i dati
df_list = [pd.read_csv(file) for file in files]
df = pd.concat(df_list, ignore_index=True)

# Creiamo una lista di pixel unici
unique_pixels = df.groupby(["lon", "lat"]).size().reset_index()[["lon", "lat"]]

# Percorso di output
output_path = "../dataset/csv/land_cover_predictions/"
os.makedirs(output_path, exist_ok=True)

# Previsioni per 5 anni
future_years = [2024, 2025, 2026, 2027, 2028]

# Dizionario per contenere le previsioni per ogni anno
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

    # Selezioniamo solo anno e valore
    train = df_pixel[["year", "value"]].set_index("year")
    train.index.freq = "YE"  # Imposta la frequenza esplicitamente

    # Definizione del modello ARIMA
    try:
        model = ARIMA(train, order=(2,1,0))  # Cambia i parametri se necessario
        model_fit = model.fit()

        # Previsione per i prossimi 5 anni
        future_dates = pd.date_range(start="2024", periods=5, freq="YE")
        forecast = model_fit.forecast(steps=5)

        for i in range(5):
            predictions_dict[future_years[i]].append({
                "lon": lon,
                "lat": lat,
                "year": future_dates[i].year,
                "value": forecast.iloc[i]
            })

    except Exception as e:
        print(f"Errore per il pixel ({lon}, {lat}): {e}")

# Salviamo il file CSV separato per ogni anno
for year in future_years:
    df_pred = pd.DataFrame(predictions_dict[year])
    df_pred.to_csv(f"{output_path}{year}.csv", index=False)

    print(f"Previsioni per il {year} completate e salvate!")

print("Previsioni per tutti gli anni completate e salvate!")
