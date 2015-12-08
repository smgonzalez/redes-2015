#!/usr/bin/python

import math
from sys import argv
from os import listdir
from tDistribution import tDistribution
from datetime import datetime
import ntpath

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
    pvalue = float(next(file).split()[P_VALUE_INDEX])

    # GrubbsTest parse
    next(file)
    N = int(next(file).split()[1])
    G = float(next(file).split()[1])

    rejectNumer = calculateRejectNumber(N)

    isOutlier = "SI" if float(G) > float(rejectNumer) else "NO"
    dateStr = ntpath.basename(filename)[4:-4]
    dateObj = datetime.strptime(dateStr, "%Y-%m-%d_%H_%M_%S")
    date = dateObj.strftime("%Y-%m-%d %H:%M")

    summarize = "%s\t%s\t%s\t%d\t%.2f\t%f\t%.2f\t%.4f\t%s\n" % (date, ip_edge1, ip_edge2, N, max_drtt, pvalue, G, rejectNumer, isOutlier)
    out_file.write(summarize)


def calculateRejectNumber(N):

    # Se calcula el primer termino del producto
    p1 = (N-1) / math.sqrt(N) 

    # Se busca el valor critico para la distribucion T con n-2 grados de libertad
    t = tDistribution[N-2]
    t2 = math.pow(t, 2)

    # Se calcula el segundo termino del producto
    p2 = math.sqrt(t2 / (N - 2 + t2))

    return p1 * p2

def main():

    file_dir = argv[1]
    
    out_file = open(file_dir+"-sum.txt", 'w')
    out_file.write("HORA\tIP_SRC\tIP_DST\tN\tDRTT_MAX\tP_VALOR\tESTADISTICO\tVALOR_CRITICO\tES_OUTLIER?\n")

    for file in listdir(file_dir):
        if ".txt" in file:
            parse_file(file_dir+"/"+file, out_file)

    out_file.close()

if __name__ == "__main__":
    main()
