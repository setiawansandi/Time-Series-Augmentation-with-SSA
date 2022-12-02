from tkinter import Tk, Canvas, Entry, Text, PhotoImage, Frame, Label, font
import os
from screen.utils.utils import relative_to_assets

class InputBox(Frame):

    def __init__(self, parent, *, input_no, fe, seperator):
        Frame.__init__(self, parent)
        
        self.parent = parent
        self.ad = "input_box" # asset dir
        self.input_no = input_no
        self.fe = fe

        self.parent.bind('<Return>', self.on_enter) # when enter is pressed

        self.normal_font = font.Font(family="Inter", size=-16)
        small_font = font.Font(family="Inter", size=-14)
        bold_font = font.Font(family="Inter", size=-18, weight="bold")

        self.canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 138,
            width = 404,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.canvas.create_text(
            21.6552734375,
            22.0,
            anchor="nw",
            text="Input file name",
            fill="#000000",
            font=bold_font
        )

        self.canvas.create_text(
            156,
            23.0,
            anchor="nw",
            text="(ignore separator and extension):",
            fill="#000000",
            font=self.normal_font
        )

        self.canvas.create_text(
            22.0,
            48.0478515625,
            anchor="nw",
            text="e.g.: sample_TS_1.csv -> [sample] [TS] [1]",
            fill="#000000",
            font=small_font
        )

        self.load_box(input_no)
        


    def load_box(self, count=3):
        self.box_container = []
        img_container = []
        entry_gap = 0
        img_gap = 0

        self.entry_image_1 = PhotoImage(
                file=relative_to_assets(self.ad, "entry_1.png"))

        for i in range(count):

            img_container.append(
                self.canvas.create_image(
                    74.0 + img_gap,
                    97.5478515625,
                    image=self.entry_image_1
                )
            )
            img_gap += 97.5478 + 29.5 # width + gap

            self.box_container.append(
                Entry(
                    bd=0,
                    bg="#dce7fa",
                    fg="#000716",
                    highlightthickness=0,
                    font=self.normal_font
                )
            ) 

            self.box_container[i].place(
                x=27 + entry_gap,
                y=81,
                width=94.0,
                height=34.0
            )

            if i == 0:
                self.box_container[i].focus()

            entry_gap += 94 + 33 # width + gap
        


    def get_file_name(self):
        return self.file_name
    


    def on_enter(self, event=None):
        from pltSSsur import pltSSsur
        from screen.utils.utils import plotly_gen
        from screen.utils.plotly_viewer import PlotlyViewer

        print("Entered")
        _fn = 'P02_TS_2.csv' # for testing
        _numComp = 3
        file_data, surr_data = pltSSsur(_fn, numComp=_numComp, plot_ok=True, data_dir_path='data')

        
        plotly_gen(file_data, surr_data, _numComp=_numComp, _file_name=_fn)


