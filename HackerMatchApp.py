from flask import Flask, jsonify, request, render_template, session, redirect, url_for, json, flash
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
        return render_template('matchingpage.html')
    else:
        return render_template('home.html')
    # return redirect(url_for('login'))
    
@HackerMatchApp.route('/about-us')
def about_us():
    return render_template('aboutus.html')

@HackerMatchApp.route('/messages')
def message_chat():
    return render_template('chatpage.html') 

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
        user_id = authenticate_user(username, password)
        
        if user_id:
            session['username'] = username
            session['user_id'] = user_id  
            
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')
    
def authenticate_user(username, password):
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        
        sql = "SELECT id, username, password FROM Users WHERE username = %s AND password = %s"
        values = (username, password) 
        
        mycursor.execute(sql, values)
        user = mycursor.fetchone() 
        
        mycursor.close()
        mydb.close()

        # If user is found, return the user ID
        if user:
            return user[0]  # Assuming the first column is the user ID
        else:
            return None
    except mysql.connector.Error as e:
        print("Error authenticating user:", e)
        return False
    
@HackerMatchApp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

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

@HackerMatchApp.route('/teams', methods=['GET'])
def display_teams():
    # Get the users and teams data directly from the function
    users_data = get_users_data()

    # Check if the result contains an error
    if 'error' in users_data:
        return render_template('teams.html', error=users_data['error'])

    # Pass the data to the template without converting to JSON
    return render_template('teams.html', users_data=users_data)

def get_users_data():
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor(dictionary=True)
        
        sql = """
            SELECT 
                u.id, u.firstname, u.lastname, u.email, u.username,
                u.status, u.project_description, u.class_standing,
                GROUP_CONCAT(DISTINCT r.role_name) AS roles,
                GROUP_CONCAT(DISTINCT l.language_name) AS languages,
                GROUP_CONCAT(DISTINCT pi.interest_name) AS interests,
                ft.team_name
            FROM 
                Users u
            LEFT JOIN 
                UserRoles ur ON u.id = ur.user_id
            LEFT JOIN 
                Roles r ON ur.role_id = r.id
            LEFT JOIN 
                UserLanguages ul ON u.id = ul.user_id
            LEFT JOIN 
                Languages l ON ul.language_id = l.id
            LEFT JOIN 
                UserProjectInterests upi ON u.id = upi.user_id
            LEFT JOIN 
                ProjectInterests pi ON upi.interest_id = pi.id
            INNER JOIN 
                TeamMembers tm ON u.id = tm.user_id
            INNER JOIN 
                FullTeams ft ON tm.team_id = ft.id
            GROUP BY 
                u.id, u.firstname, u.lastname, u.email, u.username, u.status, u.project_description, u.class_standing, ft.team_name
        """
        
        mycursor.execute(sql)
        results = mycursor.fetchall()
        
        mycursor.close()
        mydb.close()

        # Return the results directly as a Python dictionary
        return results

    except mysql.connector.Error as e:
        # Handle database errors
        return {"error": f"Error fetching users in full teams: {e}"}
    
# def get_current_user_data(user_id):
#     try:
#         with mysql.connector.connect(**db_config) as mydb:
#             with mydb.cursor(dictionary=True) as mycursor:
                
#                 # SQL query to fetch the current user's information
#                 sql = """
#                     SELECT 
#                         u.id, u.firstname, u.lastname, u.email, u.username,
#                         GROUP_CONCAT(DISTINCT pi.interest_name) AS interests,
#                         GROUP_CONCAT(DISTINCT l.language_name) AS skills
#                     FROM 
#                         Users u
#                     LEFT JOIN 
#                         UserProjectInterests upi ON u.id = upi.user_id
#                     LEFT JOIN 
#                         ProjectInterests pi ON upi.interest_id = pi.id
#                     LEFT JOIN 
#                         UserLanguages ul ON u.id = ul.user_id
#                     LEFT JOIN 
#                         Languages l ON ul.language_id = l.id
#                     WHERE 
#                         u.id = %s
#                     GROUP BY 
#                         u.id, u.firstname, u.lastname, u.email, u.username
#                 """
                
#                 # Execute the SQL query with the provided user ID
#                 mycursor.execute(sql, (user_id,))
#                 user_data = mycursor.fetchone()  # Fetch the single result
                
#                 # Return the current user's data
#                 return user_data

#     except mysql.connector.Error as e:
#         # Return an error message in case of a database error
#         return {"error": f"Error fetching current user data: {e}"}


# @HackerMatchApp.route('/feed', methods=['GET'])
# def get_feed():
#     # Current user fetched from database, assumed you pass user_id as query parameter
#     user_id = session.get('user_id')
#     current_user = get_current_user_data(user_id)

#     if not current_user or 'error' in current_user:
#         return jsonify({"error": "Could not fetch user"}), 500

#     # Process user interests and skills into lists
#     current_user['project_interests'] = current_user['interests'].split(',') if current_user['interests'] else []
#     current_user['skills'] = current_user['skills'].split(',') if current_user['skills'] else []

