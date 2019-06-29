#!/usr/bin/en python
import time
import telnetlib
import sys, os
import re # module for regex
from netaddr import IPNetwork
import socket # need for resolving IP hostname
import subprocess
import sqlite3
def telnetDLink(host):
        tn = telnetlib.Telnet(host)
        e= tn.read_until("Username:")
        tn.write("you_login\r")
        d = tn.read_until("Password:")
        tn.write("you_pass\r")
        e= tn.read_until("Username:")
        tn.write("you_login\r")
        tn.write("you_pass\r")
        return tn
def telnetCiscoWS(host):
        tn = telnetlib.Telnet(host)
        tn.read_until("Username:")
        tn.write("you_login\r")
        tn.read_until("Password:")
        tn.write("you_pass\r")
        tn.read_until(">")
        tn.write("enable\r")
        tn.read_until("Password:")
        tn.write("you_pass\r")
        return tn
def telnetExtreme(host):
        tn = telnetlib.Telnet(host)
        tn.read_until("login:")
        tn.write("you_login\r")
        tn.read_until("password:")
        tn.write("you_pass\r")
        return tn
def telnet(host):
        tn = telnetlib.Telnet(host)
        tn.read_until("login:")
        tn.write("you_login\r")
        tn.read_until("Password:")
        tn.write("you_pass\r")
        tn.write("enable\r")
        i = 1
        try:
                tn.read_until("Password:",0.5)
        except Exception:
                i = 0
        if i <> 0:
                tn.write("publik_pass_enable\r")
        return tn
def telnetAsotel(host):
        tn = telnetlib.Telnet(host)
        tn.write("\r")
        tn.read_until("Username:")
        tn.write("admin\r")
        tn.read_until("Password:")
        tn.write("publik_pass\r")
        return tn

def telnet6008(host):
        tn = telnetlib.Telnet(host)
        tn.read_until("login:")
        tn.write("admin\r")
        tn.read_until("password:")
        tn.write("publik_pass\r")
        return tn
def telnetDELL(host):
        tn = telnetlib.Telnet(host)
        tn.read_until("User Name:")
        tn.write("you_login\r")
        tn.read_until("Password:")
        tn.write("you_pass\r")
        tn.write("enable\r")
        i = 1
        try:
                tn.read_until("Password:",0.5)
        except Exception:
                i = 0
        if i <> 0:
                tn.write("publik_pass_enable\r")
        tn.write("enable\r")
        i = 1
        try:
                tn.read_until("Password:",0.5)
        except Exception:
                i = 0
        if i <> 0:
                tn.write("publik_pass_enable\r")

        return tn
def telnetCOM(host):
        tn = telnetlib.Telnet(host)
        e= tn.read_until("Login:")
        tn.write("you_login\r")
        d = tn.read_until("Password:")
        tn.write("you_pass\r")
        return tn



def getmac(s):
	w = ''
	li = []
	for i in s:
        	if i == '-' or i == '.' or i == ':' or  i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9' or i == '0' or i == 'a' or i == 'b' or i == 'c' or i == 'd' or i == 'e' or i == 'f' or i == 'A' or i == 'B' or i == 'C' or i == 'D' or i == 'E' or i == 'F':
			if i == '-' or i == '.' or i == ':':
				w = w
			else:
				 w = w + i
                	if len(w) == 12:
				if w == "FFFFFFFFFFFF" or w.find("2012") >= 0 or w.find("2013") >= 0 or w.find("2014") >= 0 or w.find("2015") >= 0 or w.find("2016") >= 0 or w.find("2011") >= 0 or w.find("2010") >= 0 or w.find("2009") >= 0 or w.find("2008") >= 0:
					w = ""
                        	else:
					w ='-'.join(w[i:i+2] for i in range(0, len(w), 2))
					li.append(w)
                        	w = ''
        	else:
                	w = ""
	return(li)


def S6224(vlanid,tn):
	stop =  tn.read_until("#",0.2)
	tn.write("show vlan id " + vlanid + " \r")
	show_vlan_id = tn.read_until(stop,1.5)
#	index_l = show_vlan_id.index("Ethernet")
#	nomer_porta = show_vlan_id[index_l + 8: index_l + 15]
	s1 = show_vlan_id.split(" ")
	i = 0
	while i < len(s1):
		s2 = s1[i]
		index = s2.find("thernet")
		if index == -1 :
			del s1[i]
		else:
			index1 = s2.find("(T)")
			if index1 == -1:
				i = i + 1
			else :
				del s1[i]
	if len(s1) == 1:	
		s1 = s1[0]
		index = s1.index("net")
		nomer_porta = s1[index + 3:]
		tn.write("show interface ethernet status | include  " + nomer_porta + " \r")
		w = tn.read_until(stop,1.5)
		q = w.index(nomer_porta)
		w = w[q:q+60]
		try:
			status_porta = w.index(" DOWN/DOWN ")
			status_porta = "DOWN"
		except Exception:
			status_porta = "UP"
