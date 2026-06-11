"""NO COASTLINES WERE DRAWN — geography as an emergent property.

This map contains no country borders, no coastline file, no land polygon.
Every point of light is one of ~29,000 real airports (the `airportsdata`
package). The continents assemble themselves out of pure human
infrastructure, like a long-exposure photo of civilization.

Great-circle "constellations" connect 40 major hubs, drawn the way a
star atlas joins its figures. Mollweide projection implemented by hand.
"""

import numpy as np
import airportsdata
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse

rng = np.random.default_rng(7)

# ------------------------------------------------------------- projection
def mollweide(lon_deg, lat_deg):
    lon = np.radians(np.asarray(lon_deg, dtype=float))
    lat = np.radians(np.asarray(lat_deg, dtype=float))
    theta = lat.copy()
    for _ in range(40):  # Newton iteration: 2t + sin 2t = pi sin(lat)
        f = 2 * theta + np.sin(2 * theta) - np.pi * np.sin(lat)
        theta -= f / np.maximum(2 + 2 * np.cos(2 * theta), 1e-9)
    x = (2 * np.sqrt(2) / np.pi) * lon * np.cos(theta)
    y = np.sqrt(2) * np.sin(theta)
    return x, y

# ------------------------------------------------------------- the stars
airports = airportsdata.load()  # ICAO-keyed dict
lats = np.array([a["lat"] for a in airports.values()])
lons = np.array([a["lon"] for a in airports.values()])
X, Y = mollweide(lons, lats)
print(f"{len(lats)} airports loaded")

iata = {a["iata"]: (a["lon"], a["lat"]) for a in airports.values() if a["iata"]}

HUBS = ["ATL", "LAX", "ORD", "DFW", "JFK", "SEA", "MIA", "YYZ", "MEX", "PTY",
        "GRU", "EZE", "SCL", "BOG", "LIM", "LHR", "CDG", "FRA", "AMS", "MAD",
        "IST", "DXB", "DOH", "JNB", "LOS", "ADD", "CAI", "NBO", "DEL", "BOM",
        "SIN", "BKK", "HKG", "PVG", "PEK", "NRT", "ICN", "SYD", "AKL", "ANC",
        "HNL", "KEF"]
ROUTES = [("JFK", "LHR"), ("LAX", "NRT"), ("SEA", "ICN"), ("SFO", "HKG"),
          ("ANC", "NRT"), ("ATL", "GRU"), ("MIA", "EZE"), ("MEX", "MAD"),
          ("GRU", "JNB"), ("SCL", "SYD"), ("LHR", "SIN"), ("CDG", "DXB"),
          ("FRA", "PEK"), ("IST", "BKK"), ("DXB", "SYD"), ("DOH", "AKL"),
          ("JNB", "SYD"), ("LOS", "GRU"), ("ADD", "PVG"), ("DEL", "LHR"),
          ("BOM", "NBO"), ("SIN", "AKL"), ("HKG", "YYZ"), ("NRT", "HNL"),
          ("HNL", "SYD"), ("KEF", "SEA"), ("AMS", "BOG"), ("CAI", "ICN"),
          ("ORD", "FRA"), ("DFW", "LIM"), ("PTY", "SCL"), ("YYZ", "AMS")]

def great_circle(a, b, k=160):
    """Slerp on the unit sphere between two (lon, lat) points."""
    def vec(lon, lat):
        lon, lat = np.radians(lon), np.radians(lat)
        return np.array([np.cos(lat) * np.cos(lon),
                         np.cos(lat) * np.sin(lon), np.sin(lat)])
    p, q = vec(*a), vec(*b)
    omega = np.arccos(np.clip(p @ q, -1, 1))
    t = np.linspace(0, 1, k)[:, None]
    v = (np.sin((1 - t) * omega) * p + np.sin(t * omega) * q) / np.sin(omega)
    lon = np.degrees(np.arctan2(v[:, 1], v[:, 0]))
    lat = np.degrees(np.arcsin(np.clip(v[:, 2], -1, 1)))
    return lon, lat

