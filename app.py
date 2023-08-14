from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq
import os

app = Flask(__name__)

#route to display home page
@app.route('/', methods=['GET'])
def home_page():
    return render_template()

# route to show the review comments in a web UI
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        try:
            search_string = request.form['content'].replace(" ", "")
            #go to the flipkart url
            flipkart_url = "https://www.flipkart.com/search?q=" + search_string
            #open the url using urlopen
            uClient = ureq(flipkart_url)
            #read the entire page of flipkart
            flipkartPage = uClient.read()
            #colse it
            uClient.close()
            #it just beautify the raw html code (little bit readable format)
            flipkart_html = bs(flipkartPage, "html.parser")
            #find the products available in the page
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            #only 24 products available in the page(index from 2 to 26)
            #so deleting first two indexes
            del bigboxes[0:2]
            #after deleting getting first index
            box = bigboxes[0]
            #href is for every products total 24href available
            #so append flipkart link with respective product
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            #getting product response form web using requests.get()
            prodRes = requests.get(productLink)
            #encoding process,it gives text in english if response is 200
            prodRes.encoding='utf-8'
            #again beautify it using beautiful soup
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html) #it gives the product html code, from here we extract reviews

            #getting entire comment boxes
            #inside this name,rating,review heading and review body everything available
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})

            # Create a directory to store the CSV files
            directory = "search_csv_files"
            if not os.path.exists(directory):
                os.makedirs(directory)

            #create file name and add it into directory
            filename = os.path.join(directory, search_string + ".csv")
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)

            reviews = []
            for commentbox in commentboxes:
                name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                rating = commentbox.div.div.div.div.text
                commentHead = commentbox.div.div.div.p.text
                comtag = commentbox.div.div.find_all('div', {'class': ''})
                customerComment = comtag[0].div.text

                mydict = {"Product": search_string, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": customerComment}
                
                reviews.append(mydict)
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])

        except Exception as e:
            print('The Exception message is: ',e)
    
    else:
        return render_template('index.html')
    
if __name__ == "__main__":
	app.run(debug=True)



