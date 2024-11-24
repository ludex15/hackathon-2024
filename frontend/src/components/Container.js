import React, { useState } from 'react';
import Question from './Question';
import Answer from './Answer';
import MenAgeChart from './GoogleChart';
import GoogleChart from './GoogleChart';

const Container = () => {
  const [questionAndAnswers, setQuestionAndAnswers] = useState([]);

  const menAgeData = [
    ["Age Range", "Number of Men"],
    ["18-24", 120],
    ["25-34", 123],
    ["35-44", 150],
    ["45-54", 100],
    ["55-64", 80],
    ["65+", 50],
  ];

  const handleResponse = (question, data) => {
    setQuestionAndAnswers((prevState) => [
      ...prevState,
      { question, answer: data.message },
    ]);
  };

  return (
    <div className="container">
      <div className="list qa">
        {questionAndAnswers.map((qa, index) => (
          <div key={index} className="qa-item">
            <p className='question'>
              <strong>Question:</strong> {qa.question}
            </p>
            <p className='answer'>
              <strong>Answer:</strong> {qa.answer}
            </p>
          </div>
        ))}
      </div>
      <div className="list visuals">
      <GoogleChart
      chartType="BarChart"
      data={menAgeData}
      title="Distribution of Men's Age Groups"
      hAxisTitle="Number of Men"
      vAxisTitle="Age Range"
      colors={["#34A853"]} // Google green
      />
      </div>

      <Question onResponse={handleResponse} />
    </div>
  );
};

export default Container;
