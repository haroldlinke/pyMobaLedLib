// This file contains the DCC and LED definitions.
//
// It was automatically generated by the program ProgGenerator Ver. 3.3.2E      by Hardi
// File creation: 02/18/25 09:50:38
// (Attention: The display in the Arduino IDE is not updated if Options/External Editor is disabled)

#ifndef __LEDS_AUTOPROG_H__
#define __LEDS_AUTOPROG_H__

#ifndef CONFIG_ONLY
#ifndef ARDUINO_RASPBERRY_PI_PICO
#define FASTLED_INTERNAL       // Disable version number message in FastLED library (looks like an error)
#include <FastLED.h>           // The FastLED library must be installed in addition if you got the error message "..fatal error: FastLED.h: No such file or directory"
                               // Arduino IDE: Sketch / Include library / Manage libraries                    Deutsche IDE: Sketch / Bibliothek einbinden / Bibliothek verwalten
                               //              Type "FastLED" in the "Filter your search..." field                          "FastLED" in das "Grenzen Sie ihre Suche ein" Feld eingeben
                               //              Select the entry and click "Install"                                         Gefundenen Eintrag auswaehlen und "Install" anklicken
#else
#include <PicoFastLED.h>       // Juergens minimum version or FastLED for Raspberry Pico
#endif
#endif // CONFIG_ONLY

#include <MobaLedLib.h>

#define START_MSG "LEDs_AutoProg Ver 1: 02.18.25 09:50"

#define TWO_BUTTONS_PER_ADDRESS 1      // Two buttons (Red/Green) are used (DCC/LNet/CAN)
#ifdef NUM_LEDS
  #warning "'NUM_LEDS' definition in the main program is replaced by the included 'LEDs_AutoProg.h' with 20"
  #undef NUM_LEDS
#endif

#define NUM_LEDS 20                    // Number of LEDs (Maximal 256 RGB LEDs could be used)

#define LEDS_PER_CHANNEL ",18,0,2"

#define USE_PROTOCOL_DCC

#define RECEIVE_LED_COLOR_PER_RS232

#define GEN_BUTTON_RELEASE
#define GEN_BUTTON_RELEASE_COM GEN_OFF
#define USE_EXT_ADDR
#define USE_RS232_OR_SPI_AS_INPUT      // Use the RS232 or SPI Input to read DCC/SX commands from the second Arduino and from the PC (The SPI is only used if enabled with USE_SPI_COM)
#define ADDR_OFFSET 0

#define ADDR_MSK  0x3FFF  // 14 Bits are used for the Address

#define S_ONOFF   (uint16_t)0
#define B_RED     (uint16_t)(1<<14)
#define B_GREEN   (uint16_t)(2<<14)
#define O_RET_MSG (uint16_t)(3<<14)    // Return messages (Rueckmelder)
#define B_TAST    B_RED


typedef struct
    {
    uint16_t AddrAndTyp; // Addr range: 0..16383. The upper two bytes are used for the type
    uint8_t  InCnt;
    } __attribute__ ((packed)) Ext_Addr_T;

// Definition of external adresses
#ifdef CONFIG_ONLY
const Ext_Addr_T Ext_Addr[] __attribute__ ((section (".MLLAddressConfig"))) =
#else
const PROGMEM Ext_Addr_T Ext_Addr[] =
#endif
         { // Addr & Typ    InCnt
           { 300  + S_ONOFF,   1 },      // Lokschuppen (pc)
           { 400  + S_ONOFF,   1 },      // Lokschuppen (pc)
         };


// Input channel defines for local inputs and expert users
#define INCH_DCC_300_ONOFF      0      // Lokschuppen (pc)
#define INCH_DCC_400_ONOFF      1      // Lokschuppen (pc)


