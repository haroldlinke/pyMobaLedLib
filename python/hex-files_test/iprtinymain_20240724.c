/*
TinyRail-Direkt-Lichtbus-Servo
Copyright (C) 2023-2024 Dipl.Ing. Joern Eckhart Bardewyck

Dieses Programm ist freie Software. Sie koennen es unter den Bedingungen der GNU General Public License, wie von der Free Software Foundation veroeffentlicht,
weitergeben und/oder modifizieren, gemaess Version 3 der GPL Lizenz.

Die Veroeffentlichung dieses Programms erfolgt in der Hoffnung, dass es Ihnen von Nutzen sein wird, aber OHNE IRGENDEINE GARANTIE, sogar ohne die implizite
Garantie der MARKTREIFE oder der VERWENDBARKEIT FUER EINEN BESTIMMTEN ZWECK. Details finden Sie in der GNU General Public License.

Sie sollten ein Exemplar der GNU General Public License zusammen mit diesem Programm erhalten haben. Falls nicht, siehe <http://www.gnu.org/licenses/>.

Kontakt ueber jbardewyck at t-online punkt de
*/

/*
Altes Projekt von Hardi Stengelin mit WS2811 Chip und nachfolgender Quantisierung der 400Hz/2kHz Licht PWM durch den ATTiny.

Probleme des alten Projektes, die von mir, unter Beibehaltung der alten Hardware, nicht geloest werden konten:

- Licht PWM Auslesegenauigkeit: Die Ausleseganuigkeit betraegt maximal 2 Lichtwerte, mit Ausreissern zu 3 Lichtwerten. Am unteren Ende des
Wertebereichs sogar noch mehr und mit einer 2kHz Licht PWM (alte Chips 400Hz) ist die Genauigkeit tendenziell noch geringer. Wir haben also
maximal 1/3 der Uebertragungsbandbreite des Wertebereichs von 0..255 zur Verfuegung!

- Servo Refresh Rate: Durch das Verfahren die Licht PWM mit der CPU im Bit-De-Bangig, fuer jeden Servo einzeln auszulesen, kann der
Servo-Stellwert nur in jedem dritten WS2811 Zyklus ausgelesen werden. Dadurch haben wir, bei einer angenommenen WS2811 Rate von 50Hz/20ms,
nur eine Werte-wirksame Servo Refresh Rate von 16.6Hz. Diese ist aber, vom menschlichen Auge, als quasi abgehackte Bewegung, wahrnehmbar!

Zusammengenommen bleiben wir, mit diesen beiden Nachteilen der Licht PWM Auslesung eines WS2811 Chips, um fast eine ganze Zehnerpotenz
(Bandbreite*(1/3)*(1/3)) hinter den Moeglichkeiten des WS2811 Lichtbusses zurueck!

 Based on the following project:
 https://arduino-projekte.webnode.at/meine-projekte/servosteuerung/servotest-attiny/


High V.                  ATTiny 85       Prog.
Prog.                    +-\/-+
       LED 2 Reset PB5  1|    |8  VCC
       LED 1 PWM   PB3  2|    |7  PB2    SCK      Servo 2   SoftwareSerial
LED    LED 0 PWM   PB4  3|    |6  PB1    MISO     Servo 1
                   GND  4|    |5  PB0    MOSI     Servo 0
                         +----+


Zu debugging zwecken kann auch der ATTiny 84 verwendet werden.

                         ATTiny 84
                         +-\/-+                     Pin numbers D0..D10 if pin mapping "Counterclockwise" is selected in the IDE
                   vcc  1|    |14 GND
 D0     Servo 0    PB0  2|    |13 PA0    LED 1 PWM  D10
 D1     Servo 1    PB1  3|    |12 PA1    LED 0 PWM  D9
        Reset      PB3  4|    |11 PA2    LED 2 PWM  D8
 D2     Servo 2    PB2  5|    |10 PA3               D7
 D3                PA7  6|    |9  PA4    SCK        D6    SoftwareSerial
 D4     MOSI       PA6  7|    |8  PA5    MISO       D5
                         +----+



 Revision History: ( informativ nur die erste und die letzte Revisionsmeldung des alten Projektes)
 ~~~~~~~~~~~~~~~~~
 16.04.19:  - Started
 ...
 04.08.20:  - Using 16 MHz CPU Frequenz instead of 8 MHz to read the LED PWM signal of new WS2811 chips
              because they use a PWM signal of 2 kHz instead of 400Hz.
              Attention: The maximal PWM signal to control a servo should be 210 and not 220 because
              otherwise the servo movement may be delayed because 221-224 stop the servo.
*/

