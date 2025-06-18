#include <xc.h>
#include <stdio.h>
#include <stdlib.h>

// CONFIG
#define _XTAL_FREQ 4000000

#pragma config FOSC = XT // Crystal Oscillator
#pragma config WDTE = OFF
#pragma config PWRTE = OFF
#pragma config BOREN = OFF
#pragma config LVP = OFF
#pragma config CPD = OFF
#pragma config WRT = OFF
#pragma config CP = OFF

//GLOBAL VARIABLE
unsigned char sound_enabled = 1;
unsigned char prev_sound_button = 1;

unsigned int read_adc(unsigned char channel) {
    ADCON0 = 0x41 | (channel << 3); // Channel selection
    __delay_ms(2);
    GO_nDONE = 1;
    while (GO_nDONE);
    return ((ADRESH << 8) + ADRESL);
}

// INIT PWM
void pwm_init() {
    TRISC2 = 0; // CCP1 output
    PR2 = 0xFF; // PWM period
    CCP1CON = 0x0C; // PWM mode
    T2CON = 0x04; // Timer2 ON
}

void set_pwm_duty(unsigned int value) {
    CCPR1L = value >> 2;
    CCP1CON = (CCP1CON & 0xCF) | ((value & 0x03) << 4);
}

// MAIN 
void main(void) {
    TRISA = 0x0F; // RA0-3 input (ADC)
    TRISB = 0xFF; // RB0-RB2 input (butonlar)
    TRISC2 = 0; // Buzzer output

    ADCON0 = 0x41; // ADC ON
    ADCON1 = 0x80; // RA0-RA3 analog, VDD/VSS ref

    pwm_init();

    TXEN = 1;
    SYNC = 0;
    BRGH = 1;
    SPEN = 1;
    TX9 = 0;
    TRISC6 = 0; // TX out
    SPBRG = 25; // 9600 baud @ 4 MHz

    unsigned int j1x, j1y, j2x, j2y;
    unsigned char b1, b2, sound_btn;

    while (1) {
        j1x = read_adc(0) >> 2;
        j1y = read_adc(1) >> 2;
        j2x = read_adc(2) >> 2;
        j2y = read_adc(3) >> 2;

        b1 = PORTBbits.RB0;
        b2 = PORTBbits.RB1;
        sound_btn = PORTBbits.RB2;

        
        if (sound_btn == 0 && prev_sound_button == 1) {
            sound_enabled = !sound_enabled;
            __delay_ms(200);
        }
        prev_sound_button = sound_btn;

        // PWM set
        if (sound_enabled && (b1 == 0 || b2 == 0)) {
            set_pwm_duty(128); // %50 duty
        } else {
            set_pwm_duty(0); // sound off
        }

        // send data over UART
        printf("J1X:%u J1Y:%u J2X:%u J2Y:%u B1:%u B2:%u SND:%u\r\n", j1x, j1y, j2x, j2y, b1, b2, sound_enabled);

        __delay_ms(50);
    }
}

// putch func for STDIO 
void putch(char data) {
    while (!TXIF);
    TXREG = data;
}