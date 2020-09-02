import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime
import os

CharaList = ["Mario", "Donkey", "Link","Sams","Dirk Sams","Yoshi","Karby","Fox","Pickachu","Luise","Ness","Chaptain Falcon","Pudding","Peach","Bowser","Ice Clubmer","Sheek", "Zelda",
"Dr.Mario","Pichu","Falco","Marth","Child Link","Ganon Durf","Mewtow","Roy","Mr.Game&Watch","Meta Night","Pit","Zero Suit Sums","Wario",
"Snake","Ike","Zenigame","Fushigisou","Rizerdon","DeDecong","Ryuka","Sonic","DeDeDe","Pikmin&Orima","Rukario","Robot","Toon Link",
"Wolf","Murabito","Megaman","WiiFittrainer","Rozeta&Chiko","Little Mac","Gureninja","Mii fight","Mii Sourd","Mii Ganer","Paltena",
"Packman","Ruffle","Shulk","Bowser Jr","Duck Hunt","Rue","Crowd","Kamui","Byonetta","InkRing","Ridrry","Shimon","King.K.Rool","Shizue",
"GaoGaen","Deyzy","Rukina","Crom","Black Pit","Ken""Rihiter","Packun Flower","Joker","Hero","Banjo&Kazui","Terry","MyenMyen"]

def table_isnotexist(conn, cur, tablename):
    cur.execute("""
        SELECT COUNT(*) FROM sqlite_master
        WHERE TYPE='table' AND name='{}'
        """.format(tablename))
    if cur.fetchone()[0] == 0:
        return True
    return False

class Main_window():
    def __init__(self):

        self.window = tk.Tk()
        self.window.geometry("700x800")
        self.window.title('Smash Memo')

        self.make_table()

        self.label1 = tk.Label(self.window, text="Daily Log")
        self.logs = DailyLog(self.window)
        self.label2 = tk.Label(self.window, text="Considerations")
        self.charabox1 = Chara_box(self.window)
        self.label3 = tk.Label(self.window, text="x")
        self.charabox2 = Chara_box(self.window)
        self.button1 = tk.Button(self.window, text="add logs", command=self.add_logs)
        self.text = tk.StringVar()
        self.consbox = tk.Entry(self.window,textvariable=self.text)
        self.consid = Consideration(self.window, self.charabox1.value.get(),self.charabox2.value.get())

        self.label1.pack()
        self.logs.box.pack()
        self.label2.pack()
        self.charabox1.box.pack()
        self.label3.pack()
        self.charabox2.box.pack()
        self.button1.pack()
        self.consbox.pack()
        self.consid.conslist.pack()

        self.window.mainloop()

    def make_table(self):
        dbname = "smashmemo.db"
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        if table_isnotexist(conn, cur, "logs"):
            cur.execute("CREATE TABLE logs(id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT, cha1 INT, cha2 INT,contents STRING)")
        conn.commit()
        conn.close()

    def add_logs(self):
        chanum1 = CharaList.index(self.charabox1.value.get())
        chanum2 = CharaList.index(self.charabox2.value.get())
        constext = str(self.text.get())
        dbname = "smashmemo.db"
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute("INSERT INTO logs(created_at, cha1, cha2, contents) values(?,?,?,?)",[datetime.datetime.now(),chanum1, chanum2, constext])
        conn.commit()
        conn.close()


class DailyLog():
    def __init__(self, window):
        self.box = tk.Listbox(window, width=400)
        dbname = "smashmemo.db"
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute("SELECT * FROM logs")
        k=0
        for i in cur.fetchall():
            print(i[1])
            self.box.insert("anchor",str(i))
        conn.commit()
        conn.close()

    def update(self):
        dbname = "smashmemo.db"
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute("SELECT * FROM logs")
        k=0
        for i in cur.fetchall():
            self.box.insert("anchor",str(i))
        conn.commit()
        conn.close()

class Consideration():
    def __init__(self, window,char1, char2):
        self.conslist = tk.Text(window,width = 200, height=200)
        self.conslist.insert('1.0', 'abocjd')
        dbname = "smashmemo.db"
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        cur.execute("SELECT * FROM logs")
        conn.commit()
        conn.close()

    def update(self):
        return

class Chara_box():
    def __init__(self, window):
        self.value = tk.StringVar()
        self.box = ttk.Combobox(window, values= CharaList, textvariable = self.value)


if __name__ == '__main__':
    Main_window()