/*
Neues Projekt "from scratch" mit direktem Auslesen des WS2811 Lichtbuses durch den ATTiny85 und Weiterleitung an nachfolgende WS2811 LEDs

ATTiny85 fuses ohne Status-LED: lfuse 0xE1, hfuse 0xD5, efuse 0xFF
ATTiny85 fuses MIT Status-LED an Pin 1 (PB5/Reset): lfuse 0xE1, hfuse 0x55, efuse 0xFF

!!!ACHTUNG!!! Wenn die Status-LED hardwaremaessig an Pin 1 verdrahtet ist, dann MUSS die hfuse auf 0x55 (Reset Pin als I/O) programmiert werden,
da der ATTIny85 sonst nicht aus dem Reset rauskommt. Um den ATTIny85 danach nochmal neu programmieren zu koennen braucht man zwingend einen
HV-Progger, wie z.B. Hardies 400er Tina !!!ACHTUNG!!!

Hardware-Voraussetzungen:

Basis ist eine modifizierte MobaLedLib 510 Servoplatine. Bei dieser muss der WS2811 Chip weggelassen, bzw. entfernt werden. Ausserdem
muessen die Widerstaende R5/R9/R10 weggelassen, bzw. entfernt werden. R5 und R9 wuerden die Lichtbus DI/DO Leitungen unzulaessig daempfen.
Statt R5 zu entfernen reicht es auch, die Bruecke SERVO1 wieder zu oeffnen. Statt R10 mit 1K sollte ein 10K Widerstand eingebaut werden,
wenn wir den ATTiny85 Pin 1 nicht zum I/O umkonfigurieren (dieser Pin wird nicht gebraucht), sondern als RESET belassen. Ein zusaetzlicher
Kondensator am RESET Pin muss hierbei noch diskutiert werden!

Ausserdem muessen statt des WS2811 Chips zwei Bruecken eingebaut werden. Und zwar am Bauelementeplatz des WS2811 (egal ob DIP-8, oder SOP-8 unten)
von Pin 1 zu Pin 6 und von Pin 2 zu Pin 5. Bitte unbedingt die Zaehlweise der Pins beachten, die Bruecken duerfen sich NICHT kreuzen!

Bei einer Neubestueckung koennen auch der Widerstand R1 und der Kondensator C1 weggelassen werden; bei einer Abaenderung der alten
Variante stoeren sie aber nicht!


Software-Konzept:

Die neue Software basiert auf zwei fundamentalen Standpfeilern.

1. Direktes Auslesen und Weiterleiten des WS2811 Licht-Busses durch den ATTiny85

Hierfuer wurde die hochoptimierte Tiny Assembler-Routine "TINYRAIL_WS2811ReceiveEnvelop" entwickelt, die einen, bei 16MHz laufenden, ATTiny85
bis aus den letzten Taktzyklus ausnutzt.

2. Zusammenwirken der 8-Bit Timer0 und Timer1 als ein gestageter 16-Bit Tandem-Registertimer

Um die neue hohe Aufloesung des WS2811 Direktausleseverfahrens auch in allen Servos parallel als Servo PWM abbilden zu koennen, werden beide
Timer im Tandem benutzt. Timer 1 hat einen Prescaler von 256 und bringt die Servo PWMs Interrupt-getrieben in den richtigen Zielbereich.
Dort schreitet eine manuelle CPU Routine den schnell laufenden Timer 0 mit Prescaler 1 so lange ab, bis der der korrekte PWM Micro-Takt
erreicht ist und der PWM Output abgeschaltet werden kann. Durch das Kombi-Konzept mit dem Interrupt betraegt die Interrupt Sperrzeit fuer
das Warten auf den Feintakt maximal 16 Microsekunden entsprechend 256 Clocks eines 16MHz Tiny.

Debugging:

Zum Debuggen wird als Nebenprodukt des Timers 0, mit einem Software Prescaler, eine TX Soft-UART mit 9600 Baud erzeugt. Diese Soft-UART
wird in die AVR Standard IO Ungebung so eingehaengt, dass das normale stdio printf, mit allen seinen Parametern, verwendet werden kann
und seinen Output automatisch auf die Soft-UART puchar piped. Die Benutzung der stdio Bibliothek fuer printf kostet ca. 1,6k Flash und
90 Byte RAM. So lange das aber speichertechnisch moeglich ist, ist es deutlich leistungsfaehiger, als eine eigene abgestrippte print
Funktion, die aber nichts kann!


Datenformat auf dem WS2811 Lichtbus, Konfiguration und Betrieb:

Die Loesung liest vom WS2811 Lichtbus fuer jeden Servo DREI Lichtkanaele Der erste 8-Bit Lichtkanal ist ein Steuer- und CRC-Sicherungskanal,
waehrend der zweite Lichtkanal einen 8-Bit Servo-Stellwert (oder Konfigurationswert) enthaelt. Ein dritter 8-Bit Wert kann einen feinen
Servo-Stellwert enthalten, wenn zusaetzliche Genauigkeit gebraucht wird. Wenn es nicht gebraucht wird, wird er mit 0 belegt.

Um die RESET Funktionen gegen ungewolltes Ausloesen zu sichern muss in den Stellwert-Kanaelen ein 16 Bit MAGIC-Code, spezifisch fuer die jeweilige
Resetfunktion, uebermittelt werden! Ausserdem wird der RESET erst in dem Moment vollzogen, wenn zusaetzlich das ENTER-Bit gesetzt wird.

Fuer die gesamte 510er Servoplatine mit 3 Servos wird also die WS2811 Bandbreite von 3 RGB LEDs verbraucht!

Der Steuerkanal und der Positionskanal sind wie folgt strukturiert:

-------------------------------------------------------------------------------------------
|     | CRC-4 nach ITU | ENTER-Bit | Command 0..7 | 2. Byte = Position | 3. Byte Pos fine |
-------------------------------------------------------------------------------------------
| Bit |        7 6 5 4 |         3 |        2 1 0 |    7 6 5 4 3 2 1 0 |  7 6 5 4 3 2 1 0 |
-------------------------------------------------------------------------------------------
|     |        0 0 0 0 |         0 |        0 0 0 |             unused |           unused | idle, nothing to do
-------------------------------------------------------------------------------------------
|     |        invalid |         X |        X X X |     not applicable |          not app | failure on WS2811 Bus
-------------------------------------------------------------------------------------------
|     |     valid (*1) |         X |        0 0 1 |           position |         pos fine | move between progt positions
-------------------------------------------------------------------------------------------
|     |          valid |         0 |        0 1 0 | training positions |       train fine | trainig in standard PWM range 1-2ms (0..255/65535)
-------------------------------------------------------------------------------------------
|     |          valid |         1 |        0 1 0 |  std prog position |        prog fine | memorize 1st and 2nd position (cycles with ENTER-Bit)
-------------------------------------------------------------------------------------------
|     |          valid |         0 |        0 1 1 | training positions |       train fine | trainig in wide PWM range 0,5-2,5ms (0..255/65525)
-------------------------------------------------------------------------------------------
|     |          valid |         1 |        0 1 1 | wide prog position |   wide prog fine | memorize 1st and 2nd position (cycles with ENTER-Bit)
-------------------------------------------------------------------------------------------
|     |          valid |         0 |        1 0 0 |     prog max speed |       MAGIC 0x9A | prerequisite: memorize max speed
-------------------------------------------------------------------------------------------
|     |          valid |         1 |        1 0 0 |     prog max speed |       MAGIC 0x9A | memorize max speed in max value-step per 20ms ( 0 = off, no limit)
-------------------------------------------------------------------------------------------
|     |          valid |         0 |        1 0 0 |                  1 |       MAGIC 0x15 | prerequisite: toggle inverse
-------------------------------------------------------------------------------------------
|     |          valid |         1 |        1 0 0 |                  1 |       MAGIC 0x15 | toggle inverse usage of 0.255 for position and memorize it
-------------------------------------------------------------------------------------------
|     |          valid |         0 |        1 0 1 |         MAGIC 0xE9 |       MAGIC 0x8A | RESET prerequisite: servo factory defaults
-------------------------------------------------------------------------------------------
|     |          valid |         1 |        1 0 1 |         MAGIC 0xE9 |       MAGIC 0x8A | RESET: load factory defaults for servo belonged to this channel
-------------------------------------------------------------------------------------------
|     |          valid |         0 |        1 0 1 |         MAGIC 0x16 |       MAGIC 0x75 | RESET prerequisite: all factory defaults
------------------------------------------------------------------------------------------
|     |          valid |         1 |        1 0 1 |         MAGIC 0x16 |       MAGIC 0x75 | RESET: load factory defaults for ALL servos
-------------------------------------------------------------------------------------------
|     |          valid |         0 |        1 0 1 |         MAGIC 0x5A |       MAGIC 0x9E | RESET prerequisite: last position
-------------------------------------------------------------------------------------------
|     |          valid |         1 |        1 0 1 |         MAGIC 0x5A |       MAGIC 0x9E | RESET: last position memory to none
-------------------------------------------------------------------------------------------
|     |          valid |         X |        1 1 0 |           reserved |              res | reserved
-------------------------------------------------------------------------------------------
|     |          valid |         X |        1 1 1 |           reserved |              res | escape (ffs)
-------------------------------------------------------------------------------------------

(*1): Nach fertig programmierten Servo Endlagen darf hier alternativ zu einer validen CRC eine "0" stehen.


Bemerkungen:

1. Zu Testzwecken kann die CRC-4 Ueberpruefung mit einem #define abgeschaltet werden. Es wird DRINGEND empfohlen, den CRC-4 Check immer dann
zu benutzen, wenn wertvolle Mechanik mit dem Servo gekoppelt ist!

2. In den ersten 10 Sekuden nach dem Booten findet eine Bewegung nur dann statt, wenn der Wert, der als letzter Positioneswert gespeichert wurde
"ueberstrichen" wird, oder wenn vorher noch keine Position gespeichert wurd. (auch nach Reset der letzten Position) Nach den 10 Sekunden wird
JEDER Wert akzeptiert und ausgefuehrt.


Blinkcodes der Status-LED:

1. Die Prioritaet hat immer die WS2811 Bus Verarbeitung und nicht die Status-LED! Bei einem ungleichmaessigen WS2811 Signal, oder Stoerungen
   auf dem WS2811 Bus, kann es zu ungleichmaessigen Blinkmustern kommen! Am besten funktionert die Status-LED bei einem gleichmaessigen
   zyklischen Refresh des WS2811 Busses!

2. Nach dem (Re)Boot leuchtet die LED fuer 5 Sekunden dauerhaft. Diese Zeit gilt fuer einen power up in einen aktiven WS2811 Bus. Diese Zeit
   verlaengert sich auf unbestimmt, wenn der WS2811 Bus inaktiv ist, bis zu einem Zeitpunkt, zu dem der WS2811 Bus aktiv geschaltet wird.

3. Nach den 5 Sekunden boot blinkt die LED in einem Wechsel von 1 Sekunde aus, zu 1 Sekunde ein, also einer Zykluszeit von 2 Sekunden. Wird der
   WS2811 Bus zwischenzeitlich inaktiv, koennen sich beide Zeiten, sowohl an, als auch aus, unbestimmt verlaengern. Wird der WS2811 Bus wieder
   aktiv, wird der 2 Sekunden Zyklus wieder aufgenommen.

4. Status-LED waehrend des Programmierens der Endlagen
   4.1 Waehrend des Einstellens der Endlagen blinkt die LED schnell mit einem Zyklus von 100 ms
   4.2 So lange man sich ausserhalb des bislang programmierten (und damit erlaubten) Bereichs befindet, blinkt die LED sehr schnell mit
       einem Zyklus von 20 ms
   4.3 Wenn man das zweite Mal das ENTER-Bit ausloest und damit die Endlagen fest programmiert, blinkt die LED kurz fuenffach mit 20 ms,
       gefolgt von Aus-Phasen von 300 ms, fuer eine Gesamtzeit von 3 Sekunden.
   Danach ist das Programmieren abgeschlossen und es wird wieder der Blinkzyklus von 2. aufgenommen!

5. Status-LED als Bestaetigung des Programmierens der Maximal-Geschwindigkeit und des Endlagen-Invertierens
   5.1 Zur Bestaetigung des Programmierens erfolgt ein Blinken wie bei 4.3

6. Status-LED als Bestaetigung eines Konfig-RESET bzw. factoy default etc.
   6.1 Nach dem Ausloesen eines factory default fuer das aktuelle Servo blinkt die LED kurz mit 50 ms, gefolgt von jeweils Aus-Phasen von
       750 ms, fuer eine Gesamtzeit von 2 Sekunden.
   6.2 Nach dem Ausloesen eines factory default fuer das ALLE Servos blinkt die LED kurz doppelt mit 50 ms, gefolgt von Aus-Phasen von
       650 ms, fuer eine Gesamtzeit von 2 Sekunden.
   6.3 Nach dem Zuruecksetzen der gespeicherten letzten Position blinkt die LED kurz dreifach mit 50 ms, gefolgt von Aus-Phasen von
       550 ms, fuer eine Gesamtzeit von 2 Sekunden.
   Danach wird jeweils wieder der Blinkzyklus von 2. aufgenommen!


Revision History:
 ~~~~~~~~~~~~~~~~~
 20.01.24: Umstellung auf 24 Bit pro Servo mit moeglicher 16-Bit Stellwert Genauigkeit von der Hauptplatine
 20.01.24: "TINYRAIL_WaitCyclePWMs" als Alternative zu Timer-Interrupt gesteuerten Servo PWMs
 18.07.24: - Verbesserte WS2811 RESET-State Erkennung
           - WS2811 Stranglaengen-Filter: Wenn 10 Mal hintereinander die selbe Stranglaenge erkannt wurde, werden andere Stranglaengen erst nach
             erneuten 10 konsekutiven WS2811, mit der neuen Straglaenge, akzeptiert
           - Grundsaetzlich Umstellung aller Programmierfunktionen auf Zweistufigkeit mit prerequisite ohne ENTER-Bit und finaler Ausfuehrung durch das
             selbe Kommando mit ENTER-Bit. Dazu muessen bestimmte Felder (s.o.) mit spezifischen MAGICS befuellt werden
           - Unterstuetzung einer Status-LED mit Blinkcodes


*/

