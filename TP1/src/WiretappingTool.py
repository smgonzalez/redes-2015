#!/usr/bin/python

import sys
import os
import argparse
from Global import *
from Sniffer import *

def main():

    args = parse_arguments()

    sniffer = Sniffer(args)
    sniffer.run()

    if args[GRAPH_PARAM_ALIAS]:

        command = GRAPH_COMMAND % (args[FILE_PARAM].name, DEFAULT_IMG_FILE) 
        os.system(command)

def parse_arguments():
    
    args_parser = argparse.ArgumentParser(description=APP_DESCRIPTION, prog='sudo '+sys.argv[0])
    args_parser.add_argument(FILE_PARAM_SHORT, FILE_PARAM_LONG, type=argparse.FileType('w'), dest=FILE_PARAM, default=DEFAULT_FILE, metavar='ARCHIVO', help=FILE_HELP)
    args_parser.add_argument(ENTROPY_FILE_PARAM_SHORT, ENTROPY_FILE_PARAM_LONG, dest=ENTROPY_FILE_PARAM, type=argparse.FileType('w'), default=DEFAULT_ENTROPY_FILE, metavar='ARCHIVO', help=ENTROPY_HELP)
    args_parser.add_argument(TIMEOUT_PARAM_SHORT, TIMEOUT_PARAM_LONG, type=int, default=DEFAULT_TIMEOUT, dest=TIMEOUT_PARAM, metavar='TIMEOUT', help=TIMEOUT_HELP)
    args_parser.add_argument(CONSOLE_PARAM_SHORT, CONSOLE_PARAM_LONG, action='store_true', dest=CONSOLE_PARAM, help=CONSOLE_HELP)
    args_parser.add_argument(ARP_PARAM, action='store_const', dest=ARP_PARAM_ALIAS, const='arp', help=ARP_HELP)
    args_parser.add_argument(ARP_ENTROPY_FILE_PARAM_SHORT, ARP_ENTROPY_FILE_PARAM_LONG, dest=ARP_ENTROPY_FILE_PARAM, type=argparse.FileType('w'), default=DEFAULT_ARP_ENTROPY_FILE, metavar='ARCHIVO', help=ARP_ENTROPY_HELP)
    args_parser.add_argument(GRAPH_PARAM, action='store_true', dest=GRAPH_PARAM_ALIAS, help=GRAPH_HELP)

    return vars(args_parser.parse_args())

if __name__ == '__main__':
    main()
