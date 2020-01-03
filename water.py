import os
import sqlite3
import sys
from datetime import date, datetime

import pandas as pd

from database.database_water import water_database, water_invoice_database, payments_database


class MediaMeter:
    def __init__(self):  # tymczasowo zmienna określona z góry.. potem przekazana
        self.water_meter = 0
        self.todays_date = str(date.today())
        self.conn = sqlite3.connect("water.db")
        self.cursor = self.conn.cursor()
        print("Connected to SQLite")

    def get_data_from_queries_last_water(self):
        try:
            last_row_water1 = """SELECT * FROM water ORDER BY id DESC LIMIT 0, 1;"""
            self.cursor.execute(last_row_water1)
            record = self.cursor.fetchall()
            for row in record:
                last_row_water = row
            self.last_row_water = list(last_row_water)


        except UnboundLocalError as error:
            input('Wciśnij enter by kontynuować.')

    def get_data_from_queries_before_last_water(self):
        try:
            before_last_row_water1 = """SELECT * FROM water ORDER BY id DESC LIMIT 0, 2;"""
            self.cursor.execute(before_last_row_water1)
            record = self.cursor.fetchall()
            for row in record:
                before_last_row_water = row
            self.before_last_row_water = list(before_last_row_water)

        except UnboundLocalError as error:
            print('Nie ma jeszcze danych w bazie danych, błąd typu:', UnboundLocalError)
            print('Pewnie nie ma jeszcze wpisów w bazie danych, które umożliwią wykonanie polecenia.')
            input('Wciśnij klawisz by kontynuować.')
            choices()

    def get_data_from_queries_last_invoice(self):
        try:
            last_row_invoice1 = """SELECT * FROM water_invoice ORDER BY id DESC LIMIT 0, 1 """
            self.cursor.execute(last_row_invoice1)
            record = self.cursor.fetchall()
            for row in record:
                last_row_invoice = row
            self.last_row_invoice = list(last_row_invoice)

        except UnboundLocalError as error:
            print('Nie ma jeszcze danych w bazie danych, błąd typu:', UnboundLocalError)
            print('Pewnie nie ma jeszcze wpisów w bazie danych, które umożliwią wykonanie polecenia.')
            input('Wciśnij klawisz by kontynuować.')
            choices()

    def get_data_from_queries_before_last_invoice(self):
        try:
            before_last_row_invoice1 = """SELECT * FROM water_invoice ORDER BY id DESC LIMIT 0, 2; """
            self.cursor.execute(before_last_row_invoice1)
            record = self.cursor.fetchall()
            for row in record:
                before_last_row_invoice = row
            self.before_last_row_invoice = list(before_last_row_invoice)

        except UnboundLocalError as error:
            print('Nie ma jeszcze danych w bazie danych, błąd typu:', UnboundLocalError)
            print('Pewnie nie ma jeszcze wpisów w bazie danych, które umożliwią wykonanie polecenia.')
            input('Aby rozliczyć media potrzebujemy wpisanych co najmniej dwóch faktur.')
            choices()

    def okres_rozliczeniowy(self):
        try:
            okres = input(
                'Wybierz okres rozliczeniowy:\n1.Grudzień/Styczeń\n2.Luty/Marzec\n3.Kwiecień/Maj\n4.Czerwiec/Lipiec\n'
                '5.Sierpień/Wrzesień\n6.Październik/Listopad')
            if not okres.isalpha():
                okres = int(okres)
        except ValueError as error:
            print('Value error', error)
        finally:
            if okres == 1:
                okres_rozliczeniowy = ('Grudzień/Styczeń')
            elif okres == 2:
                okres_rozliczeniowy = ('Luty/Marzec')
            elif okres == 3:
                okres_rozliczeniowy = ('Kwiecień/Maj')
            elif okres == 4:
                okres_rozliczeniowy = ('Czerwiec/Lipiec')
            elif okres == 5:
                okres_rozliczeniowy = ('Sierpień/Wrzesień')
            elif okres == 6:
                okres_rozliczeniowy = ('Październik/Listopad')
            return okres_rozliczeniowy

    def water_meter_values(self):
        # pobieram dane z poprzednich faktur, by obliczyć faktyczne zużycie mediów
        self.get_data_from_queries_last_water()
        # NADAJĘ ZMIENNE BY WPISAĆ DO BAZY DANYCH
        okres_rozliczeniowy = MediaMeter.okres_rozliczeniowy(self)
        # dzień dzisiejszy
        dzien_dzisiejszy = self.todays_date
        # DOM WODA LICZNIK
        dom_woda_licznik = int(input('Wpisz stan licznika DOM: '))
        # GORA WODA LICZNIK
        gora_woda_licznik = int(input('Wpisz stan licznika GÓRA: '))
        # GABINET WODA LICZNIK
        gabinet_woda_licznik = int(input('Wpisz stan licznika GABINET: '))
        # DOM_WODA_ZUZYCIE

        try:
            ab = self.last_row_water[3]
            print('ab', ab)
            print('dom woda licznik', dom_woda_licznik)
            dom_woda_zuzycie = dom_woda_licznik - ab
            # GORA_WODA_ZUZYCIE
            bb = self.last_row_water[4]
            gora_woda_zuzycie = gora_woda_licznik - bb
            # GABINET WODA ZUZYCIE
            cb = self.last_row_water[5]
            gabinet_woda_zuzycie = gabinet_woda_licznik - cb
            # DÓŁ WODA ZUZYCIE
            dol_woda_zuzycie = dom_woda_zuzycie - (gora_woda_zuzycie + gabinet_woda_zuzycie)
        except AttributeError as error:
            dom_woda_zuzycie = input('Podaj zużycie wody dla całego domu.')
            gora_woda_zuzycie = input('Podaj zużycie wody dla gory.')
            gabinet_woda_zuzycie = input('Podaj zużycie wody dla gabinetu.')
            dol_woda_zuzycie = input('Podaj zużycie wody dla dołu - Mikołaj.')

        check = str(input('Czy dane zostały wprowadzone poprawnie? T/N: '))
        if check == 'T' or check == 't':
            MediaMeter.water_db_insert_values(self, okres_rozliczeniowy, dzien_dzisiejszy, dom_woda_licznik,
                                              gora_woda_licznik, gabinet_woda_licznik, dom_woda_zuzycie,
                                              gora_woda_zuzycie, gabinet_woda_zuzycie, dol_woda_zuzycie)
        elif check == 'N' or check == 'n':
            MediaMeter.water_meter_values()

    def water_db_insert_values(self, a, b, c, d, e, f, g, h, i):
        sqlite_insert_query = """INSERT INTO water (okres_rozliczeniowy, todays_date, dom_woda_licznik,
        gora_woda_licznik, gabinet_woda_licznik, dom_woda_zuzycie,
        gora_woda_zuzycie, gabinet_woda_zuzycie, dol_woda_zuzycie) VALUES (?,?,?,?,?,?,?,?,?);"""
        data_tuple = (a, b, c, d, e, f, g, h, i)
        self.cursor.execute(sqlite_insert_query, data_tuple)
        self.conn.commit()
        print('Row added')
        # self.water_payment_values()

    def water_invoice_values(self):
        okres_rozliczeniowy = MediaMeter.okres_rozliczeniowy(self)
        # dzień dzisiejszy
        dzien_dzisiejszy = self.todays_date
        # data otrzymania faktury
        while True:
            try:
                data_otrzymania_faktury = input('Wpisz datę otrzymania faktury |rok-msc-dzien|')
                check = datetime.strptime(data_otrzymania_faktury, "%Y-%m-%d")
                break
            except ValueError as error:
                print(error, '. Wpisz właściwy format.')
        # woda_zuzycie_m3
        while True:
            woda_zuzycie_m3 = input('Wpisz zużycie wody (stan jak na liczniku): ')
            if woda_zuzycie_m3.isdigit():
                break
        # woda_koszt_za_1m3
        while True:
            woda_koszt_za_1m3 = input('Woda, koszt za 1m3: ')
            if not woda_koszt_za_1m3.isalpha():
                woda_koszt_za_1m3 = float(woda_koszt_za_1m3.replace(',', '.'))
                break
        # woda_ilość_abonamentów
        while True:
            woda_ilosc_abonamentow = input('Ilość abonamentów: ')
            if woda_ilosc_abonamentow.isdigit():
                break
        # woda_koszt_1_abonament
        while True:
            woda_koszt_1_abonament = input('Woda, koszt abonamentu: ')
            if not woda_koszt_1_abonament.isalpha():
                woda_koszt_1_abonament = float(woda_koszt_1_abonament.replace(',', '.'))
                break
        # scieki_zuzycie_m3
        while True:
            scieki_zuzycie_m3 = input('Wpisz zużycie scieki (stan jak na liczniku): ')
            if scieki_zuzycie_m3.isdigit():
                break
        # scieki_koszt_za_1m3
        while True:
            scieki_koszt_za_1m3 = input('Scieki, koszt za 1m3: ')
            if not scieki_koszt_za_1m3.isalpha():
                scieki_koszt_za_1m3 = float(scieki_koszt_za_1m3.replace(',', '.'))
                break
        # scieki_ilość_abonamentów
        while True:
            scieki_ilosc_abonamentow = input('Ilość abonamentów: ')
            if scieki_ilosc_abonamentow.isdigit():
                break
        # scieki_koszt_1_abonament
        while True:
            scieki_koszt_1_abonament = input('Ścieki, koszt abonamentu: ')
            if not scieki_koszt_1_abonament.isalpha():
                scieki_koszt_1_abonament = scieki_koszt_1_abonament.replace(',', '.')
                break
        # do zaplaty netto
        while True:
            do_zaplaty_netto = input('Całość do zapłaty, netto: ')
            if not do_zaplaty_netto.isalpha():
                do_zaplaty_netto = do_zaplaty_netto.replace(',', '.')
                break
        # status faktury -  opłacona?
        oplacona = False

        # self.dane_wprowadzone_poprawnie()

        check = str(input('Czy dane zostały wprowadzone poprawnie? T/N: '))
        if check == 'T' or check == 't':
            MediaMeter.water_invoice_insert_values(self, okres_rozliczeniowy, dzien_dzisiejszy, data_otrzymania_faktury,
                                                   woda_zuzycie_m3, woda_koszt_za_1m3, woda_ilosc_abonamentow,
                                                   woda_koszt_1_abonament, scieki_zuzycie_m3, scieki_koszt_za_1m3,
                                                   scieki_ilosc_abonamentow, scieki_koszt_1_abonament, do_zaplaty_netto,
                                                   oplacona)
        elif check == 'N' or check == 'n':
            MediaMeter.water_invoice_values(self)

        self.woda_koszt_za_1m3 = woda_koszt_za_1m3
        self.woda_zuzycie_m3 = woda_zuzycie_m3
        self.woda_ilosc_abonamentow = woda_ilosc_abonamentow

    def water_invoice_insert_values(self, a, b, c, d, e, f, g, h, i, j, k, l, m):
        sqlite_insert_query = """INSERT INTO water_invoice (okres_rozliczeniowy, dzien_dzisiejszy, data_otrzymania_faktury,
                                                   woda_zuzycie_m3, woda_koszt_za_1m3, woda_ilosc_abonamentow,
                                                   woda_koszt_1_abonament, scieki_zuzycie_m3, scieki_koszt_za_1m3,
                                                   scieki_ilosc_abonamentow, scieki_koszt_1_abonament, do_zaplaty, 
                                                   oplacona)
         VALUES
         (?,?,?,?,?,?,?,?,?,?,?,?,?);"""
        data_tuple = (a, b, c, d, e, f, g, h, i, j, k, l, m)
        self.cursor.execute(sqlite_insert_query, data_tuple)
        self.conn.commit()
        print('Row added')

    def water_payment_values(self):
        # WPISZ ROZLICZENIE MEDIÓW
        try:
            self.get_data_from_queries_last_water()
        except AttributeError as error:
            input('Najpierw dodaj zużycie wody.')
            choices()
        try:
            self.get_data_from_queries_last_invoice()
            m3_cena = self.last_row_invoice[5]  # cena za 1m3 wody
            n3_cena = self.last_row_invoice[9]  # cena za 1m3 ścieki

            w_koszt_gora = round(self.last_row_water[7] * m3_cena, 2)
            w_koszt_gabinet = round(self.last_row_water[8] * m3_cena, 2)
            w_koszt_dol = round(self.last_row_water[9] * m3_cena, 2)
            s_koszt_gora = round(self.last_row_water[7] * n3_cena, 2)
            s_koszt_gabinet = round(self.last_row_water[8] * n3_cena, 2)
            s_koszt_dol = round(self.last_row_water[9] * n3_cena, 2)
            w_koszt_abon = self.last_row_invoice[6] * self.last_row_invoice[7] / 3
            s_koszt_abon = self.last_row_invoice[11] * self.last_row_invoice[10] / 3

            gora_do_zaplaty = round((w_koszt_gora + w_koszt_abon) * 1.08 + (s_koszt_gora + s_koszt_abon) * 1.08, 2)
            gora_oplacony = False

            gabinet_do_zaplaty = round(
                (w_koszt_gabinet + w_koszt_abon) * 1.08 + (s_koszt_gabinet + s_koszt_abon) * 1.08, 2)
            gabinet_oplacony = False

            dol_do_zaplaty = round((w_koszt_dol + w_koszt_abon) * 1.08 + (s_koszt_dol + s_koszt_abon) * 1.08, 2)
            dol_oplacony = False

        except AttributeError as error:
            input('Pierwsze rozliczenie w całości wpiszemy ręcznie.')

            gora_do_zaplaty = int(input('Góra do zapłaty: '))
            gora_oplacony = False

            gabinet_do_zaplaty = int(input('Gabinet do zapłaty: '))
            gabinet_oplacony = False

            dol_do_zaplaty = int(input('Dół do zapłaty: '))
            dol_oplacony = False

        okres_rozliczeniowy = MediaMeter.okres_rozliczeniowy(self)
        dzien_dzisiejszy = self.todays_date

        check = str(input('Czy dane zostały wprowadzone poprawnie? T/N: '))
        if check == 'T' or check == 't':
            MediaMeter.payments_db_insert_values(self, okres_rozliczeniowy, dzien_dzisiejszy, gora_do_zaplaty,
                                                 gora_oplacony, gabinet_do_zaplaty, gabinet_oplacony, dol_do_zaplaty,
                                                 dol_oplacony)
        elif check == 'N' or check == 'n':
            MediaMeter.water_payment_values()

    def payments_db_insert_values(self, a, b, c, d, e, f, g, h):
        sqlite_insert_query = """INSERT INTO payments (okres_rozliczeniowy, todays_date, gora_do_zaplaty, gora_oplacona,
                                                    gabinet_do_zaplaty, gabinet_oplacony, dol_do_zaplaty, dol_oplacony)
                 VALUES
                 (?,?,?,?,?,?,?,?);"""
        data_tuple = (a, b, c, d, e, f, g, h)
        self.cursor.execute(sqlite_insert_query, data_tuple)
        self.conn.commit()
        print('Row added')

    def get_all_media_meter(self):
        list = ['id', 'okres rozliczeniowy', 'dzien dzisiejszy', 'woda licznik dom', 'woda licznik gora',
                'woda licznik gabinet', 'woda zuzycie caly dom', 'woda zuzycie gora', 'woda zuzycie gabinet',
                'woda zuzycie dol']

        sqlite_count_query = """SELECT COUNT(*) FROM water"""
        self.cursor.execute(sqlite_count_query)
        count = self.cursor.fetchone()
        for e in count:
            if e > 0:
                try:
                    sqlite_select_query = """SELECT * FROM water"""
                    self.cursor.execute(sqlite_select_query)
                    records = self.cursor.fetchall()
                    n = 0
                    for row in records:
                        print(f'ZUŻYCIE: ')
                        for e in row:
                            print(f'{list[n]}: {e}')
                            n += 1
                        n = 0
                        input('Wciśnij enter by kontynuować.')
                        print('\n' * 50)
                except sqlite3.Error as error:
                    print("Failed to read data from sqlite table", error)
            else:
                print('Nie ma jeszcze wpisów w "stany liczników"')
                input('Wciśnij jakiś klawisz. Najlepiej enter. Raz lub dwa.')

    def get_all_invoice(self):
        list = ['id', 'okres_rozliczeniowy', 'dzien_dzisiejszy', 'data_otrzymania_faktury', 'woda_zuzycie_m3',
                'woda_koszt_za_1m3', 'woda_ilosc_abonamentow', 'woda_koszt_1_abonament', 'scieki_zuzycie_m3',
                'scieki_koszt_za_1m3', 'scieki_ilosc_abonamentow', 'scieki_koszt_1_abonament', 'do_zaplaty', 'oplacona']

        sqlite_count_query = """SELECT COUNT(*) FROM water_invoice"""
        self.cursor.execute(sqlite_count_query)
        count = self.cursor.fetchone()
        for e in count:
            if e > 0:
                try:
                    sqlite_select_query = """SELECT * FROM water_invoice"""
                    self.cursor.execute(sqlite_select_query)
                    records = self.cursor.fetchall()
                    n = 0
                    for row in records:
                        print(f'FAKTURA: ')
                        for e in row:
                            print(f'{list[n]}: {e}')
                            n += 1
                        n = 0
                        input('Wciśnij enter by kontynuować.')
                        print('\n' * 50)
                except sqlite3.Error as error:
                    print("Failed to read data from sqlite table", error)
            else:
                print('Nie ma jeszcze wpisów w "faktury"')
                input('Wciśnij jakiś klawisz. Najlepiej enter. Raz lub dwa.')

    def get_all_payments(self):
        list = ['id', 'okres_rozliczeniowy', 'todays_date', 'gora_do_zaplaty', 'gora_oplacona',
                'gabinet_do_zaplaty', 'gabinet_oplacony', 'dol_do_zaplaty', 'dol_oplacony']
        sqlite_count_query = """SELECT COUNT(*) FROM payments"""
        self.cursor.execute(sqlite_count_query)
        count = self.cursor.fetchone()
        for e in count:
            if e > 0:
                try:
                    sqlite_select_query = """SELECT * FROM payments"""
                    self.cursor.execute(sqlite_select_query)
                    records = self.cursor.fetchall()
                    n = 0
                    for row in records:
                        print(f'ROZLICZENIE MEDIÓW: ')
                        for e in row:
                            if e == 1:
                                print(f'{list[n]}: Opłacony')
                            elif e == 0:
                                print(f'{list[n]}: Nieopłacony')
                            else:
                                print(f'{list[n]}: {e}')
                            n += 1
                        n = 0
                        input('Wciśnij enter by kontynuować.')
                        print('\n' * 50)
                except sqlite3.Error as error:
                    print("Failed to read data from sqlite table", error)
            else:
                print('Nie ma jeszcze wpisów w "ROZLICZENIE MEDIÓW"')
                input('Wciśnij jakiś klawisz. Najlepiej enter. Raz lub dwa.')

    def check_if_exists(self, select_id):
        sqlite_count_query = """SELECT COUNT(*) FROM payments WHERE id = ?"""
        data_tuple = (select_id,)
        self.cursor.execute(sqlite_count_query, data_tuple)
        count = self.cursor.fetchone()
        for e in count:
            if e == 1:
                continue
            else:
                print('Nie ma jeszcze wpisów w "ROZLICZENIE MEDIÓW"')
                input('Wciśnij jakiś klawisz. Najlepiej enter. Raz lub dwa.')
                choices()

    def potwierdzenie_oplacenia_faktury(self):
        select_id = input('Podaj id rozliczenia, które chcesz zmodyfikować i wciśnij "enter".')
        self.check_if_exists(select_id)
        gora_oplacona = input('Czy góra została opłacona? t/n')
        dol_oplacony = input('Czy dół został opłacony? t/n')
        gabinet_oplacony = input('Czy gabinet został opłacony? t/n')

        if gora_oplacona == 'T' or gora_oplacona == 't':
            gora_oplacona1 = True
        else:
            gora_oplacona1 = False

        if gabinet_oplacony == 'T' or gora_oplacona == 't':
            gabinet_oplacony1 = True
        else:
            gabinet_oplacony1 = False

        if dol_oplacony == 'T' or dol_oplacony == 't':
            dol_oplacony1 = True
        else:
            dol_oplacony1 = False

        sqlite_insert_query = """UPDATE payments SET gora_oplacona = ?, gabinet_oplacony = ?, dol_oplacony = ?
        WHERE id = ?;"""
        data_tuple = (gora_oplacona1, gabinet_oplacony1, dol_oplacony1, select_id)
        self.cursor.execute(sqlite_insert_query, data_tuple)
        self.conn.commit()
        print('Dane zostały zmienione')
        input('Wciśnij jakiś klawisz')

    def print_faktura(self):
        self.get_data_from_queries_last_water()
        self.get_data_from_queries_last_invoice()
        self.get_data_from_queries_before_last_invoice()
        # pandas https://www.geeksforgeeks.org/python-pandas-dataframe/
        # define a dictionary:
        # Define a dictionary containing employee data

        m3_cena = self.last_row_invoice[5]  # cena za 1m3 wody
        n3_cena = self.last_row_invoice[9]  # cena za 1m3 ścieki
        woda_zuzycie_stok = self.last_row_invoice[4] - self.before_last_row_invoice[4]
        w_koszt_gora = round(self.last_row_water[7] * m3_cena, 2)
        w_koszt_gabinet = round(self.last_row_water[8] * m3_cena, 2)
        w_koszt_dol = round(self.last_row_water[9] * m3_cena, 2)
        s_koszt_gora = round(self.last_row_water[7] * n3_cena, 2)
        s_koszt_gabinet = round(self.last_row_water[8] * n3_cena, 2)
        s_koszt_dol = round(self.last_row_water[9] * n3_cena, 2)
        w_koszt_abon = self.last_row_invoice[6] * self.last_row_invoice[7] / 3
        s_koszt_abon = self.last_row_invoice[11] * self.last_row_invoice[10] / 3

        dane_podstawowe = {'PODMIOT': ['STOK'],
                           '  WODA-KOSZT-1m3': [f"{m3_cena} zł / 1m3"],
                           '  WODA-ZUŻYCIE': [f"{woda_zuzycie_stok} m3"],
                           '  WODA-KOSZT-CAŁOŚĆ': [f"{woda_zuzycie_stok * m3_cena} zł netto"],
                           '  WODA-ILOŚĆ-ABONAMENTÓW': [self.last_row_invoice[6]],
                           '  WODA-KOSZT-ABONAMENT|*1|': [f"{self.last_row_invoice[7]} zł netto"],
                           '  WODA-KOSZT-ABONAMENT': [
                               f"{self.last_row_invoice[6] * self.last_row_invoice[7]} zł netto"],
                           'ŚCIEKI-KOSZT-1m3': [f"{n3_cena} zł / 1m3"],
                           'ŚCIEKI-ZUŻYCIE': [f"{woda_zuzycie_stok} m3"],
                           'ŚCIEKI-KOSZT-CAŁOŚĆ': [f"{woda_zuzycie_stok * n3_cena} zł netto"],
                           'ŚCIEKI-ILOŚĆ-ABONAMENTÓW': [self.last_row_invoice[10]],
                           'ŚCIEKI-KOSZT-ABONAMENT|*1|': [f'{self.last_row_invoice[11]} zł netto'],
                           'ŚCIEKI-KOSZT-ABONAMENT': [
                               f"{self.last_row_invoice[10] * self.last_row_invoice[11]} zł netto"]
                           }

        faktura = {'PODMIOT': ['GÓRA', 'GABINET', 'DÓŁ'],
                   '  WODA-ZUŻYCIE': [f"{self.last_row_water[7]} m3", f"{self.last_row_water[8]} m3",
                                      f"{self.last_row_water[9]} m3"],
                   '  WODA-KOSZT': [f"{w_koszt_gora}zł",
                                    f"{w_koszt_gabinet}zł",
                                    f"{w_koszt_dol}zł"],
                   '  WODA-KOSZT-ABON.-NA-LOKAL': [w_koszt_abon, w_koszt_abon, w_koszt_abon],
                   'W-RAZEM-NETTO': [f"{round(w_koszt_gora + w_koszt_abon, 2)}zł",
                                     f"{round(w_koszt_gabinet + w_koszt_abon, 2)}zł",
                                     f"{round(w_koszt_dol + w_koszt_abon, 2)}zł"],
                   'W-RAZEM-BRUTTO': [f"{round((w_koszt_gora + w_koszt_abon) * 1.08, 2)}zł",
                                      f"{round((w_koszt_gabinet + w_koszt_abon) * 1.08, 2)}zł",
                                      f"{round((w_koszt_dol + w_koszt_abon) * 1.08, 2)}zł"],

                   'ŚCIEKI-ZUŻYCIE': [f"{self.last_row_water[7]} m3", f"{self.last_row_water[8]} m3",
                                      f"{self.last_row_water[9]} m3"],
                   'ŚCIEKI-KOSZT': [f"{s_koszt_gora}zł",
                                    f"{s_koszt_gabinet}zł",
                                    f"{s_koszt_dol}zł"],
                   'ŚCIEKI-KOSZT-ABON.-NA-LOKAL': [s_koszt_abon, s_koszt_abon, s_koszt_abon],
                   'S-RAZEM-NETTO': [f"{round(s_koszt_gora + s_koszt_abon, 2)}zł",
                                     f"{round(s_koszt_gabinet + s_koszt_abon, 2)}zł",
                                     f"{round(s_koszt_dol + s_koszt_abon, 2)}zł"],
                   'S-RAZEM-BRUTTO': [f"{round((s_koszt_gora + s_koszt_abon) * 1.08, 2)}zł",
                                      f"{round((s_koszt_gabinet + s_koszt_abon) * 1.08, 2)}zł",
                                      f"{round((s_koszt_dol + s_koszt_abon) * 1.08, 2)}zł"],

                   'SUMA-DO-ZAPŁATY': [
                       f"{round((w_koszt_gora + w_koszt_abon) * 1.08 + (s_koszt_gora + s_koszt_abon) * 1.08, 2)}zł",
                       f"{round((w_koszt_gabinet + w_koszt_abon) * 1.08 + (s_koszt_gabinet + s_koszt_abon) * 1.08, 2)}zł",
                       f"{round((w_koszt_dol + w_koszt_abon) * 1.08 + (s_koszt_dol + s_koszt_abon) * 1.08, 2)}zł"]

                   }

        # Convert the dictionary into DataFrame
        df = pd.DataFrame(faktura)
        df1 = pd.DataFrame(dane_podstawowe)
        pd.set_option('display.max_rows', 12)
        pd.set_option('display.max_columns', 50)
        pd.set_option('display.width', 700)

        # select columns
        print('\n\033[1mWODA - dane cały stok:\033[0m')
        print(df1[[
            'PODMIOT', '  WODA-KOSZT-1m3', '  WODA-ZUŻYCIE', '  WODA-KOSZT-CAŁOŚĆ', '  WODA-ILOŚĆ-ABONAMENTÓW',
            '  WODA-KOSZT-ABONAMENT|*1|', '  WODA-KOSZT-ABONAMENT',
        ]])
        print('\n\033[1mŚCIEKI - dane cały stok:\033[0m')
        print(df1[[
            'PODMIOT', 'ŚCIEKI-KOSZT-1m3', 'ŚCIEKI-ZUŻYCIE', 'ŚCIEKI-KOSZT-CAŁOŚĆ', 'ŚCIEKI-ILOŚĆ-ABONAMENTÓW',
            'ŚCIEKI-KOSZT-ABONAMENT|*1|', 'ŚCIEKI-KOSZT-ABONAMENT'
        ]])

        print('\n\033[1mWODA - podział kosztów:\033[0m')
        print(df[['PODMIOT', '  WODA-ZUŻYCIE', '  WODA-KOSZT', '  WODA-KOSZT-ABON.-NA-LOKAL', 'W-RAZEM-NETTO']])

        print('\n\033[1mŚCIEKI - podział kosztów:\033[0m')
        print(df[['PODMIOT', 'ŚCIEKI-ZUŻYCIE', 'ŚCIEKI-KOSZT', 'ŚCIEKI-KOSZT-ABON.-NA-LOKAL', 'S-RAZEM-NETTO']])

        print('\n\033[1mDO ZAPŁATY:\033[0m')
        print(df[['PODMIOT', 'W-RAZEM-BRUTTO', 'S-RAZEM-BRUTTO', 'SUMA-DO-ZAPŁATY']])
        input('press enter')

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
            print("The SQLite connection is closed")

    def drop_databases_payments(self):
        dropTableStatement = "DROP TABLE payments"
        self.cursor.execute(dropTableStatement)

    def drop_databases_water(self):
        dropTableStatement = "DROP TABLE water"
        self.cursor.execute(dropTableStatement)

    def drop_databases_water_invoice(self):
        dropTableStatement = "DROP TABLE water_invoice"
        self.cursor.execute(dropTableStatement)


