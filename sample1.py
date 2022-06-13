import pyvisa as visa
 
rm = visa.ResourceManager()
inst = rm.list_resources()
usb = list(filter(lambda x: 'USB' in x, inst))
scope = rm.open_resource(usb[0])
print(scope.query("*IDN?"))
