# -*- coding: utf-8 -*-

#SOLO FUNCIONA EN WINDOWS

import os
import re
import socket
import time

if os.name == "posix":
	print "Lanzar programa como superusuario"

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
	if os.name == "nt":
		os_portos_usados = os.popen("netstat -oan").read().split("\n")
	else:
		os_netstat = os.popen("sudo netstat -anptu").read().split("\n")
		os_portos_usados = []
		dict_servizos_pid = {}
		for line in os_netstat[2:]:
			line_s = line.split()
			line_s = [x for x in line_s if len(x)>1 and not x.isdigit()]
			if len(line_s) > 3:
				if len(line_s) == 4:
					if len(line_s[3].split("/")) > 1:
						serv_name_s = line_s[3].split("/")[1]
						pid_s = line_s[3].split("/")[0]
					else:
						serv_name_s = "none"
						pid_s = "none"
					os_portos_usados.append("\t".join(
							line_s[:3]+["NONE"]+[pid_s]))
				else:
					if len(line_s[4].split("/")) > 1:
						serv_name_s = line_s[4].split("/")[1]
						pid_s = line_s[4].split("/")[0]
					else:
						print "coas:",line_s
						serv_name_s = "none"
						pid_s = "none"
					line_final = line_s[:4]+[pid_s]
					if len(line_final) == 5 and line_final[4].isdigit(): 
						dict_servizos_pid[pid_s] = serv_name_s
						os_portos_usados.append("\t".join(line_final))
	#DICT COAS PIDs E OS SERVIZOS
	if os.name == "nt":
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
				if estado in ["LISTENING","ESCUCHAR"]:
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
									ip["conectado"].append([ip_puerto_remota, estado])
									conexion_entrante = True
						if not conexion_entrante:
							if not pid in ESTABLISHED:
								ESTABLISHED[pid] = {"servizo":nome_servicio,"estado":estado,"conexions":[]}
								ESTABLISHED[pid]["conexions"].append(conexion)
							elif not [protocolo,ip_puerto_local,ip_puerto_remota] in ESTABLISHED[pid]["conexions"]:
								ESTABLISHED[pid]["conexions"].append(conexion)
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")
	print "LISTENING"
	print ":::::::::::::"
	for x in LISTENING:
		print "pid: "+str(x)+" "+str(LISTENING[x]["servizo"])
		for i in LISTENING[x]["conexions"]:
			print "\t"+i["protocolo"]+" "+"local: "+i["local"]
			for u in i["conectado"]:
				if u[1] in ["ESTABLISHED", "ESTABLECIDO"]:
					ip_remota = u[0].split(":")[0]
					if ip_remota in ["127.0.0.1","0.0.0.0"]:
						servizo_conectando = False
						for s in ESTABLISHED.values():
							if i["local"] in [x["remota"] for x in s["conexions"]]:
								servizo_conectando = s["servizo"]
						if servizo_conectando:
							print "\t\t>> conexion dende: "+str(u[0])+", servizo: "+str(servizo_conectando)
						else:
							print "\t\t>> conexion dende: "+str(u[0])
					else:
						print "\t\t>> conexion dende: "+str(u[0])
	print ""
	print "ESTABLISHED"
	print ":::::::::::::"
	for j in ESTABLISHED:
		if ("ESTABLISHED" or "ESTABLECIDO" in 
				[x["estado"] for x in ESTABLISHED[j]["conexions"]]):
			print "pid: "+str(j)+" "+str(ESTABLISHED[j]["servizo"])
			for i in ESTABLISHED[j]["conexions"]:
				if i["estado"] in ["ESTABLISHED","ESTABLECIDO"]:
					ip_remota = i["remota"].split(":")[0]
					if ip_remota in ["127.0.0.1", "0.0.0.0"]:
						servizo_remoto = False
						for s in LISTENING.values():
							if i["remota"] in [x["local"] for x in s["conexions"]]:
								servizo_remoto = s["servizo"]
						if servizo_remoto:
							print ("\t"+i["protocolo"]+" "+i["estado"]+" "+"local: "+i["local"]+", "+
									"remota: "+i["remota"]+", "+"conectando a: "+servizo_remoto)
						else:
							print "\t"+i["protocolo"]+" "+i["estado"]+" "+"local: "+i["local"]+", "+"remota: "+i["remota"]
					else:
						print "\t"+i["protocolo"]+" "+i["estado"]+" "+"local: "+i["local"]+", "+"remota: "+i["remota"]

while True:
	netstat_conexions()
	print ""
	try:
		raw_input("PULSA 'ENTER' PARA REFRESCAR")
	except:
		print
		break
	
	
	
	


