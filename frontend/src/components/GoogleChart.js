import React from "react";
import { Chart } from "react-google-charts";

const GoogleChart = ({ chartType, data }) => {
  return (
    <div style={{ 
      borderRadius: '15px',
      overflow: 'hidden',
      border: '2px solid #ccc',
      boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    }}>
      <Chart
        chartType={chartType}
        data={data}
        width="35vw"
        height="30vh"
        options={{legend: { position: 'none' }}}
      />
    </div>
  );
};

export default GoogleChart;
