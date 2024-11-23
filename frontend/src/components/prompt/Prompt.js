import React, { useState } from 'react';

const Prompt = ({ onResponse }) => {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const response = await fetch('your-api-url', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: inputValue }),
    });

    const data = await response.json();

    onResponse(data);
  };

  return (
    <div className="prompt">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Enter your query"
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default Prompt;
