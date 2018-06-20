# DESCRIPTION: sets the global variables
"""
Set the global variables for:

* Directories
* Aerosol corrections
* Colors
* Masking
* Image segments
* Sun features
* GLCM calculations
* Thresholding
* Plotting
* Toggling functions
"""
import sys
import files_folders

# import the path
sys.path.append('./plotting')

# data
# project folder
project_folder = '/nobackup/users/mos/'
results_folder = project_folder + 'results/'

# main data
# main_data = project_folder + 'data/TSI/DBASE/201606/'
main_data = project_folder + 'data/SWIM/swimseg/'
# main_data = '/data/mobotix/bbc.knmi.nl/'
# main_data = 'data/mobotix/development_images/subfolder/'
# main_data = project_folder+'data/mobotix/bbc.knmi.nl/MEMBERS/knmi/datatransfer/mobotix/vectrontest/2018/05/11/'

# data type
tsi_str = 'TSI'
seg_str = 'swimseg'
cat_str = 'swimcat'
mob_str = 'mobotix'

if main_data.find(tsi_str, 0, len(main_data)) != -1:
    data_type = tsi_str
elif main_data.find(seg_str, 0, len(main_data)) != -1:
    data_type = seg_str
elif main_data.find(cat_str, 0, len(main_data)) != -1:
    data_type = cat_str
elif main_data.find(mob_str, 0, len(main_data)) != -1:
    data_type = mob_str
else:
    raise Exception('Data type not found in string: ' + str(main_data))

output_folder = files_folders.set_output_folder()

# output
output_data = project_folder + 'cloud_detection/cloudDetection/data.csv'
output_data_copy = project_folder + 'cloud_detection/cloudDetection/data' + data_type + '.csv'

# csv delimiter
delimiter = ','

# image extensions
if data_type == 'TSI':
    # the '0' is added to exclude some files in the directory
    properties_extension = '0.properties.gz'
    jpg_extension = '0.jpg'
    png_extension = '0.png'
else:
    properties_extension = None
    jpg_extension = '.jpg'
    png_extension = '.png'

# coordinates
camera_latitude = '51.968243'
camera_longitude = '4.927675'
camera_elevation = 1

# looping
skip_loops = 120 # every 'x' files are used in stead of all files

# aerosol correction
initial_adjustment_factor_limit = 0.5
st_dev_limit = 0.09
remainder_st_dev_limit = 0.05
sun_sky_cover_limit = 0.3
horizon_sky_cover_limit = 0.2
remainder_limit = 0.2
st_dev_width = 11
smoothing_width = 5

# resolutions of the system are set using get_resolution, initialize with None
x = None
y = None
n_colors = None

# colors
max_color_value = 256
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
green = (0, 255, 0)
gray = (150, 150, 150)
white = (255, 255, 255)
black = (0, 0, 0)

# mask
mask_value = -99

# regions
radius_sun_circle = 40
radius_inner_circle = 80
radius_circle = 130
radius_mirror = 140
outline_thickness = 3
band_thickness = 35
width_horizon_area_degrees = 50
r_inner = 40
r_outer = 140
radius_mobotix_circle = 850

# sun position
minimum_altitude = 10

# GLCM
dx = 1
dy = 1
grey_levels = 256

# thresholds
# fixed
# TSI ######################
fixed_sunny_threshold = 0.80  # working: 0.795
fixed_thin_threshold = 0.9  # working: 0.9
# swim #####################
fixed_threshold_swim = 0.64

use_single_threshold = True  # if True: fixed thin/opaque threshold == fixed thin/clear sky threshold
use_hybrid_SEG = False  # if True: use hybrid thresholding for SEG database (not recommended)

# hybrid
# setups: 1) devThr: 0.065, fixThr: 0.20
#         2) devThr: 0.03 , fixThr: 0.20
#         2) devThr: 0.03 , fixThr: 0.25
nbins_hybrid = 100
if data_type == tsi_str or data_type == seg_str or data_type == cat_str:
    deviation_threshold = 0.03  # original was 0.03, 'working:0.065'
    fixed_threshold = 0.25  # original was 0.250, 'working:0.20'
elif data_type == mob_str:
    deviation_threshold = 0.08
    fixed_threshold = 0.10

# machine learning
use_knn = False
use_kmeans = True

# core functionality
use_processing_loop = True
use_postprocessing = False
use_statistical_analysis = False
use_machine_learning = False
crop_mobotix_images = True

# plotting
plot_sky_cover_comparison = False
plot_sky_cover_time_series = False
plot_correction_result = False
plot_overview = False
plot_poster_images = False
use_project_3d = False
plot_comparion_scatter = False
plot_difference_histogram = False
