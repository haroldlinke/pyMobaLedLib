/*
TinyRail-Direkt-Lichtbus-Bootloader/Bootupdater
Copyright (C) 2023-2024 Dipl.Ing. Joern Eckhart Bardewyck

Dieses Programm ist freie Software. Sie koennen es unter den Bedingungen der GNU General Public License, wie von der Free Software Foundation veroeffentlicht,
weitergeben und/oder modifizieren, gemaess Version 3 der GPL Lizenz.

Die Veroeffentlichung dieses Programms erfolgt in der Hoffnung, dass es Ihnen von Nutzen sein wird, aber OHNE IRGENDEINE GARANTIE, sogar ohne die implizite
Garantie der MARKTREIFE oder der VERWENDBARKEIT FUER EINEN BESTIMMTEN ZWECK. Details finden Sie in der GNU General Public License.

Sie sollten ein Exemplar der GNU General Public License zusammen mit diesem Programm erhalten haben. Falls nicht, siehe <http://www.gnu.org/licenses/>.

Kontakt ueber jbardewyck at t-online punkt de

High V.                  ATTiny 85       Prog.
Prog.                    +-\/-+
       LED 2 Reset PB5  1|    |8  VCC
       LED 1 PWM   PB3  2|    |7  PB2    SCK      Servo 2   SoftwareSerial
LED    LED 0 PWM   PB4  3|    |6  PB1    MISO     Servo 1
                   GND  4|    |5  PB0    MOSI     Servo 0
                         +----+

                         ATTiny 84
                         +-\/-+
                   vcc  1|    |14 GND
 D0     Servo 0    PB0  2|    |13 PA0    LED 1 PWM  D10
 D1     Servo 1    PB1  3|    |12 PA1    LED 0 PWM  D9
        Reset      PB3  4|    |11 PA2    LED 2 PWM  D8
 D2     Servo 2    PB2  5|    |10 PA3               D7
 D3                PA7  6|    |9  PA4    SCK        D6    SoftwareSerial
 D4     MOSI       PA6  7|    |8  PA5    MISO       D5


Bootloader fuer ATTiny85 fuses: lfuse 0xE1, hfuse 0x55, efuse 0xFE
Bootloader fuer ATTIny84 fuses: lfuse 0xFF, hfuse 0x55, efuse 0xFE

Der Steuerkanal ist wie folgt strukturiert:

--------------------------------------------------------------------------------------------------------------
|     | CRC-4 nach ITU | ENTER-Bit | Command 0..7 | 2. Byte Modulo | 3. Byte reserved | 4.-24. Byte HEX-Data |
--------------------------------------------------------------------------------------------------------------
| Bit |        7 6 5 4 |         3 |        2 1 0 |                |                  |                      |
--------------------------------------------------------------------------------------------------------------
|     |        0 0 0 0 |         0 |        0 0 0 |         unused |           unused |               unused | idle, nothing to do
--------------------------------------------------------------------------------------------------------------
|     |        invalid |         X |        X X X | not applicable |   not applicable |       not applicable | failure on WS2811 Bus
--------------------------------------------------------------------------------------------------------------
|     |          valid |   first 1 |        0 0 1 |    modulo (*1) |                0 |        HEX-File-Data | TRANSFER Update File first block/line
--------------------------------------------------------------------------------------------------------------
|     |          valid |  follow 0 |        0 0 1 |    modulo (*1) |                0 |        HEX-File-Data | TRANSFER Update File following blocks/lines
--------------------------------------------------------------------------------------------------------------

Nur fuer den Bootupdater zusaetzlich:

--------------------------------------------------------------------------------------------------------------
|     |          valid |         0 |        0 1 0 |              0 |                0 |                all 0 | prerequisite: enter bootloader
--------------------------------------------------------------------------------------------------------------
|     |          valid |         1 |        0 1 0 |              0 |                0 |                all 0 | execute: enter bootloader
--------------------------------------------------------------------------------------------------------------

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

// #define TINYRAIL_DEBUG from makefile now!

#define CONTROL_BIT_NUMBER          (24*8)
#define TRANSMIT_BIT_NUMBER         24

#define IPR_UPDATE_STATE_FLAG_OLD_FLASH_OK                  0x0001
#define IPR_UPDATE_STATE_FLAG_NEW_FLASH_OK                  0x0002
#define IPR_UPDATE_STATE_FLAG_REC_CRC16                     0x0004
#define IPR_UPDATE_STATE_FLAG_REC_CRC16_VALID               0x0008
#define IPR_UPDATE_STATE_FLAG_UPDATE_REQUESTED              0x0010
#define IPR_UPDATE_STATE_FLAG_ADDRESS_RANGE_ILLEGAL         0x0020
#define IPR_UPDATE_STATE_FLAG_REC_HARDWARE_TYPE             0x0040
#define IPR_UPDATE_STATE_FLAG_REC_HARDWARE_TYPE_VALID       0x0080
#define IPR_UPDATE_STATE_FLAG_REC_HARDWARE_REVISION         0x0100
#define IPR_UPDATE_STATE_FLAG_REC_HARDWARE_REVISION_VALID   0x0200
#define IPR_UPDATE_STATE_FLAG_REC_SOFTWARE_VERSION          0x0400
#define IPR_UPDATE_STATE_FLAG_REC_SOFTWARE_VERSION_VALID    0x0800
#define IPR_UPDATE_STATE_FLAG_REC_SERIAL_NUMBER             0x1000
#define IPR_UPDATE_STATE_FLAG_REC_SERIAL_NUMBER_VALID       0x2000

uint8_t recBuffer[CONTROL_BIT_NUMBER/8];
uint8_t transmitBuffer[TRANSMIT_BIT_NUMBER/8] = { 0, 0, 0};
uint8_t lastControl = 0;
uint8_t modulo = 0;
unsigned short updateStateFlags    = 0;
unsigned short tinyRecCrc16        = 0;
unsigned short calcCrc16           = 0xFFFF;
unsigned short firstAddress        = 0xFFFF;
unsigned short lastAddress         = 0;
#ifdef RAILMAIL_TINY_BOOT_UPDATER
uint16_t       resetVectorBackup   = 0;
uint16_t       t0ca_A_VectorBackup = 0;
#endif // ifdef RAILMAIL_TINY_BOOT_UPDATER
unsigned short hardwareTypeHigh    = 0;
unsigned char  flashStateFlags     = IPR_FLASH_STATE_FLAGS_NONE;
#ifdef TINYRAIL_DEBUG
uint16_t        crcErrorCounter    = 0;
#endif // ifdef TINYRAIL_DEBUG

unsigned short IprCalculateChecksum( unsigned char  addressType,
                                     unsigned short calcAddress,
                                     unsigned short calcLength,
                                     unsigned short crc16)
{
    unsigned short calcIndex;
    unsigned short c;
    unsigned char  i;


    for ( calcIndex = 0; calcIndex < calcLength; calcIndex++)
    {
        if ( addressType)
            c = ( ( unsigned short)pgm_read_byte( calcAddress + calcIndex)) << 8;
        else
            c = ( ( unsigned short)( *( unsigned char *)( unsigned short)( calcAddress + calcIndex))) << 8;
        for ( i = 0; i < 8; i++)
        {
            if ( ( crc16 ^ c) & 0x8000)
                crc16 = ( crc16 << 1) ^ 0x0589;
            else
                crc16 <<= 1;
            c <<= 1;
        }
    }
    return crc16;
}


/*unsigned short IprCalcCheckNext256PageBorder( unsigned short dummyAddress, unsigned short calcCrc16)
{
    uint8_t dummyNand = 0xFF;

    // calc CRC up to next page (256) border
    while ( dummyAddress & ~0xFF00)
    {
        calcCrc16 = IprCalculateChecksum( 0, ( unsigned short)&dummyNand, 1, calcCrc16);
        dummyAddress++;
    }
    return calcCrc16;
}*/