#	index_w = w.index(nomer_porta)
#	status_porta = w[index_w + 23: index_w + 32]
		tn.write("show mac-address-table interface ethernet " + nomer_porta + " \r")
		b = tn.read_until(stop,4)
		mac_addres = getmac(b)
#        try:
#	   index_b = b.index(vlanid)
#        except Exception:
#           index_b = 0
#        if index_b <> 0 :
#	   mac_addres = b[index_b + 5: index_b + 22]
#	else:
#	   mac_addres = "no mac addres"
		if len(mac_addres) > 1:
			port = "||port||" + nomer_porta + "glup||"
		else:
			port = "||port||" + nomer_porta + "||"
		port_state = "||port state||" + status_porta + "||"
		mac = "||mac||" + ' '.join(mac_addres)+ "||"
	elif   len(s1) == 0:
			port = "||port||no vlan on untagget ports||"
			port_state = "||port state|| - ||"
			mac = "||mac||hz||"
	else:
			port = "||port|| many untagget ports for this vlans ||"
			port_state = "||port state|| - ||"
			mac = "||mac||hz||"
	return (port, port_state, mac)
def PC3324(vlanid,tn):
        stop =  tn.read_until("#",3)
	index_stop = stop.index('#')
	stop = stop[index_stop -3: index_stop]
        qa =tn.write("show vlan tag " + vlanid + " \r")
	PORT =  tn.read_until(stop,3)
	try:
		index_port = PORT.index(',')
	except:
		index_port = PORT.index('-')
	port = PORT[index_port - 5: index_port]
	port = port.replace('(','')
	tn.write("show interfaces status ethernet " + port + " \r")
	STATUS_PORTA =  tn.read_until(stop,3)
	index_status_porta = STATUS_PORTA.index('Mode')
	port_state = STATUS_PORTA[index_status_porta + 135: index_status_porta + 140]
	tn.write("show bridge address-table ethernet " + port + " \r")
	b = tn.read_until(stop,4)
	try:
		index_b = b.index(vlanid)
        except Exception:
        	index_b = 0
	if index_b <> 0 :
                mac_addres = getmac(b)
#		mac_addres = b[index_b + 9: index_b + 26]
	else:
		mac_addres = "no mac addres"
	port_state = "||port state||{}||".format(port_state)

	mac = "||mac||" + ' '.join(mac_addres)+ "||"
#        mac = "||mac||{}||".format(.join(mac_addres))
	port = '||port||{}||'.format(port)
        return (port, port_state, mac)
def Extreme(vlanid,tn):
        tn.read_until("#",2)
	stop = "#"
        tn.write("show vlan v?\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t")
	VLAN = tn.read_until(stop,4)
	VLAN = VLAN.split()
	for x in VLAN:
		if x.find(vlanid) >= 0:
			vlan_name = x
			break
			
#	try:
#		q = tn.read_until(stop,4)
#		q1 = q.index(vlanid)
#		q2 = q[q1-10:q1+10]
#		index_vlan_left = q2.index(" ")
#		index_vlan_right = q2.rindex(" ")
#		vlan_name = q2[index_vlan_left: index_vlan_right]
	vlan_name = vlan_name.replace("\r","")
	vlan_name = vlan_name.replace("\n","")
	vlan_name = vlan_name.replace('"',"")
	vlan_name = vlan_name.replace(',',"")
#	except Exception:
#		print 'chto-to ne to'
	tn.write("              \r")
	VLAN = "show vlan " + vlan_name + "\r"
	tn.write(VLAN)
	PORT = tn.read_until("hui",1)
	q = PORT.index("Untag:")
	q1 = PORT.index("(",q)
	port = PORT[q + 6:q1].strip()
	port = port.replace("*","")
	tn.write("show ports " + port + " configuration \r")
	tn.write(chr(27))
	PORT_STATE = tn.read_until(stop,2)
	try:
		port_state = PORT_STATE.index(" R ")
		port_state = "DOWN"
	except Exception:
		port_state = "UP"
	tn.write("show fdb ports " + port + " \r")
	MAC = tn.read_until("hui",2)
	mac = getmac(MAC)
	port = '||port||{}||'.format(port)
	port_state = '||port state||{}||'.format(port_state)
	mac  = '||mac on port||{}||'.format(" ".join(mac))
	return (port, port_state, mac)
