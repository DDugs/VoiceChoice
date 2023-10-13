from flask import Flask, flash, render_template, request, redirect, url_for
import smtplib
import json
import os
import re
from datetime import datetime, timedelta

app = Flask(__name__)

# Define a route for the index.html page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/elections')
def elections():
    # Sample data for elections, you can load this from your database
    elections_data = [
        {"id": 2000, "title": "Student Election", "start_date": "01-10-2024", "end_date": "10-10-2023", "description": "Where you become the mentor for other students", "state": "Uttar Pradesh"},
        {"id": 2001, "title": "MUN Election", "start_date": "01-11-2023", "end_date": "10-11-2023", "description": "Where you debate", "state": "Uttar Pradesh"},
        {"id": 2002, "title": "Food Election", "start_date": "01-12-2023", "end_date": "10-12-2023", "description": "Where you eat", "state": "Uttar Pradesh"},
    ]

    upcoming_elections, ongoing_elections = check_and_move_elections(elections_data)

    return render_template('data/elections.html', upcoming_elections=upcoming_elections, ongoing_elections=ongoing_elections)

def check_and_move_elections(elections):
    today = datetime.now()
    one_week = timedelta(weeks=1)
    upcoming_elections = []
    ongoing_elections = []

    for election in elections:
        start_date = datetime.strptime(election['start_date'], '%d-%m-%Y')
        if start_date - today <= one_week:
            ongoing_elections.append(election)
        else:
            upcoming_elections.append(election)

    return upcoming_elections, ongoing_elections

@app.route('/admin')
def admin():
    return render_template('data/admin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the form data
        fullname = request.form['fullname']
        gender = request.form['gender']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        dob = request.form['dob']
        address = request.form['address']
        phone = request.form['phone']
        state = request.form['state']
        voter = request.form['voter']

        # Check if any field is empty
        if not (fullname and gender and email and username and password and dob and address and phone and state and voter):
            # Handle this case with JavaScript on the client-side
            pass

        # Add image upload validation
        if 'profile-photo' not in request.files:
            # Handle this case with JavaScript on the client-side
            pass

        photo = request.files['profile-photo']

        # Add email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            # Handle this case with JavaScript on the client-side
            pass

        # Add phone number validation (exactly 10 digits)
        if not re.match(r"^\d{10}$", phone):
            # Handle this case with JavaScript on the client-side
            pass

        # Parse and validate the date (dd-mm-yyyy)
        try:
            dob_date = datetime.datetime.strptime(dob, '%d-%m-%Y')
        except ValueError:
            # Handle this case with JavaScript on the client-side
            pass

        # Create a dictionary with user data
        user_data = {
            'fullname': fullname,
            'gender': gender,
            'email': email,
            'username': username,
            'password': password,
            'dob': dob_date.strftime('%d-%m-%Y'),
            'address': address,
            'phone': phone,
            'state': state,
            'voter': voter,
            'profile-photo': photo.filename
        }

        # Save the uploaded image
        photo.save(os.path.join('uploads', photo.filename))

        # Save user data to a JSON file
        with open('users.json', 'a') as file:
            json.dump(user_data, file)
            file.write('\n')

    # Render the registration form for GET requests
    return render_template('data/register.html')

@app.route('/login-admin')
def loginadmin():
    return render_template('data/login-admin.html')

@app.route('/login-user')
def loginuser():
    return render_template('data/login-user.html')

@app.route('/user')
def user():
    return render_template('data/user.html')

@app.route('/add-elections')
def addelec():
    return render_template('data/add-elec.html')

@app.route('/edit-elections')
def editelec():
    return render_template('data/edit-elec.html')

@app.route('/add-candidates')
def addcandidate():
    return render_template('data/add-candidate.html')

@app.route('/vote-1000')
def vote1000():
    return render_template('data/vote/1000-vote.html')

@app.route('/vote-1001')
def vote1001():
    return render_template('data/vote/1001-vote.html')

@app.route('/vote-1002')
def vote1002():
    return render_template('data/vote/1002-vote.html')

@app.route('/vote-1003')
def vote1003():
    return render_template('data/vote/1003-vote.html')

@app.route('/vote-1004')
def vote1004():
    return render_template('data/vote/1004-vote.html')

@app.route('/results-1000')
def stats1000():
    return render_template('data/stats/1000-stats.html')

@app.route('/results-1001')
def stats1001():
    return render_template('data/stats/1001-stats.html')

@app.route('/results-1002')
def stats1002():
    return render_template('data/stats/1002-stats.html')

@app.route('/results-1003')
def stats1003():
    return render_template('data/stats/1003-stats.html')

@app.route('/results-1004')
def stats1004():
    return render_template('data/stats/1004-stats.html')

@app.route('/profile-1000')
def profile1000():
    return render_template('data/elec-profile-ongo/1000.html')

@app.route('/profile-1001')
def profile1001():
    return render_template('data/elec-profile-ongo/1001.html')

@app.route('/profile-1002')
def profile1002():
    return render_template('data/elec-profile-ongo/1002.html')

@app.route('/profile-1003')
def profile1003():
    return render_template('data/elec-profile-ongo/1003.html')

@app.route('/profile-1004')
def profile1004():
    return render_template('data/elec-profile-ongo/1004.html')

@app.route('/profile-2000')
def profile2000():
    return render_template('data/elec-profile-upco/2000.html')

@app.route('/profile-2001')
def profile2001():
    return render_template('data/elec-profile-upco/2001.html')

@app.route('/profile-2002')
def profile2002():
    return render_template('data/elec-profile-upco/2002.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        from_email = request.form['from_email']
        from_name = request.form['from_name']
        subject = request.form['subject']
        message = request.form['message']

        # Send the email using smtplib or your preferred email library
        # Replace the placeholders with your email configuration
        smtp_server = 'smtp@gmail.com'
        smtp_port = 587
        smtp_username = 'guptadhruv2105@gmail.com'
        smtp_password = 'divyanshi2811'
        to_email = 'guptadhruv2105@gmail.com'

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)

            email_body = f'From: {from_name} <{from_email}>\nSubject: {subject}\n\n{message}'
            server.sendmail(from_email, to_email, email_body)
            server.quit()

        except Exception as e:
            flash(f'Error sending email: {str(e)}', 'error')
            return redirect(url_for('index'))
        
if __name__ == '__main__':
    app.run(debug=True)