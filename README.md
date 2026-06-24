# sphere-gallery

Spherical and walkable-room bookmark gallery for Dragon's Chrome `Now` bookmark
folder. You can stand at the center of a sphere with bookmarks wrapped around
the inner wall, or switch into a museum-style room with bookmark frames hung
along both sides.

- **Three.js** — bookmark cards on the inside of a sphere, camera at the origin
- **GSAP** — staggered intro, hover scale, click-to-open detail page transition
- Lenis-style drag: eased follow (lerp) + inertia on release; wheel orbits too
- Click a card -> camera dollies toward it, a bookmark detail page slides up
- Room mode -> walkable 3D gallery with one wall frame per bookmark
- Images use saved screenshots when available, with generated artwork fallback

No build step — a single `index.html` with an import map (three + gsap from CDN).

## Data Source

`shots/manifest.json` is a snapshot of Chrome's `Bookmarks Bar / Now` folder from
the `Default` Chrome profile:

`/Users/jefffranzen/Library/Application Support/Google/Chrome/Default/Bookmarks`

## Run

```bash
npm run serve   # http://localhost:4179
```

## Test

```bash
npm install
npx playwright test
```

Real thumbnails do not populate automatically. `shots/manifest.json` points to
saved screenshots where this repo already had one; everything else gets
generated artwork until a capture job writes a real `shots/*.jpg` and updates
the manifest.

Tests cover load, drag easing + inertia, click -> detail open/close + camera
restore, Room mode, WebGL nonblank rendering, and text contrast.
