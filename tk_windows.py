import sqlite3
import tkinter as tk
from datetime import date

from water import MediaMeter


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, "water_invoice.db")

# db_water_path = '/home/amick/PycharmProjects/BILLS/water_invoice.db'
# db_path = os.path.join(BASE_DIR, self.db_name)
# with sqlite3.connect(db_path) as conn:

# TKINTER
class MainWindow:  # tworzę klasę tworzącą program
    def __init__(self, master):  # wrzucam w mastera główną funkcję: tk.Tk(), czyli tkinter.Tk() - czyli ROOT
        self.master = master  # self.master jest tkinter.Tk()
        self.windowname = master.wm_title('Rozliczenie Mediów Na Stoku')
        self.master.geometry("300x200")
        self.frame = tk.Frame(self.master)

        self.Button1 = \
            tk.Button(self.frame, text="WODA", fg='blue', width=125, command=lambda: self.new_window(Water_tk)).pack()
        self.Button2 = \
            tk.Button(self.frame, text="PRĄD", fg='red', width=125, command=lambda: self.new_window(Water_tk)).pack()
        self.Button3 = \
            tk.Button(self.frame, text="GAZ", fg='orange', width=125, command=lambda: self.new_window(Water_tk)).pack()
        self.Button4 = \
            tk.Button(self.frame, text="EXIT", fg='green', width=125, command=self.close_windows).pack()
        self.frame.pack()

    def new_window(self, _class):
        self.newwindow = tk.Toplevel(self.master)
        _class(self.newwindow)

    def close_windows(self):
        self.master.destroy()


