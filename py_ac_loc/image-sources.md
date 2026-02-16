# Image Sources for Line-Break Editors

## Source

All page images come from the Internet Archive scan of the Aleppo Codex:

- **Item:** <https://archive.org/details/aleppo-codex>
- **Server:** `ia601801.us.archive.org`

## API

Images are fetched via the BookReader image API:

```
https://ia601801.us.archive.org/BookReader/BookReaderImages.php
  ?zip=/7/items/aleppo-codex/Aleppo%20Codex_jp2.zip
  &file=Aleppo%20Codex_jp2/Aleppo%20Codex_{NNNN}.jp2
  &id=aleppo-codex
  &scale=2
  &rotate=0
```

where `{NNNN}` is a zero-padded 4-digit page index (see below).

## Leaf-to-page-index formula

For a codex leaf like `270r`:

```
page_index = (leaf_number - 1) * 2 + 2 + (0 if recto else 1)
```

Examples: `270r` → `(270-1)*2+2+0` = `540`, `270v` → `541`.

## Pages used (270r–281v)

| Leaf  | Page index | `{NNNN}` |
|-------|-----------|----------|
| 270r  | 540       | 0540     |
| 270v  | 541       | 0541     |
| 271r  | 542       | 0542     |
| 271v  | 543       | 0543     |
| 272r  | 544       | 0544     |
| 272v  | 545       | 0545     |
| 273r  | 546       | 0546     |
| 273v  | 547       | 0547     |
| 274r  | 548       | 0548     |
| 274v  | 549       | 0549     |
| 275r  | 550       | 0550     |
| 275v  | 551       | 0551     |
| 276r  | 552       | 0552     |
| 276v  | 553       | 0553     |
| 277r  | 554       | 0554     |
| 277v  | 555       | 0555     |
| 278r  | 556       | 0556     |
| 278v  | 557       | 0557     |
| 279r  | 558       | 0558     |
| 279v  | 559       | 0559     |
| 280r  | 560       | 0560     |
| 280v  | 561       | 0561     |
| 281r  | 562       | 0562     |
| 281v  | 563       | 0563     |
