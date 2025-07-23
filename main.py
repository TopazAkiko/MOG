from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # your HTML file

@app.route('/register', methods=['POST'])
def register():
    fullName = request.form['fullName']
    email = request.form['email']
    phone = request.form['phone']
    dob = request.form['dob']
    gender = request.form['gender']
    address = request.form['address']
    declaration = request.form.get('declaration')

    msg = EmailMessage()
    msg['Subject'] = 'New Missio Dei Fellowship Registration'
    msg['From'] = 'YOUR_GMAIL@gmail.com'
    msg['To'] = 'missionofgod55@gmail.com'
    msg.set_content(f'''
    Full Name: {fullName}
    Email: {email}
    Phone: {phone}
    DOB: {dob}
    Gender: {gender}
    Address: {address}
    Declaration Agreed: {declaration}
    ''')

    # You must create a Gmail App Password, do NOT use your normal password
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('YOUR_GMAIL@gmail.com', 'YOUR_APP_PASSWORD')
        smtp.send_message(msg)

    return 'Registration submitted successfully!'

if __name__ == '__main__':
    app.run(debug=True)
