import React from "react";
import { Chart } from "react-google-charts";

const GoogleChart = ({ chartType, data }) => {
  return (
    <div style={{ 
      borderRadius: '5px',
      overflow: 'hidden',
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
