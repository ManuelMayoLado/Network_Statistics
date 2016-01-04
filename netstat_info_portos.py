# -*- coding: utf-8 -*-

#SOLO FUNCIONA EN WINDOWS

import os

os_servizos_pid = os.popen("tasklist").read().split("\n")
os_portos_usados = os.popen("netstat -oan").read().split("\n")

def servizos_pid():

	dict_servizos_pid = {}
	
	for servizo in os_servizos_pid:
		l_servizo = servizo.split()
		if len(l_servizo) > 2 and l_servizo[1].isdigit():
			dict_servizos_pid[l_servizo[1]] = l_servizo[0]
			
	return dict_servizos_pid

def netstat_servicios():

	dict_servizos_pid = servizos_pid()
	netstat_servicios = []
	
	for info_porto in os_portos_usados:
		l_info_porto = info_porto.split()
		if len(l_info_porto) == 5:
			if l_info_porto[4] in dict_servizos_pid:
				netstat_servicios.append({
					"protocolo":l_info_porto[0],"local":l_info_porto[1],
					"remota":l_info_porto[2],"estado":l_info_porto[3],"pid":l_info_porto[4],
					"servizo":dict_servizos_pid[l_info_porto[4]]})
			else:
				netstat_servicios.append({
					"protocolo":l_info_porto[0],"local":l_info_porto[1],
					"remota":l_info_porto[2],"estado":l_info_porto[3],"pid":l_info_porto[4]})
					
		elif len(l_info_porto) == 4:
			if l_info_porto[3] in dict_servizos_pid:
				netstat_servicios.append({
						"protocolo":l_info_porto[0],"local":l_info_porto[1],
						"remota":l_info_porto[2],"pid":l_info_porto[3],
						"servizo":dict_servizos_pid[l_info_porto[3]]})
			else:
				netstat_servicios.append({
						"protocolo":l_info_porto[0],"local":l_info_porto[1],
						"remota":l_info_porto[2],"pid":l_info_porto[3]})
						
	return netstat_servicios

def show_netstat_info():

	for info_porto in netstat_servicios():
		print info_porto
		
def html_netstat_info(abrir=0):

	import webbrowser
	from re import findall

	html_document = open("tabla_info_portos.html","w")

	tags_apertura = "<html>\n<head>\n<title>info netstat</title>\n</head>\n"
	tags_style = "<style>\ntable {border-collapse: collapse;}\ntd {padding: 5px;}\n</style>\n"
	tags_body = "<body>\n<table border=1 bgcolor='#F8F8F8'>\n"
	tags_tabla_cabecera = ("<tr bgcolor='lightblue' style='font-weight:bold'>\n<td>Protocolo</td>"+
							"<td>Direcci&oacute;n local</td><td>Direcci&oacute;n remota</td>"+
							"<td>PID</td><td>Servizo</td><td>Estado</td>\n</tr>\n")
	tags_final = "</body>\n</html>"
	
	html_document.write(tags_apertura)
	html_document.write(tags_style)
	html_document.write(tags_body)
	html_document.write(tags_tabla_cabecera)
	
	for info_porto in netstat_servicios():
		local_ip,local_port = findall("(.+):(.+)$",info_porto["local"])[0]
		remota_ip,remota_port = findall("(.+):(.+)$",info_porto["remota"])[0]
		html_document.write("<tr><td>"+info_porto["protocolo"]+"</td>"+
			"<td>"+local_ip+":"+"<font color=brown>"+local_port+"</font></td>"+
			"<td>"+remota_ip+":"+"<font color=brown>"+remota_port+"</font></td>"+
			"<td>"+info_porto["pid"]+"</td>"+
			"<td>"+ (info_porto["servizo"] if "servizo" in info_porto else " ") +"</td>"+
			"<td>"+ (info_porto["estado"] if "estado" in info_porto else " ") +"</td>"+
			"</tr>\n")
					
	html_document.write("</table>")
	
	html_document.close()
	
	if abrir:
		webbrowser.open("tabla_info_portos.html")
		

html_netstat_info(1)
	
	
	
	
	


