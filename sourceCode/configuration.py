# This file contains the configuration parameters for the LatencyQuality project

from datetime import date
from datetime import datetime

# The maximum timeout for the ping command
maxPingTimeout = "0.2"

# The path to the folder where the project is located
path = "/home/mrx/TFG/proyecto/LatencyQuality/"
#path = "/home/mrx/TFG/Client/LatencyQuality/"

# The path to the folder where the input files are located
# hostsFile: the file containing the list of hosts to be tested
hostsFile = path + 'inFiles/TotalWebs.txt'
# PingBlockFile: the file containing the list of hosts to be blocked
pingBlockFile = path + 'inFiles/PingBlock.txt'

# The path to the folder where are located the script files to be executed for cleaning the DNS cache
cleanFile = path + 'clean/dns-clean'

# The path to the folder where the results will be stored
resultsPath = path + 'results/'

# dd/mm/YY
fecha = date.today().strftime("%d-%m-%Y")
