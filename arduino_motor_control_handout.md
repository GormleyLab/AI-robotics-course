# Arduino Motor Control for Robotic Systems

## Smart Prosthetics and Robotic Systems (14:125:444)
**Instructor:** Dr. Adam Gormley  
**Module:** Motors and Drives — Drivers, PWM, Stepper, and Servo Motors

---

## Table of Contents

1. [Introduction to Arduino](#1-introduction-to-arduino)
2. [Motor Fundamentals: Drivers, Steppers, and Servos](#2-motor-fundamentals-drivers-steppers-and-servos)
3. [Wiring the Arduino, A4988 Driver, and Stepper Motor](#3-wiring-the-arduino-a4988-driver-and-stepper-motor)
4. [First Program: Direct Microstepping Control](#4-first-program-direct-microstepping-control)
5. [Motor Control with the AccelStepper Library](#5-motor-control-with-the-accelstepper-library)
6. [Positional Control with Potentiometer and Limit Switch](#6-positional-control-with-potentiometer-and-limit-switch)
7. [Troubleshooting Guide](#7-troubleshooting-guide)
8. [Servo Motor Control with the MG996R](#8-servo-motor-control-with-the-mg996r)

---

## 1. Introduction to Arduino

### 1.1 What is Arduino?

Arduino is an open-source electronics platform combining easy-to-use hardware and software. For this course, we will use the **Arduino Uno Q**, Arduino's newest board that combines a powerful Qualcomm Dragonwing™ QRB2210 microprocessor (MPU) running Debian Linux with an STM32U585 microcontroller (MCU) for real-time control—all in the familiar Uno form factor.

The Arduino Uno Q maintains the same header layout as the classic Arduino Uno, making it compatible with existing shields and tutorials while providing significantly more computational power for AI and robotics applications.

### 1.2 Power Supply Options

The Arduino Uno Q can be powered through several methods:

| Power Source | Voltage Range | Notes |
|--------------|---------------|-------|
| USB-C | 5V | Primary connection for programming and power |
| VIN Pin | 7-24V | External power for high-current applications |
| 5V Pin | 5V (regulated) | Direct 5V input from regulated supply |
| Barrel Jack | 7-12V recommended | Standard DC adapter connection |

**Important:** When driving motors, always use an external power supply. The USB connection alone cannot provide sufficient current for motor operation.

### 1.3 GPIO Pinout Overview

The Arduino Uno Q features the standard Uno header layout:

```
                    DIGITAL PINS (PWM marked with ~)
    ┌─────────────────────────────────────────────────────┐
    │  ~D13  D12  ~D11  ~D10  ~D9  D8  D7  ~D6  ~D5  D4  D3  D2  TX  RX  │
    │                                                                      │
    │  [USB-C]                              [POWER]                        │
    │                                                                      │
    │  A0   A1   A2   A3   A4   A5    VIN  GND  GND  5V  3.3V  RST  IOREF │
    └─────────────────────────────────────────────────────────────────────┘
                    ANALOG PINS
```

**Key Pin Categories:**

| Pin Type | Pins | Function |
|----------|------|----------|
| Digital I/O | D0-D13 | General purpose input/output |
| PWM Output | D3, D5, D6, D9, D10, D11 | Pulse Width Modulation (marked with ~) |
| Analog Input | A0-A5 | 10-bit ADC (0-1023 values) |
| Power | 5V, 3.3V, GND, VIN | Power supply pins |
| Communication | TX (D1), RX (D0) | Serial communication |
| I2C | A4 (SDA), A5 (SCL) | I2C bus communication |
| SPI | D11 (MOSI), D12 (MISO), D13 (SCK) | SPI bus communication |

**Critical Note for Uno Q:** The GPIO pins on the Arduino Uno Q operate at **3.3V logic** (not 5V like the classic Uno). When interfacing with 5V devices, use a logic level shifter to prevent damage to the board. However, the A4988 driver accepts 3.3V-5.5V logic, so direct connection is safe.

---

## 2. Motor Fundamentals: Drivers, Steppers, and Servos

### 2.1 Stepper Motors

A stepper motor is a brushless DC motor whose rotation is divided into discrete angular steps. This allows precise position control without feedback sensors.

**Working Principle:**

Stepper motors consist of two main components:

1. **Rotor** - A permanent magnet shaft
2. **Stator** - Electromagnetic coils surrounding the rotor

By energizing the stator coils in a specific sequence, we create rotating magnetic fields that cause the rotor to move in precise angular increments called "steps."

```
    Step Sequence (Bipolar Motor - Full Step Mode)
    
    Step 1: A+, B+     Step 2: A-, B+     Step 3: A-, B-     Step 4: A+, B-
       ┌─┐                ┌─┐                ┌─┐                ┌─┐
       │N│                │S│                │S│                │N│
    ───┼─┼───          ───┼─┼───          ───┼─┼───          ───┼─┼───
       │S│                │N│                │N│                │S│
       └─┘                └─┘                └─┘                └─┘
```

**NEMA17 Stepper Motor Specifications:**

The NEMA17 is the most common stepper motor for desktop robotics:

| Parameter | Typical Value |
|-----------|---------------|
| Step Angle | 1.8° (200 steps/revolution) |
| Rated Current | 1.5-2.0A per phase |
| Holding Torque | 40-60 N·cm |
| Voltage | 12-24V |
| Phases | 2 (bipolar, 4 wires) |

**Note:** "NEMA17" refers to the faceplate size (1.7 × 1.7 inches), not the motor's electrical characteristics.

### 2.2 Stepper Motor Drivers

Stepper motors cannot be controlled directly from a microcontroller—they require a **driver circuit** that can:

1. Supply sufficient current (1-2A per phase)
2. Control current direction through H-bridges
3. Implement microstepping for smoother motion
4. Provide current limiting for motor protection

**The A4988 Stepper Driver:**

The A4988 is a microstepping driver for bipolar stepper motors with built-in translator for simple step/direction control.

```
         A4988 Pinout
    ┌─────────────────────┐
    │ ENABLE     VMOT    │
    │ MS1        GND     │
    │ MS2        2B      │
    │ MS3        2A      │
    │ RESET      1A      │
    │ SLEEP      1B      │
    │ STEP       VDD     │
    │ DIR        GND     │
    └─────────────────────┘
```

| Pin | Function |
|-----|----------|
| VMOT | Motor power supply (8-35V) |
| GND | Ground (motor and logic share common ground) |
| 1A, 1B | Motor Phase A connections |
| 2A, 2B | Motor Phase B connections |
| VDD | Logic power supply (3.3-5V) |
| STEP | Step input - one pulse = one step |
| DIR | Direction input - HIGH/LOW determines rotation direction |
| MS1, MS2, MS3 | Microstepping selection (see table below) |
| ENABLE | Active LOW - enables driver when LOW |
| SLEEP | Active LOW - put driver to sleep when LOW |
| RESET | Active LOW - resets internal translator |

**Microstepping Resolution:**

| MS1 | MS2 | MS3 | Resolution | Steps/Rev |
|-----|-----|-----|------------|-----------|
| LOW | LOW | LOW | Full step | 200 |
| HIGH | LOW | LOW | Half step | 400 |
| LOW | HIGH | LOW | Quarter step | 800 |
| HIGH | HIGH | LOW | Eighth step | 1600 |
| HIGH | HIGH | HIGH | Sixteenth step | 3200 |

Microstepping provides smoother motion by energizing coils at intermediate current levels, creating sub-step positions.

### 2.3 Servo Motors

Servo motors are closed-loop systems with built-in position feedback (typically a potentiometer) and control circuitry. They're controlled by PWM signals where pulse width determines angular position.

**PWM Control Signal:**

```
    Servo Control Signal (50Hz - 20ms period)
    
    0° Position:        90° Position:       180° Position:
    ┌─┐                 ┌──┐                ┌───┐
    │ │                 │  │                │   │
    ┘ └─────────────    ┘  └────────────    ┘   └───────────
    |1ms|   19ms   |    |1.5ms|  18.5ms|    |2ms|   18ms   |
    
    └────── 20ms ──────┘
```

| Pulse Width | Servo Position |
|-------------|----------------|
| 0.5-1.0 ms | 0° |
| 1.5 ms | 90° (center) |
| 2.0-2.5 ms | 180° |

**Common Servo Motors:**

| Model | Torque | Current | Weight | Use Case |
|-------|--------|---------|--------|----------|
| SG90 | 1.6 kg·cm | 100-650mA | 9g | Light duty, small mechanisms |
| MG996R | 13 kg·cm | 500-2500mA | 55g | Medium duty, robot arms |

---

## 3. Wiring the Arduino, A4988 Driver, and Stepper Motor

### 3.1 Required Components

- Arduino Uno Q (or compatible Arduino board)
- A4988 Stepper Driver Module
- NEMA17 Stepper Motor
- 12V DC Power Supply (2A minimum)
- 100µF electrolytic capacitor
- Breadboard and jumper wires

### 3.2 Circuit Diagram

```
                                    ┌─────────────────┐
                                    │   12V Power     │
                                    │    Supply       │
                                    └────┬───────┬────┘
                                         │       │
                                         │       │
    ┌─────────────────┐            ┌─────┴───────┴─────┐
    │                 │            │                   │
    │  Arduino Uno Q  │            │   100µF Cap       │
    │                 │            │   (across VMOT    │
    │                 │            │    and GND)       │
    │   D2 ──────────────────────────► STEP               │
    │                 │            │                   │
    │   D5 ──────────────────────────► DIR                │
    │                 │            │                   │
    │   5V ──────────────────────────► VDD                │
    │                 │            │     A4988         │
    │   GND ─────────────────────────► GND   Driver       │
    │                 │            │                   │
    │                 │            │   VMOT ◄─────────── 12V+
    │                 │            │   GND  ◄─────────── 12V-
    │                 │            │                   │
    └─────────────────┘            │   1A ────────────► Motor Coil A+
                                   │   1B ────────────► Motor Coil A-
                                   │   2A ────────────► Motor Coil B+
                                   │   2B ────────────► Motor Coil B-
                                   │                   │
                                   │ RESET ──┬── SLEEP │ (Connect together)
                                   │         │         │
                                   └─────────┴─────────┘
```

### 3.3 Wiring Steps

1. **Connect the capacitor:** Place a 100µF electrolytic capacitor across VMOT and GND on the A4988 (observe polarity!). This protects against voltage spikes.

2. **Connect power to the driver:**
   - VMOT → 12V positive from power supply
   - GND (motor side) → 12V negative from power supply
   - VDD → Arduino 5V pin
   - GND (logic side) → Arduino GND

3. **Connect control signals:**
   - STEP → Arduino D2
   - DIR → Arduino D5

4. **Enable the driver:**
   - Connect RESET and SLEEP pins together (both pulled HIGH internally)
   - Leave ENABLE pin unconnected (internally pulled LOW = enabled)

5. **Connect the stepper motor:**
   - Identify motor phases using a multimeter (continuity test)
   - Phase A wires → 1A and 1B
   - Phase B wires → 2A and 2B

**Finding Motor Phases:**
```
Method 1: Continuity Test
- Wires with continuity between them are one phase
- NEMA17 typically: Black-Green = Phase A, Red-Blue = Phase B

Method 2: Rotation Resistance
- Short two wires together
- Try to rotate the shaft by hand
- If harder to turn, those wires are one phase
```

### 3.4 Setting the Current Limit

**CRITICAL:** Before powering the motor, you must set the A4988 current limit to match your motor's rated current.

**Method: Reference Voltage Measurement**

1. Power only the logic side (connect VDD and GND, NOT VMOT)
2. Measure voltage between GND and the adjustment potentiometer
3. Calculate using: **Current Limit = Vref / (8 × Rcs)**

Where Rcs is the current sense resistor value (typically 0.1Ω for most modules):

| Desired Current | Required Vref (Rcs=0.1Ω) |
|-----------------|--------------------------|
| 0.5A | 0.4V |
| 1.0A | 0.8V |
| 1.5A | 1.2V |
| 2.0A | 1.6V |

Adjust the potentiometer clockwise to increase current, counter-clockwise to decrease.

---

## 4. First Program: Direct Microstepping Control

### 4.1 Basic Stepper Control Without Libraries

This example demonstrates fundamental stepper motor control by directly generating step pulses. We start with full-step mode (no microstepping pins connected, defaulting to LOW).

```cpp
/*
 * Basic Stepper Motor Control - No Library
 * Smart Prosthetics and Robotic Systems
 * 
 * This program demonstrates direct control of a stepper motor
 * using the A4988 driver by generating step pulses manually.
 * Full-step mode: 200 steps per revolution
 */

// Pin definitions
#define STEP_PIN 2    // Step signal to A4988
#define DIR_PIN  5    // Direction signal to A4988

// Motor parameters (full-step mode)
#define STEPS_PER_REV 200   // 1.8° per step = 200 steps/revolution

void setup() {
  // Configure pins as outputs
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
}

void loop() {
  // Rotate clockwise one full revolution
  digitalWrite(DIR_PIN, HIGH);  // Set direction to clockwise
  
  for (int i = 0; i < STEPS_PER_REV; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(1000);    // Pulse width (minimum ~1µs)
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(1000);    // Time between steps (controls speed)
  }
  
  delay(1000);  // Pause for 1 second
  
  // Rotate counter-clockwise one full revolution
  digitalWrite(DIR_PIN, LOW);   // Set direction to counter-clockwise
  
  for (int i = 0; i < STEPS_PER_REV; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(1000);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(1000);
  }
  
  delay(1000);  // Pause for 1 second
}
```

### 4.2 Understanding the Timing

The step pulse timing controls motor speed:

```
    Step Pulse Timing
    
         ┌───┐       ┌───┐       ┌───┐
    HIGH │   │       │   │       │   │
    ─────┘   └───────┘   └───────┘   └─────
    LOW      
         |←→|←─────→|
          tw    td
    
    tw = Pulse width (HIGH time) - minimum ~1µs for A4988
    td = Delay time (LOW time) - determines step frequency
    
    Step Frequency = 1 / (tw + td)
    
    Example: tw = 1000µs, td = 1000µs
    Frequency = 1 / 0.002s = 500 steps/second
    Speed = 500 / 200 = 2.5 revolutions/second = 150 RPM
```

### 4.3 Variable Speed Control

```cpp
/*
 * Variable Speed Stepper Control
 * Demonstrates changing motor speed dynamically
 * Full-step mode: 200 steps per revolution
 */

#define STEP_PIN 2
#define DIR_PIN  5
#define STEPS_PER_REV 200

// Speed settings (delay in microseconds between steps)
#define FAST_DELAY   500    // ~1000 steps/sec
#define MEDIUM_DELAY 1500   // ~333 steps/sec
#define SLOW_DELAY   3000   // ~166 steps/sec

void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
}

// Function to rotate motor a specified number of steps at given speed
void rotateSteps(int steps, int stepDelay) {
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(stepDelay);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(stepDelay);
  }
}

void loop() {
  digitalWrite(DIR_PIN, HIGH);  // Clockwise
  
  // Slow speed - 1/4 revolution
  rotateSteps(STEPS_PER_REV / 4, SLOW_DELAY);
  delay(500);
  
  // Medium speed - 1/4 revolution
  rotateSteps(STEPS_PER_REV / 4, MEDIUM_DELAY);
  delay(500);
  
  // Fast speed - 1/4 revolution
  rotateSteps(STEPS_PER_REV / 4, FAST_DELAY);
  delay(500);
  
  // Fast speed - 1/4 revolution
  rotateSteps(STEPS_PER_REV / 4, FAST_DELAY);
  delay(2000);
  
  // Reverse direction
  digitalWrite(DIR_PIN, LOW);  // Counter-clockwise
  rotateSteps(STEPS_PER_REV, MEDIUM_DELAY);
  delay(2000);
}
```

### 4.4 Quarter-Step Microstepping Mode

Microstepping provides smoother motion by dividing each full step into smaller increments. For **quarter-step mode**, we need to set **MS2 HIGH** while leaving MS1 and MS3 LOW. This gives us **800 steps per revolution** instead of 200.

**Updated Wiring for Quarter-Step Mode:**

Add one additional wire to your circuit:
- Arduino D4 → A4988 MS2 pin

```
    Additional connection for quarter-step mode:
    
    Arduino D4 ──────────────────► MS2 (A4988)
    
    MS1 and MS3 remain unconnected (internally pulled LOW)
```

**Quarter-Step Control Program:**

```cpp
/*
 * Quarter-Step Microstepping Control
 * Smart Prosthetics and Robotic Systems
 * 
 * This program demonstrates quarter-step microstepping for smoother motion.
 * Quarter-step mode: 800 steps per revolution (4x full-step resolution)
 */

// Pin definitions
#define STEP_PIN 2    // Step signal to A4988
#define DIR_PIN  5    // Direction signal to A4988
#define MS2_PIN  4    // Microstepping pin 2 (for quarter-step mode)

// Motor parameters (quarter-step mode)
#define STEPS_PER_REV 800   // 200 * 4 = 800 steps/revolution in quarter-step

void setup() {
  // Configure pins as outputs
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(MS2_PIN, OUTPUT);
  
  // Enable quarter-step mode: MS1=LOW, MS2=HIGH, MS3=LOW
  // MS1 and MS3 are internally pulled LOW, so we only need to set MS2
  digitalWrite(MS2_PIN, HIGH);
}

// Function to rotate motor a specified number of steps at given speed
void rotateSteps(int steps, int stepDelay) {
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(stepDelay);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(stepDelay);
  }
}

void loop() {
  // Rotate clockwise one full revolution (800 steps in quarter-step mode)
  digitalWrite(DIR_PIN, HIGH);
  rotateSteps(STEPS_PER_REV, 500);  // 500µs delay = smooth motion
  
  delay(1000);
  
  // Rotate counter-clockwise one full revolution
  digitalWrite(DIR_PIN, LOW);
  rotateSteps(STEPS_PER_REV, 500);
  
  delay(1000);
  
  // Demonstrate precise positioning: rotate exactly 90 degrees (1/4 turn)
  // 90° = 800 / 4 = 200 steps in quarter-step mode
  digitalWrite(DIR_PIN, HIGH);
  rotateSteps(200, 400);  // Quarter turn clockwise
  
  delay(500);
  
  rotateSteps(200, 400);  // Another quarter turn
  
  delay(500);
  
  rotateSteps(200, 400);  // Another quarter turn
  
  delay(500);
  
  rotateSteps(200, 400);  // Final quarter turn (back to start)
  
  delay(2000);
}
```

**Benefits of Quarter-Step Mode:**

| Aspect | Full Step (200/rev) | Quarter Step (800/rev) |
|--------|---------------------|------------------------|
| Resolution | 1.8° per step | 0.45° per step |
| Smoothness | Noticeable stepping | Much smoother motion |
| Torque | Full torque | Slightly reduced |
| Speed | Higher max RPM | Lower max RPM |
| Noise | Louder | Quieter |

**When to Use Quarter-Step:**
- When smooth motion is important (gripper positioning, camera movements)
- When precise positioning is required
- When reducing motor noise is desirable

**Important:** From this point forward, all programs in this handout will use **quarter-step mode (800 steps/revolution)**. Make sure MS2 is connected to D4 and set HIGH.

---

## 5. Motor Control with the AccelStepper Library

### 5.1 Introduction to AccelStepper

The AccelStepper library provides advanced stepper motor control including:

- Acceleration and deceleration profiles
- Speed control
- Position tracking
- Non-blocking operation

### 5.2 Installing the Library

1. Open Arduino IDE
2. Go to **Sketch → Include Library → Manage Libraries**
3. Search for "AccelStepper"
4. Install "AccelStepper by Mike McCauley"

### 5.3 Basic AccelStepper Example

```cpp
/*
 * AccelStepper Basic Example
 * Smart Prosthetics and Robotic Systems
 * 
 * Demonstrates basic motor control with acceleration/deceleration
 * Using quarter-step mode: 800 steps per revolution
 */

#include <AccelStepper.h>

// Define stepper motor connection type
// Type 1 = Driver (step/dir pins)
#define MOTOR_INTERFACE_TYPE 1

// Pin definitions
#define STEP_PIN 2
#define DIR_PIN  5
#define MS2_PIN  4

// Create stepper object
// AccelStepper(interface, stepPin, dirPin)
AccelStepper stepper(MOTOR_INTERFACE_TYPE, STEP_PIN, DIR_PIN);

void setup() {
  // Enable quarter-step mode
  pinMode(MS2_PIN, OUTPUT);
  digitalWrite(MS2_PIN, HIGH);
  
  // Configure motor parameters
  stepper.setMaxSpeed(2000);      // Maximum speed in steps/second
  stepper.setAcceleration(1000);  // Acceleration in steps/second^2
}

void loop() {
  // Move to position 3200 (4 revolutions in quarter-step mode)
  stepper.moveTo(3200);
  
  // Run until target position reached (blocking)
  while (stepper.distanceToGo() != 0) {
    stepper.run();
  }
  
  delay(1000);
  
  // Move back to position 0
  stepper.moveTo(0);
  
  while (stepper.distanceToGo() != 0) {
    stepper.run();
  }
  
  delay(1000);
}
```

### 5.4 Key AccelStepper Functions

| Function | Description |
|----------|-------------|
| `setMaxSpeed(speed)` | Set maximum speed (steps/sec) |
| `setAcceleration(accel)` | Set acceleration (steps/sec²) |
| `setSpeed(speed)` | Set constant speed for runSpeed() |
| `moveTo(position)` | Set target absolute position |
| `move(relative)` | Set target relative to current position |
| `run()` | Execute one step if needed (non-blocking) |
| `runSpeed()` | Execute step at constant speed |
| `runToPosition()` | Block until position reached |
| `currentPosition()` | Get current position |
| `distanceToGo()` | Steps remaining to target |
| `setCurrentPosition(pos)` | Reset position counter |

### 5.5 Non-Blocking Motor Control

```cpp
/*
 * Non-Blocking AccelStepper Control
 * Motor moves while other code executes
 * Using quarter-step mode: 800 steps per revolution
 */

#include <AccelStepper.h>

#define STEP_PIN 2
#define DIR_PIN  5
#define MS2_PIN  4

AccelStepper stepper(1, STEP_PIN, DIR_PIN);

// LED for demonstrating non-blocking operation
#define LED_PIN 13
unsigned long previousMillis = 0;
const long interval = 200;  // LED blink interval
bool ledState = LOW;

void setup() {
  // Enable quarter-step mode
  pinMode(MS2_PIN, OUTPUT);
  digitalWrite(MS2_PIN, HIGH);
  
  pinMode(LED_PIN, OUTPUT);
  
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(500);
  stepper.moveTo(4000);  // Set initial target (5 revolutions)
}

void loop() {
  // Non-blocking motor control - call run() as frequently as possible
  stepper.run();
  
  // Other tasks can execute while motor is moving
  // Example: Blink LED independently
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState);
  }
  
  // Check if motor reached target, then reverse
  if (stepper.distanceToGo() == 0) {
    delay(500);  // Brief pause at each end
    stepper.moveTo(-stepper.currentPosition());  // Reverse direction
  }
}
```

---

## 6. Positional Control with Potentiometer and Limit Switch

### 6.1 Components for Position Feedback

**10kΩ Potentiometer:**
- Analog position sensor
- Voltage divider output proportional to rotation
- Connect: One end to GND, other to 5V, wiper to analog input

**KW12-3 Limit Switch (Microswitch):**

The KW12-3 is a mechanical microswitch used for detecting end-of-travel positions. Understanding its three terminals is essential for proper wiring.

```
    KW12-3 Limit Switch Terminal Layout
    
         Lever/Actuator
              │
              ▼
        ┌───────────┐
        │    ●      │ ◄── Pivot point
        │   ╱       │
        │  ╱        │
        │ ●─────────│──── COM (Common)
        │           │
        │ ●─────────│──── NC (Normally Closed)
        │           │
        │ ●─────────│──── NO (Normally Open)
        └───────────┘
```

**Understanding the Three Terminals:**

| Terminal | Name | Description |
|----------|------|-------------|
| **COM** | Common | The "moving" contact - always connect your signal wire here |
| **NC** | Normally Closed | Connected to COM when switch is NOT pressed |
| **NO** | Normally Open | Connected to COM when switch IS pressed |

**How It Works:**

```
    Switch NOT Pressed:              Switch PRESSED:
    
    COM ──●──── NC                   COM ────── NC
           ╲                              ╲
            ○ NO                      ●──── NO
    
    (COM connects to NC)             (COM connects to NO)
```

**Which Terminals to Use?**

For homing and safety limit applications, we use **COM** and **NC** (Normally Closed):

- **Why NC?** If a wire breaks or comes loose, the circuit opens (same as switch pressed), triggering a safety stop. This is called "fail-safe" design.
- Connect **COM** to your Arduino input pin (D7)
- Connect **NC** to **GND**
- Enable the internal pull-up resistor on D7

**Circuit Behavior:**
- Switch NOT pressed → COM-NC connected → Pin reads LOW (pulled to GND)
- Switch PRESSED → COM-NC disconnected → Pin reads HIGH (pull-up resistor)

**Wait, that seems backwards!** You're right—with the wiring above, the pin reads LOW normally and HIGH when pressed. In our code, we'll check for **HIGH** to detect the switch being triggered. Alternatively, you can swap the logic in code or use NO instead of NC (but NC is safer for limit switches).

### 6.2 Wiring Diagram with Sensors

```
                     ┌─────────────────┐
                     │  Arduino Uno Q  │
                     │                 │
    Potentiometer    │   A0 ◄─────────── Wiper (middle pin)
    ┌───────────┐    │                 │
    │     ┌─┐   │    │   5V ─────────► Left pin
    │     │W│───┼────│                 │
    │     └─┘   │    │   GND ────────► Right pin
    └───────────┘    │                 │
                     │                 │
    Limit Switch     │   D7 ◄─────────── COM (Common)
    (KW12-3)         │                 │
                     │   GND ────────► NC (Normally Closed)
    ┌─────┐          │                 │
    │ [L] │          │   (NO terminal left unconnected)
    │     │──COM     │                 │
    │     │──NC      │   D4 ──────────► MS2 (A4988)
    │     │──NO      │   D2 ──────────► STEP (A4988)
    └─────┘          │   D5 ──────────► DIR (A4988)
                     │                 │
                     └─────────────────┘
                     
    Note: Enable internal pull-up on D7 in code: pinMode(D7, INPUT_PULLUP)
```

### 6.3 Potentiometer Speed Control

```cpp
/*
 * Potentiometer-Controlled Stepper Speed
 * Smart Prosthetics and Robotic Systems
 * 
 * Use a potentiometer to control motor speed in real-time
 * Using quarter-step mode: 800 steps per revolution
 */

#include <AccelStepper.h>

#define STEP_PIN 2
#define DIR_PIN  5
#define MS2_PIN  4
#define POT_PIN  A0

AccelStepper stepper(1, STEP_PIN, DIR_PIN);

void setup() {
  // Enable quarter-step mode
  pinMode(MS2_PIN, OUTPUT);
  digitalWrite(MS2_PIN, HIGH);
  
  stepper.setMaxSpeed(2000);
}

void loop() {
  // Read potentiometer (0-1023)
  int potValue = analogRead(POT_PIN);
  
  // Map to speed range (0 to max speed)
  // Values below 50 = stopped, above = proportional speed
  int motorSpeed = 0;
  
  if (potValue > 50) {
    motorSpeed = map(potValue, 50, 1023, 200, 2000);
  }
  
  // Set speed and run
  stepper.setSpeed(motorSpeed);
  stepper.runSpeed();
}
```

### 6.4 Potentiometer Position Control

```cpp
/*
 * Potentiometer Position Control
 * Map potentiometer position to stepper motor position
 * Using quarter-step mode: 800 steps per revolution
 */

#include <AccelStepper.h>

#define STEP_PIN 2
#define DIR_PIN  5
#define MS2_PIN  4
#define POT_PIN  A0

#define MAX_POSITION 3200  // Maximum steps from home (4 revolutions)

AccelStepper stepper(1, STEP_PIN, DIR_PIN);

void setup() {
  // Enable quarter-step mode
  pinMode(MS2_PIN, OUTPUT);
  digitalWrite(MS2_PIN, HIGH);
  
  stepper.setMaxSpeed(1600);
  stepper.setAcceleration(800);
}

void loop() {
  // Read potentiometer
  int potValue = analogRead(POT_PIN);
  
  // Map pot value (0-1023) to position range (0 to MAX_POSITION)
  long targetPosition = map(potValue, 0, 1023, 0, MAX_POSITION);
  
  // Move to target position
  stepper.moveTo(targetPosition);
  stepper.run();
}
```

### 6.5 Homing with Limit Switch

```cpp
/*
 * Homing Sequence with Limit Switch
 * Smart Prosthetics and Robotic Systems
 * 
 * Motor moves until limit switch is triggered, establishing home position
 * Using quarter-step mode: 800 steps per revolution
 * 
 * Limit switch wiring: COM to D7, NC to GND
 * - Switch NOT pressed: D7 reads LOW (COM connected to NC/GND)
 * - Switch PRESSED: D7 reads HIGH (COM disconnected, pull-up active)
 */

#include <AccelStepper.h>

#define STEP_PIN 2
#define DIR_PIN  5
#define MS2_PIN  4
#define LIMIT_SWITCH_PIN 7

#define HOMING_SPEED -400     // Negative = toward home direction

AccelStepper stepper(1, STEP_PIN, DIR_PIN);

bool isHomed = false;

void setup() {
  // Enable quarter-step mode
  pinMode(MS2_PIN, OUTPUT);
  digitalWrite(MS2_PIN, HIGH);
  
  // Configure limit switch with internal pull-up
  // With NC wiring: LOW = not pressed, HIGH = pressed
  pinMode(LIMIT_SWITCH_PIN, INPUT_PULLUP);
  
  stepper.setMaxSpeed(1600);
  stepper.setAcceleration(800);
  
  // Perform homing on startup
  homeMotor();
}

void homeMotor() {
  // Move toward home until limit switch is triggered
  stepper.setSpeed(HOMING_SPEED);
  
  // Keep moving until switch is pressed (reads HIGH with NC wiring)
  while (digitalRead(LIMIT_SWITCH_PIN) == LOW) {
    stepper.runSpeed();
  }
  
  // Stop immediately
  stepper.stop();
  stepper.runToPosition();
  
  // Back off slightly from the switch
  stepper.move(100);  // Move 100 steps away from switch
  stepper.runToPosition();
  
  // Set this as home position (0)
  stepper.setCurrentPosition(0);
  
  isHomed = true;
}

void loop() {
  if (!isHomed) return;
  
  // Example movement after homing
  stepper.moveTo(1600);  // Move 2 revolutions from home
  stepper.runToPosition();
  delay(1000);
  
  stepper.moveTo(800);   // Move to 1 revolution position
  stepper.runToPosition();
  delay(1000);
  
  stepper.moveTo(0);     // Return home
  stepper.runToPosition();
  delay(2000);
}
```

### 6.6 Complete System: Position Control with Limits

```cpp
/*
 * Complete Position Control System
 * Features: Homing, potentiometer control, soft limits, limit switch safety
 * Using quarter-step mode: 800 steps per revolution
 */

#include <AccelStepper.h>

#define STEP_PIN 2
#define DIR_PIN  5
#define MS2_PIN  4
#define POT_PIN  A0
#define LIMIT_SWITCH_PIN 7
#define LED_PIN 13

// Position limits (after homing)
#define MIN_POSITION 0
#define MAX_POSITION 6400  // 8 revolutions in quarter-step mode

AccelStepper stepper(1, STEP_PIN, DIR_PIN);

// System state
bool isHomed = false;
bool limitTriggered = false;

void setup() {
  // Enable quarter-step mode
  pinMode(MS2_PIN, OUTPUT);
  digitalWrite(MS2_PIN, HIGH);
  
  pinMode(LIMIT_SWITCH_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  
  stepper.setMaxSpeed(1600);
  stepper.setAcceleration(1000);
  
  // Auto-home on startup
  homeMotor();
}

void homeMotor() {
  digitalWrite(LED_PIN, HIGH);  // LED on during homing
  
  stepper.setSpeed(-600);
  
  // Move until limit switch triggered (HIGH with NC wiring)
  while (digitalRead(LIMIT_SWITCH_PIN) == LOW) {
    stepper.runSpeed();
  }
  
  stepper.stop();
  delay(100);
  
  // Back off from switch
  stepper.move(200);
  stepper.runToPosition();
  
  stepper.setCurrentPosition(0);
  isHomed = true;
  
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  // Check limit switch (safety)
  if (digitalRead(LIMIT_SWITCH_PIN) == HIGH) {
    if (!limitTriggered) {
      stepper.stop();
      limitTriggered = true;
    }
    // Only allow movement away from limit
    if (stepper.distanceToGo() < 0) {
      stepper.stop();
    }
  } else {
    limitTriggered = false;
  }
  
  if (!isHomed) {
    // Blink LED to indicate not homed
    digitalWrite(LED_PIN, (millis() / 500) % 2);
    return;
  }
  
  // Read potentiometer and map to position
  int potValue = analogRead(POT_PIN);
  long targetPosition = map(potValue, 0, 1023, MIN_POSITION, MAX_POSITION);
  
  // Apply soft limits
  targetPosition = constrain(targetPosition, MIN_POSITION, MAX_POSITION);
  
  // Update target and run
  stepper.moveTo(targetPosition);
  stepper.run();
}
```

---

## 7. Troubleshooting Guide

### 7.1 Common Problems and Solutions

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| Motor doesn't move | No power to driver | Check VMOT connection and power supply |
| | Driver not enabled | Ensure ENABLE pin is LOW (or unconnected) |
| | Wrong wiring | Verify phase connections with multimeter |
| | Current limit too low | Increase Vref with potentiometer |
| Motor vibrates but doesn't rotate | Phases swapped | Swap one pair of motor wires (1A↔1B or 2A↔2B) |
| | One phase disconnected | Check all four motor connections |
| Motor runs but skips steps | Speed too high | Reduce speed, add acceleration |
| | Current limit too low | Increase current limit |
| | Load too heavy | Use higher-torque motor or gear reduction |
| Motor gets very hot | Current limit too high | Reduce Vref to match motor rating |
| | Continuous operation | Normal - add heatsink or reduce duty cycle |
| Arduino resets when motor runs | Power supply insufficient | Use separate power for motor (not USB) |
| | Missing capacitor | Add 100µF capacitor across VMOT and GND |
| Erratic movement | Loose connections | Secure all wiring |
| | Electrical noise | Add decoupling capacitors, use shielded cables |
| Limit switch not working | Wrong terminals used | Verify COM and NC connections |
| | Pull-up not enabled | Add INPUT_PULLUP in pinMode() |
| | Wiring reversed | Check COM goes to Arduino, NC goes to GND |

### 7.2 Diagnostic Code

```cpp
/*
 * Stepper Motor Diagnostic Test
 * Run this to verify your hardware setup
 * Using quarter-step mode: 800 steps per revolution
 */

#include <AccelStepper.h>

#define STEP_PIN 2
#define DIR_PIN  5
#define MS2_PIN  4
#define LED_PIN  13

AccelStepper stepper(1, STEP_PIN, DIR_PIN);

void setup() {
  // Enable quarter-step mode
  pinMode(MS2_PIN, OUTPUT);
  digitalWrite(MS2_PIN, HIGH);
  
  pinMode(LED_PIN, OUTPUT);
  
  stepper.setMaxSpeed(400);
  stepper.setAcceleration(200);
  
  // Visual indicator that test is starting
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
  
  // Test 1: Direction control
  // LED ON = clockwise rotation
  digitalWrite(LED_PIN, HIGH);
  stepper.setSpeed(200);
  unsigned long start = millis();
  while (millis() - start < 2000) stepper.runSpeed();
  
  delay(500);
  
  // LED OFF = counter-clockwise rotation
  digitalWrite(LED_PIN, LOW);
  stepper.setSpeed(-200);
  start = millis();
  while (millis() - start < 2000) stepper.runSpeed();
  
  delay(1000);
  
  // Test 2: Position control
  // LED blink = moving to position
  stepper.setCurrentPosition(0);
  stepper.moveTo(800);  // One full revolution
  
  while (stepper.distanceToGo() != 0) {
    stepper.run();
    digitalWrite(LED_PIN, (millis() / 100) % 2);
  }
  
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  
  stepper.moveTo(0);
  while (stepper.distanceToGo() != 0) {
    stepper.run();
    digitalWrite(LED_PIN, (millis() / 100) % 2);
  }
  
  // Test complete - rapid LED blink
  for (int i = 0; i < 10; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(100);
    digitalWrite(LED_PIN, LOW);
    delay(100);
  }
}

void loop() {
  // Empty - diagnostic runs once in setup
  // Steady LED = test complete
  digitalWrite(LED_PIN, HIGH);
}
```

### 7.3 Best Practices

1. **Always use external power** for motors - never power from USB alone
2. **Set current limit before first run** to protect motor and driver
3. **Add decoupling capacitors** across power connections
4. **Start with low speeds** and gradually increase
5. **Implement acceleration** to prevent missed steps
6. **Use limit switches** for safety in position-controlled systems
7. **Ground everything to a common point** to prevent noise issues
8. **Keep motor wires short** or use shielded cable for long runs
9. **Use quarter-step mode** for smoother, quieter operation
10. **Wire limit switches NC (Normally Closed)** for fail-safe operation

---

## 8. Servo Motor Control with the MG996R

### 8.1 Introduction to the MG996R

The MG996R is a high-torque servo motor commonly used in robotic arms and grippers. Unlike stepper motors that rotate continuously, servos are designed to move to specific angular positions (typically 0° to 180°).

**MG996R Specifications:**

| Parameter | Value |
|-----------|-------|
| Operating Voltage | 4.8V - 7.2V |
| Stall Torque | 9.4 kg·cm (4.8V) / 11 kg·cm (6V) |
| Operating Speed | 0.17 sec/60° (4.8V) / 0.14 sec/60° (6V) |
| Rotation Range | 0° - 180° (can vary by model) |
| PWM Signal | 50Hz (20ms period) |
| Pulse Width | 500µs - 2500µs |
| Weight | 55g |
| Gear Type | Metal gears |

**Important Power Considerations:**

The MG996R can draw **up to 2.5A under load**. This is far more than the Arduino can supply from its 5V pin. **You must use an external power supply** for the servo.

### 8.2 Wiring the MG996R Servo

**Required Components:**
- MG996R Servo Motor
- 5V-6V DC Power Supply (2A minimum recommended)
- Arduino Uno Q
- Breadboard and jumper wires

**Servo Wire Colors:**

| Wire Color | Function |
|------------|----------|
| Brown (or Black) | Ground (GND) |
| Red | Power (VCC) - 5V to 6V |
| Orange (or Yellow/White) | Signal (PWM) |

**Circuit Diagram:**

```
                                    ┌─────────────────┐
                                    │   5V-6V Power   │
                                    │    Supply       │
                                    │   (2A+ rated)   │
                                    └────┬───────┬────┘
                                         │       │
                                         │ +     │ -
                                         │       │
    ┌─────────────────┐                  │       │
    │                 │                  │       │
    │  Arduino Uno Q  │                  │       │
    │                 │                  │       │
    │   D9 ───────────────────────────────────────┐
    │   (PWM)         │                  │       │ │
    │                 │                  │       │ │
    │   GND ──────────────────────────────┼───────┤ │
    │                 │                  │       │ │
    └─────────────────┘                  │       │ │
                                         │       │ │
                                    ┌────┴───┬───┴─┴──┐
                                    │  RED   │ BROWN  │ ORANGE
                                    │ (VCC)  │ (GND)  │ (Signal)
                                    │        │        │
                                    └────────┴────────┘
                                         MG996R
                                         Servo
```

**Critical Wiring Notes:**

1. **Common Ground:** The Arduino GND and external power supply GND **must be connected together**. This provides a common reference for the PWM signal.

2. **Never power from Arduino 5V:** The Arduino's 5V pin cannot supply enough current for the MG996R. Always use an external supply.

3. **PWM Pin:** Use a PWM-capable pin (D9 recommended). On the Arduino Uno Q, PWM pins are marked with ~ (D3, D5, D6, D9, D10, D11).

### 8.3 Basic Servo Control with the Servo Library

Arduino includes a built-in Servo library that makes controlling servos simple.

```cpp
/*
 * Basic MG996R Servo Control
 * Smart Prosthetics and Robotic Systems
 * 
 * Demonstrates basic servo motor positioning
 */

#include <Servo.h>

#define SERVO_PIN 9  // PWM pin for servo signal

Servo myServo;

void setup() {
  myServo.attach(SERVO_PIN);
  
  // Move to center position on startup
  myServo.write(90);
  delay(1000);
}

void loop() {
  // Move to 0 degrees
  myServo.write(0);
  delay(1000);
  
  // Move to 90 degrees (center)
  myServo.write(90);
  delay(1000);
  
  // Move to 180 degrees
  myServo.write(180);
  delay(1000);
  
  // Move to 90 degrees (center)
  myServo.write(90);
  delay(1000);
}
```

### 8.4 Smooth Servo Movement

Servos move quickly to their target position, which can cause jerky motion. For smoother movement, we can incrementally step through positions.

```cpp
/*
 * Smooth Servo Movement
 * Smart Prosthetics and Robotic Systems
 * 
 * Demonstrates gradual servo movement for smoother motion
 */

#include <Servo.h>

#define SERVO_PIN 9

Servo myServo;

int currentPosition = 90;  // Track current position

void setup() {
  myServo.attach(SERVO_PIN);
  myServo.write(currentPosition);
  delay(500);
}

// Function to smoothly move servo to target position
void smoothMove(int targetPosition, int stepDelay) {
  // Constrain target to valid range
  targetPosition = constrain(targetPosition, 0, 180);
  
  if (targetPosition > currentPosition) {
    // Moving clockwise
    for (int pos = currentPosition; pos <= targetPosition; pos++) {
      myServo.write(pos);
      delay(stepDelay);
    }
  } else {
    // Moving counter-clockwise
    for (int pos = currentPosition; pos >= targetPosition; pos--) {
      myServo.write(pos);
      delay(stepDelay);
    }
  }
  
  currentPosition = targetPosition;
}

void loop() {
  // Smooth move to 0 degrees (15ms per degree = slow)
  smoothMove(0, 15);
  delay(500);
  
  // Smooth move to 180 degrees (10ms per degree = medium)
  smoothMove(180, 10);
  delay(500);
  
  // Smooth move to 90 degrees (5ms per degree = fast)
  smoothMove(90, 5);
  delay(1000);
}
```

### 8.5 Potentiometer-Controlled Servo

```cpp
/*
 * Potentiometer-Controlled Servo
 * Smart Prosthetics and Robotic Systems
 * 
 * Use a potentiometer to control servo position in real-time
 */

#include <Servo.h>

#define SERVO_PIN 9
#define POT_PIN   A0

Servo myServo;

void setup() {
  myServo.attach(SERVO_PIN);
}

void loop() {
  // Read potentiometer (0-1023)
  int potValue = analogRead(POT_PIN);
  
  // Map to servo range (0-180 degrees)
  int angle = map(potValue, 0, 1023, 0, 180);
  
  // Move servo to position
  myServo.write(angle);
  
  // Small delay for stability
  delay(15);
}
```

### 8.6 Combined Stepper and Servo Control

This example demonstrates controlling both a stepper motor (for arm movement) and a servo motor (for gripper) in a coordinated system.

```cpp
/*
 * Combined Stepper and Servo Control
 * Smart Prosthetics and Robotic Systems
 * 
 * Coordinated control of stepper motor (arm) and servo (gripper)
 * Stepper: Quarter-step mode, 800 steps per revolution
 * Servo: MG996R for gripper open/close
 */

#include <AccelStepper.h>
#include <Servo.h>

// Stepper motor pins
#define STEP_PIN 2
#define DIR_PIN  5
#define MS2_PIN  4

// Servo pin
#define SERVO_PIN 9

// Gripper positions
#define GRIPPER_OPEN   30    // Degrees for open position
#define GRIPPER_CLOSED 120   // Degrees for closed position

AccelStepper stepper(1, STEP_PIN, DIR_PIN);
Servo gripper;

int gripperPosition = GRIPPER_OPEN;

void setup() {
  // Initialize stepper (quarter-step mode)
  pinMode(MS2_PIN, OUTPUT);
  digitalWrite(MS2_PIN, HIGH);
  
  stepper.setMaxSpeed(1600);
  stepper.setAcceleration(800);
  
  // Initialize servo
  gripper.attach(SERVO_PIN);
  gripper.write(GRIPPER_OPEN);
  delay(500);
}

// Smooth gripper movement
void moveGripper(int targetAngle, int stepDelay) {
  targetAngle = constrain(targetAngle, 0, 180);
  
  if (targetAngle > gripperPosition) {
    for (int pos = gripperPosition; pos <= targetAngle; pos++) {
      gripper.write(pos);
      delay(stepDelay);
    }
  } else {
    for (int pos = gripperPosition; pos >= targetAngle; pos--) {
      gripper.write(pos);
      delay(stepDelay);
    }
  }
  gripperPosition = targetAngle;
}

// Move arm to position and wait
void moveArm(long position) {
  stepper.moveTo(position);
  while (stepper.distanceToGo() != 0) {
    stepper.run();
  }
}

void loop() {
  // Sequence: Move arm, close gripper, move arm, open gripper
  
  // Step 1: Move arm to pickup position
  moveArm(1600);  // 2 revolutions from home
  delay(200);
  
  // Step 2: Close gripper (grab object)
  moveGripper(GRIPPER_CLOSED, 10);
  delay(500);
  
  // Step 3: Move arm to drop position
  moveArm(3200);  // 4 revolutions from home
  delay(200);
  
  // Step 4: Open gripper (release object)
  moveGripper(GRIPPER_OPEN, 10);
  delay(500);
  
  // Step 5: Return to home position
  moveArm(0);
  delay(1000);
}
```

### 8.7 Key Servo Library Functions

| Function | Description |
|----------|-------------|
| `attach(pin)` | Attach servo to specified PWM pin |
| `attach(pin, min, max)` | Attach with custom pulse width range (µs) |
| `write(angle)` | Move servo to angle (0-180 degrees) |
| `writeMicroseconds(µs)` | Set position by pulse width (500-2500µs) |
| `read()` | Read last written angle |
| `attached()` | Check if servo is attached to a pin |
| `detach()` | Detach servo (stops PWM signal) |

### 8.8 Servo Troubleshooting

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| Servo doesn't move | No power | Check external power supply connections |
| | Signal wire loose | Verify orange/yellow wire to PWM pin |
| | Wrong pin | Use PWM-capable pin (D3, D5, D6, D9, D10, D11) |
| Servo jitters/twitches | Insufficient power | Use power supply with higher current rating |
| | Electrical noise | Add 100µF capacitor across servo power |
| | Missing common ground | Connect Arduino GND to power supply GND |
| Servo doesn't reach full range | Default pulse range | Use attach(pin, 500, 2500) for wider range |
| Servo overheats | Stalled against obstacle | Ensure free movement, reduce holding time |
| | Overvoltage | Use 5V-6V supply (not higher) |
| Arduino resets | Current spike | Use separate power supply for servo |

---

## Additional Resources

### Recommended Reading

1. AccelStepper Library Documentation: https://www.airspayce.com/mikem/arduino/AccelStepper/
2. Arduino Servo Library Reference: https://www.arduino.cc/reference/en/libraries/servo/
3. A4988 Datasheet: Search "A4988 datasheet" for manufacturer specifications
4. Arduino Reference: https://www.arduino.cc/reference/en/

### Component Sources

- Stepper Motors (NEMA17): Amazon, Pololu, SparkFun
- A4988 Drivers: Amazon, Pololu, AliExpress
- MG996R Servos: Amazon, Adafruit, RobotShop
- Arduino Boards: arduino.cc, Adafruit, SparkFun

---

*Document Version 2.0 - Smart Prosthetics and Robotic Systems (14:125:444)*  
*Rutgers University Department of Biomedical Engineering*
