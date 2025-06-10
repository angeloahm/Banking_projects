import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Helper function to plot mean with min/max shading.
def plot_with_range(ax, data, col, line_color):
    # Group by date and compute statistics
    grp = data.groupby('Date')[col]
    # compute important quantiles:
    q25 = grp.quantile(0.25)
    q75 = grp.quantile(0.75)
    mean_val = grp.mean()
    min_val = grp.min()
    max_val = grp.max()
    # Plot mean
    ax.plot(mean_val.index, mean_val.values, lw=3, color=line_color, label='Mean')
    # Shade between min and max
    ax.fill_between(mean_val.index, q25, q75, color=line_color, alpha=0.2, label='Interquartile Range')
    # Shade between q75 and max:
    ax.fill_between(mean_val.index, q75, max_val, color=line_color, alpha=0.1, label='Over 75th Percentile')
    # Shade between min and q25:
    ax.fill_between(mean_val.index, min_val, q25, color=line_color, alpha=0.1, label='Under 25th Percentile')
    ax.set_ylabel(col)
    ax.grid(True, linestyle='--', alpha=0.5, linewidth=0.5, color='lightgray')
    ax.tick_params(axis='x', rotation=45)
    return ax

def binned_scatter(x, y, q, marker='o', dispersion=False, label=None):
    # Convert x to a pandas Series if needed
    if not isinstance(x, pd.Series):
        x = pd.Series(x)
    # Compute percentile rank for each observation (values between 0 and 1)
    x_pct = x.rank(method='average', pct=True)
    
    # Create quantile bins on the percentile ranks
    x_binned, bin_edges = pd.qcut(x_pct, q=q, retbins=True, duplicates='drop')
    bin_centers = []
    binned_means = []
    binned_median = []
    binned_min = []
    binned_max = []
    
    # Compute statistics within each bin (using the percentile x-values)
    for interval in x_binned.unique():
        x_in_bin = x_pct[x_binned == interval]
        y_in_bin = y[x_binned == interval]
        bin_center = x_in_bin.mean()
        mean_val = y_in_bin.mean()
        median_val = y_in_bin.median()
        # Dispersion: 25th and 75th percentiles of y
        min_val = y_in_bin.quantile(0.25)
        max_val = y_in_bin.quantile(0.75)
        bin_centers.append(bin_center)
        binned_means.append(mean_val)
        binned_median.append(median_val)
        binned_min.append(min_val)
        binned_max.append(max_val)
    
    # Sort results by bin centers
    sorted_indices = np.argsort(bin_centers)
    bin_centers = np.array(bin_centers)[sorted_indices]
    binned_means = np.array(binned_means)[sorted_indices]
    binned_median = np.array(binned_median)[sorted_indices]
    binned_min = np.array(binned_min)[sorted_indices]
    binned_max = np.array(binned_max)[sorted_indices]
    
    # Plot the mean values
    plt.scatter(bin_centers, binned_means, marker=marker, alpha=1, s=50, edgecolors='black', label=label)
    
    # Optionally plot additional dispersion markers
    if dispersion:
        plt.scatter(bin_centers, binned_median, marker=marker, alpha=0.7, s=50, color='green')
        plt.scatter(bin_centers, binned_min, marker=marker, alpha=0.7, s=50, color='grey')
        plt.scatter(bin_centers, binned_max, marker=marker, alpha=0.7, s=50, color='grey')
    
    # Label the axes
    xlabel = f'Percentile Rank of {x.name}' if x.name else 'Percentile Rank'
    plt.xlabel(xlabel)
    plt.ylabel(y.name if hasattr(y, 'name') else 'y')
    plt.grid(True, linestyle='--', alpha=0.5, linewidth=0.5, color='lightgrey')
    
    # Set x-ticks from 0 to 100
    tick_positions = np.linspace(0, 1, 6)
    tick_labels = [f'{int(val*100)}' for val in tick_positions]
    plt.xticks(tick_positions, tick_labels)


def lorenz_points(series):
    s = np.sort(series.values)                  # ascending order
    cum_val  = np.cumsum(s) / s.sum()          # cumulative share of variable
    cum_bank = np.arange(1, len(s)+1) / len(s) # cumulative share of banks
    return cum_bank, cum_val