#!/usr/bin/python

import sys
import math

MINUTE = 0
IP_SRC = 1
IP_DST = 2
PROTO = 3

def main():

    infile = open(sys.argv[1], 'r')
    outfile = open(sys.argv[2], 'w')
    outfile.write("Minuto\tEntropia IP\tEntropia Proto\n")

    ip_dict = dict()
    proto_dict = dict()
    current_minute = 1

    for line in infile:
        pkt = line.replace("\n","").split()    
        minute = int(pkt[MINUTE])

        if minute > current_minute:
            calculate_entropy(ip_dict, proto_dict, current_minute, outfile)
            current_minute = minute

        src = pkt[IP_SRC]
        dst = pkt[IP_DST]
        proto = "ARP" if "ARP" in pkt[PROTO] else pkt[PROTO]
        
        add_to_dict(proto_dict, proto)

        if proto == "ARP":
            add_to_dict(ip_dict, src)
            add_to_dict(ip_dict, dst)

    infile.close()


def calculate_entropy(ip_dict, proto_dict, minute, outfile):

    total_ips = float(sum(ip_dict.values()))
    total_proto_pkgs = float(sum(proto_dict.values()))

    entropy_ip = 0.0
    entropy_proto = 0.0

    for ip, cant in ip_dict.items():
        prob = cant / total_ips 
        info = -math.log(prob,2)
        entropy_ip += (prob * info)

    for proto, cant in proto_dict.items():
        prob = cant / total_proto_pkgs 
        info = -math.log(prob,2)
        entropy_proto += (prob * info)

    line = "%d\t%.2f\t%.2f\n" % (minute, entropy_ip, entropy_proto)
    outfile.write(line)


def add_to_dict(dicc, key):
    
    if dicc.get(key) != None:
        dicc[key] += 1
    else:
        dicc[key] = 1


if __name__ == "__main__":
    main()
