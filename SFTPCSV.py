import paramiko
import pysftp  #installed pysftp-0.2.8
import re
import MySQLdb
import pandas as pd
from sqlalchemy import create_engine

ssh = paramiko.SSHClient()
table_name_start = 'tab'
pattern = '[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])(2[0-3]|[01][0-9]):[0-5][0-9]+.csv'
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# details to connect with remote server
remote_host = '' #'192.168.43.14'
remote_user = '' #'satish123'
remote_password = '' #'satish123'

#details to coonect with database
host = '' #'localhost'
user = '' #'root'
password = '' #'satish'
database = '' #'test'
ssh.connect(remote_host,port=22, username=remote_user,password=remote_password)
sftp_client = ssh.open_sftp()

def CommunicatingWithRemoteServer(remote_path, local_path):
	'''This Function assuming every .csv is a one Table, eg: tab1, tab2,tab3...'''
	files = (sftp_client.listdir(remote_path))
	for file_name in files:
		fileNameChecking = re.search(pattern, file_name) #patternMAtching with date and time stamp and should be ends with .csv
		print(fileNameChecking)
		if fileNameChecking:
			remote_path = ('remote_path'+file_name)
			print('RemotePath:  'remote_path)
			# file = sftp.put('C://Users/Satish/Desktop/Perf-1-2016-10-21 1345.csv')
			file = sftp_client.get(remote_path, local_path+file_name)

			df = pd.read_csv(local_path, sep = ',')
			try:
				# creating Mysql connection
				engine = create_engine('mysql://{user}:{passsword}@{host}}/{db}'.format(user = user, passsword=passsword,db=database), echo=False)
				print(engine)
				# print(file_name.strip('.csv'))
				resp = df.to_sql(tab+str(1), engine, index=False)
			except Exception as Error:
				print(Error)
			else:
				return 'added data into database'

			#deleting downloaded file from local machine
			if os.path.exists(local_path+file_name):
				os.remove(file_name)


def alltogather(tableName,remote_path, local_path):
	'''This function assuming need to Save all the CSV files into single table'''
	db = MySQLdb.connect (host=host,
	    user=user,
	    passwd=password,
	    db=database,
	    local_infile = 1) #Grants permission to write to db from an input file. Without this you get sql Error: (1148, 'The used command is not allowed with this MySQL version')

	print ("Connection to DB established")
	cur = db.cursor()
	files = (sftp_client.listdir(remote_path))
	for file_name in files:
		fileNameChecking = re.search(pattern, file_name) #patternMAtching with date and time stamp and should be ends with .csv
		print(fileNameChecking)
		if fileNameChecking:
			remote_path = ('remote_path'+file_name)
			print('RemotePath:  'remote_path)
			# file = sftp.put('C://Users/Satish/Desktop/Perf-1-2016-10-21 1345.csv')
			file = sftp_client.get(remote_path, local_path+file_name)
	
	with open(local_path+file, 'r') as tb:
		schema = (tb.readlines())
		cols = ''.join(schema[0].split()).split(',')
		print(cols)
		try:
			query = """create table  if not exists {table} ({cols0} Datetime, {cols1} INT, {cols2} Char(100), {cols3} INT UNIQUE, {cols4} INT)""".format(table=tableName,cols0 = cols[0], cols1 = cols[1], cols2= cols[2], cols3 = cols[3], cols4 = cols[4])
			cur.execute(query)
			for i in schema[1::]:
			 	# insert values into hugedata ()
				values = ''.join(i.split()).split(',')
				print(values)
				insert_values = """insert into hugedata1 values({v1}, {v2}, {v3}, {v4}, {v5})""".format(v1 = values[0], v2= values[1], v3 = values[2], v4 = values[3], v5 = values[4])
				cur.execute(insert_values)
				cur.commit()
			except Exception as Error:
				cur.rollback()
				print(Error)
			finally:
				cur.close()
			#deleting downloaded file from local machine
			if os.path.exists(local_path+file_name):
				os.remove(file_name)
	
if __name__() == '__main__':
	CommunicatingWithRemoteServer(remote_path, local_path)
	alltogather(tableName,remote_path, local_path)
