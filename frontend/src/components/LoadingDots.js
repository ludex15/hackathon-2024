import React, { useState, useEffect } from 'react';

const LoadingDots = () => {
  const [dots, setDots] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prevDots) => (prevDots + 1) % 4);
    }, 500);

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  return <span className='answer'>{'.'.repeat(dots)}</span>;
};

export default LoadingDots;
