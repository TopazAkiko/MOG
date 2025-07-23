from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Make sure this folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Replace with your Gmail credentials
EMAIL_ADDRESS = "mission@example.com"   # your email
EMAIL_PASSWORD = "YOUR_APP_PASSWORD"    # use Gmail App Password

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['fullName']
    email = request.form['email']
    phone = request.form['phone']
    dob = request.form['dob']
    gender = request.form['gender']
    address = request.form['address']

    # Handle file uploads
    passport_photo = request.files['passportPhoto']
    sig1 = request.files['signature1']
    sig2 = request.files['signature2']

    passport_filename = secure_filename(passport_photo.filename)
    sig1_filename = secure_filename(sig1.filename)
    sig2_filename = secure_filename(sig2.filename)

    passport_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], passport_filename))
    sig1.save(os.path.join(app.config['UPLOAD_FOLDER'], sig1_filename))
    sig2.save(os.path.join(app.config['UPLOAD_FOLDER'], sig2_filename))

    # Compose email
    msg = EmailMessage()
    msg['Subject'] = f'New Membership Registration - {name}'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS  # send to yourself

    body = f'''
    New Registration:

    Name: {name}
    Email: {email}
    Phone: {phone}
    Date of Birth: {dob}
    Gender: {gender}
    Address: {address}
    '''

    msg.set_content(body)

    # Attach files
    for file_path in [passport_filename, sig1_filename, sig2_filename]:
        with open(os.path.join(app.config['UPLOAD_FOLDER'], file_path), 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(file_path)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # Send email using Gmail SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    return 'Registration submitted! ✅'

if __name__ == '__main__':
    app.run(debug=True)
