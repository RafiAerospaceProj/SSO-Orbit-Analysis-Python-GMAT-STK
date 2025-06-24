# --- generate_gmat_script.py ---
# This script generates a GMAT script based on provided orbital parameters.
import os

def generate_gmat_script(sma, inc, raan, GS, drag='On', srp='On', ecc=0.001, output_file='current_gmat.script'):
    template_path = 'templates/gmat_template.script'
    with open(template_path, 'r') as f:
        template = f.read()

    filled = template.replace('{{SMA}}', str(sma)) \
                     .replace('{{ECC}}', str(ecc)) \
                     .replace('{{INC}}', str(inc)) \
                     .replace('{{RAAN}}', str(raan)) \
                     .replace('{{DRAG}}', drag) \
                     .replace('{{SRP}}', srp) \
                     .replace('{{LAT}}', str(GS[0])) \
                     .replace('{{LONG}}', str(GS[1])) \
                     .replace('{{ALT}}', str(GS[2])) 
    
    with open(output_file, 'w') as f:
        f.write(filled)

    print(f' GMAT script written to: {output_file}')
    return output_file
