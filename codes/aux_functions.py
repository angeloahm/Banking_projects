import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textwrap import dedent

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

def binned_scatter(
    x,
    y,
    q,
    marker="o",
    dispersion=False,
    label=None,
    color='navy',
    x_axis="rank",     # "rank"  → percentile ranks    (default, original behaviour)
                       # "value" → actual x-values
):
    """
    Scatter the mean of *y* in q-quantile bins of *x*.

    Parameters
    ----------
    x, y : array-like or pd.Series
    q    : int
        Number of equal-frequency bins.
    marker : str
        Matplotlib marker for the mean dots.
    dispersion : bool
        If True, also plot the median and IQR of *y* in each bin.
    label : str | None
        Legend label for the mean dots.
    x_axis : {"rank", "value"}
        What to place on the x-axis:
        - "rank"  → percentile ranks of *x* (0–1).
        - "value" → the underlying *x* (in data units).
    """

    # -- ensure pandas Series -------------------------------------------------
    if not isinstance(x, pd.Series):
        x = pd.Series(x, name=getattr(x, "name", None))
    if not isinstance(y, pd.Series):
        y = pd.Series(y, name=getattr(y, "name", None))

    # -- percentile ranks & bin membership -----------------------------------
    x_pct = x.rank(method="average", pct=True)
    x_binned = pd.qcut(x_pct, q=q, duplicates="drop")

    # -- within-bin statistics ------------------------------------------------
    bin_centers, means, medians, mins, maxs = [], [], [], [], []

    for interval in x_binned.unique():
        mask = x_binned == interval
        # centre depends on the chosen x-axis
        if x_axis == "rank":
            bin_center = x_pct[mask].mean()
        elif x_axis == "value":
            bin_center = x[mask].mean()
        else:
            raise ValueError("x_axis must be 'rank' or 'value'.")

        ys = y[mask]
        bin_centers.append(bin_center)
        means.append(ys.mean())
        medians.append(ys.median())
        mins.append(ys.quantile(0.25))
        maxs.append(ys.quantile(0.75))

    # -- sort by x ------------------------------------------------------------
    order = np.argsort(bin_centers)
    bin_centers = np.array(bin_centers)[order]
    means       = np.array(means)[order]
    medians     = np.array(medians)[order]
    mins        = np.array(mins)[order]
    maxs        = np.array(maxs)[order]

    # -- plot -----------------------------------------------------------------
    plt.scatter(
        bin_centers,
        means,
        marker=marker,
        alpha=1,
        s=50,
        edgecolors="black",
        color=color,
        label=label,
    )

    if dispersion:
        plt.scatter(bin_centers, medians, marker=marker, s=50, alpha=0.7, color="green")
        plt.scatter(bin_centers, mins,    marker=marker, s=50, alpha=0.7, color="grey")
        plt.scatter(bin_centers, maxs,    marker=marker, s=50, alpha=0.7, color="grey")

    # -- labels & grid --------------------------------------------------------
    if x_axis == "rank":
        plt.xlabel(f"Percentile Rank of {x.name or 'x'}")
        ticks = np.linspace(0, 1, 6)
        plt.xticks(ticks, [f"{int(t*100)}" for t in ticks])
    else:  # actual values
        plt.xlabel(x.name or "x")

    plt.ylabel(y.name or "y")
    plt.grid(True, linestyle="--", alpha=0.5, linewidth=0.5, color="lightgrey")



def lorenz_points(series):
    s = np.sort(series.values)                  # ascending order
    cum_val  = np.cumsum(s) / s.sum()          # cumulative share of variable
    cum_bank = np.arange(1, len(s)+1) / len(s) # cumulative share of banks
    return cum_bank, cum_val



def interp_row(row: pd.Series, mids_array: np.ndarray) -> np.ndarray:
    """
    Interpolates one quarter's Treasury curve to the requested mid-points.
    Uses straight-line (piece-wise linear) interpolation.
    Returns NaNs if fewer than two valid curve points are available.
    """
    mask = row.notna()
    xp   = row.index.values[mask].astype(float)
    fp   = row.values[mask].astype(float)

    if xp.size < 2:
        return np.full_like(mids_array, np.nan, dtype=float)

    # numpy.interp = plain linear interpolation
    return np.interp(mids_array, xp, fp)

def coef_line(param, res):
    coef, se, p = res.params[param], res.std_errors[param], res.pvalues[param]
    star = '^{***}' if p < .01 else ('^{**}' if p < .05 else ('^{*}' if p < .10 else ''))
    return f"${coef:.3f}{star}$", f"$({se:.3f})$"
