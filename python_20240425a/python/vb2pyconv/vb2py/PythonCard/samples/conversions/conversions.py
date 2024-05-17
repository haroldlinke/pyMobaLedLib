#!/usr/bin/python

"""
conversions provides conversion between english <-> morse code and celsius
"""
__version__ = "$Revision: 1.17 $"
__date__ = "$Date: 2005/12/13 11:13:22 $"

from PythonCard import model
try:
    import SOAP
    SOAP_AVAILABLE = True
except ImportError:
    SOAP_AVAILABLE = False


class Conversion:
    def __init__(self, components):
        pass

    def toDown(self, value):
        pass

    def toUp(self, value):
        pass
    
class TemperatureConversion(Conversion):
    def __init__(self, components):
        components.labelUp.text = 'Fahrenheit'
        components.btnConvertUp.label = 'Celsius to Fahrenheit'
        components.btnConvertDown.label = 'Fahrenheit to Celsius'
        components.labelDown.text = 'Celsius'

    def toDown(self, degrees):
        return str(self.FahrenheitToCelsius(float(degrees)))

    def toUp(self, degrees):
        return str(self.CelsiusToFahrenheit(float(degrees)))

    def FahrenheitToCelsius(self, degrees):
        return (degrees - 32.0) / 9.0 * 5.0

    def CelsiusToFahrenheit(self, degrees):
        return degrees * 9.0 / 5.0 + 32.0

class MorseCodeConversion(Conversion):
    def __init__(self, components):
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
                         'H', 'I', 'J', 'K', 'L', 'M', 'N',
                         'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                         'V', 'W', 'X', 'Y', 'Z', '0', '1',
                         '2', '3', '4', '5', '6', '7', '8',
                         '9']
        self.morseAlphabet = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.',
                              '....', '..', '.---', '-.-', '.-..', '--', '-.',
                              '---', '.--.', '--.-', '.-.', '...', '-', '..-',
                              '...-', '.--', '-..-', '-.--', '--..',
                              '-----', '.----', '..---', '...--', '....-', '.....',
                              '-....', '--...', '---..', '----.']
        
        components.labelUp.text = 'English'
        components.btnConvertUp.label = 'Morse code to English'
        components.btnConvertDown.label = 'English to Morse code'
        components.labelDown.text = 'Morse code'

    def toDown(self, txt):
        return self.convertToMorse(txt)

    def toUp(self, txt):
        return self.convertFromMorse(txt)

    def convertToMorse(self, txt):
        converted = ''
        for c in txt[:]:
            ordC = c.upper()
            if c == ' ':
                # three spaces between words
                # when you include the space after each character
                converted = converted + '  '
            else:
                try:
                    converted += self.morseAlphabet[self.alphabet.index(ordC)] + ' '
                except ValueError:
                    return converted + "\n\ncharacter out of bounds, unable to complete conversion"
        return converted[:-1]

    def convertFromMorse(self, txt):
        converted = ''
        words = txt.split('  ')
        for w in words:
            letters = w.split(' ')
            for c in letters:
                if c == '':
                    continue
                try:
                    ordC = self.alphabet[self.morseAlphabet.index(c)]
                except ValueError:
                    return converted + "\n\nmorse out of bounds error, unable to complete conversion"
                converted += ordC
            converted += ' '
        return converted

class CurrencyConversion(Conversion):
    def convert(self, fromCur, toCur, txt):
        import SOAP
        server = SOAP.SOAPProxy('http://services.xmethods.net/soap', \
                        namespace='urn:xmethods-CurrencyExchange')
        try:
            dummy = float(txt)
        except ValueError:
            return "Cannot convert anything but numbers"
        try:
            rate = server.getRate(fromCur, toCur)
        except ValueError:
            return "Error getting exchange rate"
        return str(float(txt) * rate)

class CurrencyConversionUKUS(CurrencyConversion):
    def __init__(self, components):
        components.labelUp.text = 'UK Pounds'
        components.btnConvertUp.label = 'US Dollars to UK Pounds'
        components.btnConvertDown.label = 'UK Pounds to US Dollars'
        components.labelDown.text = 'US Dollars'

    def toDown(self, txt):
        return self.convertToUS(txt)

    def toUp(self, txt):
        return self.convertToUK(txt)

    def convertToUS(self, txt):
        return self.convert('UK', 'US', txt)

    def convertToUK(self, txt):
        return self.convert('US', 'UK', txt)

class CurrencyConversionAUSUS(CurrencyConversion):
    def __init__(self, components):
        components.labelUp.text = 'Aussie Dollars'
        components.btnConvertUp.label = 'US Dollars to Aussie Dollars'
        components.btnConvertDown.label = 'Aussie Dollars to US Dollars'
        components.labelDown.text = 'US Dollars'

    def toDown(self, txt):
        return self.convertToUS(txt)

    def toUp(self, txt):
        return self.convertToAus(txt)

    def convertToUS(self, txt):
        return self.convert('Australia', 'US', txt)

    def convertToAus(self, txt):
        return self.convert('US', 'Australia', txt)


class Conversions(model.Background):

    def on_initialize(self, event):
        # only enable currency conversion option if the SOAP module is installed
        if not SOAP_AVAILABLE:
            self.menuBar.setChecked('menuConvertCurrencyUKUS', False) 
            self.menuBar.setEnabled('menuConvertCurrencyUKUS', False)
            self.menuBar.setChecked('menuConvertCurrencyAUSUS', False) 
            self.menuBar.setEnabled('menuConvertCurrencyAUSUS', False)
        #self.conversion = TemperatureConversion(self.components)
        self.on_menuConvertTemperature_select(None)

    def on_btnConvertDown_mouseClick(self, event):
        self.components.field2.text = self.conversion.toDown(self.components.field1.text)

    def on_btnConvertUp_mouseClick(self, event):
        self.components.field1.text = self.conversion.toUp(self.components.field2.text)

    def uncheckAllMenuItems(self):
        self.menuBar.setChecked('menuConvertMorseCode', False)
        self.menuBar.setChecked('menuConvertTemperature', False)
        self.menuBar.setChecked('menuConvertCurrencyUKUS', False)
        self.menuBar.setChecked('menuConvertCurrencyAUSUS', False)
        
    def on_menuConvertMorseCode_select(self, event):
        self.conversion = MorseCodeConversion(self.components)
        self.uncheckAllMenuItems()
        self.menuBar.setChecked('menuConvertMorseCode')

    def on_menuConvertTemperature_select(self, event):
        self.conversion = TemperatureConversion(self.components)
        self.uncheckAllMenuItems()
        self.menuBar.setChecked('menuConvertTemperature')

    def on_menuConvertCurrencyUKUS_select(self, event):
        self.conversion = CurrencyConversionUKUS(self.components)
        self.uncheckAllMenuItems()
        self.menuBar.setChecked('menuConvertCurrencyUKUS')

    def on_menuConvertCurrencyAUSUS_select(self, event):
        self.conversion = CurrencyConversionAUSUS(self.components)
        self.uncheckAllMenuItems()
        self.menuBar.setChecked('menuConvertCurrencyAUSUS')


if __name__ == '__main__':
    app = model.Application(Conversions)
    app.MainLoop()
