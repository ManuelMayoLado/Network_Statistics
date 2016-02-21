# -*- coding: utf-8 -*-

#SOLO FUNCIONA EN WINDOWS

import os

os_servizos_pid = os.popen("tasklist").read().split("\n")
os_portos_usados = os.popen("netstat -oan").read().split("\n")

def servizos_pid():

	dict_servizos_pid = {}
	
	for servizo in os_servizos_pid:
		l_servizo = servizo.split()
		l_servicio_pid = ["",""]
		if len(l_servizo) > 2:
			for col in l_servizo:
				if not col.isdigit():
					l_servicio_pid[0] += col
				else:
					l_servicio_pid[1] = col
					break
			pid = l_servicio_pid[1]
			servizo = l_servicio_pid[0]
			if pid.isdigit():
				dict_servizos_pid[pid] = servizo
		
	return dict_servizos_pid

def netstat_conexions():

	dict_servizos_pid = servizos_pid()
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
	

def show_netstat_info():

	for info_porto in netstat_conexions():
		print info_porto
		
def html_netstat_info(abrir=0):

	import webbrowser
	from re import findall

	html_document = open("tabla_info_portos.html","w")

	tags_apertura = "<html>\n<head>\n<title>info netstat</title>\n</head>\n"
	tags_style = "<style>\ntable {border-collapse: collapse;}\ntd {padding: 5px;}\n</style>\n"
	tags_body = "<body>\n"
	tags_tabla_cabecera_con = ("<table border=1 bgcolor=#F8F8F8>\n"+
							"<tr bgcolor='lightblue' style='font-weight:bold'>\n<td>Protocolo</td>"+
							"<td>Direcci&oacute;n local</td><td>Direcci&oacute;n remota</td>"+
							"<td>PID</td><td>Servizo</td><td>Estado</td>\n</tr>\n")
	tags_tabla_cabezera_ser = ("<table border=1 bgcolor=#F8F8F8>\n"+
							"<tr bgcolor='lightblue' style='font-weight:bold'>\n<td>Servicio</td>"+
							"<td>N&uacutemero Conexi&oacutens</td><td>PIDS</td></tr>\n")
	tags_final = "</body>\n</html>"
	
	html_document.write(tags_apertura)
	html_document.write(tags_style)
	html_document.write(tags_body)
	html_document.write(tags_tabla_cabecera_con)
	
	for info_porto in netstat_conexions():
		local_ip,local_port = findall("(.+):(.+)$",info_porto["local"])[0]
		remota_ip,remota_port = findall("(.+):(.+)$",info_porto["remota"])[0]
		color_estado = "#F8F8F8"
		if "estado" in info_porto:
			if info_porto["estado"] == "LISTENING":
				color_estado = '#F6F7E2'
			if info_porto["estado"] == "ESTABLISHED":
				color_estado = '#D5EBD4'
			if info_porto["estado"] == "TIME_WAIT":
				color_estado = "#E5DDBC"
			if info_porto["estado"] == "CLOSE_WAIT":
				color_estado = "#F3DDCD"
		color_remota = "#F8F8F8"
		if findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",remota_ip) and remota_ip not in ["0.0.0.0","127.0.0.1"]:
			color_remota = "#FCEBE0"
		#TABLA CONEXIÓNS
		html_document.write("<tr><td>"+info_porto["protocolo"]+"</td>"+
			"<td>"+local_ip+":"+"<font color=brown>"+local_port+"</font></td>"+
			"<td bgcolor="+color_remota+">"+remota_ip+":"+"<font color=brown>"+remota_port+"</font></td>"+
			"<td>"+info_porto["pid"]+"</td>"+
			"<td>"+ (info_porto["servizo"] if "servizo" in info_porto else " ") +"</td>"+
			"<td bgcolor="+color_estado+">"+ (info_porto["estado"] if "estado" in info_porto else " ") +"</td>"+
			"</tr>\n")
			
	html_document.write("</table>")
	html_document.write("\n<br/>")
	
	#TABLA SERVICIOS
	html_document.write(tags_tabla_cabezera_ser)
	for servicio in num_servizos():
		html_document.write("<tr><td>"+servicio["nome"]+"</td>"+
			"<td>"+str(servicio["num"])+"</td>"+
			"<td>"+", ".join(map(str,servicio["pids"]))+"</td></tr>\n")
	
	html_document.write("</table>")
	html_document.write("\n<br/>")
	
	html_document.close()
	
	if abrir:
		webbrowser.open("tabla_info_portos.html")
		
def matar_servicio(pid):
	os.system("TASKKILL /PID "+str(pid))

	
html_netstat_info(1)
	
	
	
	


