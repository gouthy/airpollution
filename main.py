from osgeo import gdal 
import urllib.request
url = "https://tgftp.nws.noaa.gov/SL.us008001/ST.opnl/DF.gr2/DC.ndgd/GT.aq/AR.conus/ds.apm25h01_bc.bin"
file_name = "ds.apm25h01_bc.bin"  # Specify the desired file name
try:
    urllib.request.urlretrieve(url, file_name)
    print("File downloaded successfully.")
except Exception as e:
    print("An error occurred while downloading the file:", str(e))

from osgeo import gdal
from osgeo import osr

def reproject_to_wgs84(input_file, output_file):
    dataset = gdal.Open(input_file)
    num_bands = dataset.RasterCount
    geotransform = dataset.GetGeoTransform()
    projection = dataset.GetProjection()
    target_srs = osr.SpatialReference()
    target_srs.ImportFromEPSG(4326) 
    vrt_options = gdal.BuildVRTOptions(resampleAlg='bilinear')
    vrt_dataset = gdal.BuildVRT('/vsimem/reprojected.vrt', dataset, options=vrt_options)
    driver = gdal.GetDriverByName('GTiff')
    output_dataset = driver.Create(output_file, vrt_dataset.RasterXSize, vrt_dataset.RasterYSize, num_bands, gdal.GDT_Float32, options=['COMPRESS=DEFLATE'])
    output_dataset.SetGeoTransform(geotransform)
    output_dataset.SetProjection(target_srs.ExportToWkt())
    for band_num in range(1, num_bands + 1):
        band = vrt_dataset.GetRasterBand(band_num)
        output_band = output_dataset.GetRasterBand(band_num)
        output_band.WriteArray(band.ReadAsArray())
    dataset = None
    vrt_dataset = None
    output_dataset = None
    gdal.Unlink('/vsimem/reprojected.vrt')
    print("Reprojection and COG conversion complete.")

# Specify the input and output file paths
input_file = file_name
output_file = 'output.tif'

# Call the reproject_to_wgs84 function
reproject_to_wgs84(input_file, output_file)
