#!/usr/bin/python3

import dns
import send
import sendElastic
import export
import bcolors
import lists as li

from configuration import *

def main():
	tabla = []
	pingFailures = 0
	hostsNA = 0

	hosts = li.getList(hostsFile)
	listaNegra = li.getList(pingBlockFile)
	total_hosts = len(hosts)

	dns.cleanDNSCache()
	# myPublicIp()

	for host in hosts:
		print(host + "\n")
		resultado = dns.getData(host, listaNegra)
		#print(resultado)

		fecha = resultado[12].split(" ")
		tabla.append(resultado)
		# tabla = [host, publicIp, estado, intentos, city, region, country, loc, org, postal, timezone, time, fecha]
		print("\n\tHost: " + str(resultado[0]) + 
			"\n\tIp Publica: " + str(resultado[1]) + 
			"\n\tEstado: " + str(resultado[2]) + 
			"\n\tIntentos: " + str(resultado[3]) + "/3" + 
			"\n\tCiudad: " + str(resultado[4]) +
			"\n\tRegion: " + str(resultado[5]) +
			"\n\tPais: " + str(resultado[6]) +
			"\n\tLocalizacion: " + str(resultado[7]) +
			"\n\tOrganizacion: " + str(resultado[8]) +
			"\n\tCodigo Postal: " + str(resultado[9]) +
			"\n\tZona Horaria: " + str(resultado[10]) +
			"\n\tLatencia: " + str(resultado[11]) + " ms" + 
			"\n\tFecha: " + str(fecha[0]) + 
			"\n\tHora: " + str(fecha[1]) + "\n"
			"\n\tFecha completa: " + str(resultado[12]) + "\n")
		
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
