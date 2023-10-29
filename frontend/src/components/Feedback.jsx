import React from 'react';
import Header from './Header';
import { useState } from 'react';

function Feedback() {

  const [rating, setRating] = useState(0);
  const [feedback, setFeedback] = useState('');

  const handleRatingChange = (event) => {
    setRating(parseInt(event.target.value));
  };

  const handleFeedbackChange = (event) => {
    setFeedback(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // You can handle the submission of feedback data here, e.g., send it to a server or store it locally.
    console.log('Rating: ', rating);
    console.log('Feedback: ', feedback);
    // Reset the form if needed
    setRating(0);
    setFeedback('');
  };


  return (
    <div><Header />
    <div className='container'>
      <h1 className='my-4'>Feedback Form</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className='mb-2'>Rating:</label>
          <select className="form-control mb-4" value={rating} onChange={handleRatingChange}>
            <option value={0}>Select a rating</option>
            <option value={1}>Poor</option>
            <option value={2}>Fair</option>
            <option value={3}>Good</option>
            <option value={4}>Very Good</option>
            <option value={5}>Excellent</option>
          </select>
        </div>
        <div className="form-group mb-4">
          <label>Feedback:</label>
          <textarea
            className="form-control"
            rows="5"
            value={feedback}
            onChange={handleFeedbackChange}
          ></textarea>
        </div>
        <button type="submit" className="btn btn-dark">Submit Feedback</button>
      </form>
    </div>
    </div>
  );
}

export default Feedback;