def choices():
    choice = 0
    while choice != 10:
        print('\n' * 50)
        print('Witaj w kalkulatorze opłat za media - WODA.\nWybierz:\n'
              '1.Stany liczników - ARCHIWUM.\n'
              '2.Faktury - ARCHIWUM\n'
              '3.Rozliczenia - ARCHIWUM\n'
              '4.Wpisz dane LICZNIKÓW.\n'
              '5.Wpisz dane FAKTURY\n'
              '6.Wpisz ROZLICZENIE MEDIÓW.\n'
              '7.Wydruk rozliczenia dla najemców.\n'
              '8.Powierdzenie opłacenia FAKTURY.\n'
              '9.ZAKOŃCZ PROGRAM.\n'
              '10.DROP DATABASES - payments.'
              '11.DROP DATABASES - water.'
              '12.DROP DATABASES - water_invoice.'
              )

        choice = input()
        if choice == '1':
            water.get_all_media_meter()
        elif choice == '2':
            water.get_all_invoice()
        elif choice == '3':
            water.get_all_payments()
        elif choice == '4':
            water.water_meter_values()
        elif choice == '5':
            water.water_invoice_values()
        elif choice == '6':
            water.water_payment_values()
        elif choice == '7':
            water.print_faktura()
        elif choice == '8':
            water.potwierdzenie_oplacenia_faktury()
        elif choice == '9':
            sqlite3.connect("water.db").close()
            sys.exit()
        elif choice == '10':
            water.drop_databases_payments()
        elif choice == '11':
            water.drop_databases_water()
        elif choice == '12':
            water.drop_databases_water_invoice()
        else:
            continue


# doubled functions
def get_all_invoice_():
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


if __name__ == '__main__':
    water_database()
    water_invoice_database()
    payments_database()
    water = MediaMeter()
    choices()
