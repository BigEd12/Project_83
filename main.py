from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import datetime

##---------------------- YEAR FOR COPYRIGHT ---------------------- ##
year = datetime.datetime.now().strftime('%Y')

#---------- FLASK ----------#
app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap(app)

@app.route("/")
def index():
    return render_template("index.html", year=year)


if __name__ == "__main__":
    app.run(debug=True)
