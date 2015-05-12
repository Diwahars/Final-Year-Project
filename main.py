import Tkinter as tk
import Tkinter as tk
import os
import tkMessageBox
from PIL import Image,ImageTk
import MySQLdb
import nltk
import time, sys, re, pickle
import ttk
import product as pro

def getproducts():
        lines = [line.strip() for line in open(os.path.join("Files",'products.txt'))]
        return lines

            

class SelectProduct(tk.Frame):
    def __init__(self, selprod):

        tk.Frame.__init__(self, selprod)
        self.canvas = tk.Canvas(selprod, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(selprod, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.OnFrameConfigure)

        self.populate()

    def populate(self):
                proname=getproducts()
                prolabel=[]
                tk.Label(self.frame,text="WELCOME, PLEASE SELECT A PRODUCT").grid(row=0,column=0,columnspan=10)
                for i in range(len(proname)):
                        prolabel.append(tk.Button(self.frame,text=proname[i],command=self.clickProduct(proname[i])))
                        prolabel[i].grid(row=i+1,column=1,padx=190,pady=10)
    def clickProduct(self,name):
                def _clickProduct():
                        pro.run(name)
                return _clickProduct
                
                        
                        
    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    selprod=tk.Tk()
    selprod.title("Product Select")    
    selprod.geometry('{}x{}'.format(550, 450))    
    SelectProduct(selprod).pack(side="top", fill="both", expand=True)
    selprod.mainloop()
