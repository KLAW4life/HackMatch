import mysql.connector
import json

# Database connection configuration
db_config = {
    'host': 'localhost',        
    'user': 'root',        
    'password': 'Kl@w$li3e!',
    'database': 'HackerMatch',
    'auth_plugin': 'mysql_native_password'
}

# Function to fetch users with their roles, languages, and project interests
def get_users_with_details():
    try:
        # Connect to the database
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor(dictionary=True)
        
        # SQL query to fetch user information along with their roles, languages, and interests
        sql = """
            SELECT 
                u.id, u.firstname, u.lastname, u.email, u.username,
                GROUP_CONCAT(DISTINCT r.role_name) AS roles,
                GROUP_CONCAT(DISTINCT l.language_name) AS languages,
                GROUP_CONCAT(DISTINCT pi.interest_name) AS interests
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
            GROUP BY 
                u.id, u.firstname, u.lastname, u.email, u.username
        """
        
        # Execute the query
        mycursor.execute(sql)
        results = mycursor.fetchall()
        
        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        # Convert results to JSON string
        json_results = json.dumps(results, indent=4)
        return json_results
    except mysql.connector.Error as e:
        # Handle database errors
        error_message = {"error": f"Error fetching users: {e}"}
        return json.dumps(error_message, indent=4)

# Main function to print the JSON output
def main():
    users = get_users_with_details()
    print(users)

if __name__ == '__main__':
    main()
