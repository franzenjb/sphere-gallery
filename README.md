# sphere-gallery

Spatial bookmark atlas for Dragon's Chrome `Now` bookmark folder.

The app no longer treats screenshots as the main artifact, because many Now
bookmarks are private, local, auth-gated, or otherwise poor screenshot targets.
Every bookmark gets a generated placard from its title, domain, category, and
source order. Saved screenshots are used only as detail-panel previews when they
already exist.

- **Three.js Atlas** - generated bookmark placards arranged in domain clusters
- **Board view** - scannable 2D wall using the same consistent placards
- **Retractable/resizable index** - search, cluster filters, selection detail,
  and open-link action
- **Thumbnail independent** - missing screenshots do not produce blank cards
- Drag and wheel rotate the atlas with eased follow and inertia

No build step - a single `index.html` with an import map for Three.js from CDN.

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
generated placard art at runtime. A capture job can still write real
`shots/*.jpg` files and update the manifest, but the UI should not depend on it.

Tests cover load, generated placards, atlas drag easing, search, cluster
filters, Board mode, detail selection, resizable/collapsible index behavior,
WebGL nonblank rendering, and text contrast.