# ------------------------------------------------------------- the canvas
BG = "#060a14"
fig, ax = plt.subplots(figsize=(19, 10.2), dpi=160)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_aspect("equal")
ax.axis("off")

W, H = 2 * np.sqrt(2), np.sqrt(2)
ax.add_patch(Ellipse((0, 0), 2 * W, 2 * H, facecolor="#081020",
                     edgecolor="#2a3a55", lw=1.4, zorder=0))

# graticule, faint, like an astrolabe
for glat in range(-60, 90, 30):
    lon_line = np.linspace(-179.9, 179.9, 240)
    gx, gy = mollweide(lon_line, np.full_like(lon_line, glat))
    ax.plot(gx, gy, color="#1c2940", lw=0.5, zorder=1)
for glon in range(-150, 181, 30):
    lat_line = np.linspace(-89.9, 89.9, 240)
    gx, gy = mollweide(np.full_like(lat_line, glon), lat_line)
    ax.plot(gx, gy, color="#1c2940", lw=0.5, zorder=1)

# every airport is a star: three passes = halo, glow, core
ax.scatter(X, Y, s=8.0, c="#1d4a78", alpha=0.10, lw=0, zorder=2)
ax.scatter(X, Y, s=2.2, c="#7fb4e8", alpha=0.35, lw=0, zorder=3)
ax.scatter(X, Y, s=0.55, c="#eaf4ff", alpha=0.85, lw=0, zorder=4)

# a few thousand airports twinkle brighter, like magnitude variation
bright = rng.choice(len(X), size=2600, replace=False)
ax.scatter(X[bright], Y[bright], s=3.2, c="#ffffff", alpha=0.55, lw=0, zorder=4)

# hub constellation lines
for a_code, b_code in ROUTES:
    if a_code not in iata or b_code not in iata:
        continue
    glon, glat = great_circle(iata[a_code], iata[b_code])
    gx, gy = mollweide(glon, glat)
    brk = np.where(np.abs(np.diff(gx)) > 0.5)[0] + 1   # split at the seam
    for seg_x, seg_y in zip(np.split(gx, brk), np.split(gy, brk)):
        ax.plot(seg_x, seg_y, color="#ffd27d", lw=2.2, alpha=0.10, zorder=5)
        ax.plot(seg_x, seg_y, color="#ffd27d", lw=0.65, alpha=0.55, zorder=5)

# hub stars + names, star-atlas style
for code in HUBS:
    if code not in iata:
        continue
    hx, hy = mollweide(*iata[code])
    ax.scatter([hx], [hy], s=46, c="#ffe9b8", alpha=0.95, lw=0, zorder=6,
               marker="*")
    ax.annotate(code, (hx, hy), xytext=(4, 4), textcoords="offset points",
                color="#caa75c", fontsize=6.2, family="DejaVu Sans Mono",
                zorder=7)

ax.text(0, H + 0.16, "NO COASTLINES WERE DRAWN",
        ha="center", color="#dce8f8", fontsize=21, family="DejaVu Serif",
        weight="bold")
ax.text(0, H + 0.055, "every light is one of 29,000 real airports — "
        "the continents assemble themselves",
        ha="center", color="#7c8aa5", fontsize=10.5, family="DejaVu Serif",
        style="italic")
ax.text(0, -H - 0.12, "a star atlas of human infrastructure · "
        "great-circle constellations join 40 hubs",
        ha="center", color="#566179", fontsize=9, family="DejaVu Serif")

ax.set_xlim(-W - 0.25, W + 0.25)
ax.set_ylim(-H - 0.30, H + 0.34)

fig.savefig("map-art/02_no_coastlines.png", facecolor=BG, bbox_inches="tight",
            pad_inches=0.18)
print("wrote map-art/02_no_coastlines.png")
