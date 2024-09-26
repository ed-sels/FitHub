from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash 
import os

app = Flask(__name__)
mysql = MySQL(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')

# MySQL configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Wsanchez00$'
app.config['MYSQL_DB'] = 'fitness'

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Get user details from form
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Insert user details into the database
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user(name, email, password, dob) VALUES(%s, %s, %s, %s)", (name, email, hashed_password, dob))
            mysql.connection.commit()
            cur.close()
            flash('You have successfully signed up!', 'success')
            return redirect('/sign_in')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect('/sign_up')

    return render_template('sign_up.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        if not name or not password:
            flash('Please enter both name and password.', 'danger')
            return redirect('/sign_in')

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM user WHERE name = %s", (name,))
            user = cur.fetchone()  # Assuming the user has columns: id, name, email, password, dob
            cur.close()

            if user:
                stored_password_hash = user[3]  # Assuming password is the 4th column in the table
                if check_password_hash(stored_password_hash, password):
                    # Store relevant user data in the session
                    session['user_id'] = user[0]    # Store user ID
                    session['name'] = user[1]       # Store user name
                    session['email'] = user[2]      # Store user email
                    session['dob'] = user[4]        # Store user date of birth

                    flash('Login successful!', 'success')
                    return redirect('/dashboard')
                else:
                    flash('Incorrect password.', 'danger')
            else:
                flash('No account found with that name.', 'danger')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('sign_in.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    if 'user_id' not in session:
        flash('Please log in to view the blog page.', 'danger')
        return redirect('/sign_in')
    
    return render_template('blog.html')


@app.route('/logout')
def logout():
    session.pop('name', None)
    flash('You have been logged out!', 'success')
    return redirect('/sign_in')

@app.route('/dashboard')
def dashboard():
    if 'name' not in session or 'email' not in session:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect('/sign_in')

    # Fetch user data from the session
    user_data = {
        'name': session['name'],
        'email': session['email'],
        'dob': session['dob']
    }

    # Pass user data to the template
    return render_template('dashboard.html', user=user_data)


@app.route('/schedule')
def schedule():
    if 'name' not in session or 'email' not in session:
        flash('Please log in to access your schedule.', 'danger')
        return redirect('/sign_in')

    # Make sure user_data is always set if the session contains the required fields
    user_data = {
        'name': session.get('name'),
        'email': session.get('email'),
        'dob': session.get('dob')
    }

    # In case any of the required fields are missing from the session, handle it gracefully
    if not user_data['name'] or not user_data['email'] or not user_data['dob']:
        flash('Incomplete user data. Please log in again.', 'danger')
        return redirect('/sign_in')

    # Pass the user data to the schedule template
    return render_template('schedule.html', user=user_data)



@app.route('/profile')
def profile():
    # Ensure the user is logged in
    if 'name' not in session:
        flash('Please log in to access your profile.', 'danger')
        return redirect('/sign_in')

    # Fetch user data from the session
    user_data = {
        'name': session['name'],
        'email': session['email'],
        'dob': session['dob']
    }

    # Pass user data to the template
    return render_template('profile.html', user=user_data)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Please log in to access the profile edit page.', 'danger')
        return redirect('/sign_in')

    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        dobb = request.form.get('dobb')
        bio = request.form.get('bio')

        if not name or not email or not dobb:
            flash('All fields are required!', 'danger')
            return redirect('/edit_profile')

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE user 
                SET name = %s, email = %s, dobb = %s, bio = %s 
                WHERE id = %s
                """, (name, email, dobb, bio, session['user_id']))
            mysql.connection.commit()
            cur.close()
            
            # Update session data
            session['name'] = name
            session['email'] = email
            session['dobb'] = dobb
            session['bio'] = bio
# MOTTEY EDWIN SELORM	UEB3504222
# TUTU LOUISA OFOSUHEMAA	UEB3507922
# BAIDOO ANIMAH	UEB3513622
# APPIAGYEI YAA KONADU	UEB3508822
# AMOAH ENOCH EDUMADZE	UEB3509222
# AMEYAW SIAW JEFF CHRIS	UEB3511422
            flash('Profile updated successfully!', 'success')
            return redirect('/profile')

        except Exception as e:
            flash('Error updating profile: ' + str(e), 'danger')
            return redirect('/edit_profile')

    else:  # GET request
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT name, email, dobb, bio FROM user WHERE id = %s", (session['user_id'],))
            user = cur.fetchone()
            cur.close()

            if user:
                user_data = {
                    'name': user[1],   # Correct index for name
                    'email': user[2],  # Correct index for email
                    'dobb': user[6],   # Correct index for dobb
                    'bio': user[5]     # Correct index for bio
                }
                return render_template('edit_profile.html', user=user_data)
            else:
                flash('User not found.', 'danger')
                return redirect('/sign_in')

        except Exception as e:
            flash('Error fetching user data: ' + str(e), 'danger')
            return redirect('/sign_in')

# Assume 'mysql' is the MySQL connection already set up in the Flask app.

@app.route('/exercises', methods=['GET'])
def exercises():
    if 'user_id' not in session:
        flash('Please log in to access the exercise tracker.', 'danger')
        return redirect('/sign_in')
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, sets, reps, progress FROM exercises WHERE user_id = %s", (session['user_id'],))
    exercises = cur.fetchall()
    cur.close()

    return render_template('exercise.html', exercises=exercises)


@app.route('/add_exercise', methods=['POST'])
def add_exercise():
    if 'user_id' not in session:
        flash('Please log in to add exercises.', 'danger')
        return redirect('/sign_in')

    name = request.form.get('exercise_name')
    sets = request.form.get('sets')
    reps = request.form.get('reps')
    progress = request.form.get('progress')

    if not name or not sets or not reps or not progress:
        flash('All fields are required!', 'danger')
        return redirect('/exercises')

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO exercises (user_id, name, sets, reps, progress)
        VALUES (%s, %s, %s, %s, %s)
        """, (session['user_id'], name, sets, reps, progress))
    mysql.connection.commit()
    cur.close()

    flash('Exercise added successfully!', 'success')
    return redirect('/exercises')


@app.route('/delete_exercise', methods=['POST'])
def delete_exercise():
    if 'user_id' not in session:
        flash('Please log in to delete exercises.', 'danger')
        return redirect('/sign_in')

    exercise_id = request.form.get('exercise_id')

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM exercises WHERE id = %s AND user_id = %s", (id, session['user_id']))
    mysql.connection.commit()
    cur.close()

    flash('Exercise deleted successfully!', 'success')
    return redirect('/exercises')


if __name__ == '__main__':
    app.run(debug=True)
