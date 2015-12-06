#!/bin/bash

while true
do
	DATE=`date +%Y-%m-%d:%H:%M:%S`
	#sudo python tp2.py www.helsinki.fi &> fin-$DATE.txt
	sudo echo hola &> fin-$DATE.txt
	DATE=`date +%Y-%m-%d:%H:%M:%S`
	#sudo python tp2.py www.ox.ac.uk &> eng-$DATE.txt
	sudo echo hola &> eng-$DATE.txt
	sleep 5
done
