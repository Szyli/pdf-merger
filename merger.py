"""
    This project aims to build a simple python based application with the sole purpose of merging pdfs.
    
    Author: Csaba Szilárd Rácz
    Github: https://github.com/Szyli/pdf-merger
"""

# ------IMPORTS------

# import numpy as np
from customtkinter import *
from PIL import Image
import os
import webbrowser
# import glob
import PyPDF2

# ------BASICS------

LABELTEXT: str = "The selected the pdf files will appear here."
TEXTLENLIM: int = 60 # max character length displayed

def TakeInput() -> (list[str]):
    """
    This function opens the system's file manager for the user to select the desired pdf files.
    
    Returns:
        file_names (tuple[str]): the list of file locations
    """
    
    # root = tkinter.Tk()
    # root.withdraw() # use to hide tkinter window

    file_names = filedialog.askopenfilenames(title='Please select pdf files to merge.',
                                            filetypes=[('pdf', '*.pdf')])
    # root.destroy()
    
    return list(file_names)
    
def PdfMerger(pdfs: tuple[str, ...], destination: str) -> None:
    """
    This function saves the final pdf given the order of pdfs.
    
    Args:
        pdfs (tuple[str]): the list of all the pdf locations
        destination (str): the location where the final pdf is saved
    """
    
    pdfMerge = PyPDF2.PdfMerger()

    for pdf in pdfs:
        pdfMerge.append(pdf)

    with open(destination, 'wb') as file:
        pdfMerge.write(file)
        
    # TODO: check if successful

# ------FRAME------

class TitleFrame(CTkFrame):
    """
    This frame is the "welcoming" title line.
    """
    def __init__(self, master):
        super().__init__(master)
        
        CTkLabel(self,text="Select pdf files to merge them into a single pdf",
                font=("Ariel", 22),corner_radius=5,
                height=40).grid(row=0, column=0,
                                padx=(10,10), pady=(10,10),
                                sticky="nwe", columnspan=2)

class BottomFrame(CTkFrame):
    """
    This frame is in the bottom.
    """
    def __init__(self, master):
        super().__init__(master)
        
        CTkLabel(self, text="Checkout the source code on my github:",
                font=("Ariel", 20),corner_radius=5,
                height=20, compound="center").grid(row=4, column=0,
                                padx=(10,10), pady=(10,10))
        
        IMAGE_PATH = "C:/Users/csaba/GitHub/pdf-merger/githublogo.png"
        githublogo = CTkImage(light_image=None,
                            dark_image=Image.open(os.path.join(IMAGE_PATH)),
                            size=(40,40))
        image = CTkButton(self, image=githublogo, text='', height=10, width=10,
                        fg_color='transparent', hover=False,
                        bg_color='transparent', border_color=None,
                        background_corner_colors=None,
                        command=self.open_url)
        image.grid(row=4, column=1, padx=(2,2))
        
    def open_url(self) -> None:
        """
        This function opens the github page dedicated to this project.
        """
        webbrowser.open("www.github.com/Szyli/pdf-merger")

class DisplayFrame(CTkFrame):
    """
    This frame displays the selected files and updates when new ones are selected.
    """
    def __init__(self, master):
        super().__init__(master)
        self.label = CTkLabel(self, text=LABELTEXT,
                            font=("Ariel", 18)) # wraplength=600
        self.label.pack(pady=20)
        # self.label.grid(row=0, column=0, sticky="w")

    def update_label(self, new_text: list[str], initial: bool = False) -> None:
        """
        Update the label in this frame with new text.
        
        Args:
            new_text (tuple[str]): The list of file locations
        """
        
        if not initial:
            fls = ''    # file names
            for fl in new_text:
                # strip the file names from the full path for clear display
                name = fl.split('/')[-1]
                if len(name) > TEXTLENLIM:
                    name = name[:int(TEXTLENLIM/2)] + " [...] " + name[-30:]
                fls += name + "\n"
            self.label.configure(text=fls)
        else:
            self.label.configure(text=new_text)