// Header des Systems
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <avr/io.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>
#include <avr/boot.h>
#include <avr/pgmspace.h>

// Header des Projektes
#include "myeeprom.h"
#include "iprtinygenlib.h"

uint16_t TINYRAIL_WS2811ReceiveEnvelop( uint8_t *receiveBuffer, uint8_t receiveBits);
void     TINYRAIL_SoftWaitPWMs( uint8_t portBit0, uint8_t portBit1, uint8_t portBit2, uint16_t time0, uint16_t time1, uint16_t time2);

// #define TINYRAIL_DEBUG set in makefile
// #define TINYRAIL_DISABLE_CRC4_CHECK
#define TINYRAIL_USE_SOFT_WAIT_PWMs

#define TINYRAIL_SERVOS_SUPPORTED       3

#define TINYRAIL_SUART_SPEED            9600
#define TINYRAIL_SUART_PRESCALER        8
#define TINYRAIL_SUART_TIMER_COUNTER    ( F_CPU / TINYRAIL_SUART_PRESCALER / TINYRAIL_SUART_SPEED)
#ifdef TINYRAIL_DEBUG
    #define TINYRAIL_SUART_TX_BUFFER_SIZE   64
#endif // ifdef TINYRAIL_DEBUG

#define TICK_PERIOD                     2500L // 2,5ms

#define TINYRAIL_SERVO_PRESCALER        256
#define TINYRAIL_SERVO_TIMER_COUNTER    ( F_CPU / 1000000L * TICK_PERIOD / TINYRAIL_SERVO_PRESCALER)
#define TINYRAIL_SLOW_PRESCALER         4096L

#define TIME_ms_2_TICKS( time)              ( ( time * 1000L) / TICK_PERIOD)
#define TIME_ms_from_TICKS( ticks)          ( ticks * ( TICK_PERIOD / 1000L))
#define TIME_us_2_T1_RES( time_us)          ( F_CPU / 1000000L * ( time_us) /*/ TINYRAIL_SERVO_PRESCALER*/)
#define TIME_T1_RES_2_us( t1_res)           ( ( t1_res) / ( F_CPU / 1000000L))
#define TIME_T1_SLOW_RES_2_us( t1_slow_res) ( ( ( t1_slow_res) * TINYRAIL_SLOW_PRESCALER) / ( F_CPU / 1000000L))
#define TIME_us_2_T1_SLOW_RES( time_us)     ( F_CPU / 1000000L * ( time_us) / TINYRAIL_SLOW_PRESCALER)
#define TIME_ms_2_T1_SLOW_RES( time_ms)     ( F_CPU / 1000L * ( time_ms) / TINYRAIL_SLOW_PRESCALER)
#define TIME_8BIT_TIMER_LEFT( cTime, lTime) ( ( cTime > lTime) ? ( cTime - lTime) : ( ( 0xFF - lTime) + cTime))

#define CONTROL_BIT_NUMBER          (24*TINYRAIL_SERVOS_SUPPORTED)

struct OutPortProcessSet outPortProcessSets[TINYRAIL_SERVOS_SUPPORTED];
struct CompControlSet    compControlSets[TINYRAIL_SERVOS_SUPPORTED];

volatile uint8_t servoPwmStep      = 0;
volatile uint8_t servoPwmRunning   = 0;
uint8_t          lastPwmTcnt1      = 0;
uint8_t          lastMainTcnt1     = 0;
uint16_t         timeLockPosPassed = TIME_ms_2_T1_SLOW_RES( 10000);
int              ledPeriod         = TIME_ms_2_T1_SLOW_RES( 5000);
uint8_t          recBuffer[CONTROL_BIT_NUMBER/8];
#ifdef USED_TEXT_START
unsigned char    flashStateFlags = IPR_FLASH_STATE_FLAGS_NONE;
#endif // ifdef USED_TEXT_START


#define TINYRAIL_SIGNATURE  "TR1"

#define SERVO_CONFING_FLAG_INVERT           0x01
#define SERVO_CONFING_FLAG_MOVE_WITHOUT_CRC 0x02
#define SERVO_CONFING_FLAG_POSITION_STORED  0x04

