import React from "react"
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Images = [
    { link: "https://i.postimg.cc/SxMqVKRw/IMG-2375.jpg", campaign_name: "1" },
    { link: "https://i.postimg.cc/HL0mDPQz/IMG-2369.jpg", campaign_name: "2" },
    { link: "https://i.postimg.cc/xC020y52/IMG-2442.jpg", campaign_name: "3" },
  ];

const HomePage = () => {
    const [currentIndex, setCurrent] = useState(0);
    const slideStyle = {
        width: '100%',
        height: "100%",
        borderRadius: "10px",
        backgroundPosition: "center",
        backgroundSize: "cover",
        backgroundImage: `url(${Images[currentIndex].link})`,
        display: "flex"
    };

    const containerStyle = {
        height: "100%",
        position: "relative"
    };

    const lArrow = {
        position: 'absolute',
        top: '50%',
        transform: 'translate(0, -50%)',
        left: '10px',
        fontSize: '45px',
        color: '#fff',
        zIndex: 1,
        cursor: 'pointer'
    }

    const rArrow = {
        position: 'absolute',
        top: '50%',
        transform: 'translate(0, -50%)',
        right: '10px',
        fontSize: '45px',
        color: '#fff',
        zIndex: 1,
        cursor: 'pointer'
    }

    const outStyle ={
        width: '650px',
        height: '400px',
        margin: "0 auto",
        color: "#216869",
        marginTop: "20px",
    }

    const goPrevious = () => {
        const isFirst = currentIndex ===0
        const newIndex = isFirst ? Images.length-1 : currentIndex -1
        setCurrent(newIndex);
    }

    const goNext = () => {
        const isLast = currentIndex === Images.length - 1
        const newIndex = isLast ? 0 : currentIndex +1
        setCurrent(newIndex);
    }

    const navigate = useNavigate();
    const goCampaign = () => {

        navigate("/campaign", {state: {img: Images[currentIndex].link}});
    }

    useEffect(() => {
        // This function will switch to the next image every 2 seconds
        const autoSlide = setInterval(() => {
            goNext(); // Go to the next image
        }, 5000); // Set the interval to 2 seconds (2000 milliseconds)
        return () => clearInterval(autoSlide);
    }, [currentIndex]);


    return (
        <div style={outStyle}>
            <div style={containerStyle}>
                <div style={lArrow} onClick={goPrevious}>❮</div>
                <div style={rArrow} onClick={goNext}>❯</div>
                <div style={slideStyle} onClick={goCampaign}></div>
            </div>
        </div> 
    );
};

export default HomePage;
