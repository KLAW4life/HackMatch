from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from Algorithm import get_users, generate_feed, filter_feed_by_percentage

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
    
@HackerMatchApp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@HackerMatchApp.route('/feed/<int:user_id>', methods=['GET'])
def get_user_feed(user_id):
    users = get_users()  # Fetch all users from the database
    if not users:
        return jsonify({"error": "No users found"}), 404

    # Find the current user by ID
    current_user = next((user for user in users if user['id'] == user_id), None)
    if not current_user:
        return jsonify({"error": "User not found"}), 404

    # Generate the feed based on match scores
    feed = generate_feed(current_user, users)

    # Apply filtering by percentage if specified in the query parameter (e.g., ?percentage=50)
    percentage = request.args.get('percentage', default=50, type=int)
    filtered_feed = filter_feed_by_percentage(feed, percentage)

    return jsonify(filtered_feed), 200

if __name__ == '__main__':
    HackerMatchApp.run(debug=True)