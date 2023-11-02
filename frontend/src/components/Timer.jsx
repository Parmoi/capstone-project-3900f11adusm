import React, { useState, useEffect } from 'react';

const Timer = ({ startDate, endDate }) => {
  const calculateTimeLeft = () => {
    const now = new Date();
    const end = new Date(endDate);
    const difference = end - now;

    let timeLeft = {};

    if (difference > 0) {
      timeLeft = {
        days: Math.floor(difference / (1000 * 60 * 60 * 24)),
        hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
        minutes: Math.floor((difference / 1000 / 60) % 60),
        seconds: Math.floor((difference / 1000) % 60),
      };
    }

    return timeLeft;
  };

  const [timeLeft, setTimeLeft] = useState(calculateTimeLeft());

  useEffect(() => {
    const timer = setTimeout(() => {
      setTimeLeft(calculateTimeLeft());
    }, 1000);

    return () => clearTimeout(timer);
  });

  const timerComponents = [];

  Object.keys(timeLeft).forEach(interval => {
    timerComponents.push(
      <span>
        {timeLeft[interval]} {interval}{" "}
      </span>
    );
  });

  const timer_style = {
    textAlign: "center",
    padding: "20px",
    marginLeft: "20px"
  }

  return (
    <div>
      <h2 style={{fontSize: "1.5rem", color: "#34495e"}}>Start Date: {startDate}</h2>
      <h2 style={{fontSize: "1.5rem", color: "#34495e"}}>End Date: {endDate}</h2>
      <h1 style={{fontSize: "3rem", color: "#2c3e50"}}>{timerComponents.length ? timerComponents : <span>Time's up!</span>}</h1>
    </div>
  );
};

export default Timer;
