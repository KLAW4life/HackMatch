from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

HackerMatchApp = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'localhost',        
    'user': 'test_user',        
    'password': 'test_password',
    'database': 'HackerMatch'   
}

# API endpoint to retrieve all users
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
    
# Test functions
def main():
  get_users()
  

if __name__ == '__main__':
    main()
    
