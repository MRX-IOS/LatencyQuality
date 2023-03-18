#!/usr/bin/python3

from elasticsearch import Elasticsearch, helpers, RequestsHttpConnection
from indexConfigurations import configurations
from configuration import path
import csv
import json
from datetime import date

#### DATE ####
# dd/mm/YY
fecha = date.today().strftime("%d-%m-%Y")

#### ELASTICSEARCH CONFIGURATIONS ####
Host = "192.168.1.58"
Port = 9200
index_name = "sonda_0"

#### FILE PATH ####
filePath = path + "exports/resultados_" + fecha + ".csv"
# print(filePath)

def isLowerCase(s):
	if s != s.lower():
		return False
	else:
		return True

def connectElastic():
	#### CONECTION ####
	print("\n[+]\tHost: " + Host)
	print("[+]\tPort: " + str(Port))
	print("[+]\tSonda: " + index_name)
	print("")

	print("[INFO] Connecting to Elasticsearch...")
	elastic_Server = Elasticsearch(host = Host, port = Port)
	return elastic_Server

def createIndex(elastic_Server):
	#### CREATE INDICE ####
	# create index if not exists
	if not elastic_Server.indices.exists(index = index_name):
		print("[INFO] Creating index...")
		elastic_Server.indices.create(
			index = index_name,
			body = configurations
		)
	else:
		print("[INFO] Index already exists!")

def generateDoc():
	"""
		Generate a document to send to Elasticsearch
	"""
	#f.to_csv(final_file_csv, index=False, encoding='utf-8', sep=';', columns=['host', 'public_ip', 'status', 'attempts', 'city', 'country', 'localization', 'organization', 'postal', 'timezone', 'latency (ms)', 'date'], na_rep='Unknow')

	#### GENERATE DOCUMENT ####
	with open(filePath, "r") as fi:
		reader = csv.DictReader(fi, delimiter=";")
		actions = []

		for row in reader:
			doc = {
				"_index": index_name,
				# "_id": row["host"],
				"_source": {
					"host": 		row["host"],
					"public_ip": 	row["public_ip"],
					"status": 		row["status"],
					"attempts": 	int(row["attempts"]),
					"city":			row["city"],
					"region": 		row["region"],
					"country": 		row["country"],
					"localization": row["localization"],
					"organization": row["organization"],
					"postal": 		int(row["postal"]),
					"timezone": 	row["timezone"],
					"latency_ms": 	float(row["latency (ms)"]),
					"date": 		row["date"],
				},
			}
			yield doc
	return doc

def sendData(elastic_Server, doc):
	#### SEND DATA ####
	# Send the data:
	helpers.bulk(elastic_Server, doc)
	# print(result.body['count'])

def run():
	if isLowerCase(index_name) == False:
		print("[ERROR] Index name must be lowercase!")
	else:
		print("[INFO] Starting script...")
		elastic_Server = connectElastic()
		createIndex(elastic_Server)
		result = elastic_Server.count(index=index_name)
		print("[INFO] Indexing data...")
		doc = generateDoc()
		print("[INFO] Sending data to Elasticsearch...")
		sendData(elastic_Server, doc)

	# Check the results:
	result = elastic_Server.count(index=index_name)
	# print(result)
	return result

# run()