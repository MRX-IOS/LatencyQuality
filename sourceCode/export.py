#!/usr/bin/python3

import json
import pandas as pd
from configuration import path, fecha
import bcolors

final_file_csv = path + "exports/resultados_" + str(fecha) + ".csv"
final_file_json = path + "exports/resultados_" + str(fecha) + ".json"

def csv(tabla):
	"""
	Exporta la tabla resultante a csv
	
	Parameters
	----------
	tabla : list
		resultado = [host, publicIp, estado, intentos, city, region, country, loc, org, postal, timezone, time, fecha]
	"""
	# exporta la tabla resultante a csv
	df = pd.DataFrame(tabla, columns=['host', 'public_ip', 'status', 'attempts', 'city', 'region', 'country', 'localization', 'organization', 'postal', 'timezone', 'latency (ms)', 'date'])
	df.to_csv(final_file_csv, index=False, encoding='utf-8', sep=';', columns=['host', 'public_ip', 'status', 'attempts', 'city', 'region', 'country', 'localization', 'organization', 'postal', 'timezone', 'latency (ms)', 'date'], na_rep='Unknow')
	print("\n[" + bcolors.OK + bcolors.BOLD + "INFO" + bcolors.ENDC + "] Los resultados se han guardado correctamente en: \n\t" + final_file_csv)

def json(tabla):
	"""
	Exporta la tabla resultante a json
	
	Parameters
	----------
	tabla : list
		tabla = [host, publicIp, estado, intentos, city, region, country, loc, org, postal, timezone, time, fecha]
	"""

	# exporta la tabla resultante a json
	df = pd.DataFrame(tabla, columns=['host', 'public_ip', 'status', 'attempts', 'city', 'region', 'country', 'localization', 'organization', 'postal', 'timezone', 'latency (ms)', 'date'])
	df.to_json(final_file_json, orient="split", index=False)
	print("\n[" + bcolors.OK + bcolors.BOLD + "INFO" + bcolors.ENDC + "] Los resultados se han guardado correctamente en: \n\t" + final_file_json)
