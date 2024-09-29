import mysql.connector
import json
from dotenv import load_dotenv
import os

# Get the database credentials
load_dotenv()

# Database connection configuration using environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'auth_plugin': os.getenv('AUTH_PLUGIN')
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


# Function to send a message
def send_message(sender_id, receiver_id, content):
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()
        
        # Check if thread exists; if not it will be created
        mycursor.execute("""
            INSERT INTO Threads (user1_id, user2_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE id=id
        """, (sender_id, receiver_id))

        # Get thread ID
        mycursor.execute("""
            SELECT id FROM Threads 
            WHERE (user1_id = %s AND user2_id = %s) OR (user1_id = %s AND user2_id = %s)
        """, (sender_id, receiver_id, receiver_id, sender_id))
        thread_id = mycursor.fetchone()[0]

        # Insert the message
        mycursor.execute("""
            INSERT INTO Messages (sender_id, receiver_id, content)
            VALUES (%s, %s, %s)
        """, (sender_id, receiver_id, content))
        message_id = mycursor.lastrowid

        # Link the message to the thread in the database
        mycursor.execute("""
            INSERT INTO ThreadMessages (thread_id, message_id)
            VALUES (%s, %s)
        """, (thread_id, message_id))

        mydb.commit()
        print("Message sent successfully.")
    except mysql.connector.Error as e:
        print("Error sending message:", e)
    finally:
        mycursor.close()
        mydb.close()

# Function to retrieve messages in a thread
def get_thread_messages(user1_id, user2_id):
    try:
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor(dictionary=True)

        # Get the thread ID
        mycursor.execute("""
            SELECT id FROM Threads 
            WHERE (user1_id = %s AND user2_id = %s) OR (user1_id = %s AND user2_id = %s)
        """, (user1_id, user2_id, user2_id, user1_id))
        thread = mycursor.fetchone()
        
        # Check if there are any threads
        if not thread:
            print("No messages found.")
            return []

        thread_id = thread['id']

        # Fetch messages linked to the thread id in database
        mycursor.execute("""
            SELECT m.content, m.timestamp, u.firstname AS sender_name
            FROM Messages m
            JOIN Users u ON m.sender_id = u.id
            JOIN ThreadMessages tm ON m.id = tm.message_id
            WHERE tm.thread_id = %s
            ORDER BY m.timestamp
        """, (thread_id,))
        messages = mycursor.fetchall()

        return messages
    except mysql.connector.Error as e:
        print("Error fetching messages:", e)
        return []
    finally:
        mycursor.close()
        mydb.close()

def main():
     users = get_users_data()
     print(users)

    # Test
    #send_message(sender_id=1, receiver_id=2, content="Hello! How are you?")

    # Get messages from a thread
    # messages = get_thread_messages(user1_id=1, user2_id=2)
    # for message in messages:
    #     print(f"{message['sender_name']}: {message['content']} at {message['timestamp']}")

if __name__ == '__main__':
    main()
