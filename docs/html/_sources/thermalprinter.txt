.. module:: ThermalPrinter 

***************
Thermal Printer
***************

This module contains class definitions for the "micro panel thermal printer" sold in shops like Adafruit and Sparkfun (e.g. http://www.adafruit.com/products/597). 
        
The code is an adaptation for Viper of the Lauri Kainulainen work (https://github.com/luopio/py-thermal-printer) and it is based on the porting of the Adafruit library made by Ladyada for Arduino.

    
    ====================
    ThermalPrinter class
    ====================

.. class:: ThermalPrinter(serialport, baudrate=19200, heatTime=80, heatInterval=2, heatingDots=7)

    This is the class for creating a thermal printer instance. 

    * serialport: it is the serial port the printer is connected to: SERIAL0, SERIAL1, SERIAL2...
    * baudrate: it is the serial port speed. Default is 19200 as set in most of the printers by default. To know the printer baudrate press for more than 5 second the printer button, the printed test ticket will report the baudrate.
    * heatTime: heating time ranges between 3 and 255, unit corresponds to 10us, Default is set to 80 (800us). Increasing the heating time will increase the printing density but printing speed will be reduced. If heating time is too short, blank page may occur.
    * heatInterval: heating interval ranges between 0 and 255, unit corresponds to 10us, Default is set to 2 (20us). Increasing the heating interval clearer prints are obtained but the printing speed is reduced.
    * heatingDots: max printing dots range between 0 and 255 Max printing dots. Each unit corresponds to 8 dots. Default is set to 7 (64 dots). Increasing the value of max heating dots will increase the peak of current when printing and consequently the printing speed.

    
.. method:: print_text(msg, justification="l", style="n", chars_per_line=None)
        
        Print text passed as string

            * msg: it is the string to be printed. Use "\\n" line breaks to write empty lines.
            * justification: it is the text alignment to be passed as string ("l"=left, "c"=centre, "r"=right) 
            * style: it is the text style to be passed as string ("n"=normal, "b"=bold, "u"=underline, "i"=inverse, "f"=font B)
            * chars_per_line: if chars_per_line is defined the printer inserts a newline character after the given amount of printed chars.        
    
        
.. method:: barcode(msg,code="UPCA",digits=11,print_numbers=2)
        
        Prints a barcode taking as input a set of digits as string.
        
            * msg: it is the string containing the digits required for the generation of the barcode
            * code: it is the barcode symbology. It can be selected according to the following table, default is UPCA.
            * digits: each symbology has a specific number of allowed digits that have also to be passed as parameter according to the following table.
            * print_numbers: barcode numbers position option: 1:Abovebarcode 2:Below 3:Both 0:Not printed

            ==============  ====================================
            CODE SYSTEM     NUMBER OF CHARACTERS REQUIRED       
            ==============  ====================================    
            UPCA            11,12    
            UPCE            11,12           (Not yet supported)  
            EAN13           12,13   
            EAN8            7,8    
            CODE39          >1    
            I25             >1 EVEN NUMBER  (not yet supported)
            CODEBAR         >1
            CODE93          >1
            CODE128         >1
            CODE11          >1
            MSI             >1    
            ==============  ====================================    
                     
            More info on barcode symbology https://en.wikipedia.org/wiki/Barcode#Linear_barcodes
            
        
