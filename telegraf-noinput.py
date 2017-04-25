#!/usr/bin/python
import os
import sys
import subprocess
import argparse

#Disponible en https://github.com/Loenberg123/

parser = argparse.ArgumentParser()
parser.add_argument("-Q", "--query", help="Realizar consulta", action="store_true")
parser.add_argument("-v", "--version", help="Consulta la version del servidor Influx", action="store_true")
parser.add_argument("-S", "--secure", help="Usar https en lugar de http", const="https", default="http", action="store_const")
parser.add_argument("-i", "--ip", help="Indica la ip de influx")
parser.add_argument("-d", "--database", help="Indica la base de datos para la consulta")
parser.add_argument("-H", "--host", help="Indica el host para la consulta")
parser.add_argument("-t", "--time", help="Indicar el tiempo de comprobacion. Ns, Nm, Nh (N=numero deseado, s-segundos, m-minutos, h-horas")
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()


if args.query:
	q = "curl -s -G "+ args.secure +"://"+ args.ip +":8086/query --data-urlencode db="+ args.database +" --data-urlencode \"q=SELECT last(boot_time) FROM kernel WHERE host='"+args.host+"' AND time >= now() - "+args.time+"\""
	result = subprocess.check_output(q, shell=True)
	check = "series"
	data = result.find(check)
	if result is None:
		print "UNKNOWN - Could not retrieve data?"
		sys.exit(3)
	if data == -1:
		print "CRITICAL - Host: "+args.host+" not sending data for: "+args.time
	       	sys.exit(2)
	else:
		print "OK - Host: "+args.host+" is sending data to InfluxDB"
		sys.exit(0)


if args.version:
	version = "curl -sl -I "+ args.secure +"://"+ args.ip +":8086/ping | awk 'NR==4{print}'"
	result = subprocess.check_output(version, shell=True)
	if result is not None:
		print result
		sys.exit(0)
	else:
		print "CRITICAL - Could not get version"
		sys.exit(2)
