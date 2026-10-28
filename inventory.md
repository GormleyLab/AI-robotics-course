# Smart Prosthetics and Robotic Systems — Parts Inventory

**Course:** 14:125:444  
**Instructor:** Dr. Adam Gormley

---

Purchased parts for the robotic arm and the Phase 1 motors module. Source: the Amazon Business order history from 10/27/2025 to 10/27/2026, which covers the Spring 2026 offering. Cancelled lines are left out. **Bought** is the total number of units from all orders (packs × pack size). It is what was purchased, not what is left: count the stock and fill in **On hand** before reordering.

**Sizing.** Spring 2026 had 20 students. There were 4 teams of 5, and team items were bought for one extra set in case something broke (5 webcams, 5 Arduino cases, 5 USB hubs). Spring 2027 has 40 students: 8 teams of 5, plus one spare, makes **9 sets**. **Per arm** comes from the CAD parts lists ([`CAD/docs/design.md`](CAD/docs/design.md) §2–§4 and [`CAD/src/README.md`](CAD/src/README.md)): base and J1, the J2 gearbox, and two belt-drive segments (J3, J4). **9 sets** is per arm × 9, so the spare set is already included. For fasteners and inserts, also allow a full extra pack, because students strip, lose and mis-insert them.

General-lab purchases in the same order history are left out. §6 lists spare parts that were bought for the course but are not used in the current CAD.

## 1. Arm: motors and drive

