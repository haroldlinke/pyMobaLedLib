# -*- coding: utf-8 -*-
#
#         Write header
#
# * Version: 1.00
# * Author: Harold Linke
# * Date: February 2, 2024
# * Copyright: Harold Linke 2024
# *
# *
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# *
# *  
# * https://github.com/Hardi-St/MobaLedLib
# *
# * MobaLedCheckColors is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * MobaLedCheckColors is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  if not, see <http://www.gnu.org/licenses/>.
# *
# *
# ***************************************************************************


# ***************************************************************************
# based on 
# TinyRail-Direkt-Lichtbus-Servo
# Copyright (C) 2023-2024 Dipl.Ing. Joern Eckhart Bardewyck
# Dieses Programm ist freie Software. Sie koennen es unter den Bedingungen der GNU General Public License, wie von der Free Software Foundation veroeffentlicht,
# weitergeben und/oder modifizieren, gemäß Version 3 der GPL Lizenz.
#
# Die Veröffentlichung dieses Programms erfolgt in der Hoffnung, daß es Ihnen von Nutzen sein wird, aber OHNE IRGENDEINE GARANTIE, sogar ohne die implizite
# Garantie der MARKTREIFE oder der VERWENDBARKEIT FÜR EINEN BESTIMMTEN ZWECK. Details finden Sie in der GNU General Public License.
#
# Sie sollten ein Exemplar der GNU General Public License zusammen mit diesem Programm erhalten haben. Falls nicht, siehe <http://www.gnu.org/licenses/>.
#
# Kontakt ueber jbardewyck at t-online punkt de
#******************************************************************************

def CalcCrc4_old(crc, v_byte, bitlen):
    #if (bitlen / 8) > 0:
    #    validbits = 8
    #else:
    #    validbits = bitlen % 8
    validbits = bitlen # bitlen <= 8

    c = v_byte
    for i in range(validbits):
        if ((crc ^ c) & 0x80) != 0:
            crc = ( crc << 1) ^ 0x03
        else:
            crc <<= 1
        c <<= 1
    return crc & 0xF

def TinyRail_GenerateChecksum_old( controlValue, positionValueHigh, positionValueLow, compare=False):
    if controlValue != 0:
        controlNibble = controlValue << 4
        crc4 = CalcCrc4_old( 0, controlNibble, 4)
    
        crc4 = CalcCrc4_old( crc4, positionValueHigh, 8)
        crc4 = CalcCrc4_old( crc4, positionValueLow, 8)
        if ( compare):
            if ( crc4 == ( controlValue >> 4)):
                return 0
            return 1; #checksum failed
        return crc4
    else:
        return controlValue

def CalculateControlValuewithChecksum_old (controlValue, positionValueHigh, positionValueLow):
    
    crc4 =  TinyRail_GenerateChecksum_old( controlValue, positionValueHigh, positionValueLow)
    
    newcontrolvalue = crc4<<4 | (controlValue & 0x0F)
    
    return newcontrolvalue

def CalcCrc4(crc, v_byte, bitlen):
    #if (bitlen / 8) > 0:
    #    validbits = 8
    #else:
    #    validbits = bitlen % 8
    validbits = bitlen # bitlen <= 8

    c = v_byte
    for i in range(validbits):
        if ((crc ^ c) & 0x80) != 0:
            crc = ( crc << 1) ^ 0x03
        else:
            crc <<= 1
        c <<= 1
    return crc

def TinyRail_GenerateChecksum( controlValue, positionValueHigh, positionValueLow, compare=False):
    if controlValue != 0:
        controlNibble = controlValue << 4
        crc4 = CalcCrc4( 0, controlNibble, 4)
    
        crc4 = CalcCrc4( crc4, positionValueHigh, 8)
        crc4 = CalcCrc4( crc4, positionValueLow, 8)
        if ( compare):
            if ( crc4 & 0xF == ( controlValue >> 4)):
                return 0
            return 1; #checksum failed
        return crc4
    else:
        return controlValue

def CalculateControlValuewithChecksum (controlValue, positionValueHigh, positionValueLow):
    
    crc4 =  TinyRail_GenerateChecksum( controlValue, positionValueHigh, positionValueLow)
    
    newcontrolvalue = crc4<<4 | (controlValue & 0x0F)
    
    return newcontrolvalue


