# http://www.wechall.net/challenge/training/www/basic/index.php

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("/index.html")

@app.route("/bogus/bogus.html")
def bogus():
    return render_template("/bogus/bogus.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
