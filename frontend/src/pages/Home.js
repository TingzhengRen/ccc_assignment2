import React from "react";
import employImage from "../images/employ.png";
import './Home.css'

const Home = () => {
    return ( 
      <div className="about">
        <div className="image" style={{ backgroundImage: `url(${employImage})` }}>
          <div className="headerContainer">
            <h1> COMP90024 Project2 </h1>
            <h2>Employment in Victoria</h2>
          </div>
        </div>
        <div className="intro">
          <h1>Project Background/Intro</h1>
          <p>
          In this project, we focus on the employment in Victoria. 
          And some analysis and visualization are conducted to explore the relationship 
          among data from Twitter, SUDO and Mastodon. 
          Firstly, we save Twitter data into CouchDB and process them to 
          merge the shapefile data from ABS. After that, some map graphs are plotted to 
          investigate how many tweets mention words related to employment and are these 
          clustered in certain areas. Secondly, we crawl some data about income from SUDO. 
          And a line graph is plotted to see the trend. Finally, we develop a word cloud 
          graph according to the data from Mastodon. Users can input their interested words 
          to discover the popularity of this word. All the graphs are displayed in the frontend.
          </p>
        </div>
      </div>
     );
}
 
export default Home;