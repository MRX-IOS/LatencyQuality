#!/usr/bin/python3
import sendElastic
import datetime 
from datetime import datetime


hora = datetime.now().strftime("%H:%M:%S")
fecha = datetime.now().strftime("%d/%m/%Y")

fecha = fecha + "@" + hora
print(fecha)