| Item | ASIN | Bought | Spent | CAD part / use | Per arm | 9 sets | On hand |
|---|---|---|---|---|---|---|---|
| STEPPERONLINE NEMA17 2 A, 84 oz·in, 48 mm body (5-pack) | [B00QEYADRQ](https://www.amazon.com/dp/B00QEYADRQ) | 5 packs = **25** | $274.95 | `purchased/nema17.py`: J1, J2, J3 | 3 | 27 | |
| STEPPERONLINE NEMA17 2 A, 48 mm, with 1 m cable (single) | [B00PNEQKC0](https://www.amazon.com/dp/B00PNEQKC0) | **4** | $55.80 | Same motor, ordered singly (spares) | — | — | |
| STEPPERONLINE NEMA17 pancake, 1 A, 16 N·cm, 20 mm body (5-pack) | [B091YDBK1S](https://www.amazon.com/dp/B091YDBK1S) | 3 packs = **15** | $118.50 | J4 motor on segment 2: it's lighter, and J4 needs less torque. The CAD still models segment 2 with the full-size `purchased/nema17.py` | 1 | 9 | |
| WINSINN GT2 20T pulley, 5 mm bore, 6 mm belt (5-pack) | [B077GNZK3J](https://www.amazon.com/dp/B077GNZK3J) | 4 packs = **20** | $23.52 | `purchased/gt2_pulley_20t.py`: motor pulleys (J1, J3, J4) | 3 | 27 | |
| WINSINN GT2 20T idler, 5 mm bore (5-pack) | [B07BPGYX3G](https://www.amazon.com/dp/B07BPGYX3G) | 6 packs = **30** | $47.28 | `purchased/gt2_idler_20t.py`: arm idlers, 2 per segment | 4 | 36 | |
| Zeelo GT2 6 mm closed belt, 280 mm (10-pack) | [B0CQP4F56W](https://www.amazon.com/dp/B0CQP4F56W) | 2 packs = **20** | $29.98 | Segment belts, 2 per segment (274.4 mm loop, design.md §4) | 4 | 36 | |
| Zeelo GT2 6 mm closed belt, 320 mm (10-pack) | [B0CQP2D8FG](https://www.amazon.com/dp/B0CQP2D8FG) | 1 pack = **10** | $14.99 | Not a CAD length: probably J1 trials | — | — | |
| Zeelo GT2 6 mm closed belt, 350 mm (10-pack) | [B0CQNZBJLT](https://www.amazon.com/dp/B0CQNZBJLT) | 1 pack = **10** | $15.99 | J1 belt (Spring 2026 build; see note) | 1 | 9 | |
| Zeelo GT2 6 mm closed belt, 500 mm (4-pack) | [B0CQP1DT4C](https://www.amazon.com/dp/B0CQP1DT4C) | **4** | $14.99 | Not in CAD | — | — | |
| Zeelo GT2 6 mm closed belt, 760 mm (4-pack) | [B0CQP1N4YL](https://www.amazon.com/dp/B0CQP1N4YL) | **4** | $14.99 | Not in CAD | — | — | |
| uxcell GT2 6 mm closed belt, 600 mm (2-pack) | [B0CMTB5WHD](https://www.amazon.com/dp/B0CMTB5WHD) | **2** | $7.68 | Not in CAD | — | — | |

**J1 belt.** The recreated base needs a **370–372 mm** loop (design.md §2: the motor then sits at x ≥ 158.0 and J1 clears ±124°). No belt in that range was bought. A 350 mm loop fits the slot, but the motor sits nearer the hinge and J1 travel is reduced (I‑14). Order 370 mm loops (185 T) for Spring 2027.

> **To order:** GT2 6 mm closed belt, **370 mm** (185 T, `370-2GT-6`), **9** (1 per set). These Amazon listings include a 370 mm × 6 mm option. The size is chosen on the product page, so check that 370 mm and 6 mm width are selected before buying:
> - [B0H152X8XD](https://www.amazon.com/dp/B0H152X8XD): 2GT/GT2 timing belt, 276–370 mm, 6 mm width, **10-pack**. This covers all 9 sets with one order.
> - [B0DWKCJ6DJ](https://www.amazon.com/dp/B0DWKCJ6DJ): GT2 timing belt, 350–380 mm, 6 mm width, sold singly.
> - [B0H338VH6R](https://www.amazon.com/dp/B0H338VH6R): GT2 closed loop, 360–380 mm in 2 mm steps, 6 mm width.
>
> A 372 mm belt also gives full J1 travel if 370 mm is out of stock. 366 and 368 mm belts fit, but J1 travel drops to ±122° and ±123° with the 48 mm motor (design.md I‑19).

## 2. Arm: bearings, pins and bushings

| Item | ASIN | Bought | Spent | CAD part / use | Per arm | 9 sets | On hand |
|---|---|---|---|---|---|---|---|
| uxcell 51108 thrust bearing 40×60×13 (2-pack) | [B07G829LM8](https://www.amazon.com/dp/B07G829LM8) | 8 packs = **16** | $77.74 | `purchased/thrust_bearing_51108.py`: J1 (×2) | 2 | 18 | |
| uxcell 6807-2RS 35×47×7 (10-pack) | [B0D54LH4KK](https://www.amazon.com/dp/B0D54LH4KK) | **10** | $15.69 | `purchased/bearing_6807.py`: box top (J1) | 1 | 9 | |
| uxcell 608-2RS 8×22×7 (8-pack) | [B07FDWW9D9](https://www.amazon.com/dp/B07FDWW9D9) | 2 packs = **16** | $13.54 | `purchased/bearing_608.py`: J1 pulley hub (box bottom) | 1 | 9 | |
| uxcell 6805-2RS 25×37×7 (10-pack) | [B082PYT33D](https://www.amazon.com/dp/B082PYT33D) | 7 packs = **70** | $87.62 | `purchased/bearing_6805.py`: hinge (×2), gearbox front cover, arm J3 (×2 per segment) | 7 | 63 | |
| uxcell 6801-2RS 12×21×5 (10-pack) | [B07FVYHWFC](https://www.amazon.com/dp/B07FVYHWFC) | 2 packs = **20** | $18.16 | `purchased/bearing_6801.py`: gearbox (×2) | 2 | 18 | |
| uxcell 6803-2RS 17×26×5 (5-pack) | [B07TRQ1YZ1](https://www.amazon.com/dp/B07TRQ1YZ1) | 6 packs = **30** | $45.88 | `purchased/bearing_6803.py`: gearbox back cover | 1 | 9 | |
| uxcell sleeve bushing 6×8×10 (10-pack) | [B07SHSN6NP](https://www.amazon.com/dp/B07SHSN6NP) | 12 packs = **120** | $60.25 | `purchased/bushing_6x8x10.py`: planets (×6), dual pulley (×2 per segment) | 10 | 90 | |
| uxcell 6×22 mm dowel pin, 304 SS (30-pack) | [B0F3JMXNGV](https://www.amazon.com/dp/B0F3JMXNGV) | 3 packs = **90** | $24.07 | `purchased/planet_pin_6x22.py`: planet pins (×6) | 6 | 54 | |
| uxcell 6×30 mm dowel pin, 304 SS (30-pack) | [B0F3JRPFSB](https://www.amazon.com/dp/B0F3JRPFSB) | 3 packs = **90** | $27.60 | `purchased/dowel_pin_6x30.py`: dual-pulley axle (×1 per segment) | 2 | 18 | |
| M6 flat washer, 6×12×1.5, 304 SS (200-pack) | [B07X14TGFX](https://www.amazon.com/dp/B07X14TGFX) | **200** | $9.46 | `purchased/washer_6.py`: 2 per planet (CAD stand-in 6.2×11.8×1.3) | 12 | 108 | |

The 6×30 dowels were bought for the Fusion design, which also used them as idler axles (3 per segment). The recreation uses M5 × 40 screws for the idlers (I‑5), so 2 dowels per arm are enough.

## 3. Arm: fasteners and threaded inserts (consumables)

Per-arm counts are approximate: design.md does not record every screw length (§2 "M5 bolts + inserts, M3 screws: lengths not recorded").

| Item | ASIN | Bought | Spent | CAD part / use | Per arm | 9 sets | On hand |
|---|---|---|---|---|---|---|---|
| ruthex M3 × 5.7 heat-set insert (100-pack) | [B08BCRZZS3](https://www.amazon.com/dp/B08BCRZZS3) | 6 packs = **600** | $58.44 | `FIT.insert_m3`: ring gear (12), back cover (4), carrier plates (6), Wall (9 per segment), Base/Top proximal (4 per segment) | ~48 | ~432 | |
| ruthex M5 × 9.5 heat-set insert (50-pack) | [B07YSVXWS8](https://www.amazon.com/dp/B07YSVXWS8) | **50** | $9.99 | `FIT.insert_m5`: box bottom (7) | 7 | 63 | |
| FFVRVSS brass insert assortment M2–M5 (328 pc) with heat-set tool | [B0FH4JQ3VB](https://www.amazon.com/dp/B0FH4JQ3VB) | 1 kit | $6.92 | Insert tips for soldering irons; spare inserts | — | — | |
| iexcell M3 × 8 button head, 12.9 (100-pack) | [B0CP4B16KF](https://www.amazon.com/dp/B0CP4B16KF) | 2 packs = **200** | $17.72 | M3 screws (lengths not recorded) | ~75 M3 screws in total, mixed lengths: motors (4 × 4), gearbox covers, mount and carriers (~22), segment plates (14 per segment), link interfaces (4 × 3) | ~675 | |
| iexcell M3 × 10 button head, 12.9 (100-pack) | [B0CP4BLD7Z](https://www.amazon.com/dp/B0CP4BLD7Z) | **100** | $8.86 | ″ | ″ | ″ | |
| iexcell M3 × 12 button head, 12.9 (100-pack) | [B0CP4B65CC](https://www.amazon.com/dp/B0CP4B65CC) | 2 packs = **200** | $17.72 | ″ | ″ | ″ | |
| iexcell M3 × 16 button head, 12.9 (100-pack) | [B0CP48RN8K](https://www.amazon.com/dp/B0CP48RN8K) | 2 packs = **200** | $17.92 | ″ | ″ | ″ | |
| Kadrick M3 assortment, 4–35 mm, with nuts and washers (2240 pc) | [B0CQNN6NY3](https://www.amazon.com/dp/B0CQNN6NY3) | 1 kit | $22.99 | Includes M3 × 35 for the idler jack screws (`purchased/socket_head_m3x35.py`, 2 per segment) | 4 × M3 × 35 | 36 | |
| M5 × 40 button head, black oxide SS (25-pack) | [B0GJJBQDCD](https://www.amazon.com/dp/B0GJJBQDCD) | 2 packs = **50** | $17.36 | `purchased/button_head_m5x40.py`: idler axles (2 per segment) | 4 | 36 | |
| M5 × 45 button head (25-pack) | [B0GJJKXJG5](https://www.amazon.com/dp/B0GJJKXJG5) | **25** | $8.68 | Probably the J1 pulley–hinge clamp (4 × M5, length not recorded) | 4? | 36? | |
| M5 × 50 button head (25-pack) | [B0GJJDKQLZ](https://www.amazon.com/dp/B0GJJDKQLZ) | **25** | $8.68 | ″ | ″ | ″ | |
| Kadrick M5 assortment, 8–40 mm, with nuts and washers (960 pc) | [B0DRCBVH8K](https://www.amazon.com/dp/B0DRCBVH8K) | 1 kit | $22.99 | Box top–bottom screws (7), M5 nuts for the idler axles (`purchased/hex_nut_m5.py`, 2 per segment) | 7 screws + 4 nuts | 63 + 36 | |
| ZDingTech M4 × 5 set screw (110-pack) | [B0CF299SDT](https://www.amazon.com/dp/B0CF299SDT) | **110** | $6.69 | Probably the gearbox input-shaft set screw (Ø4 cross hole) | 1 | 9 | |
| 304 SS flat washer assortment M2–M12 (1100 pc) | [B0DZ5H9T4Z](https://www.amazon.com/dp/B0DZ5H9T4Z) | 1 kit | $6.99 | General | — | — | |

## 4. Electronics

The handout ([`arduino_motor_control_handout.md`](arduino_motor_control_handout.md)) uses an A4988 driver, a NEMA17, an MG996R servo, a limit switch and a potentiometer.

| Item | ASIN | Bought | Spent | Use | Per arm | 9 sets | On hand |
|---|---|---|---|---|---|---|---|
| **Arduino Uno Q** | — | Bought from the Arduino store, not Amazon: *quantity to be filled in* | | Controller | 1 | 9 | |
| ACEIRMC CNC Shield V3 kit with 4 × A4988 and heat sinks | [B07TT3C3HB](https://www.amazon.com/dp/B07TT3C3HB) | 6 kits (6 shields, **24** A4988) | $58.14 | Drives the 4 steppers (UNO header). Check that it fits the Uno Q | 1 | 9 | |
| HiLetgo A4988 driver with heat sink (5-pack) | [B07BND65C8](https://www.amazon.com/dp/B07BND65C8) | 3 packs = **15** | $29.04 | Phase 1 breadboard wiring; spares for the shields | — | — | |
| MG996R metal-gear servo (6-pack) | [B0BMM1G74B](https://www.amazon.com/dp/B0BMM1G74B) | **6** | $26.98 | Handout `SERVO_PIN`; gripper/end effector | 1 | 9 | |
| SG90 9 g micro servo (5-pack) | [B0BJQ2QTHG](https://www.amazon.com/dp/B0BJQ2QTHG) | **5** | $9.98 | Light-duty servo (handout §2 table) | — | — | |
| URBEST roller-lever micro switch, SPDT (10-pack) | [B00MFRMFS6](https://www.amazon.com/dp/B00MFRMFS6) | 4 packs = **40** | $27.96 | Handout `LIMIT_SWITCH_PIN`; joint homing | 4 | 36 | |
| Flutesan 10 kΩ trim potentiometer with knob (12 pc) | [B09G9TBY38](https://www.amazon.com/dp/B09G9TBY38) | **12** | $7.99 | Handout `POT_PIN` | 1 | 9 | |
| Geekworm UNO case, clear ABS | [B01C8500L8](https://www.amazon.com/dp/B01C8500L8) | **5** | $25.00 | Controller enclosure | 1 | 9 | |
| NexiGo N60 1080p webcam | [B088TSR6YJ](https://www.amazon.com/dp/B088TSR6YJ) | **5** | $124.95 | Machine vision (Phase 3) | 1 | 9 | |
| UGREEN Revodok 105 USB-C hub, 5-in-1 | [B0BR3M8XHK](https://www.amazon.com/dp/B0BR3M8XHK) | **6** | $79.89 | Laptop: webcam + Arduino | 1 | 9 | |
| TAKAGI USB-A to USB-C cable, 6 ft (3-pack) | [B07SMNZK8H](https://www.amazon.com/dp/B07SMNZK8H) | 4 packs = **12** | $36.96 | Uno Q programming (USB-C) | 1 | 9 | |
| USB-C 20 W charger block (4-pack) | [B0B2WLSY9D](https://www.amazon.com/dp/B0B2WLSY9D) | **4** | $9.98 | Probably powers the Uno Q off-laptop | — | — | |
| ELEGOO 400-point breadboard (6-pack) | [B0CYPVMK9J](https://www.amazon.com/dp/B0CYPVMK9J) | 2 packs = **12** | $15.88 | Phase 1 wiring | 1 | 9 | |
| MCIGICM 830-point breadboard (10-pack) | [B07H9X7XVN](https://www.amazon.com/dp/B07H9X7XVN) | **10** | $19.99 | Phase 1 wiring | 1 | 9 | |
| EDGELEC jumper wires M–F, 20 cm (120 pc) | [B07GD2BWPY](https://www.amazon.com/dp/B07GD2BWPY) | 2 packs | $12.86 | Wiring | — | — | |
| EDGELEC jumper wires M–M, 20 cm (120 pc) | [B07GD3JVHD](https://www.amazon.com/dp/B07GD3JVHD) | 1 pack | $7.98 | Wiring | — | — | |
| ELEGOO Dupont jumper kit M–F / M–M / F–F (120 pc) | [B01EV70C78](https://www.amazon.com/dp/B01EV70C78) | 1 pack | $6.88 | Wiring | — | — | |
| TUOFENG 22 AWG solid hookup wire, 6 colors × 30 ft | [B07TX6BX47](https://www.amazon.com/dp/B07TX6BX47) | 1 | $15.10 | Wiring | — | — | |
| 4-conductor 22 AWG cable, 40 ft | [B0793NGKL9](https://www.amazon.com/dp/B0793NGKL9) | 1 | $14.98 | Stepper lead extensions up the arm | — | — | |
| DaFuRui 4-pin 5.08 mm pluggable screw terminal (15 pairs) | [B0C2Y3VSVB](https://www.amazon.com/dp/B0C2Y3VSVB) | **15** | $16.99 | Motor connectors | — | — | |
| Goupchn banana plug to breadboard leads | [B08KZKGWTJ](https://www.amazon.com/dp/B08KZKGWTJ) | 2 | $17.62 | Bench supply to breadboard | — | — | |
| BOJACK resistor kit, 25 values (1000 pc) | [B08FD1XVL6](https://www.amazon.com/dp/B08FD1XVL6) | 1 kit | $9.89 | LEDs, pull-ups | — | — | |

**Provided by the department (not ordered):** the **12 V motor supplies** (the handout calls for 12 V, 2 A minimum) and **PLA filament**.

## 5. Tools (reusable)

| Item | ASIN | Bought | Spent | Notes |
|---|---|---|---|---|
| Bondhus 10686 ball-end hex screwdriver set, 1.5–5 mm | [B0006O4AD8](https://www.amazon.com/dp/B0006O4AD8) | **5** sets | $84.20 | 1 per team plus a spare: 9 sets needed, so buy 4 more |
| AstroAI digital multimeter | [B01ISAMUA6](https://www.amazon.com/dp/B01ISAMUA6) | 1 | $13.95 | |
| Adoric 6" digital caliper | [B07DFFYCXS](https://www.amazon.com/dp/B07DFFYCXS) | 1 | $6.99 | |
| NSZETZ precision screwdriver set, 11 pc | [B08ZS76VDG](https://www.amazon.com/dp/B08ZS76VDG) | 1 | $7.59 | A4988 current-limit trimmer |
| WGGE WG-015 wire stripper/crimper | [B073YG65N2](https://www.amazon.com/dp/B073YG65N2) | 1 | $8.69 | |
| MAIYUM 63/37 rosin-core solder, 0.8 mm, 50 g | [B075WB98FJ](https://www.amazon.com/dp/B075WB98FJ) | 1 | $8.90 | Consumable |
| Weller brass tip cleaner | [B08FQBS97L](https://www.amazon.com/dp/B08FQBS97L) | 1 | $10.73 | |

## 6. Spare parts (not in the current CAD)

Bought for the course but not used on the arm. They stay in the parts inventory in case a design change needs them. They don't need restocking.

| Item | ASIN | Bought | Spent | Notes |
|---|---|---|---|---|
| uxcell 51107 thrust bearing 35×52×12 (2-pack) | [B07G847G75](https://www.amazon.com/dp/B07G847G75) | **2** | $9.28 | CAD uses 51108 |
| uxcell 6802-2RS 15×24×5 (10-pack) | [B07FVZKBKX](https://www.amazon.com/dp/B07FVZKBKX) | 2 packs = **20** | $18.76 | Not in CAD |
| uxcell 625-2RS 5×16×5 (5-pack) | [B07TNNX9YX](https://www.amazon.com/dp/B07TNNX9YX) | 3 packs = **15** | $21.18 | Not in CAD (5 mm bore: an idler variant?) |
| uxcell 686-2RS 6×13×5 (20-pack) | [B0DCP3V3B5](https://www.amazon.com/dp/B0DCP3V3B5) | 3 packs = **60** | $44.73 | Not in CAD (6 mm bore: planet bearings instead of bushings?) |
| uxcell 6×35 mm dowel pin (30-pack) | [B0F3JPNX6R](https://www.amazon.com/dp/B0F3JPNX6R) | **30** | $11.29 | CAD uses 6×22 and 6×30 |
| ruthex M4 × 8.1 heat-set insert (50-pack) | [B07YSV66Y5](https://www.amazon.com/dp/B07YSV66Y5) | **50** | $9.49 | CAD uses only M3 and M5 inserts |
| Kadrick M4 assortment, 6–40 mm (1400 pc) | [B0CQNPWSG4](https://www.amazon.com/dp/B0CQNPWSG4) | 1 kit | $22.99 | CAD has no M4 screws (only the set screw) |
