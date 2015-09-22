from scapy.all import *
from Global import *
from EntropyCalculator import *

class Sniffer(object):

    def __init__(self, args):
        self.index=0

        # Parametros
        self.file = args[FILE_PARAM]
        self.entropy_file = args[ENTROPY_FILE_PARAM]
        self.arp_entropy_file = args[ARP_ENTROPY_FILE_PARAM]
        self.timeout = args[TIMEOUT_PARAM]
        self.arp = args[ARP_PARAM_ALIAS]
        self.console = args[CONSOLE_PARAM]

        # Variables
        self.entropyCalculator = EntropyCalculator()
        self.arp_text= {
            SCAPY_WHO_HAS : WHO_HAS_TEXT,
            SCAPY_IS_AT : IS_AT_TEXT
        } 

    def run(self):

        self.file.write(FILE_HEADER)
        sniff(prn=self.writePacketToFile, timeout = self.timeout, filter=self.arp)
        self.file.close()

        self.entropyCalculator.write_to_file(self.entropy_file)

        self.entropyCalculator.arp_write_to_file(self.arp_entropy_file)

    def writePacketToFile(self, packet):

        if ARP in packet:
            packetInfo = str(self.index)+':'
            packetInfo += self.decorate(packet[1].hwsrc)
            packetInfo += self.decorate(packet[1].hwdst)
            packetInfo += self.decorate(packet[1].psrc)
            packetInfo += self.decorate(packet[1].pdst)
            packetInfo += self.decorate(self.arp_text[packet[1].op])

        else:
            packetInfo = str(self.index)+':'
            packetInfo += self.decorate(packet.src)
            packetInfo += self.decorate(packet.dst)

            if IP in packet:
                packetInfo += self.decorate(packet[IP].src)
                packetInfo += self.decorate(packet[IP].dst)
            else:
                packetInfo += FAKE_IP
                packetInfo += FAKE_IP

            packetInfo += self.decorate(packet[1].name)

        if self.console:
            print(packetInfo)

        packetInfo += '\n'
        self.file.write(packetInfo)
        self.index+=1

	self.entropyCalculator.arp_entropyUpdate(packet)
	
	self.entropyCalculator.entropyUpdate(packet)

    def decorate(self, obj):
        return "\t'" + str(obj) + '\''
