#ifndef CONFIG_H
#define CONFIG_H

#define _XTAL_FREQ 20000000  // 20 MHz crystal oscilator

#include <xc.h>

// CONFIGURATION BITS
#pragma config FOSC = HS        // High Speed Oscillator
#pragma config WDTE = OFF       // Watchdog Timer disabled
#pragma config PWRTE = ON
#pragma config BOREN = ON
#pragma config LVP = OFF        // Low voltage programming off
#pragma config CPD = OFF
#pragma config WRT = OFF
#pragma config CP = OFF

#endif