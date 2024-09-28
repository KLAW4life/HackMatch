import mysql.connector

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Machete67!',
    'database': 'HackerMatch',
    'auth_plugin': 'mysql_native_password'
}

# Function to fetch users from the database
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

# Main function to run the match scoring and feed generation
def main():
    users = get_users()  # Get users from the database
    if users:
        current_user = users[0]  # Assume the first user is the current user
        feed = generate_feed(current_user, users)  # Generate feed

        # Apply the filter by percentage (e.g., 50%)
        filtered_feed = filter_feed_by_percentage(feed, 30)

        # Print the results
        print(f"Feed generated for {current_user['firstname']} {current_user['lastname']}:")
        for entry in filtered_feed:
            user = entry['user']
            print(f"Matched with {user['firstname']} {user['lastname']} (Match Score: {entry['match_score']})")

if __name__ == "__main__":
    main()
