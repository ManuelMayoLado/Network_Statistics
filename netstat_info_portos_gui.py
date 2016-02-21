# -*- coding: utf-8 -*-

#SOLO FUNCIONA EN WINDOWS

import os
import Tkinter

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
	#COMANDO PARA VER AS CONEXIONS ACTIVAS
	os_portos_usados = os.popen("netstat -oan").read().split("\n")
	#DICT COAS PIDs E OS SERVIZOS
	dict_servizos_pid = servizos_pid()
	#SERVIZOS A ESCOITA
	LISTENING = {}
	#CONEXIONS ESTABLECIDAS
	ESTABLISHED = {}
	
	netstat_servizos = []
	
	for info_porto in os_portos_usados:
		l_info_porto = info_porto.split()
		if len(l_info_porto) == 5:
			if l_info_porto[4] in dict_servizos_pid:
				netstat_servizos.append({
					"protocolo":l_info_porto[0],"local":l_info_porto[1],
					"remota":l_info_porto[2],"estado":l_info_porto[3],"pid":l_info_porto[4],
					"servizo":dict_servizos_pid[l_info_porto[4]]})
			else:
				netstat_servizos.append({
					"protocolo":l_info_porto[0],"local":l_info_porto[1],
					"remota":l_info_porto[2],"estado":l_info_porto[3],"pid":l_info_porto[4]})
					
		elif len(l_info_porto) == 4:
			if l_info_porto[3] in dict_servizos_pid:
				netstat_servizos.append({
						"protocolo":l_info_porto[0],"local":l_info_porto[1],
						"remota":l_info_porto[2],"pid":l_info_porto[3],
						"servizo":dict_servizos_pid[l_info_porto[3]]})
			else:
				netstat_servizos.append({
						"protocolo":l_info_porto[0],"local":l_info_porto[1],
						"remota":l_info_porto[2],"pid":l_info_porto[3]})
						
	return netstat_servizos
	
print netstat_conexions()
	
def num_servizos():

	lista_info_servizos = []
	dict_num_servizos = {}
	
	netstat_conexions_var = netstat_conexions()
	
	for conect in netstat_conexions_var:
		if "servizo" in conect:
			if conect["servizo"] in dict_num_servizos:
				dict_num_servizos[conect["servizo"]] += 1
			else:
				dict_num_servizos[conect["servizo"]] = 1
	
	for servizo in dict_num_servizos:
		dict_info_servizo = {"nome":servizo,
							"num":dict_num_servizos[servizo],"pids":[]}
		for conect in netstat_conexions_var:
			if "servizo" in conect:
				if conect["servizo"] == servizo and not conect["pid"] in dict_info_servizo["pids"]:
					dict_info_servizo["pids"].append(conect["pid"])
		lista_info_servizos.append(dict_info_servizo)
	
	return lista_info_servizos

def matar_servicio(pid):
	os.system("taskkill /pid "+str(pid))
	
	
	
	


