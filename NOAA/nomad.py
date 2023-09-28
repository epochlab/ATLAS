#!/usr/bin/env python3

# National Weather Service: http://nomads.ncep.noaa.gov

import struct
from osgeo import gdal
import matplotlib.pylab as plt

FILENAME = "gfs.t12z.pgrb2.0p25.f000"
dataset = gdal.Open(FILENAME, gdal.GA_ReadOnly)

print(f"Projection: {dataset.GetProjection()}")
print(f"Driver: {dataset.GetDriver().ShortName}/{dataset.GetDriver().LongName}")
print(f"Size: {dataset.RasterXSize} x {dataset.RasterYSize} x {dataset.RasterCount}")
print(f"Projection: {dataset.GetProjection()}")

geotransform = dataset.GetGeoTransform()
print(f"Origin: ({geotransform[0]}, {geotransform[3]})")
print(f"Pixel Size: ({geotransform[1]}, {geotransform[5]})")

band = dataset.GetRasterBand(1)
print(f"Band Type:{gdal.GetDataTypeName(band.DataType)}")

b_min = band.GetMinimum()
b_max = band.GetMaximum()

(b_min, b_max) = band.ComputeRasterMinMax(True)
print(f"Min: {b_min:.3f}, Max:{b_max:.3f}")

raster = band.ReadAsArray()
plt.imshow(raster)
plt.show()