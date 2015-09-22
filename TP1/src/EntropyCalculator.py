from scapy.all import *
from Global import *

class EntropyCalculator(object):

    def __init__(self):
        self.entropy = 0.0
        self.total_packets = 0.0
        self.packet_types = {}
        self.packet_names = {}
        self.total_ips = 0.0
        self.packet_ips = {}

    def entropyUpdate(self, pkt):

        self.total_packets += 1 
        if self.packet_types.get(pkt[Ether].type) != None:
            self.packet_types[pkt[Ether].type] += 1  
        else:
            self.packet_types[pkt[Ether].type] = 1
            self.packet_names[pkt[Ether].type] = pkt[1].name

    def arp_entropyUpdate(self, pkt):

        if(pkt[1].name == 'ARP'):        

          self.total_ips += 2 

          psrc = pkt[ARP].psrc
          pdst = pkt[ARP].pdst

          if self.packet_ips.get(psrc) != None:
             self.packet_ips[psrc] += 1  
          else:
             self.packet_ips[psrc] = 1

          if self.packet_ips.get(pdst) != None:
             self.packet_ips[pdst] += 1  
          else:
             self.packet_ips[pdst] = 1

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

    def arp_write_to_file(self, file):

        file.write("ips: "+str(self.total_ips)+"\n")
        entropy = 0.0

        for ip in self.packet_ips:
            file.write("("+str(ip)+") cantidad: "+str(self.packet_ips[ip])+"\n")
            prob = self.packet_ips[ip]/self.total_ips
            file.write("P("+str(ip)+") = "+str(prob)+"\n")
            info = -math.log(prob,2)
            file.write("I("+str(ip)+") = "+str(info)+"\n")
            entropy = entropy + (prob * info)

        file.write("H(S) = "+str(entropy)+"\n")
        file.close()

