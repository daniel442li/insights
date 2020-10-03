from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('template.html')

@app.route('/signedIn')
def main_page():
    return render_template('mainpage.html')

if __name__ == "__main__":
    app.run(debug=True,port=5000)