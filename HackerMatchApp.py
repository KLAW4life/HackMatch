from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Get the database credentials
load_dotenv()

HackerMatchApp = Flask(__name__)

# Set the secret key from the environment variable for encrypting the session
HackerMatchApp.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Database connection configuration using environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'auth_plugin': os.getenv('AUTH_PLUGIN')
}

# API endpoint to retrieve all users

@HackerMatchApp.route('/')
def index():
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))
    
@HackerMatchApp.route('/about-us')
def about_us():
    return render_template('aboutus.html')
    

@HackerMatchApp.route('/users', methods=['GET'])
def get_users():
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        sql = "SELECT * FROM Users"
        mycursor.execute(sql)
        results = mycursor.fetchall()
        
        mycursor.close()
        mydb.close()
        return jsonify(results)
    except mysql.connector.Error as e:
        print("Error fetching users:", e)
        return []
    
@HackerMatchApp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        major = request.form['major']
        classStanding = request.form['classStanding']
        skills = request.form['skills']
        desiredProject = request.form['desiredProject']
        project_description = request.form['project_description']
        


        if register_user(password, first_name, last_name, email, username, major, classStanding, skills, desiredProject, project_description):
            return redirect(url_for('login')) 
        else:
            return render_template('register.html', error='Error registering user')
    else:
        # Fetch available majors, langauges, desired projects and desired role from the database
        majors = get_available_majors()
        lang = get_skills()
        interest = get_projects()

        return render_template('register.html', majors=majors, lang=lang, interest=interest)


    
# Represents roles in database schema   
def get_available_majors():
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT role_name FROM Roles")
        majors = [row[0] for row in mycursor.fetchall()]
        mycursor.close()
        mydb.close()
        return majors
    except mysql.connector.Error as e:
        print("Error fetching majors:", e)
        return []

# Represents programming languages in database schema   
def get_skills():
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT language_name FROM Languages")
        lang = [row[0] for row in mycursor.fetchall()]
        mycursor.close()
        mydb.close()
        return lang
    except mysql.connector.Error as e:
        print("Error fetching programming languages:", e)
        return []    

# Represents programming desired projects in database schema   
def get_projects():
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT interest_name FROM ProjectInterests")
        interest = [row[0] for row in mycursor.fetchall()]
        mycursor.close()
        mydb.close()
        return interest
    except mysql.connector.Error as e:
        print("Error fetching project interests:", e)
        return []   
    
def register_user(password, first_name, last_name, email, username, major, classStanding, skills, desiredProject, project_description):
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        # Insert user data into Users table
        user_insert_query = """
        INSERT INTO Users (first_name, last_name, email, username, password, major, class_standing, project_description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        user_data = (first_name, last_name, email, username, password, major, classStanding, project_description)
        mycursor.execute(user_insert_query, user_data)

        # Get the user ID of the newly inserted user
        user_id = mycursor.lastrowid

        
        mycursor.execute(skill_insert_query, (user_id, skill))
        if skills:
            for skill in skills:
                skill_insert_query = """
                INSERT INTO UserLanguages (user_id, language_id)
                VALUES (
                    %s, 
                    (SELECT id FROM Languages WHERE language_name = %s)
                )
                """

        # Insert desired project
        project_insert_query = """
        INSERT INTO UserProjectInterests (user_id, project_id)
        VALUES (
            %s,
            (SELECT id FROM Projects WHERE project_name = %s)
        )
        """
        mycursor.execute(project_insert_query, (user_id, desiredProject))

        # Insert user role based on major
        role_insert_query = """
        INSERT INTO UserRoles (user_id, role_id)
        VALUES (
            %s,
            (SELECT id FROM Roles WHERE role_name = %s)
        )
        """
        mycursor.execute(role_insert_query, (user_id, major))

        mydb.commit()

        return True

    except Error as e:
        print("Error inserting data:", e)
        return False

    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()


@HackerMatchApp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')
    
def authenticate_user(username, password):
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        sql = "SELECT username, password FROM Users WHERE username = %s AND password = %s"
        values = (username, password)
        mycursor.execute(sql, values)
        user = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        return user is not None
    except mysql.connector.Error as e:
        print("Error authenticating user:", e)
        return False

if __name__ == '__main__':
    HackerMatchApp.run(debug=True)