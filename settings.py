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
* And more
"""
import sys
import files_folders
import warnings

# import the path
sys.path.append('./plotting')

# data
# project folder
project_folder = '/nobackup/users/mos/'
results_folder = project_folder + 'results/'

# main data
main_data = project_folder + 'data/TSI/DBASE/201606/20160601_tsi-cabauw_realtime/'
# main_data = '/net/baltink/nobackup/users/baltink/DATABASE/TSI/'
# main_data = project_folder + 'data/SWIM/swimseg/'
# main_data = '/data/mobotix/bbc.knmi.nl/'
# main_data = 'data/mobotix/development_images/subfolder/'
# main_data = project_folder+'data/mobotix/bbc.knmi.nl/MEMBERS/knmi/datatransfer/mobotix/vectrontest/2018/05/same_alignment/'

# external data sources
tsi_database = '/net/baltink/nobackup/users/baltink/DATABASE/TSI/'

# temporary folder(s)
tmp = 'tmp/'

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

if data_type == cat_str:
    # SWIM folders
    swim_dirs = (main_data + 'A-sky/images/',
                 # main_data + 'B-pattern/images/',
                 # main_data + 'C-thick-dark/images/',
                 main_data + 'D-thick-white/images/')
                 # main_data + 'E-veil/images/')

output_folder = files_folders.set_output_folder()

# output
output_data = project_folder + 'cloud_detection/cloudDetection/output_data/data.csv'
output_data_copy = project_folder + 'cloud_detection/cloudDetection/output_data/data' + data_type + '.csv'

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

# dates/time
year = '2018'
month = '01'
day = '01'
hour = '12'
minute = '00'

# looping
# every 'x' files are used in stead of all files
# 4 images are taken every minute in case of the mobotix file
# that means: 'skip_loops = 120' results in 1 image every half an hour being processed as 4*30=120
skip_loops = 40

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
outline_thickness = 2
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
    deviation_threshold = 0.045  # original was 0.03, 'working:0.065'
    fixed_threshold = 0.20  # original was 0.250, 'working:0.20'
elif data_type == mob_str:
    deviation_threshold = 0.08
    fixed_threshold = 0.10

# machine learning
use_knn = False
use_kmeans = True

# core functionality
use_processing_loop = 1
use_postprocessing = 0
use_statistical_analysis = 0
use_machine_learning = 0
crop_mobotix_images = 0
use_ui = 0

# plotting
plot_sky_cover_comparison = 0
plot_sky_cover_time_series = 0
plot_correction_result = 0
plot_overview = 0
plot_poster_images = 0
use_project_3d = 0
plot_comparison_scatter = 0
plot_difference_histogram = 0

# ignore FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)
