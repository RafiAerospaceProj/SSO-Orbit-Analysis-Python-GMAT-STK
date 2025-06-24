import os
import subprocess

def run_gmat(script_path):
    gmat_path = r'C:\Users\Admin\Rafi\GMAT_R2025a\bin\GmatConsole.exe'  # Adjust this!
    work_dir = r"C:\Users\Admin\OneDrive\Space Project\Python_Material" # Adjust this!
    file_path = os.path.join(work_dir, script_path)
    result = subprocess.run([gmat_path, '--run', file_path,'--exit'])