void flash_line_data( unsigned char *lineData)
{
    unsigned char indexFill;

    for ( indexFill = 0; indexFill < lineData[0]; indexFill += 2)
    {
        unsigned short currentAddress = ( ( unsigned short)lineData[1] << 8) + ( unsigned short)lineData[2] + ( unsigned short)indexFill;

        // protect against selfoverpatching
        if ( ( currentAddress >= USED_TEXT_START)
            && ( currentAddress <= USED_TEXT_END))
            updateStateFlags |= IPR_UPDATE_STATE_FLAG_ADDRESS_RANGE_ILLEGAL;
        else
        {
            uint8_t sreg = SREG;

            cli();

            if ( firstAddress > currentAddress)
                firstAddress = currentAddress;

            // if other page, flash previous page
            if ( lastAddress && ( ( currentAddress & 0xFFC0) != ( lastAddress & 0xFFC0)))
            {
                unsigned short indexFlash;

                // DPRINTF_P( PSTR( "flash page %x\n"), ( unsigned)lastAddress);

                updateStateFlags &= ~IPR_UPDATE_STATE_FLAG_OLD_FLASH_OK;

                boot_page_erase_safe( lastAddress);
                boot_page_write_safe( lastAddress);

                // init next page with 0xFF
                for ( indexFlash = 0; indexFlash < 64; indexFlash += 2)
                    boot_page_fill_safe( ( currentAddress & 0xFFC0) + indexFlash, 0xFFFF);

#ifdef RAILMAIL_TINY_BOOT_UPDATER
                if ( !( lastAddress & 0xFFC0))
                {
                    // DPRINTF_P( PSTR( "vector page %x, %x, %x\n"), ( unsigned)lastAddress, resetVectorBackup, t0ca_A_VectorBackup);

                    for ( indexFlash = 0; indexFlash < 64; indexFlash += 2)
                    {
                        uint16_t dummyData;

                        if ( !indexFlash)
                            dummyData = resetVectorBackup;
                        else if ( indexFlash == ( TIMER0_COMPA_VECTOR_NUMBER << 1))
                            dummyData = t0ca_A_VectorBackup;
                        else
                            dummyData = pgm_read_word( indexFlash);

                        calcCrc16 = IprCalculateChecksum( 0, ( unsigned short)&dummyData, 2, calcCrc16);
                    }
                }
                else
#endif // ifdef RAILMAIL_TINY_BOOT_UPDATER
                    calcCrc16 = IprCalculateChecksum( 1, lastAddress & 0xFFC0, ( lastAddress & ~0xFFC0) + 2, calcCrc16);
                    // calcCrc16 = IprCalculateChecksum( 1, lastAddress & 0xFFC0, 64, calcCrc16);
            }

#ifdef RAILMAIL_TINY_BOOT_UPDATER
            if ( !currentAddress)
            {
                resetVectorBackup = lineData[4+indexFill] + ( lineData[4+indexFill+1] << 8);
                boot_page_fill_safe( currentAddress, 0xC000 + ( USED_TEXT_START >> 1) - 1);
                // boot_page_fill_safe( currentAddress, pgm_read_word( USED_TEXT_START + ( 0x0 << 1)) + ( ( USED_TEXT_START) >> 1));
            }
            else if ( currentAddress == ( TIMER0_COMPA_VECTOR_NUMBER << 1))
            {
                t0ca_A_VectorBackup = lineData[4+indexFill] + ( lineData[4+indexFill+1] << 8);
                boot_page_fill_safe( currentAddress, 0xC000 + ( USED_TEXT_START >> 1) - 1 + TIMER0_COMPA_VECTOR_SHADOW - TIMER0_COMPA_VECTOR_NUMBER);
                // boot_page_fill_safe( currentAddress, pgm_read_word( USED_TEXT_START + ( TIMER0_COMPA_VECTOR_NUMBER << 1)) + ( ( USED_TEXT_START) >> 1));
            }
            else
#endif // ifdef RAILMAIL_TINY_BOOT_UPDATER
                boot_page_fill_safe( currentAddress, lineData[4+indexFill] + ( lineData[4+indexFill+1] << 8));

            SREG = sreg;

            lastAddress = currentAddress;
        }
    }
}

