# Robotic Arm Assembly Guide

**14:125:444 Smart Prosthetics and Robotic Systems** — Dr. Adam Gormley

This guide takes you from a pile of printed and bought parts to a complete robotic
arm. Wiring and programming are in a separate guide.

> **Draft status.** Chapters 1 to 3 are written. The gearbox's order follows the
> [design's source article](#where-this-procedure-comes-from). The order of Chapters 2 and 3
> was worked out from the CAD model. All three have been checked against the CAD, but none
> has yet been followed step by step on real parts. Anything marked **TO CONFIRM** is
> calculated or assumed, and nothing so far settles it. Each chapter ends with a list:
> [gearbox](#open-items-to-confirm), [base](#open-items-base-and-joint-1),
> [hinge](#open-items-hinge-and-joint-2).

**Contents**

1. [Before you start](#before-you-start)
2. [Chapter 1: Planetary gearbox](#chapter-1-planetary-gearbox)
3. [Chapter 2: Base and joint 1](#chapter-2-base-and-joint-1)
4. [Chapter 3: Hinge and joint 2](#chapter-3-hinge-and-joint-2)
5. Chapter 4: Belt-drive arm segments *(to be written)*
6. Chapter 5: Final assembly *(to be written)*

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
| Long 2 mm ball-end hex key, and a short-armed key | J1 motor screws through the box's window (step 26), and hinge screws in the narrow gap (steps 31, 32) |
| 3 mm hex key and 8 mm spanner | M5 button head screws and nuts |
| Small clamp and a flat plate about 60 mm square | Pressing bearings once the hinge is on the base (steps 28, 29) |
| Round spacer about Ø24 × 40 mm, such as a socket from a socket set | Pressing the coupling's stub (step 29) |
| Caliper | Setting the 20T pulley's height (step 22) |
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

---

## Chapter 1: Planetary gearbox

The gearbox drives joint 2, the shoulder. It has two stages, each reducing speed
4:1, for **16:1** overall. In each stage the sun gear in the middle turns three planet
gears, which roll around the inside of the fixed ring gear and carry a carrier around
with them. That carrier then turns the next stage's sun.

![The gearbox with every part separated](img/gearbox_exploded.png)

![Cut-away of the assembled gearbox, with each part labelled](img/assembly/gearbox/overview_section.png)

### Where this procedure comes from

The gearbox is based on a design published on How To Mechatronics:
[*How Planetary Gears Work: 3D Printed Planetary Gearbox Design and Test*](https://howtomechatronics.com/how-it-works/how-planetary-gears-work-3d-printed-planetary-gearbox-design-and-test/).
This chapter follows the article's order and adapts it to our parts. The article is
also worth reading for how planetary gears work and how the gearbox performs.

### Parts

**Printed**

![The nine printed gearbox parts](img/assembly/gearbox/parts_printed.png)

| Part | Print-list name | Qty |
|---|---|---|
| Ring gear | `ring_gear` | 1 |
| Back cover | `back_cover` | 1 |
| Front cover | `front_cover` | 1 |
| Motor mount | `nema17_mount` | 1 |
| Input shaft | `input_shaft` | 1 |
| Planet gear | `planet_gear` | 6 |
| Carrier plate | `carrier_plate` | 2 |
| Stage-1 output carrier | `carrier_stage1_output` | 1 |
| Stage-2 output carrier | `carrier_stage2_output` | 1 |

**Bought**

![The bought gearbox parts and hardware](img/assembly/gearbox/parts_bought.png)

| Part | Qty | Where it goes |
|---|---|---|
| 6801 bearing, 12 × 21 × 5 | 2 | One in each output carrier |
| 6803 bearing, 17 × 26 × 5 | 1 | Back cover |
| 6805 bearing, 25 × 37 × 7 | 1 | Front cover |
| Dowel pin, 6 × 22 | 6 | Planet axles |
| Sleeve bushing, 6 × 8 × 10 | 6 | Inside the planets |
| M6 flat washer, 6 × 12 × 1.5 | 12 | Two per planet |
| Ruthex M3 × 5.7 insert | 18 | Ring gear 12, carrier plates 3 + 3 |
| Ruthex M3S × 4.0 short insert | 4 | Back cover. **Not stocked yet:** on the to-order list in `inventory.md` §3 |
| M3 button head screw × 10 (**TO CONFIRM**) | 6 | Carrier halves, 3 per carrier |
| M3 button head screw × 12 (**TO CONFIRM**) | 6 | Front cover to ring gear |
| M3 button head screw × 16 (**TO CONFIRM**) | 6 | Back cover to ring gear |
| M3 screw × 18 | 4 | Motor to mount. Check the assortment has this length |
| M3 screw × 22 | 4 | Mount to back cover. Check the assortment has this length |
| Set screw, probably M4 × 5 (**TO CONFIRM**) | 1 | Input shaft to motor shaft |
| NEMA17 motor, 48 mm body | 1 | |

### Step 0: Check the parts

1. Lay out every part and tick it off against the tables above.
2. Remove any support marks from fit surfaces: bearing seats, shaft journals, gear
   teeth, and the faces where parts meet. Sand them lightly.
3. Check the flat parts on a flat surface. They should not rock.
4. Try each fit dry, without forcing anything: a planet pin in each carrier hole, a
   bushing started in a planet, and each bearing started in its seat.

**Check:** nothing is cracked, warped or badly oversized. If a fit is far off, stop and
find out why before pressing parts together. Reprinting one part now is much easier
than taking the gearbox apart later.

### Step 1: Install the threaded inserts

**Parts:** ring gear, back cover, both carrier plates, 18 M3 × 5.7 inserts, 4 M3S × 4
short inserts.

Do this first. In resin the epoxy has to cure (4–6 hours to set), so **plan ahead**.

![Inserts going into the ring gear](img/assembly/gearbox/step01a_ring.png)

**Ring gear:** 6 inserts in each end face, 12 in all.

![Short inserts going into the motor side of the back cover](img/assembly/gearbox/step01b_back_cover.png)

**Back cover:** 4 **short** inserts in the motor-side face. The holes are only 4.5 mm
deep, and a standard insert won't fit.

![Inserts going into a carrier plate's flat face](img/assembly/gearbox/step01c_plate.png)

**Each carrier plate:** 3 inserts, in the flat face with the three small pegs.

**How to install them:**

- **PLA:** heat-set with a soldering iron until flush with the surface.
- **Resin:** cured resin doesn't melt, so bond them with epoxy:
  1. Check the insert slides into the hole by hand before mixing any epoxy.
  2. Coat the hole wall with epoxy, not the insert, so glue stays out of the threads.
  3. Press the insert in until flush.
  4. Thread a greased M3 screw into it while the epoxy cures. This keeps the threads
     clean and holds the insert square. Remove the screw once fully cured.

**Check:** every insert is flush and square, and an M3 screw threads in by hand.

### Step 2: Press the bushings into the planets

**Parts:** 6 planet gears, 6 bushings.

![A bushing above a planet gear, ready to press in](img/assembly/gearbox/step02a_bushing.png)

1. Start a bushing squarely in a planet's bore.
2. Press it in with a vise until **centred**: the bushing is 10 mm long and the planet 9
   mm thick, so it should stand **0.5 mm proud of each face**.
3. Repeat for all six.

![Cut-away of a planet showing the bushing proud of both faces](img/assembly/gearbox/step02b_section.png)

The proud ends are what the washers run against, so the plastic gear face doesn't rub.

> **Caution:** Grey V5 planets are thin and brittle. Keep the bushing square, and use
> a vise or arbor press, not a hammer. On the Form 4 Grey V5 coupon this fit took light
> tapping, and in X1C PLA a bit of pressure.

**Check:** a planet pin slides and turns freely through the full length of the bushing.
A bushing pressed too hard closes up its bore.

### Step 3: Build the stage-2 carrier

**Parts:** stage-2 output carrier, 6801 bearing, 3 pins, 3 planets with bushings, 6
washers, 1 carrier plate, 3 M3 × 10 screws.

This is the carrier with the output shaft and hex on it.

![Bearing and three pins going into the output carrier](img/assembly/gearbox/step03a_pins_bearing.png)

1. **Press the 6801 bearing** into the recess in the centre of the carrier, until it
   seats. Do this now: the bearing can't pass between the planets later.
2. **Press the 3 pins** into their holes, working from the flange's inner face. Stand
   the carrier's flange on something flat, with a recess or gap for the shaft, so that
   each pin finishes **flush with the outer face**. About 17 mm of pin stands above the
   flange.

![Washer, planet, washer going onto each pin](img/assembly/gearbox/step03b_planets.png)

3. **Stack each pin:** washer, planet, washer. A planet can go on either way up.

![Carrier plate lowered over the three pins](img/assembly/gearbox/step03c_plate.png)

4. **Lower the carrier plate** over the pins, with the inserts and pegs facing down.
   Each pin goes through its hole, and the three small pegs enter their sockets. The
   pins finish flush with the top of the plate.

![Three screws going in from the outer face](img/assembly/gearbox/step03d_screws.png)

5. **Turn the carrier over.** Fit 3 M3 × 10 screws (**TO CONFIRM**) from the outer face,
   through the conical holes and into the plate's inserts. The narrow part of each hole
   is Ø2.8, so the screw cuts its own thread there. Tighten gently and evenly.

**Check:** the two halves sit flat together, and every planet spins freely by hand with
only slight end play. If the planets bind, see the washer item in
[the open list](#open-items-to-confirm).

### Step 4: Build the stage-1 carrier

**Parts:** stage-1 output carrier, 6801 bearing, 3 pins, 3 planets with bushings, 6
washers, 1 carrier plate, 3 M3 × 10 screws.

This is the same procedure as step 3. The only difference is that the carrier's stem
has a small gear on it, the **stage-2 sun**, instead of the output shaft. Protect those
teeth when you stand the part up to press the pins.

![Bearing and pins going into the stage-1 output carrier](img/assembly/gearbox/step04a_pins_bearing.png)

![Planets and washers going onto the pins](img/assembly/gearbox/step04b_planets.png)

![Carrier plate going over the pins](img/assembly/gearbox/step04c_plate.png)

![Screws going in from the outer face](img/assembly/gearbox/step04d_screws.png)

**Check:** as in step 3.

### Step 5: Fit the input shaft into the stage-1 carrier

**Parts:** stage-1 carrier, input shaft.

![Input shaft lowered into the stage-1 carrier](img/assembly/gearbox/step05a_input_shaft.png)

1. Hold the carrier with the plate up, and lower the input shaft through the plate's
   central opening, gear end first.
2. The teeth are helical, so the shaft must **turn as it goes in**. Twist gently and let
   it find its way between the three planets. Don't force it straight down.
3. Keep going until the shaft's narrow tip enters the 6801 bearing, then press it home.

![Cut-away showing the sun meshed with the planets and the tip in the bearing](img/assembly/gearbox/step05b_section.png)

**Check:** turning the input shaft spins all three planets smoothly.

### Step 6: Twist stage 1 into the ring gear

**Parts:** stage-1 assembly from step 5, ring gear.

![Stage 1 lowered into the ring gear](img/assembly/gearbox/step06_stage1_in_ring.png)

1. Stand the ring gear with its **motor end up**: the end where the teeth run right up
   to the face. The other end, the output end, has a plain wide counterbore.
2. Lower stage 1 in, stem first. As the planets reach the teeth, slowly turn the input
   shaft or the carrier so that the planets thread in. It should go with little force.
3. Keep going until the planets are fully on the upper band of teeth.

**Check:** with the ring held still, turning the input shaft turns the carrier, about
one carrier turn for four input turns.

### Step 7: Twist stage 2 in from the other end

**Parts:** stage-2 carrier from step 3, ring gear with stage 1.

This is the most awkward step, because three things must line up at once.

![Stage 2 coming up into the ring gear from below](img/assembly/gearbox/step07a_stage2_in_ring.png)

1. Turn the ring gear over, holding stage 1 in. Rest the ring on something that leaves
   room for the input shaft, which sticks out about 20 mm, such as open vise jaws or a
   roll of tape.
2. Lower the stage-2 carrier into the counterbore end, plate first. Its plate has a
   central opening that passes over the stage-2 sun.
3. Turn stage 1 slowly, using the input shaft from below or by rocking the stage-2
   carrier, until:
   - the stage-2 sun threads in between the stage-2 planets,
   - the stage-2 planets thread onto the ring's lower band of teeth, and
   - the end of the stem enters the 6801 bearing in the stage-2 carrier.
4. Press it home gently.

![Cut-away showing both stages in the ring gear and where each shaft end sits](img/assembly/gearbox/step07b_section.png)

**Check:** turning the input shaft turns the output shaft, smoothly and slowly.

> **If it won't go in:** don't force it. Lift stage 2 out, turn it by one tooth and try
> again.

### Step 8: Grease the gears and check the mesh

1. Apply a small amount of gear grease (**TO CONFIRM** which) to the teeth.
2. Turn the input shaft through several full turns to spread it.

**Check:** the gears should turn with very little resistance. A tight spot that returns
at the same place every turn usually means one part is out of round or a tooth has a
print defect, so find it now.

### Step 9: Fit the output bearing and front cover

**Parts:** 6805 bearing, front cover, 6 M3 × 12 screws.

![The 6805 bearing and front cover going onto the output shaft](img/assembly/gearbox/step09_front_cover.png)

1. With the output shaft up, slide the **6805 bearing** over the hex and press it onto
   the round Ø25 shaft until it stops on the shoulder.
2. Lower the **front cover** over the shaft, with the raised boss toward the ring.
   Press it onto the bearing until it sits flat on the ring gear, with the 6 holes lined
   up with the ring's inserts.
3. Fit 6 M3 × 12 screws (**TO CONFIRM**), with heads in the cover's pockets, and tighten
   evenly in a star pattern.

> Five of these screws come out again in [step 30](#step-30-take-out-five-front-cover-screws),
> when the gearbox goes onto the hinge, because the hinge's screws use the same inserts.

**Check:** the output shaft still turns freely. If it got tight, the cover is probably
not sitting flat.

### Step 10: Fit the input bearing and back cover

**Parts:** 6803 bearing, back cover, 6 M3 × 16 screws.

![The 6803 bearing and back cover going over the input shaft](img/assembly/gearbox/step10_back_cover.png)

1. Press the **6803 bearing** into the seat on the inside of the back cover, the side
   with the big recess, until it stops.
2. Turn the gearbox motor end up. Lower the cover over the input shaft, with the short
   inserts facing up, so that the shaft enters the bearing.
3. Press it down until the cover sits flat on the ring gear, with the 6 holes lined up.
4. Fit 6 M3 × 16 screws (**TO CONFIRM**), heads in the pockets, and tighten evenly in a
   star pattern.

**Check:** the input shaft turns freely.

### Step 11: Check the ratio

![The closed gearbox, with input and output marked](img/assembly/gearbox/step11_closed.png)

1. Mark the input shaft and the output hex with a pen.
2. Turn the input shaft **16 full turns** by hand and count them.

**Check:** the output hex has turned **exactly one full turn**, in the same direction,
with no tight spots. If it binds now, fix it before the motor goes on.

### Step 12: Start the set screw

**Parts:** set screw (**TO CONFIRM** size).

![The set screw going into the side of the input shaft](img/assembly/gearbox/step12_set_screw.png)

1. Thread the set screw into the cross hole in the input shaft, only until it holds.
2. **Keep its tip out of the central bore**, or the motor shaft won't go in.

> **TO CONFIRM:** the hole is Ø4.0, an M4 screw's outer diameter, so an M4 may not grip
> the plastic.

### Step 13: Fix the mount to the motor

**Parts:** NEMA17 motor, motor mount, 4 M3 × 18 screws.

This comes **before** the mount goes on the gearbox, because these screws go in from the
side that ends up against the back cover.

![Motor mount and screws going onto the motor's face](img/assembly/gearbox/step13_motor_mount.png)

1. Set the mount on the motor's face, with the **counterbores facing away from the
   motor** and the motor's round boss in the mount's bore.
2. Fit 4 M3 × 18 screws through the counterbores into the motor. Don't use longer
   screws: M3 × 18 goes 3 mm into the motor, and its threaded holes are typically about
   4.5 mm deep.

> **TO CONFIRM:** which way the motor's connector should point relative to the mount's
> access slot. The mount fits four ways round.

### Step 14: Slide the motor shaft in and bolt the mount down

**Parts:** motor with mount, 4 M3 × 22 screws.

![Motor and mount lowered onto the back cover](img/assembly/gearbox/step14_motor_on.png)

1. Turn the input shaft so that the set screw faces where the mount's **access slot**
   will be.
2. Turn the motor shaft so that its **flat lines up with the flat in the input shaft's
   bore**, which is on the set screw's side.
3. Lower the motor and mount so the shaft slides into the bore. The mount sits on the
   back cover, with the slot lined up with the set screw.
4. Fit 4 M3 × 22 screws through the mount's outer holes, on the ledges either side of the
   motor, into the short inserts. Use exactly this length: M3 × 25 bottoms out in
   the hole, and M3 × 20 engages only 2 mm of thread.

### Step 15: Tighten the set screw

![Cut-away showing the set screw on the motor shaft's flat, reached through the slot](img/assembly/gearbox/step15_section.png)

1. Reach through the access slot with the 2 mm hex key and find the set screw.
2. Tighten it onto the motor shaft's flat. Stop when it's snug: the input shaft is plastic.

**Check:** hold the motor body and try to turn the output by hand, gently. The motor
shaft and input shaft should turn together, with no slip between them.

**The gearbox is finished.** It goes onto the hinge in Chapter 3.

### Open items to confirm

These need checking on a real build. The article and the CAD don't settle them.

| Item | What the guide assumes | Why it's open |
|---|---|---|
| Whole procedure | The article's order, adapted to our parts | Not yet followed step by step on real parts |
| Carrier screws (steps 3, 4) | M3 × 10 button head, 6 in all | Calculated: the head seats 0.9 mm into the Ø7.5 cone and stands about 0.75 mm proud, and the tip passes through the insert. The article gives no type or length. A flat-head countersunk screw may be intended. Self-threading through the Ø2.8 hole may be risky in brittle resin |
| Front cover screws (step 9) | M3 × 12 button head, 6 in all | Calculated. Five come out in step 30, and M3 × 20 go into the same inserts from the hinge's side |
| Back cover screws (step 10) | M3 × 16 button head, 6 in all | Calculated: 5.2 mm into the insert |
| Set screw (steps 12, 15) | M4 × 5 | The article gives no size, and `inventory.md` says "probably". The Ø4.0 hole may be too large for an M4 to grip |
| Washer stack (steps 3, 4) | Fits as shown | The pocket is 13.0 mm tall. Two 1.5 mm washers plus the 10 mm bushing also total 13.0 mm, so there may be no end play and the planets may bind (the CAD's 1.3 mm stand-in washers leave 0.4 mm) |
| Grease (step 8) | Any gear grease | The article adds lubricant without naming it. Check it's safe for the plastic |
| Motor connector direction (step 13) | Not specified | Nothing in the CAD sets it |

---

## Chapter 2: Base and joint 1

The base is a box that holds the J1 motor, with the hinge turning on top of it. J1 is the
waist: it turns the whole arm about a vertical axis. The motor's 20-tooth pulley drives a
160-tooth pulley through a belt, for **8:1**.

The hinge's shaft carries the load. A long stack sits on it: hinge, upper thrust bearing,
box top, lower thrust bearing and pulley, all clamped together by four M5 screws. The stack
turns in the box top's 6807 bearing, with a 608 bearing in the box bottom holding the
pulley's lower end.

Build this chapter **before putting the gearbox on**. The hinge is easier to handle
without it, and the gearbox would block some of the box's screws.

![Cut-away of the base, with each part labelled](img/assembly/joint1/overview_section.png)

### Parts

**Printed**

![The four printed base parts](img/assembly/joint1/parts_printed.png)

| Part | Print-list name | Qty |
|---|---|---|
| Box bottom | `box_bottom` | 1 |
| Box top | `box_top` | 1 |
| Hinge | `hinge` | 1 |
| 160T pulley | `gt2_pulley_160t` | 1 |

**Bought**

![The bought base parts and hardware](img/assembly/joint1/parts_bought.png)

| Part | Qty | Where it goes |
|---|---|---|
| 51108 thrust bearing, 40 × 60 × 13 | 2 | Above and below the box top |
| 6807 bearing, 35 × 47 × 7 | 1 | Box top |
| 608 bearing, 8 × 22 × 7 | 1 | Box bottom |
| 6805 bearing, 25 × 37 × 7 | 1 | Hinge, gearbox cheek. The other cheek's is in Chapter 3 |
| NEMA17 motor, 48 mm body | 1 | J1 |
| GT2 20T pulley, 5 mm bore | 1 | J1 motor |
| GT2 closed belt, 6 mm wide, **370 mm** | 1 | **Not stocked yet:** on the to-order list in `inventory.md` §1 |
| Ruthex M5 × 9.5 insert | 7 | Box bottom |
| M5 × 40 button head screw | 4 | Hinge to pulley. Use this length: M5 × 45 would hit the 608 |
| M5 nut | 4 | Under the pulley |
| M5 × 20 button head screw (**TO CONFIRM**) | 7 | Box top to box bottom. Check the assortment has this length |
| M3 × 16 button head screw | 4 | Motor to box top |

### Step 16: Check the parts

1. Lay out every part and tick it off against the tables above.
2. Remove any support marks from fit surfaces and sand them lightly, as in step 0.
3. Try each fit dry, without forcing anything: the hinge shaft started in the 6807, the
   6807 and 608 started in their seats, and a thrust bearing in the box top's recess, the
   pulley's pocket and the hinge's pocket.
4. Try the **pulley's hub in the 608**. The hub is modelled at Ø8.0 exactly, with no
   allowance for printing. If it won't start, sand it gently until it does (**TO CONFIRM**).

**Check:** the thrust bearings drop into all three pockets, and the hub starts in the 608.

### Step 17: Install the threaded inserts in the box bottom

**Parts:** box bottom, 7 M5 × 9.5 inserts.

![Inserts going into the box bottom's top face](img/assembly/joint1/step17_inserts.png)

Install them as in [step 1](#step-1-install-the-threaded-inserts): heat-set in PLA, or
bonded with epoxy in resin, which needs 4–6 hours to set. **Plan ahead.**

**Check:** every insert is flush and square, and an M5 screw threads in by hand.

### Step 18: Press the 608 and 6807 bearings

**Parts:** box bottom, 608 bearing, box top, 6807 bearing.

![The 608 going into its seat in the box bottom](img/assembly/joint1/step18a_608.png)

1. **Press the 608** into the raised ring on the box bottom's floor, until it reaches the
   floor.

![Cut-away of the box top, top face down, with the 6807 going in from the recess side](img/assembly/joint1/step18b_6807.png)

2. **Press the 6807** into the box top. Its seat goes all the way through and has **no
   shoulder to stop it**, so the bearing can go too far. Lay the box top with its **top
   face down on a flat surface**, so that the wide Ø60 recess faces up. Press the bearing in
   from the recess side until it stops on the flat surface.

**Check:** the 6807 is flush with the box top's top face, and both bearings spin freely.

### Step 19: Press a 6805 bearing into the hinge's gearbox cheek

**Parts:** hinge, 6805 bearing.

Do this now, while the hinge is on its own and fits in a vise. The hinge has two different
cheeks: the **taller** one takes the gearbox, and the bearing goes in that one.

![A 6805 bearing going into the outside of the hinge's taller cheek](img/assembly/joint1/step19_left_6805.png)

1. Put a block about 56 mm long between the cheeks, so that the vise doesn't bend them.
2. Start the bearing from the outside of the taller cheek. Put a flat plate over it.
3. Close the vise until the plate reaches the cheek. This seat has no shoulder either: the
   plate is what stops the bearing, flush with the cheek's outer face.

Leave the other cheek's seat **empty**. Chapter 3 needs it open.

**Check:** the bearing is flush with both faces of the cheek and spins freely.

### Step 20: Stack the joint 1 parts

**Parts:** 160T pulley, 2 thrust bearings, box top with its 6807, hinge.

The stack goes together from the bottom up. Each thrust bearing is **three loose pieces**,
two washers and a ball cage, so keep each set together. Grease them lightly with the gear
grease (**TO CONFIRM**).

![The stack, separated: hinge, upper thrust bearing, box top, lower thrust bearing, pulley](img/assembly/joint1/step20a_stack.png)

1. Stand the **pulley** on something that leaves room for its hub, such as a roll of tape.
   The hub points down.
2. Put the **lower thrust bearing** in the pulley's pocket.
3. Lower the **box top** onto it, top face up, so that the bearing enters the Ø60 recess.
4. Put the **upper thrust bearing** on the box top, around the 6807.
5. Lower the **hinge** so that its shaft passes through the upper thrust bearing and starts
   in the 6807. The bearing enters the pocket under the hinge's floor.
6. Press the hinge down, with a block on its floor if it needs a vise, until the shaft end
   stops on the floor of the pulley's pocket.
7. Turn the pulley until its 4 holes line up with the 4 holes in the hinge's floor.

![Cut-away of the finished stack](img/assembly/joint1/step20b_section.png)

> **TO CONFIRM:** the two thrust bearings and the box top total 33 mm, and the shaft is also
> exactly 33 mm long. If the printed parts come out thick, the stack could bind when
> clamped in the next step. **Don't sand the shaft's end:** a shorter shaft makes it
> tighter. Ease the nuts off until it turns freely, and report what you found.

### Step 21: Clamp the stack with the M5 screws

**Parts:** stack, 4 M5 × 40 screws, 4 M5 nuts.

![The M5 screws going in from the hinge floor, with nuts under the pulley](img/assembly/joint1/step21a_clamp.png)

1. Drop the 4 screws through the hinge's floor. Their heads sit in the Ø12 counterbores.
2. Lift the assembly and thread a nut onto each screw under the pulley.
3. Hold each nut with the 8 mm spanner and tighten with the 3 mm hex key, evenly, a little
   at a time. Stop at snug: the shaft end bottoms on the pulley, so more force only
   stresses the plastic.

![Cut-away showing a screw head in its counterbore and a nut under the pulley](img/assembly/joint1/step21b_section.png)

Don't use longer screws. With M5 × 40, the nut's far side is about 0.3 mm above the 608's
seat and the screw ends inside the nut. M5 × 45 would run into the 608 when the box closes.

**Check:** holding the box top, the hinge and pulley turn together, smoothly, with no tight
spot and no up-and-down play. If it binds, see the note in step 20.

### Step 22: Fit the 20T pulley to the J1 motor

**Parts:** NEMA17 motor, 20T pulley.

Do this now, because the pulley's set screw is hard to reach once the motor is on the box.

![The 20T pulley going onto the motor shaft](img/assembly/joint1/step22_pulley.png)

1. Slide the pulley onto the motor shaft.
2. Set it **15 mm from the motor's face to the pulley's nearest flange**, measured with a
   caliper. This lines it up with the 160T pulley's teeth.
3. Tighten its set screw onto the flat on the motor shaft.

**Check:** the pulley doesn't move on the shaft, and the distance is still 15 mm.

### Step 23: Fit the motor to the box top

**Parts:** stack, motor with pulley, 4 M3 × 16 screws.

![The motor going down into the box top's slot, with screws coming up from below](img/assembly/joint1/step23_motor.png)

1. Turn the hinge so that one **cheek faces the motor slot**. With the motor at this end of
   the slot, the hinge's corners would hit it if turned. Keep the hinge square until step 26.
2. Lower the motor onto the box top, so that the shaft and pulley pass through the wide slot.
3. Slide it to the **hinge end of the slot**.
4. From below, fit the 4 M3 × 16 screws through the two narrow slots into the motor. Leave
   them **snug but not tight**, so that the motor can still slide.

The screws go through 12 mm of box top and about 4 mm into the motor. Don't use longer
ones: the motor's threaded holes are typically about 4.5 mm deep.

**Check:** the motor slides along the slot with light pressure and stays square to it.

### Step 24: Fit the belt

**Parts:** stack with motor, 370 mm belt.

![The belt coming up to the two pulleys, seen from below](img/assembly/joint1/step24_belt.png)

1. Hold the assembly so that you can see under the box top.
2. Loop the belt around the 160T pulley, between its flanges, and then over the 20T pulley.

The picture shows the motor where it finishes, at the far end of the slot. With the motor
still at the hinge end, as it should be now, the belt is loose and goes on easily.

**Check:** the belt sits between the flanges on both pulleys. It should look level, because
the two toothed bands are at the same height. If it doesn't, recheck the 15 mm in step 22.

### Step 25: Close the box

**Parts:** box bottom, stack with motor and belt, 7 M5 × 20 screws.

![The stack lowered into the box bottom, with seven screws going in from the top](img/assembly/joint1/step25_close.png)

1. Stand the box bottom on the bench, with its side window toward the motor.
2. Lower the stack in, so that the pulley's hub enters the 608. Keep the belt on its
   pulleys. If the hub is tight, turn the hinge slightly as it goes in.
3. Line up the corners and fit the 7 M5 × 20 screws (**TO CONFIRM**) with the 3 mm hex key.
   They reach 8 mm into the 10.5 mm deep holes.

**Check:** the box top sits flat on the box bottom, and the hinge still turns as easily as
in step 21, as far as the loose motor allows.

### Step 26: Tension the belt and check joint 1

![Cut-away along one line of motor screws, showing where each one is reached](img/assembly/joint1/step26a_window.png)

1. Pull the motor **away from the hinge**, by hand, until the belt is taut. The belt's
   length decides where the motor stops: with a 370 mm belt, its far side ends up about 1 mm
   short of the box's edge.
2. Hold it there and tighten the **two screws nearest the box's edge** first. They are just
   above the side window. Reach in with the 2 mm hex key.
3. Tighten the **other two** through the same window, with a **long ball-end key** held at
   an angle. It has to pass over the belt to reach them.

![The finished base](img/assembly/joint1/step26b_closed.png)

**Check:**

- Mark the 20T pulley's flange with a pen and watch it through the window. Turn the hinge
  **one full turn** by hand: the pulley turns **8 times**, and the belt doesn't skip.
- Nothing touches through the whole turn. There is no gearbox yet, so the hinge is free to
  go all the way round.
- The belt deflects a little when pressed, about 3–5 mm (**TO CONFIRM**), and the motor
  hasn't moved.

**The base is finished.** The gearbox goes on next.

### Open items: base and joint 1

| Item | What the guide assumes | Why it's open |
|---|---|---|
| Whole procedure | The order above | Worked out from the CAD and not yet followed on real parts |
| Pulley hub in the 608 (steps 16, 25) | Sand until it fits | The hub is exactly Ø8.0, with no print allowance |
| Stack height (steps 20, 21) | Turns freely when clamped | The parts and the shaft are both exactly 33 mm. Printed parts may bind or leave play |
| Clamp clearance (step 21) | M5 × 40 and nut clear the 608 | A real M5 nut leaves about 0.3 mm above the 608's seat. A taller locking nut would not fit |
| Box screws (step 25) | M5 × 20 button head, 7 in all | Calculated: 8 mm into the insert's hole. Check the assortment has this length |
| Thrust bearing grease (step 20) | The same grease as the gears | Check it's safe for the plastic |
| Belt tension (step 26) | About 3–5 mm deflection | There is no measured value yet. The belt length mostly decides it |

---

## Chapter 3: Hinge and joint 2

Joint 2 is the shoulder. The gearbox from Chapter 1 bolts to the hinge's taller cheek, and
its output hex drives the coupling shaft, a block between the cheeks that the arm will bolt
to. The output shaft and the coupling each run in a 6805 bearing in the cheeks.

**The order matters.** The coupling has to go in first: with the gearbox bolted on, its hex
would stick too far into the gap for the coupling to get past it.

![Cut-away of joint 2, with each part labelled](img/assembly/joint2/overview_section.png)

### Parts

You also need the finished gearbox from Chapter 1 and the finished base from Chapter 2.

![The coupling shaft, the second 6805 bearing and an M3 × 20 screw](img/assembly/joint2/parts_sheet.png)

| Part | Print-list name or size | Qty | Where it goes |
|---|---|---|---|
| Coupling shaft (printed) | `coupling_shaft` | 1 | Between the cheeks |
| 6805 bearing | 25 × 37 × 7 | 1 | Hinge, shorter cheek |
| M3 button head screw | × 20 | 5 | Gearbox to hinge. Check the assortment has this length |

### Step 27: Check the fits

1. Sand any support marks off the coupling's stub and off its block's faces.
2. Try the coupling on the gearbox's **output hex**, without forcing it. It fits one flat at
   a time, so try it at several angles.
3. Try the 6805 on the coupling's **stub**, just started.

**Check:** the hex slides into the socket, and the stub starts in the bearing. Take them
apart again before continuing.

### Step 28: Put the coupling between the cheeks

**Parts:** base, coupling shaft, 6805 bearing, a small clamp, a flat plate.

The hinge stays on the base from here on, so use a small clamp in place of a vise. Turn
the hinge so that you can reach it easily.

![The coupling coming down between the cheeks](img/assembly/joint2/step28a_drop.png)

1. Point the coupling's **stub toward the shorter cheek**, whose seat is still empty.
2. Lower it between the cheeks. **The fit is exact:** the coupling is 56 mm long, and so is
   the gap, so the stub can't clear the cheek on its way down to the seat. Flex the shorter
   cheek outward a little, about 1 mm, with your hand as the coupling goes past. Once the
   stub reaches the seat, the cheek can spring back. Don't force it. In resin this is
   **TO CONFIRM**, because the parts are more brittle.
3. Let the stub line up with the empty seat, then hold the block against the **taller**
   cheek. The stub now stops just short of the seat. Rest the block on something about 15 mm
   thick on the hinge's floor, so that it stays at this height.

![Cut-away with the coupling against the taller cheek and the bearing about to go in](img/assembly/joint2/step28b_right_6805.png)

4. Start the 6805 in the shorter cheek from the outside, and put the flat plate over it.
5. Clamp between the plate and the taller cheek's outer face, gently, until the plate reaches
   the cheek. Like the other seat, this one has no shoulder, so the plate stops the bearing
   flush.

**Check:** the bearing is flush with the cheek's outer face.

### Step 29: Press the stub into the right bearing

**Parts:** a round spacer about Ø24 and 40 mm long, such as a socket from a socket set; the
flat plate; the clamp.

![Cut-away showing the plate, the stub, the coupling and the spacer in line](img/assembly/joint2/step29_stub.png)

1. Keep the flat plate on the shorter cheek, covering the bearing.
2. Pass the spacer through the 6805 in the taller cheek, until it rests on the rim of the
   coupling's hex socket.
3. Line the stub up with the bearing's bore, then clamp between the plate and the spacer.
4. Close it slowly. The block moves about 7 mm until the **stub's end reaches the plate**.

This force goes straight through the coupling and the bearing's inner ring, so the cheeks
aren't loaded. If the stub goes in by hand, you don't need the clamp at all.

Take out the 15 mm block.

**Check:** the coupling turns freely by hand, until its block meets the hinge's floor at
about 80° either way. There is now a gap of about 7 mm between the block and the taller cheek.

### Step 30: Take out five front cover screws

**Parts:** finished gearbox.

The screws that hold the gearbox to the hinge use the same inserts as the front cover's
M3 × 12 screws, so five of those have to come out.

![The gearbox's front cover with five screws out and one left in at the bottom](img/assembly/joint2/step30_screws.png)

1. Hold the gearbox so that the motor mount's **access slot points sideways, level**. The
   set screw stays reachable that way, and it puts one cover screw at the very bottom.
2. Leave that **bottom screw in**. It lines up with the place on the hinge where there is no
   hole, because the hinge's floor is in the way. It keeps the cover on the ring gear.
3. Take out the other **five**. Keep them as spares.

**Check:** the cover is still seated flat on the ring gear.

### Step 31: Slide the gearbox in and start three screws

**Parts:** gearbox, 3 M3 × 20 screws.

![The gearbox coming up to the hinge's taller cheek, hex first](img/assembly/joint2/step31a_gearbox.png)

1. Turn the coupling so that its top face is level. Unplug the gearbox motor's leads: it's
   much harder to turn with its wires joined together.
2. Pass the output hex through the 6805 in the taller cheek. Keep the coupling level and turn
   the hex by hand until its flats line up with the socket, with a corner straight up. This
   turns the motor too, quickly and gently. Slide the hex into the socket. The round output
   shaft then enters the bearing's inner ring.
3. Line up the cover's holes with the cheek's, with the kept screw at the bottom and the
   access slot sideways. Push the gearbox in as far as it goes by hand.

![From inside the hinge, three screws going in with the coupling square](img/assembly/joint2/step31b_screws.png)

4. From **inside** the hinge, fit 3 M3 × 20 screws in the holes clear of the coupling: the
   one at the top and the two at the lower sides. Their heads sit in the cheek's counterbores.
   A short-armed 2 mm key fits in the gap.
5. Tighten them a little at a time, in turn, to **draw the gearbox in** until the cover sits
   flat on the cheek. The screws can reach their inserts once the cover is within about 6 mm
   of the cheek. If it stops turning smoothly, back off and find out why.

![Cut-away showing a screw through cheek and cover into the insert, and the hex in its socket](img/assembly/joint2/step31c_section.png)

**Check:** the cover is flat on the cheek all the way round, with no gap.

### Step 32: Turn joint 2 and fit the last two screws

**Parts:** 2 M3 × 20 screws.

With the coupling level, its block covers the last two holes, at the upper sides.

![The coupling turned about 40°, leaving the last two holes clear](img/assembly/joint2/step32_screws.png)

1. Turn the coupling about **40°**, either way, by hand. This turns the gearbox backward
   through 16:1, so the motor spins quickly: go gently.
2. Fit the last 2 M3 × 20 screws.
3. Tighten all five evenly, in a star pattern. Stop at snug.
4. Turn the coupling back to level.

> The screw reaches through 5 mm of cheek and 9 mm of cover, then 6 mm into the ring gear,
> which is the full length of its insert.

**Check:** all five heads sit below the cheek's inner face, and nothing touches them when the
coupling turns.

### Step 33: Check joint 2

![The finished base and shoulder](img/assembly/joint2/step33_closed.png)

The ratio was checked in [step 11](#step-11-check-the-ratio) and can't be repeated here,
because the motor's shaft is out of reach and the coupling can't make a full turn.

**Check:**

- **Joint 2:** with the motor leads unplugged, turn the coupling gently back and forth, to
  about 75° either way. It should move smoothly, with no tight spot and no clicks. It stops
  when the block meets the hinge's floor. Don't push it against that stop: force at the
  coupling is multiplied 16 times at the motor's end, and it strains the gear teeth.
- **Binding:** this joint runs in three bearings on one line (the front cover and both
  cheeks). If it's stiff, loosen the five screws slightly and try again. If it then runs
  freely, the cover wasn't square to the cheek.
- **Joint 1:** turn the hinge about **120° either way**. The gearbox swings over the box
  without touching anything. It meets the J1 motor at about 125°, so don't go further.

**The base and shoulder are finished.** Arm segment 1 bolts to the coupling's top face in
Chapter 4. On the finished arm, joint 2's travel is about ±63°, set by the segment's motor.

### Open items: hinge and joint 2

| Item | What the guide assumes | Why it's open |
|---|---|---|
| Whole procedure | The order above | Worked out from the CAD and not yet followed on real parts |
| Flexing the cheek in resin (step 28) | Flex the shorter cheek out about 1 mm, as on the built arm | The coupling and the gap are both exactly 56 mm, so the cheek has to flex during insertion. This may be risky in brittle resin |
| Pressing the stub (step 29) | A Ø24 spacer on the socket's rim | The spacer has to pass the Ø25 bearing bore and still land on the socket's Ø21.65 flats. Nobody has tried it yet. The stub may go in by hand |
| Drawing the gearbox in (step 31) | The first 3 screws pull it the last 6 mm | The shaft is a press fit in the cheek's bearing. If it's tight, the inserts take the load |
| Three bearings on one axis (step 33) | Runs freely | The front cover and both cheeks must line up closely (`design.md` I‑1). Print accuracy decides it |
| Turning the coupling by hand (step 32) | The gearbox can be back-driven | 16:1 through printed gears, with the motor unpowered. If it's too stiff, step 32 is hard to do |
