-- Create a new user for test database
CREATE USER 'admin_user'@'localhost' IDENTIFIED BY 'password';

-- Giving them admin privilages
CREATE ROLE 'admin_role';

-- Grant all privileges 
GRANT ALL PRIVILEGES ON HackerMatch.* TO 'admin_role';

-- Assign the role to the user
GRANT 'admin_role' TO 'admin_user'@'localhost';

FLUSH PRIVILEGES;
