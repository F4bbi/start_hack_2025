# start_hack_2025

da runnare prima: `create extension postgis_raster;`

il nome del database su grafana e' `postgres`

cose: `raster2pgsql -s 4326 -I -C -M 2010R.tif public.raster_table`

## Website Branch

Per avviare usare `streamlit run app.py`