void TinyRail_InitServoPorts()
{
    memset( &outPortProcessSets, sizeof( outPortProcessSets), 0);

    outPortProcessSets[0].portAddr               = &PORTB;
    outPortProcessSets[0].portBitOut             = 1 << PB0;
    outPortProcessSets[0].pwmPulseInTimerResCurr = TIME_us_2_T1_RES( 1500);

    outPortProcessSets[1].portAddr               = &PORTB;
    outPortProcessSets[1].portBitOut             = 1 << PB1;
    outPortProcessSets[1].pwmPulseInTimerResCurr = TIME_us_2_T1_RES( 1500);

#ifndef TINYRAIL_DEBUG
    outPortProcessSets[2].portAddr               = &PORTB;
    outPortProcessSets[2].portBitOut             = 1 << PB2;
    outPortProcessSets[2].pwmPulseInTimerResCurr = TIME_us_2_T1_RES( 1500);

    // define pin PB0 and PB1 as output
    DDRB |= ( 1 << PB0) | ( 1 << PB1) | ( 1 << PB2);
    // set default to low
    PORTB &= ~( ( 1 << PB0) | ( 1 << PB1) | ( 1 << PB2));
#else // ifndef TINYRAIL_DEBUG
    // define pin PB0 and PB1 as output
    DDRB |= ( 1 << PB0) | ( 1 << PB1);
    // set default to low
    PORTB &= ~( ( 1 << PB0) | ( 1 << PB1));
#endif // else // ifndef TINYRAIL_DEBUG
}

uint32_t lastCounter = 0;
uint8_t xxxCount = 0;

void TinyRail_InitServoTimer()
{
    memset( &compControlSets, sizeof( compControlSets), 0);

    // prescaler to 4096 and PWM A/B without outputs
    TCCR1 = ( 1 << PWM1A) | ( 1 << PWM1B) | ( 1 << CS10) | ( 1 << CS12) | ( 1 << CS13);

    TCNT1 = 0;
    OCR1C = 0xFF;
}

const uint8_t blinkFast[1] = { 0x55};
const uint8_t blink1[2]    = { 0x01, 0x00};
const uint8_t blink2[2]    = { 0x01, 0x40};
const uint8_t blink3[2]    = { 0x01, 0x50};
const uint8_t blink5[3]    = { 0x01, 0x55, 0x00};

const uint8_t *ledPattern = 0;
uint8_t  ledValidBits = 0;
uint8_t  ledBitIndex  = 0;
uint8_t  ledBitMs     = 0;
uint16_t ledPlayTime  = 0;

inline void TinyRail_SetLedPlayer( const uint8_t *nLedPattern, uint8_t nLedValidBits, uint8_t nLedBitIndex, uint8_t nLedBitMs, uint16_t nLedPlayTime)
{
    ledPattern   = 0;
    ledValidBits = nLedValidBits;
    ledBitIndex  = nLedBitIndex;
    ledBitMs     = nLedBitMs;
    ledPlayTime  = nLedPlayTime;
    ledPattern   = nLedPattern;
    ledPeriod    = 1;
}

int TinyRail_GetNextLedPeriod( void)
{
    int newTime = 0;

    if ( ledPattern && ledPlayTime)
    {
        uint8_t currPatternBit;
        uint8_t nextPatternBit;

        nextPatternBit = ledPattern[ledBitIndex/8] & ( 0x80 >> ( ledBitIndex % 8));
        do
        {
            currPatternBit = nextPatternBit;

            newTime += TIME_ms_2_T1_SLOW_RES( ledBitMs);
            ledBitIndex++;
            ledBitIndex %= ledValidBits;
            nextPatternBit = ledPattern[ledBitIndex/8] & ( 0x80 >> ( ledBitIndex % 8));
        } while ( --ledPlayTime && ( ( currPatternBit && nextPatternBit) || ( !currPatternBit && !nextPatternBit)));

        // DPRINTF_P( PSTR( "play %u\n"), ( unsigned)ledPlayTime);

        if ( !currPatternBit)
            newTime *= -1;
    }

    return newTime;
}

uint8_t TinyRail_GetLongestServoPWMSet()
{
    uint16_t pwmPulseInTimerResLongest = 0;
    uint8_t  indexPwmSetLongest        = 0xFF;
    uint8_t  index;

    for ( index = 0; index < TINYRAIL_SERVOS_SUPPORTED; index++)
    {
        if ( outPortProcessSets[index].needPwm && ( pwmPulseInTimerResLongest <= outPortProcessSets[index].pwmPulseInTimerResCurr))
        {
            pwmPulseInTimerResLongest = outPortProcessSets[index].pwmPulseInTimerResCurr;
            indexPwmSetLongest = index;
        }
    }
    return indexPwmSetLongest;
}

void TinyRail_GetSortedServoPWMList( uint8_t *indexList, uint8_t *usedIndexes)
{
    if ( indexList && usedIndexes)
    {
        uint8_t index, sortIndex;

        *usedIndexes = 0;
        // discover PWMs to sort
        for ( index = 0; index < TINYRAIL_SERVOS_SUPPORTED; index++)
            if ( outPortProcessSets[index].needPwm)
                indexList[( *usedIndexes)++] = index;

        // sort by bubblesort
        for ( index = 0 ; index < *usedIndexes - 1; index++)
        {
            for ( sortIndex = 0 ; sortIndex < *usedIndexes - index - 1; sortIndex++)
            {
                if (  outPortProcessSets[indexList[sortIndex]].pwmPulseInTimerResCurr >  outPortProcessSets[indexList[sortIndex+1]].pwmPulseInTimerResCurr)
                {
                    uint8_t tempIndex = indexList[sortIndex];

                    indexList[sortIndex]   = indexList[sortIndex+1];
                    indexList[sortIndex+1] = tempIndex;
                }
            }

        }
    }
}

void TinyRail_StoreLastPosition( uint8_t store, ServoConfigSet *sConf, uint8_t *pFlags, uint8_t posValueHigh)
{
    if ( store)
    {
        if ( posValueHigh != my_eeprom_read_byte( &sConf->lastPos))
            my_eeprom_write_byte( &sConf->lastPos, posValueHigh);

        if ( !( *pFlags & SERVO_CONFING_FLAG_POSITION_STORED))
        {
            *pFlags |= SERVO_CONFING_FLAG_POSITION_STORED;
            my_eeprom_write_byte( &sConf->flags, *pFlags);
        }
    }
    else
    {
        if ( *pFlags & SERVO_CONFING_FLAG_POSITION_STORED)
        {
            *pFlags &= ~SERVO_CONFING_FLAG_POSITION_STORED;
            my_eeprom_write_byte( &sConf->flags, *pFlags);
        }
    }
}