//*** Output Channels ***
#define START_VARIABLES   2                                        // Define the start number for the variables.
#define licht1                  2                                        // Z21-RM-R�ckmelder: Adresse:1 Eingang:1
#define licht6                  3                                        // Z21-RM-R�ckmelder: Adresse:1 Eingang:2
#define licht5                  4                                        // Z21-RM-R�ckmelder: Adresse:1 Eingang:3
#define licht3                  5                                        // Z21-RM-R�ckmelder: Adresse:1 Eingang:4
#define licht2                  6                                        // Z21-RM-R�ckmelder: Adresse:1 Eingang:5
#define licht4                  7                                        // Z21-RM-R�ckmelder: Adresse:1 Eingang:6
#define licht9                  8                                        // Z21-RM-R�ckmelder: Adresse:1 Eingang:7
#define licht10                 9                                        // Z21-RM-R�ckmelder: Adresse:1 Eingang:8
#define licht8                  10                                       // Z21-RM-R�ckmelder: Adresse:2 Eingang:1
#define licht7                  11                                       // Z21-RM-R�ckmelder: Adresse:2 Eingang:2
#define lichtunten              12                                       // Z21-RM-R�ckmelder: Adresse:2 Eingang:3
#define lichtoben               13                                       // Z21-RM-R�ckmelder: Adresse:2 Eingang:4
#define lichtoben2              14                                       // Z21-RM-R�ckmelder: Adresse:2 Eingang:5
#define lichtunten2             15                                       // Z21-RM-R�ckmelder: Adresse:2 Eingang:6
#define lichtaus7               16                                       // Z21-RM-R�ckmelder: Adresse:2 Eingang:7
#define lichtaus6               17                                       // Z21-RM-R�ckmelder: Adresse:2 Eingang:8
#define lichtaus5               18                                       // Z21-RM-R�ckmelder: Adresse:3 Eingang:1
#define lichtaus4               19                                       // Z21-RM-R�ckmelder: Adresse:3 Eingang:2
#define lichtaus2               20                                       // Z21-RM-R�ckmelder: Adresse:3 Eingang:3
#define lichtaus3               21                                       // Z21-RM-R�ckmelder: Adresse:3 Eingang:4
#define lichtaus8               22                                       // Z21-RM-R�ckmelder: Adresse:3 Eingang:5
#define lichtaus1               23                                       // Z21-RM-R�ckmelder: Adresse:3 Eingang:6
#define lichtobenan             24                                       // Z21-RM-R�ckmelder: Adresse:3 Eingang:7
#define lichtuntenan            25                                       // Z21-RM-R�ckmelder: Adresse:3 Eingang:8


#define START_SEND_INPUTS 2                                        // Start address of all switches/variables
#define TOTAL_SEND_INPUTS 24                                       // Number of used switches/variables
#define TOTAL_SWITCHES_A  0                                        // Number of used inputs for analog keyboard
#define TOTAL_SWITCHES_B  0                                        // Number of used inputs for keyboard 1
#define TOTAL_SWITCHES_C  0                                        // Number of used inputs for keyboard 2
#define TOTAL_SWITCHES_D  0                                        // Number of used inputs for main board switches
#define TOTAL_VARIABLES   24                                       // Number of used variables
/*********************/
#define SETUP_FASTLED()                                                      \
/*********************/                                                      \
  CLEDController& controller0 = FastLED.addLeds<NEOPIXEL,  6>(leds+  0, 18); \
                                                                             \
  controller0.clearLeds(256);                                                \
  FastLED.setDither(DISABLE_DITHER);       // avoid sending slightly modified brightness values
/*End*/

// ----- LED to Var -----
  #define USE_LED_TO_VAR

  #define T_EQUAL_THEN     0
  #define T_NOT_EQUAL_THEN 1
  #define T_LESS_THEN      2
  #define T_GREATER_THAN   3
  #define T_BIN_MASK       4
  #define T_NOT_BIN_MASK   5

  typedef struct
      {
      uint8_t  Var_Nr;
      uint8_t  LED_Nr;
      uint8_t  Offset_and_Typ; // ---oottt    Offset: 0..2
      uint8_t  Val;
      } __attribute__ ((packed)) LED2Var_Tab_T;

#ifdef CONFIG_ONLY
  const LED2Var_Tab_T LED2Var_Tab[] __attribute__ ((section (".MLLL2VConfig"))) =
#else
  const PROGMEM LED2Var_Tab_T LED2Var_Tab[] =
#endif
      {
        // Var name           LED_Nr LED Offset   Typ                Compare value
        { licht1,             18,    (0   << 3) | T_GREATER_THAN,    1   },
        { licht6,             18,    (0   << 3) | T_GREATER_THAN,    2   },
        { licht5,             18,    (0   << 3) | T_GREATER_THAN,    3   },
        { licht3,             18,    (0   << 3) | T_GREATER_THAN,    4   },
        { licht2,             18,    (0   << 3) | T_GREATER_THAN,    5   },
        { licht4,             18,    (0   << 3) | T_GREATER_THAN,    6   },
        { licht9,             18,    (0   << 3) | T_GREATER_THAN,    7   },
        { licht10,            18,    (0   << 3) | T_GREATER_THAN,    8   },
        { licht8,             18,    (0   << 3) | T_GREATER_THAN,    9   },
        { licht7,             18,    (0   << 3) | T_GREATER_THAN,    10  },
        { lichtaus7,          19,    (0   << 3) | T_GREATER_THAN,    1   },
        { lichtaus6,          19,    (0   << 3) | T_GREATER_THAN,    2   },
        { lichtaus5,          19,    (0   << 3) | T_GREATER_THAN,    3   },
        { lichtaus4,          19,    (0   << 3) | T_GREATER_THAN,    4   },
        { lichtaus2,          19,    (0   << 3) | T_GREATER_THAN,    5   },
        { lichtaus3,          19,    (0   << 3) | T_GREATER_THAN,    6   },
        { lichtaus8,          19,    (0   << 3) | T_GREATER_THAN,    7   },
        { lichtaus1,          19,    (0   << 3) | T_GREATER_THAN,    8   }
      };




