"""
    PDF merger functions.
    
    Author: Csaba Szilárd Rácz
    Github: https://github.com/Szyli/pdf-merger
"""

import Tkinter
import tkFileDialog
import os
import glob
import PyPDF2
import re

def TakeInput() -> list[str]:
    print('Give source.')
    # gather input file locations
    # type check of input
    root = Tkinter.Tk()
    root.withdraw() #use to hide tkinter window

    currdir = os.getcwd()
    file = tkFileDialog.askopenfile(parent=root, mode='rb',
                                    initialdir=currdir,
                                    title='Please select files to merge.')
    
    if file != None:
        data = file.read()
        file.close()
        print("I got %d bytes from this file." % len(data))
    
    
    # basic saving using file manager
    return data
    
def PdfMerger(pdfs: list[str], destination: str):
    """
    This function saves the final pdf given the order of pdfs.
    
    Args:
        pdfs (list[str]): the list of all the pdfs' location in the system
        destination (str): the location where the final pdf is saved
    """
    
    pdfMerge = PyPDF2.PdfMerger()

    for pdf in pdfs:
        pdfMerge.append(pdf, pages=(0,-1))

    with open(destination, 'wb') as file:
        pdfMerge.write(file)
        
    # check if successful
    

def test():
    print("Test ran.")

if __name__ == "__main__":
    test()