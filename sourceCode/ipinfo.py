#!/usr/bin/python3

import os
import json	
import requests

"""

	https://ipinfo.io/account/home
	Esta API es gratuita para 50.000 peticiones al mes.
	Para más peticiones, se requiere una suscripción.

"""

URL = 'https://ipinfo.io/'
token = 'c94afc1c907984'

def myPublicIP():
	# curl
	ip = os.popen("curl -s https://ipinfo.io/ip").read()
	return ip

def myData():
	ip = myPublicIP()
	# añadir ip a la lista
	data = []
	data.append(ip)
	# añadir info a la lista
	data.extend(getInfo(ip))

	return data

def getInfo(host):
	"""

		Parameters
		----------
		host : str
		
		Returns
		-------
		info : list
		info = [city, region, country, loc, org, postal, timezone]

	"""

	"""
	CURL EXAMPLE

		{
		  "ip": "138.100.147.163",
		  "city": "Madrid",
		  "region": "Madrid",
		  "country": "ES",
		  "loc": "40.4165,-3.7026",
		  "org": "AS766 Entidad Publica Empresarial Red.es",
		  "postal": "28001",
		  "timezone": "Europe/Madrid"
		}

	"""
	# inializate variables	
	city = ''
	region = ''
	country = ''
	loc = ''
	org = ''
	postal = 0
	timezone = ''
	
	# os.system("curl -s https://ipinfo.io/" + host + "/json?token=" + token)
	elements = os.popen("curl -s " + URL + host + "/json?token=" + token).read()
	# elements to dict
	elements = json.loads(elements)
	# if exist field
	if 'city' in elements:
		city = elements['city']
	if 'region' in elements:
		region = elements['region']
	if 'country' in elements:
		country = elements['country']
	if 'loc' in elements:
		loc = elements['loc']
	if 'org' in elements:
		org = elements['org']
	if 'postal' in elements:
		postal = int(elements['postal'])
	if 'timezone' in elements:
		timezone = elements['timezone']

	info = [city, region, country, loc, org, postal, timezone]
	return info

if __name__ == '__main__':
	print("MY PUBLIC IP:= ", myPublicIP())
	print("MY DATA:= ", myData())
	print(getInfo('92.189.190.237'))
	print(getInfo('39.156.66.10')) # baidu.com
