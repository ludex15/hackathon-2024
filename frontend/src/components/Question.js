import React, { useState } from 'react';

const Question = ({ onNewQuestion, onResponse }) => {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const question = inputValue.trim();
    if (!question) return;

    onNewQuestion(question);
    setInputValue(''); 

    try {
      const response = await fetch('http://127.0.0.1:5000/api/prompt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ datasetName: 'dataset.csv', prompt: question }),
      });

      const data = await response.json();

      onResponse(question, data);
    } catch (error) {
      console.error('Error fetching data: ', error);
    }
  };

  return (
    <div className="prompt">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Enter your question"
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default Question;
