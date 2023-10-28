// src/LandingPage.js
import React from 'react';
import landing_page_icon from '../images/landing_page_icon.png'

function LandingPage() {
  
  //style of image
  const ImageAdjust = {
    display: 'flex',
    justifyContent: 'center',
    alignItems:'center',
    height:'100vh'

  }

  return (
    <div style={ImageAdjust}>
      <img src= {landing_page_icon} alt="Icon of CollectiblesCorner" display='flex' />
      <h1>Welcome to CollectiblesCorner!</h1>
    </div>
  );
}

export default LandingPage;