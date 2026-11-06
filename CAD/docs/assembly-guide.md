# Robotic Arm Assembly Guide

**14:125:444 Smart Prosthetics and Robotic Systems** — Dr. Adam Gormley

This guide takes you from a pile of printed and bought parts to a complete robotic
arm. Wiring and programming are in a separate guide.

> **Draft status.** All five chapters are written. The gearbox's order follows the
> [design's source article](assembly-1-gearbox.md#where-this-procedure-comes-from). The order of Chapters 2 to 5
> was worked out from the CAD model. All have been checked against the CAD, but none
> has yet been followed step by step on real parts. Anything marked **TO CONFIRM** is
> calculated or assumed, and nothing so far settles it. Each chapter ends with a list of them:
> [gearbox](assembly-1-gearbox.md#open-items-to-confirm), [base](assembly-2-base-joint1.md#open-items-base-and-joint-1),
> [hinge](assembly-3-hinge-joint2.md#open-items-hinge-and-joint-2), [segments](assembly-4-arm-segments.md#open-items-arm-segments),
> [final assembly](assembly-5-final.md#open-items-final-assembly).

**Contents**

1. [Before you start](#before-you-start)
2. [Chapter 1: Planetary gearbox](assembly-1-gearbox.md)
3. [Chapter 2: Base and joint 1](assembly-2-base-joint1.md)
4. [Chapter 3: Hinge and joint 2](assembly-3-hinge-joint2.md)
5. [Chapter 4: Belt-drive arm segments](assembly-4-arm-segments.md)
6. [Chapter 5: Final assembly](assembly-5-final.md)

---

## Before you start

### Reading the pictures

- **Coloured parts** are the ones you're adding in that step. Each part type keeps its
  colour throughout the chapter, and these colours are only for the pictures, not the
  colour your parts will be.
- **Pale grey parts** are already installed.
- **Dashed lines** show where a part goes.
- **Cut-away pictures** show the inside of an assembly with the near half removed.
- Most gearbox pictures stand the gearbox on its output, with the motor end up. When a
  step has you work from the other end, the picture is drawn from below.
- Step numbers run through the whole guide, so Chapter 2 starts at step 16.

The screws, inserts, set screw, belt and pressing tools in the pictures are simplified
shapes. The bought parts are stand-ins too, so yours may look slightly different.

### Tools and supplies

| Item | Used for |
|---|---|
| 2 mm hex key | M3 button head screws and the set screw |
| Long 2 mm ball-end hex key, and a short-armed key | J1 motor screws through the box's window (step 26), hinge screws in the narrow gap (steps 31, 32) and the link screws (steps 50, 51) |
| 2.5 mm hex key | Jack screws (step 45) |
| 3 mm hex key and 8 mm spanner | M5 button head screws and nuts |
| Blocks about 60 mm high | Holding a segment up so that its motor can hang below it (steps 39–47) |
| A second person, or a stand to rest the arm on, and a clamp or weight for the base | Holding the arm up during final assembly (steps 49–52) |
| Small clamp and a flat plate about 60 mm square | Pressing bearings once the hinge is on the base (steps 28, 29), and the pins in a segment (steps 40, 44) |
| Round spacer about Ø24 × 40 mm, such as a socket from a socket set | Pressing the coupling's stub (step 29) |
| Caliper | Setting the 20T pulleys' height (steps 22, 39) |
| Bench vise or arbor press, with a flat scrap to protect the part | Pressing bushings, pins and bearings |
| Flat surface | Checking parts for warping, setting pins flush |
| Soldering iron with an insert tip (PLA parts) | Heat-set inserts |
| J-B Weld slow-cure epoxy, plus a spare greased M3 screw for each insert (resin parts) | Bonded inserts |
| Gear grease (**TO CONFIRM** which type) | Gear teeth |
| Fine sandpaper | Support marks |

Don't use a hammer on printed parts. Press squarely and slowly, and stop if a part
starts to go in crooked.

### Printing

Print the parts from a print set, not from `CAD/STEP/`. See
[Preparing prints](claude-code-guide.md#3-preparing-prints). Each set's `print_list.txt`
is the checklist of what to print. Bought parts are in
[`inventory.md`](../../inventory.md).

**PLA and resin differ only in how the inserts go in** (step 1). Resin is also more
brittle, so press and tighten more gently.
