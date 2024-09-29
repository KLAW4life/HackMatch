# Import the necessary functionality from apiconnector.py
from apiconnector import db_config, get_users_data, send_message, get_thread_messages
import mysql.connector

# Function to accept or reject a match request
def respond_to_match_request(user1_id, user2_id, response):
    try:
        # Connect to the database using the imported db_config from apiconnector.py
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        if response == "accept":
            # Step 1: Create a new team and insert both users into the team
            team_name = f"Team_{user1_id}_{user2_id}"  # Example team name
            project_name = "Project_X"  # Example project name
            create_team_sql = "INSERT INTO FullTeams (team_name, project_name) VALUES (%s, %s)"
            mycursor.execute(create_team_sql, (team_name, project_name))
            
            # Get the team_id of the newly created team
            team_id = mycursor.lastrowid # Get the newly created team ID

            # Step 2: Insert both users into TeamMembers
            insert_team_member_sql = "INSERT INTO TeamMembers (team_id, user_id) VALUES (%s, %s)"
            mycursor.execute(insert_team_member_sql, (team_id, user1_id))
            mycursor.execute(insert_team_member_sql, (team_id, user2_id))

            # Step 3: Update MatchRequests table to 'accepted'
            update_match_request_sql = "UPDATE MatchRequests SET status = 'accepted' WHERE user1_id = %s AND user2_id = %s"
            mycursor.execute(update_match_request_sql, (user1_id, user2_id))

            print(f"Match request accepted. Team '{team_name}' created with members {user1_id} and {user2_id}.")

        elif response == "reject":
            # Step 4: If rejected, just update the MatchRequests table to 'rejected'
            update_match_request_sql = "UPDATE MatchRequests SET status = 'rejected' WHERE user1_id = %s AND user2_id = %s"
            mycursor.execute(update_match_request_sql, (user1_id, user2_id))
            
            print(f"Match request rejected between user {user1_id} and user {user2_id}.")

        # Commit the changes to the database
        mydb.commit()

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

    except mysql.connector.Error as e:
        print(f"Error responding to match request: {e}")

# Function to get the number of team members in a team
def get_team_member_count(team_id):
    try:
        # Connect to the database using the dynamic db_config from apiconnector.py
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        # Get the number of members in the team
        count_sql = "SELECT COUNT(*) FROM TeamMembers WHERE team_id = %s"
        mycursor.execute(count_sql, (team_id,))
        member_count = mycursor.fetchone()[0]

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        return member_count

    except mysql.connector.Error as e:
        print(f"Error getting team member count: {e}")
        return 0

# Function to fetch all members of a team
def get_team_members(team_id):
    try:
        # Connect to the database using the dynamic db_config from apiconnector.py
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        # SQL query to get all members of the team, joining with Users table to get user details
        sql = """
            SELECT u.id, u.firstname, u.lastname, u.email, u.username
            FROM TeamMembers tm
            INNER JOIN Users u ON tm.user_id = u.id
            WHERE tm.team_id = %s
        """
        mycursor.execute(sql, (team_id,))
        team_members = mycursor.fetchall()

        # Close the cursor and connection
        mycursor.close()
        mydb.close()

        # Display team members
        if team_members:
            print(f"Members of team {team_id}:")
            for member in team_members:
                print(f"User ID: {member[0]}, Name: {member[1]} {member[2]}, Email: {member[3]}, Username: {member[4]}")
        else:
            print(f"No members found for team {team_id}.")

    except mysql.connector.Error as e:
        print(f"Error fetching team members: {e}")

# Example usage
def main():
    user1_id = 1  # Example: Alice Smith's user ID
    user2_id = 2  # Example: Thomas Young's user ID

    # Accept the match request and form a team
    respond_to_match_request(user1_id, user2_id, "accept")

    # Reject a match request
    # respond_to_match_request(user1_id, user2_id, "reject")

    # Get the count of team members in a specific team (example team_id: 1)
    team_id = 1
    member_count = get_team_member_count(team_id)
    print(f"Team {team_id} has {member_count} members.")

    # Fetch and display the members of the team
    get_team_members(team_id)

if __name__ == "__main__":
    main()
