#!/usr/bin/python

import math
from sys import argv
from os import listdir
from tDistribution import tDistribution
from datetime import datetime
import ntpath

IGNORE_HEADER = True
IGNORE_FIRST_DRTT = True

IP_INDEX = 1
DRTT_INDEX = 5
P_VALUE_INDEX = 3

NO_RESPONSE = "No hubo respuesta"
NORMALTEST_BEGIN = "NormalTest"
GRUBBS_BEGIN = "GrubbsTest"

def parse_file(filename):

    file = open(filename,'r')

    if IGNORE_HEADER:
        next(file)
    
    ip_ant = "IP origen"
    drtts = []

    for line in file:
        
        if NORMALTEST_BEGIN in line:
            break

        if NO_RESPONSE in line:
            continue

        hop = line.split("\t")
        ip = hop[IP_INDEX]
        drtt = float(hop[DRTT_INDEX].replace("ms",""))

        drtts.append((ip_ant, ip, drtt))
        ip_ant = ip

    return drtts


def calculateGrubbsTest(drtts, infile, outfile):
    
    if IGNORE_FIRST_DRTT:   # For testing 2 outliers
        maxValue = maxRtt(drtts)
        drtts.remove(maxValue)

    maxDrtt = maxRtt(drtts) 

    numbers = []
    for ip1, p2, drtt in drtts:
        
        numbers.append(drtt)

    # Normal test
    #normal = stats.normaltest(numbers)
    #pValue =  normal[1]
    pValue = 1.0

    # Test de Grubbs #
    zscores = calculateZScore(numbers)

    N = len(numbers)
    sampleMean = calculateAverage(numbers)
    standarDeviation = calculateStandardDeviation(numbers)

    # Estadistico
    G = (max(numbers) - sampleMean) / standarDeviation

    rejectNumer = calculateRejectNumber(N)

    isOutlier = "SI" if float(G) > float(rejectNumer) else "NO"
    dateStr = ntpath.basename(infile)[4:-4]
    dateObj = datetime.strptime(dateStr, "%Y-%m-%d_%H_%M_%S")
    date = dateObj.strftime("%Y-%m-%d %H:%M")

    summarize = "%s\t%s\t%s\t%d\t%.2f\t%f\t%.2f\t%.4f\t%s\n" % (date, maxDrtt[0], maxDrtt[1], N, maxDrtt[2], pValue, G, rejectNumer, isOutlier)
    outfile.write(summarize)   


def maxRtt(drtts):
            
    max_drtt = drtts[0]
    for drtt in drtts:
        if max_drtt[2] < drtt[2]:
            max_drtt = drtt

    return max_drtt


def calculateAverage(numbers):

    sum=0
    for num in numbers:
        sum += num

    return sum / float(len(numbers))


def calculateStandardDeviation(numbers):

    average = calculateAverage(numbers)
    variance = 0.0

    for num in numbers:
        variance += pow(num - average, 2)

    variance = variance / float(len(numbers)-1)
    return math.sqrt(variance)


def calculateZScore(numbers):

    average = calculateAverage(numbers)
    standarDeviation = calculateStandardDeviation(numbers)

    zscores = []
    for num in numbers:
        zscore = math.fabs(num - average) / standarDeviation
        zscores.append((num, zscore))

    return zscores


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
            drtts = parse_file(file_dir+"/"+file)
            calculateGrubbsTest(drtts, file, out_file)
            


    out_file.close()

if __name__ == "__main__":
    main()
