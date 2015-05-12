Welcome to our Final Year Project. This tool allows you to view the most frequently talked about features in user reviews and the reviews sentences which contains these features for a selected product. 

To get started, you will have to crawl an E-commerce website for user reviews. In our tool we have crawled flipkart. 

To do this the database has to be setup with the DB dump included(productdb.sql present in root) with the DB name as product_productname eg. : product_mobilephone

crawler.py in the folder Crawler crawls the Product Selection page for product links.

To add new products first add the name of the product and then the link of the product at the end of the file Product Links which is present in the folder Crawler in the format shown below:

After doing so add the product name at the end of products.txt present in the folder Files. 

Product Name <new line>
(If product name is more than one word, leave a space in between; This name should match the db name) eg: Mobile Phone
Product Link

Running crawler.py would prompt you to enter 2 numbers the 1st number the the start no and the 2nd number is the end number of the product page. Entering 1 and 10 would result in crawling 10 product links.

In productInfocrawler.py similarly you would be prompted to enter two numbers there the two numbers are the start and end limit of the no of products details to be crawled. 

Once the product details have been crawled, run extractor.py providing the start and end limits. 
extractor.py extracts the most frequent features from the user reviews. 

Now run main.py which contains GUI which would help in selecting a Product Category such as Mobile Phone or Pen Drive.

main.py invokes product.py which shows all the products in the selected category. 

once a product is selected feat_select.py in invoked which display all the frequent features. Selecting a freqent feature allows the user to see all the positive and negative reviews sentences containing the features. 
