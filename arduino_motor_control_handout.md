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
    └─────────────────────────────────────────────────────┘
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
    │   D2 ──────────────────────► STEP               │
    │                 │            │                   │
    │   D5 ──────────────────────► DIR                │
    │                 │            │                   │
    │   5V ──────────────────────► VDD                │
    │                 │            │     A4988         │
    │   GND ─────────────────────► GND   Driver       │
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

This example demonstrates fundamental stepper motor control by directly generating step pulses.

```cpp
/*
 * Basic Stepper Motor Control - No Library
 * Smart Prosthetics and Robotic Systems
 * 
 * This program demonstrates direct control of a stepper motor
 * using the A4988 driver by generating step pulses manually.
 */

// Pin definitions
#define STEP_PIN 2    // Step signal to A4988
#define DIR_PIN  5    // Direction signal to A4988

// Motor parameters
#define STEPS_PER_REV 200   // 1.8° per step = 200 steps/revolution

void setup() {
  // Configure pins as outputs
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  
  // Initialize serial for debugging
  Serial.begin(9600);
  Serial.println("Stepper Motor Control Initialized");
}

void loop() {
  // Rotate clockwise one full revolution
  Serial.println("Rotating CW - 1 revolution");
  digitalWrite(DIR_PIN, HIGH);  // Set direction to clockwise
  
  for (int i = 0; i < STEPS_PER_REV; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(1000);    // Pulse width (minimum ~1µs)
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(1000);    // Time between steps (controls speed)
  }
  
  delay(1000);  // Pause for 1 second
  
  // Rotate counter-clockwise one full revolution
  Serial.println("Rotating CCW - 1 revolution");
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
         |←─→|←─────→|
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
  Serial.begin(9600);
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
  
  Serial.println("Slow speed - 1/4 revolution");
  rotateSteps(STEPS_PER_REV / 4, SLOW_DELAY);
  delay(500);
  
  Serial.println("Medium speed - 1/4 revolution");
  rotateSteps(STEPS_PER_REV / 4, MEDIUM_DELAY);
  delay(500);
  
  Serial.println("Fast speed - 1/4 revolution");
  rotateSteps(STEPS_PER_REV / 4, FAST_DELAY);
  delay(500);
  
  Serial.println("Fast speed - 1/4 revolution");
  rotateSteps(STEPS_PER_REV / 4, FAST_DELAY);
  delay(2000);
  
  // Reverse direction
  digitalWrite(DIR_PIN, LOW);  // Counter-clockwise
  Serial.println("Returning to start...");
  rotateSteps(STEPS_PER_REV, MEDIUM_DELAY);
  delay(2000);
}
```

---

## 5. Motor Control with the AccelStepper Library

### 5.1 Introduction to AccelStepper

The AccelStepper library provides advanced stepper motor control including:

- Acceleration and deceleration profiles
- Speed control
- Position tracking
- Non-blocking operation
- Support for multiple motors

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
 */

#include <AccelStepper.h>

// Define stepper motor connection type
// Type 1 = Driver (step/dir pins)
#define MOTOR_INTERFACE_TYPE 1

// Create stepper object
// AccelStepper(interface, stepPin, dirPin)
AccelStepper stepper(MOTOR_INTERFACE_TYPE, 2, 5);

void setup() {
  Serial.begin(9600);
  
  // Configure motor parameters
  stepper.setMaxSpeed(1000);      // Maximum speed in steps/second
  stepper.setAcceleration(500);   // Acceleration in steps/second^2
  
  Serial.println("AccelStepper Initialized");
}

