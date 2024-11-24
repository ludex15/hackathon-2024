// import React, { useState } from "react";
// import { Chart } from "react-google-charts";

// const supportedChartTypes = [
//   { label: "Bar Chart", value: "BarChart" },
//   { label: "Line Chart", value: "LineChart" },
//   { label: "Pie Chart", value: "PieChart" },
//   { label: "Column Chart", value: "ColumnChart" },
//   { label: "Area Chart", value: "AreaChart" },
// ];

// const ChartDropdown = ({ data, options }) => {
//   const [selectedChartType, setSelectedChartType] = useState("BarChart");

//   const handleChartTypeChange = (e) => {
//     setSelectedChartType(e.target.value);
//   };

//   return (
//     <div className="dropdown">
//         <select
//           id="chart-type"
//           value={selectedChartType}
//           onChange={handleChartTypeChange}
//           style={{ padding: "5px", fontSize: "16px" }}
//         >
//           {supportedChartTypes.map((type) => (
//               <option className="dropdown-item"key={type.value} value={type.value}>
//               {type.label}
//             </option>
//           ))}
//         </select>
//     </div>
//   );
// };

// export default ChartDropdown;
