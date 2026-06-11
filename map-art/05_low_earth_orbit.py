"""LOW EARTH ORBIT — the planet wearing its air routes as a crown.

A true 3D globe in matplotlib's mplot3d: coastlines wrapped onto a
sphere, every one of ~28,000 airports a point of light on the night
side of nothing, and great-circle flight paths physically lifting off
the surface like charged field lines. The far hemisphere is removed
by hand — every vertex is culled against the camera vector, which is
the oldest trick in 3D graphics and still works.
"""

import numpy as np
import geopandas as gpd
import shapely
import airportsdata
from matplotlib import pyplot as plt
from matplotlib.path import Path

WORLD_SHP = "/tmp/gpd14/geopandas/datasets/naturalearth_lowres/naturalearth_lowres.shp"
rng = np.random.default_rng(5)

ELEV, AZIM = 18.0, -55.0     # camera over the North Atlantic

def to_xyz(lon_deg, lat_deg, r=1.0):
    lon, lat = np.radians(lon_deg), np.radians(lat_deg)
    return (r * np.cos(lat) * np.cos(lon),
            r * np.cos(lat) * np.sin(lon),
            r * np.sin(lat))

# camera direction for the chosen view
e, a = np.radians(ELEV), np.radians(AZIM)
view = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])

def facing(x, y, z, r=1.0):
    """True where a point on a sphere of radius r faces the camera."""
    return (x * view[0] + y * view[1] + z * view[2]) / max(r, 1e-9) > 0.06

def plot_culled(ax, x, y, z, keep, **kw):
    """Plot a polyline, broken wherever vertices fall on the far side."""
    brk = np.where(~keep)[0]
    runs = np.split(np.arange(len(x)), brk)
    for run in runs:
        run = run[keep[run]]
        if len(run) > 1:
            ax.plot(x[run], y[run], z[run], **kw)

# ------------------------------------------------------------------ canvas
BG = "#05070d"
fig = plt.figure(figsize=(13.5, 13.5), dpi=160)
fig.patch.set_facecolor(BG)

# starfield behind everything
sky = fig.add_axes((0, 0, 1, 1), zorder=0)
sky.set_facecolor(BG)
sky.set_xticks([]); sky.set_yticks([])
for s in sky.spines.values():
    s.set_visible(False)
ns = 900
sx, sy = rng.random(ns), rng.random(ns)
sky.scatter(sx, sy, s=rng.power(0.4, ns) * 2.2, c="#cdd8ee",
            alpha=rng.uniform(0.15, 0.8, ns), lw=0)

ax = fig.add_axes((0.02, 0.0, 0.96, 0.96), projection="3d",
                  computed_zorder=False, zorder=1)
ax.set_facecolor((0, 0, 0, 0))
ax.patch.set_alpha(0)

# the planet body: a dark disc of ocean-night
u = np.linspace(0, 2 * np.pi, 90)
v = np.linspace(0, np.pi, 60)
SX = 0.992 * np.outer(np.cos(u), np.sin(v))
SY = 0.992 * np.outer(np.sin(u), np.sin(v))
SZ = 0.992 * np.outer(np.ones_like(u), np.cos(v))
ax.plot_surface(SX, SY, SZ, color="#0a1322", linewidth=0,
                antialiased=False, shade=False, alpha=1.0)

# ------------------------------------------------------------- coastlines
world = gpd.read_file(WORLD_SHP)
land = shapely.union_all(world.geometry.values)
for poly in shapely.get_parts(land):
    for ring in [poly.exterior, *poly.interiors]:
        lon_r, lat_r = np.array(ring.coords).T
        x, y, z = to_xyz(lon_r, lat_r, 1.0)
        keep = facing(x, y, z)
        plot_culled(ax, x, y, z, keep, color="#4f7fa8", lw=0.8, alpha=0.9)

# graticule, faint
for glat in range(-60, 90, 30):
    gl = np.linspace(-180, 180, 181)
    x, y, z = to_xyz(gl, np.full_like(gl, float(glat)))
    plot_culled(ax, x, y, z, facing(x, y, z), color="#1b2a40", lw=0.45)
for glon in range(-180, 180, 30):
    gl = np.linspace(-90, 90, 91)
    x, y, z = to_xyz(np.full_like(gl, float(glon)), gl)
    plot_culled(ax, x, y, z, facing(x, y, z), color="#1b2a40", lw=0.45)

