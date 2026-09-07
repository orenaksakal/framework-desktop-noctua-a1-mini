# Noctua panel for Bambu Lab A1 mini

Three panel pieces, eight recessed glue-in keys, and the original one-piece duct. All STL files are in millimetres and already oriented for printing. Use 100% scale. Designed for a 0.4 mm nozzle and PETG.

These files have passed mesh and Bambu Studio slicing checks. They have not been physically printed or fitted to your Framework Desktop. Print the small joint test first, and check mounting and G2 duct clearance before bonding or running sustained loads.

## What to print

| Order | STL | Quantity | Purpose |
|---|---|---:|---|
| First | `00_PRINT_FIRST_joint_test.stl` | 1 | Two pieces copied from the actual panel seam and one standard key |
| Then | `01_panel_A_logo_strip.stl` | 1 | Logo strip, already rotated diagonally to fit |
| | `02_panel_B_upper_strip.stl` | 1 | Upper strip |
| | `03_panel_C_main_grille.stl` | 1 | Main panel with the complete original grille |
| | `04_duct_whole.stl` | 1 | Original Noctua duct, rotated flange-down |
| | `05_keys_standard_PRINT_ONCE_8_keys.stl` | 1 | All eight standard keys in one file; do not print eight copies |

Each row fits on one A1 mini plate. Print each file as a separate job. When importing the test or key set, keep the components together at their existing positions; they are separate physical pieces intentionally.

The `optional_keys` folder contains single alternative keys. Use the **loose 0.30 mm** key if the standard test key will not seat after removing first-layer flare. Use the **snug 0.10 mm** key if the standard key is excessively loose. Print one alternative to test, then eight for the panel if needed. Do not scale the panel or key to adjust fit.

## Bambu Studio settings

1. Select **Bambu Lab A1 mini**, **0.4 mm nozzle**, and your actual PETG filament profile. The verification used **Bambu PETG HF @BBL A1M** and the **Textured PEI Plate**.
2. Import one STL at a time. Keep its supplied orientation. Do not use automatic orientation or mirror. In-plane rotation/arrangement is fine as long as the entire part, supports and brim stay on the plate. The A strip is already diagonal.
3. Begin with **0.16 mm Optimal** and set the following overrides:

| Setting | Value used for verification |
|---|---|
| First layer height | 0.20 mm |
| Walls | 4 |
| Top / bottom shell layers | 5 / 5 |
| Infill | 20% gyroid |
| Outer / inner wall speed | 45 / 80 mm/s |
| First layer / first layer infill speed | 20 / 30 mm/s |
| Elephant-foot compensation | 0.15 mm |
| Brim | Outer only, 2 mm wide, 0.15 mm object gap |
| Supports | Enabled, normal auto, 30° threshold |
| Support on build plate only | Off |
| Support top Z distance | 0.20 mm |
| Support/object XY distance | 0.35 mm |
| Print sequence | By layer |
| Prime tower | Off |

The automatic supports are mainly for original mounting details. Pockets open upward and do not need support inside them. Inspect the preview before printing. Do not enlarge the brim on the A strip without checking the available space. Cool the plate before carefully removing the thin grille and the 0.8 mm keys.

The panel's exterior is against the plate. Using the same spool and plate surface for A, B and C gives a consistent finish. The duct's broad flange is against the plate.

Dry the PETG according to the manufacturer. Bambu specifies 65°C for eight hours in a suitable dryer for PETG HF. These slicer settings are a verified starting point, not a replacement for selecting/calibrating your actual filament.

## Joint test

1. Print `00_PRINT_FIRST_joint_test.stl` in the PETG you will use for the panel. PLA can check the concept but does not establish PETG tolerances.
2. Remove brim, support and any first-layer flare. Put the two coupon pieces exterior-down on a flat surface and bring their cut edges together. The two half-pockets form one butterfly-shaped recess.
3. Seat the test key from the back. It should drop into the recess with gentle finger pressure and a little room for adhesive. Do not force it or bend the skin. The key is recessed below the surrounding inner surface.
4. Bond this test joint with the adhesive you intend to use, let it fully cure according to its instructions, and check the seam alignment and bond before making the full panel.

The standard key has 0.20 mm clearance around its outline. The pockets leave 1.0 mm of continuous exterior skin. Keys are 0.8 mm thick. They are not snap-fit fasteners: adhesive retains them.

