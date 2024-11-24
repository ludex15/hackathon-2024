import React from "react";
import { Chart } from "react-google-charts";

const supportedChartTypes = [
  { label: "Bar Chart", value: "BarChart" },
  { label: "Line Chart", value: "LineChart" },
  { label: "Pie Chart", value: "PieChart" },
  { label: "Column Chart", value: "ColumnChart" },
  { label: "Area Chart", value: "AreaChart" },
];

const GoogleChart = ({
  // supported chart types
  // BarChart
  // LineChart
  // PieChart
  // ColumnChart
  // AreaChart
  chartType = "BarChart",
  data = [],
  title = "Sample Chart",
  hAxisTitle = "Horizontal Axis",
  vAxisTitle = "Vertical Axis",
  colors = ["#9ABF80"],
  width = "100%",
  height = "400px",
}) => {

  const options = {
    title,
    chartArea: { width: "60%" },
    hAxis: { title: hAxisTitle, minValue: 0 },
    vAxis: { title: vAxisTitle },
    colors,
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", marginTop: "20px" }}>
      <Chart
        chartType={chartType}
        data={data}
        options={options}
        width={width}
        height={height}
        loader={<div>Loading Chart...</div>}
      />
    </div>
  );
};

export default GoogleChart;
