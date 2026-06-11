"""THE ANTI-EARTH — a planet where altitude is distance from the sea.

Take the signed distance-to-coast field and read it as terrain:
the farther you sail from shore, the higher you climb, so the middle
of the Pacific becomes the new Himalaya — while the continental
interiors, farthest from salt water, sink into the deepest basins.
The coastline is sea level, as it always was.

Rendered as a true 3D surface with matplotlib's mplot3d + LightSource
hillshading. GeoPandas/Shapely supply the only geography used.
"""

import numpy as np
import geopandas as gpd
import shapely
from scipy import ndimage
from matplotlib import pyplot as plt
from matplotlib.colors import LightSource, LinearSegmentedColormap
from matplotlib.path import Path

WORLD_SHP = "/tmp/gpd14/geopandas/datasets/naturalearth_lowres/naturalearth_lowres.shp"
rng = np.random.default_rng(3)

# ------------------------------------------------------------- distance field
NX, NY = 1440, 720
lon = np.linspace(-180, 180, NX)
lat = np.linspace(-90, 90, NY)
LON, LAT = np.meshgrid(lon, lat)

world = gpd.read_file(WORLD_SHP)
world = world[world["continent"] != "Antarctica"]
land_geom = shapely.union_all(world.geometry.values)
shapely.prepare(land_geom)
mask = shapely.contains_xy(land_geom, LON.ravel(), LAT.ravel()).reshape(LAT.shape)

d_ocean = ndimage.distance_transform_edt(~mask)
d_land = ndimage.distance_transform_edt(mask)
signed = np.where(mask, -d_land, d_ocean) * (360.0 / NX)   # degrees from coast
print("distance field done")

# the terrain: smooth swell + fractal roughness that grows with altitude
def billow(shape, octaves=5, base=8):
    out = np.zeros(shape)
    for o in range(octaves):
        small = rng.normal(0, 1, (base * 2**o, base * 2**o * 2))
        out += ndimage.zoom(small, (shape[0] / small.shape[0],
                                    shape[1] / small.shape[1]), order=3) / 2**o
    return out / np.abs(out).max()

Z = ndimage.gaussian_filter(signed, sigma=2.0)
Z += billow(Z.shape) * (0.18 * np.abs(Z) + 0.4)

step = 3                                     # surface resolution
Zs = Z[::step, ::step]
LONs, LATs = LON[::step, ::step], LAT[::step, ::step]

# ------------------------------------------------------------- color + shade
# inverted hypsometric tint, pinned so 0.5 = the coastline = sea level
terrain = LinearSegmentedColormap.from_list("antiearth", [
    (0.00, "#102e38"),   # deepest basins: old continental cores
    (0.22, "#1d5a52"),
    (0.40, "#3f8266"),
    (0.50, "#d8c690"),   # the coastline
    (0.60, "#b3925e"),
    (0.74, "#8c6a4a"),
    (0.87, "#a4938a"),
    (1.00, "#f7f5f0"),   # mid-ocean summits: the new snowcaps
])

zmin, zmax = Zs.min(), Zs.max()
normed = np.where(Zs < 0, 0.5 * (1 - Zs / zmin), 0.5 * (1 + Zs / zmax))
rgb = terrain(normed)[..., :3]
ls = LightSource(azdeg=310, altdeg=40)
shaded = ls.shade_rgb(rgb, Zs, vert_exag=0.12, blend_mode="soft")

# ------------------------------------------------------------------ render
BG = "#0a0c10"
fig = plt.figure(figsize=(19, 11.6), dpi=150)
fig.patch.set_facecolor(BG)
ax = fig.add_subplot(111, projection="3d", computed_zorder=False)
ax.set_facecolor(BG)

ax.plot_surface(LONs, LATs, Zs, facecolors=shaded, rstride=1, cstride=1,
                linewidth=0, antialiased=False, shade=False)

# the old coastline, traced at sea level like a ghost
cs = plt.figure().add_subplot()                     # scratch axes for paths
coast = cs.contour(LON, LAT, mask.astype(float), levels=[0.5])
plt.close(cs.figure)
for path in coast.get_paths():
    codes = path.codes if path.codes is not None else \
        np.r_[Path.MOVETO, np.full(len(path.vertices) - 1, Path.LINETO)]
    breaks = np.where(codes == Path.MOVETO)[0]
    for seg in np.split(path.vertices, breaks[1:]):
        if len(seg) > 1:
            ax.plot(seg[:, 0], seg[:, 1], np.full(len(seg), 0.6),
                    color="#15181d", lw=0.6, alpha=0.7)

ax.view_init(elev=52, azim=-95)
ax.set_box_aspect((2.1, 1.1, 0.34))
ax.set_zlim(zmin * 1.5, zmax * 1.1)
ax.set_axis_off()
ax.set_position((-0.16, -0.24, 1.32, 1.46))         # fill the frame

fig.text(0.5, 0.94, "THE ANTI-EARTH", ha="center", color="#e8e4da",
         fontsize=25, family="DejaVu Serif", weight="bold")
fig.text(0.5, 0.90, "a planet where altitude is distance from the sea — "
         "the mid-Pacific is the new Himalaya, and the heart of Asia "
         "is the deepest basin on Earth",
         ha="center", color="#8b8fa0", fontsize=11.5, family="DejaVu Serif",
         style="italic")
fig.text(0.5, 0.045, "the dark line is the old coastline · it is still sea level",
         ha="center", color="#6c7080", fontsize=10, family="DejaVu Serif")

fig.savefig("map-art/04_anti_earth.png", facecolor=BG)
print("wrote map-art/04_anti_earth.png")
