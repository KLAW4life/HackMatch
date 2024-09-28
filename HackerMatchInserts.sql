INSERT INTO Users (firstname, lastname, email, username, password, status, project_description, class_standing)
VALUES
('Alice', 'Smith', 'alice.smith@example.com', 'alice_smith', 'password1', 'available', 'Interested in building AI-based projects', 'junior'),
('Bob', 'Johnson', 'bob.johnson@example.com', 'bob_johnson', 'password2', 'available', 'Looking for a front-end team', 'senior'),
('Charlie', 'Williams', 'charlie.williams@example.com', 'charlie_w', 'password3', 'available', 'Interested in VR development', 'masters'),
('David', 'Jones', 'david.jones@example.com', 'david_j', 'password4', 'matched', NULL, 'phd'),
('Eva', 'Brown', 'eva.brown@example.com', 'eva_b', 'password5', 'available', 'Working on cybersecurity projects', 'freshmen'),
('Frank', 'Miller', 'frank.miller@example.com', 'frank_m', 'password6', 'available', 'Passionate about AR technology', 'junior'),
('Grace', 'Davis', 'grace.davis@example.com', 'grace_d', 'password7', 'matched', 'Interested in AI and ML', 'senior'),
('Henry', 'Wilson', 'henry.wilson@example.com', 'henry_w', 'password8', 'available', 'Building game development projects', 'sophomore'),
('Isla', 'Taylor', 'isla.taylor@example.com', 'isla_t', 'password9', 'available', 'Focused on software engineering', 'graduated'),
('Jack', 'Anderson', 'jack.anderson@example.com', 'jack_a', 'password10', 'available', 'Working on web development projects', 'freshmen'),
('Kara', 'Thomas', 'kara.thomas@example.com', 'kara_t', 'password11', 'available', 'Interested in VR and AR', 'junior'),
('Liam', 'Martinez', 'liam.martinez@example.com', 'liam_m', 'password12', 'matched', NULL, 'phd'),
('Mia', 'Garcia', 'mia.garcia@example.com', 'mia_g', 'password13', 'available', 'Working on mobile app development', 'masters'),
('Noah', 'Lopez', 'noah.lopez@example.com', 'noah_l', 'password14', 'available', 'Developing full-stack applications', 'senior'),
('Olivia', 'Gonzalez', 'olivia.gonzalez@example.com', 'olivia_g', 'password15', 'available', '2D game development enthusiast', 'sophomore'),
('Paul', 'Clark', 'paul.clark@example.com', 'paul_c', 'password16', 'matched', 'VR and AR development focus', 'graduated'),
('Quincy', 'Lee', 'quincy.lee@example.com', 'quincy_l', 'password17', 'available', 'Exploring AI and ML', 'freshmen'),
('Riley', 'Hall', 'riley.hall@example.com', 'riley_h', 'password18', 'available', 'Interested in back-end development', 'junior'),
('Sophia', 'Allen', 'sophia.allen@example.com', 'sophia_a', 'password19', 'available', 'Data analytics projects', 'masters'),
('Thomas', 'Young', 'thomas.young@example.com', 'thomas_y', 'password20', 'available', '3D game development focus', 'senior'),
('Uma', 'Hernandez', 'uma.hernandez@example.com', 'uma_h', 'password21', 'available', 'Cybersecurity projects', 'sophomore'),
('Victor', 'King', 'victor.king@example.com', 'victor_k', 'password22', 'matched', NULL, 'phd'),
('Wendy', 'Wright', 'wendy.wright@example.com', 'wendy_w', 'password23', 'available', 'Passionate about AR', 'graduated'),
('Xander', 'Scott', 'xander.scott@example.com', 'xander_s', 'password24', 'available', 'Working on UI/UX', 'senior'),
('Yara', 'Green', 'yara.green@example.com', 'yara_g', 'password25', 'available', 'Software engineering focus', 'masters'),
('Zane', 'Baker', 'zane.baker@example.com', 'zane_b', 'password26', 'available', '2D game development', 'junior'),
('Anna', 'Nelson', 'anna.nelson@example.com', 'anna_n', 'password27', 'available', 'Web development projects', 'sophomore'),
('Ben', 'Carter', 'ben.carter@example.com', 'ben_c', 'password28', 'matched', 'AI and ML projects', 'phd'),
('Carla', 'Mitchell', 'carla.mitchell@example.com', 'carla_m', 'password29', 'available', 'VR/AR applications', 'graduated'),
('Daniel', 'Perez', 'daniel.perez@example.com', 'daniel_p', 'password30', 'available', 'Cybersecurity focus', 'junior');

