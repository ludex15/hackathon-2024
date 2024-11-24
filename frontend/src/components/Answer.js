import React from 'react';
import GoogleChart from './GoogleChart';

const Answer = ({ type, data }) => {
  if (type === 'complex') {
    return (
      <p className='answer'>
        <strong>Answer:</strong>
        {/* add chart type props */}
        {/* <GoogleChart data={data} /> */}
        <GoogleChart
          chartType="BarChart"
          data={data}
          title="Distribution of Men's Age Groups"
          hAxisTitle="Number of Men"
          vAxisTitle="Age Range"
          colors={["#34A853"]} // Google green
          />
      </p>
    );
  }

  if (type === 'text') {
    return (
      <p className='answer'>
        <strong>Answer:</strong> {data}
      </p>
    );
  }
};

export default Answer;
