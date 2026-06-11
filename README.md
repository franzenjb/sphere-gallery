# sphere-gallery

Phantom.land-style spherical gallery — you stand at the center of a sphere and the
gallery wraps around you on its inner wall.

- **Three.js** — 50 image cards on the inside of a sphere, camera at the origin
- **GSAP** — staggered intro, hover scale, click-to-open detail page transition
- Lenis-style drag: eased follow (lerp) + inertia on release; wheel orbits too
- Click a card → camera dollies toward it, a template detail page slides up
- Images from picsum.photos with canvas-gradient fallback (works offline)

No build step — a single `index.html` with an import map (three + gsap from CDN).

## Run

```bash
npm run serve   # http://localhost:4179
```

## Test

```bash
npm install
npx playwright test
```

Tests cover load, drag easing + inertia, click → detail open/close + camera
restore, and text contrast.
