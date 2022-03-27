import pandas as pd
from detect_delimiter import detect
import cx_Oracle
import unidecode
import os


class Converter():

    def __init__(self):

        # SET VARIABLES

        self.host = '127.0.0.1'
        self.port = '1521'
        self.service = 'dbprd'
        self.username = 'username'
        self.password = 'password'
        self.table = 'owner.table'
        self.csv_file = r'/folder/folder/file'

    def Convert(self):

        # CONNECT ORACLE DB
        dsn_tns = cx_Oracle.makedsn(
            self.host, self.port, service_name=self.service)
        conn = cx_Oracle.connect(
            user=self.username, password=self.password, dsn=dsn_tns)

        cursor = conn.cursor()

        # DETECT CSV DELIMITER
        file = open(self.csv_file, 'r')
        CSVDelimiter = detect(file.readline(), whitelist=[',', ';'])
        file.close()

        # READ CSV
        CSVData = ''

        CSVData = pd.read_csv(self.csv_file,
                              encoding='iso8859-1', delimiter=CSVDelimiter)

        CSVData = CSVData.fillna('NULL')

        # DROP TABLE
        try:
            cursor.execute('DROP TABLE {}'.format(self.table))
            conn.commit()
        except:
            pass

        # CREATE TABLE
        columnsCreate = ''

        for column in CSVData.keys():
            column = str(column)
            column = column.replace(' ', '_')
            column = column.upper()
            column = unidecode.unidecode(column)
            columnsCreate = columnsCreate + column + ' varchar2(255),\n'
        columnsCreate = columnsCreate[:-2]

        cursor.execute('''
            CREATE TABLE {} (
                {}
            )
        '''.format(self.table, columnsCreate))
        conn.commit()

        # INSERT DATA
        columnsInsert = ''
        for column in CSVData.keys():
            column = str(column)
            column = column.replace(' ', '_')
            column = column.upper()
            column = unidecode.unidecode(column)
            columnsInsert = columnsInsert + column + ', '
        columnsInsert = columnsInsert[:-2]

        for index, row in CSVData.iterrows():
            rowData = ''
            for value in row:
                value = str(value)[0:254]
                if value == 'NULL':
                    rowData = rowData + value + ', '
                else:
                    rowData = rowData + "'" + value + "'" + ', '
            rowData = rowData[:-2]
            cursor.execute('''
            INSERT INTO {}
            ({})
            VALUES
            ({})
            '''.format(self.table, columnsInsert, rowData))
            conn.commit()

        # CLOSE DB CONNECTION
        conn.close()


converter = Converter()
converter.Convert()
