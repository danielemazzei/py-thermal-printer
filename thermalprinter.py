"""
.. module: ThermalPrinter 

Viper Thermal Printer

This module is contains class definitions for the "micro panel thermal printer" sold in shops like Adafruit and Sparkfun (e.g. http://www.adafruit.com/products/597). 
        
The code is an adaptation for Viper www.viperize.it of the Lauri Kainulainen work https://github.com/luopio/py-thermal-printer and based on the porting of Ladyada's Arduino library.    

"""

import streams

class ThermalPrinter():
    """
==================
ThermalPrinter class
==================

.. class:: ThermalPrinter(serialport, baudrate=19200, heatTime=80, heatInterval=2, heatingDots=7)

    This is the class for creating a thermal printer instance. 
    * serialport: The name of the serial port where the printer is connected: SERIAL0, SERIAL1, SERIAL2...
    * baudrate: The serial port speed. default is 19200 as set in most of the printer by default. To know the printer configured baudrate press for more than 5 second the printer button, the printed test ticket will report the baudrate.

    Other parameters are "max printing dots", "heating time"and "heating interval"
    printing dots = 0-255 Max printing dots, Unit (8dots), Default: 7 (64 dots); heating time = 3-255 Heating time, Unit (10us), Default: 80 (800us); heating interval = 0-255 Heating interval, Unit (10us), Default: 2 (20us).
    
    The more max heating dots, the more peak current will cost when printing, the faster printing speed. The max heating dots is 8*(n1+1). The more heating time, the more density,
    but the slower printing speed. If heating time is too short, blank page may occur. The more heating interval, the more clear, but the slower printing speed. 

    """   
    

    TIMEOUT = 3

    # pixels with more color value (average for multiple channels) are counted as white
    # tweak this if your images appear too black or too white
    black_threshold = 48
    # pixels with less alpha than this are counted as white
    alpha_threshold = 127

    printer = None

    


    _ESC = chr(27)

    # These values (including printDensity and printBreaktime) are taken from 
    # lazyatom's Adafruit-Thermal-Library branch and seem to work nicely with bitmap 
    # images. Changes here can cause symptoms like images printing out as random text. 
    # Play freely, but remember the working values.
    # https://github.com/adafruit/Adafruit-Thermal-Printer-Library/blob/0cc508a9566240e5e5bac0fa28714722875cae69/Thermal.cpp
    
    # Set 
    
    def __init__(self, serialport, baudrate=19200, heatTime=80, heatInterval=2, heatingDots=7):
        self.printer = streams.serial(serialport,baudrate)        
        self.write(self._ESC) # ESC - command
        self.write(chr(64)) # @   - initialize
        self.write(self._ESC) # ESC - command
        self.write(chr(55)) # 7   - print settings
        self.write(chr(heatingDots))  # Heating dots (20=balance of darkness vs no jams) default = 20
        self.write(chr(heatTime)) # heatTime Library default = 255 (max)
        self.write(chr(heatInterval)) # Heat interval (500 uS = slower, but darker) default = 250

        # Description of print density from page 23 of the manual:
        # DC2 # n Set printing density
        # Decimal: 18 35 n
        # D4..D0 of n is used to set the printing density. Density is 50% + 5% * n(D4-D0) printing density.
        # D7..D5 of n is used to set the printing break time. Break time is n(D7-D5)*250us.
        printDensity = 15 # 120% (? can go higher, text is darker but fuzzy)
        printBreakTime = 15 # 500 uS
        self.write(chr(18))
        self.write(chr(35))
        self.write(chr((printDensity << 4) | printBreakTime))

    def write(self,msg):        
        for c in msg:
            self.printer.write(c)
            sleep(2)
    
    def reset(self):
        self.write(self._ESC)
        self.write(chr(64))

    def linefeed(self):
        self.write(chr(10))

    def justify(self, align="L"):
        pos = 0
        if align == "L" or align == "l":
            pos = 0
        elif align == "C" or align == "c":
            pos = 1
        elif align == "R" or align == "r":
            pos = 2
        self.write(self._ESC)
        self.write(chr(97))
        self.write(chr(pos))

    def bold_off(self):
        self.write(self._ESC)
        self.write(chr(69))
        self.write(chr(0))

    def bold_on(self):
        self.write(self._ESC)
        self.write(chr(69))
        self.write(chr(1))

    def font_b_off(self):
        self.write(self._ESC)
        self.write(chr(33))
        self.write(chr(0))

    def font_b_on(self):
        self.write(self._ESC)
        self.write(chr(33))
        self.write(chr(1))

    def underline_off(self):
        self.write(self._ESC)
        self.write(chr(45))
        self.write(chr(0))

    def underline_on(self):
        self.write(self._ESC)
        self.write(chr(45))
        self.write(chr(1))

    def inverse_off(self):
        self.write(chr(29))
        self.write(chr(66))
        self.write(chr(0))

    def inverse_on(self):
        self.write(chr(29))
        self.write(chr(66))
        self.write(chr(1))

    def upsidedown_off(self):
        self.write(self._ESC)
        self.write(chr(123))
        self.write(chr(0))

    def upsidedown_on(self):
        self.write(self._ESC)
        self.write(chr(123))
        self.write(chr(1))
        
    def barcode_chr(self, msg):
        self.write(chr(29)) # Leave
        self.write(chr(72)) # Leave
        self.write(msg)     # Print barcode # 1:Abovebarcode 2:Below 3:Both 0:Not printed
        
    def barcode_height(self, msg):
        self.write(chr(29))  # Leave
        self.write(chr(104)) # Leave
        self.write(msg)      # Value 1-255 Default 50
        
    def barcode_height(self):
        self.write(chr(29))  # Leave
        self.write(chr(119)) # Leave
        self.write(chr(2))   # Value 2,3 Default 2
        
    def barcode(self, msg,print_numbers=2):
        """
.. method:: barcode(msg,print_numbers=2)

    Prints a barcode. 
    Print barcode number option: 1:Abovebarcode 2:Below 3:Both 0:Not printed
    Please read http://www.adafruit.com/datasheets/A2-user%20manual.pdf for information on how to use barcodes. 
    This function need a 12 digits code as input
    """
        # CODE SYSTEM, NUMBER OF CHARACTERS        
        # 65=UPC-A    11,12    #71=CODEBAR    >1
        # 66=UPC-E    11,12    #72=CODE93    >1
        # 67=EAN13    12,13    #73=CODE128    >1
        # 68=EAN8    7,8    #74=CODE11    >1
        # 69=CODE39    >1    #75=MSI        >1
        # 70=I25        >1 EVEN NUMBER 
        self.barcode_chr(print_numbers)          
        self.write(chr(29))  # LEAVE
        self.write(chr(107)) # LEAVE
        self.write(chr(65))  # USE ABOVE CHART
        self.write(chr(12))  # USE CHART NUMBER OF CHAR 
        self.write(msg)
        
        
    
    def print_text(self, msg, justification="l", style="n", chars_per_line=None):
        """ 
        .. method:: print_text(msg, allignement=l, style=n, chars_per_line=None)

        Print some text defined by msg. If chars_per_line is defined, inserts newlines after the given amount. 
        Use normal '\n' line breaks for empty lines.

        style (n=normal, b=bold, u=underline, i=inverse, f=font B)
        justification (l=left, c=centre, r=right) 

        print_text also supports auto line ending specifying chars_per_line 
        """ 
        stylesDictionary={
    "b":(self.bold_on, self.bold_off),
    "u":(self.underline_on,self.underline_off),
    "i":(self.inverse_on,self.inverse_off),
    "f":(self.font_b_on,self.font_b_off),
    "r":(self.inverse_on,self.inverse_off)}

        self.justify(justification)

        for v in stylesDictionary:
            if style==v:
                
                stylesDictionary[v][0]()
                break

        if not chars_per_line:
            self.write(msg)
        else:
            p=0
            le=len(msg)
            for i in range(chars_per_line+1,le,chars_per_line+1):
                self.write(msg[p:i])
                self.write("\n")
                p=i
            if p<le:
                self.write(msg[p:])
        stylesDictionary[v][1]()        
            