def S6008(vlanid,tn):
	stop = "Switch>"
	tn.read_until(stop,4)
        tn.write("show vlan " + vlanid + "\r")
	PORT = tn.read_until(stop,4)
	q = PORT.index("port")
	port = PORT[q+5:q+7]
        tn.write("show port state \r")
	PORT_STATE = tn.read_until(stop,4)
	index = "Port " + port
        q = PORT_STATE.index(index)
	PORT_STATE = PORT_STATE[q:q+50]
	try:
		port_state = PORT_STATE.index(" Down ")
		port_state = "DOWN"
	except Exception:
		port_state = "UP"
        tn.write("show port mac-learning " + port + "\r")
        tn.write("                                                                                       "*8)
        MAC = tn.read_until(stop,4)
	mac = getmac(MAC)
	port = '||port||{}||'.format(port)
	port_state = '||port state||{}||'.format(port_state)
	mac  = '||mac on port||{}||'.format(mac)
	return (port, port_state, mac)
def CISCO(vlanid,tn):
	stop =  "#"
	tn.read_until(stop,4)
	tn.write("show vlan id " + vlanid + " \r")
	show_vlan_id = tn.read_until(stop,4)
	s1 = show_vlan_id.split()
	i = 0
	while i < len(s1):
		s2 = s1[i]
		index = s2.find("Fa")
		if index == -1 :
			del s1[i]
		else:
			i = i + 1
	if len(s1) == 1:	
		nomer_porta = s1[0]
		tn.write("show interface status | include  " + nomer_porta + " \r")
		w = tn.read_until(stop,1.5)
		try:
			status_porta = w.index(" notconnect ")
			status_porta = "DOWN"
		except Exception:
			status_porta = "UP"
		tn.write("show mac-address-table interface " + nomer_porta + " \r")
		b = tn.read_until(stop,4)
		mac_addres = getmac(b)
		if len(mac_addres) > 1:
			port = "||port||" + nomer_porta + "glup||"
		else:
			port = "||port||" + nomer_porta + "||"
		port_state = "||port state||" + status_porta + "||"
		mac = "||mac||" + ' '.join(mac_addres)+ "||"
	elif   len(s1) == 0:
			port = "||port||no vlan on untagget ports||"
			port_state = "||port state|| - ||"
			mac = "||mac||hz||"
	else:
			port = "||port|| many untagget ports for this vlans ||"
			port_state = "||port state|| - ||"
			mac = "||mac||hz||"
	return (port, port_state, mac)
def Asotel(vlanid,tn):
	stop =  ">"
	model = tn.read_until(stop,3)
	print model
	if model.find("Vector 1908G2>") <> -1:
		tn.write("show 1qvlan" + " \r")
		G2 = tn.read_until(stop,3)
		index = G2.find("[Port List]")
		G2 = G2[index:]
		G2 = G2.split("\n")
		G2 = filter(lambda x:x.find(vlanid)>=0,G2)
		G2 = "".join(G2)
		G2 = G2.split()
		G2 = filter(lambda x:x.find("[U")>=0,G2)
		G2 = "".join(G2)
		G2 = G2.split("[U")
		G2 = [x for x in G2 if x]
		if len(G2) == 1:
			port = "".join(G2)
			tn.write("show port \r\n")
			show_port = tn.read_until(stop,3)
			show_port = show_port.split("\r\n")
			show_port = [x for x in show_port if x.find("  " + port + "  ",0,28) >=0]
			show_port = "\n".join(show_port)
			index = show_port.find("DOWN")
			if index == -1:
				port_state = "||link sw|| + ||"
			else:
				port_state = "||link sw|| - ||"
			tn.write("show arl dynamic" + " \r\r\r\r\r\r\r\r")
			show_dynamic = tn.read_until(stop,3)
			show_dynamic = show_dynamic.split("\r")
			show_dynamic = [x for x in show_dynamic if x.find(" " + port + " ", 20) >=0]
			show_dynamic = " ".join(show_dynamic)
			mac = getmac(show_dynamic)
			mac = "||mac||" + "".join(mac) + "||"
                        port = "||port|| " + "".join(port) + " ||"

		else:
			mac = "||mac||||"
			port_state = "||link sw||hz||"
			port = "||port|| many untagget ports for this vlan||"

	else:
		if model.find("Vector 1908>") <> -1: 
			tn.write("show 1qvlan pvid" + " \r")
		elif model.find("10-port Switch>"):
			tn.write("show 1qvlan port" + " \r")
		show_vlan_id = tn.read_until(stop,3)
		vlan = show_vlan_id.split("\r\n")
		i = 0
		while i < len(vlan):
			s2 = vlan[i]
			index = s2.find(vlanid)
			if index == -1 :
				del vlan[i]
			else:
				i = i + 1
		if len(vlan) == 1 :
			vlan =	"".join(vlan)
			vlan_id = vlan.split()
			port = vlan_id[0]
			tn.write("show port" + " \r")
			show_port = tn.read_until(stop,3)
			show_port = show_port.split("\r")
			i = 0
			while i < len(show_port):
				s2 = show_port[i]
				index = s2.find("  " + port + "  ")
				if index == -1 :
					del show_port[i]
				else:
					i = i + 1
			show_port = "\n".join(show_port)
			index = show_port.find("DOWN")
			if index == -1:
				port_state = "||link sw|| + ||"
			else:
				port_state = "||link sw|| - ||"

			if model.find("Vector 1908>") <> -1: 
				tn.write("show dynamic" + " \r")
			elif model.find("10-port Switch>"):
				tn.write("show arl dynamic" + " \r\r\r\r\r\r\r\r")
			show_dynamic = tn.read_until(stop,3)
			show_dynamic = show_dynamic.split("\r")
			i = 0
			while i < len(show_dynamic):
				s2 = show_dynamic[i]
				index = s2.find("  " + port + "  ")
				if index == -1 :
					del show_dynamic[i]
				else:
					i = i + 1
			show_dynamic = "\n".join(show_dynamic)
			mac = getmac(show_dynamic)
			mac = " ".join(mac)
			mac = "||mac||" + mac + "||"
			port = "||port|| " + port + " ||"
		else:
			mac = "||mac||||"
			port_state = "||link sw||hz||"
			port = "||port|| many untagget ports for this vlan||"

	return (port, port_state, mac)
