from flask import Flask, render_template, request, redirect, session, flash,url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash 

app = Flask(__name__)
mysql = MySQL(app)
app.config

# MySQL configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Wsanchez00$'
app.config['MYSQL_DB'] = 'fitness'



@app.route('/')
def homepage():
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM fitness")
    # data = cur.fetchall()

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

        # Do something with the user details (e.g., save to database)
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO fitness.user(name, dob, email, password) VALUES(%s, %s, %s, %s)", (name, dob, email, hashed_password ))
            mysql.connection.commit()
            cur.close()
            flash('You have successfully signed up!', 'success')
            return redirect('/sign_in')
        except Exception as e:
            flash('Error: ' + str(e), 'danger')
            return redirect('/sign_up')
        print(f"New user: {'name'} , {'email'}, {'password'}, {'email'}")

        # Redirect to homepage after sign-up
        return redirect(url_for('sign_in'))
    return render_template('sign_up.html')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
     if request.method == 'POST':
         name = request.form['name']
         password = request.form['password']
         #cur = mysql.connection.cursor()
        #  cur.execute("SELECT * FROM user WHERE name = %s", (name,))
        #  user = cur.fetchone()
        #  cur.close()
        
         if user and check_password_hash(user[2], password):
             session['name'] = name
             flash('Login successful!', 'success')
             return redirect('/dashboard')
         else:
             flash('Invalid name or password!', 'danger')

     return render_template('sign_in.html')
# Logout route
@app.route('/logout')
def logout():
    session.pop('name', None)
    flash('You have been logged out!', 'success')
    return redirect('/sign_in')

# Main page route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)