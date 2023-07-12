#!/usr/bin/python3

def getList(path):
	"""
	Funcion que devuelve una lista con los elementos de un archivo
	
	Parameters:
	-----------
	path: str
	
	Returns:
	--------
	lista: list
	
	"""
	# Convertimos un archivo en una lista, cuyos elementos son las lineas, se quitan tambien los saltos de linea
	lista = []
	with open(path, 'r') as file:
		lista = [str(line.rstrip('\n')) for line in file.readlines()]
	return lista

def shortList(lista):
	"""
	Funcion que ordena una lista alfabeticamente y numericamente
	
	Parameters:
	-----------
	lista: list
	
	Returns:
	--------
	lista: list
	
	"""

	# ordena una lista numericamente y alfabeticamente
	return sorted(lista)

def searchElement(host, lista):
	"""
	Funcion que busca un elemento en una lista
	
	Parameters:
	-----------
	host: str
	lista: list
	
	Returns:
	--------
	True: bool
	False: bool
	
	"""

	# encuentra el elemento host en una lista
	# la lista ha de estar ordenada alfabeticamente para el uso de esta funcion, es importante
	lista_ordenada = shortList(lista)
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
