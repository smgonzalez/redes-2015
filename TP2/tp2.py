from scapy.all import *
import time
import sys

#traceroute sobre ICMP

ECHO_REPLY = 0
ECHO_REQUEST = 11

TIMEOUT = 2
MAX_TTL = 100

# Intentos para el mismo TTL, de cambiar la IP en menos de MIN_ATTEMPS, se reinicia el TTL
MAX_ATTEMPTS = 10
MIN_ATTEMPS = 3

filename = "Output.txt"
header = "TTL\tIP\tIntentos\tRTT Promedio\tDesvio Standard\tDelta RTT"

print(header)

class Route:

	def __init__(self):
		self.hops = dict()
		self.text_file = open(filename, "w")
		print(header, file=self.text_file)
		
	def trace(self, hostname):

		#Sea h la IP del host destino y sea ttl = 1.

		ttl = 1

		#Repetir los siguientes pasos hasta obtener una respuesta ICMP de tipo
		#Echo Reply por parte de h:
		
		reply = False
		
		last_rtt_prom = 0.0
		
		while((not reply) and ttl < MAX_TTL):
		
			#Enviar un paquete ICMP de tipo Echo Request al host h cuyo campo
			#TTL en el header IP valga ttl.
			packet = IP(dst=hostname, ttl=ttl) / ICMP()

			rtt_sum = 0.0       # Suma de los RTT para cada TTL
			cant_success = 0    # Cantidad de paquetes enviados y recibidos exitosamente para cada TTL
			answer_ip = None
			
			rtts = []
			attempt=1
			while attempt <= MAX_ATTEMPTS:

				rtt = int(round(time.time() * 1000))
				answer = sr1(packet, timeout=TIMEOUT, verbose=0)
				rtt = int(round(time.time() * 1000)) - rtt

				if answer != None:

					if answer.type == ECHO_REPLY:
						reply = True
				
					if answer_ip == None: 
						answer_ip = answer[IP].src
					
					elif answer_ip != answer[IP].src: # Cambio la IP
						if attempt <= MIN_ATTEMPS: # volvemos a empezar, porque no tenemos suficientes RTTs para promediar
							answer_ip = answer[IP].src
							attempt = 2
							rtt_sum = rtt
							cant_success = 1
							rtts = [rtt]
							continue
						else:	# Si tenemos por lo menos MIN_ATTEMPS, promediamos con eso y seguimos al proximo TTL
							break
						
					# Si proviene del a misma IP que antes (o es el primer intento), se suma el RTT
					rtt_sum += rtt
					cant_success += 1
					rtts.append(rtt)
				
				attempt += 1
										
			#Si se recibe una respuesta ICMP de tipo Time Exceeded, anotar la IP
			#origen de dicho paquete.    
			if rtt_sum > 0:

				deviation = self.standardDeviation(rtts)
				rtt_prom = rtt_sum / cant_success
				
				deltaRTTi = rtt_prom - last_rtt_prom
				last_rtt_prom = rtt_prom
					
				self.hops[ttl] = Hop(ttl, answer_ip, cant_success, rtt_prom, deviation, deltaRTTi)
				
				info_hop = "%d:\t%s\t%d\t%.2fms\t%.2fms\t%.2fms" % (ttl, answer_ip, cant_success, rtt_prom, deviation, deltaRTTi)
					
				print(info_hop)
				print(info_hop, file=self.text_file)

			else:
				#En otro caso, marcar como desconocido (*) el
				#hop.
				noResponse = str(ttl) + ":\t **** No hubo respuesta ***"
				print(noResponse)
				print(noResponse, file=self.text_file)

			#Incrementar ttl.
			ttl = ttl+1

		self.text_file.close()
		
	def standardDeviation(self, numbers):
	
		sum=0
		for num in numbers:
			sum += num
			
		average = sum / float(len(numbers))
		variance = 0.0
		
		for num in numbers:
			variance += pow(num - average, 2)

		variance = variance / float(len(numbers)-1)
		return math.sqrt(variance)


class Hop:
	
	def __init__(self, ttl, ip_source, attempts, rtt_prom, deviation, deltaRTTi):
	
		self.ttl = ttl
		self.ip_source = ip_source
		self.attempts = attempts
		self.rtt_prom = rtt_prom
		self.deviation = deviation
		self.deltaRTTi = deltaRTTi
		
		
		
def main(argv=sys.argv):
	route = Route()
	route.trace(argv[1])

	
	
if __name__ == '__main__':
	main()