void TinyRail_ConvertControlAndValue( uint8_t servoIndex, struct OutPortProcessSet *processSet, ServoConfigSet *sConf, uint8_t control, uint8_t posValueHigh, uint8_t posValueLow)
{
    uint8_t flags = my_eeprom_read_byte( &sConf->flags);

#ifndef TINYRAIL_DISABLE_CRC4_CHECK
    if ( ( ( control == SERVO_CONTROL_MODE_MOVE) && ( flags & SERVO_CONFING_FLAG_MOVE_WITHOUT_CRC))
      || !TinyRail_GenerateChecksum( control, posValueHigh, posValueLow, 1))
#endif // ifndef TINYRAIL_DISABLE_CRC4_CHECK
    {
        uint16_t pwmPulseInTimerResCurrBackup = processSet->pwmPulseInTimerResCurr;
        uint16_t minPos                       = my_eeprom_read_word( &sConf->minPos);
        uint16_t maxPos                       = my_eeprom_read_word( &sConf->maxPos);
        uint8_t  maxSpeed                     = my_eeprom_read_byte( &sConf->maxSpeed);
        uint8_t  usePulse                     = 0;

        if ( ( control & SERVO_CONTROL_MODE_MASK) && ( ( control & SERVO_CONTROL_MODE_MASK) <= SERVO_CONTROL_MODE_PROG_WIDE))
        {
            uint8_t currentTcnt1 = TCNT1;
            uint8_t leftTcnt1    = TIME_8BIT_TIMER_LEFT( currentTcnt1, lastPwmTcnt1);

            /*if ( !( xxxCount % 50))
            {
                DPRINTF_P( PSTR( "leftTcnt1 %u(%u)\n"), ( unsigned)leftTcnt1, ( unsigned)TIME_T1_SLOW_RES_2_us( leftTcnt1));
            }*/

            if ( TIME_T1_SLOW_RES_2_us( leftTcnt1) > 15000)
            {
                processSet->needPwm = 1;

#ifdef TINYRAIL_DEBUG
                // DPRINTF_P( PSTR( ",%u"), ( unsigned)posValueHigh);
#endif // ifdef TINYRAIL_DEBUG
            }
            else
            {
                processSet->needPwm = 0;

#ifdef TINYRAIL_DEBUG
                // DPRINTF_P( PSTR( "backoff %u\n"), ( unsigned)TIME_T1_SLOW_RES_2_us( TCNT1));
#endif // ifdef TINYRAIL_DEBUG
            }
        }
        else
        {
            processSet->needPwm = 0;

            if ( ( processSet->controlChannel & SERVO_CONTROL_MODE_MASK)
              && ( ( processSet->controlChannel & SERVO_CONTROL_MODE_MASK) <= SERVO_CONTROL_MODE_PROG_WIDE))
            {
                TinyRail_StoreLastPosition( 1, sConf, &flags, posValueHigh);

                processSet->countContinous = 0;

#ifdef TINYRAIL_DEBUG
                // DPRINTF_P( PSTR( "%x,%d store pos (off) %u\n"), ( unsigned)control, ( unsigned)posValueHigh, ( unsigned)processSet->positionValue);
#endif // ifdef TINYRAIL_DEBUG
            }
        }

        switch ( control & SERVO_CONTROL_MODE_MASK)
        {
#ifdef USED_TEXT_START
            case SERVO_CONTROL_MODE_ESCAPE :
                if ( ( posValueHigh == ESCAPE_CONTROL2_UPDATE_FUNC) && ( posValueLow == ESCAPI_CONTROL3_UPDATE_ENTER_BOOTLOADER))
                {
                    flashStateFlags |= IPR_FLASH_STATE_FLAG_UPDATE_REQUEST;
                    return;
                }
                break;
#endif // ifdef USED_TEXT_START

            case SERVO_CONTROL_MODE_PROG_POS :
                if ( ( processSet->controlChannel & SERVO_CONTROL_MODE_MASK) != SERVO_CONTROL_MODE_PROG_POS)
                {
                    processSet->tempUsValueProg = 0;
                    processSet->inPrevProgRange = 0;
#ifdef TINYRAIL_DEBUG
                    // DPRINTF_P( PSTR( "enter prog pos\n"));
#endif // ifdef TINYRAIL_DEBUG
                }
                usePulse = 1;
                break;

            case SERVO_CONTROL_MODE_PROG_WIDE :
                if ( ( processSet->controlChannel & SERVO_CONTROL_MODE_MASK) != SERVO_CONTROL_MODE_PROG_WIDE)
                {
                    processSet->tempUsValueProg = 0;
                    processSet->inPrevProgRange = 0;
#ifdef TINYRAIL_DEBUG
                    // DPRINTF_P( PSTR( "enter prog wide\n"));
#endif // ifdef TINYRAIL_DEBUG
                }
                usePulse = 2;
                break;

            case SERVO_CONTROL_MODE_PROG_AUX :
                if ( ( control & SERVO_CONTROL_BIT_ENTER)
                  && ( ( processSet->controlChannel & SERVO_CONTROL_MODE_MASK) == SERVO_CONTROL_MODE_PROG_AUX)
                  && !( processSet->controlChannel & SERVO_CONTROL_BIT_ENTER))
                {
                    uint8_t playLed = 0;
#ifdef TINYRAIL_DEBUG
                    DPRINTF_P( PSTR( "Prog AUX %u magic %x\n"), ( unsigned)posValueHigh, ( unsigned)posValueLow);
#endif // ifdef TINYRAIL_DEBUG

                    switch ( posValueLow)
                    {
                        case SERVO_CONTROL_PROG_AUX_MAGIC_MAX_SPEED :
                            my_eeprom_write_byte( &sConf->maxSpeed, posValueHigh);
                            playLed = 1;
                            break;

                        case SERVO_CONTROL_PROG_AUX_MAGIC_INVERT :
                            flags = ( ~flags & SERVO_CONFING_FLAG_INVERT) | ( flags & ~SERVO_CONFING_FLAG_INVERT);
                            my_eeprom_write_byte( &sConf->flags, flags);
                            playLed = 1;
                            break;
                    }

                    if ( playLed)
                        TinyRail_SetLedPlayer( blink5, 24, 0, 20, 150);
                }
                break;

            case SERVO_CONTROL_MODE_RESET :
                if ( ( control & SERVO_CONTROL_BIT_ENTER)
                  && ( ( processSet->controlChannel & SERVO_CONTROL_MODE_MASK) == SERVO_CONTROL_MODE_RESET)
                  && !( processSet->controlChannel & SERVO_CONTROL_BIT_ENTER))
                {
                    const uint8_t *playLed = 0;
#ifdef TINYRAIL_DEBUG
                    DPRINTF_P( PSTR( "Reset magic %x\n"), ( ( uint16_t)posValueHigh << 8) | posValueLow);
#endif // ifdef TINYRAIL_DEBUG

                    switch ( ( ( uint16_t)posValueHigh << 8) | posValueLow)
                    {
                        case SERVO_CONTROL_RESET_MAGIC_FACTORY_DEFAULTS :
                            TinyRail_ConfigRestoreFactoryDefaults( servoIndex);
                            playLed = blink1;
                            break;

                        case SERVO_CONTROL_RESET_MAGIC_ALL_FACTORY_DEFAULTS :
                            TinyRail_ConfigRestoreFactoryDefaults( 0xFF);
                            playLed = blink2;
                            break;

                        case SERVO_CONTROL_RESET_MAGIC_POSITION_STORE :
                            TinyRail_StoreLastPosition( 0, sConf, &flags, posValueHigh);
                            playLed = blink3;
                            break;
                    }

                    if ( playLed)
                        TinyRail_SetLedPlayer( playLed, 16, 0, 50, 100);
                }
                break;
        }

        if ( flags & SERVO_CONFING_FLAG_INVERT)
            posValueHigh = 255 - posValueHigh;

        if ( maxSpeed)
        {
            if ( posValueHigh >= processSet->positionValue)
            {
                if ( ( posValueHigh - processSet->positionValue) > maxSpeed)
                    posValueHigh = processSet->positionValue + maxSpeed;
            }
            else
            {
                if ( ( processSet->positionValue - posValueHigh) > maxSpeed)
                    posValueHigh = processSet->positionValue - maxSpeed;
            }
        }

        if ( minPos <= maxPos)
            processSet->pwmPulseInTimerResCurr = PortCalcPwmPulseInTimerRes( ( ( uint16_t)posValueHigh << 8) | posValueLow, minPos, maxPos-minPos, usePulse);
        else
            processSet->pwmPulseInTimerResCurr = PortCalcPwmPulseInTimerRes( ( ( uint16_t)posValueHigh << 8) | posValueLow, maxPos, minPos-maxPos, usePulse);

        switch ( control & SERVO_CONTROL_MODE_MASK)
        {
            case SERVO_CONTROL_MODE_MOVE :
                if ( processSet->lastPosPassed < 3)
                {
                    if ( !( flags & SERVO_CONFING_FLAG_POSITION_STORED))
                        processSet->lastPosPassed = 3;
                    else
                    {
                        if ( posValueHigh == my_eeprom_read_byte( &sConf->lastPos))
                            processSet->lastPosPassed = 3;
                        else if ( posValueHigh < my_eeprom_read_byte( &sConf->lastPos))
                        {
                            if ( processSet->lastPosPassed == 2)
                                processSet->lastPosPassed = 3;
                            else
                                processSet->lastPosPassed = 1;
                        }
                        else if ( posValueHigh > my_eeprom_read_byte( &sConf->lastPos))
                        {
                            if ( processSet->lastPosPassed == 1)
                                processSet->lastPosPassed = 3;
                            else
                                processSet->lastPosPassed = 2;
                        }
                    }

                    if ( timeLockPosPassed && ( processSet->lastPosPassed < 3))
                    {
                        // last position not passed (and not first move), roll back to prev settings and disable PWM
                        processSet->pwmPulseInTimerResCurr = pwmPulseInTimerResCurrBackup;
                        processSet->needPwm                = 0;
                        posValueHigh                       = processSet->positionValue;
                        posValueLow                        = 0;
                    }
                }
                break;

            case SERVO_CONTROL_MODE_PROG_POS :
            case SERVO_CONTROL_MODE_PROG_WIDE :
                {
                    uint16_t usValueProg = TIME_T1_RES_2_us( processSet->pwmPulseInTimerResCurr);

                    if ( !processSet->inPrevProgRange
                      && ( ( ( minPos <= maxPos) && ( ( usValueProg < minPos) || ( usValueProg > maxPos)))
                        || ( ( minPos > maxPos) && ( ( usValueProg > minPos) || ( usValueProg < maxPos)))))
                    {
                        // out of range, roll back to prev settings and disable PWM
                        processSet->pwmPulseInTimerResCurr = pwmPulseInTimerResCurrBackup;
                        processSet->needPwm                = 0;
                        posValueHigh                       = processSet->positionValue;
                        posValueLow                        = 0;

                        if ( !ledPlayTime)
                            TinyRail_SetLedPlayer( blinkFast, 8, 0, 10, 100);
                    }
                    else
                    {
                        processSet->inPrevProgRange = 1;

                        if ( ( control & SERVO_CONTROL_BIT_ENTER)
                          && ( ( processSet->controlChannel & SERVO_CONTROL_MODE_MASK) == ( control & SERVO_CONTROL_MODE_MASK))
                          && !( processSet->controlChannel & SERVO_CONTROL_BIT_ENTER))
                        {
#ifdef TINYRAIL_DEBUG
                            // DPRINTF_P( PSTR( "prog value %u, %u\n"), usValueProg, processSet->tempUsValueProg);
#endif // ifdef TINYRAIL_DEBUG

                            if ( !processSet->tempUsValueProg)
                                processSet->tempUsValueProg = usValueProg;
                            else
                            {
                                my_eeprom_write_word( &sConf->minPos, processSet->tempUsValueProg);
                                my_eeprom_write_word( &sConf->maxPos, usValueProg);
                                processSet->tempUsValueProg = 0;
                                processSet->inPrevProgRange = 0;

                                // allow standard movement without CRC
                                flags |= SERVO_CONFING_FLAG_MOVE_WITHOUT_CRC;
                                my_eeprom_write_byte( &sConf->flags, flags);

                                // clear last position
                                TinyRail_StoreLastPosition( 0, sConf, &flags, posValueHigh);

                                TinyRail_SetLedPlayer( blink5, 24, 0, 20, 150);
                            }
                        }
                        else
                        {
                            if ( !ledPlayTime)
                                TinyRail_SetLedPlayer( blinkFast, 8, 0, 50, 20);
                        }
                    }
                }
                break;
        }

        if ( processSet->needPwm)
        {
            if ( processSet->positionValue == posValueHigh)
            {
                if ( processSet->countContinous <= SERVO_STORE_CONTINOUS_POSITION_COUNT)
                    processSet->countContinous++;

                if ( processSet->countContinous == SERVO_STORE_CONTINOUS_POSITION_COUNT)
                {
                    TinyRail_StoreLastPosition( 1, sConf, &flags, posValueHigh);

                    processSet->countContinous = 0;

#ifdef TINYRAIL_DEBUG
                    // DPRINTF_P( PSTR( "%x, store pos (cnt) %u\n"), ( unsigned)control, ( unsigned)posValueHigh);
#endif // ifdef TINYRAIL_DEBUG
                }
            }
            else
                processSet->countContinous = 0;
        }

        processSet->positionValue  = posValueHigh;
        processSet->controlChannel = control;
    }
}

