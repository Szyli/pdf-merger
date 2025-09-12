"""
    This project aims to build a simple python based application with the sole purpose of merging pdfs.
    
    Author: Csaba Szilárd Rácz
    Github: https://github.com/Szyli/pdf-merger
"""

# ------IMPORTS------

# import numpy as np
import tkinter
# import tkinter.filedialog
from customtkinter import *
# import os
# import glob
import PyPDF2

# ------BASICS------

def TakeInput() -> (tuple[str, ...] | str):
    """
    This function opens the system's file manager for the user to select the desired pdf files.
    
    Returns:
        file_names (tuple[str]): the list of file locations
    """
    # TODO: type check of input
    root = tkinter.Tk()
    # root.withdraw() # use to hide tkinter window

    file_names = filedialog.askopenfilenames(title='Please select pdf files to merge.')
    root.destroy()
    
    return file_names
    
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

class DisplayFrame(CTkFrame):
    """
    This frame displays the selected files and updates when new ones are selected.
    """
    def __init__(self, master):
        super().__init__(master)
        self.label = CTkLabel(self, text="The selected the pdf files will appear here.", font=("Ariel", 18))
        self.label.pack(pady=20)

    def update_label(self, new_text: tuple[str]) -> None:
        """
        Update the label in this frame with new text.
        
        Args:
            new_text (tuple[str]): The list of file locations
        """
        fls = []    # file names
        for fl in new_text:
            # strip the file names from the full path for clear display
            fls.append(fl.split('/')[-1])
            
        self.label.configure(text=fls)

class TitleFrame(CTkFrame):
    """
    This frame is the "welcoming" title line.
    """
    def __init__(self, master):
        super().__init__(master)
        
        CTkLabel(self,text="Select pdf files to merge them into a single pdf!",
                font=("Ariel", 22),corner_radius=5,fg_color="#0058B5",
                height=40).grid(row=0, column=0,
                                padx=0, pady=(10,0),
                                sticky="nwe", columnspan=2)

class OptionsFrame(CTkFrame):
    """
    This frame holds the buttons the user can interact with:
        - Select files button
        - Merge button
    """
    def __init__(self, master):
        super().__init__(master)
        self.storage = ()
        
        # select input button
        input_button = CTkButton(self,text="Select files",font=("Ariel",20),
                                fg_color="#0058B5", command=self.input_button_callback)
        input_button.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        # add button (for additional files)
        add_button = CTkButton(self,text="Add more files",font=("Ariel",20),
                                fg_color="#0058B5", command=self.input_button_callback)
        add_button.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        # merger button
        merger_button = CTkButton(self,text="Merge",
                                font=("Ariel",20),fg_color="#B5004B",
                                command=self.merger_button_callback)
        merger_button.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        
        
    def input_button_callback(self):
        """
        Callback to print a message on the adjacent frame i.e.
        print out the names of the selected files.
        """
        
        self.storage = TakeInput()
        self.display_frame.update_label(self.storage)
        
    def add_button_callback(self):
        """
        Callback to print a message on the adjacent frame i.e.
        print out the names of the selected files.
        """
        
        self.storage = TakeInput()
        self.display_frame.update_label(self.storage)
    # TODO: Add button for "Add" if any is already selected
    
    def merger_button_callback(self):
        """
        Executes the pdf merging and asks the user for the destination of the new file.
        """
        # TODO: define file name
        
        folder_selected = filedialog.askdirectory()
        PdfMerger(pdfs=self.storage, destination=folder_selected+"/merged_pdf.pdf")
        self.display_frame.update_label("merge was sucesful")
        
# class PDFViewer():
#     root = CTk()
#     root.geometry("700x600")
#     pdf_frame = CTkPDFViewer(root, file="my_file.pdf")
#     pdf_frame.pack(fill="both", expand=True, padx=10, pady=10)
#     root.mainloop()

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
        self.attributes("-topmost", True)  # sets above every other window

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
        self.options_frame.grid(row=1, column=0, padx=10, pady=(10, 0),
                                sticky="nsw")
        
        self.display_frame = DisplayFrame(self)
        self.display_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Link the frames
        self.options_frame.display_frame = self.display_frame

# ------Running------

# creating application window
root = App()
# running window
root.mainloop()

