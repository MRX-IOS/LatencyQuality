#!/usr/bin/python3

from elasticsearch import Elasticsearch, helpers, RequestsHttpConnection
from indexConfigurations import configurations
import csv
import json
from datetime import date

#### DATE ####
# dd/mm/YY
fecha = date.today().strftime("%d-%m-%Y")

#### FILE PATH ####
filePath = "./exports/resultados_" + fecha + ".csv"
Host = "192.168.1.58"
Port = 9200

print(filePath)

#### CONECTION ####

#elastic_Server = Elasticsearch(host = "192.168.1.58", port = 9200)
elastic_Server = Elasticsearch(host = Host, port = Port)

#### CREATE INDICE ####

# create index if not exists
if not elastic_Server.indices.exists(index="prueba"):
	elastic_Server.indices.create(
		index="prueba",
		body = configurations
	)
else:
	print("Index already exists")



#### READ DATA ####

index_name = "prueba"

def generate_docs():
	with open(filePath, "r") as fi:
		reader = csv.DictReader(fi, delimiter=";")
		actions = []

		for row in reader:
			doc = {
				"_index": index_name,
				"_id": row["host"],
				"_source": {
					"host": 		row["host"],
					"public_ip": 		row["public_ip"],
					"status": 		row["status"],
					"attempts": 		int(row["attempts"]),
					"latency_ms": 		float(row["latency (ms)"]),
					"date": 		row["date"],
					"timestamp": 		row["timestamp"],
				},
			}
			yield doc

#### SEND DATA ####

helpers.bulk(elastic_Server, generate_docs())

# Check the results:
result = elastic_Server.count(index=index_name)
# print(result.body['count'])
