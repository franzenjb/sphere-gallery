# sphere-gallery

Spherical and walkable-room bookmark gallery for Dragon's Chrome bookmark
folders. You can stand at the center of a sphere with bookmarks wrapped around
the inner wall, or switch into a museum-style room selector where each Chrome
bookmark folder becomes a separate walk-around gallery.

- **Three.js** — bookmark cards on the inside of a sphere, camera at the origin
- **GSAP** — staggered intro, hover scale, click-to-open detail page transition
- Lenis-style drag: eased follow (lerp) + inertia on release; wheel orbits too
- Click a card -> camera dollies toward it, a bookmark detail page slides up
- Room mode -> selectable walk-around 3D galleries with one wall frame per bookmark
- Search -> type a room name, bookmark title, domain, or URL to rebuild Sphere
  and Room as a temporary results gallery
- Images use saved screenshots when available, with generated artwork fallback

No build step — a single `index.html` with an import map (three + gsap from CDN).

## Data Source

`shots/collections.json` is a snapshot of Chrome bookmark folders from the
`Default` Chrome profile. Each folder with bookmarks becomes a selectable room.
`shots/manifest.json` remains the default `Bookmarks Bar / Now` room for
backward compatibility and focused tests:

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

Real thumbnails do not populate automatically. Current default `Now` thumbnail
coverage is 58 of 72 bookmarks. The remaining entries use generated artwork
because they are local files, private/login pages, ArcGIS sign-in pages, or
unreachable hosts. A safe capture pass can add more later, but the sphere and
walk-around rooms stay usable with generated artwork.

Tests cover load, drag easing + inertia, click -> detail open/close + camera
restore, folder room selection, search results, Room mode, WebGL nonblank
rendering, and text contrast.
