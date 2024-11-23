import React from 'react';

const Answer = ({ data }) => {
  return (
    <div>
      <pre>{JSON.stringify(data.message)}</pre>
    </div>
  );
};

export default Answer;
