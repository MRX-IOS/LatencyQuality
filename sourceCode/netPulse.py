#!/usr/bin/python3 -B

import dns
import send
import sendElastic
import export
import bcolors
import lists as li
from ipinfo import myPublicIP, myData

from configuration import *

def main():
	tabla = []
	pingFailures = 0
	hostsNA = 0

	hosts = li.getList(hostsFile)
	listaNegra = li.getList(pingBlockFile)
	total_hosts = len(hosts)

	dns.cleanDNSCache()

	data = myData()
	print("Public IP: " + data[0])
	print("City: " + data[1])
	print("Region: " + data[2])
	print("Country: " + data[3])
	print("Source Location: " + data[4])
	print("ASN: " + data[5])
	print("ISP: " + data[6])
	print("Postal: " + data[7])
	print("Timezone: " + data[8])

	for host in hosts:
		print(host + "\n")
		resultado = dns.getData(host, listaNegra)

		# data[4] = source location
		# insertar source location en el resultado, en la posicion 7 del array (8 posiciones por el "0")
		resultado.insert(7, data[4])

		fecha = resultado[14].split(" ")
		tabla.append(resultado)

		# tabla = [host, publicIp, estado, intentos, city, region, country, loc, org, postal, timezone, time, fecha]
		print("\n\tHost: " + str(resultado[0]) + 
			"\n\tIp Publica: " + str(resultado[1]) + 
			"\n\tEstado: " + str(resultado[2]) + 
			"\n\tIntentos: " + str(resultado[3]) + "/3" + 
			"\n\tCiudad: " + str(resultado[4]) +
			"\n\tRegion: " + str(resultado[5]) +
			"\n\tPais: " + str(resultado[6]) +
			"\n\tSource Point: " + str(resultado[7]) +
			"\n\tDestination: " + str(resultado[8]) +
			"\n\tASN: " + str(resultado[9]) +
			"\n\tISP: " + str(resultado[10]) +
			"\n\tCodigo Postal: " + str(resultado[11]) +
			"\n\tZona Horaria: " + str(resultado[12]) +
			"\n\tLatencia: " + str(resultado[13]) + " ms" + 
			"\n\tFecha: " + str(fecha[0]) + 
			"\n\tHora: " + str(fecha[1]) + "\n"
			"\n\tFecha completa: " + str(resultado[14]) + "\n")
		
		# Aqui se cuentan los pingFailures, ademas de trazas de estado de ejecucion
		# Si solo se desea los pingFailures if resultado != "OK": pingfailures + 1
		if resultado[2] != "OK":
			if resultado[2] != "KO":
				print("\t[" + bcolors.FAIL + "FAIL" + bcolors.ENDC + "] NO PING, " + bcolors.FAIL + "BANNED " + bcolors.ENDC + "HOST\n")
				hostsNA = hostsNA + 1
			else:
				print("\t[" + bcolors.FAIL + "FAIL" + bcolors.ENDC +"] PING " + bcolors.FAIL + "ERROR\n" + bcolors.ENDC)
				pingFailures = pingFailures + 1
		else:
			print("\t[" + bcolors.OK + "OK" + bcolors.ENDC + "] PING " + bcolors.OK + "SUCCESS\n" + bcolors.ENDC)

		print("==============================================")
		
	# pingeds es los que han dado OK o KO
	pingeds = total_hosts - hostsNA
	
	export.csv(tabla)
	export.json(tabla)
	print("\n")
	send.email(pingFailures, pingeds)
	sendElastic.run()

if __name__ == "__main__":
    main()
