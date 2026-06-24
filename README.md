# sphere-gallery

Spherical bookmark gallery for Dragon's Chrome `Now` bookmark folder. You stand
at the center of a sphere and the bookmarks wrap around you on its inner wall,
with an alternate Art view that turns the same bookmarks into a generated
gallery wall.

- **Three.js** — bookmark cards on the inside of a sphere, camera at the origin
- **GSAP** — staggered intro, hover scale, click-to-open detail page transition
- Lenis-style drag: eased follow (lerp) + inertia on release; wheel orbits too
- Click a card -> camera dollies toward it, a bookmark detail page slides up
- Art mode -> full-screen grid of generated bookmark artwork
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

Tests cover load, drag easing + inertia, click -> detail open/close + camera
restore, Art mode, WebGL nonblank rendering, and text contrast.
