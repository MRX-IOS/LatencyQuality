#!/usr/bin/python3
import os
import socket
import json
import smtplib
import pandas as pd
import numpy as np
from datetime import date
from requests import get
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from datetime import date

# dd/mm/YY
fecha = date.today().strftime("%d-%m-%Y")
print (fecha)

# rango del tiempo de ping en Espana:
# Fibra: de 4 - 20 ms
# ADSL:  de 55 - 60 ms
# timeout a 60 ms, deberia valer, mas de esto es problema de red o de nodo caido

# # # V A R I A B L E S  G L O B A L E S # # #
maxPingTimeout = str(0.5) #Tiemeout in seconds 
cleanFile = './clean/dns-clean'
hostsFile = './inFiles/TotalWebs.txt'
pingBlockFile = './inFiles/PingBlock.txt'
#hostsFile = './inFiles/hostsList.txt'

class bcolors:
	OK = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'

# # # F U N C I O N E S # # #
def limpiarCacheDNS():
	print ('\nLimpiando la cache de DNS...\n')
	# os.system('sudo /etc/init.d/dns-clean start') #Limpiamos la cache de resolucion DNS
	os.system("sudo " + cleanFile) #Limpiamos la cache de resolucion DNS

def myPublicIp():
	ip = get('https://api.ipify.org').text
	print("\n\n\t\tLa IP Publica es: " + str(ip) + "\n\n")

def get_lista(path):
	# Convertimos un archivo en una lista, cuyos elementos son las lineas, se quitan tambien los saltos de linea
	lista = []
	with open(path, 'r') as file:
		lista = [str(line.rstrip('\n')) for line in file.readlines()]
	return lista

def ordenarLista(lista):
	# ordena una lista numericamente y alfabeticamente
	return sorted(lista)


def maxTime(tabla):
	mayor = 0.0
	for i in tabla:
		print(int(tabla[i][4]))
		#if(int[i][4] > mayor):
		#	mayor = tabla[i][4]
		#	print(tabla[i][4])
		#	print(mayor)
		#else:
		#	print("No es mayor")

def busqueda_binaria(host, lista):
	# encuentra el elemento host en una lista
	# la lista ha de estar ordenada alfabeticamente para el uso de esta funcion, es importante
	lista_ordenada = ordenarLista(lista)
	izquierda, derecha = 0, len(lista) - 1
	while izquierda <= derecha:
		indiceDelElementoDelMedio = (izquierda + derecha) // 2
		elementoDelMedio = lista_ordenada[indiceDelElementoDelMedio]
		if str(elementoDelMedio) == str(host):
			return True
		if host < elementoDelMedio:
			derecha = indiceDelElementoDelMedio - 1
		else:
			izquierda = indiceDelElementoDelMedio + 1

	# Si salimos del ciclo significa que no existe el valor
	return False

def exportarResultados(tabla):
	# exporta la tabla resultante a csv
	final_file_csv = "./exports/resultados_" + str(fecha) + ".csv"
	final_file_json = "./exports/resultados_" + str(fecha) + ".json"

	df = pd.DataFrame(tabla, columns=['host', 'public_ip', 'status', 'attempts', 'latency (ms)', 'date', 'timestamp'])
	# print("\n")
	# print(df)
	# print("\n")

	df.to_json(final_file_json, orient="split", index=False)
	df.to_csv(final_file_csv, index=False, encoding='utf-8', sep=';', columns=['host', 'public_ip', 'status', 'attempts', 'latency (ms)', 'date', 'timestamp'], na_rep='Unknow')
	
	print("\n[" + bcolors.OK + bcolors.BOLD + "INFO" + bcolors.ENDC + "] Los resultados se han guardado correctamente en: \n\t" + final_file_csv + "\n\t" + final_file_json)
	print("\n")

