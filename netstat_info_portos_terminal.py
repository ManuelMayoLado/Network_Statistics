# -*- coding: utf-8 -*-

#SOLO FUNCIONA EN WINDOWS

import os
import re
import socket
import time

def servizos_pid():
	#COMANDO PARA ESTRAER OS PID DOS DIFERENTES SERVIZOS
	os_servizos_pid = os.popen("tasklist").read().split("\n")
	#CREAMOS UN DICCIONARIO
	dict_servizos_pid = {}
	
	for servizo in os_servizos_pid:
		#DIVIDIMOS CADA COLUMNA DOS DATOS DOS SERVIZOS
		l_servizo = servizo.split()
		#CREAOS UNHA LISTA A QUE AGREGAREMOS O NOME E O PID
		l_servicio_pid = ["",""]
		if len(l_servizo) > 2:
			for col in l_servizo:
				#RECORREMOS AS COLUMNAS E AGREGAMOS OS DATOS AO PRIMEIRO ELEMENTO DA LISTA
				#ATA QUE ENCONTRAMOS UN NUMERO.
				if not col.isdigit():
					l_servicio_pid[0] += col
				else:
					#ENGADIMOS O NUMERO AO PID E DEIXAMOS DE RECORRER O BUCLE
					l_servicio_pid[1] = col
					break
			servizo = l_servicio_pid[0]
			pid = l_servicio_pid[1]
			#DICT: PID => NOME SERVIZO
			if pid.isdigit():
				dict_servizos_pid[pid] = servizo
	return dict_servizos_pid

def netstat_conexions():
	#IPs DA MAQUINA
	IPS = socket.gethostbyname_ex(socket.gethostname())[2]
	IPS.append("127.0.0.1")
	IPS.append("0.0.0.0")
	#COMANDO PARA VER AS CONEXIONS ACTIVAS
	os_portos_usados = os.popen("netstat -oan").read().split("\n")
	#DICT COAS PIDs E OS SERVIZOS
	dict_servizos_pid = servizos_pid()
	#SERVIZOS A ESCOITA
	LISTENING = {}
	#CONEXIONS ESTABLECIDAS
	ESTABLISHED = {}
	
	for info_porto in os_portos_usados:
		#SEPARAMOS OS DATOS DE CADA LINHA DE 'info_porto'
		l_info_porto = info_porto.split()
		if len(l_info_porto) == 5:
			#SE O PID SE CORRESPONDE A UN SERVICIO
			pid = l_info_porto[4]
			if pid in dict_servizos_pid:
				#EXTRAEMOS O NOME DO PROTOCOLO E O NOME DO SERVIZO
				estado = l_info_porto[3]
				protocolo = l_info_porto[0]
				nome_servicio = dict_servizos_pid[pid]
				ip_puerto_local = l_info_porto[1]
				ip_puerto_remota = l_info_porto[2]
				re_ip_puerto = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"
				#SEPARAMOS OS SERVIZOS A ESCOITA DAS CONEXIÓNS ESTABLECIDAS
				#SERVIZOS A ESCOITA
				if estado == "LISTENING":
					if re.findall(re_ip_puerto,ip_puerto_local) and re.findall(re_ip_puerto,ip_puerto_local):
						conexion = {"protocolo":protocolo,"local":ip_puerto_local,"conectado":[]}
						if not l_info_porto[4] in LISTENING:
							LISTENING[pid] = {"servizo":nome_servicio,"conexions":[]}
							LISTENING[pid]["conexions"].append(conexion)
						elif not [protocolo,ip_puerto_local] in LISTENING[pid]["conexions"]:
							LISTENING[pid]["conexions"].append(conexion)
				else:
				#CONEXIONS
					if re.findall(re_ip_puerto,ip_puerto_local) and re.findall(re_ip_puerto,ip_puerto_local):
						conexion = {"protocolo":protocolo,"estado":estado,"local":ip_puerto_local,"remota":ip_puerto_remota}
						lista_escoitando = [x["conexions"] for x in LISTENING.values()]
						conexion_entrante = False
						for listen in lista_escoitando:
							for ip in listen:
								if ip_puerto_local.split(":")[0] in IPS and ip_puerto_local.split(":")[1] == ip["local"].split(":")[1]:
									ip["conectado"].append(ip_puerto_remota)
									conexion_entrante = True
						if not conexion_entrante:
							if not pid in ESTABLISHED:
								ESTABLISHED[pid] = {"servizo":nome_servicio,"estado":estado,"conexions":[]}
								ESTABLISHED[pid]["conexions"].append(conexion)
							elif not [protocolo,ip_puerto_local,ip_puerto_remota] in ESTABLISHED[pid]["conexions"]:
								ESTABLISHED[pid]["conexions"].append(conexion)
	os.system("cls")
	print "LISTENING"
	print ":::::::::::::"
	for x in LISTENING:
		print "pid: "+str(x)+" "+str(LISTENING[x]["servizo"])
		for i in LISTENING[x]["conexions"]:
			print "\t"+i["protocolo"]+" "+"local: "+i["local"]
			for u in i["conectado"]:
				print "\t\t>> conexion dende: "+str(u)
	print ""
	print "ESTABLISHED"
	print ":::::::::::::"
	for x in ESTABLISHED:
		print "pid: "+str(x)+" "+str(ESTABLISHED[x]["servizo"])
		for i in ESTABLISHED[x]["conexions"]:
			print "\t"+i["protocolo"]+" "+i["estado"]+" "+"local: "+i["local"]+", "+"remota: "+i["remota"]

while True:
	netstat_conexions()
	time.sleep(1)
	
	
	
	


