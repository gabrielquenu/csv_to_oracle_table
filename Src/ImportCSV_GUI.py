import pandas as pd
from detect_delimiter import detect
import cx_Oracle
import unidecode

from dataclasses import replace
from tkinter import *
from tkinter import filedialog

import os


class Converter():

    def Convert(host, port, service, username, password, csv_file, table):

        # CONNECT ORACLE DB
        dsn_tns = cx_Oracle.makedsn(host, port, service_name=service)
        conn = cx_Oracle.connect(user=username, password=password, dsn=dsn_tns)

        cursor = conn.cursor()

        # DETECT CSV DELIMITER
        file = open(csv_file, 'r')
        CSVDelimiter = detect(file.readline(), whitelist=[',', ';'])
        file.close()

        # READ CSV
        CSVData = ''

        CSVData = pd.read_csv(csv_file,
                              encoding='iso8859-1', delimiter=CSVDelimiter)

        CSVData = CSVData.fillna('NULL')

        # DROP TABLE
        try:
            cursor.execute('DROP TABLE {}'.format(table))
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
        '''.format(table, columnsCreate))
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
            '''.format(table, columnsInsert, rowData))
            conn.commit()

        # CLOSE DB CONNECTION
        conn.close()

        success = Success()
        success.Label()
        success.mainloop()


class Main(Tk):
    host = ''
    port = ''
    service = ''
    username = ''
    password = ''
    csv_file = ''
    table = ''

    def __init__(self):
        super().__init__()
        self.geometry('700x500')
        self.resizable(False, False)
        self.title('CSV to Oracle Table')
        self.host = StringVar()
        self.port = StringVar()
        self.service = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.table = StringVar()

    def Label(self):
        self.host_lbl = Label(self, text="Host:", font="Helvetica 24")
        self.host_lbl.place(x=190, y=50)

        self.port_lbl = Label(self, text="Port:", font="Helvetica 24")
        self.port_lbl.place(x=194, y=100)

        self.service_lbl = Label(self, text="Service:", font="Helvetica 24")
        self.service_lbl.place(x=146, y=150)

        self.db_username_lbl = Label(
            self, text="DB Username:", font="Helvetica 24")
        self.db_username_lbl.place(x=50, y=200)

        self.db_password_lbl = Label(
            self, text="DB Password:", font="Helvetica 24")
        self.db_password_lbl.place(x=58, y=250)

        self.table_name_lbl = Label(
            self, text="Table Name:", font="Helvetica 24")
        self.table_name_lbl.place(x=72, y=300)

        self.csv_file_lbl = Label(self, text="CSV File:", font="Helvetica 24")
        self.csv_file_lbl.place(x=124, y=350)

        self.csv_file_selected_lbl = Label(
            self, text='', font="Helvetica 8")
        self.csv_file_selected_lbl.place(x=380, y=365)

    def Entry(self):
        self.host_entry = Entry(
            self, width=22, textvariable=self.host)
        self.host_entry.insert(0, '127.0.0.1')
        self.host_entry.place(x=280, y=50, height=40)

        self.port_entry = Entry(
            self, width=22, textvariable=self.port)
        self.port_entry.insert(0, '1521')
        self.port_entry.place(x=280, y=100, height=40)

        self.service_entry = Entry(
            self, width=22, textvariable=self.service)
        self.service_entry.insert(0, 'dbprd')
        self.service_entry.place(x=280, y=150, height=40)

        self.username_entry = Entry(
            self, width=22, textvariable=self.username)
        self.username_entry.insert(0, 'username')
        self.username_entry.place(x=280, y=200, height=40)

        self.password_entry = Entry(
            self, show='*', width=22, textvariable=self.password)
        self.password_entry.insert(0, 'password')
        self.password_entry.place(x=280, y=250, height=40)

        self.table_entry = Entry(
            self, width=22, textvariable=self.table)
        self.table_entry.insert(0, 'owner.table_name')
        self.table_entry.place(x=280, y=300, height=40)

    def Button(self):
        self.csv_btn = Button(self, text='Select File',
                              command=self.GetFileName)
        self.csv_btn.place(x=280, y=350, height=40)

        self.convert_btn = Button(
            self, text='Convert', command=self.ConvertFile)
        self.convert_btn.place(x=320, y=420, height=40)

    def GetFileName(self):
        self.csv_file = filedialog.askopenfilename()
        self.csv_file_selected_lbl.config(text=self.csv_file)

    def ConvertFile(self):
        Converter.Convert(self.host.get(), self.port.get(), self.service.get(),
                          self.username.get(), self.password.get(), self.csv_file, self.table.get())


class Success(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('250x150')
        self.resizable(False, False)
        self.title('Success')

    def Label(self):
        self.success_lbl = Label(
            self, text="File converted!", font="Helvetica 24")
        self.success_lbl.place(x=10, y=10)


main = Main()

main.Label()
main.Entry()
main.Button()
main.mainloop()
