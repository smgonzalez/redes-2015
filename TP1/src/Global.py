# -- coding: utf-8 --

# Variables
FILE_HEADER="Fecha y Hora  |  Mac origen  |  Mac destino  |  IP origen  |  IP destino  |  Type\n"
FAKE_IP='\txxx:xxx:xxx:xxx'

DEFAULT_TIMEOUT=None
DEFAULT_FILE='./out/sniff.out'
DEFAULT_ENTROPY_FILE='./out/entropy.out'
DEFAULT_ARP_ENTROPY_FILE='./out/arp_entropy.out'

SCAPY_WHO_HAS=1
SCAPY_IS_AT=2

WHO_HAS_TEXT='ARP:who-has'
IS_AT_TEXT='ARP:is-at'

GRAPH_COMMAND="grafos/Graficador.py %s %s" #(data_file, img_file)
DEFAULT_IMG_FILE="./graph.jpg"

# Parameters
APP_DESCRIPTION='Capturador de paquetes y calculo de entropia'

ARP_PARAM='--arp'
ARP_PARAM_ALIAS='arp'
ARP_HELP='Capturar solo paquetes ARP'

CONSOLE_PARAM='console'
CONSOLE_PARAM_SHORT='-c'
CONSOLE_PARAM_LONG='--console'
CONSOLE_HELP='Mostrar salida en consola'

FILE_PARAM='file'
FILE_PARAM_SHORT='-f'
FILE_PARAM_LONG='--file'
FILE_HELP='Archivo de salida para las capturas, (default: '+DEFAULT_FILE+')'

ARP_ENTROPY_FILE_PARAM='arpefile'
ARP_ENTROPY_FILE_PARAM_SHORT='-arpe'
ARP_ENTROPY_FILE_PARAM_LONG='--arp-entropy-file'
ARP_ENTROPY_HELP='Archivo de salida para la entropia, (default:'+DEFAULT_ARP_ENTROPY_FILE+')'

GRAPH_PARAM_ALIAS='graph'
GRAPH_PARAM='--graph'
GRAPH_HELP='Graficar el grafo de nodos basandose en ARP. (Requiere: graphviz)'

ENTROPY_FILE_PARAM='efile'
ENTROPY_FILE_PARAM_SHORT='-e'
ENTROPY_FILE_PARAM_LONG='--entropy-file'
ENTROPY_HELP='Archivo de salida para la arp entropia, (default: '+DEFAULT_ENTROPY_FILE+')'

TIMEOUT_PARAM='timeout'
TIMEOUT_PARAM_SHORT='-t'
TIMEOUT_PARAM_LONG='--timeout'
TIMEOUT_HELP='Tiempo de capura, (default: capturar indefinidamente)'
