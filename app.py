from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>This is a title</h1>"

@app.route('/postoption', methods=["GET", "POST"])
def posto():
    response = request.method
    return f"Method is {response}"#

@app.route('/name/<name>/<int:num>')
def name(name, num):
    var1 = f"{name}<br>" * num
    return var1

@app.route('/gotogoogle')
def gotogoogle():
    return redirect("http://www.google.com")

@app.route('/gotohome')
def gotohome():
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)