class Water_tk:
    def __init__(self, master):
        self.windowname = master.wm_title('WODA')
        self.master = master
        self.master.geometry("800x300")
        self.frame = tk.Frame(self.master)

        self.label = tk.Label(master, text=f"Wybierz opcję:", anchor='w')
        self.label.pack()
        # self.get_all_invoice_Button = tk.Button(self.frame, text='Przejrzyj faktury', anchor='w', width=125,
        #                                         command=lambda: get_all_invoice_())
        self.get_all_invoice_Button = tk.Button(self.frame, text='Przejrzyj faktury', anchor='w', width=125,
                                                command=lambda: self.get_water_records())
        self.get_all_invoice_Button.pack(fill='x')
        self.insert_invoice_Button = tk.Button(self.frame, text='Wprowadź fakturę', anchor='w', width=125)
        self.insert_invoice_Button.pack(fill='x')
        self.insert_flat_meter_Button = tk.Button(self.frame, text='Wprowadź zużycie mediów / mieszkanie', anchor='w',
                                                  width=125)
        self.insert_flat_meter_Button.pack(fill='x')
        self.insert_flat_meter_Button = tk.Button(self.frame, text='Wydrukuj rozliczenie mediów.', anchor='w',
                                                  width=125)
        self.insert_flat_meter_Button.pack(fill='x')

        self.quitButton = tk.Button(self.frame, text='Quit', anchor='w', width=125, command=self.close_windows)
        self.quitButton.pack(fill='x')

        self.frame.pack()

    def close_windows(self):
        self.master.destroy()

    def get_water_records(self):
        try:
            conn = sqlite3.connect("water.db")
            cursor = conn.cursor()
            sqlite_select_query = """SELECT * FROM water_invoice"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for row in records:
                print(row)
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            input('Wciśnij enter by kontynuować.')



class GetRecords:
    def __init__(self, master):
        self.master = master
        self.master.geometry('1950x200+100+200')
        self.master.title('Faktury')
        self.frame = tk.Frame(self.master)

        self.connection = sqlite3.connect('water_invoice.db')
        self.cur = self.connection.cursor()
        self.idLabel = tk.Label(self.master, text="\nID", width=10, relief='ridge')
        self.idLabel.grid(row=0, column=0)
        self.okrRozLabel = tk.Label(self.master, text="OKRES\nROZLICZ.", width=10, relief='ridge')
        self.okrRozLabel.grid(row=0, column=1)
        self.todayLabel = tk.Label(self.master, text="dzień\nwpisu", width=10, relief='ridge')
        self.todayLabel.grid(row=0, column=2)
        self.datFaktLabel = tk.Label(self.master, text="data\nfaktury", width=10, relief='ridge')
        self.datFaktLabel.grid(row=0, column=3)
        self.wodaLabel = tk.Label(self.master, text="woda\n", width=10, relief='ridge')
        self.wodaLabel.grid(row=0, column=4)
        self.wOplataLabel = tk.Label(self.master, text="woda\nopłata", width=10, relief='ridge')
        self.wOplataLabel.grid(row=0, column=5)
        self.wAbonLabel = tk.Label(self.master, text="woda\nabonament", width=10, relief='ridge')
        self.wAbonLabel.grid(row=0, column=6)
        self.sciekiLabel = tk.Label(self.master, text="ścieki\n", width=10, relief='ridge')
        self.sciekiLabel.grid(row=0, column=7)
        self.sOplataLabel = tk.Label(self.master, text="ścieki\nopłata", width=10, relief='ridge')
        self.sOplataLabel.grid(row=0, column=8)
        self.sAbonLabel = tk.Label(self.master, text="ścieki\nabonament", width=10, relief='ridge')
        self.sAbonLabel.grid(row=0, column=9)
        self.oplaconaLabel = tk.Label(self.master, text="opłacona\n", width=10, relief='ridge')
        self.oplaconaLabel.grid(row=0, column=20)

        self.showallrecords()
        self.frame.pack()

    def showallrecords(self):
        data = self.readfromdatabase()
        for index, dat in enumerate(data):
            tk.Label(self.master, text=dat[0]).grid(row=index + 1, column=0)
            tk.Label(self.master, text=dat[1]).grid(row=index + 1, column=1)
            tk.Label(self.master, text=dat[2]).grid(row=index + 1, column=2)
            tk.Label(self.master, text=dat[3]).grid(row=index + 1, column=3)
            tk.Label(self.master, text=dat[4]).grid(row=index + 1, column=4)
            tk.Label(self.master, text=dat[5]).grid(row=index + 1, column=5)
            tk.Label(self.master, text=dat[6]).grid(row=index + 1, column=6)
            tk.Label(self.master, text=dat[7]).grid(row=index + 1, column=7)
            tk.Label(self.master, text=dat[8]).grid(row=index + 1, column=8)
            tk.Label(self.master, text=dat[9]).grid(row=index + 1, column=9)
            tk.Label(self.master, text=dat[10]).grid(row=index + 1, column=10)

    def readfromdatabase(self):
        sqlite_select_query1 = """SELECT * FROM main.water_invoice"""
        self.cur.execute(sqlite_select_query1)
        return self.cur.fetchall()


class Current_tk:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x400+400+400")
        self.frame = tk.Frame(self.master)

        self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.close_windows)
        self.label = tk.Label(master, text=f"this is window number")
        self.label.pack()
        self.label2 = tk.Label(master, text="PRĄD", bg='red')
        self.label2.pack()
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


class Gas_tk:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x400+400+400")
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text='Quit', width=25, command=self.close_windows)

        self.label = tk.Label(master, text=f"this is window number")
        self.label.pack()
        self.label2 = tk.Label(master, text="GAZ")
        self.label2.pack()
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


# ROZLICZENIA MEDIÓW
class MediaMeter:
    def __init__(self):  # tymczasowo zmienna określona z góry.. potem przekazana
        self.water_meter = 0
        self.todays_date = str(date.today())
        self.conn = sqlite3.connect("water.db")
        self.cursor = self.conn.cursor()
        print("Connected to SQLite")

    def water_meter_values(self):
        todays_date = self.todays_date
        glowny_woda = input('Wpisz stan licznika wody - GŁÓWNY: ')
        dol_woda = input('Wpisz stan licznika wody - DÓŁ: ')
        while glowny_woda != dol_woda:
            print('Wpisz poprawne dane. Stan licznika GŁÓWNY jest taki sam jak DÓŁ')
            glowny_woda = input('Wpisz stan licznika wody - GŁÓWNY: ')
            dol_woda = input('Wpisz stan licznika wody - DÓŁ: ')
        gora_woda = input('Wpisz stan licznika wody - GÓRA: ')
        gabinet_woda = input('Wpisz stan licznika wody - "GABINET": ')
        okres_rozliczeniowy_od = str(input('Wpisz początek okresu rozliczeniowego [rok-miesiac-dzień]: '))
        okres_rozliczeniowy_do = str(input('Wpisz koniec okresu rozliczeniowego [rok-miesiąc-dzień]: '))

        print(
            f'\n     Wpisałeś:\nDzień dziejszy: {todays_date},\nGŁÓWNY (łącznie): {glowny_woda},\nGÓRA: {gora_woda},'
            f'\nDÓŁ: {dol_woda},\n'
            f'GABINET: {gabinet_woda},\nOkres od: {okres_rozliczeniowy_od},\nOkres do: {okres_rozliczeniowy_do}.')
        check = str(input('Czy dane zostały wprowadzone poprawnie? T/N: '))
        if check == 'T' or check == 't':
            MediaMeter.water_db_insert_values(self, todays_date, glowny_woda, gora_woda, dol_woda, gabinet_woda,
                                              okres_rozliczeniowy_od, okres_rozliczeniowy_do)
        elif check == 'N' or check == 'n':
            MediaMeter.water_meter_values()

    def water_db_insert_values(self, a, b, c, d, e, f, g):
        sqlite_insert_query = """INSERT INTO water (todays_date, glowny_woda, gora_woda, dol_woda, gabinet_woda, okres_rozliczeniowy_od, okres_rozliczeniowy_do)
        VALUES 
        (?,?,?,?,?,?,?);"""
        data_tuple = (a, b, c, d, e, f, g)
        self.cursor.execute(sqlite_insert_query, data_tuple)
        self.conn.commit()
        print('Row added')

    def water_invoice_values(self):
        todays_date = self.todays_date
        set_year = str(self.todays_date)
        okres_rozliczeniowy = int(input(
            'Wybierz okres rozliczeniowy:\n1. Styczeń/luty\n2.Marzec/kwiecień\n3.Maj/czerwiec\n4.Lipiec/sierpierń\n'
            '5.Wrzesień/październik\n6.Listopad/Grudzień'))
        if okres_rozliczeniowy == 1:
            okres_rozliczeniowy = [(set_year[0:4], 'styczen'), (set_year[0:4], 'luty')]
        elif okres_rozliczeniowy == 2:
            pass
        dzien_dzisiejszy = self.todays_date
        data_otrzymania_faktury = str(input('Wpisz datę otrzymania faktury |rok-msc-dzien|'))
        woda = int(input('Wpisz stan licznika wody: '))
        woda_oplata = int(input('Woda netto: '))
        woda_abonament = int(input('Abonament woda netto: '))
        scieki = int(input('Wpisz stan licznika sciekow: '))
        scieki_oplata = int(input('Ścieki netto: '))
        scieki_abonament = int(input('Abonament scieki netto: '))
        oplacona = False

        print(
            f'\nWpisałeś:\nDzień dziejszy: {dzien_dzisiejszy},\nData otrzymania faktury: {data_otrzymania_faktury},'
            f'\nWoda-stan licznika: {woda},\nWoda-koszt |netto|: {woda_oplata},'
            f'\nWoda-abonament |netto|: {woda_abonament},\nŚcieki-stan licznika: {scieki},'
            f'\nŚcieki-koszt |netto|: {scieki_oplata},\nŚcieki-abonament |netto|: {scieki_abonament},'
            f'\nFaktura opłacona: {oplacona}\nOkres rozliczeniowy {okres_rozliczeniowy}')
        input('Wciśnij enter by kontynuować.')

        check = str(input('Czy dane zostały wprowadzone poprawnie? T/N: '))
        if check == 'T' or check == 't':
            MediaMeter.water_invoice_insert_values(self, okres_rozliczeniowy, dzien_dzisiejszy, data_otrzymania_faktury,
                                                   woda, woda_oplata, woda_abonament, scieki, scieki_oplata,
                                                   scieki_abonament, oplacona)
        elif check == 'N' or check == 'n':
            MediaMeter.water_invoice_values()

    def water_invoice_insert_values(self, a, b, c, d, e, f, g, h, i, j):
        sqlite_insert_query = """INSERT INTO water_invoice (okres_rozliczeniowy, dzien_dzisiejszy, 
        data_otrzymania_faktury, woda, woda_oplata, woda_abonament, scieki, scieki_oplata, scieki_abonament, oplacona)
         VALUES
         (?,?,?,?,?,?,?,?,?,?);"""
        data_tuple = (a, b, c, d, e, f, g, h, i, j)
        self.cursor.execute(sqlite_insert_query, data_tuple)
        self.conn.commit()
        print('Row added')

    def get_all_media_meter(self):
        try:
            sqlite_select_query = """SELECT * FROM water"""
            self.cursor.execute(sqlite_select_query)
            records = self.cursor.fetchall()
            for row in records:
                print(row, ' - okres rozliczeniowy: ', row[7:8])
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            input('\nWciśnij enter by kontynuować.')

    def get_all_invoice(self):
        try:
            sqlite_select_query = """SELECT * FROM water_invoice"""
            self.cursor.execute(sqlite_select_query)
            records = self.cursor.fetchall()
            for row in records:
                print(row)
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            input('Wciśnij enter by kontynuować.')

    def get_row(self, number):
        try:
            sqlite_select_query = """SELECT * FROM water WHERE id = ?"""
            data_tuple = number
            self.cursor.execute(sqlite_select_query, (data_tuple,))
            records = self.cursor.fetchall()
            for row in records:
                print(row)
            self.cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            # if (self.conn):
            #     self.conn.close()
            print("The SQLite connection is closed")


# here we have files without class


def water_database():
    conn = sqlite3.connect("water.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS water(
    id INTEGER PRIMARY KEY, 
    todays_date DATE,
    glowny_woda INTEGER,
    gora_woda INTEGER,
    dol_woda INTEGER,
    gabinet_woda INTEGER,
    okres_rozliczeniowy_od DATE,
    okres_rozliczeniowy_do DATE)
    """)


