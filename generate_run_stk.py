# --- generate_run_stk.py ---
# This script generates and run an STK scenario with a satellite in a specified orbit.
import win32com.client
import os
from datetime import datetime
from agi.stk12.stkobjects import *

def generate_run_stk(sma, inc, raan, GS, scenario_name="SSO_Access_Auto"):
    app = win32com.client.Dispatch("STK12.Application")
    app.Visible = True
    root = app.Personality2

    # Close previous scenario if exists
    try:
        root.CloseScenario()
        existing_sat = scenario.Children.Item("Sat1")
        existing_sat.Unload()
    except:
        pass

    # Create new scenario
    root.NewScenario(scenario_name)
    scenario = root.CurrentScenario
    scenario.SetTimePeriod("1 Jun 2025 00:00:00.000", "3 Jun 2025 00:00:00.000") # Adjust this!
    scenario.Epoch = "1 Jun 2025 00:00:00.000" # Adjust this!

    # Create satellite
    sat = scenario.Children.New(18, "Sat1")  # 18 is eSatellite
    sat.SetPropagatorType(1)  # ePropagatorJ2Perturbation
    prop = sat.Propagator
    prop.InitialState.Representation.AssignClassical(3, sma,0.001,inc,0.0,raan,0.0)
    prop.Propagate()
    LOSsensor = sat.Children.New(20, "LOSsensor")  # 21 is eSensor
    
    # Example: run access report to a fixed Boulder location
    facility = scenario.Children.New(AgESTKObjectType.eFacility, "Boulder")
    facility.Position.AssignGeodetic(GS[0], GS[1], GS[2])  # lat, lon, alt (km)
    # Set minimum elevation angle
    facility.AccessConstraints.AddConstraint(AgEAccessConstraints.eCstrElevationAngle)
    elevConstraint = facility.AccessConstraints.GetActiveConstraint(AgEAccessConstraints.eCstrElevationAngle)
    elevConstraint.EnableMin = True
    elevConstraint.Min = 30  # 30 degrees

    access = facility.GetAccessToObject(sat)
    access.ComputeAccess()

    # Make output folder if it doesn't exist
    output_dir = os.path.join(os.getcwd(), "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    report_file = os.path.join(os.getcwd(), "output", "access_report.txt")

   # Use the correct method - ComputedAccessIntervalTimes() is a method, not a property
    try:
        # Get computed access intervals (note the parentheses - it's a method)
        intervals = access.ComputedAccessIntervalTimes
        
        print(f"Access computation completed. Found {intervals.Count} intervals")
        
        with open(report_file, 'w') as f:
            f.write("STK Access Analysis Report\n")
            f.write("=" * 50 + "\n")
            f.write(f"Satellite: {sat.InstanceName}\n")  # Use InstanceName, not Name
            f.write(f"Facility: {facility.InstanceName}\n")  # Use InstanceName, not Name
            f.write(f"Total Access Intervals: {intervals.Count}\n")
            f.write("-" * 50 + "\n")
            f.write("Start Time\t\t\tStop Time\t\t\tDuration (s)\t\t\tDuration (m)\n")
            f.write("-" * 50 + "\n")
            
            # Iterate through intervals
            for i in range(intervals.Count):
                interval = intervals.GetInterval(i)
                start_time_str = interval[0]
                stop_time_str = interval[1]
                start_time = datetime.strptime(start_time_str, '%d %b %Y %H:%M:%S.%f')  # Adjust format as needed
                stop_time = datetime.strptime(stop_time_str, '%d %b %Y %H:%M:%S.%f')   # Adjust format as needed

                # Calculate the time interval
                time_difference = stop_time - start_time

                # Get the duration in different formats
                duration_seconds = time_difference.total_seconds()
                duration_minutes = duration_seconds / 60
                f.write(f"{start_time}\t{stop_time}\t{duration_seconds}\t{duration_minutes}\n")
            
            if intervals.Count == 0:
                f.write("No access intervals found between satellite and facility.\n")
        
        print(f"Access report successfully written to {report_file}")

    except Exception as e:
        print(f"Error getting access intervals: {e}")