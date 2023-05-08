#!/usr/bin/python3

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
	print("Location: " + data[4])
	print("Organization: " + data[5])
	print("Postal: " + str(data[6]))
	print("Timezone: " + data[7])

	with ThreadPoolExecutor(max_workers=6) as executor:	
		futures = [executor.submit(getData_Tread, host, listaNegra) for host in hosts]
		for future in as_completed(futures):
			resultado = future.result()
			tabla.append(resultado)

	# resultado = [host, publicIp, estado, intentos, city, region, country, loc, org, postal, timezone, time, fecha]

	for i in tabla:
		print(i) 
		if i[2] != "OK":
			if i[2] == "NA":
				hostsNA += 1
			else:
				pingFailures += 1
		
	pingeds = total_hosts - hostsNA
	export.csv(tabla)
	print("\n")
	send.email(pingFailures, pingeds)
	sendElastic.run()

if __name__ == "__main__":
    main()