def water_invoice_database():
    conn = sqlite3.connect("water.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS water_invoice(
    id INTEGER PRIMARY KEY, 
    okres_rozliczeniowy DATE,
    dzien_dzisiejszy DATE,
    data_otrzymania_faktury DATE, 
    woda INTEGER,
    woda_oplata FLOAT,
    woda_abonament FLOAT,
    scieki INTEGER,
    scieki_oplata FLOAT,
    scieki_abonament FLOAT,
    oplacona BOOLEAN,
    FOREIGN KEY(okres_rozliczeniowy) REFERENCES water(okres_rozliczeniowy_od)
    )
    """)


def choices():
    choice = 0
    while choice != 10:
        print('\n' * 50)
        print('Witaj w kalkulatorze opłat za media - WODA.\nWybierz:\n'
              '1. Wpisz stan licznika na dzień dzisiejszy.\n'
              '2. Zmień stan licznika na wybrany dzień.\n'
              '3. Pokaż stany liczników - całość.\n'
              '4. Pokaż stan licznika na konkretny okres rozliczeniowy\n'
              '5. Wydrukuj rozliczenie mediów.\n'
              '6. Wpisz taryfy za wodę.\n'  # można przecież tutaj wpisać self.name - np woda, gaz, prąd
              '7. Porównaj okresy rozliczeniowe.\n'
              '8. Wpisz dane z faktury.\n'
              '9. Pokaż stan faktur.\n'
              '10. Wyjście.')

        choice = int(input())
        if choice == 1:
            water.water_meter_values()
        elif choice == 2:
            pass
        elif choice == 3:
            water.get_all_media_meter()
        elif choice == 4:
            water.get_row(1)
        elif choice == 5:
            pass
        elif choice == 6:
            pass
        elif choice == 7:
            pass
        elif choice == 8:
            water.water_invoice_values()
        elif choice == 9:
            water.get_all_invoice()
        elif choice == 10:
            pass


# #doubled functions
# def get_all_invoice_():
#     try:
#         conn = sqlite3.connect("water.db")
#         cursor = conn.cursor()
#         sqlite_select_query = """SELECT * FROM water_invoice"""
#         cursor.execute(sqlite_select_query)
#         records = cursor.fetchall()
#         for row in records:
#             print(row)
#     except sqlite3.Error as error:
#         print("Failed to read data from sqlite table", error)
#     finally:
#         input('Wciśnij enter by kontynuować.')


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    water_database()
    water_invoice_database()
    water = MediaMeter()
    main()
