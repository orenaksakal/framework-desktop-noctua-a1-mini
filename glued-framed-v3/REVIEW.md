# V3.1 review

## Fixed

- **Thin lap backing:** the V3 female recess began at 0.40 mm while the exterior channel reached 0.24 mm, leaving only 0.16 mm of backing locally. It now begins at 1.00 mm, preserving 0.76 mm. The lip overlap is reduced from 1.4 to 0.8 mm to keep its 45-degree underside and original inner envelope.
- **Incomplete thickness validation:** the old CAD check preserved only a 0.25–0.39 mm slice. The new check preserves the complete original 0.24–1.00 mm slice. A regression check confirms the original recess fails. Exported STLs are also transformed back into assembly coordinates and checked for backing loss and overlap within recorded numerical tolerances.
- **Limited appearance test:** the original coupon had only the glued seam. The revised coupon also includes an unbroken decorative groove from the actual panel border for direct comparison.
- **Stale verification risk:** the slicer clears its own old G-code before running. The renderer requires a complete receipt set and checks STL and G-code hashes; it handles both relative and absolute extrusion modes. Packaging requires matching geometry/slicing/toolpath receipts.
- **Revision ambiguity:** the new download is explicitly V3.1. The old V3 ZIP alias is refreshed to the corrected contents. Existing downloaded V3 files must be replaced; initial V3 panel parts must not be mixed with V3.1.

## Verified

Geometry and assembly-path checks passed. All six STL files sliced successfully for the A1 mini. The 4-piece test estimates 21m33s / 3.79 g using the recorded PETG HF profile. Preview images were inspected. Original V1 keys and duct remain usable. No additional inner thickness is introduced.

## Still requires a physical sample

Printed groove consistency, PETG dimensional fit, glue strength, long-term durability, case fit and cooling/acoustic performance. Geometry checks are not material-strength tests.