void flash_last_page( void)
{
    if ( lastAddress)
    {
        uint8_t sreg = SREG;

        // DPRINTF_P( PSTR( "last flash page %x\n"), ( unsigned)lastAddress);

        updateStateFlags &= ~IPR_UPDATE_STATE_FLAG_OLD_FLASH_OK;

        cli();

        boot_page_erase_safe( lastAddress);
        boot_page_write_safe( lastAddress);

        SREG = sreg;

        calcCrc16 = IprCalculateChecksum( 1, lastAddress & 0xFFC0, ( lastAddress & ~0xFFC0) + 2, calcCrc16);
        /*calcCrc16 = IprCalculateChecksum( 1, lastAddress & 0xFFC0, 64, calcCrc16);

        {
            unsigned short dummyAddress = lastAddress;

            dummyAddress &= 0xFFC0;
            dummyAddress += 64;
            calcCrc16 = IprCalcCheckNext256PageBorder( dummyAddress, calcCrc16);
        }*/

        DPRINTF_P( PSTR( "calcCrc16 %X, tinyRecCrc16 %X\n"), calcCrc16, tinyRecCrc16);

        if ( ( updateStateFlags & IPR_UPDATE_STATE_FLAG_REC_CRC16) && ( calcCrc16 == tinyRecCrc16))
#ifdef RAILMAIL_TINY_BOOT_UPDATER
        {
            uint8_t        sreg = SREG;
            unsigned short indexFlash;
            uint16_t       dummyData;

            for ( indexFlash = 0; indexFlash < 64; indexFlash += 2)
            {
                if ( !indexFlash)
                    dummyData = resetVectorBackup;
                else if ( indexFlash == ( TIMER0_COMPA_VECTOR_NUMBER << 1))
                    dummyData = t0ca_A_VectorBackup;
                else
                    dummyData = pgm_read_word( indexFlash);

                boot_page_fill_safe( indexFlash, dummyData);
            }

            cli();

            boot_page_erase_safe( 0);
            boot_page_write_safe( 0);

            SREG = sreg;

            my_eeprom_write_word( &BOOT_INFO.flashBootStart, firstAddress);
            my_eeprom_write_word( &BOOT_INFO.flashBootEnd, lastAddress + 2);
            my_eeprom_write_word( &BOOT_INFO.flashBootCrc16, calcCrc16);
        }
#else // ifdef RAILMAIL_TINY_BOOT_UPDATER
        {
            my_eeprom_write_word( &BOOT_INFO.flashMainStart, firstAddress);
            my_eeprom_write_word( &BOOT_INFO.flashMainEnd, lastAddress + 2);
            my_eeprom_write_word( &BOOT_INFO.flashMainCrc16, calcCrc16);

            updateStateFlags |= ( IPR_UPDATE_STATE_FLAG_REC_CRC16_VALID | IPR_UPDATE_STATE_FLAG_NEW_FLASH_OK);
        }
#endif // else // ifdef RAILMAIL_TINY_BOOT_UPDATER
    }
}

