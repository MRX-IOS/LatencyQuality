#!/usr/bin/python3

from elasticsearch import Elasticsearch, helpers, RequestsHttpConnection
from elasticsearch.exceptions import ElasticsearchWarning
from indexConfigurations import configurations
from configuration import projectPath, fecha, elasticHost, elasticPort, elasticUser, elasticPassword, elasticIndex
from datetime import date
import warnings
import json
import csv

warnings.filterwarnings("ignore", category=ElasticsearchWarning)

#### FILE PATH ####
filePath = projectPath + "exports/resultados_" + fecha + ".csv"

def isLowerCase(s):
	if s != s.lower():
		return False
	else:
		return True

def connectElastic():
	#### CONECTION ####
	print("\n[+]\tHost: " + elasticHost)
	print("[+]\tPort: " + str(elasticPort))
	print("[+]\tUser: " + elasticUser)
	print("[+]\tSonda: " + elasticIndex)
	print("")

	print("[INFO] Connecting to Elasticsearch...")
	elastic_Server = Elasticsearch(host = elasticHost, port = elasticPort, http_auth=(elasticUser, elasticPassword), timeout=30, max_retries=10, retry_on_timeout=True)
	return elastic_Server

def createIndex(elastic_Server):
	#### CREATE INDICE ####
	# create index if not exists
	if not elastic_Server.indices.exists(index = elasticIndex):
		print("[INFO] Creating index...")
		elastic_Server.indices.create(
			index = elasticIndex,
			body = configurations
		)
	else:
		print("[INFO] Index already exists!")

def generateDoc():
	""" 
		Generate the document to send to Elasticsearch
	"""
	#### GENERATE DOCUMENT ####

	with open(filePath, "r") as fi:
		reader = csv.DictReader(fi, delimiter=";")
		actions = []
	
		for row in reader:
			doc = {
				"_index": elasticIndex,
				"_source": {
					"host": 		row["host"],
					"public_ip": 	row["public_ip"],
					"status": 		row["status"],
					"attempts": 	int(row["attempts"]),
					"city":			row["city"],
					"region": 		row["region"],
					"country": 		row["country"],
					"source_point": row["source_point"],
					"destination": 	row["destination"],
					"ASN": 			row["ASN"],
					"ISP": 			row["ISP"],
					"postal": 		row["postal"],
					"timezone": 	row["timezone"],
					"latency_ms": 	float(row["latency (ms)"]),
					"date": 		row["date"]
				}
			}
			yield doc
	return doc

def sendData(elastic_Server, doc):
	#### SEND DATA ####
	helpers.bulk(elastic_Server, doc)

def run():
	if isLowerCase(elasticIndex) == False:
		print("[ERROR] Index name must be lowercase!")
	else:
		print("[INFO] Starting Elastic bulk script...")
		elastic_Server = connectElastic()
		createIndex(elastic_Server)
		result = elastic_Server.count(index=elasticIndex)
		print("[INFO] Indexing data...")
		doc = generateDoc()
		print("[INFO] Sending data to Elasticsearch...")
		sendData(elastic_Server, doc)

	# Check the results:
	result = elastic_Server.count(index=elasticIndex)
	return result

run()
