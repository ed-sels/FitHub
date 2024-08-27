from flask import Flask, request, jsonify, render_template

import mysql.connector

# Define database connection parameters
username = 'root'
password = 'Wsanchez00$'
host = '127.0.0.1'
database = 'fitness'

# Establish a connection to the database
cnx = mysql.connector.connect(
    user=username,
    password=password,
    host=host,
    database=database
)

# Create a cursor object
cursor = cnx.cursor()

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('sign-up.html')


@app.route('/sign_up', methods=['POST'])
def sign_up():
    # Get the form data from the request
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    date_of_birth = request.form['dob']

    # Hash the password (you should use a secure hashing algorithm like bcrypt)
    password_hash = password  # Replace with a secure hashing algorithm

    # Insert the user data into the database
    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, email, password_hash))

    # Commit the changes
    cnx.commit()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Return a success message
    return jsonify({'message': 'User created successfully'})

if __name__ == '__main__':
    app.run(debug=True)




# Execute SQL queries
query = "SELECT * FROM information_schema.tables WHERE table_schema = 'fitness'"
cursor.execute(query)

# Fetch all rows
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
cnx.close()