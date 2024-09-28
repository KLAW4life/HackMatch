import mysql.connector
# import jsonify
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

def get_users():
    try:

       #Use test person to connect to the database. Reconfigure per person
        mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Kl@w$li3e!',
        database='HackerMatch',
        auth_plugin='mysql_native_password'
        )
        
        mycursor = mydb.cursor()
        sql = "SELECT * FROM Users"
        mycursor.execute(sql)
        results = mycursor.fetchall()
        
        mycursor.close()
        mydb.close()
        return results
    except mysql.connector.Error as e:
        print("Error fetching users:", e)
        return []
    
    
def main():
    get_users()


if __name__ == "__main__":
  main()
