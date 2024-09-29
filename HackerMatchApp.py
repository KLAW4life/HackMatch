from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Get the database credentials
load_dotenv()

HackerMatchApp = Flask(__name__)

# Database connection configuration using environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'auth_plugin': os.getenv('AUTH_PLUGIN')
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
    
