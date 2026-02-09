/*
 MobaLedLib: LED library for model railways
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 Copyright (C) 2018 - 2021  Hardi Stengelin: https://forum.mobaledlib.de

 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
 -------------------------------------------------------------------------------------------------------------

 Dummy for pyMobaLedLib

*/
#ifndef __LIB_CONFIG_H__
#define __LIB_CONFIG_H__
#include <Arduino.h>

#define _USE_SEP_CONST

#define _NEW_INITIALIZE                 // allows to restore input state after constructor before first initialize run    


// Memory usage tests / optimisation                  Flash  Ram   Attention _PRINT_DEBUG_MESSAGES must be disabled
#define _USE_COUNTER        1           // 28.10.18:    592    0
#define _USE_HOUSE          1           // 28.10.18:   2924   18?
#define _USE_SET_COLTAB     1           // 09.12.18:
#define _USE_SET_TVTAB      1           // 10.01.20:    176    4
#define _USE_DEF_NEON       1           // 12.01.20:     96  -31 ?
#define _USE_PATTERN        1           // 28.10.18:   2096    0
#define _USE_FIRE           1           // 28.10.18:    594    0
#define _USE_HSV_GROUP      1           // 28.10.18:     62    0
#define _USE_LOCAL_VAR      1           // 07.11.18:     ??
#define _USE_USE_GLOBALVAR  1           // 26.11.18:    124    2
#define _USE_INCH_TO_VAR    1           // 25.11.18:     ??
#define _USE_LOGIC          1           // 28.10.18:    172    0
#define _USE_RANDOM         1           // 28.10.18:    292    0
#define _USE_RANMUX         1           // 28.10.18:    364    0
#define _USE_WELDING        1           // 28.10.18:    430    0
#define _USE_COPYLED        1           // 28.10.18:    116    0
#define _USE_SCHEDULE       1           // 28.10.18:    264    0
#define _USE_STORE_STATUS   1           // 22.04.20:    138    5                                              // 19.05.20: Juergen
#define _USE_INCH_TRIGGER   1           // 08.06.20:    -12    0
#define _USE_CANDLE         1           // 10.06.20:    352    2                                              // 09.06.20:
#define _USE_EXT_PROC       1           // 26.09.21:     48    4                                              // 26.09.21: Juergen
                                        //             8800    Sum
// Memory usage tests / optimisation                  Flash  Ram   Attention _PRINT_DEBUG_MESSAGES must be disabled
#define _USE_COUNTER        1           // 28.10.18:    592    0
#define _USE_HOUSE          1           // 28.10.18:   2924   18?
#define _USE_SET_COLTAB     1           // 09.12.18:
#define _USE_SET_TVTAB      1           // 10.01.20:    176    4
#define _USE_DEF_NEON       1           // 12.01.20:     96  -31 ?
#define _USE_PATTERN        1           // 28.10.18:   2096    0
#define _USE_FIRE           1           // 28.10.18:    594    0
#define _USE_HSV_GROUP      1           // 28.10.18:     62    0
#define _USE_LOCAL_VAR      1           // 07.11.18:     ??
#define _USE_USE_GLOBALVAR  1           // 26.11.18:    124    2
#define _USE_INCH_TO_VAR    1           // 25.11.18:     ??
#define _USE_LOGIC          1           // 28.10.18:    172    0
#define _USE_RANDOM         1           // 28.10.18:    292    0
#define _USE_RANMUX         1           // 28.10.18:    364    0
#define _USE_WELDING        1           // 28.10.18:    430    0
#define _USE_COPYLED        1           // 28.10.18:    116    0
#define _USE_SCHEDULE       1           // 28.10.18:    264    0
#define _USE_STORE_STATUS   1           // 22.04.20:    138    5                                              // 19.05.20: Juergen
#define _USE_INCH_TRIGGER   1           // 08.06.20:    -12    0
#define _USE_CANDLE         1           // 10.06.20:    352    2                                              // 09.06.20:
#define _USE_EXT_PROC       1           // 26.09.21:     48    4                                              // 26.09.21: Juergen
                                        //             8800    Sum  
#endif // __LIB_CONFIG_H__
