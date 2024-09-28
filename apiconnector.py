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

#Test User
db_config = {
    'host': 'localhost',        
    'user': 'root',        
    'password': 'Kl@w$li3e!',
    'database': 'HackerMatch',
    'auth_plugin': 'mysql_native_password'
}

# def get_users():
#     try:
#         # Connect to the database
#         mydb = mysql.connector.connect(**db_config)
        
#         mycursor = mydb.cursor()
#         sql = "SELECT * FROM Users"
#         mycursor.execute(sql)
#         results = mycursor.fetchall()

#         # Close the cursor and connection
#         mycursor.close()
#         mydb.close()
        
#         # Convert the results to a list of dictionaries for easy JSON conversion
#         users = []
#         for row in results:
#             user = {
#                 "id": row[0],
#                 "firstname": row[1],
#                 "lastname": row[2],
#                 "email": row[3],
#                 "username": row[4]
#             }
#             users.append(user)
        
#         return json.dumps(users, indent=4)  # Return as a formatted JSON string
#     except mysql.connector.Error as e:
#         print("Error fetching users:", e)
#         return []

def get_users_details():
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor(dictionary=True)
        
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
        
        mycursor.execute(sql)
        results = mycursor.fetchall()
        
        mycursor.close()
        mydb.close()

        json_results = json.dumps(results, indent=4)
        return json_results
    except mysql.connector.Error as e:
        error_message = {"error": f"Error fetching users: {e}"}
        return json.dumps(error_message, indent=4)


def main():
    # users = get_users()
    # if users:
    #     print(users)
    users = get_users_details()
    print(users)


    

if __name__ == "__main__":
  main()





