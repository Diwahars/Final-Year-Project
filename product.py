import Tkinter as tk
import os
import tkMessageBox
from PIL import Image,ImageTk
import MySQLdb
import nltk
import time, sys, re, pickle
import ttk
import feat_select as fs

def processReviews(pid,self):
	reviews=getReviews(pid)
	adjectives=[]
	featsent=[]
	self.progress.pack(side=tk.BOTTOM)
	self.progress["value"] = 0
	self.progress["maximum"] = 100	
	self.proglabel.pack_forget()
	for r in range(0,len(reviews)):
		#sentence tokeniztion
		sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
		#first review for first pid
		text=reviews[r][0]
		text = unicode(text, 'utf-8')
		text=re.sub("\.+",". ",text)
		sentence=sent_detector.tokenize(text.strip())
		#looping to check if any of the features is present in the review sentences
		sentences=[]
		for i in range(0,len(features)):
			featsent.append([])
			for j in range(0,len(sentence)):
				if(features[i] in sentence[j]):
					#print "feature:  "+features[i]+"\n"+"sentence: "+sentence[j]+"\n"
					sentences.append(sentence[j])
					if(features[i] not in featsent[i]):
						featsent[i].append(features[i])
					featsent[i].append(sentence[j])
						
		
		for i in range(0,len(sentences)):
			tokens=nltk.word_tokenize(sentences[i])
			tagged= nltk.pos_tag(tokens)
			for item in tagged:
				if (item[1] == 'JJ'):
					#print sentences[i]
					#print item[0]
					adjectives.append(item[0])				
			#print "\n"
		self.parent.update_idletasks()
		self.progress["value"] =(r/(float)(len(reviews)))*100
		


	adjectives=list(set(adjectives))
	adj=[]
	#removing stopwords from opnions
	size=len(adjectives)
	for i in range(size):
		if("." in adjectives[i]):
			t=adjectives[i].split(".");
			for j in range(len(t)):
				if t[j]:
					t[j]=nltk.word_tokenize(t[j])
					tag= nltk.pos_tag(t[j])
					for item in tag:
						if (item[1] == 'JJ'):
							adj.append(item[0])
		if("-" in adjectives[i]):
			t=adjectives[i].split("-");
			for j in range(len(t)):
				if t[j]:
					t[j]=nltk.word_tokenize(t[j])
					tag= nltk.pos_tag(t[j])
					for item in tag:
						if (item[1] == 'JJ'):
							adj.append(item[0])
		if("," in adjectives[i]):
			t=adjectives[i].split(",");
			for j in range(len(t)):
				if t[j]:
					t[j]=nltk.word_tokenize(t[j])
					tag= nltk.pos_tag(t[j])
					for item in tag:
						if (item[1] == 'JJ'):
							adj.append(item[0])
		if("/" in adjectives[i]):
			t=adjectives[i].split("/");
			for j in range(len(t)):
				if t[j]:
					t[j]=nltk.word_tokenize(t[j])
					tag= nltk.pos_tag(t[j])
					for item in tag:
						if (item[1] == 'JJ'):
							adj.append(item[0])
		else:
			adj.append(adjectives[i])
	pickle.dump(featsent,open(os.path.join("Files","features_sentence.txt"),"w"))
	pickle.dump(adj,open(os.path.join("Files","adjectives.txt"),"w"))
	return featsent


def callback(i,spname,self): 
	def _callback():
		global features
		global selectpid
		flag=tkMessageBox.askquestion( "Do you want to continue?","Selected product:"+pname[i] )
		if flag=="yes":
			selectpid=button[i].config('text')[-1]
			for j in range(0,len(file_read),2):
				if(file_read[j][0] in selectpid):
					features=file_read[j+1]
					break
			#print features
			pickle.dump(features,open(os.path.join("Files","feat_select.txt"),"w"))
			featsent=processReviews(selectpid,self)
			self.progress["value"] = 0
			self.proglabel.pack(side=tk.BOTTOM)
			self.progress.pack_forget()
			self.parent.update_idletasks()
			self.proglabel.pack_forget()
			fs.run(selectpid,spname,featsent)
	return _callback


def getReviews(pid):
	sql = "SELECT `review` FROM `product_review` WHERE `pid` = " + `pid` +";"
	try:
		cursor.execute(sql)
		rows = cursor.fetchall()
	except:
		print "Pid : ",pid," not found"
		return
	return rows

def getProducts():
	d=[]
	for i in range(len(pid)):
		sql="SELECT `pid`,`pname` FROM `product_details` WHERE `pid` = " + `pid[i]` +";"
		try:
			cursor.execute(sql)
			rows = cursor.fetchall()
			d.append(rows)
		except:
			print "not found"
			return
	return d