#ifdef xRAILMAIL_TINY_BOOT_UPDATER
void IprModifyFlash( unsigned short flashAddress,
                     unsigned char  patchAddressType,
                     unsigned short patchAddress,
                     unsigned short patchLength)
{
    unsigned short indexFlash;
    uint8_t        sreg = SREG;

    cli();

    for ( indexFlash = 0; indexFlash < 64; indexFlash += 2)
    {
        if ( ( indexFlash >= ( flashAddress & 0x003F))
          && ( ( indexFlash + 1) < ( ( flashAddress & 0x003F) + patchLength)))
        {
            // DPRINTF_P( PSTR( "patch flash address %x\n"), ( flashAddress & 0xFFC0) + indexFlash);

            if ( patchAddressType)
                boot_page_fill_safe( ( flashAddress & 0xFFC0) + indexFlash,
                                     pgm_read_word( patchAddress + ( indexFlash - ( flashAddress & 0x003F))));
            else
                boot_page_fill_safe( ( flashAddress & 0xFFC0) + indexFlash,
                                     *( unsigned short *)( unsigned short)( patchAddress + ( indexFlash - ( flashAddress & 0x003F))));
        }
        else
            boot_page_fill_safe( ( flashAddress & 0xFFC0) + indexFlash,
                                 pgm_read_word( ( flashAddress & 0xFFC0) + indexFlash));
    }

    boot_page_erase_safe( flashAddress);
    boot_page_write_safe( flashAddress);

    SREG = sreg;
}

void Tiny_ModifyVectors()
{
    uint16_t patchArg;

    DPRINTF_P( PSTR( "Curr Reset: %x, boot %x\n"), pgm_read_word( USED_TEXT_START), pgm_read_word( 0));
    DPRINTF_P( PSTR( "Curr T0CA: %x, boot %x\n"), pgm_read_word( USED_TEXT_START + ( TIMER0_COMPA_VECTOR_NUMBER << 1)), pgm_read_word( TIMER0_COMPA_VECTOR_NUMBER << 1));

    patchArg = pgm_read_word( USED_TEXT_START + ( 0x0 << 1)) + ( ( USED_TEXT_START) >> 1);
    IprModifyFlash( ( 0x0 << 1), 0, ( unsigned short)&patchArg, 2);
    patchArg = pgm_read_word( USED_TEXT_START + ( TIMER0_COMPA_VECTOR_NUMBER << 1)) + ( ( USED_TEXT_START) >> 1);
    IprModifyFlash( ( TIMER0_COMPA_VECTOR_NUMBER << 1), 0, ( unsigned short)&patchArg, 2);

    DPRINTF_P( PSTR( "New Reset: %x, boot %x\n"), pgm_read_word( USED_TEXT_START), pgm_read_word( 0));
    DPRINTF_P( PSTR( "New T0CA: %x, boot %x\n"), pgm_read_word( USED_TEXT_START + ( TIMER0_COMPA_VECTOR_NUMBER << 1)), pgm_read_word( TIMER0_COMPA_VECTOR_NUMBER << 1));
}
#endif // ifdef RAILMAIL_TINY_BOOT_UPDATER

