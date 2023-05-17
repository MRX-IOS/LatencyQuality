#!/usr/bin/python3 -B

import dns
import send
import sendElastic
import export
import bcolors
import lists as li
from ipinfo import myPublicIP, myData
from concurrent.futures import ThreadPoolExecutor, as_completed

from configuration import *

def getData_Tread(host, listaNegra):
	print(host + "\n")
	resultado = dns.getData(host, listaNegra)
	print("==============================================")
	return resultado

def main():
	tabla = []
	hostsNA = 0
	numWorkers = 6
	pingFailures = 0

	hosts = li.getList(hostsFile)
	listaNegra = li.getList(pingBlockFile)
	total_hosts = len(hosts)

	dns.cleanDNSCache()

	data = myData()
	print("Public IP: " + data[0])
	print("City: " + data[1])
	print("Region: " + data[2])
	print("Country: " + data[3])
	print("Source_point: " + data[4])
	print("ASN: " + data[5])
	print("ISP: " + data[6])
	print("Postal: " + str(data[7]))
	print("Timezone: " + data[8])

	with ThreadPoolExecutor(max_workers=numWorkers) as executor:	
		futures = [executor.submit(getData_Tread, host, listaNegra) for host in hosts]
		for future in as_completed(futures):
			resultado = future.result()
			resultado.insert(7, data[4]) # insertar source location en el resultado, en la posicion 7 del array (8 posiciones por el "0")
			tabla.append(resultado)

	# resultado = [host, publicIp, estado, intentos, city, region, country, src, dst, asn, isp, postal, timezone, time, fecha]

	for i in tabla:
		# print(i) 
		if i[2] != "OK":
			if i[2] != "KO":
				hostsNA += 1
			else:
				pingFailures += 1
		
	pingeds = total_hosts - hostsNA
	
	print("==============================================")
	print("NA HOSTS:\t" + str(hostsNA))
	print("PINGEDS:\t" + str(pingeds))
	print("PING FAILURES:\t" + str(pingFailures))
	print("PING SUCCESS:\t" + str(pingeds - pingFailures))

	export.csv(tabla)
	export.json(tabla)
	send.email(pingFailures, pingeds)
	sendElastic.run()

if __name__ == "__main__":
    main()
