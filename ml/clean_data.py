# 16: Barren
# 10: Grasslands
# 7: Open Shurblands
# 13: Urban and ...

import pandas as pd
import glob
import os
import numpy as np

# Percorso ai file CSV
input_path = "../dataset/csv/land_cover/*.csv"
output_path = "../dataset/csv/land_cover_corrected/"
os.makedirs(output_path, exist_ok=True)

# Valori ammessi per l'arrotondamento
valid_values = np.array([7, 10, 13, 16])

# Funzione per arrotondare al valore più vicino tra quelli ammessi
def round_to_nearest(value):
    if value in valid_values:
        return value
    return valid_values[np.abs(valid_values - value).argmin()]

# Leggiamo e modifichiamo i file
files = sorted(glob.glob(input_path))
for file in files:
    df = pd.read_csv(file)

    # Controlla se la colonna 'value' esiste
    if "value" in df.columns:
        df["value"] = df["value"].apply(round_to_nearest)

        # Salva il file corretto
        output_file = os.path.join(output_path, os.path.basename(file))
        df.to_csv(output_file, index=False)
        print(f"File salvato: {output_file}")
    else:
        print(f"Attenzione: colonna 'value' non trovata in {file}")

print("Correzione completata!")