void TinyRail_ProcessServoPWMsStep1( uint8_t *values)
{
    TinyRail_ConvertControlAndValue( 0, &outPortProcessSets[0], &CV.servoConf[0], values[0], values[1], values[2]);
    TinyRail_ConvertControlAndValue( 1, &outPortProcessSets[1], &CV.servoConf[1], values[3], values[4], values[5]);
    TinyRail_ConvertControlAndValue( 2, &outPortProcessSets[2], &CV.servoConf[2], values[6], values[7], values[8]);

    /*if ( !( xxxCount % 50))
    {
        DPRINTF_P( PSTR( "TCNT1 %u(%u)\n"), ( unsigned)TCNT1, ( unsigned)TIME_T1_SLOW_RES_2_us( TCNT1));
    }*/

#ifdef TINYRAIL_USE_SOFT_WAIT_PWMs
    {
        uint8_t indexPwmSet = 0;
        uint8_t indexPwmSetLongest;

        indexPwmSetLongest = TinyRail_GetLongestServoPWMSet();
        if ( indexPwmSetLongest != 0xFF)
        {
            uint8_t  portBit0        = 0;
            uint8_t  portBit1        = 0;
            uint8_t  portBit2        = outPortProcessSets[indexPwmSetLongest].portBitOut;
            uint16_t pwmPulseCycles0 = 0;
            uint16_t pwmPulseCycles1 = 0;
            uint16_t pwmPulseCycles2 = outPortProcessSets[indexPwmSetLongest].pwmPulseInTimerResCurr >> 2;

            if ( indexPwmSet == indexPwmSetLongest)
                indexPwmSet++;
            if ( outPortProcessSets[indexPwmSet].needPwm)
            {
                portBit1        = outPortProcessSets[indexPwmSet].portBitOut;
                pwmPulseCycles1 = outPortProcessSets[indexPwmSet].pwmPulseInTimerResCurr >> 2;
                indexPwmSet++;
            }

            if ( indexPwmSet == indexPwmSetLongest)
                indexPwmSet++;
            if ( outPortProcessSets[indexPwmSet].needPwm)
            {
                portBit0        = outPortProcessSets[indexPwmSet].portBitOut;
                pwmPulseCycles0 = outPortProcessSets[indexPwmSet].pwmPulseInTimerResCurr >> 2;
            }

            if ( pwmPulseCycles0 > pwmPulseCycles1)
            {
                uint16_t tempPwmPulseCycles = pwmPulseCycles0;
                uint8_t  tempPortBit        = portBit0;

                pwmPulseCycles0 = pwmPulseCycles1;
                portBit0        = portBit1;
                pwmPulseCycles1 = tempPwmPulseCycles;
                portBit1        = tempPortBit;
            }

            // calc it as cascade
            pwmPulseCycles2 -= pwmPulseCycles1;
            pwmPulseCycles1 -= pwmPulseCycles0;

            // at least 1 for loop exit condition
            if ( !pwmPulseCycles0)
                pwmPulseCycles0 = 1;
            if ( !pwmPulseCycles1)
                pwmPulseCycles1 = 1;
            if ( !pwmPulseCycles2)
                pwmPulseCycles2 = 1;

            lastPwmTcnt1 = TCNT1;

            TINYRAIL_SoftWaitPWMs( portBit0, portBit1, portBit2, pwmPulseCycles0, pwmPulseCycles1, pwmPulseCycles2);
        }
    }
#else // ifdef TINYRAIL_USE_SOFT_WAIT_PWMs
    if ( TinyRail_GetLongestServoPWMSet() != 0xFF)
    {
        TIMSK &= ~( 1 << OCIE0A);
        servoPwmRunning = 1;
        servoPwmStep = 1;

        // prescaler to 256 and PWM A/B without outputs
        TCCR1 = ( 1 << PWM1A) | ( 1 << PWM1B) | ( 1 << CS10) | ( 1 << CS13);

        TCNT1 = 0;
        OCR1C = 50;

        TIFR  |= ( ( 1 << OCF1A) | ( 1 << OCF1B) | ( 1 << TOV1));
        //Timer/Counter Interrupt Mask Register
        TIMSK |= ( 1 << TOIE1)             // Timer1 Overflow
               | ( 0 << OCIE1A)            // Timer1 Compare A
               | ( 0 << OCIE1B);           // Timer1 Compare B
    }
    else
    {
        if ( TIME_T1_SLOW_RES_2_us( TCNT1) > 40000)
            TCNT1 >>= 1;
    }
#endif // else // ifdef TINYRAIL_USE_SOFT_WAIT_PWMs
}

