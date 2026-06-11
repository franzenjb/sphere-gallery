# DESIGN.md — sphere-gallery

This app follows the Franzen App Standard.

Canonical standard:

`/Users/jefffranzen/dev/franzen-app-standards/DESIGN_SYSTEM.md`

## App Identity

- Operational Red Cross / GIS / data tool.
- Calm, scannable, practical.
- Map/data/workflow first.
- No generic AI styling.

## Required Tokens

Use:

```css
@import "./brand-system.css";
```

or copy the relevant tokens from `templates/brand-system.css`.

## Red Cross Map Base

For new Red Cross map apps, start from `/Users/jefffranzen/dev/red-cross-map-base-template` unless Jeff explicitly says otherwise. Preserve the proven `livessaved.jbf.com` filters, zoom behavior, sidebars, and right-sidebar tab model.

## Required Checks

- Approved logo asset used.
- Max two font families.
- Shared color tokens used.
- Buttons match shared styles.
- Sidebars retractable and resizable.
- Map controls match standard.
- Default ArcGIS popups disabled.
- Public views hide internal plumbing.
- Contrast checked.

