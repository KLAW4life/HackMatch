function UserFeed({ currentUser, users }) {
    const [feed, setFeed] = React.useState([]);
  
    React.useEffect(() => {
      const matchedFeed = generateFeed(currentUser, users);
      setFeed(matchedFeed);
    }, [currentUser, users]);
  
    return (
      <div>
        {feed.map(({ user, score }) => (
          <div key={user.id}>
            <h3>{user.name}</h3>
            <p>University: {user.university}</p>
            <p>Role: {user.role}</p>
            <p>Skills: {user.skills.join(', ')}</p>
            <p>Project Interests: {user.projectInterests.join(', ')}</p>
            <p>Match Score: {score}</p>
            {/* Buttons for Heart (like) and X (reject) */}
            <button>Heart</button>
            <button>X</button>
          </div>
        ))}
      </div>
    );
  }
  