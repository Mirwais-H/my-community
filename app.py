from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

client = MongoClient('localhost', 27017)
db = client['Afghan-Community']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/membership')
def membership():
    return render_template('membership.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html')
    else:
        flash("Please log in to access your profile.")
        return redirect(url_for('login'))

@app.route('/change-username', methods=['POST'])
def change_username():
    # Implement the logic to change the username
    return redirect(url_for('profile'))

@app.route('/change-password', methods=['POST'])
def change_password():
    # Implement the logic to change the password
    return redirect(url_for('profile'))

@app.route('/delete-profile', methods=['POST'])
def delete_profile():
    # Implement the logic to delete the profile
    return redirect(url_for('profile'))

# Route to change username
@app.route('/change-username', methods=['GET', 'POST'])
def change_username():
    if request.method == 'POST':
        password = request.form['password']
        if password == dummy_user['password']:
            # Logic to change username
            new_username = 'NewUsername'  # Replace with actual logic to change username
            flash(f'Username changed to {new_username}', 'success')
            return redirect(url_for('home'))  # Redirect to home or profile page
        else:
            flash('Incorrect password. Please try again.', 'error')
    return render_template('profile.html')  # Render profile page or redirect as needed

# Route to change password
@app.route('/change-password', methods=['POST'])
def change_password():
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    if current_password == dummy_user['password']:
        # Logic to change password
        dummy_user['password'] = new_password  # Update password (should be hashed in real scenario)
        flash('Password changed successfully', 'success')
    else:
        flash('Incorrect current password. Please try again.', 'error')
    return redirect(url_for('home'))  # Redirect to home or profile page

# Route to delete profile
@app.route('/delete-profile', methods=['POST'])
def delete_profile():
    password = request.form['password']
    if password == dummy_user['password']:
        # Logic to delete profile
        flash('Profile deleted successfully', 'success')
        return redirect(url_for('home'))  # Redirect to home page after deletion
    else:
        flash('Incorrect password. Profile deletion failed.', 'error')
        return redirect(url_for('home'))  # Redirect to home or profile page


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        existing_user = users.find_one({'username': username})

        if existing_user:
            error = 'Username already exists. Please choose a different username.'
            return render_template('signup.html', error=error)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user_data = {
            'username': username,
            'password': hashed_password,
            'first_name': first_name,
            'last_name': last_name
        }

        users.insert_one(user_data)
        session['username'] = username  # Log the user in after signup
        return redirect(url_for('index'))

    return render_template('signup.html')



# Profile route
@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        user = users.find_one({'username': username})
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
