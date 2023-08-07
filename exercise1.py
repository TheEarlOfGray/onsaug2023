from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Homepage"

@app.route('/square/<int:num>')
def square(num):
    return str(num ** 2)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)