#     # Fetch all users from the database
#     users_data = get_users_data()

#     # Handle any errors from fetching users
#     if 'error' in users_data:
#         return jsonify(users_data), 500

#     # Convert user data into the required format for generating feed
#     users = []
#     for user in users_data:
#         users.append({
#             "id": user['id'],
#             "name": f"{user['firstname']} {user['lastname']}",
#             "project_interests": user['interests'].split(',') if user['interests'] else [],
#             "skills": user['languages'].split(',') if user['languages'] else [],
#             "roles": user['roles'].split(',') if user['roles'] else [],
#             "team_name": user['team_name']
#         })

#     # Generate the feed based on match scores
#     feed = generate_feed(current_user, users)

#     # Filter the feed by match percentage
#     percentage = request.args.get('percentage', default=50, type=int)
#     filtered_feed = filter_feed_by_percentage(feed, percentage)

#     # Render the template with the filtered feed data
#     return render_template('feed.html', feed=filtered_feed)

def get_users():
    try:
        # Connect to the database
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
    
        # Query to fetch users, roles, languages, and project interests
        sql = """
            SELECT u.id, u.firstname, u.lastname, u.email, u.username, 
                   GROUP_CONCAT(DISTINCT r.role_name) AS roles,
                   GROUP_CONCAT(DISTINCT l.language_name) AS languages,
                   GROUP_CONCAT(DISTINCT pi.interest_name) AS project_interests
            FROM Users u
            LEFT JOIN UserRoles ur ON u.id = ur.user_id
            LEFT JOIN Roles r ON ur.role_id = r.id
            LEFT JOIN UserLanguages ul ON u.id = ul.user_id
            LEFT JOIN Languages l ON ul.language_id = l.id
            LEFT JOIN UserProjectInterests upi ON u.id = upi.user_id
            LEFT JOIN ProjectInterests pi ON upi.interest_id = pi.id
            GROUP BY u.id;
        """
    
        mycursor.execute(sql)
        results = mycursor.fetchall()
    
        # Close the cursor and connection
        mycursor.close()
        mydb.close()
    
        # Convert the results to a list of dictionaries
        users = []
        for row in results:
            user = {
                "id": row[0],
                "firstname": row[1],
                "lastname": row[2],
                "email": row[3],
                "username": row[4],
                "roles": row[5].split(',') if row[5] else [],  # Split roles by comma
                "languages": row[6].split(',') if row[6] else [],  # Split languages by comma
                "project_interests": row[7].split(',') if row[7] else []  # Split project interests by comma
            }
            users.append(user)
    
        return users  # Return list of dictionaries instead of JSON string
    except mysql.connector.Error as e:
        print("Error fetching users:", e)
        return []

# Match scoring function
def compute_match_score(userA, userB):
    score = 0
    
    # 1. Compare project interests (50% weight)
    shared_interests = set(userA['project_interests']).intersection(set(userB['project_interests']))
    if shared_interests:
        score += 0.5
    
    # 2. Compare roles (30% weight)
    shared_roles = set(userA['roles']).intersection(set(userB['roles']))
    if shared_roles:
        score += 0.3
    
    # 3. Compare skills (20% weight)
    shared_skills = set(userA['languages']).intersection(set(userB['languages']))
    if shared_skills:
        score += 0.2
    
    return score

# Generate the feed based on matching scores
def generate_feed(current_user, users):
    feed = []
    for user in users:
        if user['id'] != current_user['id']:
            score = compute_match_score(current_user, user)
            feed.append({"user": user, "match_score": score})
    
    # Sort feed by match score (highest to lowest)
    feed = sorted(feed, key=lambda x: x['match_score'], reverse=True)
    
    return feed

# Function to filter the feed by match score percentage
def filter_feed_by_percentage(feed, percentage):
    threshold = percentage / 100  # Convert percentage to a decimal (e.g., 50% -> 0.5)
    
    # Filter out users with match score lower than the threshold
    filtered_feed = [entry for entry in feed if entry['match_score'] >= threshold]
    
    return filtered_feed

# Flask route to display the feed
@HackerMatchApp.route('/feed')
def home():
    # users = get_users() 
    # if users:
    #     current_user = users[0]  
    #     feed = generate_feed(current_user, users)  
    #     filtered_feed = filter_feed_by_percentage(feed, 30)  # Apply filter (e.g., 30%)
    #     return render_template('matchingpage.html', current_user=current_user, feed=filtered_feed)
    # else:
    #     return "No users found."
    users = get_users()  # Get users from the database
    if users:
        current_user = next((user for user in users if user['id'] == session['user_id']), None)  
        if current_user:
            feed = generate_feed(current_user, users)  # Generate feed
            filtered_feed = filter_feed_by_percentage(feed, 30)  # Apply filter (e.g., 30%)
            return render_template('feed.html', current_user=current_user, feed=filtered_feed)
        else:
            return "User not found", 404
    else:
        return "No users found."
    
if __name__ == '__main__':
    HackerMatchApp.run(debug=True)