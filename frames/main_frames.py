from .support_frames import *
from PIL import Image, ImageTk
import pandas as pd


class App(tk.Tk):
    """The main root of the app, it also stores some constants used in the Antoine's equation"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry('600x400')
        self.title('Antoine App')
        self.columnconfigure(0, weight=1)
        self.antoine_table = pd.read_csv('assets/antoine_list_df.csv', index_col=0)

        #Initialing some constants and vars
        self.compound = tk.StringVar()
        self.compound.set('Water')
        self.compound_name = tk.StringVar()
        self.compound_formula = tk.StringVar()

        self.A = 0
        self.B = 0
        self.C = 0
        self.max = 0
        self.min = 0

        container = ttk.Frame(self)
        container.pack(expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        #Creating the command to switch the windows of the app
        self.frames = {}
        for F in (AntoineFrame, MainWindow, NotFoundWindow):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('MainWindow')

        self.bind('<Return>', lambda x: self.frames['MainWindow'].search(self))
        self.bind("<BackSpace>", lambda x: self.show_frame('MainWindow'))

    def show_frame(self, page_name):
        """It shows the frame that it is called by raising it"""
        frame = self.frames[page_name]
        frame.tkraise()

    def update(self):
        """Updates the constants and the labels of the AntoineFrame for the
        values entered by the user in the main window"""
        self.frames['AntoineFrame'].update_frames(controller=self)


class MainWindow(ttk.Frame):
    """Main Window where the user search for the compound by name or formula"""
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.option = tk.StringVar()

        compound_label = ttk.Label(self, text='Search by:')
        compound_label.grid(row=0, column=0)

        self.compound_box = ttk.Combobox(
            self,
            textvariable=self.option,
            state='readonly',
            values=['Compound Name', 'Compound Formula']
        )
        self.compound_box.current(0)
        self.compound_box.grid(row=1, column=0, sticky='EW', padx=(25, 10))

        self.input_search = ttk.Entry(self, textvariable=controller.compound)
        self.input_search.grid(row=1, column=1, sticky='EW', padx=(0, 25))

        search_button = ttk.Button(self, text='Search', command=lambda: self.search(controller=controller))
        search_button.grid(row=2, column=0, columnspan=2, pady=(20, 20))

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
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.compound_tag = CompoundTag(self, controller)
        self.compound_tag.grid(row=1, column=0, columnspan=2, sticky='EW')

        equation_image = Image.open('assets/equation.png')
        equation_photo = ImageTk.PhotoImage(equation_image)

        equation_label = ttk.Label(self, image=equation_photo)
        equation_label.image = equation_photo
        equation_label.grid(row=0, column=0, columnspan=2, pady=(30, 30))

        self.constants_frame = ConstantsFrame(self, controller)
        self.constants_frame.grid(row=2, column=0, columnspan=2)

        information_frame = InformationFrame(self)
        information_frame.grid(row=3, column=0, columnspan=2)

        entry_frame = EntryTab(self, controller)
        entry_frame.grid(row=4, column=0, columnspan=2)

        back_button = ttk.Button(self,
                                 text='Back',
                                 command=lambda: controller.show_frame('MainWindow'))
        back_button.grid(row=5, column=0, columnspan=2, pady=(10, 10))

    def update_frames(self, controller):
        """Updates the labels and constant values"""
        self.compound_tag.update(controller)
        self.constants_frame.update(controller)


class NotFoundWindow(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.label = ttk.Label(self, text='Could not found your compound')
        self.label.configure(anchor='center')
        self.label.grid(row=0, column=0, sticky='NSEW')

        self.button = ttk.Button(self, text='Back', command=lambda: controller.show_frame('MainWindow'))
        self.button.grid(row=1, column=0)