#ifndef TINYRAIL_USE_SOFT_WAIT_PWMs
void TinyRail_ProcessServoPWMsStep2()
{
    uint8_t orTimsk     = 0;
    uint8_t orTifr      = 0;
    uint8_t orPortb     = 0;
    uint8_t indexPwmSet = 0;
    uint8_t indexPwmSetLongest;

    indexPwmSetLongest = TinyRail_GetLongestServoPWMSet();
    if ( indexPwmSetLongest != 0xFF)
    {
        compControlSets[2].portAddr           = outPortProcessSets[indexPwmSetLongest].portAddr;
        compControlSets[2].portBit            = outPortProcessSets[indexPwmSetLongest].portBitOut;
        compControlSets[2].pwmPulseCyclesRest = ( uint8_t)outPortProcessSets[indexPwmSetLongest].pwmPulseInTimerResCurr;
        orTifr  |= ( 1 << TOV1);
        orTimsk |= ( 1 << TOIE1);
        orPortb |= outPortProcessSets[indexPwmSetLongest].portBitOut;
        OCR1C = ( uint8_t)( outPortProcessSets[indexPwmSetLongest].pwmPulseInTimerResCurr >> 8);

        if ( indexPwmSet == indexPwmSetLongest)
            indexPwmSet++;
        if ( outPortProcessSets[indexPwmSet].needPwm)
        {
            compControlSets[1].portAddr           = outPortProcessSets[indexPwmSet].portAddr;
            compControlSets[1].portBit            = outPortProcessSets[indexPwmSet].portBitOut;
            compControlSets[1].pwmPulseCyclesRest = ( uint8_t)outPortProcessSets[indexPwmSet].pwmPulseInTimerResCurr;
            orTifr  |= ( 1 << OCF1B);
            orTimsk |= ( 1 << OCIE1B);
            orPortb |= outPortProcessSets[indexPwmSet].portBitOut;
            OCR1B = ( uint8_t)( outPortProcessSets[indexPwmSet].pwmPulseInTimerResCurr >> 8);
            indexPwmSet++;
        }

        if ( indexPwmSet == indexPwmSetLongest)
            indexPwmSet++;
        if ( outPortProcessSets[indexPwmSet].needPwm)
        {
            compControlSets[0].portAddr           = outPortProcessSets[indexPwmSet].portAddr;
            compControlSets[0].portBit            = outPortProcessSets[indexPwmSet].portBitOut;
            compControlSets[0].pwmPulseCyclesRest = ( uint8_t)outPortProcessSets[indexPwmSet].pwmPulseInTimerResCurr;
            orTifr  |= ( 1 << OCF1A);
            orTimsk |= ( 1 << OCIE1A);
            orPortb |= outPortProcessSets[indexPwmSet].portBitOut;
            OCR1A = ( uint8_t)( outPortProcessSets[indexPwmSet].pwmPulseInTimerResCurr >> 8);
        }

#ifdef TINYRAIL_DEBUG
        orPortb &= ~( 1 << PB2);
#endif // ifdef TINYRAIL_DEBUG

        PORTB |= orPortb;
        TCNT1 = 0;

        TIFR  |= orTifr;
        TIMSK |= orTimsk;
    }
}

void TinyRail_WaitCycles( uint8_t tcnt0_1, uint8_t cycles)
{
    while ( cycles)
    {
        uint8_t tcnt0_2 = TCNT0;

        if ( tcnt0_2 >= tcnt0_1)
        {
            if ( ( tcnt0_2 - tcnt0_1) >= cycles)
                cycles = 0;
            else
                cycles -= ( tcnt0_2 - tcnt0_1);
        }
        else
        {
            if ( ( ( TINYRAIL_SUART_TIMER_COUNTER - tcnt0_1) + tcnt0_2) >= cycles)
                cycles = 0;
            else
                cycles -= ( ( TINYRAIL_SUART_TIMER_COUNTER - tcnt0_1) + tcnt0_2);
        }
        tcnt0_1 = tcnt0_2;
    }
}

ISR( TIMER1_COMPA_vect)
{
    uint8_t tcnt0 = TCNT0;

    TIMSK &= ~( 1 << OCIE1A);
    if ( compControlSets[0].portAddr)
    {
        TinyRail_WaitCycles( tcnt0, compControlSets[0].pwmPulseCyclesRest);

#ifdef TINYRAIL_DEBUG
        if ( compControlSets[0].portBit != ( 1 << PB2))
#endif // ifdef TINYRAIL_DEBUG

        *compControlSets[0].portAddr &= ~compControlSets[0].portBit;
        compControlSets[0].portAddr = 0;
    }

    // DPRINTF_P( PSTR( "T1A %u\n"), ( unsigned)TCNT1);
}

ISR( TIMER1_COMPB_vect)
{
    uint8_t tcnt0 = TCNT0;

    TIMSK &= ~( 1 << OCIE1B);
    if ( compControlSets[1].portAddr)
    {
        TinyRail_WaitCycles( tcnt0, compControlSets[1].pwmPulseCyclesRest);

#ifdef TINYRAIL_DEBUG
        if ( compControlSets[1].portBit != ( 1 << PB2))
#endif // ifdef TINYRAIL_DEBUG

        *compControlSets[1].portAddr &= ~compControlSets[1].portBit;
        compControlSets[1].portAddr = 0;
    }

    // DPRINTF_P( PSTR( "T1B %u\n"), ( unsigned)TCNT1);
}

ISR( TIMER1_OVF_vect)
{
    uint8_t tcnt0 = TCNT0;

    TIMSK &= ~( 1 << TOIE1);
    if ( servoPwmStep == 1)
    {
        servoPwmStep = 0;
        TinyRail_ProcessServoPWMsStep2();
    }
    else
    {
        if ( compControlSets[2].portAddr)
        {
            TinyRail_WaitCycles( tcnt0, compControlSets[2].pwmPulseCyclesRest);

#ifdef TINYRAIL_DEBUG
            if ( compControlSets[2].portBit != ( 1 << PB2))
#endif // ifdef TINYRAIL_DEBUG
            *compControlSets[2].portAddr &= ~compControlSets[2].portBit;
            compControlSets[2].portAddr = 0;
        }

        servoPwmRunning = 0;
        TIMSK |= ( 1 << OCIE0A);

        // DPRINTF_P( PSTR( "T1C %u\n"), ( unsigned)TCNT1);

        // prescaler to 4096 and PWM A/B without outputs
        TCCR1 = ( 1 << PWM1A) | ( 1 << PWM1B) | ( 1 << CS10) | ( 1 << CS12) | ( 1 << CS13);

        TCNT1 = 0;
        OCR1C = 0xFF;
    }
}
#endif // ifndef TINYRAIL_USE_SOFT_WAIT_PWMs

void TinyRail_StopServoPWMs()
{
#ifndef TINYRAIL_USE_SOFT_WAIT_PWMs
    TIMSK &= ~( ( 1 << TOIE1)             // Timer1 Overflow
              | ( 1 << OCIE1A)            // Timer1 Compare A
              | ( 1 << OCIE1B));          // Timer1 Compare B
#endif // ifndef TINYRAIL_USE_SOFT_WAIT_PWMs

#ifdef TINYRAIL_DEBUG
    PORTB &= ~( ( 1 << PB0) | ( 1 << PB1));
#else // ifdef TINYRAIL_DEBUG
    PORTB &= ~( ( 1 << PB0) | ( 1 << PB1) | (1 << PB2));
#endif // else // ifdef TINYRAIL_DEBUG
}

