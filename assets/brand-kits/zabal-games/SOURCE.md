# SOURCE - this kit is a copy, not the original

`assets/brand-kits/zabal-games/` in `zpoidh`.

## Where these files come from

They were copied from **`bettercallzaal/zao-brand`** (private), the canonical
home for every ZAO and ZABAL mark. The ZABAL Gamez kit lives there at
`assets/zabal/zabal-gamez/`; `icon.png` comes from the separate ZABAL kit at
`assets/zabal/zabal/`.

Copied against zao-brand commit **`384c19e`**, verified 2026-09-03 by hashing
every file in this directory against that tree.

## The map

Three files were renamed on the way in. That is the reason a text search for
drift never found them, and it is the single most useful line in this document.

| Here | In zao-brand | Last changed upstream | sha256 (first 16) | State 2026-09-03 |
|---|---|---|---|---|
| `embed-card-gamez.png` | `assets/zabal/zabal-gamez/embed-card-1200x630.png` | `19032e2` | `f4b72b9e0d8b57be` | identical |
| `embed-card.svg` | `assets/zabal/zabal-gamez/embed-card.svg` | `19032e2` | `0c8e621322a2b1bb` | identical |
| `logo.png` | `assets/zabal/zabal-gamez/logo-arcade-hero.png` | `19032e2` | `35f58afcbe9fb148` | identical |
| `logo-gamez.png` | `assets/zabal/zabal-gamez/logo-gamez.png` | `19032e2` | `9e0bd18deb05ed6b` | identical |
| `logo-wordmark.svg` | `assets/zabal/zabal-gamez/logo-wordmark.svg` | `2b1014c` | `c47be9d10b729e7a` | identical |
| `og-card.svg` | `assets/zabal/zabal-gamez/og-card.svg` | `2b1014c` | `1e416ecd76b182be` | identical |
| `palette-arcade.svg` | `assets/zabal/zabal-gamez/palette-arcade.svg` | `19032e2` | `08a4959032c22028` | identical |
| `palette.svg` | `assets/zabal/zabal-gamez/palette.svg` | `f059ad2` | `d508890dbd448815` | identical |
| `icon.png` | `assets/zabal/zabal/zabal-z.png` | `19032e2` | `a893878668fb44ca` | identical |

All nine matched byte for byte at the time of writing. The two SVG wordmarks
matched only after the spelling fix landed here; before that they shipped
`ZABAL GAMES` while zao-brand had been corrected.

## Not from zao-brand

`README.md`, `asset-inventory.md`, `index.html`, `phrases.md` and the audio
files are local to this repo. Nothing upstream owns them, so nothing upstream
will update them.

## The rule

**Fix upstream first, then copy down.** A correction made only here reaches one
repo and quietly diverges from every other copy.

`ZABAL GAMES` was fixed three separate times and kept shipping, because each fix
landed in one copy and no copy knew where it came from. Three rasters
(`logo-arcade-hero.png` / `logo.png`, `logo-gamez.png`,
`embed-card-1200x630.png` / `embed-card-gamez.png`) still have the wrong
spelling baked into the artwork; that needs a designer, not an edit, and it is
tracked upstream.

A grep will not catch the next one either: `ZABAL <tspan>GAMES</tspan>` does not
contain the string `ZABAL GAMES`. Hash, do not search.

## Check for drift

With `zao-brand` cloned beside this repo:

```sh
Z=~/Documents/zao-brand/assets
for pair in \
  "embed-card-gamez.png:zabal/zabal-gamez/embed-card-1200x630.png" \
  "embed-card.svg:zabal/zabal-gamez/embed-card.svg" \
  "logo.png:zabal/zabal-gamez/logo-arcade-hero.png" \
  "logo-gamez.png:zabal/zabal-gamez/logo-gamez.png" \
  "logo-wordmark.svg:zabal/zabal-gamez/logo-wordmark.svg" \
  "og-card.svg:zabal/zabal-gamez/og-card.svg" \
  "palette-arcade.svg:zabal/zabal-gamez/palette-arcade.svg" \
  "palette.svg:zabal/zabal-gamez/palette.svg" \
  "icon.png:zabal/zabal/zabal-z.png"; do
  here="${pair%%:*}"; there="$Z/${pair#*:}"
  a=$(shasum -a256 "$here" | cut -d' ' -f1)
  b=$(shasum -a256 "$there" | cut -d' ' -f1)
  [ "$a" = "$b" ] && echo "ok      $here" || echo "DRIFTED $here"
done
```

Anything that prints `DRIFTED` is a decision, not a bug: either upstream moved
and this copy is stale, or someone edited here and upstream never learned.
