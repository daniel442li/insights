from flask import Flask, render_template, request, redirect, url_for
import os
import pytesseract
from PIL import Image

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('template.html')

@app.route('/signedIn')
def main_page():
    return render_template('mainpage.html')

@app.route('/signedIn', methods=['POST'])
def process():
    uploaded_file = request.files['file']
    text = pytesseract.image_to_string(Image.open(uploaded_file))
    sorted_text = text.lower().split()

    total = 0

    cat_totals = [0, 0, 0, 0, 0, 0, 0]

    again = 1

    titles = ['groceries/necessities', 'dining', 'entertainment', 'clothing', 'transportation', 'utilities', 'miscellaneous']

    categories = {"costco": 0, "cvs": 0, "kroger": 0, "piggly wiggly":0, "mcdonald":1, "chick-fil-a":1, "chick fil a":1,"hattie b":1, "amc": 2, "topgolf": 2, "gap":3, "nordstrom":3,"lululemon":3, "macy":3, "macys": 3, "uber": 4, "lyft":4, "bp":4, "shell":4, "marathon": 4, "exxon": 4}

    for x in sorted_text:
        if x == 'total' or x == 'total:':
            total = float(sorted_text[sorted_text.index(x) + 1])
            break
        elif x == 'charge' or x == 'charge:':
            total = float(sorted_text[sorted_text.index(x) + 1])
            break
        elif x == 'subtotal' or x == 'subtotal:':
            for y in sorted_text:
                if y == 'tax' or y == 'tax':
                    total = float(sorted_text[sorted_text.index(x) + 1]) + float(sorted_text[sorted_text.index(y) + 1])
                    break
        else:
            total = 0
    for x in sorted_text:
        for key in categories:
            if x == key:
                cat_totals[categories[key]] += total
                break
            else:
                cat_totals[len(cat_totals) - 1] += total
                break
        break

    print(total)

    print(cat_totals)
    return redirect(url_for('main_page'))

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == "__main__":
    app.run(debug=True,port=5000)