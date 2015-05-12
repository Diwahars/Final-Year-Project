from bs4 import BeautifulSoup
import urllib2
import MySQLdb
import re
import sys
import os

productLinks = []

class ProductLink:
	def __init__(self,pid,link):
		self.pid = pid
		self.link = link
		
	def __hash__(self):
		return hash(('pid',self.pid))

selproduct = [line.strip() for line in open(os.path.join("../Files",'products.txt'))]
print "Select a product:"
for i in range(0,len(selproduct)):
	print str(i+1)+". "+selproduct[i]
selected=int(input("Enter the product number:"))
selected=selproduct[selected-1]

links= [line.strip() for line in open('Product Links')]
for i in range(0,len(links),2):
	if selected in links[i]:
		break

selected=selected.replace(" ","").lower()

global_url=links[i+1]
#get start and stop numbers
start=input()
end=input()
soup = ""

#init db
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="root", # your password
                      db="product_"+selected) # name of the data base

cursor = db.cursor()


#parse the html page that was obtained
def parseHTML(html):
	soup = BeautifulSoup(html)
	#find all the a tags with class and get the href of those tags
	for a in soup.find_all("a",{"class" : "fk-display-block"},href=True):
		link = a['href']
		print link
		try:
			#split the text using regex
			pid = re.search("pid=(.+)&srno",link).group(1)
			#print pid
		except AttributeError:
			pid=""
			continue
			#sys.exit("pid Not found error")
		#add the base URL
		link = "http://www.flipkart.com"+link
		#append the data
		productLinks.append(ProductLink(pid,link))

#get all the reviews from start to end
for i in range(start,end,20):
	url=global_url+`i`
	print url
	page= urllib2.urlopen(url)
	html = page.read()
	parseHTML(html)

productLinks = list(set(productLinks))

#insert pid into table
insert_str = ""
for i in range(len(productLinks)):
	insert_str= "('"+productLinks[i].pid+"','"+productLinks[i].link+"')"
	sql ="INSERT INTO productlink VALUES "+insert_str
	#print sql
	try:
		#execute and then commit
		cursor.execute(sql)
		db.commit()
	except:
		#if insert fails rollback
		db.rollback()
		continue	
