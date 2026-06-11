# AGENTS.md - Global Franzen App Standard

Use this file in every Jeff Franzen / JBF / Red Cross GIS app repo.

## Mandatory Design Source

Before changing UI, read the local `DESIGN.md` if present. If it is missing, use:

`/Users/jefffranzen/dev/franzen-app-standards/DESIGN_SYSTEM.md`

Do not invent a new visual identity for each app.

## New Repo Bootstrap

Every new Jeff/JBF/Red Cross app repo must start with these three files before feature work begins:

- `AGENTS.md`
- `CLAUDE.md`
- `DESIGN.md`

Install them with:

```bash
node /Users/jefffranzen/dev/franzen-app-standards/scripts/install-app-standard.mjs /path/to/new-repo
```

Run this immediately after creating or cloning a blank app repo.

## Red Cross Map Base Rule

For new Red Cross map apps, start from `/Users/jefffranzen/dev/red-cross-map-base-template` unless Jeff explicitly says otherwise. It captures the proven `livessaved.jbf.com` map pattern: filters, zoom-to-results behavior, app-owned sidebars, right-sidebar tabs for dense data, disabled default ArcGIS popups, and recognizable Jeff/JBF map-first UX.

## Brand Rules

- Use the approved Red Cross logo asset. Never fake it with a plus sign, emoji, generated SVG, or text-only mark.
- Use one primary UI font and one mono font.
- Use the shared role tokens for red, ink, muted text, borders, canvas, and surface.
- Do not add decorative gradients, orbs, bokeh blobs, or random brand palettes.
- Red is brand/primary/urgent, not a full-page theme.

## Operational UI Rules

- Build the usable tool as the first screen.
- Keep app UI dense, calm, and scannable.
- Side panels must be retractable and resizable.
- Buttons use the shared primary/secondary/ghost/icon styles.
- Cards have 8px radius maximum and are not nested inside other cards.
- All text must have readable contrast.

## Map Rules

- ArcGIS maps: Home and Zoom top-left, Basemap Gallery in Expand bottom-right, Scale bar bottom-left, Search top-right when useful.
- Disable default ArcGIS popups.
- Feature details belong in a formatted app-owned side panel.
- No raw schema fields in public UI.

## Public/Donor-Facing Rules

Hide internal plumbing:

- no item IDs
- no Client IDs
- no raw layer names
- no `Open in ArcGIS`
- no admin/debug badges
- no implementation labels

## AI Drift Checks

Before final response or deploy, scan for:

- more than two font families
- color values outside shared tokens
- fake logo marks
- emojis used as production icons
- default ArcGIS popup behavior
- internal/dev copy in public UI

Run when practical:

```bash
node /Users/jefffranzen/dev/franzen-app-standards/scripts/audit-app-style.mjs .
```

## Continuity & Multi-Agent (mandatory)

Canonical policy: vault note `methods/claude-code-session-handoff.md`.

- **If it isn't in git, the vault, or the project handoff file, it doesn't exist.** Chat dies with the session.
- **Rewrite the project handoff/thread file after every commit or decision**, not just at session end — crashes give no warning.
- **Commit + push every phase.** For substantial builds keep a committed `docs/SPEC_VS_BUILT.md` (or plan/status) so any agent reads the same truth.
- **Two agents (Claude + Codex) on one repo: exactly ONE git owner at a time;** the other is read-only until handed control. Never present a stale doc as current — check its date vs the latest commit.

