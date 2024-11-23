import React from 'react';

const Response = ({ data }) => {
  if (!data) {
    return <div className="response">No response yet.</div>;
  }

  return (
    <div className="response">
      <pre>{JSON.stringify(data.message)}</pre>
    </div>
  );
};

export default Response;
