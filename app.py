from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    #return '<h1>O</h1>'
    return render_template("main.html")
