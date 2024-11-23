import React from 'react';

const Response = ({ data }) => {
  if (!data) {
    return <div className="response">No response yet.</div>;
  }

  return (
    <div className="response">
      <h3>Response:</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre> {/* Format the response as needed */}
    </div>
  );
};

export default Response;
