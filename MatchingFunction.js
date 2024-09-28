function computeMatchScore(userA, userB) {
    let score = 0;
  
    // 1. Compare project interests
    const projectInterestMatch = userA.projectInterests.some(interest =>
      userB.projectInterests.includes(interest)
    );
    if (projectInterestMatch) score += 0.5; // 50%
  
    // 2. Compare roles
    if (userA.role === userB.role) {
      score += 0.3; // 30%
    }
  
    // 3. Compare skills
    const commonSkills = userA.skills.filter(skill =>
      userB.skills.includes(skill)
    );
    if (commonSkills.length > 0) {
      score += 0.2; // 20%
    }
  
    return score;
  }
  