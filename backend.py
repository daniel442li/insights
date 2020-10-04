from flask import Flask, render_template, request, redirect, url_for
import os
import pytesseract
from PIL import Image
import json
import datetime
import numpy as np
import pymongo

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('template.html')

@app.route('/clear', methods=['POST'])
def clear ():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static", "receipts.json")
    data = {"data": [
        {
            "date": "Total",
            "category": "",
            "total": 0
        }
        ]}
    with open(json_url,'w') as f: 
        json.dump(data, f, indent=4) 
    
    return redirect(url_for('main_page'))

@app.route('/signedIn')
def main_page():
    return render_template('mainpage.html')

@app.route('/signedIn', methods=['POST'])
def process():
    uploaded_file = request.files['file']
    try:
        text = pytesseract.image_to_string(Image.open(uploaded_file))
    except:
        return redirect(url_for('main_page'))
    pre_sorted_text = text.lower().split()
    sorted_text = []

    total = 0

    total_total = 0
    charge_total = 0
    subtotal_total = 0

    cat_totals = [0, 0, 0, 0, 0, 0]

    category = ""

    date = datetime.datetime.now()
    date_formated = date.strftime("%B %d, %Y, %H:%M")

    titles = ['groceries', 'dining', 'entertainment', 'clothing', 'transportation', 'miscellaneous']

    categories = {"costco": 0, "cvs": 0, "kroger": 0, "piggly wiggly":0, "mcdonald":1, "chick-fil-a":1, "chick fil a":1, "mcdougals":1, "hattie b":1,"amc": 2, "topgolf": 2, "gap":3, "nordstrom":3,"lululemon":3, "macy's":3, "macys": 3, "uber": 4, "lyft":4, "bp":4, "shell":4, "marathon": 4, "exxon": 4}

    for w in pre_sorted_text:
        sorted_text.append(w.replace('$', ''))

    for x in sorted_text:
        if x == 'total' or x == 'total:':
            try:
                total_total = float(sorted_text[sorted_text.index(x) + 1])
                break
            except ValueError:
                total_total = float(sorted_text[sorted_text.index(x) + 2])
        elif x == 'charge' or x == 'charge:' and check == False:
            charge_total = float(sorted_text[sorted_text.index(x) + 1])
        elif x == 'subtotal' or x == 'subtotal:' or x == 'sub':
            for y in sorted_text:
                if y == 'tax' or y == 'tax':
                    try:
                        subtotal_total = float(sorted_text[sorted_text.index(x) + 1]) + float(sorted_text[sorted_text.index(y) + 1])
                    except ValueError:
                        subtotal_total = float(sorted_text[sorted_text.index(x) + 1]) + float(sorted_text[sorted_text.index(y) + 2])
        else:
            total = 0

    if total_total != 0:
        total = total_total
    elif charge_total != 0:
        total = charge_total
    elif subtotal_total != 0:
        total = subtotal_total

    for x in sorted_text:
        for key in categories:
            if x == key:
                cat_totals[categories[key]] += total
                category = titles[categories[key]]
                break
        if np.count_nonzero(cat_totals) != 0:
            break

    if np.count_nonzero(cat_totals) == 0:
        cat_totals[len(titles) - 1] += total
        category = titles[len(titles) - 1]
    
    category = category.capitalize()

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static", "receipts.json")

    def write_json(data, filename=json_url): 
        with open(filename,'w') as f: 
            json.dump(data, f, indent=4) 
      
      
    with open(json_url) as json_file: 
        data = json.load(json_file) 
        
        temp = data['data'] 
        temp.pop()
    
        # python object to be appended 
        y = {
            "date": date_formated,
            "category": category,
            "total" : total
            } 
    
        # appending data to emp_details  
        temp.append(y) 

        total = 0
        for obj in temp:
            total = total + (obj['total'])
        
        z = {
            "date": "Total",
            "category": "",
            "total" : total
        }

        temp.append(z)

      
    write_json(data)  

    return redirect(url_for('main_page'))

@app.after_request
def adding_header_content(head):
    head.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    head.headers["Pragma"] = "no-cache"
    head.headers["Expires"] = "0"
    head.headers['Cache-Control'] = 'public, max-age=0'
    return head

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/retrieve', methods = ['POST'])
def retrieve():
    data = request.data
    my_json = data.decode('utf8')
    user_data = json.loads(my_json) 
    myclient = pymongo.MongoClient("mongodb://daniel442li:KANQzahn5dF3VzZ@cluster0-shard-00-00-jq2na.mongodb.net:27017,cluster0-shard-00-01-jq2na.mongodb.net:27017,cluster0-shard-00-02-jq2na.mongodb.net:27017/<dbname>?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    database = myclient["vandyhacks"]
    collection = database["users"]   
    return 'Done'

@app.route('/push', methods = ['POST'])
def push():
    data = request.data
    myclient = pymongo.MongoClient("mongodb://daniel442li:KANQzahn5dF3VzZ@cluster0-shard-00-00-jq2na.mongodb.net:27017,cluster0-shard-00-01-jq2na.mongodb.net:27017,cluster0-shard-00-02-jq2na.mongodb.net:27017/<dbname>?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    database = myclient["vandyhacks"]
    collection = database["users"]
    return 'Done'

if __name__ == "__main__":
    app.run(debug=True,port=5000)