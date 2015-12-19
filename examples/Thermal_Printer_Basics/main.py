################################################################################
# Thermal Printer Basics
#
# Created by VIPER Team 2015 CC
# Authors: D. Mazzei, G. Baldi,  
###############################################################################

import streams

from community.floyd.thermalprinter import thermalprinter

# create a printer passing the serial port name. Printer RX wire have to be connected 
# to the selected serial port TX pin. The default baudrate for the thermal printers is 19200
# In this case SERIAL1 is used. In Arduino the serial 1 TX pin is D18 while in the Nucleo is on the morphos connector (seventh from the top on the right series)
p = thermalprinter.ThermalPrinter(SERIAL1,19200)

# another serial port for printing to the console
s= streams.serial(SERIAL0)

def test(printer):  
    # print_text(msg,"a","s") takes as input a string containing the massage and two characters for the definition of the a:alignment and s:style    
    # first character denotes justification (l=left, c=centre, r=right)
    # second character denotes style (n=normal, b=bold, u=undfrom drivers.thermalprinter erline, i=inverse, f=font B)
    # normal style with left alignment is the default
    # \n is required for line termination
    
    p.print_text("Default\n")
    p.print_text("Left and Bold\n","l","b")
    p.print_text("Center and Underlined\n","c","u")
    p.print_text("Right and Inverted\n","r","i")
    p.print_text("Left and Font B\n\n","l","f")    

    # print_text also supports auto line ending giving as input chars_per_line as last parameter
    
    p.print_text("VIPER (Viper Is Python Embedded in Realtime) is an easy to use, professional and performant development suite for the cross-platform and high level design of interactive objects.\n""", chars_per_line=31)
i=1
string=""
while True:
    string=str(i)+" Print!\n"
    # In Viper the print function automatically selects the last opened stream. 
    # If s is not created as last stream, stream=s have to passed as parameter to the print, e.g. print("test",stream=s)
    print(string)
    
    #
    p.print_text(string)
    test(p)
    i+=1
    sleep(10000)