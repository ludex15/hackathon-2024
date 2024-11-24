import React, { useState, useEffect } from 'react';
import GoogleChart from './GoogleChart';
import ReactMarkdown from 'react-markdown';

const supportedChartTypes = [
  { label: "Bar Chart", value: "BarChart" },
  { label: "Line Chart", value: "LineChart" },
  { label: "Pie Chart", value: "PieChart" },
  { label: "Column Chart", value: "ColumnChart" },
  { label: "Area Chart", value: "AreaChart" },
];

const Answer = ({ answers, previousPrompt }) => {
  const [chartType, setChartType] = useState("BarChart");
  const [chartData, setChartData] = useState([]);

  const handleChartTypeChange = (newChartType) => {
    setChartType(newChartType);
  };

  useEffect(() => {
    answers.forEach(answer => {
      if (answer.type === 'complex') {
        const data = [
          ['', ''],
          ...Object.entries(answer.data)
        ];
        setChartData(data);
      }
    });
  }, [answers]);

  return (
    <div>
      {previousPrompt && (
        <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#f0f0f0', borderRadius: '8px' }}>
          <strong>Previous Prompt:</strong> <ReactMarkdown>{previousPrompt}</ReactMarkdown>
        </div>
      )}

      {answers.map((answer, index) => {
        if (answer.type === 'complex') {
          return (
            <div key={index} style={{ width: '100%' }}>
              <select
                onChange={(e) => handleChartTypeChange(e.target.value)}
                value={chartType}
                style={{
                  marginBottom: '20px',
                  padding: '5px',
                  fontSize: '16px',
                  display: 'block',
                }}
              >
                {supportedChartTypes.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>

              <GoogleChart
                chartType={chartType}
                data={chartData}
                width="100%"
                height="30vh"
                options={{ legend: { position: 'none' } }}
              />
            </div>
          );
        } else {
          const answerText = typeof answer.data === 'string' ? answer.data : JSON.stringify(answer.data);
          
          return (
            <div key={index}>
              <strong>Answer:</strong>
              <div>
                <ReactMarkdown>{answerText}</ReactMarkdown>
              </div>
            </div>
          );
        }
      })}
    </div>
  );
};

export default Answer;
