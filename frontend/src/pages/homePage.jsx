import React from "react"
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";



const  Campaigns = {
    past: [
        { link: "https://i.postimg.cc/SxMqVKRw/IMG-2375.jpg", campaign_name: "campaign1", start_date: "Fri, 01 Jan 1999 00:00:00 GMT", end_date: "Fri, 24 Nov 2023 00:00:00 GMT", des: "babababbabab"},
        { link: "https://i.postimg.cc/HL0mDPQz/IMG-2369.jpg", campaign_name: "campaign2", start_date: "Fri, 01 Jan 1999 00:00:00 GMT", end_date: "Fri, 24 Nov 2023 00:00:00 GMT", des: "babababbabab"}
      
    ],
    future: [
        { link: "https://i.postimg.cc/HL0mDPQz/IMG-2369.jpg", campaign_name: "campaign2", start_date: "Fri, 01 Jan 1999 00:00:00 GMT", end_date: "Fri, 24 Nov 2023 00:00:00 GMT", des: "babababbabab"},
        { link: "https://i.postimg.cc/HL0mDPQz/IMG-2369.jpg", campaign_name: "campaign3", start_date: "Fri, 01 Jan 1999 00:00:00 GMT", end_date: "Fri, 24 Nov 2023 00:00:00 GMT", des: "babababbabab"}
    ],
    current: [
        { link: "https://i.postimg.cc/HL0mDPQz/IMG-2375.jpg", campaign_name: "campaign2", start_date: "Fri, 01 Jan 1999 00:00:00 GMT", end_date: "Fri, 24 Nov 2023 00:00:00 GMT", des: "babababbabab"},
        { link: "https://i.postimg.cc/HL0mDPQz/IMG-2369.jpg", campaign_name: "campaign4", start_date: "Fri, 01 Jan 1999 00:00:00 GMT", end_date: "Fri, 24 Nov 2023 00:00:00 GMT", des: "babababbabab"},
        { link: "https://i.postimg.cc/xC020y52/IMG-2442.jpg", campaign_name: "campaign3", start_date: "Fri, 01 Jan 1999 00:00:00 GMT", end_date: "Fri, 24 Nov 2023 00:00:00 GMT", des: "babababbabab"},
    ]
  };

  const ItemDisplay = ({ link, start_date, end_date, des, campaign_name}) => (
    <div style={{ display: 'flex', alignItems: 'center', borderBottom: '1px solid #ccc', padding: '10px 0' }}>
      <img src={link} alt="Item" style={{ width: '300px', height: '200px', marginRight: '20px' }} />
      <div>
        <p style={{ fontSize: '30px' }}> <strong>{campaign_name}</strong></p>
        <p><strong>From </strong>{start_date.slice(0,16)} <strong>To</strong> {end_date.slice(0,16)}</p>
        <p>{des}</p>
      </div>
      
    </div>
  );


const HomePage = () => {
    const [currentIndex, setCurrent] = useState(0);
    const [selection, setSelection] = useState('current');
    const slideStyle = {
        width: '100%',
        height: "100%",
        borderRadius: "10px",
        backgroundPosition: "center",
        backgroundSize: "cover",
        backgroundImage: `url(${Campaigns.current[currentIndex].link})`,
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
        const newIndex = isFirst ? Campaigns.current.length-1 : currentIndex -1
        setCurrent(newIndex);
    }

    const goNext = () => {
        const isLast = currentIndex === Campaigns.current.length - 1
        const newIndex = isLast ? 0 : currentIndex +1
        setCurrent(newIndex);
    }

    const navigate = useNavigate();
    const goCampaign = () => {

        navigate("/campaign", {state: {img: Campaigns.current[currentIndex].link, 
            campaign_name: Campaigns.current[currentIndex].campaign_name, 
            start_date:Campaigns.current[currentIndex].start_date, 
            end_date: Campaigns.current[currentIndex].end_date}});
    }
    // 
    useEffect(() => {
        // This function will switch to the next image every 2 seconds
        const autoSlide = setInterval(() => {
            goNext(); // Go to the next image
        }, 5000); // Set the interval to 2 seconds (2000 milliseconds)
        return () => clearInterval(autoSlide);
    }, [currentIndex]);


    return (
       <>
        <div style={outStyle}>
            <div style={containerStyle}>
                <div style={lArrow} onClick={goPrevious}>❮</div>
                <div style={rArrow} onClick={goNext}>❯</div>
                <div style={slideStyle} onClick={goCampaign}></div>
            </div>
        </div >
      <div style={{ backgroundColor: 'white', padding: '20px', width: '1000px', height: '500px', minWidth: '500px', minHeight: '300px',overflow: 'auto', marginBottom: '20px', borderRadius: '4px', borderWidth: "20px"}}>
        <div style={{ marginBottom: '20px' }}>
            <button
            style={{ marginRight: '20px', background: selection === 'current' ? "#216869" : "#CCC", variant:"contained",width: "75px", height: "35px", borderRadius: "10px", border: "none", color: selection === 'current' ? "#F0F4EF" : "#000000"}}
            onClick={() => setSelection('current')}
          >
            Current
          </button>
          <button
            style={{ marginRight: '20px', background: selection === 'past' ? "#216869" : "#CCC", variant:"contained",width: "75px", height: "35px", borderRadius: "10px", border: "none", color: selection === 'past' ? "#F0F4EF" : "#000000"}}
            onClick={() => setSelection('past')}
          >
            Past
          </button>
          <button
            style={{ background: selection === 'future' ? "#216869" : "#CCC", variant:"contained",width: "75px", height: "35px", borderRadius: "10px", border: "none", color: selection === 'future' ? "#F0F4EF" : "#000000"}}
            onClick={() => setSelection('future')}
          >
            Future
          </button>
        </div>

        <div>
          {Campaigns[selection].map((item) => (
            <ItemDisplay key={item.id} campaign_name={item.campaign_name} link={item.link} des={item.des} start_date={item.start_date} end_date={item.end_date}/>
          ))}
        </div>
      </div>
       </>
    );
};

export default HomePage;
