import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import find_peaks

# Load data and calculate invariant mass
df = pd.read_csv('MuRun2010B.csv', header=0)

E1, E2 = df.iloc[:, 3].astype(float), df.iloc[:, 12].astype(float)
px1, px2 = df.iloc[:, 4].astype(float), df.iloc[:, 13].astype(float)
py1, py2 = df.iloc[:, 5].astype(float), df.iloc[:, 14].astype(float)
pz1, pz2 = df.iloc[:, 6].astype(float), df.iloc[:, 15].astype(float)

# M = sqrt((E1 + E2)^2 - (px1 + px2)^2 - (py1 + py2)^2 - (pz1 + pz2)^2)
invariant_mass = np.sqrt((E1 + E2)**2 - ((px1 + px2)**2 + (py1 + py2)**2 + (pz1 + pz2)**2))

# Set up the plot
plt.figure(figsize=(11, 6))

# Set up the plot with logarithmic scales
ax = sns.kdeplot(
    invariant_mass, 
    log_scale=True,  
    fill=False, 
    color="blue", 
    linewidth=2, 
    label="Data Distribution"
)

# Explicitly declare axes scales 
ax.set_xscale('log')
ax.set_yscale('symlog', linthresh=1.0)

# Map peak positions
line = ax.lines[0]
x_data = line.get_xdata()
y_density = line.get_ydata()

# Event count scaling
total_events = len(invariant_mass)
grid_points = len(x_data)
log_range = np.log10(x_data.max()) - np.log10(x_data.min())
dx = log_range / grid_points

y_data = y_density * total_events * dx
line.set_ydata(y_data) 

peaks, _ = find_peaks(y_data, prominence=1.0) # Adjusted for real counts scale

# Peak 1 (J/Psi): Locate the absolute highest point on the entire graph
global_max_idx = np.argmax(y_data)
jpsi_idx = peaks[np.abs(peaks - global_max_idx).argmin()]
x_jpsi = x_data[jpsi_idx]
y_jpsi = y_data[jpsi_idx]

# Peak 2 (Υ): Filter peaks that exist after the J/Psi peak along the x-axis to find the next significant resonance
right_peaks = [idx for idx in peaks if x_data[idx] > x_jpsi]

if right_peaks:
    # Pick the highest remaining peak in this right-hand region
    upsilon_idx = right_peaks[np.argmax(y_data[right_peaks])]
    x_up = x_data[upsilon_idx]
    y_up = y_data[upsilon_idx]
else:
    # Fallback to J/Psi values if no secondary peak exists to the right
    x_up, y_up = x_jpsi, y_jpsi

# Peak 3 (Z Boson): Filter peaks that exist after the Uplison peak along the x-axis to find the next significant resonance
right_peaks = [idx for idx in peaks if x_data[idx] > x_up]

if right_peaks:
    # Pick the highest remaining peak in this right-hand region
    Z_Boson_idx = right_peaks[np.argmax(y_data[right_peaks])]
    x_z_boson = x_data[Z_Boson_idx]
    y_z_boson = y_data[Z_Boson_idx]
else:
    # Fallback to Uplison values if no secondary peak exists to the right
    x_z_boson, y_z_boson = x_up, y_up
    
# Populate the search criteria dynamically using the detected values
particle_targets = {
    r'$J/\psi$': {'mass': x_jpsi, 'count': y_jpsi, 'color': 'red'},
    r'$\Upsilon$': {'mass': x_up, 'count': y_up, 'color': 'purple'},
    r'$Z$ Boson': {'mass': x_z_boson, 'count': y_z_boson, 'color': 'orange'}
}

explicit_y_ticks = [0, 1, 100, 1000, 10000]
explicit_labels = ["0", "1", "$10^2$", "$10^3$", "$10^4$"]

new_y_ticks = []
new_y_labels = []
box_text_lines = []

# Draw tracking lines, modify Y-axis, and collect stats for the box
for name, config in particle_targets.items():
    actual_mass = config['mass']
    peak_y_val = config['count']
    
    # Draw thin vertical line up to the curve height using configured color (Red / Purple)
    plt.vlines(x=actual_mass, ymin=0, ymax=peak_y_val, color=config['color'], linestyle='-', linewidth=1.2)
    
    # Create horizontal tracking indicator to the y-axis
    plt.hlines(y=peak_y_val, xmin=x_data.min(), xmax=actual_mass, color='gray', linestyle=':', linewidth=0.8)
    
    # Save values for the Y-axis labels (Changed text to [Event: ...])
    new_y_ticks.append(peak_y_val)
    new_y_labels.append(f"{name}\n[Event: {int(peak_y_val)}]")
    
    # Format text row for the stats box
    box_text_lines.append(f"{name} Mass: {actual_mass:.3f} GeV/c²")

# Combine explicit log steps with your custom particle peak values
combined_ticks = explicit_y_ticks + new_y_ticks
combined_labels = explicit_labels + new_y_labels

ax.set_yticks(combined_ticks)
ax.set_yticklabels(combined_labels, fontsize=9, color='darkred', fontweight='bold')

for label in ax.get_yticklabels()[:len(explicit_y_ticks)]:
    label.set_color('black')
    label.set_fontweight('normal')

# Fixed Y limits to keep the axis clean from 0 to slightly above 10^4
plt.ylim(bottom=0, top=15000)

# Information box stating the values
box_text = "\n".join(box_text_lines)
props = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', alpha=0.8)
ax.text(0.95, 0.85, box_text, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='right', bbox=props)

# Chart finalization
plt.title(r'Dimuon Invariant Mass Spectrum', fontsize=14)
plt.xlabel(r'Invariant Mass $M$ [GeV/c$^2$]', fontsize=12)
plt.ylabel('Event', fontsize=12)  
plt.xlim(2.0, 110.0)  
plt.grid(True, which="both", linestyle='--', alpha=0.4)
plt.legend(loc='upper left')

plt.tight_layout()
plt.savefig('dimuon_invariant_mass_spectrum.png', dpi=300)
plt.show()
