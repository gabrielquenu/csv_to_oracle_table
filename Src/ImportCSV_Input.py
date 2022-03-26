import pandas as pd
import cx_Oracle
import unidecode
import getpass
import os


class Converter():

    def __init__(self):

        # SET VARIABLES

        self.host = input('Insert host name or IP (127.0.0.1): ')
        self.port = input('Insert host port (1521): ')
        self.service = input('Insert service name (dbprd): ')
        self.username = input('Insert db username: ')
        self.password = getpass.getpass('Insert db password: ')
        self.table = input('Insert table name (owner.table_name): ')
        self.csv_file = input(
            'Insert CSV file path (/folder/folder/file.csv): ')

    def Convert(self):

        # CONNECT ORACLE DB

        dsn_tns = cx_Oracle.makedsn(
            self.host, self.port, service_name=self.service)
        conn = cx_Oracle.connect(
            user=self.username, password=self.password, dsn=dsn_tns)

        cursor = conn.cursor()

        # FORMAT CSV FILE

        CSVHandler.format_csv(self.csv_file)
        formatted_csv_file = '{}_formatted.csv'.format(
            self.csv_file[:-4])

        # READ CSV

        CSVData = ''

        CSVData = pd.read_csv(formatted_csv_file,
                              encoding='iso8859-1', delimiter='!@#')

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

        # REMOVE FORMATTED CSV

        try:
            os.remove(formatted_csv_file)
        except OSError as error:
            print("Failed with:", error.strerror)
            print("Error code:", error.code)

        # CLOSE DB CONNECTION

        conn.close()


class CSVHandler():
    def format_csv(file_name):
        csv_file = open(file_name, 'r', encoding='iso8859-1')
        data = csv_file.read().replace(';', '!@#').replace('"',
                                                           '').replace("'", '').replace('!@#\n', '\n')
        csv_file.close()

        csv_file = open('{}_formatted.csv'.format(file_name[:-4]), 'w')
        csv_file.write(data)
        csv_file.close()

        new_file_name = '{}_formatted.csv'.format(
            file_name[:-4])

        return new_file_name


converter = Converter()
converter.Convert()
