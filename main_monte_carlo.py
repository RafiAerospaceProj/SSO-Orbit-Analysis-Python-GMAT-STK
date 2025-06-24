from generate_gmat_script import generate_gmat_script
from generate_run_stk import generate_run_stk
from run_gmat import run_gmat
import numpy as np
import parse_gmat
import parse_stk
import parse_gmat_raan_report
import plot_output

# Parameters
sma = 7488.6 # Semi-major axis in km
sma_delta = list(range(-60, 61, 30))
inc = 97.49 # Inclination in degrees
inc_delta = np.arange(-0.3, 0.31, 0.1)  # Inclination delta in degrees
raan = 98.545 # Right Ascension of Ascending Node in degrees
boulder = (40.15, -105.2705, 1.6)  # lat, lon, alt (km)
output_path = 'output'  # Directory to save output files

# gmat_data_all = []
# stk_data_all = []
# raan_drift_all = []

# for item in sma_delta:
#     sma = sma + item  # Update semi-major axis for each iteration
#     for item in inc_delta:
#         inc = inc + item    # Update inclination for each iteration
# Generate scripts
gmat_script_path = generate_gmat_script(sma=sma, inc=inc, raan=raan, GS=boulder)
stk_script_path = generate_run_stk(sma=sma, inc=inc, raan=raan, GS=boulder)

# Run GMAT
run_gmat(gmat_script_path)

# parse and plot data
gmat_dict = parse_gmat.parse_gmat(output_path,'ContactLocator1.txt')
stk_dict = parse_stk.parse_stk(output_path, 'access_report.txt')

# Optional: load RAAN list manually or compute from orbit logs
raan_dict = parse_gmat_raan_report.parse_gmat_raan_report(output_path, 'ltan_report.txt')

plot_output.plot_output(gmat_dict, stk_dict, raan_dict)