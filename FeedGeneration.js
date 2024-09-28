function generateFeed(currentUser, users) {
    const feed = users
      .filter(user => user.id !== currentUser.id) // Don’t match the user with themselves
      .map(user => {
        return {
          user: user,
          score: computeMatchScore(currentUser, user),
        };
      })
      .sort((a, b) => b.score - a.score); // Sort by highest match score
  
    return feed;
  }
  