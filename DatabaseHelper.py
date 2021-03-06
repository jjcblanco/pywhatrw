# Inicializa la conexion con la BD y se asegura de que no se cierre.
# Gestiona tambien la ejecucion de queries y la construccion/armado de query's INSERT.
# Basicamente, es la funcion que va a ser el middleware entre las queries de AFIP y la BD.
import time
import mysql.connector as mysql
import sys
import re
import traceback

class DatabaseHelper():
	def __init__(self):
		self.server = "192.168.0.140"   #"192.168.2.210"
		self.database = "coins"  # "mop_bd"
		self.username = "root"   # "webbackend"
		self.password = "retsam77" # "rootmysql114!"


		if self.password is None:
			self.password = ""
		print(self.server)
		self.conn = mysql.connect(user=self.username, password=self.password, host=self.server, database=self.database)
		self.cursor = self.conn.cursor(dictionary=True)

		

	def DBQuery(self, query):
		self.cursor.execute(query)

		
		if("SELECT" not in query.upper()[:12]):
			self.conn.commit()
			return True
		else:
			result = self.cursor.fetchall()
			self.conn.commit()
			return result



	def ArreglarFecha(self, date, timestamp=''):
		if timestamp == '':
			if date == 'null' or date == '-':
				return 'null'
			listDate = date.split("/")
			return str(listDate[2]) + "/" + str(listDate[1]) + "/" + str(listDate[0])
		elif timestamp=="timestamp":
			if date == 'null' or date == '-':
				return 'null'
			fechayhora = date.split(" ")
			
			listDate = fechayhora[0].split("/")
			return str(listDate[2]) + "/" + str(listDate[1]) + "/" + str(listDate[0])+ " "+fechayhora[1]
			

	def constructorInsert(self, tabla, arrayValores):
		columnas=''
		valores=[]
		query=''
		valoresstring=''
		extension=""
		extensionquery=""
		for valor in arrayValores:
			for (col,val) in valor.items():
				columnas+=col +','
				valores.append(val)
		columnas=columnas[:-1]

		for value in valores:
			value = str(value).replace("'"," ")
			if value is None or value.upper() == "NONE" or value.upper()=="S/N" or value == "-" or value.upper() =="NULL":
				valoresstring += "null" + ","
			elif len(re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}.[\d]{1,2}:[\d]{1,2}:[\d]{1,2}", value))>0:
				valoresstring += "'" +self.ArreglarFecha(value,timestamp="timestamp")+"',"
			elif len(re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", value))>0:
				valoresstring += "'" +self.ArreglarFecha(value)+"',"
			elif isinstance(value, int):
				valoresstring += str(value).replace('.','').replace(',','.') + ","
			elif(re.match("^[^a-zA-Z]*[^a-zA-Z]$", value)):
				valoresstring += "'" + value.replace('.','').replace(',','.') + "',"
			elif(re.match("^[A-Za-z0-9_-]*$", value)):
				valoresstring += "'" + value + "',"
			else:
				valoresstring +="'"+ value + "',"
		valoresstring = valoresstring[:-1]
		if False:
			query="insert into "+ tabla +"("+columnas+") values("+valoresstring+") "
		else:
			query="replace into "+ tabla +"("+columnas+") values("+valoresstring+") "
		for valor in arrayValores:
			for (col,val) in valor.items():
				if col not in ("ID_LEGAJO", "idFactura", "ID", "idLiquidacion", "idDetSimi", "ID_LEGAJO_INTER_FK"):
					extension+=col+"=VALUES("+col +'), '
		extension= extension[:-2]
		extensionquery= "ON DUPLICATE KEY UPDATE "+extension 
		if False:
			query = query + extensionquery
		else:
			query = query+";"
		return query


	def fixFormatting(self, value):
		value = str(value).replace("'"," ")
		if value is None or value.upper() == "NONE" or value.upper()=="S/N" or value == "-" or value.upper() =="NULL":
			value="null"
		elif len(re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}.[\d]{1,2}:[\d]{1,2}:[\d]{1,2}", value))>0:
			value = "'" +self.ArreglarFecha(value,timestamp="timestamp")+ "'"
		elif len(re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", value))>0:
			value = "'" +self.ArreglarFecha(value)+ "'"
		elif isinstance(value, int):
			value = str(value).replace('.','').replace(',','.')
		elif(re.match("^[^a-zA-Z]*[^a-zA-Z]$", value)):
			value = "'" + value.replace('.','').replace(',','.') + "'"
		elif(re.match("^[A-Za-z0-9_-]*$", value)):
			value = "'" + value + "'"
		else:
			value = "'"+ value + "'"
		'''
		Regex, etc etc etc.
		Se checkea el tipo de info y se a??aden comillas para denotar que es string, etc??tera.
		'''
		return value

	def cnstInsert(self, objeto, tabla, replaceInsteadOfInsert=False):
		keys=[]
		values=[]
		for attrib in dir(objeto):
			if attrib[:2]!="__":
				keys.append(attrib)
				values.append(self.fixFormatting(getattr(objeto, attrib)))
		
		keys = ",".join(keys)
		values= ",".join(values)

		q = "INSERT INTO %s(%s) VALUES (%s)"%(tabla, keys, values)
		if replaceInsteadOfInsert:
			q= "REPLACE INTO %s(%s) VALUES (%s)"%(tabla, keys, values)
		return q
