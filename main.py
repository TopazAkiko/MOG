from flask import Flask, render_template_string, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

# Folder for uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions for uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'mp4', 'avi', 'mov'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Serve the HTML as a template string (or you can put it in templates/index.html)
HTML_PAGE = """
<!-- Paste your entire HTML code here between triple quotes -->
<!-- For brevity, I will just redirect to static index.html in this example -->
"""


@app.route('/')
def index():
    # If you want to serve HTML from a file, replace this with:
    # return render_template('index.html')
    # For now, let's just serve the static file directly
    return app.send_static_file('index.html')


@app.route('/register', methods=['POST'])
def register():
    # Process membership registration form data
    full_name = request.form.get('fullName')
    email = request.form.get('email')
    phone = request.form.get('phone')
    dob = request.form.get('dob')
    gender = request.form.get('gender')
    address = request.form.get('address')

    passport_photo = request.files.get('passportPhoto')
    signature1 = request.files.get('signature1')
    signature2 = request.files.get('signature2')

    # Basic validation
    if not all([full_name, email, phone, dob, gender, address, passport_photo, signature1, signature2]):
        flash('Please fill all required fields and upload all files.')
        return redirect(url_for('index'))

    # Save uploaded files
    for file in [passport_photo, signature1, signature2]:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('Invalid file type.')
            return redirect(url_for('index'))

    # Here, you would save the form data to a database or email it

    flash('Registration successful! Thank you.')
    return redirect(url_for('index'))


@app.route('/payment', methods=['POST'])
def payment():
    orange_money = request.form.get('orangeMoneyNumber')
    amount = request.form.get('amount')

    if not orange_money or not amount:
        flash('Please enter all payment details.')
        return redirect(url_for('index'))

    # Save or process payment details here

    flash('Payment received, thank you!')
    return redirect(url_for('index'))


@app.route('/upload_activities', methods=['POST'])
def upload_activities():
    audio_files = request.files.getlist('audioFiles')
    video_files = request.files.getlist('videoFiles')
    picture_files = request.files.getlist('pictureFiles')

    all_files = audio_files + video_files + picture_files

    for file in all_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash('One or more files have invalid type.')
            return redirect(url_for('index'))

    flash('Activities uploaded successfully.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