def envioCorreo(errors, total_hosts):
	# envia un correo con el archivo y resultados finales
	# H:M:S
	# traza = datetime.now()
	hora = datetime.now().strftime("%H:%M:%S")

	porcentaje_error = float(errors)/float(total_hosts)
	print("\nPorcentaje de ERROR: " + str(porcentaje_error * 100) + "%")

	# Iniciamos los parámetros del script
	remitente = 'raspberry.tfg.etsisi@gmail.com'
	destinatarios = ['raspberry.tfg.etsisi@gmail.com', 'rodrigo.santaana.reina@alumnos.upm.es']
	asunto1 = "[RPI] [S0] POSIBLE CAIDA DE NODO " + str(fecha) + " " + str(hora)
	asunto2 = "[RPI] [S0] Calidad de conexión " + str(fecha) + " " + str(hora)
	cuerpo1 = "Desde Sonda: 0\n¿Caída de Nodo?\n\nPrueba de calidad de conexión mediante una raspberry pi 4 model B.\nSe envian los resultados obtenidos con fecha: " + str(fecha) + " y hora: " + str(hora) + "\n\n"
	cuerpo2 = "Desde Sonda: 0\n\nPrueba de calidad de conexión mediante una raspberry pi 4 model B.\nSe envian los resultados obtenidos con fecha: " + str(fecha) + " y hora: " + str(hora) + "\n\n"
	ruta_adjunto = "./exports/resultados_" + str(fecha) + ".csv"
	nombre_adjunto = "resultados_" + str(fecha) + ".csv"
	aplicationPassword = 'hjzoicvkxjilrsbj'

	# Creamos el objeto mensaje
	mensaje = MIMEMultipart()
 
	# Establecemos los atributos del mensaje
	mensaje['From'] = remitente
	mensaje['To'] = ", ".join(destinatarios)
 
	# Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
	if porcentaje_error > 0.05: # si falla un 5 % o mas de los pings, es decir si hay menos que el 95 % de pings exitosos:
		if porcentaje_error > 0.6: # si fallan mas del 60%
			print("\nSE ENVIA CORREO POSIBLE CAIDA DE NODO\n") # Se ha caido el nodo entero
			mensaje['Subject'] = asunto1
			mensaje.attach(MIMEText(cuerpo1, 'plain'))
		else:
			print("\nSE ENVIA EL CORREO\n") # Se envia para revision
			mensaje['Subject'] = asunto2
			mensaje.attach(MIMEText(cuerpo2, 'plain'))
 
		# Abrimos el archivo que vamos a adjuntar
		archivo_adjunto = open(ruta_adjunto, 'rb')
 
		# Creamos un objeto MIME base
		adjunto_MIME = MIMEBase('application', 'octet-stream')
		# Y le cargamos el archivo adjunto
		adjunto_MIME.set_payload((archivo_adjunto).read())
		# Codificamos el objeto en BASE64
		encoders.encode_base64(adjunto_MIME)
		# Agregamos una cabecera al objeto
		adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
		# Y finalmente lo agregamos al mensaje
		mensaje.attach(adjunto_MIME)
 
		# Creamos la conexión con el servidor
		sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
 
		# Ciframos la conexión
		sesion_smtp.starttls()

		# Iniciamos sesión en el servidor
		sesion_smtp.login('raspberry.tfg.etsisi@gmail.com', aplicationPassword)
		# https://support.google.com/accounts/answer/185833
	
		# Convertimos el objeto mensaje a texto
		texto = mensaje.as_string()

		# Enviamos el mensaje
		sesion_smtp.sendmail(remitente, destinatarios, texto)

		# Cerramos la conexión
		sesion_smtp.quit()
	else:
		print("\nNO SE ENVIA EL CORREO\n") # Todo OK


def resolucionDNSAndPing(host, listaNegra):
	tablaResultado = []
	host = host.rstrip()
	host = host.replace("\n", "")
	print("[>] DNS RESOLUTION FOR: " + host)
	
	try:
		host_resolved = socket.gethostbyname_ex(host)
		print("\t[" + bcolors.OK + bcolors.BOLD + "OK" + bcolors.ENDC+ "] DNS " + bcolors.OK + "SUCCESS\n" + bcolors.ENDC)
		print("[>] THROWING PING FOR: " + host)
		pingResult = lanzarPing(host_resolved[0], listaNegra)

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

def lanzarPing(host, listaNegra):
	# Lanza un ping, y devuelve un array indicando, host, estado de finalizacion, intento en el que se consigue exito y tiempo
	resultado = []
	estado = "N/A"
	intentos = 0
	time = 0.0
	publicIp = "N/A"

	exito = False

	if busqueda_binaria(host, listaNegra) == True:
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
			
	hora = datetime.now().strftime("%H:%M:%S")
	resultado = [host, publicIp, estado, intentos, time, fecha, hora]
	return resultado

def main():
	tabla = []
	pingFailures = 0
	hostsNA = 0
	hosts = get_lista(hostsFile)
	listaNegra = get_lista(pingBlockFile)
	total_hosts = len(hosts)
	limpiarCacheDNS()
	myPublicIp()

	for host in hosts:
		print(host + "\n")
		resultado = resolucionDNSAndPing(host, listaNegra)
		#print(resultado)

		tabla.append(resultado)
		print("\n\tHost: " + str(resultado[0]) + "\n\tIp Publica: " + str(resultado[1]) + "\n\tEstado: " + str(resultado[2]) + "\n\tIntentos: " + str(resultado[3]) + "/3\n\tLatencia: " + str(resultado[4]) + " ms" + "\n\tFecha: " + str(resultado[5]) + "\n\tHora: " + str(resultado[6] + "\n"))
		
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
	#print(tabla)
	exportarResultados(tabla)
	#maxTime(tabla)
	envioCorreo(pingFailures, pingeds)

if __name__ == "__main__":
	main()
