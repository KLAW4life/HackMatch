CREATE DATABASE IF NOT EXISTS HackerMatch;

USE HackerMatch;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
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
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (role_id) REFERENCES Roles(id)
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
