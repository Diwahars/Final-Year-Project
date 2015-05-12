from __future__ import division
from numpy import *
import nltk,os
import MySQLdb,pickle
count =0
#init db

selproduct = [line.strip() for line in open(os.path.join("Files",'products.txt'))]
print "Select a product:"
for i in range(0,len(selproduct)):
	print str(i+1)+". "+selproduct[i]
selected=int(input("Enter the product number:"))
selected=selproduct[selected-1]

	
db = MySQLdb.connect(host="localhost", # host
                     user="root", #username
                      passwd="root", #password
                      db="product_"+selected.replace(" ","").lower()) #data base

cursor = db.cursor()

#get set of product ids
productId=[]

#start value - start from 1
start = input("Enter the Start value: ")
start = start - 1
#end value
end = input("Enter the End Value: ")
brl=[]
#sql to fetch desired pids
sql = "SELECT `pid` FROM `product_details` LIMIT "+`start`+","+`end`+";"
cursor.execute(sql)
rows = cursor.fetchall()
#get set of reviews of each product
def getReviews(pid):
	sql = "SELECT `review` FROM `product_review` WHERE `pid` = " + `pid` +";"
	try:
		cursor.execute(sql)
		rows = cursor.fetchall()
	except:
		print "Pid : ",pid," not found"
		return
	return rows
#print nltk.pos_tag(['flipkart','samsung'])

#lemmatiser and stopwords initialization
lemmatizer = nltk.WordNetLemmatizer()
from nltk.corpus import stopwords

#building the stopwords list
stopwords = stopwords.words('english')
stoplist = ['>','<','%','.','br/','(',')','=','!']
for i in stoplist:
	stopwords.append(i)

#normalise each qualified word
def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    word = lemmatizer.lemmatize(word)
    return word

def armAssoc(dust,strength):
	print

def writetofile(l):
	feat=[]
	remove=["flipkart","problem","time","product","awesome","thing","port","delivery","buying","perfect","mode","reason","anything","point","excellent","hand","till","fact","market","weather","brand","life","option","guide","money"]
	for i in range(0,len(l)):		
		if l[i] not in remove:
			feat.append(l[i])
			#print l[i]
	print feat
	f = open(os.path.join("Files/Features",selected+".txt"), "a+")
	global count
	f.write(rows[count][0]+'\n')
	for i in feat: 
		f.write(i+' ')
	f.write('\n')
	count+=1
	f.close()



def armMine(dataset,strength):
	features={}
	#build a list of feature and their strength - dictionary data structure used
	for data in dataset:
		for noun in data:
			#Calculate the frequency
			if(features.has_key(noun)):
				count = features[noun]
				features[noun] = (count + 1)
			else:
				features[noun] = 1
	#length of dataset
	length = len(dataset)
	#filter features based on strength
	dust = []
	for feature in features:
		if (features[feature] / length) >= strength:
			#print feature," ",
			dust.append(feature)
	#more filtering with association rules
	writetofile(dust);
	armAssoc(dust, strength)
	L,supportData=apriori(dataset,0.1)
	brl.append(generateRules(L, supportData,0.1))
	#pickle.dump(brl,open(os.path.join("Files","brl.txt"),"w"))



def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)#use frozen set so we
                            #can use it as a key in a dict

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can):
                	ssCnt[can]=1
                else:
                	ssCnt[can] = ssCnt[can] + 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList, supportData


def aprioriGen(Lk, k): #creates Ck
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
	    #print "L1:",L1
	    #print "L2:",L2
	    #compare the first items to avoid duplicate
            if L1==L2: #if first k-2 elements are equal,namely,besides the last item,all the items of the two sets are the same!
                retList.append(Lk[i] | Lk[j]) #set union
    return retList

def apriori(dataSet, minSupport = 0.1):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)#scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


def generateRules(L, supportData, minConf=0.1):  #supportData is a dict coming from scanD
    bigRuleList = []
    for i in range(1, len(L)):#only get the sets with two or more items
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

def calcConf(freqSet, H, supportData, brl, minConf=0.1):
    prunedH = [] #create new list to return
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq] #calc confidence
        if conf >= minConf:
            print freqSet-conseq,'-->',conseq,'conf:',conf
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.1):
    print "freqSet:",freqSet

    Hmp1=calcConf(freqSet, H, supportData, brl, minConf)

    m = len(Hmp1[0])
    print "m:",m,"Hmp1 now:",Hmp1
    if (len(freqSet) > (m + 1)): #try further merging
        Hmp1 = aprioriGen(Hmp1, m+1)#create Hm+1 new candidates
	print 'Hmp1:',Hmp1
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
	print 'Hmp1 after calculate:',Hmp1
        if (len(Hmp1) > 1):    #need at least two sets to merge
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)



#loop through the product ids
for row in rows:
	reviews = getReviews(row[0])
	dataset=[]
	#loop through the reviews of the current product
	for review in reviews:
		content = review[0]
		#convert to utf-8 encoding
		content = unicode(content, 'utf-8')
		#tokenize and POS tag
		tokens = nltk.word_tokenize(content)
		tagged = nltk.pos_tag(tokens)
		#print tagged
		nouns=[]
		#check  each word for qualification
		for item in tagged:
			#conditions - Noun, length > 3
			if (item[1] == 'NN' and item[0].lower() not in stopwords and len(item[0]) > 3):
				nouns.append(normalise(item[0]))
		#eliminate duplicates
		nouns = list(set(nouns))
		#add the possible features to the dataset
		dataset.append(nouns)
	#calculate strength dynamically based on dataset size - need to figure this out
	#as of now, setting strength as a constant
	if selected in "Mobile Phones":
		strength = 0.1
	if selected in "Pen Drives":
		strength=0.05
	#find frequent features
	armMine(dataset,strength)
