from datetime import datetime
from collections import defaultdict
import numpy as np
import os

def parse_stk(filepath, name):
    filename = os.path.join(filepath, name)
    filename = os.path.join(filepath, name)
    intervals = []
    by_day = defaultdict(list)
    days = []
    single_days = []
    first_accesses = []
    drifts  = [0]
    intervals =[]
    duration = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("Start Time"):
                continue
            parts = line.split()
            try:
                start_str = f"{parts[0]} {parts[1]}"
                start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S.%f")
                duration_sec = float(parts[4])
                day = start_dt.day
                time_mn = start_dt.hour*60+start_dt.minute
                by_day[day].append((time_mn, duration_sec))
                days.append(day)
                intervals.append(start_dt)
                duration.append(duration_sec)
            except:
                continue
        sorted_days = sorted(by_day)
        for i, day in enumerate(sorted_days):
            first_accesses.append(min(by_day[day])[0])
            single_days.append(day)
            if i > 0:
                delta_min = (first_accesses[i] - first_accesses[i-1])
                drifts.append(delta_min)
    intervals_array = np.array(intervals)
    duration_array = np.array(duration)  
    days_array = np.array(days)     
    drifts_array = np.array(drifts)
    return {'Days': days_array,'Single Days':single_days, 'Drift': drifts_array, 'Intervals': intervals_array, 'Duration': duration_array}
