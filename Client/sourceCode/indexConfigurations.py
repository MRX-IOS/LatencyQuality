#!/usr/bin/python3

# f.to_csv(final_file_csv, index=False, encoding='utf-8', sep=';', columns=['host', 'public_ip', 'status', 'attempts', 'city', 'country', 'localization', 'organization', 'postal', 'timezone', 'latency (ms)', 'date'], na_rep='Unknow')

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
			"city": {
				"type": "keyword"
			},
			"country": {
				"type": "keyword"
			},
			"source_point": {
				"type": "geo_point",
				"ignore_malformed": True,
				"null_value": "0,0"
			},
			"destination": {
				"type": "geo_point",
				"ignore_malformed": True,
				"null_value": "0,0"
            },
			"ASN": {
				"type": "keyword"
			},
			"ISP": {
				"type": "keyword"
			},
			"postal": {
				"type": "keyword"
			},
			"timezone": {
				"type": "keyword"
			},
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
