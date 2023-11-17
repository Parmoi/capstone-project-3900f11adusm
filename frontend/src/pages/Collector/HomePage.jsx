import React from "react"
import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { apiCall } from "../../App";

// Displays current, past and future campaigns, and gives user access to campaign pages 
const HomePage = () => {
    const [currentIndex, setCurrent] = useState(0);
    const [selection, setSelection] = useState('current');
    const location = useLocation();
    // some dummy data for initialization
    const [data, setData] = React.useState([{ image: "https://i.postimg.cc/sX59yLfP/IMG-2438.jpg", campaign_name: "NO DATA HAS BEEN PROVIDED", start_date: "Fri, 01 Jan 1999 00:00:00 GMT", end_date: "Fri, 24 Mar 2023 00:00:00 GMT", des: "babababbabab", id: 10000},
      { image: "https://i.postimg.cc/wT4JKzc8/IMG-2304.jpg", campaign_name: "NO DATA HAS BEEN PROVIDED", start_date: "Fri, 01 Jan 1999 00:00:00 GMT", end_date: "Fri, 23 Mar 2023 00:00:00 GMT", des: "babababbabab", id: 200000},
      { image: "https://i.postimg.cc/NfnyJ4BQ/IMG-2441.jpg", campaign_name: "NO DATA HAS BEEN PROVIDED", start_date: "Fri, 24 Nov 2023 00:00:00 GMT", end_date: "Fri, 27 Nov 2023 00:00:00 GMT", des: "babababbabab", id: 30000},
      { image: "https://i.postimg.cc/2jc3ywqn/IMG-2436.jpg", campaign_name: "NO DATA HAS BEEN PROVIDED", start_date: "Fri, 24 Nov 2023 00:00:00 GMT", end_date: "Fri, 27 Nov 2023 00:00:00 GMT", des: "babababbabab", id: 40000},
      { image: "https://i.postimg.cc/SxMqVKRw/IMG-2375.jpg", campaign_name: "NO DATA HAS BEEN PROVIDED", start_date: "Fri, 01 Jan 1999 00:00:00 GMT", end_date: "Fri, 24 Nov 2023 00:00:00 GMT", des: "babababbabab", id: 50000},
      { image: "https://i.postimg.cc/HL0mDPQz/IMG-2369.jpg", campaign_name: "NO DATA HAS BEEN PROVIDED", start_date: "Fri, 01 Jan 1999 00:00:00 GMT", end_date: "Fri, 25 Nov 2023 00:00:00 GMT", des: "babababbabab", id: 60000},
      { image: "https://i.postimg.cc/xC020y52/IMG-2442.jpg", campaign_name: "NO DATA HAS BEEN PROVIDED", start_date: "Fri, 01 Jan 1999 00:00:00 GMT", end_date: "Fri, 26 Nov 2023 00:00:00 GMT", des: "babababbabab", id: 70000},
    ]);

  const fetchData = () => {
    // call api with data
    const options = {
      method: 'GET',
      route: "/campaign/get_campaigns",
    };

    apiCall((d) => {
      if (d["campaigns"].length != 0) {
        setData(d["campaigns"]);
      }
    }, options);
  }

  React.useEffect(() => {
    fetchData();
  }, []);

  // divide the campaigns
  const now = new Date();
  const future = [];
  const past = [];
  const current = [];

  data.map((campaign) => {
    const startDate = new Date(campaign.start_date);
    const endDate = new Date(campaign.end_date);
    if (startDate > now) {
      future.push(campaign)
    } else if ( endDate < now) {
      past.push(campaign)
    } else {
      current.push(campaign)
    }
  })

  const Campaigns = {
    past: past,
    current: current,
    future: future,
  } 
    const slideStyle = {
        width: '100%',
        height: "100%",
        borderRadius: "10px",
        backgroundPosition: "center",
        backgroundSize: "cover",
        backgroundImage: `url(${Campaigns.current[currentIndex].image})`,
        display: "flex",
        cursor: 'pointer'
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

    // for photoslide arrow function
    const goPrevious = () => {
        const isFirst = currentIndex ===0
        const newIndex = isFirst ? Campaigns.current.length-1 : currentIndex -1
        setCurrent(newIndex);
    }
    // for photoslide arrow function
    const goNext = () => {
        const isLast = currentIndex === Campaigns.current.length - 1
        const newIndex = isLast ? 0 : currentIndex +1
        setCurrent(newIndex);
    }

    const navigate = useNavigate();
    // use goCampaign for photoslider, if click photo, jump to the campaign
    const goCampaign = () => {

        navigate("/campaign", {state: {img: Campaigns.current[currentIndex].image, 
            name: Campaigns.current[currentIndex].name, 
            start_date:Campaigns.current[currentIndex].start_date, 
            end_date: Campaigns.current[currentIndex].end_date, 
            id: Campaigns.current[currentIndex].id}});
            
    }
    // display the staff for the past, current, future campaign
    const ItemDisplay = ({ image, start_date, end_date, des, campaign_name, id}) => {
      const navigate = useNavigate();
      const [isHovering, setIsHovering] = useState(false);
      const handleClick = () => {
          // Navigate to the campaign page or perform any other action
          navigate("/campaign", {
              state: {
                  img: image,
                  name: campaign_name,
                  start_date: start_date,
                  end_date: end_date,
                  id: id,
              }
          });
      };
      const handleMouseEnter = () => setIsHovering(true);
      const handleMouseLeave = () => setIsHovering(false);
      return (
        <div onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave} onClick={handleClick} style={{ display: 'flex', alignItems: 'center', borderBottom: '1px solid #ccc', padding: '10px 0', cursor: 'pointer', backgroundColor: isHovering ? '#ddd' : 'transparent',}}>
          <img src={image} alt="Item" style={{ width: '300px', height: '200px', marginRight: '20px' } } />
          <div>
            <p style={{ fontSize: '30px' }}> <strong>{campaign_name}</strong></p>
            <p><strong>From </strong>{start_date.slice(0,16)} <strong>To</strong> {end_date.slice(0,16)}</p>
            <p>{des}</p>
          </div>
          
        </div>
      )
      };
    
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
            style={{ marginRight: '20px', background: selection === 'current' ? "#216869" : "#CCC", variant:"contained",width: "75px", height: "35px", borderRadius: "10px", border: "none", color: selection === 'current' ? "#F0F4EF" : "#000000", cursor: 'pointer'}}
            onClick={() => setSelection('current')}
          >
            Current
          </button>
          <button
            style={{ marginRight: '20px', background: selection === 'past' ? "#216869" : "#CCC", variant:"contained",width: "75px", height: "35px", borderRadius: "10px", border: "none", color: selection === 'past' ? "#F0F4EF" : "#000000", cursor: 'pointer'}}
            onClick={() => setSelection('past')}
          >
            Past
          </button>
          <button
            style={{ background: selection === 'future' ? "#216869" : "#CCC", variant:"contained",width: "75px", height: "35px", borderRadius: "10px", border: "none", color: selection === 'future' ? "#F0F4EF" : "#000000", cursor: 'pointer'}}
            onClick={() => setSelection('future')}
          >
            Future
          </button>
        </div>

        <div>
          {Campaigns[selection].map((item, index) => (
            <ItemDisplay key={index} campaign_name={item.name} image={item.image} des={item.des} start_date={item.start_date} end_date={item.end_date} id ={item.id}/>
          ))}
        </div>
      </div>
       </>
    );
};

export default HomePage;
