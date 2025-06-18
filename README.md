# Bluetooth Controlled Dual Joystick Gamepad with PIC16F877A

This project implements a Bluetooth-controlled gamepad system using a PIC16F877A microcontroller. The system reads input from two analog joysticks and sends the data over Bluetooth to a Python-based graphical user interface (GUI), which displays real-time control feedback.

---

## Hardware Components

- PIC16F877A Microcontroller
- 2 × Analog Joystick Modules (each with X, Y axes and 1 push-button)
- HC-05 Bluetooth Module
- 1 × Passive Buzzer
- 1 × Tactile Button for sound toggle
- 4 MHz Crystal Oscillator + 2 × 22pF Capacitors
- USB-TTL or PICkit3 for programming
- Voltage Regulator (5V 1A)
- Breadboard, Wires, Resistors (optional pull-downs)

---

## Pin Connections

| Component        | PIC16F877A Pin |
|------------------|----------------|
| Joystick 1 X     | RA0 (AN0)      |
| Joystick 1 Y     | RA1 (AN1)      |
| Joystick 1 Btn   | RB0 (Digital)  |
| Joystick 2 X     | RA2 (AN2)      |
| Joystick 2 Y     | RA3 (AN3)      |
| Joystick 2 Btn   | RB1 (Digital)  |
| Sound Toggle Btn | RB2 (Digital)  |
| Buzzer Output    | RC2 (PWM)      |
| HC-05 TX         | RC7 (RX)       |
| HC-05 RX         | RC6 (TX)       |

> For HC-05 RX: Use a voltage divider (1kΩ + 2kΩ) to step down 5V to ~3.3V.

---

## Project Features

- 4 analog axis readings (10-bit ADC, scaled to 8-bit)
- 2 digital input buttons for game actions
- 1 sound toggle button to enable/disable buzzer
- PWM control for passive buzzer (on/off only)
- Serial communication via HC-05 over UART
- GUI in Python with live canvas and joystick data

---

## Python GUI (Tkinter)

- Displays joystick coordinates (X/Y) in text
- Canvas shows live joystick position
- Button indicators (green/red)
- Displays buzzer status: `ON` or `OFF`

### Required Library

```bash
pip install pyserial
```

### Running the GUI

```bash
python main.py
```

Make sure the `COM_PORT` in the script matches the Bluetooth device on your PC (usually COM3–COM7).

---

## UART Output Format

The microcontroller sends data like this every ~20ms:

```
J1X:60 J1Y:72 J2X:124 J2Y:131 B1:0 B2:1 SND:1
```

- `J1X`, `J1Y` → Joystick 1 X/Y  
- `J2X`, `J2Y` → Joystick 2 X/Y  
- `B1`, `B2` → Buttons  
- `SND` → Sound ON/OFF  

---

## Build and Flash

- Develop in **MPLAB X IDE**
- Compile using **XC8 Compiler**
- Flash `*.hex` using **PICkit3** via **MPLAB IPE**

> Crystal must be 4 MHz and properly connected with two 22pF capacitors.

---

## Files Included

- `main.c` – PIC source code with config  
- `main.py` – Python GUI interface  
- `README.md` – This documentation    
- `hex/` – Compiled hex file  

---

##  Author

- Developed by: **Talha Ali Sagar- Evren Ozkul**  
- University: **Istanbul Medipol University- Microprocessors course project**
- Course Instructor: **Mustafa Turkboylari**  
- Year: **2025**

---

## License

This project is for educational purposes only.
