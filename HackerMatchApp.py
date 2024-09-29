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
        # match = get_user_matches(session['user_id'])
        return render_template('matchingpage.html')
    else:
        return render_template('home.html')
    # return redirect(url_for('login'))
    
@HackerMatchApp.route('/about-us')
def about_us():
    return render_template('aboutus.html')

@HackerMatchApp.route('/messages')
def message_chat():
    return render_template('message-chat.html') 

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
        stand = get_classStanding()

        return render_template('register.html', majors=majors, lang=lang, interest=interest, stand=stand)


    
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

# Represents student status in database schema   
def get_classStanding():
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT DISTINCT class_standing FROM Users;") 
        stand = [row[0] for row in mycursor.fetchall()]
        # print("Fetched standings:", stand)
        mycursor.close()
        mydb.close()
        return stand
    except mysql.connector.Error as e:
        print("Error fetching class standing options:", e)
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
    

def register_user(password, first_name, last_name, email, username, major, class_standing, skills, desired_project, project_description):
    try:

        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        # Convert skills from a comma-separated string to a list if needed
        if isinstance(skills, str):
            skills = [skill.strip() for skill in skills.split(',')]

        
        # Insert user data into Users table
        user_insert_query = """
        INSERT INTO Users (firstname, lastname, email, username, password, class_standing, project_description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        user_data = (first_name, last_name, email, username, password, class_standing, project_description)
        mycursor.execute(user_insert_query, user_data)

        # Get the user ID of the newly inserted user
        user_id = mycursor.lastrowid

        # Insert skills for the user
        if skills:
            for skill in skills:
                # Check if the language exists in the Languages table
                mycursor.execute("SELECT id FROM Languages WHERE language_name = %s", (skill,))
                language = mycursor.fetchone()

                if language:
                    language_id = language[0]
                    skill_insert_query = """
                    INSERT INTO UserLanguages (user_id, language_id)
                    VALUES (%s, %s)
                    """
                    mycursor.execute(skill_insert_query, (user_id, language_id))
                else:
                    print(f"Warning: Language '{skill}' not found in the Languages table.")

        # Check if the desired project exists in ProjectInterests
        mycursor.execute("SELECT id FROM ProjectInterests WHERE interest_name = %s", (desired_project,))
        interest = mycursor.fetchone()

        # If the project interest doesn't exist, insert it
        if not interest:
            mycursor.execute("INSERT INTO ProjectInterests (interest_name) VALUES (%s)", (desired_project,))
            interest_id = mycursor.lastrowid
        else:
            interest_id = interest[0]

        # Insert the user and interest into UserProjectInterests
        project_insert_query = """
        INSERT INTO UserProjectInterests (user_id, interest_id)
        VALUES (%s, %s)
        """
        mycursor.execute(project_insert_query, (user_id, interest_id))


        # Insert user role based on major (only if a major is provided)
        if major:
            role_insert_query = """
            INSERT INTO UserRoles (user_id, role_id)
            VALUES (
                %s,
                (SELECT id FROM Roles WHERE role_name = %s)
            )
            """
            mycursor.execute(role_insert_query, (user_id, major))

        # Commit the transaction
        mydb.commit()

        return True

    except mysql.connector.Error as e:
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
            # session['user_id'] = get_id(username)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

# def get_id(username):
#     try:
#         mydb = mysql.connector.connect(**db_config)
#         mycursor = mydb.cursor()
#         sql = "SELECT id FROM Users WHERE username = %s;"
#         values = (username)
#         mycursor.execute(sql, values)
#         user = mycursor.fetchone()
#         mycursor.close()
#         mydb.close()
#         return user is not None
#     except mysql.connector.Error as e:
#         print("Error getting user id:", e)
#         return False



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
    
@HackerMatchApp.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Represents student status in database schema   
def get_user_matches(user_id):
    try:
        # Connect to the database
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor(dictionary=True)

        # SQL query to get match requests where the current user is user1 or user2
        query = """
        SELECT m.id, 
               u1.firstname AS user1_firstname, 
               u1.lastname AS user1_lastname,
               u2.firstname AS user2_firstname, 
               u2.lastname AS user2_lastname,
               m.status
        FROM MatchRequests m
        JOIN Users u1 ON m.user1_id = u1.id
        JOIN Users u2 ON m.user2_id = u2.id
        WHERE m.user1_id = %s OR m.user2_id = %s;
        """

        # Execute the query, passing in the current user_id for both placeholders
        mycursor.execute(query, (user_id, user_id))

        # Fetch all the results
        matches = mycursor.fetchall()

        # Close the cursor and the connection
        mycursor.close()
        mydb.close()

        # Return the list of matches
        return matches

    except mysql.connector.Error as e:
        print("Error fetching user matches:", e)
        return []


if __name__ == '__main__':
    HackerMatchApp.run(debug=True)