# Robotic Arm Assembly Guide

**14:125:444 Smart Prosthetics and Robotic Systems** — Dr. Adam Gormley

This guide takes you from a pile of printed and bought parts to a complete robotic
arm. Wiring and programming are in a separate guide.

> **Draft status.** The gearbox chapter is the first one written. Its order follows
> the [design's source article](#where-this-procedure-comes-from) and has been checked
> against the CAD model, but it has not yet been followed step by step on real parts.
> Anything marked **TO CONFIRM** is calculated or assumed, and neither the article nor
> the CAD settles it. [The list is at the end of the chapter](#open-items-to-confirm).

**Contents**

1. [Before you start](#before-you-start)
2. [Chapter 1: Planetary gearbox](#chapter-1-planetary-gearbox)
3. Chapter 2: Base and joint 1 *(to be written)*
4. Chapter 3: Hinge and joint 2 *(to be written)*
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
- Most pictures stand the gearbox on its output, with the motor end up. When a step
  has you work from the other end, the picture is drawn from below.

The screws, inserts and set screw in the pictures are simplified shapes. The bought
parts are stand-ins too, so yours may look slightly different.

### Tools and supplies

| Item | Used for |
|---|---|
| 2 mm hex key | M3 button head screws and the set screw |
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

> **TO CONFIRM:** the hinge's screws use the same bolt circle. Chapter 3 will say which
> of these screws come out when the gearbox goes onto the hinge.

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
| Front cover screws (step 9) | M3 × 12 button head, 6 in all | Calculated. What stays and what comes out on the hinge isn't decided, because the hinge screws use the same bolt circle (`design.md` Q4) |
| Back cover screws (step 10) | M3 × 16 button head, 6 in all | Calculated: 5.2 mm into the insert |
| Set screw (steps 12, 15) | M4 × 5 | The article gives no size, and `inventory.md` says "probably". The Ø4.0 hole may be too large for an M4 to grip |
| Washer stack (steps 3, 4) | Fits as shown | The pocket is 13.0 mm tall. Two 1.5 mm washers plus the 10 mm bushing also total 13.0 mm, so there may be no end play and the planets may bind (the CAD's 1.3 mm stand-in washers leave 0.4 mm) |
| Grease (step 8) | Any gear grease | The article adds lubricant without naming it. Check it's safe for the plastic |
| Motor connector direction (step 13) | Not specified | Nothing in the CAD sets it |
