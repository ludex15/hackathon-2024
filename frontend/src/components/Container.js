import React, { useState, useEffect, useRef } from 'react';
import Question from './Question';
import Answer from './Answer';
import LoadingDots from './LoadingDots';

const Container = () => {
  const [questions, setQuestions] = useState([]); // Stores all questions
  const [answers, setAnswers] = useState({});    // Maps each question to its answer
  const listRef = useRef(null);

  const handleNewQuestion = (question) => {
    setQuestions((prevQuestions) => [...prevQuestions, question]);

    setTimeout(() => {
      setAnswers((prevAnswers) => {
        if (!prevAnswers[question]) {
          return {
            ...prevAnswers,
            [question]: "We're sorry, but the server is taking too long to respond.",
          };
        }
        return prevAnswers; 
      });
    }, 30000); 
  };


  const handleAnswerResponse = (question, data) => {
    console.log(data)
    setAnswers((prevAnswers) => ({
      ...prevAnswers,
      [question]: data.message,
    }));
  };

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [questions, answers]);

  return (
    <div className="container">
      <div className="list qa" ref={listRef}>
        {questions.map((question, index) => (
          <div key={index} className="qa-item">
            <p className="question">
              <strong>Question:</strong> {question}
            </p>
            {answers[question] ? (
              <Answer type="text" data={answers[question]} />
            ) : (
              <p className="answer"><LoadingDots/></p>
            )}
          </div>
        ))}
      </div>
      <Question 
        onNewQuestion={handleNewQuestion} 
        onResponse={handleAnswerResponse} 
      />
    </div>
  );
};

export default Container;
