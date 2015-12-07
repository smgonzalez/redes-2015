#!/usr/bin/python

from sys import argv
from os import listdir

IGNORE_HEADER = True

IP_INDEX = 1
DRTT_INDEX = 5
P_VALUE_INDEX = 3

NO_RESPONSE = "No hubo respuesta"
NORMALTEST_BEGIN = "NormalTest"
GRUBBS_BEGIN = "GrubbsTest"

def parse_file(filename, out_file):

    file = open(filename,'r')

    if IGNORE_HEADER:
        next(file)
    
    max_drtt = 0.0
    ip_ant = "IP origen"
    ip_edge1 = ip_ant
    ip_edge2 = None

    for line in file:
        
        if NORMALTEST_BEGIN in line:
            break

        if NO_RESPONSE in line:
            continue

        hop = line.split("\t")
        ip = hop[IP_INDEX]
        drtt = float(hop[DRTT_INDEX].replace("ms",""))

        if drtt > max_drtt:
            ip_edge1 = ip_ant
            ip_edge2 = ip
            max_drtt = drtt

        ip_ant = ip

    # NormalTest parse
    pvalue = next(file).split()[P_VALUE_INDEX]

    # GrubbsTest parse
    next(file)
    N = next(file).split()[1]
    G = next(file).split()[1]
    C = next(file).split()[1]

    isOutlier = "SI" if float(G) > float(C) else "NO"

    summarize =  ip_edge1 +"\t"+ ip_edge2 +"\t"+ N +"\t"+ str(max_drtt) +"\t"+ pvalue +"\t"+ G +"\t"+ C +"\t"+ isOutlier +"\n"
    out_file.write(summarize)

def main():

    file_dir = argv[1]
    
    out_file = open(file_dir+"-sum.txt", 'w')
    out_file.write("IP_SRC\tIP_DST\tN\tDRTT_MAX\tP_VALOR\tESTADISTICO\tVALOR_CRITICO\tES_OUTLIER?\n")

    for file in listdir(file_dir):
        if ".txt" in file:
            parse_file(file_dir+"/"+file, out_file)

    out_file.close()

if __name__ == "__main__":
    main()
