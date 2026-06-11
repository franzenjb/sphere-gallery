# map-art — three wild things GeoPandas + Matplotlib can do

Three experimental map artworks made entirely in Python — no ArcGIS, no
Photoshop, no Illustrator. Each is a single script: run it, get the print.

```bash
pip install geopandas matplotlib scipy airportsdata
# world geometry comes bundled with the geopandas 0.14 wheel:
pip install "geopandas==0.14.4" --target /tmp/gpd14 --no-deps

python3 map-art/01_vinyl_earth.py
python3 map-art/02_no_coastlines.py
python3 map-art/03_dendrocartography.py
```

## 01 · Terra, 33⅓ RPM

The planet pressed to vinyl. One continuous spiral groove — 88 revolutions,
outer rim at 84°N, runout groove at 60°S. As the needle travels, the
rotation angle is longitude and the groove radius is latitude. Wherever
the groove crosses land, the recorded "signal" modulates; over ocean the
groove runs silent. The continents are the loud passages of the record.

*Technique: a parametric spiral sampled 123k times, `shapely.contains_xy`
land tests, a smoothed-noise waveform, and one big `LineCollection`.*

## 02 · No Coastlines Were Drawn

A world map containing zero geographic boundary data. Every point of
light is one of 28,426 real airports; the continents assemble themselves
out of pure human infrastructure, like a star atlas of civilization.
Great-circle "constellations" join 40 major hubs. Mollweide projection
implemented by hand (Newton iteration), great circles by spherical slerp.

*Technique: the `airportsdata` package, three scatter passes for star
glow, and an annotated hub constellation layer.*

## 03 · Dendrocartography

The Earth cut like timber. Every growth ring is an iso-distance contour
from the nearest coastline: oceans grain outward ring by ring, continents
sit in the wood as knots, and the coastline is the seam where they meet.
Hammer projection gives the slab its elliptical cross-section.

*Technique: rasterized land mask → `scipy.ndimage.distance_transform_edt`
in both directions → signed distance field, warped with multi-octave
noise so the grain wanders like real wood, then `contour`/`contourf`.*

## 04 · The Anti-Earth (3D)

A planet where altitude is distance from the sea, rendered as a true 3D
relief surface. Sail away from shore and you climb: the mid-Pacific is
the new Himalaya, while the heart of Asia — farthest from salt water —
sinks into the deepest basin on Earth. The dark line draped on the
terrain is the old coastline; it is still sea level.

*Technique: signed distance field + fractal noise → `mplot3d`
`plot_surface` with `LightSource` hillshading and a hypsometric
colormap pinned to the coastline.*

## 05 · Low Earth Orbit (3D)

A true 3D globe: coastlines wrapped onto a sphere, 23,000 visible
airports as city lights, and great-circle flight paths physically
lifting off the surface like a crown. The far hemisphere is removed
the old-fashioned way — every vertex culled against the camera vector.

*Technique: spherical coordinates by hand, per-vertex hemisphere
culling, layered scatter glow, slerp arcs with altitude lift, and an
atmosphere limb drawn in the camera's image plane.*
