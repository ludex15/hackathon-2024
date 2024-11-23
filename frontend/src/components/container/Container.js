import React, { useState } from 'react';
import Prompt from '../prompt/Prompt';
import Response from '../response/Response';

const Container = () => {
  const [responseData, setResponseData] = useState(null);

  // Function to update the response data (called by the Prompt component)
  const handleResponse = (data) => {
    setResponseData(data);
  };

  return (
    <div className="container">      
      {/* The Response component will display the API response */}
      <Response data={responseData} />
      {/* The Prompt component will send its response to the Container */}
      <Prompt onResponse={handleResponse} />     
    </div>
  );
};

export default Container;
