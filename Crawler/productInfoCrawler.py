from bs4 import BeautifulSoup
import urllib2,math
import MySQLdb
import re
import sys
import os

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


#init db
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="root", # your password
                      db="product_"+selected) # name of the data base

cursor = db.cursor()

start = input()
end = input()

#select all the data from the db
sql = "SELECT * FROM `productlink` LIMIT "+`start`+","+`end`+";"

cursor.execute(sql)
#rows will contain the pid and link
rows = cursor.fetchall()


def crawlReview(pid,url):
	page= urllib2.urlopen(url)
	html = page.read()
	#print html
	soup = BeautifulSoup(html)
	#productID
	pid = pid
	reviews = []
	uids = []
	try:
	reviewList = soup.find_all("div",{"class":"review-list"})
	reviewArray = reviewList[0].find_all("div",{"class":"fclear fk-review fk-position-relative line "})
	except:
		return
	for i in reviewArray:
		#review ID
		reviewId =  i["review-id"]
		print "Review ID : "+reviewId
		
		reviewerId = i.find_all("a",{"class":"load-user-widget fk-underline"})
		uid = ""
		for j in reviewerId:
			uid = j["profile_name"]
			print "UserID"+uid
		reviewText = i.find_all("span",{"class":"review-text"})
		review = ""
		for j in reviewText:
			review = str(j)
			review = review.replace("<br/>","")
			review = review.replace("\n","")
			review = review.replace('''<span class="review-text">''',"")
			review = review.replace("</span>","")
			review = re.search("([\s]+)(.+)",review).group(2)
			review = review.replace("\xe2\x80\x99","")
			review = review.replace("'","")
			review = review.replace("\"","")
			print review
		feedback = i.find_all("strong")
		posFeedback = str(feedback[1].string)
		if("%" in posFeedback):
			posFeedback=posFeedback.replace("%","")
			posFeedback=int(posFeedback)
			totFeedback = int(str(feedback[2].string))
			posFeedback=(posFeedback/100.0)*totFeedback
			negFeedback= totFeedback - posFeedback
			posFeedback=int(math.floor(posFeedback))
			negFeedback=int(math.ceil(negFeedback))
		else:
			posFeedback=int(posFeedback)
			totFeedback = int(str(feedback[2].string))
			negFeedback= totFeedback - posFeedback
			
			
		print "Positive FeedBack : "+ `posFeedback`
		print "Negative FeedBack : "+ `negFeedback`
		
		#find the review rating
		rating = 0
		StarRating = i.find_all("div",{"class":"fk-stars"})
		for j in StarRating:
			StarRating = j["title"]
			rating = int(str(StarRating).split(' ')[0])
		print "Rating : "+ `rating`
		
		#find date
		dateTag = i.find_all("div",{"class":"date line fk-font-small"})
		date = ""
		for i in dateTag:
			date = i.string
			date = re.search("([\s]+)([0-9]{2} [\w]{3} [0-9]{4})",date).group(2)
			print "Date : "+date		
		try:
			#execute and then commit
			sql = "INSERT INTO `product_review` VALUES (%s,%s,%s,%s,%s,%s,%s,%s,0)"
			cursor.execute(sql,(pid,uid,reviewId,review,posFeedback,negFeedback,rating,date))
			db.commit()
		except:
			#if insert fails rollback
			print sql
			print "INSERT FAILED.... "
			db.rollback()
		


def parseHTML(link,pid):
	page= urllib2.urlopen(link)
	html = page.read()
	#print html
	soup = BeautifulSoup(html)
	img=soup.find_all("img",{"class":"productImage  current"})
	imgUrl=img[0]['data-src']
	response=urllib2.urlopen(imgUrl)
	content=response.read()
	f = open(os.path.join("../Images",pid+".jpeg"), "w")
	f.write( content )
	#getting pname
	pname = ""
	for i in soup.find_all("h1",{"class" : "title","itemprop" : "name"}):
		pname = i.string
	print "Product Name : "+pname
	
	#getting Selling price
	price = ""
	for i in soup.find_all("span",{"class":"selling-price"}):
		price = i.string
		break
	#format the price info
	#price = re.search("([\n ]*Rs. )([0-9,]*)([ \n]*)",price).group(2)
	price=price.replace("Rs. ","")
	price = price.replace(",","")
	print "Product Price : "+price
	
	avgRating = ""
	#avg rating
	for i in soup.find_all("div",{"class":"bigStar"}):
		avgRating = i.string
	print "Average Rating : "+avgRating
	#5Star
	for i in soup.find_all("a",{"title":"Read 5 star reviews"}):
		star5=re.search('''<div class="progress".+">(.+)</div>''',str(i)).group(1)
	print "5 Star:"+star5
	for i in soup.find_all("a",{"title":"Read 4 star reviews"}):
		star4=re.search('''<div class="progress".+">(.+)</div>''',str(i)).group(1)
	print "4 Star:"+star4
	for i in soup.find_all("a",{"title":"Read 3 star reviews"}):
		star3=re.search('''<div class="progress".+">(.+)</div>''',str(i)).group(1)
	print "3 Star:"+star3
	for i in soup.find_all("a",{"title":"Read 2 star reviews"}):
		star2=re.search('''<div class="progress".+">(.+)</div>''',str(i)).group(1)
	print "2 Star:"+star2
	for i in soup.find_all("a",{"title":"Read 1 star reviews"}):
		star1=re.search('''<div class="progress".+">(.+)</div>''',str(i)).group(1)
	print "1 Star:"+star1
	star1 = star1.replace(",","")
	star2 = star2.replace(",","")
	star3 = star3.replace(",","")
	star4 = star4.replace(",","")
	star5 = star5.replace(",","")
	sql ="INSERT INTO product_details VALUES "
	insert_str= "('"+pid+"','"+pname+"','"+price+"','"+avgRating+"','"+star5+"','"+star4+"','"+star3+"','"+star2+"','"+star1+"')"
	sql+=insert_str
	try:
		#execute and then commit
		cursor.execute(sql)
		db.commit()
	except:
		#if insert fails rollback
		#print sql
		#print "Error"
		db.rollback()
	url = ""
	for i in soup.find_all("p",{"class":"subText"}):
		try:
			url=re.search('''<a href="(.+)".+</a>''',str(i)).group(1)
		except AttributeError:
			continue
	test=soup.find_all("a",{"class":"lnkViewAll"})
	rCount=test[1].text
	reCount=re.search('''[0-9]+,[0-9]+|[0-9]+''',rCount).group(0);
	reviewCount=int(reCount.replace(",",""));
	#reviewCount = int(soup.find_all("span",{"itemprop":"reviewCount"})[0].string)
	#reviewCount=0
	print "Review Count : "+`reviewCount`
	for i in range(0,reviewCount,10):
		crawlReview(pid,"http://www.flipkart.com"+url+"&start="+`i`)
	
	

for row in rows:
	pid = row[0]
	link = row[1]
	print "pid : "+pid+"\n"
	print "link : "+link+"\n"
	parseHTML(link,pid)
	




