#!/usr/bin/python3

import os
import ping
import socket
import bcolors

from datetime import date
from datetime import datetime

from configuration import cleanFile
from configuration import pingBlockFile as listaNegra


def cleanDNSCache():
	"""
	Funcion que limpia la cache de resolucion DNS
	"""

	print ('\nLimpiando la cache de DNS...\n')
	os.system("sudo " + cleanFile) #Limpiamos la cache de resolucion DNS

def dnsLookUp(host):
	"""
	Funcion que realiza la resolucion DNS de un host
	
	Parameters:
	-----------
	host: str
	
	Returns:
	--------
	host_resolved: list
	
	"""
	return socket.gethostbyname_ex(host)

def getData(host, listaNegra):
	"""
	Funcion que realiza la resolucion DNS de un host y lanza un ping
	
	Parameters:
	-----------
	host: str
	listaNegra: list
	
	Returns:
	--------
	pingResult: list
	
	"""
	"""
	  Ping result:
		resultado: list 
		resultado = [host, publicIp, estado, intentos, city, region, country, loc, org, postal, timezone, time, fecha]

	"""
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
		# dd/mm/YY
		fecha = date.today().strftime("%d-%m-%Y")
		hora = datetime.now().strftime("%H:%M:%S")
		fecha = fecha + " " + hora
		
		"""
		loc Geopoint	
		"""
		loc = "0.0,0.0"
		pingNotPossible = [host, "N/A", "N/A", "0", "N/A", "N/A", "N/A", loc, "N/A", 0, "N/A", 0.0, fecha]

		print("\t[" + bcolors.FAIL + bcolors.BOLD + "FAIL" + bcolors.ENDC + "] DNS " + bcolors.FAIL + "ERROR" + bcolors.ENDC + "\n")

		#return host_no_resolved
		return pingNotPossible
		next

def main():
	hosts = ["google.com", "youtube.com"]
	listaNegra = ["google.com", "gmail.com"]
	for host in hosts:
		results = getData(host, listaNegra)
		print(results)
	
if __name__ == "__main__":
	main()



