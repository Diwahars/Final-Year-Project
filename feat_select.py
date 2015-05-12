import Tkinter as tk
import os
import tkMessageBox
from PIL import Image,ImageTk
import MySQLdb
import nltk
import time, sys, re, pickle
import ttk
from nltk.corpus import wordnet as wn
import review_display as rd

adj=[]
positive=[]
negative=[]

def update_progress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "="*block + " "*(barLength-block), round(progress,2)*100, status)
    sys.stdout.write(str(round(progress,2)*100))
    sys.stdout.flush()

def classifyadj():
	global positive
	global negative
	b = r'(\s|^|$)' 
	size=len(adj)
	for i in range(size):
			#checking if the adj is not present in positive and negative
			if((adj[i].lower() not in positive) and (adj[i].lower() not in negative)):
				#checking if adjective is present in positive synset
				for j in range(len(positive)):
					for synset in wn.synsets(positive[j]):
						for lemma in synset.lemmas():
							if bool(re.match(b + re.escape(adj[i]) + b, lemma.name(), flags=re.IGNORECASE)):							
								positive.append(adj[i])
				
				#checking if adjective is present in positive synset
				for k in range(len(negative)):
					for synset in wn.synsets(negative[k]):
						for lemma in synset.lemmas():
							if bool(re.match(b + re.escape(adj[i]) + b, lemma.name(), flags=re.IGNORECASE)):							
								negative.append(adj[i])
			#update_progress(i/(float)(size))
			

	#removing possible duplicates
	positive=list(set(positive))
	negative=list(set(negative))
	#writing updated positive and negative
	pickle.dump(positive,open(os.path.join("Files","positive.txt"),"w"))
	pickle.dump(negative,open(os.path.join("Files","negative.txt"),"w"))



pos_check=0
neg_check=0

def wordOrientation(word,sentence,value):
	negation=["not","but","yet","non","no","except"]
	flag=0
	check=0
	for i in range(len(negation)):
		p=re.compile("\\b"+negation[i]+"\\b")
		if p.search(sentence.lower())>0:
			check=1
			break
	if(check==1):
		neg=negation[i]
	elif(check==0):
		neg="`"
	count=0
	indexes= [m.start() for m in re.finditer(neg,sentence)]
	for i in range(len(indexes)):
		flag=0
		start=sentence.find(word)
		end=indexes[i]
		count=0
		if start>end:
			temp=start
			start=end
			end=temp
		for j in range(start,end):
			if(sentence[j] in " "):
				count+=1
		if count in range(1,4):
			flag=1
	if flag==1 and ((value==1 and pos_check==0) or (value==-1 and neg_check==0)):
		return -value
	else:
		return value
positive_sent=[]
negative_sent=[]	
orient_pos=[]
orient_neg=[]
star_rating=[]
def classifyreviews(features_sentence):
	#print feature
	feature=pickle.load(open(os.path.join("Files","feat_select.txt")))
	creview=[]
	#features_sentence=pickle.load(open(os.path.join("Files","features_sentence.txt")))
	for x in range(len(feature)):
		positive_sent=[]
		negative_sent=[]	
		orient_pos=[]
		orient_neg=[]
		for i in range(len(feature)):
			if features_sentence[i][0] in feature[x]:
				for j in range(len(features_sentence[i])-1):
					orientation=0
					pos_check=0
					neg_check=0
					for k in range(len(positive)):
						p=re.compile("\\b"+positive[k]+"\\b")
						if p.search(features_sentence[i][j+1].lower())>0:
							orientation+=wordOrientation(positive[k],features_sentence[i][j+1],1)
							pos_check=1
					for k in range(len(negative)):
						p=re.compile("\\b"+negative[k]+"\\b")
						if p.search(features_sentence[i][j+1].lower())>0:
							orientation+=wordOrientation(negative[k],features_sentence[i][j+1],-1)
							neg_check=1
					if orientation>0:
						positive_sent.append(features_sentence[i][j+1])
						orient_pos.append(orientation)
					if orientation<0:
						negative_sent.append(features_sentence[i][j+1])
						orient_neg.append(orientation)
		creview.append(feature[x])
		creview.append(positive_sent)
		creview.append(orient_pos)
		creview.append(negative_sent)
		creview.append(orient_neg)
		no_pos=float(len(positive_sent))
		no_neg=float(len(negative_sent))
		#maximum=no_pos+no_neg
		#minimum=no_pos if no_pos<no_neg else no_neg
		#star=((no_pos-minimum)/(maximum-minimum))*(5.0)	
		star=(no_pos*5.0)/(no_pos+no_neg)
		star_rating.append(star)
	pickle.dump(creview,open(os.path.join("Files","reviews.txt"),"w"))
	return creview