def DLink(vlanid,tn):
	stop =  "#"
	W = tn.read_until(stop,4)
	tn.write("show vlan vlanid " + vlanid + " \r")
	show_vlan_id = tn.read_until(stop,7)
	show_vlan_id = show_vlan_id[show_vlan_id.index("Static Untagged ports  :") + 24:show_vlan_id.index("Static Untagged ports  :") + 32].split()
	if len(show_vlan_id) == 1 :
		port = "".join(show_vlan_id)
		tn.write("show ports " + port + "\r")
                tn.write("q")
		show_port = tn.read_until(stop,4)
		port_state = "Down" if  show_port.find("LinkDown") >= 0 else "UP"
		tn.write("show fdb port " + port + "\r")
		show_fdb = tn.read_until(stop,4)
		mac = getmac(show_fdb) 
		mac = "||mac||" + " ".join(mac) + "||"
		port = "||port|| {} ||".format(port)
		port_state = "||link sw|| {} ||".format(port_state)
	else:
		mac = "||mac||||"
		port = "||port|| ||"
		port_state = "||link sw|| ||"
		
	return (port, port_state, mac)
def ExtremeS48i(vlanid,tn):
	stop =  "#"
	W = tn.read_until(stop,4)
	tn.write("show vlan v" + vlanid + " \r")
	PORT = tn.read_until(stop,7)
	q = PORT.index("Untag:")
	q1 = PORT.index("(",q)
	port = PORT[q + 6:q1].strip()
	port = port.replace("*","")
	tn.write("show ports " + port + " configuration \r")
	tn.write(chr(27))
	PORT_STATE = tn.read_until(stop,2)
	try:
		port_state = PORT_STATE.index(" READY ")
		port_state = "DOWN"
	except Exception:
		port_state = "UP"
	tn.write("show fdb ports " + port + " \r")
	MAC = tn.read_until("hui",2)
	mac = getmac(MAC)
	port = '||port||{}||'.format(port)
	port_state = '||port state||{}||'.format(port_state)
	mac  = '||mac on port||{}||'.format(" ".join(mac))
	return (port, port_state, mac)

def com2128(vlanid,tn): 
        stop =  "#"
        tn.read_until(stop,4)
        tn.write("show vlan " + vlanid + " \r")
        port = tn.read_until(stop,7)
        try:
                port = port.split()[17]
        except:
                return("||port||no vlan in SW||","||port state||xz||","||mac||xz||")
        try:
                int(port)
        except:
                return("||port||xz||","||port state||xz||","||mac||xz||")
        tn.write("show interface port " + port + " \r")
        port_state = tn.read_until(stop,7)
        port_state = port_state.split()[25]
        if port_state.find("up") <> -1:
                tn.write("show mac-address-table l2-address port " + port + " \r")
        else:
                return("||port||{}||".format(port),"||port state||down||","||mac|| - ||")
        mac_str = tn.read_until(stop,7)
        mac = " ".join(getmac(mac_str))
        return("||port|| {} ||".format(port),"||port state||{}||".format(port_state),"||mac||{}||".format(mac))
