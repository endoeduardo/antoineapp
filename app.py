from frames import AntoineFrame
from frames.main_frames import MainWindow
from frames.main_frames import NotFoundWindow
import tkinter as tk
from tkinter import ttk
from os import path
import sys
from PIL import Image, ImageTk
import pandas as pd

COLOR_PRIMARY = '#2e3f4f'
COLOR_SECONDARY = '#293846'
COLOR_LIGHT_BACKGROUND = '#fff'
COLOR_LIGHT_TEXT = '#eee'
COLOR_DARK_TEXT = '#8095a8'


class App(tk.Tk):
    """The main root of the app, it also stores some constants used in the Antoine's equation"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Creating a style
        style = ttk.Style(self)
        style.theme_use('clam')

        style.configure('App.TFrame', background=COLOR_LIGHT_BACKGROUND)
        style.configure('Background.TFrame', background=COLOR_PRIMARY)
        style.configure(
            'AppText.TLabel', background=COLOR_PRIMARY,
            foreground=COLOR_LIGHT_TEXT,
            font='Arial 11'
        )
        style.configure(
            'NotFoundText.TLabel',
            background=COLOR_PRIMARY,
            foreground=COLOR_LIGHT_TEXT,
            font='Arial 20'
            )
        style.configure(
            'AppButton.TButton',
            background=COLOR_SECONDARY,
            foreground=COLOR_LIGHT_TEXT
        )
        #Enables the hoff-over mouse
        style.map(
            'AppButton.TButton',
            background=[('active', COLOR_PRIMARY), ('disabled', COLOR_SECONDARY)]
        )

        self['background'] = COLOR_PRIMARY

        #App settings
        self.geometry('400x300')
        self.title('Antoine App')
        self.columnconfigure(0, weight=1)
        self.load_assets()

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

    def show_frame(self, page_name):
        """It shows the frame that it is called by raising it"""
        frame = self.frames[page_name]
        frame.tkraise()

    def update(self):
        """Updates the constants and the labels of the AntoineFrame for the
        values entered by the user in the main window"""
        self.frames['AntoineFrame'].update_frames(controller=self)

    def load_assets(self):
        try:
            bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))

            path_to_antoine_table = path.join(bundle_dir, 'assets', 'antoine_list_df.csv')
            self.antoine_table = pd.read_csv(path_to_antoine_table, index_col=0)

            self.path_to_equation_image = path.join(bundle_dir, 'assets', 'equation.png')
            equation_image = Image.open(self.path_to_equation_image)
            self.equation_photo = ImageTk.PhotoImage(equation_image)
        except IOError as error:
            print(error)
            self.destroy()


app = App()
app.mainloop()
