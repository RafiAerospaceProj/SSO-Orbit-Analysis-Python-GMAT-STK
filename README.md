# SSO-Orbit-Analysis-Python-GMAT-STK
Dual-tool orbit analysis with Python, GMAT, and STK — automated RAAN/LTAN drift evaluation for SSO missions. Extracts and compares RAAN drift, LTAN consistency, and daily access durations.
SSO Mission is just one example, the code can be modified to fit any mission.

Need to adjust to user environment: 
    mission parameters
    gmat_path and work_dir, lines 5,6 in run_gmat.py

Known issues:
    The epoch and mission period are modified in generate_run_stk.py for STK, but are hardcoded in the GMAT template.
    GMAT outputs are written to the default GMAT output path instead of the project output path.

## Tools Used
- Python 3.x
- GMAT R2025a (NASA General Mission Analysis Tool)
- STK12 (AGI Systems Tool Kit)
- NumPy, Matplotlib, etc.
