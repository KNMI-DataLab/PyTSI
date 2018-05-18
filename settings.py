# DESCRIPTION: sets the global variables

# data
main_data = '/nobackup/users/mos/poster_data'

# variables
# aerosol correction
initial_adjustment_factor_limit = 0.5
st_dev_limit = 0.09
remainder_st_dev_limit = 0.05
sun_sky_cover_limit = 0.3
horizon_sky_cover_limit = 0.2
remainder_limit = 0.2
st_dev_width = 11
smoothing_width = 5

# colors
max_color_value = 256
blue = (0, 0, 255)
gray = (150, 150, 150)
white = (255, 255, 255)
black = (0, 0, 0)

# mask
mask_value = -99

# sun position
minimum_altitude = 10

# GLCM
dx = 1
dy = 1
grey_levels = 16

# thresholds
# fixed
fixed_sunny_threshold = 0.795
fixed_thin_threshold = 0.9

# hybrid algorithm
# setups: 1) devThr: 0.065, fixThr: 0.20
#         2) devThr: 0.03 , fixThr: 0.20
#         2) devThr: 0.03 , fixThr: 0.25
deviation_threshold = 0.065  # original was 0.03, 'high:0.065'
fixed_threshold = 0.20  # original was 0.250, 'high:0.20'
nbins_hybrid = 100

# core functionality
use_postprocessing = True
use_statistical_analysis = True

# plotting
plot_sky_cover_comparison = False
plot_correction_result = False
use_project_3d = False
