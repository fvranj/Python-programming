# login app

import tkinter as tk
import sqlite3

conn = sqlite3.connect('smartkey.db')
print ("Opened database successfully")
conn.execute('''DROP TABLE IF EXISTS LOCK;''')
conn.execute('''CREATE TABLE LOCK
         (ID INTEGER PRIMARY KEY  AUTOINCREMENT   NOT NULL,
         NAME           TEXT    NOT NULL,
         PIN            INT     NOT NULL,
         ADMIN          BOOLEAN  NOT NULL,
         ACTIVE         BOOLEAN  NOT NULL);''')
print ('Table created successfully')

conn.execute("INSERT INTO LOCK (NAME,PIN,ADMIN,ACTIVE) \
      VALUES ('SpuzvaBob', 123456, TRUE, TRUE )");

conn.execute("INSERT INTO LOCK (NAME,PIN,ADMIN,ACTIVE) \
      VALUES ('Kalamarko', 666666, FALSE, TRUE )");

conn.execute("INSERT INTO LOCK (NAME,PIN,ADMIN,ACTIVE) \
      VALUES ('Patrik', 111111, FALSE, TRUE )");

conn.execute("INSERT INTO LOCK (NAME,PIN,ADMIN,ACTIVE) \
      VALUES ('G. Klijestic', 252525, FALSE, TRUE )");

conn.execute("INSERT INTO LOCK (NAME,PIN,ADMIN,ACTIVE) \
      VALUES ('Luna', 941538, FALSE, TRUE )");

conn.execute("INSERT INTO LOCK (NAME,PIN,ADMIN,ACTIVE) \
      VALUES ('Koraljka', 585321, FALSE, TRUE )");

conn.execute("INSERT INTO LOCK (NAME,PIN,ADMIN,ACTIVE) \
      VALUES ('Plankton', 123579, FALSE, TRUE )");

conn.execute("INSERT INTO LOCK (NAME,PIN,ADMIN,ACTIVE) \
      VALUES ('Slavko', 121212, FALSE, TRUE )");

conn.commit()

conn.close()


