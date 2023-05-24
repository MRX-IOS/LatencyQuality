#!/usr/bin/python3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from datetime import date
from configuration import projectPath
from configuration import fecha

def email(errors, total_hosts):
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
	ruta_adjunto = projectPath + "exports/resultados_" + str(fecha) + ".csv"
	# print(ruta_adjunto)
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

