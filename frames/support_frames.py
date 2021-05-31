import tkinter as tk
from tkinter import ttk
import numpy as np


class CompoundTag(ttk.Frame):
    """It is the visual information of the compound name, formula, max and min temperatures"""
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent)
        self.c_name = tk.StringVar()
        self.c_formula = tk.StringVar()
        self.max = tk.StringVar()
        self.min = tk.StringVar()

        self.update(controller)

        compound_name = ttk.Label(self, textvariable=self.c_name)
        compound_name.grid(row=0, column=0, sticky='W', padx=(10, 10))

        compound_formula = ttk.Label(self, textvariable=self.c_formula)
        compound_formula.grid(row=0, column=1, sticky='W', padx=(10, 10))

        max_display = ttk.Label(self, textvariable=self.max)
        min_display = ttk.Label(self, textvariable=self.min)
        max_display.grid(row=0, column=2, sticky='E', padx=(10, 10))
        min_display.grid(row=0, column=3, sticky='E', padx=(10, 10))

    def update(self, controller):
        """Updates the labels"""
        self.c_name.set('Name: ' + controller.compound.get())
        self.c_formula.set('Formula: ' + controller.compound_formula.get())
        self.max.set('Max: ' + str(controller.max))
        self.min.set('Min: ' + str(controller.min))


class ConstantsFrame(ttk.Frame):
    """Visual information of the Antoine's equation constants"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.a_v = tk.StringVar()
        self.b_v = tk.StringVar()
        self.c_v = tk.StringVar()
        self.update(parent)

        a_label = ttk.Label(self, text='A=')
        b_label = ttk.Label(self, text='B=')
        c_label = ttk.Label(self, text='C=')
        a_value = ttk.Label(self, textvariable=self.a_v)
        b_value = ttk.Label(self, textvariable=self.b_v)
        c_value = ttk.Label(self, textvariable=self.c_v)
        a_label.grid(row=0, column=0)
        b_label.grid(row=0, column=2)
        c_label.grid(row=0, column=4)
        a_value.grid(row=0, column=1, padx=(0, 10))
        b_value.grid(row=0, column=3, padx=(0, 10))
        c_value.grid(row=0, column=5, padx=(0, 10))

    def update(self, parent):
        """Updates the values of the antoine's constants"""
        self.a_v.set(parent.A)
        self.b_v.set(parent.B)
        self.c_v.set(parent.C)


class InformationFrame(ttk.Frame):
    """Info of the units used in the equation"""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, **kwargs)
        pressure_label = ttk.Label(self, text='P=Pressure (mmHg)')
        temperature_label = ttk.Label(self, text='T=Temperature (K)')
        pressure_label.grid(row=1, column=0)
        temperature_label.grid(row=1, column=1)


class EntryTab(ttk.Frame):
    """Where the user enter a value to calculate the pressure and temperature"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.p_value = tk.StringVar()
        self.p_value.set('760')
        self.t_value = tk.StringVar()
        self.t_value.set('298.15')

        self.p_out = tk.StringVar()
        self.p_out.set('---')
        self.t_out = tk.StringVar()
        self.t_out.set('---')
        p_entry_label = ttk.Label(self, text='P')
        t_entry_label = ttk.Label(self, text='T')

        p_input = ttk.Entry(self, width=10, textvariable=self.p_value)
        t_input = ttk.Entry(self, width=10, textvariable=self.t_value)
        t_label = ttk.Label(self, text='-->  Tsat =')
        p_label = ttk.Label(self, text='-->  Psat =')

        p_output = ttk.Entry(self, width=10, textvariable=self.p_out)
        t_output = ttk.Entry(self, width=10, textvariable=self.t_out)

        t_calculate = ttk.Button(self, text='Calculate', command=lambda: self.antoine_t(parent))
        p_calculate = ttk.Button(self, text='Calculate', command=lambda: self.antoine_p(parent))

        p_entry_label.grid(row=0, column=0)
        p_input.grid(row=0, column=1)
        t_label.grid(row=0, column=2)
        t_output.grid(row=0, column=3)
        t_calculate.grid(row=0, column=4, padx=(10, 10))

        t_entry_label.grid(row=1, column=0)
        t_input.grid(row=1, column=1)
        p_label.grid(row=1, column=2)
        p_output.grid(row=1, column=3)
        p_calculate.grid(row=1, column=4, padx=(10, 10))

    def antoine_p(self, parent):
        """It receives a temperature and calculates the saturation pressure"""
        A = float(parent.A.replace(',', '.'))
        B = float(parent.B.replace(',', '.'))
        C = float(parent.C.replace(',', '.'))
        T = float(self.t_value.get())
        pressure = f'{np.exp(A - B / (C + T)):.3f}'
        self.p_out.set(pressure)

    def antoine_t(self, parent):
        """It receives a pressure and returns the saturation temperature"""
        A = float(parent.A.replace(',', '.'))
        B = float(parent.B.replace(',', '.'))
        C = float(parent.C.replace(',', '.'))
        P = float(self.p_value.get())
        temperature = f'{B / (A - np.log(P)) - C:.3f}'
        self.t_out.set(temperature)
