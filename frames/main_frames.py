from .support_frames import *
from tkinter import ttk
import tkinter as tk


class MainWindow(ttk.Frame):
    """Main Window where the user search for the compound by name or formula"""
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self['style'] = 'Background.TFrame'
        self.controller = controller
        self.option = tk.StringVar()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        compound_label = ttk.Label(self, text='Search by:', style='AppText.TLabel', justify='right')
        compound_label.grid(row=0, column=0, sticky='EW')

        self.compound_box = ttk.Combobox(
            self,
            textvariable=self.option,
            state='readonly',
            values=['Compound Name', 'Compound Formula']
        )
        self.compound_box.current(0)
        self.compound_box.grid(row=0, column=1, sticky='EW', padx=(0, 10))

        self.input_search = ttk.Entry(self, textvariable=controller.compound)
        self.input_search.grid(row=0, column=2, sticky='EW', padx=(0, 25))

        search_button = ttk.Button(self, text='Search',
                                   style='AppButton.TButton',
                                   command=lambda: self.search(controller=controller))
        search_button.grid(row=2, column=0, columnspan=3, pady=(20, 20), sticky='s')

    def search(self, controller):
        """It searches for the compound requested by the user, then updates the App frame to
        update the values showed on the Labels in the AntoineFrame"""
        self.controller.show_frame('AntoineFrame')
        search_option = self.compound_box.get()
        try:
            if search_option == 'Compound Name':
                self.search_compound(controller, 'Composto')
                controller.update()
            else:
                self.search_compound(controller, 'Formula')
                controller.update()
        except IndexError:
            self.controller.show_frame('NotFoundWindow')

    @staticmethod
    def search_compound(controller, n):
        if n == 'Composto':
            compound_name = controller.compound.get()
            compound_name = compound_name.lower()
            obj = controller.antoine_table.loc[controller.antoine_table[n] == compound_name]
            controller.compound_name.set(compound_name.capitalize())
            controller.compound_formula.set(obj['Formula'].values[0])
        else:
            compound_formula = controller.compound.get()
            compound_formula = compound_formula.upper()
            obj = controller.antoine_table.loc[controller.antoine_table[n] == compound_formula]
            controller.compound.set(compound_formula)
            controller.compound_formula.set(compound_formula)
            controller.compound_name.set(obj['Composto'].values[0].capitalize())

        controller.A = obj['Ant (A)'].values[0]
        controller.B = obj['Ant (B)'].values[0]
        controller.C = obj['Ant (C)'].values[0]
        controller.max = obj['Max'].values[0]
        controller.min = obj['Min'].values[0]


class AntoineFrame(ttk.Frame):
    """The calculator window, here the user enter a value to calculate the saturation temperature or pressure"""
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self['style'] = 'Background.TFrame'
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.compound_tag = CompoundTag(self, controller)
        self.compound_tag.grid(row=1, column=0, columnspan=2, sticky='EW')

        equation_label = ttk.Label(self, image=controller.equation_photo)
        equation_label.image = controller.equation_photo
        equation_label.grid(row=0, column=0, columnspan=2, pady=(30, 30))

        self.constants_frame = ConstantsFrame(self, controller)
        self.constants_frame.grid(row=2, column=0, columnspan=2)

        information_frame = InformationFrame(self)
        information_frame.grid(row=3, column=0, columnspan=2)

        entry_frame = EntryTab(self, controller)
        entry_frame.grid(row=4, column=0, columnspan=2)

        back_button = ttk.Button(self,
                                 text='Back',
                                 style='AppButton.TButton',
                                 command=lambda: controller.show_frame('MainWindow'))
        back_button.grid(row=5, column=0, columnspan=2, pady=(10, 10))

    def update_frames(self, controller):
        """Updates the labels and constant values"""
        self.compound_tag.update(controller)
        self.constants_frame.update(controller)


class NotFoundWindow(ttk.Frame):
    """Window which returns a not found message"""
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self['style'] = 'Background.TFrame'
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.label = ttk.Label(self,
                               text='Could not found your compound!\n'
                                    'Please try again!',
                               justify='center',
                               style='NotFoundText.TLabel')
        self.label.configure(anchor='center')
        self.label.grid(row=0, column=0, sticky='NSEW')

        self.button = ttk.Button(self, text='Back',
                                 style='AppButton.TButton',
                                 command=lambda: controller.show_frame('MainWindow'))
        self.button.grid(row=1, column=0)