//*******************************************************************
// *** Configuration array which defines the behavior of the LEDs ***
MobaLedLib_Configuration()
  {
  RGB_Heartbeat2(0, 5, 64)                                                                                    /* Excel row 6                                                                                                                                                                                 */
  // Set_LED_OutpPinLst(6 A4 V)                                                                               /* Excel row 10                                                                                                                                                                                */
  // Activation: Binary                                                                                       /* Lokschuppen (pc)                                                                                                                                                                            */
  Bin_InCh_to_TmpVar(0, 1)                                                                                    /*     "                                                                                                                                                                                       */
  PatternT13(18,28,SI_LocalVar,1,0,30,0,PM_NORMAL,100,5 Sec,3 Sec,3 Sec,5 Sec,5 Sec,5 Sec,5 Sec,5 Sec,5 Sec,5 Sec,5 Sec,100,0,2,3,4,5,6,7,8,9,10,11,12,0  ,63,128,0,0,0,0,0,0,0,0,64,1,63) /*     "                                                                                                          */
  // LED_to_Var(licht1, 0, >, 1)                                                                              /* thekenlicht an                                                                                                                                                                              */
  // LED_to_Var(licht6, 0, >, 2)                                                                              /* treppe unten an                                                                                                                                                                             */
  // LED_to_Var(licht5, 0, >, 3)                                                                              /* treppe oben an                                                                                                                                                                              */
  // LED_to_Var(licht3, 0, >, 4)                                                                              /* billardraum an                                                                                                                                                                              */
  // LED_to_Var(licht2, 0, >, 5)                                                                              /* strahler vorne an                                                                                                                                                                           */
  // LED_to_Var(licht4, 0, >, 6)                                                                              /* strahler hinten an                                                                                                                                                                          */
  // LED_to_Var(licht9, 0, >, 7)                                                                              /* treppe oben an                                                                                                                                                                              */
  // LED_to_Var(licht10, 0, >, 8)                                                                             /* treppe unten an                                                                                                                                                                             */
  // LED_to_Var(licht8, 0, >, 9)                                                                              /* Schankraum an                                                                                                                                                                               */
  // LED_to_Var(licht7, 0, >, 10)                                                                             /* k�che an                                                                                                                                                                                    */
  Const(1, C1, licht1, 0, 128)                                                                                /* Thekenlicht                                                                                                                                                                                 */
  Const(1, C2, licht4, 0, 200)                                                                                /* Strahler hinten                                                                                                                                                                             */
  Const(1, C3, licht2, 0, 200)                                                                                /* Strahlervorne                                                                                                                                                                               */
  ConstRGB(2, licht3, 0, 0, 0, 224, 236, 110)                                                                 /* Billardraum                                                                                                                                                                                 */
  MonoFlop(lichtunten, licht5, 4 Sek)                                                                         /* Excel row 26                                                                                                                                                                                */
  ConstRGB(3, lichtunten, 0, 0, 0, 75, 75, 75)                                                                /* Treppe oben                                                                                                                                                                                 */
  MonoFlop(lichtoben, licht6, 4 Sek)                                                                          /* Excel row 28                                                                                                                                                                                */
  ConstRGB(4, lichtoben, 0, 0, 0, 75, 75, 75)                                                                 /* Treppe unten                                                                                                                                                                                */
  // Next_LED(-2)                                                                                             /* Excel row 30                                                                                                                                                                                */
  MonoFlop(lichtoben2, licht9, 4 Sek)                                                                         /* Excel row 31                                                                                                                                                                                */
  ConstRGB(3, lichtoben2, 0, 0, 0, 75, 75, 75)                                                                /* Excel row 32                                                                                                                                                                                */
  MonoFlop(lichtunten2, licht10, 4 Sek)                                                                       /* Excel row 33                                                                                                                                                                                */
  ConstRGB(4, lichtunten2, 0, 0, 0, 75, 75, 75)                                                               /* Excel row 34                                                                                                                                                                                */
  ConstRGB(5, licht7, 0, 0, 0, 193, 220, 221)                                                                 /* K�che                                                                                                                                                                                       */
  ConstRGB(6, licht8, 0, 0, 0, 228, 233, 165)                                                                 /* Schankraum                                                                                                                                                                                  */
  // Next_LED(-6)                                                                                             /* Excel row 37                                                                                                                                                                                */
  // Activation: Binary                                                                                       /* Lokschuppen (pc)                                                                                                                                                                            */
  Bin_InCh_to_TmpVar(1, 1)                                                                                    /*     "                                                                                                                                                                                       */
  PatternT11(19,28,SI_LocalVar,1,0,30,0,PM_NORMAL,100,5 Sec,3 Sec,3 Sec,5 Sec,5 Sec,5 Sec,5 Sec,5 Sec,5 Sec,100,0,2,3,4,5,6,7,8,9,10,0  ,63,128,0,0,0,0,0,0,64,1,63) /*     "                                                                                                                                */
  // LED_to_Var(lichtaus7, 0, >, 1)                                                                           /* K�che aus                                                                                                                                                                                   */
  // LED_to_Var(lichtaus6, 0, >, 2)                                                                           /* treppe unten an                                                                                                                                                                             */
  // LED_to_Var(lichtaus5, 0, >, 3)                                                                           /* treppe oben an                                                                                                                                                                              */
  // LED_to_Var(lichtaus4, 0, >, 4)                                                                           /* Strahler vorne aus                                                                                                                                                                          */
  // LED_to_Var(lichtaus2, 0, >, 5)                                                                           /* Strahler hinten aus                                                                                                                                                                         */
  // LED_to_Var(lichtaus3, 0, >, 6)                                                                           /* Billardraum aus                                                                                                                                                                             */
  // LED_to_Var(lichtaus8, 0, >, 7)                                                                           /* Schankraum aus                                                                                                                                                                              */
  // LED_to_Var(lichtaus1, 0, >, 8)                                                                           /* Theke aus                                                                                                                                                                                   */
  Const(1, C1, lichtaus1, 0, 0)                                                                               /* Thekenlicht                                                                                                                                                                                 */
  Const(1, C2, lichtaus4, 0, 0)                                                                               /* Strahler hinten                                                                                                                                                                             */
  Const(1, C3, lichtaus2, 0, 0)                                                                               /* Strahlervorne                                                                                                                                                                               */
  ConstRGB(2, lichtaus3, 0, 0, 0, 0, 0, 0)                                                                    /* Billardraum                                                                                                                                                                                 */
  MonoFlop(lichtobenan, lichtaus5, 3 Sek)                                                                     /* Excel row 52                                                                                                                                                                                */
  ConstRGB(3, lichtobenan, 0, 0, 0, 44, 44, 36)                                                               /* Treppe oben                                                                                                                                                                                 */
  MonoFlop(lichtuntenan, lichtaus6, 3 Sek)                                                                    /* Excel row 54                                                                                                                                                                                */
  ConstRGB(4, lichtuntenan, 0, 0, 0, 29, 29, 21)                                                              /* Treppe unten                                                                                                                                                                                */
  ConstRGB(5, lichtaus7, 0, 0, 0, 0, 0, 0)                                                                    /* K�che                                                                                                                                                                                       */
  ConstRGB(6, lichtaus8, 0, 0, 0, 0, 0, 0)                                                                    /* Schankraum                                                                                                                                                                                  */

  EndCfg // End of the configuration
  };
