import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_output(gmat_data, stk_data=None, raan_data=None):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=False)
    
    # --- Plot 1: Access duration ---
    ax1.plot(gmat_data['Intervals'], gmat_data['Duration'], 'o', label='GMAT', color='blue')
    if stk_data:
        ax1.plot(stk_data['Intervals'], stk_data['Duration'], 's', label='STK', color='orange')
    ax1.set_ylabel('Duration (sec)')
    ax1.set_xlabel('Date & Time')
    ax1.legend()
    ax1.set_title('Access Duration Comparison (GMAT vs STK)')
    
    # --- Plot 2: RAAN Drift (optional) ---
    if raan_data:
        ax2.plot(raan_data['Days'], raan_data['RAAN'], '^r')
        ax2.set_ylabel('RAAN Drift (deg)')
        ax2.set_title('RAAN Drift Over Time')
    
    # --- Formatting ---
    ax2.set_xlabel('Date & Time')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d %b\n%H:%M'))

    ax3.plot(gmat_data['Single Days'], gmat_data['Drift'], 'o', label='GMAT', color='blue')
    if stk_data:
        ax3.plot(stk_data['Single Days'], stk_data['Drift'], 's', label='STK', color='orange')
    ax3.set_ylabel('LTAN Drift (Min)')
    ax3.set_xlabel('Day from Epoch')
    ax3.legend()
    ax3.set_title('Access Daily Drift Comparison (GMAT vs STK)')

    fig.tight_layout()
    plt.show()
