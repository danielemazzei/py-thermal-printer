################################################################################
# Thermal Printer Barcode
#
# Created by VIPER Team 2015 CC
# Authors: D. Mazzei, G. Baldi,  
###############################################################################

import streams

from drivers.thermalprinter import thermalprinter

# create a printer passing to the class the serial port name. Printer RX wire have to be connected 
# to the selected serial port TX pin. The default baudrate for the thermal printers is 19200
# In this case SERIAL1 is used. In Arduino the serial 1 TX pin is D18 while in the Nucleo is on the morphos connector (seventh from the top on the right series)
p = thermalprinter.ThermalPrinter(SERIAL1,19200)

# another serial port for printign on the console
s= streams.serial(SERIAL0)


# the code symbology and the message containing the digits to be printed as barcode have to be passes as strings while the number of digits as int.
# In this example the number of digits is passed as number withouth using len(message) in order to clearly specify the max number of allowd digits.
# However, this example is very verbose...
codes=("UPCA","EAN13","EAN8","CODE39","CODEBAR","CODE93","CODE128","CODE11","MSI")
digits=(12,13,8,5,5,5,5,5,5)
msgs=("123456789990","1234567899990","12345678","12345","12345","12345","12345","12345","12345")

while True:
    
    for i in range(len(codes)):   
        
        # prepare a string to be wrote as text before the barcode and also on the serial port connected to the Viper console 
        string="Printing:"+str(msgs[i])+" with code:"+str(codes[i])+"\n" 
        print(string)
        print("-"*20)
        
        # print the string as text on the printer
        p.print_text(string)
        
        # print the barcode taking as input the digits, the symbology and the number of digits contained in the message. 
        p.barcode(msgs[i],codes[i],digits[i])
        sleep(3000)
   