//*******************************************************************

#ifndef COPYLED_OFF
#define COPYLED_OFF 0
#endif

#ifndef COPYLED_OFF_ONCE
#define COPYLED_OFF_ONCE 1
#endif

//---------------------------------------------
void Set_Start_Values(MobaLedLib_C &MobaLedLib)
//---------------------------------------------
{
}


// if function returns TRUE the calling loop stops
typedef bool(*HandleValue_t) (uint8_t CallbackType, uint8_t ValueId, uint8_t* Value, uint16_t EEPromAddr, uint8_t TargetValueId, uint8_t Options);


#define InCnt_MSK  0x003F  // 6 bits are used for the InCnt, 2 bits for the type ttcc cccc => Max InCnt=63
#define IS_COUNTER (uint8_t)0x80
#define IS_PULSE   (uint8_t)0x40
#define IS_TOGGLE  (uint8_t)0x00
#define COUNTER_ID

typedef struct
    {
    uint8_t TypAndInCnt; // Type bits 7 & 6, InCnt 0..5
    uint8_t Channel;
    } __attribute__ ((packed)) Store_Channel_T;

// Definition of channels and counters that need to store state in EEProm
const PROGMEM Store_Channel_T Store_Values[] =
         { // Mode + InCnt , Channel
           { IS_TOGGLE + 1 , INCH_DCC_300_ONOFF  },      // Lokschuppen (pc)
           { IS_TOGGLE + 1 , INCH_DCC_400_ONOFF  },      // Lokschuppen (pc)
         };

#ifndef CONFIG_ONLY
#endif // CONFIG_ONLY





#endif // __LEDS_AUTOPROG_H__
