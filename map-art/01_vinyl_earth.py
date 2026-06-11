"""TERRA, 33 1/3 RPM — the planet pressed to vinyl.

One continuous spiral groove, outer rim = 84N, inner runout = 60S.
As the needle travels the spiral, longitude is the rotation angle and
latitude is the groove radius. Wherever the groove crosses land the
"signal" modulates — continents become the loud passages of the record.

Pure GeoPandas/Shapely + Matplotlib. No basemap service, no GIS suite.
"""

import numpy as np
import geopandas as gpd
import shapely
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle

WORLD_SHP = "/tmp/gpd14/geopandas/datasets/naturalearth_lowres/naturalearth_lowres.shp"

rng = np.random.default_rng(42)

# ---------------------------------------------------------------- geography
world = gpd.read_file(WORLD_SHP)
land = shapely.union_all(world.geometry.values)
shapely.prepare(land)

# ---------------------------------------------------------------- the groove
R_OUT, R_IN = 0.965, 0.345          # groove band radii
LAT_TOP, LAT_BOT = 84.0, -60.0      # latitude carried by the groove band
N_REV = 88                          # revolutions of the spiral
SAMPLES_PER_REV = 1400

n = N_REV * SAMPLES_PER_REV
t = np.linspace(0.0, 1.0, n)
theta = 2 * np.pi * N_REV * t
radius = R_OUT - (R_OUT - R_IN) * t

lon = (np.degrees(theta) % 360.0) - 180.0
lat = LAT_TOP - (LAT_TOP - LAT_BOT) * t
on_land = shapely.contains_xy(land, lon, lat)

# Audio-like signal: smoothed noise, only audible over land
pitch = (R_OUT - R_IN) / N_REV                       # spacing between grooves
raw = rng.normal(0.0, 1.0, n)
kernel = np.hanning(9); kernel /= kernel.sum()
signal = np.convolve(raw, kernel, mode="same")
signal += 0.6 * np.sin(theta * 31.0) * np.convolve(rng.normal(0, 1, n), kernel, mode="same")
signal /= np.abs(signal).max()

amp = np.where(on_land, 0.38 * pitch, 0.03 * pitch)
r_mod = radius + amp * signal

x = r_mod * np.cos(theta)
y = r_mod * np.sin(theta)

# ---------------------------------------------------------------- styling
BG = "#0b0a08"
GOLD = np.array([0.93, 0.78, 0.42])     # land signal
GROOVE = np.array([0.36, 0.34, 0.31])   # silent vinyl groove

pts = np.column_stack([x, y]).reshape(-1, 1, 2)
segs = np.concatenate([pts[:-1], pts[1:]], axis=1)

# vinyl sheen: two soft angular highlights sweeping across the disc
sheen = 0.62 + 0.38 * np.cos(2.0 * (theta - 0.7)) ** 2
base_rgb = np.where(on_land[:, None], GOLD, GROOVE)
alpha = np.where(on_land, 0.95, 0.34) * sheen
colors = np.concatenate([base_rgb, alpha[:, None]], axis=1)[:-1]
widths = np.where(on_land, 0.85, 0.45)[:-1]

fig, ax = plt.subplots(figsize=(14, 14), dpi=170)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-1.12, 1.12)
ax.set_ylim(-1.12, 1.12)

# disc body
ax.add_patch(Circle((0, 0), 1.045, color="#11100d", zorder=0))
ax.add_patch(Circle((0, 0), 1.045, fill=False, ec="#3a352c", lw=1.2, zorder=6))
ax.add_patch(Circle((0, 0), 0.995, fill=False, ec="#221f1a", lw=2.4, zorder=1))

ax.add_collection(LineCollection(segs, colors=colors, linewidths=widths,
                                 capstyle="round", zorder=2))

# lead-out grooves and label
for r in np.linspace(R_IN - 0.012, 0.318, 4):
    ax.add_patch(Circle((0, 0), r, fill=False, ec="#2c2922", lw=0.5, zorder=2))

ax.add_patch(Circle((0, 0), 0.30, color="#7d1f24", zorder=3))           # label
ax.add_patch(Circle((0, 0), 0.30, fill=False, ec="#caa75c", lw=1.1, zorder=4))
ax.add_patch(Circle((0, 0), 0.262, fill=False, ec="#caa75c", lw=0.4, alpha=0.55, zorder=4))
ax.add_patch(Circle((0, 0), 0.018, color=BG, zorder=5))                  # spindle
ax.add_patch(Circle((0, 0), 0.018, fill=False, ec="#caa75c", lw=0.6, zorder=5))

label_kw = dict(ha="center", color="#f3e2b8", zorder=5, family="DejaVu Serif")
ax.text(0, 0.215, "TERRA", fontsize=21, weight="bold", **label_kw)
ax.text(0, 0.168, "33⅓ RPM · LONG PLAY", fontsize=7.5, **label_kw)
ax.text(0, -0.118, "SIDE A — ONE GROOVE, EVERY COASTLINE", fontsize=6.8, **label_kw)
ax.text(0, -0.163, "outer rim 84°N · runout 60°S · 88 revolutions",
        fontsize=6.4, alpha=0.85, **label_kw)
ax.text(0, -0.215, "recorded live over 4.5 billion years", fontsize=6.4,
        style="italic", alpha=0.85, **label_kw)

ax.text(0, -1.085, "the signal is land — the silence is ocean",
        ha="center", color="#8a8273", fontsize=10, family="DejaVu Serif",
        style="italic")

fig.savefig("map-art/01_vinyl_earth.png", facecolor=BG, bbox_inches="tight",
            pad_inches=0.18)
print("wrote map-art/01_vinyl_earth.png")