class AdminPanel(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        conn = sqlite3.connect('smartkey.db')
        query = f"SELECT NAME FROM LOCK;"
        cursor=conn.execute(query)
        user = cursor.fetchall()
        conn.close()
        
        self.users = []
        self.var = tk.Variable(value=self.users)
        
        self.listbox=tk.Listbox(container, selectmode=tk.SINGLE, listvariable=self.var)
        self.update_list()
        self.listbox.grid(row=10, column=3, rowspan=20, padx=5, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.insert_name_and_pin)

        
        self.name_label=tk.Label(container, text="Ime korisnika")
        self.name_label.grid(row=10, column=5, columnspan=3, padx=5, pady=5)
        
        self.sv_name = tk.StringVar()
        self.name_entry=tk.Entry(container, textvariable=self.sv_name)
        self.name_entry.grid(row=11, column=5, columnspan=3, padx=5, pady=5)
        
        self.pin_label=tk.Label(container, text="PIN")
        self.pin_label.grid(row=12, column=5, columnspan=3, padx=5, pady=5)
        

        self.sv_pin = tk.StringVar()
        self.pin_entry=tk.Entry(container, textvariable=self.sv_pin)
        self.pin_entry.grid(row=13, column=5, columnspan=3, padx=5, pady=5)
        
        self.gumb_aktivacija=tk.Button(container, text="Deaktiviraj korisnika", bg="red", command=lambda :self.deaktiviraj_korisnika())
        self.gumb_aktivacija.grid(row=14, column=8, columnspan=10, padx=5, pady=5)
        
        self.gumb_spremi=tk.Button(container, text="Spremi promjene", command=lambda :self.spremi_promjene_ime_i_pin())
        self.gumb_spremi.grid(row=10, column=8, columnspan=10, padx=5, pady=5)
        
        self.gumb_odustani=tk.Button(container, text="Odustani", command=lambda :self.odustani())
        self.gumb_odustani.grid(row=11, column=8, columnspan=10, padx=5, pady=5)
        
        self.gumb_izbrisi=tk.Button(container, text="Izbrisi korisnika", command= lambda :self.izbrisi_korisnika())
        self.gumb_izbrisi.grid(row=12, column=8, columnspan=10, padx=5, pady=5)
        
        
    def insert_name_and_pin(self, event):
        text=self.listbox.get(self.listbox.curselection())
        self.name_entry.delete(0,tk.END)
        self.name_entry.insert(0,text)
        
        conn = sqlite3.connect('smartkey.db')
        query = f"SELECT PIN FROM LOCK WHERE NAME='{text}';"
        cursor=conn.execute(query)
        pin = cursor.fetchall()
        conn.close()      
        
        self.pin_entry.delete(0,tk.END)
        self.pin_entry.insert(0,pin[0][0])
        
    def spremi_promjene_ime_i_pin(self):
        new_name = self.name_entry.get()
        new_pin = self.pin_entry.get()

        global msg
        
        if len(new_pin)==6 and new_pin.isdigit():
        
            conn = sqlite3.connect('smartkey.db')
            query1 = f"SELECT ID FROM LOCK WHERE NAME='{self.listbox.get(self.listbox.curselection())}';"
            cursor=conn.execute(query1)
            id_old = cursor.fetchall()
            id_old=id_old[0][0]
        
            query2 = f"UPDATE LOCK SET NAME='{new_name}', PIN={new_pin} WHERE ID={id_old};"
            cursor=conn.execute(query2)
            conn.commit()
            conn.close() 

            self.update_list() 

            msg = f"\nPodaci korisnika '{new_name}' su uspjesno izmjenjeni."
            post_message(msg)

        else:
            msg = "\nPin mora imati 6 znamenki!"
            post_message(msg)

            
            
    def izbrisi_korisnika(self):
        
        conn = sqlite3.connect('smartkey.db')
        query = f"DELETE FROM LOCK WHERE NAME='{self.listbox.get(self.listbox.curselection())}';"
        cursor=conn.execute(query)
        conn.commit()
        conn.close()
        
        global msg 
        msg = f"\nKorisnik {self.listbox.get(self.listbox.curselection())} je uspjesno izbrisan"
        post_message(msg)
        self.update_list()
    
    def novi_korisnik(self):
        new_name = self.name_entry.get()
        new_pin = self.pin_entry.get()
        
        if self.name_entry.get() != self.listbox.get(self.listbox.curselection()) and len(new_pin)==6 and new_pin.isdigit():
            conn = sqlite3.connect('smartkey.db')
            query = "INSERT INTO LOCK(NAME, PIN, ADMIN, ACTIVE) VALUES (?,?,0,1);"
            cursor=conn.execute(query, (new_name, new_pin))
            conn.commit()
            conn.close()
            global msg 
            msg = "\nNovi korisnik uspjesno dodan!"
            post_message(msg)
            self.update_list()
        
        elif self.name_entry.get() == self.listbox.get(self.listbox.curselection()) and len(new_pin)==6 and new_pin.isdigit():
            msg = "\nNovi korisnik ne smije imati vec postojece ime!"
            post_message(msg)
        
        else:
            msg = "\nPin mora imati 6 znamenki!"
            post_message(msg)
        

    def odustani(self):
        quitWindow = tk.Toplevel(app)
        tk.Label(quitWindow, text="Zelite li spremiti novog korisnika?").grid(row=0, column=0, columnspan=4)
        gumb_da = tk.Button(quitWindow, text="Da", padx=5, pady=5, command= lambda :[self.novi_korisnik(), quitWindow.destroy()])
        gumb_da.grid(row=1, column=0)
        gumb_ne = tk.Button(quitWindow, text="Ne", padx=5, pady=5, command=lambda :quitWindow.destroy())
        gumb_ne.grid(row=1, column=3)


    def deaktiviraj_korisnika(self):
        
        name = self.listbox.get(self.listbox.curselection())
        
        conn = sqlite3.connect('smartkey.db')
        query = f"UPDATE LOCK SET ACTIVE=0 WHERE NAME='{name}';"
        cursor=conn.execute(query)
        conn.commit()
        conn.close()  
        
        self.gumb_aktivacija.config(bg='green', text="Aktiviraj korisnika", command=lambda :self.aktiviraj_korisnika())
        global msg 
        msg = f"\nKorisnik {self.listbox.get(self.listbox.curselection())} je deaktiviran"
        post_message(msg)

    
    def aktiviraj_korisnika(self):
        
        name = self.listbox.get(self.listbox.curselection())
        
        conn = sqlite3.connect('smartkey.db')
        query = f"UPDATE LOCK SET ACTIVE=1 WHERE NAME='{name}';"
        cursor=conn.execute(query)
        conn.commit()
        conn.close()  
        
        self.gumb_aktivacija.config(bg='red', text="Deaktiviraj korisnika", command=lambda :self.deaktiviraj_korisnika())
        global msg 
        msg = f"\nKorisnik {self.listbox.get(self.listbox.curselection())} je aktiviran"
        post_message(msg)

    def update_list(self):

        conn = sqlite3.connect('smartkey.db')
        query = f"SELECT NAME FROM LOCK;"
        cursor=conn.execute(query)
        user = cursor.fetchall()
        conn.close()
        
        self.users = [user[i][0] for i in range(len(user))]
        self.var = tk.Variable(value=self.users)
        self.listbox.config(listvariable=self.var)

class Grid_button(tk.Button):
    def __init__(self, number):
        super().__init__ (text=number, height=5, width=5, command=self.get_num)
        self.number=number

    def get_num(self):
        return self.number

class Pinpad(tk.Frame):
    def __init__(self, container):
        super().__init__()
        
        self.pin = ""
        self.neuspjesni_pokusaji=0
        
        self.pin_entry = tk.Entry(show="*")
        self.pin_entry.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        
        options={'padx':5, 'pady':5} 
        
        self.button_1 = Grid_button('1')
        self.button_1['command'] =  lambda :self.update_pin('1')
        self.button_1.grid(row=5, column=0, **options)
        self.button_2 = Grid_button('2')
        self.button_2['command'] =  lambda :self.update_pin('2')
        self.button_2.grid(row=5, column=1, **options)
        self.button_3 = Grid_button('3')
        self.button_3['command'] =  lambda :self.update_pin('3')
        self.button_3.grid(row=5, column=2, **options)
        self.button_4 = Grid_button('4')
        self.button_4['command'] =  lambda :self.update_pin('4')
        self.button_4.grid(row=6, column=0, **options)
        self.button_5 = Grid_button('5')
        self.button_5['command'] =  lambda :self.update_pin('5')
        self.button_5.grid(row=6, column=1, **options)
        self.button_6 = Grid_button('6')
        self.button_6['command'] =  lambda :self.update_pin('6')
        self.button_6.grid(row=6, column=2, **options)
        self.button_7 = Grid_button('7')
        self.button_7['command'] =  lambda :self.update_pin('7')
        self.button_7.grid(row=7, column=0, **options)
        self.button_8 = Grid_button('8')
        self.button_8['command'] =  lambda :self.update_pin('8')
        self.button_8.grid(row=7, column=1, **options)
        self.button_9 = Grid_button('9')
        self.button_9['command'] =  lambda :self.update_pin('9')
        self.button_9.grid(row=7, column=2, **options)
        self.button_ac = Grid_button('AC')
        self.button_ac['command'] =  lambda :self.clear_pin()
        self.button_ac.grid(row=8, column=0, **options)
        self.button_0 = Grid_button('0')
        self.button_0['command'] =  lambda :self.update_pin('0')
        self.button_0.grid(row=8, column=1, **options)
        self.button_c = Grid_button('C')
        self.button_c['command'] =  lambda :self.trunc_pin()
        self.button_c.grid(row=8, column=2, **options)
        
        self.message_box = tk.Text()
        self.message_box.grid(row=4, column=3, rowspan=5, columnspan=10, padx=15, pady=15)
        
        
    def update_pin(self, num):
        self.pin += num
        self.update_entry()
        
    def update_entry(self):
        self.pin_entry.delete(0, tk.END)
        self.pin_entry.insert(tk.END, self.pin)
        self.check_pin()
        
        
    def check_pin(self):
        if len(self.pin)==6:
            conn = sqlite3.connect('smartkey.db')
            query = f"SELECT NAME FROM LOCK WHERE ACTIVE=1 AND PIN={self.pin}"
            cursor=conn.execute(query)
            user = cursor.fetchall()
            query2 = "SELECT NAME FROM LOCK WHERE ADMIN=1"
            cursor=conn.execute(query2)
            admin = cursor.fetchall()
            conn.close()
            if len(user)==1:
                self.message_box.insert(tk.END, f"\n{user[0][0]}, dobrodosli doma!")
                self.clear_pin()
                self.update_entry()
                self.neuspjesni_pokusaji=0
                if user[0][0]==admin[0][0]:
                    self.admin_screen()
            else:
                self.message_box.insert(tk.END, f"\nPokusajte ponovno, imate jos {3-self.neuspjesni_pokusaji} pokusaja")
                self.clear_pin()
                self.update_entry()
                self.neuspjesni_pokusaji+=1
                if self.neuspjesni_pokusaji==3:
                    self.zamrzni_grid()
                    self.message_box.insert(tk.END, f"\nMolimo pozvonite!")
    
    def clear_pin(self):
        self.pin=""
        self.update_entry()
    
    def trunc_pin(self):
        if len(self.pin)>=1:
            self.pin=self.pin[:-1]
            self.update_entry()
            
    def zamrzni_grid(self):
        self.button_1["state"]=tk.DISABLED
        self.button_2["state"]=tk.DISABLED
        self.button_3["state"]=tk.DISABLED
        self.button_4["state"]=tk.DISABLED
        self.button_5["state"]=tk.DISABLED
        self.button_6["state"]=tk.DISABLED
        self.button_7["state"]=tk.DISABLED
        self.button_8["state"]=tk.DISABLED
        self.button_9["state"]=tk.DISABLED
        self.button_0["state"]=tk.DISABLED
        self.button_c["state"]=tk.DISABLED
        self.button_ac["state"]=tk.DISABLED
        endgame()
        
    def admin_screen(self):
        adminWindow = tk.Toplevel(app)
        tk.Label(adminWindow, text="Zelite li otvoriti admin panel?").grid(row=0, column=0, columnspan=4)
        gumb_da = tk.Button(adminWindow, text="Da", padx=10, pady=10, command= lambda :[self.open_admin_panel(), adminWindow.destroy()])
        gumb_da.grid(row=1, column=0)
        gumb_ne = tk.Button(adminWindow, text="Ne", padx=10, pady=10, command=lambda :adminWindow.destroy())
        gumb_ne.grid(row=1, column=3)
        
    def open_admin_panel(self):
        AdminPanel(app).grid(row = 10, column = 0, padx=5, pady=5)

class Frame_main(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        options = {'padx': 10, 'pady': 10}
        
        self.button_unlock = tk.Button(container, text='Otkljucaj vrata', command=self.unlock_pinpad)
        self.button_unlock.grid(row = 0, column = 3, **options)
        
        self.button_ring = tk.Button(container, text='Pozvoni', command=self.bell)
        self.button_ring.grid(row = 0, column = 8, **options)

    
    def bell(self):
        bell_screen = tk.Toplevel(app)
        
        tk.Label(bell_screen, text='Molimo za strpljenje, netko ce uskoro doci otvoriti vrata', padx=15, pady=15).pack()
        
    def unlock_pinpad(self):
        global pinpad
        pinpad = Pinpad(app)
        pinpad.grid(row = 0, column=0, padx=5, pady=5)

    
def post_message(message):
    pinpad.message_box.insert(tk.END, message)

def endgame():
    intro_frame.button_unlock['state']=tk.DISABLED

if __name__=="__main__":
    app = tk.Tk()
    intro_frame = Frame_main(app)
    app.mainloop()
