#!/usr/bin/python3

import os
import ping
import socket
import bcolors

from datetime import date
from datetime import datetime

from configuration import cleanFile
from configuration import pingBlockFile as listaNegra

# dd/mm/YY
fecha = date.today().strftime("%d-%m-%Y")

def cleanDNSCache():
	print ('\nLimpiando la cache de DNS...\n')
	os.system("sudo " + cleanFile) #Limpiamos la cache de resolucion DNS

def dnsLookUp(host):
	return socket.gethostbyname_ex(host)

def getData(host, listaNegra):
	tablaResultado = []
	host = host.rstrip()
	host = host.replace("\n", "")
	print("[>] DNS RESOLUTION FOR: " + host)
	
	try:
		host_resolved = dnsLookUp(host)
		print("\t[" + bcolors.OK + bcolors.BOLD + "OK" + bcolors.ENDC+ "] DNS " + bcolors.OK + "SUCCESS\n" + bcolors.ENDC)
		print("[>] THROWING PING FOR: " + host)
		pingResult = ping.run(host_resolved[0], listaNegra)

		# print(pingResult)
		# print("\n")
		# print(host_resolved)
		
		# tablaResultado.append(host_resolved)
		# tablaResultado.append(pingResult)

		# print(tablaResultado)
                # return host_resolved

		return pingResult

	except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout):
		# host_no_resolved = ["N/A", ["N/A"], ["N/A"]]

		hora = datetime.now().strftime("%H:%M:%S")
		pingNotPossible = [host, "N/A", "N/A", "0", "0.0", fecha, hora]

		print("\t[" + bcolors.FAIL + bcolors.BOLD + "FAIL" + bcolors.ENDC + "] DNS " + bcolors.FAIL + "ERROR" + bcolors.ENDC + "\n")

		#return host_no_resolved
		return pingNotPossible
		next

