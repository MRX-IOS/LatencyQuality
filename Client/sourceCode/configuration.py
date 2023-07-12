# This file contains the configuration parameters for the LatencyQuality project

from datetime import date
from datetime import datetime
import os

# Path variables
projectPath = "/home/mrx/TFG/proyecto/LatencyQuality/Client"

# File paths
hostsFilePath = projectPath + 'inFiles/TotalWebs.txt'
pingBlockFilePath = projectPath + 'inFiles/PingBlock.txt'
cleanFilePath = projectPath + 'clean/dns-clean'
resultsPath = projectPath + 'results/'

# Ping variables
maxPingTimeout = "0.2" # seconds (200 ms) max ping timeout

# Date variables
fecha = date.today().strftime("%d-%m-%Y") # dd/mm/YY

# Elastic variables
elasticHost = "92.189.190.237"
elasticPort = "999"
elasticUser = "sonda"
elasticPassword = "sonda_tfg_2023"
elasticIndex = "sonda_0"
