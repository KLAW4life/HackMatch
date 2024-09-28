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

def get_users():
    try:
        # Connect to the database
        mydb = mysql.connector.connect(**db_config)
        
        mycursor = mydb.cursor()
        sql = "SELECT * FROM Users"
        mycursor.execute(sql)
        results = mycursor.fetchall()

        # Close the cursor and connection
        mycursor.close()
        mydb.close()
        
        # Convert the results to a list of dictionaries for easy JSON conversion
        users = []
        for row in results:
            user = {
                "id": row[0],
                "firstname": row[1],
                "lastname": row[2],
                "email": row[3],
                "username": row[4]
            }
            users.append(user)
        
        return json.dumps(users, indent=4)  # Return as a formatted JSON string
    except mysql.connector.Error as e:
        print("Error fetching users:", e)
        return []


def main():
    users = get_users()
    if users:
        print(users)


if __name__ == "__main__":
  main()