#ifdef TINYRAIL_DEBUG
uint32_t lastCounter = 0;
uint8_t xxxCount = 0;
#endif // ifdef TINYRAIL_DEBUG

uint8_t loopCount = 0;

#ifdef RAILMAIL_TINY_BOOT_UPDATER
    #define UPDATE_SIGNAL_CHANNEL   1
#else // ifdef RAILMAIL_TINY_BOOT_UPDATER
    #define UPDATE_SIGNAL_CHANNEL   0
#endif // else // ifdef RAILMAIL_TINY_BOOT_UPDATER

uint16_t transmitZeroBits = 0;

void BlinkState( uint8_t state)
{
    loopCount++;
    if ( ( loopCount & ( 0x80 >> state)))
    {
        transmitBuffer[UPDATE_SIGNAL_CHANNEL] = 64;
        TinyRail_SetStatusLED( 1);
    }
    else
    {
        transmitBuffer[UPDATE_SIGNAL_CHANNEL] = 0;
        TinyRail_SetStatusLED( 0);
    }
}

int main( void)
{
    uint8_t osccalBackup = OSCCAL;

#if defined( __AVR_ATtiny85__) && ( F_CPU==20000000UL)
    OSCCAL += 40; // go for 20MHz with internal oscillator
#else // if defined( __AVR_ATtiny85__) && ( F_CPU==20000000UL)
    OSCCAL += DEVIATION_STANDARD_OSCCAL_ADD;
#endif // else // if defined( __AVR_ATtiny85__) && ( F_CPU==20000000UL)

#ifdef TINYRAIL_DEBUG
    TinyRail_SUART_Init();
#endif // ifdef TINYRAIL_DEBUG
    TinyRail_InitMainTimer();
    TinyRail_InitStatusLED();
    TinyRail_SetStatusLED( 1);

#ifdef RAILMAIL_TINY_BOOT_UPDATER
    // Tiny_ModifyVectors();
#endif // ifdef RAILMAIL_TINY_BOOT_UPDATER

#ifdef RAILMAIL_TINY_BOOT_UPDATER
    // my_eeprom_write_byte( &BOOT_INFO.bootSig[0], 0xA5);
    Boot_InfoInit();
    flashStateFlags = my_eeprom_read_byte( &BOOT_INFO.flashStateFlags);

    // if ( !IprCheckBootloaderProgramFlash())
    //     updateStateFlags |= IPR_UPDATE_STATE_FLAG_OLD_FLASH_OK;

    // clear update request because we are running successfully
    // or bootloader redirect is enabled and we have called ourself
    if ( flashStateFlags & ( IPR_FLASH_STATE_FLAG_UPDATE_REQUEST | IPR_FLASH_STATE_FLAG_RESET_REQUEST))
    {
        flashStateFlags &= ~( IPR_FLASH_STATE_FLAG_UPDATE_REQUEST | IPR_FLASH_STATE_FLAG_RESET_REQUEST);
        my_eeprom_write_byte( &BOOT_INFO.flashStateFlags, flashStateFlags);
    }

    {
        unsigned short usedFlashStart = my_eeprom_read_word( &BOOT_INFO.flashMainStart);
        unsigned short dummyAddress   = my_eeprom_read_word( &BOOT_INFO.flashMainEnd);
        unsigned short calcCrc16      = 0xFFFF;

        DPRINTF_P( PSTR( "MainFlash %x, %x, %x\n"), usedFlashStart, dummyAddress, ( uint16_t)flashStateFlags);

        if ( ( usedFlashStart >= USED_TEXT_START) && ( dummyAddress < 8192) && ( usedFlashStart < dummyAddress))
        {
            calcCrc16 = IprCalculateChecksum( 1, usedFlashStart, dummyAddress - usedFlashStart, calcCrc16);
            // calcCrc16 = IprCalcCheckNext256PageBorder( dummyAddress, calcCrc16);

            DPRINTF_P( PSTR( "MainFlash CRC %x, %x\n"), calcCrc16, my_eeprom_read_word( &BOOT_INFO.flashMainCrc16));
        }
    }

    {
        unsigned short usedFlashStart = my_eeprom_read_word( &BOOT_INFO.flashBootStart);
        unsigned short dummyAddress   = my_eeprom_read_word( &BOOT_INFO.flashBootEnd);
        unsigned short calcCrc16      = 0xFFFF;

        DPRINTF_P( PSTR( "BootFlash %x, %x, %x\n"), usedFlashStart, dummyAddress, ( uint16_t)flashStateFlags);

        if ( ( usedFlashStart < USED_TEXT_START) && ( dummyAddress < USED_TEXT_START) && ( usedFlashStart < dummyAddress))
        {
            calcCrc16 = IprCalculateChecksum( 1, usedFlashStart, dummyAddress - usedFlashStart, calcCrc16);
            // calcCrc16 = IprCalcCheckNext256PageBorder( dummyAddress, calcCrc16);

            DPRINTF_P( PSTR( "BootFlash CRC %x, %x\n"), calcCrc16, my_eeprom_read_word( &BOOT_INFO.flashBootCrc16));
        }
    }
#else // ifdef RAILMAIL_TINY_BOOT_UPDATER
    flashStateFlags = my_eeprom_read_byte( &BOOT_INFO.flashStateFlags);
    if ( flashStateFlags == 0xFF)
        flashStateFlags = IPR_FLASH_STATE_FLAGS_NONE;
    else
    {
        unsigned short usedFlashStart = my_eeprom_read_word( &BOOT_INFO.flashMainStart);
        unsigned short dummyAddress   = my_eeprom_read_word( &BOOT_INFO.flashMainEnd);
        unsigned short calcCrc16      = 0xFFFF;

        DPRINTF_P( PSTR( "MainFlash %x, %x, %x\n"), usedFlashStart, dummyAddress, ( uint16_t)flashStateFlags);

        if ( ( usedFlashStart > USED_TEXT_END) && ( dummyAddress < 8192) && ( usedFlashStart < dummyAddress))
        {
            calcCrc16 = IprCalculateChecksum( 1, usedFlashStart, dummyAddress - usedFlashStart, calcCrc16);
            // calcCrc16 = IprCalcCheckNext256PageBorder( dummyAddress, calcCrc16);

            if ( calcCrc16 == my_eeprom_read_word( &BOOT_INFO.flashMainCrc16))
                updateStateFlags |= IPR_UPDATE_STATE_FLAG_OLD_FLASH_OK;

            DPRINTF_P( PSTR( "MainFlash CRC %x, %x\n"), calcCrc16, my_eeprom_read_word( &BOOT_INFO.flashMainCrc16));
        }

        hardwareTypeHigh = my_eeprom_read_word( &BOOT_INFO.hardwareTypeHigh);
        // hardwareType = my_eeprom_read_word( &BOOT_INFO.hardwareTypeLow) + ( ( unsigned long)my_eeprom_read_word( &BOOT_INFO.hardwareTypeHigh) << 16);
    }
#endif // else // ifdef RAILMAIL_TINY_BOOT_UPDATER

#ifdef RAILMAIL_TINY_BOOT_UPDATER
    while ( !( flashStateFlags & ( IPR_FLASH_STATE_FLAG_UPDATE_REQUEST | IPR_FLASH_STATE_FLAG_RESET_REQUEST)))
#else // ifdef RAILMAIL_TINY_BOOT_UPDATER
    while ( ( ( flashStateFlags & IPR_FLASH_STATE_FLAG_UPDATE_REQUEST) || !( updateStateFlags & IPR_UPDATE_STATE_FLAG_OLD_FLASH_OK))
         && !( updateStateFlags & IPR_UPDATE_STATE_FLAG_NEW_FLASH_OK))
#endif // else // ifdef RAILMAIL_TINY_BOOT_UPDATER
    {
#ifdef TINYRAIL_DEBUG
        uint32_t useCounter;
        uint32_t timeDelta;

        useCounter = hiresTimerCounter;
        while ( useCounter != hiresTimerCounter)
            useCounter = hiresTimerCounter;
        if ( useCounter >= lastCounter)
            timeDelta = useCounter - lastCounter;
        else
            timeDelta = useCounter + ( 0xFFFFFFFFL - lastCounter);

        if ( timeDelta >= ( F_CPU / 333))
#endif // ifdef TINYRAIL_DEBUG
        {
            uint8_t  blinkState = 1;
            uint16_t recLength;

#ifdef TINYRAIL_DEBUG
            TinyRail_SUART_Suspend( 1, 1);
#endif // ifdef TINYRAIL_DEBUG

            recLength = TINYRAIL_WS2811ReceiveEnvelop( recBuffer, CONTROL_BIT_NUMBER, transmitZeroBits >> 8, transmitZeroBits & 0xFF, TRANSMIT_BIT_NUMBER, transmitBuffer);
            if ( ( recLength >= CONTROL_BIT_NUMBER) && !Distri_GenerateChecksum( recBuffer, CONTROL_BIT_NUMBER / 8, 1))
            {
                switch ( recBuffer[0] & UPDATE_CONTROL_MODE_MASK)
                {
#if defined( RAILMAIL_TINY_BOOT_UPDATER)
                    case UPDATE_CONTROL_MODE_ENTER_BOOTLOADER :
                        if ( ( recBuffer[0] & GENERAL_CONTROL_BIT_ENTER_OR_FIRST)
                          && ( ( lastControl & UPDATE_CONTROL_MODE_MASK) == UPDATE_CONTROL_MODE_ENTER_BOOTLOADER)
                          && !( lastControl & GENERAL_CONTROL_BIT_ENTER_OR_FIRST))
                        {
                            flashStateFlags |= IPR_FLASH_STATE_FLAG_UPDATE_REQUEST;
                        }
                        break;
#endif // if defined( RAILMAIL_TINY_BOOT_UPDATER)

                    case UPDATE_CONTROL_MODE_CONFIG_BOOTLOADER :
                        transmitZeroBits =  *( ( uint16_t *)&recBuffer[1]);
                        break;

                    case UPDATE_CONTROL_MODE_TRANSFER :
                        if ( ( recBuffer[0] & GENERAL_CONTROL_BIT_ENTER_OR_FIRST) && !( lastControl & GENERAL_CONTROL_BIT_ENTER_OR_FIRST))
                        {
                            uint8_t indexFlash;

                            updateStateFlags = 0;
                            modulo           = 0;
                            calcCrc16        = 0xFFFF;
                            firstAddress     = 0xFFFF;
                            lastAddress      = 0;

                            for ( indexFlash = 0; indexFlash < 64; indexFlash += 2)
                                boot_page_fill_safe( ( lastAddress & 0xFFC0) + indexFlash, 0xFFFF);
                        }

                        if ( recBuffer[1] == modulo)
                        {
                            uint8_t *lineData      = &recBuffer[3];
                            uint8_t lineDataLength = 5 + lineData[0];

                            // DPRINTF_P( PSTR( "rec modulo %d\n"), ( unsigned)recBuffer[1]);

                            if ( lineData[0])
                            {
                                unsigned char checksum = 0xFF;
                                unsigned char indexChecksum;

                                for ( indexChecksum = 0; indexChecksum < ( lineDataLength - 1); indexChecksum++)
                                    checksum += lineData[indexChecksum];

                                if ( checksum == ( unsigned char)~lineData[lineDataLength-1])
                                {
                                    switch ( lineData[3])
                                    {
                                        case 0x00 :
                                            if ( ( updateStateFlags & IPR_UPDATE_STATE_FLAG_REC_CRC16)
                                              && ( updateStateFlags & IPR_UPDATE_STATE_FLAG_REC_HARDWARE_TYPE_VALID))
                                            {
                                                flash_line_data( lineData);
                                                blinkState = 2;
                                            }
                                            else
                                                blinkState = 4;
                                            break;

                                        case 0x06 :
                                            tinyRecCrc16 = ( ( unsigned short)lineData[4] << 8) + ( unsigned short)lineData[5];
                                            updateStateFlags |= IPR_UPDATE_STATE_FLAG_REC_CRC16;
                                            break;

                                        case 0x07 :
                                            {
                                                unsigned short recHardwareTypeHigh = ( ( unsigned short)lineData[4] << 8)
                                                                                   + ( unsigned short)lineData[5];
                                                /*unsigned long recHardwareType = ( ( unsigned long)lineData[4] << 24)
                                                                              + ( ( unsigned long)lineData[5] << 16)
                                                                              + ( ( unsigned long)lineData[6] << 8)
                                                                              + ( unsigned long)lineData[7];*/
                                                if (
                                                #if defined( __AVR_ATtiny84__)
                                                     ( recHardwareTypeHigh & IP_RAIL_HARDWARE_ATTINY84_HIGH)
                                                #elif defined( __AVR_ATtiny85__) // if defined( __AVR_ATtiny84__)
                                                     ( recHardwareTypeHigh & IP_RAIL_HARDWARE_ATTINY85_HIGH)
                                                #endif // elif defined( __AVR_ATtiny85__) // if defined( __AVR_ATtiny85__)

                                                #if defined( RAILMAIL_TINY_BOOT_UPDATER)
                                                  && ( recHardwareTypeHigh & IP_RAIL_MODULE_BOOTLOADER_HIGH)
                                                #else // if defined( RAILMAIL_TINY_BOOT_UPDATER)
                                                  && !( recHardwareTypeHigh & IP_RAIL_MODULE_BOOTLOADER_HIGH)
                                                  && ( ( recHardwareTypeHigh == hardwareTypeHigh)
                                                    || ( recHardwareTypeHigh & IP_RAIL_MODULE_BOOT_UPDATER_HIGH)
                                                    || ( hardwareTypeHigh == 0))
                                                #endif // else // if defined( RAILMAIL_TINY_BOOT_UPDATER)
                                                   )
                                                    updateStateFlags |= IPR_UPDATE_STATE_FLAG_REC_HARDWARE_TYPE_VALID;
                                                else
                                                {
                                                    DPRINTF_P( PSTR( "HW not supp %x\n"), recHardwareTypeHigh);
                                                }
                                            }
                                            break;

                                        default :
                                            // DPRINTF_P( PSTR( "HEX unsupp cmd %x\n"), lineData[3]);
                                            break;
                                    }
                                }
                            }
                            else
                            {
                                if ( lineData[3] == 0x01)
                                {
                                    flash_last_page();
                                }
                            }

                            modulo++;
                        }
                        break;
                }
                lastControl = recBuffer[0];
            }
#ifdef TINYRAIL_DEBUG
            else
            {
                crcErrorCounter++;
            }
#endif // ifdef TINYRAIL_DEBUG

            BlinkState( blinkState);

#ifdef TINYRAIL_DEBUG
            TinyRail_SUART_Resume();
#endif // ifdef TINYRAIL_DEBUG

#ifdef TINYRAIL_DEBUG
            if ( !( xxxCount++ % 64))
            {
                DPRINTF_P( PSTR( "Step len %u, crc %u: %x, %x, %x, %x, %x, %x, %x, %x, %x, %x\n"), recLength, crcErrorCounter, ( unsigned)recBuffer[0], ( unsigned)recBuffer[1], ( unsigned)recBuffer[2], ( unsigned)recBuffer[3], ( unsigned)recBuffer[4], ( unsigned)recBuffer[5], ( unsigned)recBuffer[6], ( unsigned)recBuffer[7], ( unsigned)recBuffer[8], ( unsigned)recBuffer[9]);
            }
#endif // ifdef TINYRAIL_DEBUG

#ifdef TINYRAIL_DEBUG
            useCounter = hiresTimerCounter;
                while ( useCounter != hiresTimerCounter)
            useCounter = hiresTimerCounter;
            lastCounter = useCounter;
#endif // ifdef TINYRAIL_DEBUG
        }
    }

    OSCCAL = osccalBackup;

#ifdef TINYRAIL_DEBUG
    TinyRail_SUART_Suspend( 2, 1);
#endif // ifdef TINYRAIL_DEBUG

    TinyRail_DeinitMainTimer();

    cli();

    my_eeprom_write_byte( &BOOT_INFO.flashStateFlags, flashStateFlags);
    my_eeprom_busy_wait();

#if defined( RAILMAIL_TINY_BOOTLOADER)
    {
        void ( *start_appl_main)( void) = ( void ( *)(void))( ( USED_TEXT_END + 1) >> 1);

        start_appl_main();
    }
#elif defined( RAILMAIL_TINY_BOOT_UPDATER) // if defined( RAILMAIL_TINY_BOOTLOADER)
    {
        void ( *start_bootloader)( void) = ( void ( *)(void))0x0000;

        start_bootloader();
    }
#endif // elif defined( RAILMAIL_TINY_BOOT_UPDATER) // if defined( RAILMAIL_TINY_BOOTLOADER)
    return 0;
}

