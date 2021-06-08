import tkinter as tk
from tkinter import ttk
import numpy as np


class CompoundTag(ttk.Frame):
    """It is the visual information of the compound name, formula, max and min temperatures"""
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent)
        self['style'] = 'Background.TFrame'
        self.c_name = tk.StringVar()
        self.c_formula = tk.StringVar()
        self.max = tk.StringVar()
        self.min = tk.StringVar()

        self.update(controller)

        compound_name = ttk.Label(self,
                                  textvariable=self.c_name,
                                  style='AppText.TLabel'
                                  )
        compound_name.grid(row=0, column=0, sticky='W', padx=(10, 10))

        compound_formula = ttk.Label(self,
                                     textvariable=self.c_formula,
                                     style='AppText.TLabel'
                                     )
        compound_formula.grid(row=0, column=1, sticky='W', padx=(10, 10))

        max_display = ttk.Label(self, textvariable=self.max, style='AppText.TLabel')
        min_display = ttk.Label(self, textvariable=self.min, style='AppText.TLabel')
        max_display.grid(row=0, column=2, sticky='E', padx=(10, 10))
        min_display.grid(row=0, column=3, sticky='E', padx=(10, 10))

    def update(self, controller):
        """Updates the labels"""
        self.c_name.set('Name: ' + controller.compound_name.get())
        self.c_formula.set('Formula: ' + controller.compound_formula.get())
        self.max.set('Max: ' + str(controller.max))
        self.min.set('Min: ' + str(controller.min))


class ConstantsFrame(ttk.Frame):
    """Visual information of the Antoine's equation constants"""
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self['style']='Background.TFrame'
        self.a_v = tk.StringVar()
        self.b_v = tk.StringVar()
        self.c_v = tk.StringVar()
        self.update(controller)

        a_label = ttk.Label(self, text='A=', style='AppText.TLabel')
        b_label = ttk.Label(self, text='B=', style='AppText.TLabel')
        c_label = ttk.Label(self, text='C=', style='AppText.TLabel')
        a_value = ttk.Label(self, textvariable=self.a_v, style='AppText.TLabel')
        b_value = ttk.Label(self, textvariable=self.b_v, style='AppText.TLabel')
        c_value = ttk.Label(self, textvariable=self.c_v, style='AppText.TLabel')
        a_label.grid(row=0, column=0)
        b_label.grid(row=0, column=2)
        c_label.grid(row=0, column=4)
        a_value.grid(row=0, column=1, padx=(0, 10))
        b_value.grid(row=0, column=3, padx=(0, 10))
        c_value.grid(row=0, column=5, padx=(0, 10))

    def update(self, controller):
        """Updates the values of the antoine's constants"""
        self.a_v.set(controller.A)
        self.b_v.set(controller.B)
        self.c_v.set(controller.C)


class InformationFrame(ttk.Frame):
    """Info of the units used in the equation"""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, **kwargs)
        self['style']='Background.TFrame'
        pressure_label = ttk.Label(self, text='P=Pressure (mmHg)', style='AppText.TLabel')
        temperature_label = ttk.Label(self, text='T=Temperature (K)', style='AppText.TLabel')
        pressure_label.grid(row=1, column=0)
        temperature_label.grid(row=1, column=1)


class EntryTab(ttk.Frame):
    """Where the user enter a value to calculate the pressure and temperature"""
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self['style']='Background.TFrame'
        self.p_value = tk.StringVar()
        self.p_value.set('760')
        self.t_value = tk.StringVar()
        self.t_value.set('298.15')

        self.p_out = tk.StringVar()
        self.p_out.set('---')
        self.t_out = tk.StringVar()
        self.t_out.set('---')
        p_entry_label = ttk.Label(self, text='P', style='AppText.TLabel')
        t_entry_label = ttk.Label(self, text='T', style='AppText.TLabel')

        p_input = ttk.Entry(self, width=10, textvariable=self.p_value)
        t_input = ttk.Entry(self, width=10, textvariable=self.t_value)
        t_label = ttk.Label(self, text='-->  Tsat =', style='AppText.TLabel')
        p_label = ttk.Label(self, text='-->  Psat =', style='AppText.TLabel')

        p_output = ttk.Entry(self, width=10, textvariable=self.p_out)
        t_output = ttk.Entry(self, width=10, textvariable=self.t_out)

        t_calculate = ttk.Button(self,
                                 text='Calculate',
                                 command=lambda: self.antoine_t(controller))
        p_calculate = ttk.Button(self,
                                 text='Calculate',
                                 command=lambda: self.antoine_p(controller))

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

    def antoine_p(self, controller):
        """It receives a temperature and calculates the saturation pressure"""
        A = float(controller.A.replace(',', '.'))
        B = float(controller.B.replace(',', '.'))
        C = float(controller.C.replace(',', '.'))
        T = float(self.t_value.get())
        pressure = f'{np.exp(A - B / (C + T)):.3f}'
        self.p_out.set(pressure)

    def antoine_t(self, controller):
        """It receives a pressure and returns the saturation temperature"""
        A = float(controller.A.replace(',', '.'))
        B = float(controller.B.replace(',', '.'))
        C = float(controller.C.replace(',', '.'))
        P = float(self.p_value.get())
        temperature = f'{B / (A - np.log(P)) - C:.3f}'
        self.t_out.set(temperature)
