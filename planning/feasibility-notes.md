# Noctua Framework Desktop / A1 mini split feasibility

Measured from the existing Noctua-named STL files in Downloads on 2026-09-07. File names match the official listing; identity has not been verified against a fresh download checksum.

This is a measured design proposal, not a print-ready remix. Joint design, slicing, mounting clearances and physical thermal/acoustic testing remain outstanding.

Panel: 215.65 × 200.40 mm, maximum depth 6.95 mm. Duct: 129 × 129 × 8.2 mm.

Diagram coordinates: u = STL X + 233.552948; v = 185.258667 - STL Z. Depth is STL Y.

- A: u <= 45 mm. Rotated 45 degrees, its clipped mesh footprint is 171.521 × 171.441 mm.
- B: u >= 45 mm and v <= 35 mm. Footprint 170.650 × 35.000 mm.
- C: u >= 45 mm and v >= 35 mm. Footprint 170.650 × 165.400 mm. Entire main grille remains intact.
- Original duct fits whole when laid on its 129 × 129 mm plane.

Footprints exclude connectors, supports, brim and slicer exclusion zones. No scaling is needed. Approximately 2–3 mm brim appears feasible; check final geometry in the slicer.

Preserve the complete grille, duct funnel, duct height and mounting interfaces. Use concealed alignment and recessed reinforcement in solid panel areas, with adhesive suitable for the chosen material. Verify local skin thickness: the maximum depth includes mounting features and is not the panel skin thickness. Do not obstruct the duct or case mounting paths. Seal unintended joint gaps and prevent rattling.

Use one spool and consistent exterior texture for a cohesive finish. Flush joints still leave hairline seams. A near-seamless finish needs filling, sanding and compatible paint, masking vents and mating surfaces. Diagram colors only identify parts.

PETG is the practical A1 mini starting point, subject to verifying actual printed-part temperature and creep, especially for the duct. Suggested prototype settings: 0.4 mm nozzle, 0.16–0.20 mm layers and 3–4 walls where geometry permits. Follow the material maker's drying/printing instructions. Inspect thin grille paths and first-layer expansion. PLA is preferable for fit prototypes rather than the final heated enclosure parts.

Compare stock and modified configurations at equal room temperature, workload and power settings. Check temperatures, fan RPM, performance/throttling, acoustic character, joint rattles and deformation after sustained workloads. Preserving vent geometry supports an expectation of retained benefits; it does not establish identical measured performance.

## Attribution and sources

Original panel geometry by Noctua_at / Noctua. The diagram is an annotated projection with proposed split locations added. Original panel and derived diagram: CC BY-NC-SA 4.0, https://creativecommons.org/licenses/by-nc-sa/4.0/

- Article: https://www.noctua.at/en/expertise/blog/how-to-make-the-framework-desktop-run-even-quieter
- Original panel and editable STP: https://www.printables.com/model/1368247-framework-destktop-side-panel-with-noctua-style-fa/files
- Original duct: https://www.printables.com/model/1368249-framework-desktop-custom-fan-duct
- Printer: https://us.store.bambulab.com/products/a1-mini
