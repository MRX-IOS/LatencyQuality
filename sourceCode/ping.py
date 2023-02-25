#!/usr/bin/python3

import os
import lists as li
from configuration import maxPingTimeout

from datetime import datetime
from datetime import date

import bcolors


def run(host, listaNegra):
	# Lanza un ping, y devuelve un array indicando, host, estado de finalizacion, intento en el que se consigue exito y tiempo
	resultado = []
	estado = "N/A"
	intentos = 0
	time = 0.0
	publicIp = "N/A"

	exito = False

	if li.searchElement(host, listaNegra) == True:
		print("\t[" + str(intentos) + "] Estado del servicio:\t[" + bcolors.BOLD + bcolors.WARNING + "N/A" + bcolors.ENDC + "]")
		estado = "N/A"
	else:
		while exito == False and intentos < 3:
			# Se lanza solo un paquete, por mayor velocidad, si se aumentan los paquetes, hay que asegurarse de subir el maxPingTimeout
			respuesta = os.popen("timeout " + maxPingTimeout + " ping -c1 " + host).read()
			#respuesta = os.popen("ping -W1 -c1 " + host).read()
			intentos = intentos + 1

			# si existe tiempo de respuesta, se ha hecho el ping correctamente
			if 'time=' in respuesta and 'ms' in respuesta:
				time = respuesta.split('time=')[1].split(' ms')[0]
				print("\t[" + str(intentos) + "] Estado del servicio:\t[" + bcolors.BOLD + bcolors.OK + "OK" + bcolors.ENDC + "]")
				publicIp = str(respuesta.split('(')[1].split(')')[0])

				print("\tTiempo de respuesta: " + time + " ms")
				exito = True # Salir del bucle
			else:
				print("\t[" + str(intentos) + "] Estado del servicio:\t[" + bcolors.BOLD + bcolors.FAIL + "KO" + bcolors.ENDC + "]")

		if exito == True:
			estado = "OK"
		else:
			estado = "KO"

	# dd/mm/YY @ H:M:S
	fecha = date.today().strftime("%d-%m-%Y")
	hora = datetime.now().strftime("%H:%M:%S")
	fecha = fecha + " " + hora
	resultado = [host, publicIp, estado, intentos, time, fecha]
	return resultado
