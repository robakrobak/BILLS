import sqlite3


def payments_database():
    conn = sqlite3.connect(("water.db"))
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        okres_rozliczeniowy VARCHAR,
        todays_date VARCHAR,
        gora_do_zaplaty INTEGER,
        gora_oplacona BOOLEAN,
        gabinet_do_zaplaty INTEGER,
        gabinet_oplacony BOOLEAN,
        dol_do_zaplaty INTEGER,
        dol_oplacony BOOLEAN,
        FOREIGN KEY (okres_rozliczeniowy) REFERENCES water_invoice(okres_rozliczeniowy))
        """)


def water_database():
    conn = sqlite3.connect("water.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS water(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        okres_rozliczeniowy TEXT,
        todays_date DATE,
        dom_woda_licznik INTEGER,
        gora_woda_licznik INTEGER,
        gabinet_woda_licznik INTEGER,
        dom_woda_zuzycie INTEGER,
        gora_woda_zuzycie INTEGER,
        gabinet_woda_zuzycie INTEGER,
        dol_woda_zuzycie INTEGER)
        """)


def water_invoice_database():
    conn = sqlite3.connect("water.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS water_invoice(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        okres_rozliczeniowy VARCHAR,
        dzien_dzisiejszy DATE,
        data_otrzymania_faktury DATE, 
        woda_zuzycie_m3 INTEGER,
        woda_koszt_za_1m3 FLOAT,
        woda_ilosc_abonamentow INTEGER,
        woda_koszt_1_abonament FLOAT,
        scieki_zuzycie_m3 INTEGER,
        scieki_koszt_za_1m3 FLOAT,
        scieki_ilosc_abonamentow INTEGER,
        scieki_koszt_1_abonament FLOAT,
        do_zaplaty FLOAT,
        oplacona BOOLEAN
        )
        """)
