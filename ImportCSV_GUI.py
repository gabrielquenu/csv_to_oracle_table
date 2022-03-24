from tkinter import *

class Main(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('700x500')
        self.resizable(False,False)
        self.title('CSV to Oracle Table')
    def Label(self):
        self.host = Label(self, text="Host:", font="Helvetica 24")
        self.host.place(x=50,y=50)
        self.port = Label(self, text="Port:", font="Helvetica 24")
        self.port.place(x=50,y=100)
        self.service = Label(self, text="Service:", font="Helvetica 24")
        self.service.place(x=50,y=150)
        self.db_username = Label(self, text="DB Username:", font="Helvetica 24")
        self.db_username.place(x=50,y=200)
        self.db_password = Label(self, text="DB Password:", font="Helvetica 24")
        self.db_password.place(x=50,y=250)
        self.csv_file = Label(self, text="DB Password:", font="Helvetica 24")
        self.csv_file.place(x=50,y=300)
        self.table_name = Label(self, text="DB Password:", font="Helvetica 24")
        self.table_name.place(x=50,y=350)
    def Entry(self):
        self.host_entry = Text(self, highlightcolor='green', width=22, height=2)
        self.host_entry.place(x=150, y=50)
        self.port_entry = Text(self, highlightcolor='green', width=22, height=2)
        self.port_entry.place(x=150, y=100)
        self.service_entry = Text(self, highlightcolor='green', width=22, height=2)
        self.service_entry.place(x=180, y=150)
        self.service_entry = Text(self, highlightcolor='green', width=22, height=2)
        self.service_entry.place(x=180, y=150)

main = Main()
main.Label()
main.Entry()
main.mainloop()