void TinyRail_InitStatusLED()
{
    // define pin PB5 as output
    DDRB |= ( 1 << PB5);
    // set default to low
    PORTB &= ~( 1 << PB5);
}

void TinyRail_SetStatusLED( uint8_t set)
{
    if ( set)
        PORTB |= ( 1 << PB5);
    else
        PORTB &= ~( 1 << PB5);
}

void TinyRail_ProcessMainTime()
{
    uint8_t currentTcnt1  = TCNT1;
    uint8_t leftSinceLast = TIME_8BIT_TIMER_LEFT( currentTcnt1, lastMainTcnt1);

    if ( ledPeriod > 0)
    {
        if ( ledPeriod > leftSinceLast)
            ledPeriod -= leftSinceLast;
        else
        {
            // DPRINTF_P( PSTR( "LED off %u\n"), leftSinceLast);

            // switch LED off
            TinyRail_SetStatusLED( 0);

            ledPeriod = TinyRail_GetNextLedPeriod();
            if ( !ledPeriod)
            {
                ledPeriod = TIME_ms_2_T1_SLOW_RES( 1000);
                ledPeriod *= -1;
            }
        }
    }
    else if ( ledPeriod < 0)
    {
        if ( ledPeriod < ( leftSinceLast * -1))
            ledPeriod += leftSinceLast;
        else
        {
            // DPRINTF_P( PSTR( "LED on %u\n"), leftSinceLast);

            // switch LED on
            TinyRail_SetStatusLED( 1);

            ledPeriod = TinyRail_GetNextLedPeriod();
            if ( !ledPeriod)
                ledPeriod = TIME_ms_2_T1_SLOW_RES( 1000);
        }
    }

    if ( timeLockPosPassed > leftSinceLast)
        timeLockPosPassed -= leftSinceLast;
    else
        timeLockPosPassed = 0;

    lastMainTcnt1  = currentTcnt1;
}

uint16_t candidateLockLength = 0;
uint16_t lockedRecLength     = 0;
uint8_t  countEqualLength    = 0;

uint8_t TinyRail_LockedToReceivedLength( uint16_t recLength)
{
    if ( recLength == candidateLockLength)
    {
        if ( countEqualLength < 255)
        {
            countEqualLength++;
            if ( countEqualLength >= 10)
                lockedRecLength = candidateLockLength;
        }
    }
    else
        countEqualLength = 0;

    if ( ( recLength == lockedRecLength) || !lockedRecLength)
        return 1;

    return 0;
}

int main( void)
{
#ifdef TINYRAIL_DEBUG
    TinyRail_SUART_Init();
#endif // ifdef TINYRAIL_DEBUG
    TinyRail_InitMainTimer();
    TinyRail_InitStatusLED();
    TinyRail_SetStatusLED( 1);
    TinyRail_InitServoPorts();
    TinyRail_InitServoTimer();
    TinyRail_InitConfig();

    // DPRINTF_P( PSTR( "Init %c%c\n"), my_eeprom_read_byte( &CV_PRESET.signature[0]), my_eeprom_read_byte( &CV_PRESET.signature[1]));
    // DPRINTF_P( PSTR( "Init2 %u, %u\n"), my_eeprom_read_word( &CV.servoConf[0].minPos), my_eeprom_read_word( &CV.servoConf[0].maxPos));

#ifdef USED_TEXT_START
    // my_eeprom_write_byte( &BOOT_INFO.bootSig[0], 0xA5);
    Boot_InfoInit();
    flashStateFlags = my_eeprom_read_byte( &BOOT_INFO.flashStateFlags);

    // clear update request because we are running successfully
    if ( flashStateFlags & ( IPR_FLASH_STATE_FLAG_UPDATE_REQUEST | IPR_FLASH_STATE_FLAG_RESET_REQUEST))
    {
        flashStateFlags &= ~( IPR_FLASH_STATE_FLAG_UPDATE_REQUEST | IPR_FLASH_STATE_FLAG_RESET_REQUEST);
        my_eeprom_write_byte( &BOOT_INFO.flashStateFlags, flashStateFlags);
    }

    while ( !( flashStateFlags & ( IPR_FLASH_STATE_FLAG_UPDATE_REQUEST | IPR_FLASH_STATE_FLAG_RESET_REQUEST)))
#else // ifdef USED_TEXT_START
    while ( 1)
#endif // else // ifdef USED_TEXT_START
    {
        uint32_t useCounter;
        uint32_t timeDelta;

        useCounter = hiresTimerCounter;
        while ( useCounter != hiresTimerCounter)
            useCounter = hiresTimerCounter;
        if ( useCounter >= lastCounter)
            timeDelta = useCounter - lastCounter;
        else
            timeDelta = useCounter + ( 0xFFFFFFFFL - lastCounter);

        if ( !servoPwmRunning)
#ifdef TINYRAIL_DEBUG
        if ( timeDelta >= ( F_CPU / 500))
#endif // ifdef TINYRAIL_DEBUG
        {
            uint16_t recLength;

#ifdef TINYRAIL_DEBUG
            TinyRail_SUART_Suspend( 1, 1);
#endif // ifdef TINYRAIL_DEBUG

            TinyRail_StopServoPWMs();

            TinyRail_ProcessMainTime();

            recLength = TINYRAIL_WS2811ReceiveEnvelop( ( uint8_t *)&recBuffer, CONTROL_BIT_NUMBER);

            if ( ( recLength >= CONTROL_BIT_NUMBER) && TinyRail_LockedToReceivedLength( recLength))
                TinyRail_ProcessServoPWMsStep1( recBuffer);

#ifdef TINYRAIL_DEBUG
            TinyRail_SUART_Resume();
#endif // ifdef TINYRAIL_DEBUG

#ifdef TINYRAIL_DEBUG
            if ( !( xxxCount++ % 50))
            {
                // DPRINTF_P( PSTR( "Step %x, %x, %x, %x, %x, %x, %x, %x\n"), recBuffer[0], recBuffer[1], recBuffer[2], recBuffer[3], recBuffer[4], recBuffer[5], recBuffer[6], recBuffer[7]);

                // DPRINTF_P( PSTR( "Stepbits %u = %x[%x]:%u(%u), %u, %u\n"), recLength, ( unsigned)recBuffer[0], ( unsigned)TinyRail_GenerateChecksum( recBuffer[0], recBuffer[1], 0), ( unsigned)recBuffer[1], ( unsigned)TIME_T1_RES_2_us( outPortProcessSets[0].pwmPulseInTimerResCurr), ( unsigned)recBuffer[3], ( unsigned)recBuffer[5]);

                DPRINTF_P( PSTR( "Stepbits %u = %x[%x]:%u(%u), %u, %u\n"), recLength, ( unsigned)recBuffer[0], ( unsigned)TinyRail_GenerateChecksum( recBuffer[0], recBuffer[1], recBuffer[2], 0), ( unsigned)recBuffer[1], ( unsigned)TIME_T1_RES_2_us( outPortProcessSets[0].pwmPulseInTimerResCurr), ( unsigned)recBuffer[4], ( unsigned)recBuffer[7]);
                // DPRINTF_P( PSTR( "LED period %u\n"), ledPeriod);
            }
#endif // ifdef TINYRAIL_DEBUG

            useCounter = hiresTimerCounter;
                while ( useCounter != hiresTimerCounter)
            useCounter = hiresTimerCounter;
            lastCounter = useCounter;
        }
    }

#ifdef USED_TEXT_START
    my_eeprom_write_byte( &BOOT_INFO.flashStateFlags, flashStateFlags);

#ifdef TINYRAIL_DEBUG
    TinyRail_SUART_Suspend( 2, 1);
#endif // ifdef TINYRAIL_DEBUG

    TinyRail_DeinitMainTimer();

    {
        void ( *start_bootloader)( void) = ( void ( *)(void))0x0000;

        start_bootloader();
    }
#endif // ifdef USED_TEXT_START

    return 0;
}

