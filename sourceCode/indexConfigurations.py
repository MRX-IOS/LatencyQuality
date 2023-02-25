#!/usr/bin/python3

configurations = {
	"settings": {
		"index": {"number_of_shards": 2},
		"analysis": {
			"filter": {
				"ngram_filter": {
					"type": "edge_ngram",
					"min_gram": 2,
					"max_gram": 15,
				},
			},
			"analyzer": {
				"ngram_analyzer": {
					"type": "custom",
					"tokenizer": "standard",
					"filter": ["lowercase", "ngram_filter"],
				},
			},
		},
	},

	"mappings": {
		"properties": {
			"@timestamp": {
				"type": "date",
			},
			"attempts": {
				"type": "long"
			},
			"date": {
				"type": "date",
				"format": "dd-MM-yyyy HH:mm:ss"
			},
			#"time": {
			#	"type": "date",
			#	"format": "HH:mm:ssZ"
			#},
			"host": {
				"type": "keyword"
			},
			"latency (ms)": {
				"type": "double"
			},
			"public_ip": {
				"type": "keyword"
			},
			"status": {
				"type": "keyword"
			},
		}
	}
}
