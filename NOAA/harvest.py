import os, requests, time
import numpy as np
from tqdm import tqdm

# https://nomads.ncep.noaa.gov/gribfilter.php?ds=gfs_0p25
# https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.20230928%2F12%2Fatmos&file=gfs.t12z.pgrb2.0p25.f000
# &var_ABSV=on (Absolute Vorticity)
# &var_DZDT=on (Vertical Velocity)
# &var_GUST=on (Wind Speed) *
# &var_HGT=on (Geopotential Height)
# &var_LAND=on (Land Cover) *
# &var_PRES=on (Pressure)
# &var_TMP=on (Temperature) *
# &var_UGRD=on (U-Component of Wind) *
# &var_VGRD=on (V-Component of Wind) *
# &all_lev=on (All levels) *

dataset = "gfs_0p25"
date = 20230928
parameter = "UGRD"
levels = "100_m_above_ground"

N = 0
samples = np.linspace(0,N,N+1, dtype=int)

OUTDIR = f"NOAA/data/{date}"
if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

for i in tqdm(samples):
    window = f"{i:03}"
    file = f"gfs.t12z.pgrb2.0p25.f{window}"

    url = f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{dataset}.pl?dir=%2Fgfs.{date}%2F12%2Fatmos&file={file}&var_{parameter}=on&lev_{levels}=on"

    response = requests.get(url)
    if response.status_code==200:
        content = response.content
        file_path = f"{OUTDIR}/{file}"

        with open(file_path, 'wb') as file:
            file.write(content)
        
        time.sleep(3)