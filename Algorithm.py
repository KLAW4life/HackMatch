def compute_match_score(userA, userB):
    score = 0.0

    # 1. Compare project interests
    project_interest_match = any(interest in userB['projectInterests'] for interest in userA['projectInterests'])
    if project_interest_match:
        score += 0.5  # 50%

    # 2. Compare roles
    if userA['role'] == userB['role']:
        score += 0.3  # 30%

    # 3. Compare skills
    common_skills = set(userA['skills']).intersection(set(userB['skills']))
    if len(common_skills) > 0:
        score += 0.2  # 20%

    return score


def generate_feed(current_user, users):
    feed = []

    for user in users:
        if user['id'] != current_user['id']:  # Exclude self
            score = compute_match_score(current_user, user)
            feed.append({
                "user": user,
                "score": score
            })

    # Sort the feed by match score (highest score first)
    feed.sort(key=lambda x: x['score'], reverse=True)
    return feed


@app.route('/api/users', methods=['GET'])
def get_users():
    # Assuming the first user is the current user for now
    current_user = users[0]
    
    # Generate feed based on the current user
    feed = generate_feed(current_user, users)
    
    return jsonify({
        "currentUserData": current_user,
        "feed": feed
    })

if __name__ == '__main__':
    app.run(debug=True)
