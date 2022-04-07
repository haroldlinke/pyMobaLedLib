# -*- coding: utf-8 -*-
#
#         MobaLedCheckColors: Color checker for WS2812 and WS2811 based MobaLedLib
#
# * Version: 1.0
# * Author: Harold Linke
# * Date: November 23rd, 2019
# * Copyright: Harold Linke 2019
# *
# * 
# * MobaLedCheckColors on Github: https://github.com/haroldlinke/MobaLedCheckColors
# * 
# *
# * History of Change
# * V1.00 23.11.2019 - Harold Linke - first release
# *
# * MobaLedCheckColors supports the MobaLedLib by Hardi Stengelin
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
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *
# * MobaLedCheckColors is based on tkColorPicker by Juliette Monsel
# * https://sourceforge.net/projects/tkcolorpicker/
# * 
# * tkcolorpicker - Alternative to colorchooser for Tkinter.
# * Copyright 2017 Juliette Monsel <j_4321@protonmail.com>
# * 
# * tkcolorpicker is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# * 
# * tkcolorpicker is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# * 
# * You should have received a copy of the GNU General Public License
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.
# * 
# * The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# * License: http://creativecommons.org/licenses/by-sa/3.0/	
# ***************************************************************************


try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
#from PIL import Image, ImageDraw, ImageTk
from math import atan2, sqrt, pi
import colorsys
import math


#PALETTE = ("#0F0D03","#162C1B", "#9B4905", "#271201", "#1E0000", "#4F2707", "#323232",
#           "#FFFFFF", "#0C0C10", "#464650", "#F5F5FF", "pink", "black",
#           "white", "gray", "saddle brown", "lightgray", "wheat")

#PALETTE = ("Kerze \n 1500K", "Natriumlampe \n 2000K", "Glühlampe \n 2600K", "Hallogenlampe \n 3000K", "Fotolampe \n 3400K", "Neonröhre \n 4000K", "Mondlicht \n 4120K",
#           "Xeonlampe \n 4500K", "Morgensonne \n 5000K", "Nachmtgsonne \n 5500K", "Mittagssonne \n 5800K", "Bed. Himmel \n 7000K", "Nebel \n 8000K",
#           "Blauer Himmel \n 10000K")


# in some python versions round returns a float instead of an int
if not isinstance(round(1.0), int):
    def round2(nb):
        """Round number to 0 digits and return an int."""
        return int(nb + 0.5)  # works because nb >= 0
else:
    round2 = round


# --- conversion functions
def rgb_to_hsv(r, g, b):
    """Convert RGB color to HSV."""
    h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
    return round2(h * 360), round2(s * 100), round2(v * 100)


def hsv_to_rgb(h, s, v):
    """Convert HSV color to RGB."""
    r, g, b = colorsys.hsv_to_rgb(h / 360., s / 100., v / 100.)
    return round2(r * 255), round2(g * 255), round2(b * 255)


def rgb_to_hexa(*args):
    """Convert RGB(A) color to hexadecimal."""
    if len(args) == 3:
        return ("#%2.2x%2.2x%2.2x" % tuple(args)).upper()
    elif len(args) == 4:
        return ("#%2.2x%2.2x%2.2x%2.2x" % tuple(args)).upper()
    else:
        raise ValueError("Wrong number of arguments.")


def hexa_to_rgb(color):
    """Convert hexadecimal color to RGB."""
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    if len(color) == 7:
        return r, g, b
    elif len(color) == 9:
        return r, g, b, int(color[7:9], 16)
    else:
        raise ValueError("Invalid hexadecimal notation.")


def col2hue(r, g, b):
    """Return hue value corresponding to given RGB color."""
    return round2(180 / pi * atan2(sqrt(3) * (g - b), 2 * r - g - b) + 360) % 360


def hue2col(h):
    """Return the color in RGB format corresponding to (h, 100, 100) in HSV."""
    if h < 0 or h > 360:
        raise ValueError("Hue should be between 0 and 360")
    else:
        return hsv_to_rgb(h, 100, 100)


# --- Fake transparent image creation with PIL
def create_checkered_image(width, height, c1=(154, 154, 154, 255),
                           c2=(100, 100, 100, 255), s=6):
    """
    Return a checkered image of size width x height.

    Arguments:
        * width: image width
        * height: image height
        * c1: first color (RGBA)
        * c2: second color (RGBA)
        * s: size of the squares
    """
    im = Image.new("RGBA", (width, height), c1)
    draw = ImageDraw.Draw(im, "RGBA")
    for i in range(s, width, 2 * s):
        for j in range(0, height, 2 * s):
            draw.rectangle(((i, j), ((i + s - 1, j + s - 1))), fill=c2)
    for i in range(0, width, 2 * s):
        for j in range(s, height, 2 * s):
            draw.rectangle(((i, j), ((i + s - 1, j + s - 1))), fill=c2)
    return im


def overlay(image, color):
    """
    Overlay a rectangle of color (RGBA) on the image and return the result.
    """
    width, height = image.size
    im = Image.new("RGBA", (width, height), color)
    preview = Image.alpha_composite(image, im)
    return preview

def convert_K_to_RGB(colour_temperature):
    """
    Converts from K to RGB, algorithm courtesy of
    http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    """
    #range check
    if colour_temperature < 1000:
        colour_temperature = 1000
    elif colour_temperature > 40000:
        colour_temperature = 40000

    tmp_internal = colour_temperature / 100.0

    # red
    if tmp_internal <= 66:
        red = 255
    else:
        tmp_red = 329.698727446 * math.pow(tmp_internal - 60, -0.1332047592)
        if tmp_red < 0:
            red = 0
        elif tmp_red > 255:
            red = 255
        else:
            red = int(tmp_red)

    # green
    if tmp_internal <=66:
        tmp_green = 99.4708025861 * math.log(tmp_internal) - 161.1195681661
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = int(tmp_green)
    else:
        tmp_green = 288.1221695283 * math.pow(tmp_internal - 60, -0.0755148492)
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = int(tmp_green)

    # blue
    if tmp_internal >=66:
        blue = 255
    elif tmp_internal <= 19:
        blue = 0
    else:
        tmp_blue = 138.5177312231 * math.log(tmp_internal - 10) - 305.0447927307
        if tmp_blue < 0:
            blue = 0
        elif tmp_blue > 255:
            blue = 255
        else:
            blue = int(tmp_blue)

    return red, green, blue