# ------------------------------------------------------- the city lights
airports = airportsdata.load()
alat = np.array([ap["lat"] for ap in airports.values()])
alon = np.array([ap["lon"] for ap in airports.values()])
x, y, z = to_xyz(alon, alat, 1.002)
keep = facing(x, y, z)
ax.scatter(x[keep], y[keep], z[keep], s=2.6, c="#ffdf9e", alpha=0.16, lw=0)
ax.scatter(x[keep], y[keep], z[keep], s=0.5, c="#fff3d0", alpha=0.75, lw=0)
print(f"{keep.sum()} airports on the day side")

# --------------------------------------------------------- orbital arcs
iata = {ap["iata"]: (ap["lon"], ap["lat"]) for ap in airports.values() if ap["iata"]}
ROUTES = [("JFK", "LHR"), ("ATL", "CDG"), ("MIA", "MAD"), ("YYZ", "FRA"),
          ("GRU", "LIS"), ("EZE", "LHR"), ("BOS", "KEF"), ("ORD", "AMS"),
          ("DFW", "LHR"), ("IAD", "GVA"), ("MEX", "MAD"), ("BOG", "CDG"),
          ("YUL", "CDG"), ("SEA", "KEF"), ("LAX", "LHR"), ("PHL", "DUB"),
          ("CLT", "MUC"), ("DTW", "AMS"), ("SFO", "ZRH"), ("PTY", "MAD"),
          ("LIM", "AMS"), ("SCL", "MAD"), ("REC", "LIS"), ("YYT", "LHR")]

def vec(lon, lat):
    lon, lat = np.radians(lon), np.radians(lat)
    return np.array([np.cos(lat) * np.cos(lon),
                     np.cos(lat) * np.sin(lon), np.sin(lat)])

for a_code, b_code in ROUTES:
    if a_code not in iata or b_code not in iata:
        continue
    p, q = vec(*iata[a_code]), vec(*iata[b_code])
    omega = np.arccos(np.clip(p @ q, -1, 1))
    t = np.linspace(0, 1, 120)[:, None]
    pts = (np.sin((1 - t) * omega) * p + np.sin(t * omega) * q) / np.sin(omega)
    lift = 1.0 + (0.05 + 0.16 * omega / np.pi) * np.sin(np.pi * t[:, 0]) ** 0.9
    x, y, z = pts[:, 0] * lift, pts[:, 1] * lift, pts[:, 2] * lift
    keep = facing(x, y, z, r=1.0)            # generous: arcs ride high
    plot_culled(ax, x, y, z, keep, color="#7fe3d2", lw=2.6, alpha=0.10)
    plot_culled(ax, x, y, z, keep, color="#a9f0e2", lw=0.8, alpha=0.8)

# the limb of the planet: a thin atmosphere ring facing the camera
n1 = np.array([1.0, 0.0, 0.0]) - view[0] * view
n1 /= np.linalg.norm(n1)
n2 = np.cross(view, n1)
tt = np.linspace(0, 2 * np.pi, 360)
for r, lw, al, c in [(1.0, 1.2, 0.9, "#3d6c96"), (1.012, 2.6, 0.25, "#6fb3e8"),
                     (1.028, 4.5, 0.10, "#8fd0ff")]:
    ring = r * (np.outer(np.cos(tt), n1) + np.outer(np.sin(tt), n2))
    ax.plot(ring[:, 0], ring[:, 1], ring[:, 2], color=c, lw=lw, alpha=al)

ax.view_init(elev=ELEV, azim=AZIM)
ax.set_box_aspect((1, 1, 1))
L = 1.06
ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_zlim(-L, L)
ax.set_axis_off()

fig.text(0.5, 0.955, "LOW EARTH ORBIT", ha="center", color="#dce8f8",
         fontsize=23, family="DejaVu Serif", weight="bold", zorder=5)
fig.text(0.5, 0.925, "the planet wearing its air routes as a crown — "
         "every light below is an airport",
         ha="center", color="#7c8aa5", fontsize=11, family="DejaVu Serif",
         style="italic", zorder=5)
fig.text(0.5, 0.035, "a true 3D globe in matplotlib · far hemisphere culled "
         "vertex by vertex against the camera",
         ha="center", color="#566179", fontsize=9, family="DejaVu Serif",
         zorder=5)

fig.savefig("map-art/05_low_earth_orbit.png", facecolor=BG)
print("wrote map-art/05_low_earth_orbit.png")
