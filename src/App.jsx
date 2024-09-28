import Header from "./Components/Header";
import Card from "./Components/Card";
import TitleFront from "./Components/TitleFront";

function App() {
  return (
    <>
      <Header></Header>
      <TitleFront></TitleFront>
      <Card
        info="The one stop spot for finding teammates for your hackathons. HackerMatch pairs you with like minded individuals that are driven to creating amazing projects during hackathons Please make an account to begin and happy coding!"
        image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSe_z8jZVU9cvwMdeoO2su-W9uWWIws0neiDw&s"
      ></Card>
    </>
  );
}

export default App;