-- Insert Roles (same roles)
INSERT INTO Roles (role_name) VALUES
('Front-end'),
('Back-end'),
('Data Science'),
('Data Analytics'),
('AI'),
('ML'),
('UI/UX'),
('2D Game Dev'),
('3D Game Dev'),
('VR'),
('AR'),
('Cyber Security'),
('Full Stack');

INSERT INTO Languages (language_name) VALUES
('Python'),
('JavaScript'),
('Java'),
('Swift'),
('Ruby'),
('Kotlin'),
('React.js'),
('Vue.js'),
('Node.js'),
('Django'),
('Flask'),
('ASP.NET'),
('MySQL'),
('PostgreSQL'),
('MongoDB'),
('R'),
('NoSQL'),
('TypeScript'),
('C++');

INSERT INTO ProjectInterests (interest_name) VALUES
('VR'),
('AR'),
('AI'),
('ML'),
('2D Game Dev'),
('3D Game Dev'),
('Web Dev'),
('Software Engineering'),
('Cyber Security');

INSERT INTO UserRoles (user_id, role_id) VALUES
(1, 1), (2, 2), (3, 10), (4, 5), (5, 12),
(6, 9), (7, 6), (8, 8), (9, 4), (10, 1),
(11, 10), (12, 5), (13, 7), (14, 13), (15, 11),
(16, 3), (17, 4), (18, 2), (19, 1), (20, 9),
(21, 12), (22, 8), (23, 6), (24, 7), (25, 11),
(26, 3), (27, 4), (28, 10), (29, 9), (30, 5);

INSERT INTO UserLanguages (user_id, language_id) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
(6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
(11, 11), (12, 12), (13, 13), (14, 14), (15, 15),
(16, 16), (17, 17), (18, 18), (19, 19), (20, 1),
(21, 2), (22, 3), (23, 4), (24, 5), (25, 6),
(26, 7), (27, 8), (28, 9), (29, 10), (30, 11);

INSERT INTO UserProjectInterests (user_id, interest_id) VALUES
(1, 3), (2, 4), (3, 9), (4, 1), (5, 8),
(6, 2), (7, 5), (8, 6), (9, 7), (10, 1),
(11, 3), (12, 4), (13, 8), (14, 9), (15, 5),
(16, 6), (17, 7), (18, 1), (19, 2), (20, 3),
(21, 4), (22, 5), (23, 9), (24, 8), (25, 7),
(26, 2), (27, 6), (28, 1), (29, 3), (30, 4);

INSERT INTO MatchRequests (user1_id, user2_id, status) VALUES
(1, 2, 'accepted'),
(3, 4, 'pending'),
(5, 6, 'rejected'),
(7, 8, 'accepted'),
(9, 10, 'pending'),
(11, 12, 'accepted'),
(13, 14, 'rejected'),
(15, 16, 'pending'),
(17, 18, 'accepted'),
(19, 20, 'pending'),
(21, 22, 'accepted'),
(23, 24, 'rejected'),
(25, 26, 'accepted'),
(27, 28, 'pending'),
(29, 30, 'accepted');

INSERT INTO FullTeams (team_name, project_name) VALUES
('Team Alpha', 'VR Exploration'),
('Team Beta', 'AI Chatbot'),
('Team Gamma', 'AR Adventure'),
('Team Delta', 'Web Security System'),
('Team Epsilon', '2D Game Development');

INSERT INTO TeamMembers (team_id, user_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4),
(2, 5), (2, 6), (2, 7), (2, 8),
(3, 9), (3, 10), (3, 11), (3, 12),
(4, 13), (4, 14), (4, 15), (4, 16),
(5, 17), (5, 18), (5, 19), (5, 20);
