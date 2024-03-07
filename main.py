from flask import Flask, render_template, url_for, request, redirect
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5
# from flask_ckeditor import CKEditor
from smtplib import SMTP
from twilio.rest import Client
import os
# from dotenv import load_dotenv
from forms import ContactForm


# dotenv_path = os.path.join("C://Users//Damian//PycharmProjects//.env.txt")
# load_dotenv(dotenv_path)
EMAIL = os.getenv('EMAIL')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
VERIFIED_NUMBER = os.getenv('VERIFIED_NUMBER')
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.getenv('WTFORMS_SECRET_KEY')
csrf = CSRFProtect(app)
smtp = SMTP()
# ckeditor = CKEditor(app)


def send_email(message):
    connection = SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(EMAIL, EMAIL_PASSWORD)
    connection.sendmail(from_addr=EMAIL, to_addrs="damian.nikodym@gmail.com",
                        msg=f"Subject:New message from my website\n\nAuthor: {message['name']} ({message['email']})\n\n"
                            f"Subject: {message['subject']}\n\nMessage: {message['text']}")


def send_SMS(message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"New message from my website from {message['name']}, subject: {message['subject']}",
        from_=TWILIO_NUMBER,
        to=VERIFIED_NUMBER
    )


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        message = {
            'name': form.name.data,
            'email': form.email.data,
            'subject': form.subject.data,
            'text': form.message.data,
        }

        send_email(message)
        # send_SMS(message)
        return redirect(url_for('home'))

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