def searchProduct(name):
	rows=[]
	if " " in name:
		name=name.split(" ")
		for i in range(len(pname)):
			count=0
			for j in range(len(name)):
				if name[j].lower() in pname[i].lower():	
					count+=1
			if count==len(name):
				rows.append(pid[i])
				rows.append(pname[i])				
	else:
		for i in range(len(pname)):
			if name.lower() in pname[i].lower():	
				rows.append(pid[i])
				rows.append(pname[i])

	return rows

class Product(tk.Frame):
	
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, borderwidth=0)
        self.stext = tk.StringVar()

        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((10,10), window=self.frame, anchor="nw",tags="self.frame")
        self.frame.bind("<Configure>", self.OnFrameConfigure)
        self.parent=root
                
        self.progress = ttk.Progressbar(self, orient="horizontal",length=200, mode="determinate")
        self.proglabel=tk.Label(self,text="Classifying Reviews",font=20)
		
        self.populate()
        		
    def populate(self):
		row=2
		col=0
		row1=3
		tk.Label(self.frame,text="Search Bar:").grid(row=0,column=1)
		self.sbar=tk.Entry(self.frame,textvariable=self.stext)
		self.sbar.grid(row=0,column=2,pady=10,sticky=tk.W)
		sbutton=tk.Button(self.frame,text="Search",command=self.clickSearch())
		sbutton.grid(row=0,column=3)
		for i,name in enumerate(pid):
			image.append(Image.open(os.path.join("Images",pid[i]+".jpeg")))
			(width,height)=image[i].size
			width=int(width*0.45)
			height=int(height*0.45)
			image[i]=image[i].resize((width,height),Image.ANTIALIAS)
			photo.append(ImageTk.PhotoImage(image[i]))
			button.append(tk.Button(self.frame, image=photo[i],text=name,command=callback(i,pname[i],self)))			
			if(col>4):
				row+=2
				row1+=2
				col=0
			col+=1
			button[i].grid(row=row, column=col,padx=35,pady=25)
			label.append(tk.Label(self.frame,text=pname[i]))
			label[i].grid(row=row1,column=col)

    def search_populate(self,spid,spname):
		indices=[]
		row=2
		col=0
		row1=3
		self.sbar.delete(0,tk.END)
		self.backbutton=tk.Button(self.frame,text="<- Back",command=self.back())
		self.backbutton.grid(row=0,column=1,padx=35)
		for i in range(0,len(spid)):
			indices.append(pid.index(spid[i]))
		for i in range(len(spid)):
			if(col>4):
				row+=2
				row1+=2
				col=0
			col+=1
			button[indices[i]].grid(row=row,column=col,padx=35,pady=25)
			label[indices[i]].grid(row=row1,column=col)
    
    def OnFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def clickSearch(self): 
		def _clickSearch():
			pname=[]
			pid=[]
			name=self.stext.get()
			if name:
				tuples=searchProduct(name)
				for i in range(1,len(tuples),2):
					pname.append(tuples[i])
				for i in range(0,len(tuples),2):
					pid.append(tuples[i])
				for i in range(0,len(button)):
					button[i].grid_forget()
					label[i].grid_forget()
				self.search_populate(pid,pname)
		return _clickSearch 
    
    def back(self):
		def _back():
			self.backbutton.grid_forget()
			row=2
			row1=3
			col=0
			for i in range(len(button)):
				button[i].grid_forget()
				label[i].grid_forget()
			for i in range(0,len(button)):
				if(col>4):
					row+=2
					row1+=2
					col=0
				col+=1
				button[i].grid(row=row,column=col,padx=35,pady=25)
				label[i].grid(row=row1,column=col)
		return _back
			
def run(name):
	global cursor,pid,pname,file_read,button,image,photo,label,features,selectpid,reviews	
	file_read=[]
	pid=[]
	button=[]
	image=[]
	photo=[]
	label=[]
	pname=[]
	features=[]
	selectpid=""
	reviews=""
	db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="product_"+name.replace(" ","").lower())
	cursor = db.cursor()
	with open(os.path.join("Files/Features",name+'.txt')) as f:
		for line in f:
			line = line.split() # to deal with blank 
			if line:            # to skip blank lines
				line = [i for i in line]
				file_read.append(line)
	for i in range(0,len(file_read),2):
		pid.append(file_read[i][0])

	#return all products in db
	tuples=getProducts()
	for i in range(0,len(tuples)):
		pname.append(tuples[i][0][1])
	root=tk.Toplevel()
	root.title("Select "+name[0:len(name)-1])
	root.attributes('-zoomed', True)
	Product(root).pack(side="top", fill="both", expand=True)
	root.mainloop()
