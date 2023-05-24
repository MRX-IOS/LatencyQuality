# This file contains the configuration parameters for the LatencyQuality project

from datetime import date
from datetime import datetime

# Path variables
projectPath = "/home/mrx/TFG/proyecto/LatencyQuality/"
#projectPath = "/home/mrx/TFG/Client/LatencyQuality/"

# File paths
hostsFilePath = projectPath + 'inFiles/TotalWebs.txt'
pingBlockFilePath = projectPath + 'inFiles/PingBlock.txt'
cleanFilePath = projectPath + 'clean/dns-clean'
resultsPath = projectPath + 'results/'

# Ping variables
# The maximum timeout for the ping command
# This value can be modified in production or development environments
maxPingTimeout = "0.2"

# Date variables
# dd/mm/YY
fecha = date.today().strftime("%d-%m-%Y")

