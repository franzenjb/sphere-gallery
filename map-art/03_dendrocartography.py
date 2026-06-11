"""DENDROCARTOGRAPHY — the Earth as a cross-cut slab of wood.

Every "growth ring" on this slab is an iso-distance contour from the
nearest coastline: the oceans grain outward ring by ring, and the
continents sit in the timber as knots. A Hammer projection gives the
slab its elliptical cross-section.

Method: rasterize the Natural Earth land polygons to a mask, take a
Euclidean distance transform in both directions (scipy), perturb the
signed field with low-frequency noise so the grain wanders like real
wood, then contour it in projected space.
"""

import numpy as np
import geopandas as gpd
import shapely
from scipy import ndimage
from matplotlib import pyplot as plt

WORLD_SHP = "/tmp/gpd14/geopandas/datasets/naturalearth_lowres/naturalearth_lowres.shp"
rng = np.random.default_rng(11)

# --------------------------------------------------------------- land mask
NX, NY = 2600, 1300
lon = np.linspace(-180, 180, NX)
lat = np.linspace(-90, 90, NY)
LON, LAT = np.meshgrid(lon, lat)

world = gpd.read_file(WORLD_SHP)
world = world[world["continent"] != "Antarctica"]   # keep the slab clean
land_geom = shapely.union_all(world.geometry.values)
shapely.prepare(land_geom)
mask = shapely.contains_xy(land_geom, LON.ravel(), LAT.ravel()).reshape(LAT.shape)
print("land mask done")

# --------------------------------------------------- signed distance field
d_ocean = ndimage.distance_transform_edt(~mask)   # rings spreading over sea
d_land = ndimage.distance_transform_edt(mask)     # rings tightening inland
signed = np.where(mask, -d_land, d_ocean) * (360.0 / NX)  # in degrees

# wood never grows in perfect circles: let the grain wander
def billow(shape, octaves=4, base=6):
    out = np.zeros(shape)
    for o in range(octaves):
        small = rng.normal(0, 1, (base * 2**o, base * 2**o * 2))
        out += ndimage.zoom(small, (shape[0] / small.shape[0],
                                    shape[1] / small.shape[1]), order=3) / 2**o
    return out / np.abs(out).max()

grain = billow(signed.shape)
signed_w = signed + 1.6 * grain + 0.35 * grain**2 * np.sign(signed)
print("distance field done")

# ------------------------------------------------------ Hammer projection
def hammer(lon_deg, lat_deg):
    lam = np.radians(lon_deg) / 2.0
    phi = np.radians(lat_deg)
    d = np.sqrt(1 + np.cos(phi) * np.cos(lam))
    return (2 * np.sqrt(2) * np.cos(phi) * np.sin(lam) / d,
            np.sqrt(2) * np.sin(phi) / d)

PX, PY = hammer(LON, LAT)

# --------------------------------------------------------------- the slab
PAPER = "#efe3cd"
fig, ax = plt.subplots(figsize=(19, 10.4), dpi=160)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_aspect("equal")
ax.axis("off")

# heartwood vs sapwood: warm fill that darkens toward the continents' core
ax.contourf(PX, PY, signed_w,
            levels=[-40, -12, -6, -2.5, 0, 8, 22, 60],
            colors=["#6d4426", "#7d5230", "#8f6038", "#a27143",
                    "#c89a62", "#d9b27a", "#e6c890"],
            zorder=1)

# ocean grain: one ring roughly every 2 degrees of sea
sea_levels = np.arange(1.0, 62, 2.0)
ax.contour(PX, PY, signed_w, levels=sea_levels, colors="#7a5a36",
           linewidths=np.where(np.arange(len(sea_levels)) % 5 == 0, 0.95, 0.45),
           alpha=0.75, zorder=2)
# fine intermediate grain
ax.contour(PX, PY, signed_w, levels=sea_levels + 1.0, colors="#8a6a44",
           linewidths=0.3, alpha=0.45, zorder=2)

# knots: rings tightening into the landmass interiors
land_levels = np.arange(-38, 0.1, 1.6)
ax.contour(PX, PY, signed_w, levels=land_levels, colors="#3c2613",
           linewidths=0.55, alpha=0.8, zorder=3)

# the coastline itself: the seam where knot meets grain
ax.contour(PX, PY, signed_w, levels=[0.0], colors="#2a1a0c",
           linewidths=1.3, zorder=4)

# bark: the elliptical rim of the slab
t = np.linspace(0, 2 * np.pi, 720)
bw, bh = 2 * np.sqrt(2), np.sqrt(2)
for k, (s, lw, a) in enumerate([(1.000, 2.6, 1.0), (1.012, 1.1, 0.8),
                                (1.024, 0.7, 0.6), (1.036, 0.5, 0.4)]):
    wob = 1 + 0.004 * np.sin(t * (9 + 3 * k) + k)
    ax.plot(bw * s * wob * np.cos(t), bh * s * wob * np.sin(t),
            color="#4a3018", lw=lw, alpha=a, zorder=5)

ax.text(0, bh + 0.22, "DENDROCARTOGRAPHY", ha="center", color="#3c2613",
        fontsize=22, family="DejaVu Serif", weight="bold")
ax.text(0, bh + 0.10, "the Earth, cut like timber — every growth ring is one "
        "step farther from the nearest coastline",
        ha="center", color="#6d533a", fontsize=10.5, family="DejaVu Serif",
        style="italic")
ax.text(0, -bh - 0.16, "continents are the knots · oceans are the grain · "
        "the coastline is the seam where they meet",
        ha="center", color="#6d533a", fontsize=9.5, family="DejaVu Serif")

ax.set_xlim(-bw - 0.22, bw + 0.22)
ax.set_ylim(-bh - 0.30, bh + 0.40)

fig.savefig("map-art/03_dendrocartography.png", facecolor=PAPER,
            bbox_inches="tight", pad_inches=0.18)
print("wrote map-art/03_dendrocartography.png")
