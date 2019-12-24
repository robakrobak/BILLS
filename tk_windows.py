import tkinter as tk
from water import MediaMeter
from water import MediaMeter
from water import water_invoice_database, water_database


class MainWindow:  # tworzę klasę tworzącą program
    def __init__(self, master):  # wrzucam w mastera główną funkcję: tk.Tk(), czyli tkinter.Tk() - czyli ROOT
        self.master = master  # self.master jest tkinter.Tk()
        self.windowname = master.wm_title('Rozliczenie Mediów Na Stoku')
        self.master.geometry("300x200")
        self.frame = tk.Frame(self.master)

        self.butnew("WODA", 'blue', Water)  # obiekt Window 1 - klasy Water
        self.butnew("PRĄD", 'red', Current)  # obiekt Window 2 - klasy Prąd
        self.butnew("GAZ", 'orange', Gas)  # obiekt Window 2 - klasy Gaz
        self.frame.pack()

    def butnew(self, text, color, _class):
        tk.Button(self.frame, text=text, fg=color, width=125, command=lambda: self.new_window(_class)).pack()

    def new_window(self, _class):
        self.newWindow = tk.Toplevel(self.master)
        _class(self.newWindow)


class Water:
    def __init__(self, master):
        self.windowname = master.wm_title('WODA')
        self.master = master
        self.master.geometry("800x300")
        self.frame = tk.Frame(self.master)

        self.label = tk.Label(master, text=f"Wybierz opcję:", anchor='w')
        self.label.pack()
        self.get_all_invoice_Button = tk.Button(self.frame, text='Przejrzyj faktury', anchor='w', width=125,
                                                command=lambda: )
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


class Current:
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


class Gas:
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


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    water_database()
    water_invoice_database()
    MediaMeter.water = MediaMeter()
    main()

