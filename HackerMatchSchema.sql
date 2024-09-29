- DROP DATABASE HackerMatch;

CREATE DATABASE IF NOT EXISTS HackerMatch;

USE HackerMatch;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    status ENUM('available', 'matched') DEFAULT 'available',
    project_description TEXT,
    class_standing ENUM('freshmen', 'sophomore', 'junior', 'senior', 'graduated', 'masters', 'phd') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Languages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    language_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE ProjectInterests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    interest_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE UserRoles (
    user_id INT,
    role_id INT,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES Roles(id) ON DELETE CASCADE
);


CREATE TABLE UserLanguages (
    user_id INT,
    language_id INT,
    PRIMARY KEY (user_id, language_id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (language_id) REFERENCES Languages(id)
);

CREATE TABLE UserProjectInterests (
    user_id INT,
    interest_id INT,
    PRIMARY KEY (user_id, interest_id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (interest_id) REFERENCES ProjectInterests(id)
);

CREATE TABLE Messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (sender_id) REFERENCES Users(id),
    FOREIGN KEY (receiver_id) REFERENCES Users(id)
);

CREATE TABLE Threads (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user1_id INT,
    user2_id INT,
    FOREIGN KEY (user1_id) REFERENCES Users(id),
    FOREIGN KEY (user2_id) REFERENCES Users(id)
);

CREATE TABLE ThreadMessages (
    thread_id INT,
    message_id INT,
    PRIMARY KEY (thread_id, message_id),
    FOREIGN KEY (thread_id) REFERENCES Threads(id),
    FOREIGN KEY (message_id) REFERENCES Messages(id)
);

CREATE TABLE MatchRequests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user1_id INT,
    user2_id INT,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
    FOREIGN KEY (user1_id) REFERENCES Users(id),
    FOREIGN KEY (user2_id) REFERENCES Users(id)
);

CREATE TABLE FullTeams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    project_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE TeamMembers (
    team_id INT,
    user_id INT,
    PRIMARY KEY (team_id, user_id),
    FOREIGN KEY (team_id) REFERENCES FullTeams(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);