## Assemble the panel

Refer to `assembly-guide.png`.

1. Remove all support, brim and stringing. Check that every vent and mounting feature is clear.
2. Dry-fit the three panel pieces and the duct to the case, with the computer powered off and unplugged. Check the G2 fan/duct seating and make sure nothing touches the blades. Temporarily align the panel with removable tape if needed; do not force the original mounting features.
3. Remove the parts from the computer. Place all three exterior faces down on one flat, protected surface. Align the two seams and the panel perimeter. Close the seams without introducing a step in the exterior.
4. Lightly prepare the pocket mating surfaces as directed by the adhesive maker. Use adhesive suitable for PETG. Medium-viscosity cyanoacrylate is an option; a PETG-compatible two-part epoxy is another. The small joint test determines whether your particular adhesive and surface preparation work.
5. Apply a small amount inside each pocket and to the mating seam edges as appropriate. Seat all **eight** keys: five along the A seam, three between B and C. Keep the panel flat throughout curing. Prevent adhesive from reaching the visible face, vents or case mounting features.
6. Let the adhesive cure fully outside the computer. Check that all keys are retained, the panel is flat and the seams do not flex or rattle. Remove loose material before installing.
7. Install the panel and duct. Compare temperatures, fan speed and performance with the stock configuration under the same workloads and room conditions. Check for joint vibration and heat deformation.

The finished panel removes as one bonded assembly. No added screws or fasteners are required. Hairline seams remain visible unless filled and refinished. The keys stay within the original panel envelope; do not add thick backing strips over them.

## Time and material estimates

Bambu Studio 2.7.1.62 estimated approximately **119 g and 6 h 22 min total**, including the small joint test and six separate job startup cycles. Actual consumption/time depends on your profile, supports, calibration, purge and filament. One 1 kg spool is ample.

## What was checked

- Every exported STL was reloaded and checked for watertightness, consistent winding, positive volume and expected solid count.
- A, B, C and the duct are one solid each. The key set has eight solids; the test has three.
- The three panels reassemble to the pocketed source without missing cut-plane volume.
- The first 0.9 mm of the exterior and the entire main grille region are unchanged.
- Mounting geometry deeper than 2.81 mm from the exterior is unchanged. Local skin/rib material is removed only for the recessed pockets.
- Keys fit geometrically without penetrating the remaining panel or extending outside the original solid envelope.
- Export transforms preserve handedness: the panel and duct have not been mirrored.
- All six main files sliced successfully with an A1 mini profile. Model/support/brim extrusion paths, including arcs, stayed inside the 180 × 180 mm bed. `slicer-preview.png` shows the first layers.

The slicer recovered from one Voronoi warning while processing the main grille; it returned success and produced complete toolpaths. This is recorded in `slicing-validation.json`. No physical fit, joint-strength, long-term creep, G2 compatibility or acoustic/thermal equivalence test has been performed. The duct geometry is Noctua's original and has not been customised to the G2.

## Sources and license

Original panel and duct: **Noctua_at / Noctua**. Remix changes: three-way panel split, eight recessed key pockets, eight separate butterfly keys, joint-test parts and print orientations. Grille and duct flow geometry retained.

- Panel: https://www.printables.com/model/1368247-framework-destktop-side-panel-with-noctua-style-fa/files
- Duct: https://www.printables.com/model/1368249-framework-desktop-custom-fan-duct
- Noctua article: https://www.noctua.at/en/expertise/blog/how-to-make-the-framework-desktop-run-even-quieter
- A1 mini: https://us.store.bambulab.com/products/a1-mini
- PETG HF: https://eu.store.bambulab.com/en-mt/products/petg-hf
- Adhesive background: https://blog.prusa3d.com/the-great-guide-to-gluing-and-assembling-3d-prints_44908/

Distributed under **Creative Commons Attribution–NonCommercial–ShareAlike 4.0**: https://creativecommons.org/licenses/by-nc-sa/4.0/ . Retain attribution and this license when sharing the remix. This is an independent, unendorsed remix, not an official Noctua or Framework replacement part.

The build used the Noctua-named source STLs already present in Downloads; source hashes are in `validation.json`. The supplied files were not compared by checksum against fresh downloads.
