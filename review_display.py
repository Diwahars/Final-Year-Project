#import neg_display as nd
import Tkinter as tk
from PIL import Image, ImageTk

class Display(tk.Frame):
    def __init__(self, rev_win,sel_pos,sel_neg,feat_name):

        tk.Frame.__init__(self,rev_win)
        self.canvas = tk.Canvas(rev_win, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(rev_win, orient="vertical", command=self.canvas.yview)
        self.hsb = tk.Scrollbar(rev_win, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.hsb.set)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((10,10), window=self.frame, anchor="nw",tags="self.frame")
        self.frame.bind("<Configure>", self.OnFrameConfigure)
        self.sel_pos=list(set(sel_pos))
        self.sel_neg=list(set(sel_neg))
        self.neglabel=[]
        self.poslabel=[]
        self.parent=rev_win
        self.feat_name=feat_name
        self.initUI()
        self.pos_disp()
	#another python script for new frame to display positive and negative reviews
    def pos_disp(self):
		self.poslabel=[]
		for i in range(len(self.neglabel)):
			self.neglabel[i].grid_forget()
		for i in range(len(self.sel_pos)):
			self.poslabel.append(tk.Label(self.frame,text=self.sel_pos[i],anchor=tk.W))
			self.poslabel[i].grid(row=i,column=0,padx=0,pady=2,sticky=tk.W)
			#print self.sel_pos[i]			
    def neg_disp(self):
		self.neglabel=[]
		for i in range(len(self.poslabel)):
			self.poslabel[i].grid_forget()
		for i in range(len(self.sel_neg)):
			self.neglabel.append(tk.Label(self.frame,text=self.sel_neg[i],anchor=tk.W))
			self.neglabel[i].grid(row=i,column=0,padx=0,pady=2,sticky=tk.W)
			#print self.sel_neg[i]			


    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def initUI(self):
		        
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Positives", command=lambda:self.pos_disp())
        fileMenu.add_command(label="Negatives", command=lambda:self.neg_disp())        
        menubar.add_cascade(label="View", menu=fileMenu)


def run(sel_pos,sel_neg,feat_name):
    rev_win=tk.Toplevel()	
    rev_win.attributes('-zoomed', True)
    rev_win.title(feat_name)
    #rev_win.geometry('{}x{}'.format(750, 550))
    Display(rev_win,sel_pos,sel_neg,feat_name).pack(side="top", fill="both", expand=True)
    rev_win.mainloop()
