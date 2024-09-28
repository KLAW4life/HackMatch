import mysql.connector
import json

''' 
# Database connection configuration for Ubuntu Specific
db_config = {
    'host': 'localhost',        
    'user': 'test_user',        
    'password': 'test_password',
    'database': 'HackerMatch' ,
    'auth_plugin': 'mysql_native_password'  
}


# Database connection configuration for Mac/Windows
db_config = {
    'host': 'localhost',        
    'user': 'test_user',        
    'password': 'test_password',
    'database': 'HackerMatch'
}
'''

db_config = {
    'host': 'localhost',        
    'user': 'root',        
    'password': 'Kl@w$li3e!',
    'database': 'HackerMatch',
    'auth_plugin': 'mysql_native_password'
}

# Function to fetch users data and team (if formed and confirmed)
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

        # Convert results to JSON string
        json_results = json.dumps(results, indent=4)
        return json_results
    except mysql.connector.Error as e:
        # Handle database errors
        error_message = {"error": f"Error fetching users in full teams: {e}"}
        return json.dumps(error_message, indent=4)


def main():
    users = get_users_data()
    print(users)

if __name__ == '__main__':
    main()





