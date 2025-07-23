from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# Use environment variables for security!
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")  # e.g., missiodei050@gmail.com
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")  # Your Gmail App Password

@app.route('/')
def index():
    return render_template('index.html')  # Your HTML page

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
    msg['From'] = EMAIL_ADDRESS  # This MUST match the logged in email!
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

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        return f"Error: {e}"

    return 'Registration submitted successfully!'

if __name__ == '__main__':
    app.run(debug=True)