class OptionsFrame(CTkFrame):
    """
    This frame holds the buttons the user can interact with:
        - Select files button
        - Merge button
    """
    def __init__(self, master) -> None:
        super().__init__(master)
        self.storage = []
        
        # select input button
        self.input_button = CTkButton(self,text="Select files", font=("Ariel",20),
                                fg_color="#0058B5", hover_color="#003976",
                                command=self.input_button_callback)
        self.input_button.grid(row=0, column=0, ipadx=10,
                        padx=(10,10), pady=(10, 0), sticky="EW")
        # add button (for additional files)
        self.add_button = CTkButton(self,text="Add more", font=("Ariel",20),
                                fg_color="#0058B5", hover_color="#003976",
                                hover=True,
                                command=self.add_button_callback, state="disabled")
        self.add_button.grid(row=1, column=0, ipadx=10,
                        padx=10, pady=(10, 0), sticky="w")
        # merger button
        self.merger_button = CTkButton(self,text="Merge", font=("Ariel",20),
                                fg_color="#D50032", hover_color="#6C002D",
                                hover=True,
                                command=self.merger_button_callback, state="disabled")
        self.merger_button.grid(row=2, column=0, ipadx=10,
                           padx=10, pady=(10, 0), sticky="w")
        
    def input_button_callback(self) -> None:
        """
        Callback to print a message on the adjacent frame i.e.
        print out the names of the selected files.
        """
        
        self.storage = TakeInput()
        if self.storage:    # if list is not empty
            self.add_button.configure(state="normal")
            if len(self.storage) >= 2:    # if we have at least two files to merge
                self.merger_button.configure(state="normal")
            else:
                self.merger_button.configure(state="disabled")
            # update label
            self.display_frame.update_label(self.storage)
        else:   # nothing changes from initials / resets to initials when nothing is selected
            self.add_button.configure(state="disabled")
            self.merger_button.configure(state="disabled")
            # reset the label to original text
            self.display_frame.update_label(LABELTEXT, initial=True)
        
    def add_button_callback(self) -> None:
        """
        Callback to extend a message on the adjacent frame i.e.
        print out the names of the newly selected files.
        """
        
        self.storage.extend(TakeInput())   # this is where we add to the data
        if len(self.storage) >= 2:
            self.merger_button.configure(state="normal")
        # else:
        #     self.merger_button.configure(fg_color="#D6647F", hover=False)
        self.display_frame.update_label(self.storage)
    
    def merger_button_callback(self) -> None:
        """
        Executes the pdf merging and asks the user for the destination of the new file.
        """
        
        final_fl = filedialog.asksaveasfilename(defaultextension=".pdf")
        if final_fl:
            PdfMerger(pdfs=self.storage, destination=final_fl)
            self.display_frame.update_label("The merge was successful!", initial=True)
        
class App(CTk):
    """
    This class defines the application window.
    """
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = int(screen_width*3/5)
        height = int(screen_height/2)

        x_coord = int(screen_width/2 - width/2)
        y_coord = int(screen_height/2 - height/2)
        self.geometry("{}x{}+{}+{}".format(width, height, x_coord, y_coord))
        self.attributes("-topmost", False)  # sets above every other window: False

        set_appearance_mode("system")
        set_default_color_theme("blue")

        self.title("PDF merger")
        
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=1)
        
        self.title_frame = TitleFrame(self)
        self.title_frame.grid(row=0, column=0, padx=10, pady=(10, 0),
                                sticky="N", columnspan=2)

        self.options_frame = OptionsFrame(self)
        self.options_frame.grid(row=1, column=0, padx=10, pady=10,
                                sticky="nsw")
        
        self.display_frame = DisplayFrame(self)
        self.display_frame.grid(row=1, column=1, padx=10, pady=10,
                                sticky="nsew")
        
        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.grid(row=2, column=0, padx=(10,10), pady=(10, 10),
                            sticky="sew", columnspan=2)

        # Link the frames
        self.options_frame.display_frame = self.display_frame

# ------Running------

# creating application window
root = App()
# running window
root.mainloop()

