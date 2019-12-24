import sqlite3
from datetime import date


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
        print('\n'*50)
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


if __name__ == '__main__':
    water_database()
    water_invoice_database()
    water = MediaMeter()
    choices()
