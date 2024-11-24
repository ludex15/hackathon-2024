import React, { useState, useEffect, useRef } from 'react';
import Question from './Question';
import Answer from './Answer';
import LoadingDots from './LoadingDots';
import GoogleChart from './GoogleChart';

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
    }, 40000); 
  };

  const handleAnswerResponse = (question, data) => {
    setAnswers((prevAnswers) => ({
      ...prevAnswers,
      [question]: data.content.map(item => ({
        data: item.data,
        type: item.type,
      })),
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
            <div className="question">
              <strong>Question:</strong> <p>{question}</p>
            </div>
            {answers[question] ? (
              <div className="answer">
                <Answer answers={answers[question]} />
              </div>
            ) : (
              <div className="answer"><LoadingDots/></div>
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
