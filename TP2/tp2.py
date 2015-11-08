from scapy.all import *
import time
import sys

#traceroute sobre ICMP

ECHO_REPLY = 0
ECHO_REQUEST = 11

TIMEOUT = 2
MAX_TTL = 100
REPEAT_COUNT = 3

text_file = open("Output.txt", "w")
header = "TTL\tIntentos\tIp\tRTT Promedio"

print(header)
print(header, file=text_file)

class Route:

	def __init__(self):
		self.hops = dict()
		
	def trace(self, hostname):

		#Sea h la IP del host destino y sea ttl = 1.

		ttl = 1

		#Repetir los siguientes pasos hasta obtener una respuesta ICMP de tipo
		#Echo Reply por parte de h:
		
		reply = False
		
		while((not reply) and ttl < MAX_TTL):
		
			#Enviar un paquete ICMP de tipo Echo Request al host h cuyo campo
			#TTL en el header IP valga ttl.
			packet = IP(dst=hostname, ttl=ttl) / ICMP()

			rtt_sum = 0.0       # Suma de los RTT para cada TTL
			cant_success = 0    # Cantidad de paquetes enviados y recibidos exitosamente para cada TTL
			
			attempt=1
			while attempt <= REPEAT_COUNT:

				rtt = int(round(time.time() * 1000))
				answer = sr1(packet, timeout=TIMEOUT, verbose=0)
				rtt = int(round(time.time() * 1000)) - rtt
				answer_ip = None

				if answer != None:

					if answer.type == ECHO_REPLY:
						reply = True
				
					if answer_ip == None: 
						ip_src = answer[IP].src
					
					elif answer_ip != answer[IP].src: #Si cambia la IP del RTT, no se promedia y se continua con el proximo TTL
						break  
						
					# Si proviene del a misma IP que antes (o es el primer intento), se suma el RTT
					rtt_sum += rtt
					cant_success += 1
				
				attempt += 1
										
			#Si se recibe una respuesta ICMP de tipo Time Exceeded, anotar la IP
			#origen de dicho paquete.    
			if rtt_sum > 0:

				rtt_prom = rtt_sum / cant_success
				self.hops[ttl] = (cant_success, ip_src, rtt_prom)		# MAP: TTL -> (intentos, ip que respondio, promedio de RTT)
				
				info_hop = "%d:\t%d\t%s\t%fms\n" % (ttl, cant_success, ip_src, rtt_prom)
					
				print(info_hop)
				print(info_hop, file=text_file)

			else:
				#En otro caso, marcar como desconocido (*) el
				#hop.
				noResponse = str(ttl) + ":\t **** No hubo respuesta ***"
				print(noResponse)
				print(noResponse, file=text_file)

			#Incrementar ttl.
			ttl = ttl+1

		text_file.close()
		
		
def main(argv=sys.argv):
	route = Route()
	route.trace(argv[1])

	
	
if __name__ == '__main__':
	main()
