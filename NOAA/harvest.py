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

def pull(dataset, samples, timestamp, para, level):
    OUTDIR = f"NOAA/data/{timestamp}/{para}"
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)

    t_range = np.linspace(0,samples,samples+1, dtype=int)
    for i in t_range:
        file = f"gfs.t12z.pgrb2.0p25.f{i:03}"
        url = f"https://nomads.ncep.noaa.gov/cgi-bin/filter_{dataset}.pl?dir=%2Fgfs.{timestamp}%2F12%2Fatmos&file={file}&var_{para}=on&{level}=on"
        
        # Wait for 3secs - NOAA compliance
        time.sleep(3)
        response = requests.get(url)
        if response.status_code==200:
            content = response.content
            file_path = f"{OUTDIR}/{para}.{file}"

            with open(file_path, 'wb') as file:
                file.write(content)
        else:
            print("Error connecting to NOAA library.")

def main()
    ds = "gfs_0p25"
    date = 20230928
    p_list = ["GUST", "UGRD", "VGRD"]
    levels = ["all_lev", "lev_10_m_above_ground", "lev_10_m_above_ground"]

    for pid, parameter in tqdm(enumerate(p_list)):
            pull(ds, 0, date, parameter, levels[pid])

if __name__ == "__main__":
    main()