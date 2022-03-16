from time import sleep
import tkinter as tk
from tkinter import messagebox
from turtle import width

from invest_simulator import InvestSimulator, KonecSimulace


class SimulatorGUI:
    """Třída s grafickým rozhraním implementující InvestSimulator"""

    def __init__(self, *args, **kwargs):
        self.sim = InvestSimulator(*args, **kwargs)
        self.sim = InvestSimulator(*args, **kwargs)
        self.app = tk.Tk()
        self.app.geometry("400x300")

        self.strvar_datum = tk.StringVar(self.app)
        self.lbl_datum = tk.Label(
            self.app, textvariable=self.strvar_datum, pady=5)
        self.lbl_datum.place(anchor="ne", relx=0.975)

        self.frame_state = tk.Label(self.app)
        self.frame_state.place(anchor="nw", relx=0.05, y=10)

        self.strvar_hotovost = tk.StringVar(self.app)
        self.lbl_hotovost = tk.Label(
            self.frame_state, textvariable=self.strvar_hotovost, font="Helvetica 10 bold")
        self.lbl_hotovost.pack(anchor="w")

        self.strvar_hodnota = tk.StringVar(self.app)
        self.lbl_hodnota = tk.Label(
            self.frame_state, textvariable=self.strvar_hodnota)
        self.lbl_hodnota.pack(anchor="w")

        self.frame_cena = tk.Frame(self.app)
        self.frame_cena.place(relx=0.5, rely=0.3, anchor="center")

        self.lbl_cena_ = tk.Label(
            self.frame_cena, text="Current market price:")
        self.lbl_cena_.pack()

        self.strvar_cena = tk.StringVar(self.app)
        self.lbl_cena = tk.Label(
            self.frame_cena, textvariable=self.strvar_cena, font="Helvetica 11 bold")
        self.lbl_cena.pack()
        """ 
        self.btn_dalsi_den = tk.Button(self.app, text="Další den", command=self.dalsi_den_click)
        self.btn_dalsi_den.pack()
        """
        self.btn_nakup = tk.Button(
            self.app, text="Nakup", command=self.btn_nakup_click, font="Helvetica 11 bold")
        self.btn_nakup.place(relx=0.5, rely=0.5, anchor="center")

        self.btn_autorun = tk.Button(
            self.app, text="Autorun", command=self.btn_autorun_click, font="Helvetica 9 bold")
        self.btn_autorun.place(relx=0.5, rely=0.63, anchor="center")

        self.frame_speed = tk.Frame(self.app)
        self.frame_speed.place(relx=0.5, rely=0.71, anchor="center")

        self.lbl_speed = tk.Label(self.frame_speed, text="Speed:")
        self.lbl_speed.pack(side="left")

        self.strvar_speed = tk.StringVar(value=30)
        self.spnbox_speed = tk.Spinbox(
            self.frame_speed, from_=1, to=500, textvariable=self.strvar_speed, width=4)
        self.spnbox_speed.pack(side="left")

    def run(self):
        self.update()
        self.app.mainloop()

    def update(self):
        self.strvar_datum.set(self.sim.datum.strftime("%#d. %#m. %Y"))
        self.strvar_hotovost.set(
            "Cash: $" + str(round(self.sim.hotovost)))
        self.strvar_hodnota.set(f"Portfolio Value: ${self.sim.hodnota:.1f}")
        self.strvar_cena.set(f"${self.sim.cena:.2f}")

    """ 
    def dalsi_den_click(self):
        self.sim.dalsi_den()
        self.update()
    """

    def btn_nakup_click(self):
        self.sim.nakup()
        self.update()

    def btn_autorun_click(self):
        self.continue_autorun = True
        self.btn_autorun.config(
            command=self.btn_autorun_cancel_click, text="Pause Autorun")
        self.autorun()

    def autorun(self):
        try:
            self.sim.dalsi_den()
        except KonecSimulace:
            self.konec_simulace()
            return

        self.update()
        if self.continue_autorun:
            self.app.after(
                1000 // (int(self.strvar_speed.get()) + 1) + 1, self.autorun)

    def btn_autorun_cancel_click(self):
        self.continue_autorun = False
        self.btn_autorun.config(command=self.btn_autorun_click, text="Autorun")

    def konec_simulace(self):
        self.btn_autorun.destroy()
        messagebox.showinfo(message="Konec simulace!")


if __name__ == "__main__":
    data = InvestSimulator.vytvor_data_csv("data.csv", "%m/%d/%Y")
    root = SimulatorGUI(data, 1200, zacatek="2013-02-01")
    root.run()
