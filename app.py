import json
import re
from flask import *
from flask_mail import Mail, Message
import mysql.connector

app = Flask(__name__)
config = json.load(open("config.json"))
mail_settings = config["mail_settings"]
app.config.update(mail_settings)
mail = Mail(app)

email_template = """<html>

<head>
  <meta name="viewport" content="width=device-width">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Baloo+Da+2&amp;display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Meddon&amp;display=swap" rel="stylesheet">
  <title>Email Template</title>
  <style>
    /* -------------------------------------
          ALL CSS
      ------------------------------------- */
    body {
      background-color: hsl(0, 0%, 96%);
      font-family: 'Baloo Da 2', cursive;
      -webkit-font-smoothing: antialiased;
      font-size: 14px;
      line-height: 1.4;
      margin: 0;
      padding: 0;
      -ms-text-size-adjust: 100%;
      -webkit-text-size-adjust: 100%;
    }

    table {
      border-collapse: separate;
      mso-table-lspace: 0pt;
      mso-table-rspace: 0pt;
      width: 100%;
    }

    table td {
      font-family: 'Baloo Da 2', cursive;
      ;
      font-size: 14px;
      vertical-align: top;
    }

    /* -------------------------------------
          BODY & CONTAINER
      ------------------------------------- */

    .body {
      background-color: #f6f6f6;
      width: 100%;
    }

    /* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
    .container {
      display: block;
      margin: 0 auto !important;
      /* makes it centered */
      max-width: 580px;
      padding: 10px;
      width: 580px;
    }

    /* This should also be a block element, so that it will fill 100% of the .container */
    .content {
      box-sizing: border-box;
      display: block;
      margin: 0 auto;
      max-width: 580px;
      padding: 10px;
    }

    /* -------------------------------------
          HEADER, FOOTER, MAIN
      ------------------------------------- */
    .main {
      background: #ffffff;
      border-radius: 3px;
      width: 100%;
    }

    .wrapper {
      box-sizing: border-box;
      padding: 20px;
    }

    .content-block {
      padding-bottom: 10px;
      padding-top: 10px;
    }

    .footer {
      clear: both;
      margin-top: 10px;
      text-align: center;
      width: 100%;
    }

    .footer td,
    .footer p,
    .footer span,
    .footer a {
      color: #999999;
      font-size: 12px;
      text-align: center;
    }

    /* -------------------------------------
          TYPOGRAPHY
      ------------------------------------- */
    h1,
    h2,
    h3,
    h4 {
      color: #000000;
      font-family: 'Baloo Da 2', cursive;
      font-weight: 400;
      line-height: 1.4;
      margin: 0;
      margin-bottom: 30px;
    }

    p,
    ul,
    ol {
      font-family: 'Baloo Da 2', cursive;
      font-size: 15px;
      font-weight: normal;
      margin: 0;
      margin-bottom: 15px;
    }


    /* -------------------------------------
          SIGNATURE
      ------------------------------------- */
    .name {
      font-family: 'Meddon', cursive;
      font-size: 12px;
    }
  </style>
</head>

<body class="">
  <table role="presentation" class="body" cellspacing="0" cellpadding="0" border="0">
    <tbody>
      <tr>
        <td>&nbsp;</td>
        <td class="container">
          <div class="content">
            <!-- START CENTERED WHITE CONTAINER -->
            <table role="presentation" class="main">
              <!-- START MAIN CONTENT AREA -->
              <tbody>
                <tr>
                  <td class="wrapper">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                      <tbody>
                        <tr>
                          <td>
                            <img src="https://istylebeauty.com/static/media/logos/anime1.png" height="50px">
                            <h3 style="padding-top:20px">Hi {name} 👋,</h3>
                            <p>My name is Ayomipo and I am the CEO and Co-founder of iStyle 👨‍💼. Thank your for signing up to become our stylists. We are delighted to have you on board 🤗.</p>
                            <p>We created iStyle with the goal to help stylists around the country increase their reachability to clients and making it accessible for clients to get stylists with ease 😉.</p>
                            <p>We are thrilled to also help your business scale around the country both large and small by giving you loyal and reliable clients 🤩.</p>
                            <p><i><b>We are still in development and will let you know as soon as we launch, you also get frequent updates about our progress so keep an eye out for our email 👀.</b></i></p>
                            <p>Thank you, and welcome once again to iStyle!</p><br>
                            <p>Cheers,</p>
                            <br>
                            <p><b>Ayomide Olamipo</b></p>
                            <p class="name">Ayomide Olamipo</p>
                            <p><b>CEO and Co-Founder iStyle</b></p>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
                <!-- END MAIN CONTENT AREA -->
              </tbody>
            </table>
            <!-- END CENTERED WHITE CONTAINER -->

            <!-- START FOOTER -->
            <div class="footer">
              <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                  <tr>
                    <td class="content-block">
                      <span class="apple-link">Copyright (c) 2020 iStyle, All right reserved</span>
                      <br> Don't like these emails? <a href="#">Unsubscribe</a>.
                    </td>
                  </tr>
                  <tr>
                    <td class="content-block powered-by">
                      Powered by <a href="#">iStyle</a>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- END FOOTER -->
          </div>
        </td>
        <td>&nbsp;</td>
      </tr>
    </tbody>
  </table>


</body>

</html>"""


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
            if re.search("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email) == None:
                raise Exception()
            fname = fname.capitalize()
            lname = lname.capitalize()
            db = mysql.connector.connect(**config["db"])
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            if cursor.fetchone():
                return render_template("vendor-registration.html", error="The account you are trying to register already exists.")
            else:
                cursor.execute("INSERT into users (email, fname, lname, phone, company, address) VALUES (%s, %s, %s, %s, %s, %s)",
                               (email, fname, lname, phone, company, address))
                db.commit()
                send_welcome_mail(email, fname)
            return render_template("vendor-registration.html", successful=True)
        except:
            return render_template("vendor-registration.html", error="An error occured while trying to register, please retry.")
    return render_template("vendor-registration.html")


def send_welcome_mail(email, name):
    with app.app_context():
        try:
            html = email_template.format(name=name)
            msg = Message(subject=subject, sender=("iStyle Team", app.config.get(
                "MAIL_USERNAME")), recipients=[email], html=html)
            mail.send(msg)
        except:
            pass


if __name__ == "__main__":
    app.run(debug=True)
