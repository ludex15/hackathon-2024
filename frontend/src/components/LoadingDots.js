import React, { useState, useEffect } from 'react';

const LoadingDots = () => {
  const [dots, setDots] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prevDots) => (prevDots + 1) % 4); // Cycle between 0, 1, 2, 3
    }, 500); // Change dots every 500ms

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  return <span className='answer'>{'.'.repeat(dots)}Loading Answer</span>;
};

export default LoadingDots;
