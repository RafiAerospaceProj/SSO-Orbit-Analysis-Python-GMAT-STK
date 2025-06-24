import numpy as np
import os

def parse_gmat_raan_report(filepath, name):
    filename = os.path.join(filepath, name)
    with open(filename, 'r') as f:
        lines = f.readlines()
    # Skip header
    header = lines[0].strip().split()
    idx_elapsed = header.index("Sat1.ElapsedDays")
    idx_raan = header.index("Sat1.RAAN")
    idx_rmag = header.index("Sat1.Earth.RMAG")

    seen_days = set()
    days_list = []
    raan_list = []
    rmag_list = []

    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) <= max(idx_elapsed, idx_raan, idx_rmag):
            continue
        try:
            elapsed = float(parts[idx_elapsed])
            day = int(elapsed)
            if day not in seen_days:
                seen_days.add(day)
                raan = float(parts[idx_raan])
                rmag = float(parts[idx_rmag])
                days_list.append(day)
                raan_list.append(raan)
                rmag_list.append(rmag)
        except ValueError:
            continue

    # Normalize day count to start at 1
    min_day = min(days_list)
    days_array = np.array([d - min_day + 1 for d in days_list])
    raan_array = np.array(raan_list)
    rmag_array = np.array(rmag_list)

    return {'Days': days_array, 'RAAN': raan_array, 'RMAG': rmag_array}
