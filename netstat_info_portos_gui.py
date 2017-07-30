# -*- coding: utf-8 -*-

#SOLO FUNCIONA EN WINDOWS

import os
import re
import socket
import time
from Tkinter import *
from ttk import *


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
								
	return LISTENING
	
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

			
TAMANHO_VENTANA = [400,300]

class App():
	def __init__(self):
		self.root = Tk()
		self.root.resizable(width=True, height=True)
		self.root.minsize(TAMANHO_VENTANA[0],TAMANHO_VENTANA[1])
		Label(self.root, text="LISTENING", background="white", width=100, relief="groove").grid(row=1, column=1, pady=5, padx=5, sticky="we")
		
		columnas_listening = ["PID","APP","N_Process"]
		self.treeview_listening = Treeview(self.root,columns=columnas_listening,show="headings",height=12)
		for c in columnas_listening:
			self.treeview_listening.heading(c,text=c)
			self.treeview_listening.column(c,width=150)
			self.treeview_listening.column(c,minwidth=50)
		
		self.treeview_listening.grid(row=2, column=1, pady=5, padx=5, sticky="we")
		
		listening=netstat_conexions()
		
		for x in listening:
			pid=x
			app=listening[x]["servizo"]
			n_p=len(listening[x]["conexions"])
			self.treeview_listening.insert("","end",values=[pid,app,n_p])
		
		self.update_clock()
		self.root.mainloop()
		
	def update_clock(self):
		listening=netstat_conexions()
		
		for i in self.treeview_listening.get_children():
			old_values = self.treeview_listening.item(i)["values"]
			if not str(old_values[0]) in listening:
				self.treeview_listening.delete(i)
			else:
				lis_value = listening[str(old_values[0])]
				if lis_value["servizo"] == old_values[1] and len(lis_value["conexions"]) == old_values[2]:
					del listening[str(old_values[0])]
				else:
					pid=old_values[0]
					app=lis_value["servizo"]
					n_p=len(lis_value["conexions"])
					#revisar se se cambian así os datos
					self.treeview_listening.item(i)["values"]=[pid,app,n_p]
			
		for x in listening:
			pid=x
			app=listening[x]["servizo"]
			n_p=len(listening[x]["conexions"])
			self.treeview_listening.insert("","end",values=[pid,app,n_p])
		self.root.after(1000, self.update_clock)
		
if __name__ == "__main__":
	app = App()


