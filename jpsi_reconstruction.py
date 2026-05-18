import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import find_peaks

# Load data and calculate invariant mass
df = pd.read_csv('Jpsimumu.csv', header=0)

E1, E2 = df.iloc[:, 3].astype(float), df.iloc[:, 12].astype(float)
px1, px2 = df.iloc[:, 4].astype(float), df.iloc[:, 13].astype(float)
py1, py2 = df.iloc[:, 5].astype(float), df.iloc[:, 14].astype(float)
pz1, pz2 = df.iloc[:, 6].astype(float), df.iloc[:, 15].astype(float)

# M = sqrt((E1 + E2)^2 - (px1 + px2)^2 - (py1 + py2)^2 - (pz1 + pz2)^2)
invariant_mass = np.sqrt((E1 + E2)**2 - ((px1 + px2)**2 + (py1 + py2)**2 + (pz1 + pz2)**2))

# Set up the plot
plt.figure(figsize=(11, 6))
ax = sns.kdeplot(invariant_mass, color='blue', linewidth=2, label='Data Distribution')

# Map peak positions
line = ax.lines[0]
x_data = line.get_xdata()
y_data = line.get_ydata()

peaks, _ = find_peaks(y_data, prominence=0.001)

# Peak 1 (J/Psi): Locate the absolute highest point on the entire graph
global_max_idx = np.argmax(y_data)
jpsi_idx = peaks[np.abs(peaks - global_max_idx).argmin()]
x_jpsi = x_data[jpsi_idx]
y_jpsi = y_data[jpsi_idx]

# Peak 2 (Psi(2S)): Filter peaks that exist after the J/Psi peak along the x-axis to find the next significant resonance
right_peaks = [idx for idx in peaks if x_data[idx] > x_jpsi]

if right_peaks:
    # Pick the highest remaining peak in this right-hand region
    psi2s_idx = right_peaks[np.argmax(y_data[right_peaks])]
    x_psi2s = x_data[psi2s_idx]
    y_psi2s = y_data[psi2s_idx]
else:
    # Fallback to J/Psi values if no secondary peak exists to the right
    x_psi2s, y_psi2s = x_jpsi, y_jpsi

# Populate the search criteria dynamically using the detected values
particle_targets = {
    r'$J/\psi$': {'mass': x_jpsi, 'density': y_jpsi, 'color': 'red'},
    r'$\psi(2S)$ meson': {'mass': x_psi2s, 'density': y_psi2s, 'color': 'purple'}
}

original_y_ticks = list(ax.get_yticks())
new_y_ticks = []
new_y_labels = []
box_text_lines = []

# Draw tracking lines, modify Y-axis, and collect stats for the box
for name, config in particle_targets.items():
    actual_mass = config['mass']
    peak_y_val = config['density']
    
    # Draw thin vertical line up to the curve height using configured color (Red / Purple)
    plt.vlines(x=actual_mass, ymin=0, ymax=peak_y_val, color=config['color'], linestyle='-', linewidth=1.2)
    
    # Create horizontal tracking indicator to the y-axis
    plt.hlines(y=peak_y_val, xmin=x_data.min(), xmax=actual_mass, color='gray', linestyle=':', linewidth=0.8)
    
    # Save values for the Y-axis labels
    new_y_ticks.append(peak_y_val)
    new_y_labels.append(f"{name}\n[Density: {peak_y_val:.2f}]")
    
    # Format text row for the stats box
    box_text_lines.append(f"{name} Mass: {actual_mass:.3f} GeV/c²")

combined_ticks = original_y_ticks + new_y_ticks
combined_labels = [f"{tick:.1f}" for tick in original_y_ticks] + new_y_labels

ax.set_yticks(combined_ticks)
ax.set_yticklabels(combined_labels, fontsize=9, color='darkred', fontweight='bold')

# Keep original numerical ticks black
for label in ax.get_yticklabels()[:len(original_y_ticks)]:
    label.set_color('black')
    label.set_fontweight('normal')

# Information box stating the values
box_text = "\n".join(box_text_lines)
props = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', alpha=0.8)
# Places the text box in the upper right quadrant of the graph
ax.text(0.95, 0.85, box_text, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', horizontalalignment='right', bbox=props)

# Chart finalization
plt.title(r'Dimuon Invariant Mass Spectrum highlighting $J/\psi$ and $ \psi(2S) $ Resonances', fontsize=14)
plt.xlabel(r'Invariant Mass $M$ [GeV/c$^2$]', fontsize=12)
plt.ylabel('Density Distribution Framework', fontsize=12)
plt.xlim(2.0, 5.0)  
plt.grid(True, linestyle='--', alpha=0.4)
plt.legend(loc='upper left')

plt.tight_layout()
plt.savefig('jpsi_mass_spectrum.png', dpi=300)
plt.show()
