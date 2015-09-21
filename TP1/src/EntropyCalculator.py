from scapy.all import *
from Global import *

class EntropyCalculator(object):

    def __init__(self):
        self.entropy = 0.0
        self.total_packets = 0.0
        self.packet_types = {}
        self.packet_names = {}

    def entropyUpdate(self, pkt):

        self.total_packets += 1 
        if self.packet_types.get(pkt[Ether].type) != None:
            self.packet_types[pkt[Ether].type] += 1  
        else:
            self.packet_types[pkt[Ether].type] = 1
            self.packet_names[pkt[Ether].type] = pkt[1].name

    def arp_entropyUpdate(self, pkt):

        self.total_packets += 2 
	
	psrc = pkt[ARP].psrc
	pdst = pkt[ARP].pdst
	
        if self.packet_types.get(psrc) != None:
            self.packet_types[psrc] += 1  
        else:
            self.packet_types[psrc] = 1
	    self.packet_names[psrc] = pkt[1].name

	if self.packet_types.get(pdst) != None:
            self.packet_types[pdst] += 1  
        else:
            self.packet_types[pdst] = 1
	    self.packet_names[pdst] = pkt[1].name

    def write_to_file(self, file):

        file.write("paquetes: "+str(self.total_packets)+"\n")
        entropy = 0.0

        for type in self.packet_types:
            file.write(self.packet_names[type]+"("+str(type)+") Paquetes: "+str(self.packet_types[type])+"\n")
            prob = self.packet_types[type]/self.total_packets
            file.write(self.packet_names[type]+" P("+str(type)+") = "+str(prob)+"\n")
            info = -math.log(prob,2)
            file.write(self.packet_names[type]+" I("+str(type)+") = "+str(info)+"\n")
            entropy = entropy + (prob * info)

        file.write("H(S) = "+str(entropy)+"\n")	
        file.close()

