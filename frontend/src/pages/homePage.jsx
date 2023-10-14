// src/LandingPage.js
import React from 'react';
import home_page_icon from '../images/home_page_icon.png'

function HomePage() {
  
  //style of image
  const ImageAdjust = {
    display: 'flex',
    justifyContent: 'center',
    alignItems:'center',
    height:'100vh'

  }

  return (
    <div style={ImageAdjust}>
      <img src= {home_page_icon} alt="Icon of CollectiblesCorner" display='flex' />
      <h1>Welcome to CollectiblesCorner!</h1>
    </div>
  );
}

export default HomePage;