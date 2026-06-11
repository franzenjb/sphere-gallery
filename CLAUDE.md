# CLAUDE.md - Franzen App Standard

You are working on a Jeff Franzen / JBF / Red Cross GIS application.

The visual goal is consistent operational craft. A user should recognize the app as Jeff's work: calm, useful, map/data first, Red Cross-aware, and not generic AI output.

## Follow These Rules

0. For a new blank app repo, install `AGENTS.md`, `CLAUDE.md`, and `DESIGN.md` before feature work:
   `node /Users/jefffranzen/dev/franzen-app-standards/scripts/install-app-standard.mjs /path/to/new-repo`
1. Read `DESIGN.md` in this repo. If missing, use `/Users/jefffranzen/dev/franzen-app-standards/DESIGN_SYSTEM.md`.
2. Use only one UI font and one mono font.
3. Use approved logo assets. Do not draw a fake Red Cross logo.
4. Use role-based color tokens. Do not create a new palette.
5. Build the real app/tool first, not a landing page.
6. Keep panels retractable and resizable.
7. Use standard map controls and disable default ArcGIS popups.
8. Hide internal plumbing in public views.
9. Verify contrast, mobile layout, and live behavior.

## Red Cross Map Base Rule

For new Red Cross map apps, start from `/Users/jefffranzen/dev/red-cross-map-base-template` unless Jeff explicitly says otherwise. Preserve the proven `livessaved.jbf.com` map pattern: filters, zoom-to-results behavior, app-owned sidebars, right-sidebar tabs for dense data, disabled default ArcGIS popups, and recognizable Jeff/JBF map-first UX.

## Default Visual Direction

White/light-gray workspace, strong Red Cross red accent, dark readable text, compact controls, restrained cards, data/map-first layout, consistent button styles.

Avoid gradients, decorative blobs, emoji UI, serif display headers, fake logos, and one-off colors.