def select_review(creview,sel_feature):
	feature=pickle.load(open(os.path.join("Files","feat_select.txt")))
	size=len(feature)*5
	for i in range(0,size,5):
		if sel_feature in creview[i]:
			index=i
			break
	sel_pos= creview[i+1]
	sel_neg= creview[i+3]
	return (sel_pos,sel_neg)

def select_summary(creview):
	feature=pickle.load(open(os.path.join("Files","feat_select.txt")))
	size=len(feature)*5
	pos_summary=[]
	neg_summary=[]
	for i in range(0,size,5):
		index= list(set(sorted(creview[i+2])))
		if index:
			index=index[-1]
		b = [item for item in range(len(creview[i+2])) if creview[i+2][item] == index]
		for j in range(len(b)):
			pos_summary.append(creview[i+1][b[j]])
	
	pos_summary=list(set(pos_summary))
	
	for i in range(0,size,5):
		index= sorted(list(set(creview[i+4])),reverse=True)
		if index:
			index=index[-1]
		b = [item for item in range(len(creview[i+4])) if creview[i+4][item] == index]
		for j in range(len(b)):
			neg_summary.append(creview[i+3][b[j]])

	neg_summary=list(set(neg_summary))
	return (pos_summary,neg_summary)

class Feat_Select(tk.Frame):
    def __init__(self, second_win,selectpid,creview):
        tk.Frame.__init__(self, second_win)
        self.canvas = tk.Canvas(second_win, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(second_win, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",tags="self.frame")
        self.frame.bind("<Configure>", self.OnFrameConfigure)
        self.selectpid=selectpid
        self.creview=creview
        self.populate()
        
    def selectFeature(self,name):
		def _selectFeature():
			self.sel_pos,self.sel_neg=select_review(self.creview,name)
			self.display_review(name)			
		return _selectFeature

    def selectSummary(self):
		def _selectSummary():
			self.sel_pos,self.sel_neg=select_summary(self.creview)
			self.display_review("Summary")			
		return _selectSummary
		
	
    def populate(self):
		#classifyadj()
		feature=pickle.load(open(os.path.join("Files","feat_select.txt")))
		self.featbutton=[]
		self.star_label=[]
		image=Image.open(os.path.join("Images",self.selectpid+".jpeg"))
		(width,height)=image.size
		p=ImageTk.PhotoImage(image)		
		self.pimage=tk.Label(self.frame,image=p)
		self.pimage.image=p
		self.pimage.grid(row=0,column=0,rowspan=width,columnspan=height,sticky=tk.W)
		self.summarybutton=tk.Button(self.frame,text="View Summary",command=self.selectSummary())
		self.summarybutton.grid(row=0,column=2,padx=(width+50,20),pady=5)
		self.flabel=tk.Label(self.frame,text="Select Feature")
		self.flabel.grid(row=1,column=2,padx=(width+50,20),pady=5)
		self.rlabel=tk.Label(self.frame,text="Rating(5)")
		self.rlabel.grid(row=1,column=3,pady=5)
		
		for i,name in enumerate(feature):
			self.featbutton.append(tk.Button(self.frame,text=name,command=self.selectFeature(name)))
			self.featbutton[i].grid(row=i+2,column=2,padx=(width+50,20),pady=5)
			self.star_label.append(tk.Label(self.frame,text=str(round(star_rating[i],2))))
			self.star_label[i].grid(row=i+2,column=3,pady=5,sticky=tk.W)
			
    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def display_review(self,name):
		rd.run(self.sel_pos,self.sel_neg,name)
	
def run(selectpid,spname,featsent):
	global adj
	global positive
	global negative
	adj=pickle.load(open(os.path.join("Files","adjectives.txt")))
	positive=pickle.load(open(os.path.join("Files","positive.txt")))
	negative=pickle.load(open(os.path.join("Files","negative.txt")))

	second_win=tk.Toplevel()	
	second_win.title(spname)
	#second_win.protocol("WM_DELETE_WINDOW",destroy_button(second_win))
	#second_win.geometry('{}x{}'.format(750, 550))
	second_win.attributes('-zoomed', True)
	print "Classifying Reviews"
	creview=classifyreviews(featsent)
	Feat_Select(second_win,selectpid,creview).pack(side="top", fill="both", expand=True)
	second_win.mainloop()