void loop() {
  // Move to position 800 (4 revolutions in full-step mode)
  Serial.println("Moving to position 800");
  stepper.moveTo(800);
  
  // Run until target position reached (blocking)
  while (stepper.distanceToGo() != 0) {
    stepper.run();
  }
  
  delay(1000);
  
  // Move back to position 0
  Serial.println("Returning to position 0");
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
 */

#include <AccelStepper.h>

AccelStepper stepper(1, 2, 5);  // Type 1, Step pin 2, Dir pin 5

// LED for demonstrating non-blocking operation
#define LED_PIN 13
unsigned long previousMillis = 0;
const long interval = 200;  // LED blink interval
bool ledState = LOW;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  
  stepper.setMaxSpeed(500);
  stepper.setAcceleration(200);
  stepper.moveTo(2000);  // Set initial target
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

### 5.6 Controlling Multiple Stepper Motors

```cpp
/*
 * Multiple Stepper Motor Control
 * Coordinated motion of two motors
 */

#include <AccelStepper.h>
#include <MultiStepper.h>

// Define two stepper motors
AccelStepper stepper1(1, 2, 5);   // Motor 1: Step=D2, Dir=D5
AccelStepper stepper2(1, 3, 6);   // Motor 2: Step=D3, Dir=D6

// Create MultiStepper object for coordinated movement
MultiStepper steppers;

void setup() {
  Serial.begin(9600);
  
  // Configure motor parameters
  stepper1.setMaxSpeed(800);
  stepper2.setMaxSpeed(800);
  
  // Add motors to MultiStepper group
  steppers.addStepper(stepper1);
  steppers.addStepper(stepper2);
  
  Serial.println("Multi-stepper system ready");
}

void loop() {
  long positions[2];  // Array to hold target positions
  
  // Move both motors to first position
  Serial.println("Moving to position 1");
  positions[0] = 400;   // Motor 1 target
  positions[1] = 800;   // Motor 2 target
  
  steppers.moveTo(positions);
  steppers.runSpeedToPosition();  // Block until both reach target
  
  delay(1000);
  
  // Return to home position
  Serial.println("Returning home");
  positions[0] = 0;
  positions[1] = 0;
  
  steppers.moveTo(positions);
  steppers.runSpeedToPosition();
  
  delay(1000);
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
- Mechanical switch for detecting end-of-travel
- Normally Open (NO) or Normally Closed (NC) contacts
- Used for homing sequences and safety limits

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
    ┌───┐            │   GND ────────► NC (Normally Closed)
    │ ● │──NC        │                 │
    │   │            │   D2 ──────────► STEP (A4988)
    │ ● │──COM       │   D5 ──────────► DIR (A4988)
    └───┘            │                 │
                     └─────────────────┘
                     
    Note: Enable internal pull-up on D7, or add external 10kΩ pull-up resistor
```

### 6.3 Potentiometer Speed Control

```cpp
/*
 * Potentiometer-Controlled Stepper Speed
 * Smart Prosthetics and Robotic Systems
 * 
 * Use a potentiometer to control motor speed in real-time
 */

#include <AccelStepper.h>

AccelStepper stepper(1, 2, 5);

#define POT_PIN A0      // Potentiometer connected to A0
#define DIR_PIN 5       // Direction control

void setup() {
  Serial.begin(9600);
  stepper.setMaxSpeed(1000);
}

void loop() {
  // Read potentiometer (0-1023)
  int potValue = analogRead(POT_PIN);
  
  // Map to speed range (0 to max speed)
  // Values below 50 = stopped, above = proportional speed
  int motorSpeed = 0;
  
  if (potValue > 50) {
    motorSpeed = map(potValue, 50, 1023, 100, 1000);
  }
  
  // Set speed and run
  stepper.setSpeed(motorSpeed);
  stepper.runSpeed();
  
  // Debug output (reduce frequency to avoid serial buffer overflow)
  static unsigned long lastPrint = 0;
  if (millis() - lastPrint > 250) {
    Serial.print("Pot: ");
    Serial.print(potValue);
    Serial.print(" | Speed: ");
    Serial.println(motorSpeed);
    lastPrint = millis();
  }
}
```

### 6.4 Potentiometer Position Control

```cpp
/*
 * Potentiometer Position Control
 * Map potentiometer position to stepper motor position
 */

#include <AccelStepper.h>

AccelStepper stepper(1, 2, 5);

#define POT_PIN A0
#define MAX_POSITION 800  // Maximum steps from home (4 revolutions)

void setup() {
  Serial.begin(9600);
  
  stepper.setMaxSpeed(800);
  stepper.setAcceleration(400);
  
  Serial.println("Position control ready - turn potentiometer");
}

void loop() {
  // Read potentiometer
  int potValue = analogRead(POT_PIN);
  
  // Map pot value (0-1023) to position range (0 to MAX_POSITION)
  long targetPosition = map(potValue, 0, 1023, 0, MAX_POSITION);
  
  // Move to target position
  stepper.moveTo(targetPosition);
  stepper.run();
  
  // Debug output
  static unsigned long lastPrint = 0;
  if (millis() - lastPrint > 200) {
    Serial.print("Pot: ");
    Serial.print(potValue);
    Serial.print(" | Target: ");
    Serial.print(targetPosition);
    Serial.print(" | Current: ");
    Serial.println(stepper.currentPosition());
    lastPrint = millis();
  }
}
```

### 6.5 Homing with Limit Switch

```cpp
/*
 * Homing Sequence with Limit Switch
 * Smart Prosthetics and Robotic Systems
 * 
 * Motor moves until limit switch is triggered, establishing home position
 */

#include <AccelStepper.h>

AccelStepper stepper(1, 2, 5);

#define LIMIT_SWITCH_PIN 7    // Limit switch connected to D7
#define HOMING_SPEED -200     // Negative = toward home direction

bool isHomed = false;

void setup() {
  Serial.begin(9600);
  
  // Configure limit switch with internal pull-up
  // Switch connects pin to GND when activated
  pinMode(LIMIT_SWITCH_PIN, INPUT_PULLUP);
  
  stepper.setMaxSpeed(800);
  stepper.setAcceleration(400);
  
  Serial.println("Starting homing sequence...");
  homeMotor();
}

void homeMotor() {
  // Move toward home until limit switch is triggered
  stepper.setSpeed(HOMING_SPEED);
  
  // Keep moving until switch is pressed (reads LOW when pressed)
  while (digitalRead(LIMIT_SWITCH_PIN) == HIGH) {
    stepper.runSpeed();
  }
  
  // Stop immediately
  stepper.stop();
  stepper.runToPosition();
  
  // Back off slightly from the switch
  stepper.move(50);  // Move 50 steps away from switch
  stepper.runToPosition();
  
  // Set this as home position (0)
  stepper.setCurrentPosition(0);
  
  isHomed = true;
  Serial.println("Homing complete! Position set to 0");
}

void loop() {
  if (!isHomed) return;
  
  // Example movement after homing
  Serial.println("Moving to position 400");
  stepper.moveTo(400);
  stepper.runToPosition();
  delay(1000);
  
  Serial.println("Moving to position 200");
  stepper.moveTo(200);
  stepper.runToPosition();
  delay(1000);
  
  Serial.println("Returning home");
  stepper.moveTo(0);
  stepper.runToPosition();
  delay(2000);
}
```

### 6.6 Complete System: Position Control with Limits

```cpp
/*
 * Complete Position Control System
 * Features: Homing, potentiometer control, soft limits, limit switch safety
 */

#include <AccelStepper.h>

AccelStepper stepper(1, 2, 5);

// Pin definitions
#define POT_PIN A0
#define LIMIT_SWITCH_PIN 7
#define LED_PIN 13

// Position limits (after homing)
#define MIN_POSITION 0
#define MAX_POSITION 1600  // 8 revolutions

// System state
bool isHomed = false;
bool limitTriggered = false;

void setup() {
  Serial.begin(9600);
  
  pinMode(LIMIT_SWITCH_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  
  stepper.setMaxSpeed(800);
  stepper.setAcceleration(500);
  
  Serial.println("=== Stepper Position Control System ===");
  Serial.println("Press limit switch or send 'H' to begin homing");
}

void homeMotor() {
  Serial.println("Homing...");
  digitalWrite(LED_PIN, HIGH);  // LED on during homing
  
  stepper.setSpeed(-300);
  
  while (digitalRead(LIMIT_SWITCH_PIN) == HIGH) {
    stepper.runSpeed();
  }
  
  stepper.stop();
  delay(100);
  
  // Back off from switch
  stepper.move(100);
  stepper.runToPosition();
  
  stepper.setCurrentPosition(0);
  isHomed = true;
  
  digitalWrite(LED_PIN, LOW);
  Serial.println("Homing complete!");
}

void loop() {
  // Check for serial commands
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'H' || cmd == 'h') {
      homeMotor();
    }
  }
  
  // Check limit switch (safety)
  if (digitalRead(LIMIT_SWITCH_PIN) == LOW) {
    if (!limitTriggered) {
      Serial.println("WARNING: Limit switch triggered!");
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
  
  // Status output
  static unsigned long lastStatus = 0;
  if (millis() - lastStatus > 500) {
    Serial.print("Target: ");
    Serial.print(targetPosition);
    Serial.print(" | Actual: ");
    Serial.print(stepper.currentPosition());
    Serial.print(" | Limit: ");
    Serial.println(digitalRead(LIMIT_SWITCH_PIN) ? "OPEN" : "CLOSED");
    lastStatus = millis();
  }
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

### 7.2 Diagnostic Code

```cpp
/*
 * Stepper Motor Diagnostic Test
 * Run this to verify your hardware setup
 */

#include <AccelStepper.h>

AccelStepper stepper(1, 2, 5);

void setup() {
  Serial.begin(9600);
  while (!Serial) delay(10);
  
  Serial.println("=== Stepper Motor Diagnostic ===\n");
  
  stepper.setMaxSpeed(200);
  stepper.setAcceleration(100);
  
  // Test 1: Direction Pin
  Serial.println("Test 1: Direction control");
  Serial.println("  Motor should rotate CW for 1 second...");
  stepper.setSpeed(100);
  unsigned long start = millis();
  while (millis() - start < 1000) stepper.runSpeed();
  
  delay(500);
  
  Serial.println("  Motor should rotate CCW for 1 second...");
  stepper.setSpeed(-100);
  start = millis();
  while (millis() - start < 1000) stepper.runSpeed();
  
  Serial.println("  [PASS if motor changed direction]\n");
  delay(1000);
  
  // Test 2: Position Control
  Serial.println("Test 2: Position control");
  stepper.setCurrentPosition(0);
  Serial.println("  Moving to position 200...");
  stepper.moveTo(200);
  stepper.runToPosition();
  Serial.print("  Reached position: ");
  Serial.println(stepper.currentPosition());
  
  Serial.println("  Returning to 0...");
  stepper.moveTo(0);
  stepper.runToPosition();
  Serial.print("  Reached position: ");
  Serial.println(stepper.currentPosition());
  
  Serial.println("  [PASS if motor completed both moves]\n");
  delay(1000);
  
  // Test 3: Speed Test
  Serial.println("Test 3: Speed range");
  Serial.println("  Testing speeds: 50, 200, 500, 800 steps/sec");
  
  int speeds[] = {50, 200, 500, 800};
  for (int i = 0; i < 4; i++) {
    Serial.print("  Speed ");
    Serial.print(speeds[i]);
    Serial.println(" - motor running...");
    
    stepper.setSpeed(speeds[i]);
    start = millis();
    while (millis() - start < 1000) stepper.runSpeed();
    
    delay(300);
  }
  
  Serial.println("  [PASS if motor ran at different speeds]\n");
  
  Serial.println("=== Diagnostic Complete ===");
  Serial.println("If all tests passed, hardware is correctly configured.");
}

void loop() {
  // Empty - diagnostic runs once in setup
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

---

## Additional Resources

### Recommended Reading

1. AccelStepper Library Documentation: https://www.airspayce.com/mikem/arduino/AccelStepper/
2. A4988 Datasheet: Search "A4988 datasheet" for manufacturer specifications
3. Arduino Reference: https://www.arduino.cc/reference/en/

### Component Sources

- Stepper Motors (NEMA17): Amazon, Pololu, SparkFun
- A4988 Drivers: Amazon, Pololu, AliExpress
- Arduino Boards: arduino.cc, Adafruit, SparkFun

---

*Document Version 1.0 - Smart Prosthetics and Robotic Systems (14:125:444)*  
*Rutgers University Department of Biomedical Engineering*
