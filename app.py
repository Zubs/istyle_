import json
from flask import *
import mysql.connector

app = Flask(__name__)
config = json.load(open("config.json"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
    fname = request.form.get("fname")
    if fname:
        try:
            lname = request.form.get("lname")
            email = request.form.get("email")
            phone = request.form.get("phone")
            company = request.form.get("company")
            address = request.form.get("address")
            if None in [fname, lname, email, phone, company, address]:
                raise Exception()
            if (not phone.startswith("+234")) or len(phone) != 14:
                raise Exception()
            fname = fname.capitalize()
            lname = lname.capitalize()
            db = mysql.connector.connect(**config["db"])
            cursor = db.cursor()
            cursor.execute("INSERT into users (fname, lname, phone, company, address) VALUES (%s, %s, %s, %s, %s)",
                           (fname, lname, phone, company, address))
            db.commit()
            return render_template("vendor-registration.html", successful=True)
        except:
            return render_template("vendor-registration.html", failed=True)
    return render_template("vendor-registration.html")


if __name__ == "__main__":
    app.run(debug=True)
