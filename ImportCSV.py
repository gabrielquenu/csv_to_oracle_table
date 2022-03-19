import pandas as pd
import cx_Oracle
import unidecode

# VARIABLES - SETUP
hostName = 'hostNameOrIp'
port = '1521'
serviceName = 'serviceName'
dbUsername = 'username'
dbPassword = 'password'
csvFileName = 'file.csv'
tableName = 'OWNER.TABLE_NAME'

# CONNECT ORACLE DB
dsn_tns = cx_Oracle.makedsn(hostName, port, service_name=serviceName) 
conn = cx_Oracle.connect(user=dbUsername, password=dbPassword, dsn=dsn_tns)

cursor = conn.cursor()

# READ CSV
CSVData = pd.read_csv(csvFileName)

# DROP TABLE
try:
    cursor.execute('DROP TABLE {}'.format(tableName))
    conn.commit()
except:
    pass

# CREATE TABLE
columnsCreate = ''

for column in CSVData.keys():
    column = column.replace(' ', '_')
    column = column.upper()
    column = unidecode.unidecode(column)
    columnsCreate = columnsCreate + column + ' varchar2(255),\n'

columnsCreate = columnsCreate[:-2]

cursor.execute('''
    CREATE TABLE {} (
        {}
    )
'''.format(tableName, columnsCreate))
conn.commit()

# INSERT DATA
columnsInsert = ''
for column in CSVData.keys():
    column = column.replace(' ', '_')
    column = column.upper()
    column = unidecode.unidecode(column)
    columnsInsert = columnsInsert + column + ', '
columnsInsert = columnsInsert[:-2]

for index, row in CSVData.iterrows():
    rowData = ''
    for value in row:
        rowData = rowData + "'" + value + "'" + ', '
    rowData = rowData[:-2]
    cursor.execute('''
    INSERT INTO {}
    ({})
    VALUES
    ({})
    '''.format(tableName, columnsInsert, rowData))
    conn.commit()

# CLOSE DB CONNECTION
conn.close()
