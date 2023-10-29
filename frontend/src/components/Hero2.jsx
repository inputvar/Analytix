import React, { useState } from 'react';
import axios from 'axios';

function Hero2() {
  const [speak, setSpeak] = useState(false);
  const [language, setLanguage] = useState('English');
  const [prompt, setPrompt] = useState('');

  const handleClickSpeak = () => {
    // Make sure 'prompt' state is updated before sending the request
    const data = { prompt: prompt };

    axios.post('http://127.0.0.1:5000/api/prompt', data)
      .then((response) => {
        // Handle the response here
        console.log(response.data);
      })
      .catch((error) => {
        // Handle any errors here
        console.error(error);
      });

    console.log(prompt);
  }

  const handleLanguageChange = (event) => {
    const selectedLanguage = event.target.value;
    setLanguage(selectedLanguage);
  };

  return (
    <div className="container container-input my-5">
      {speak ? (
        <div className="p-5 text-center bg-body-tertiary rounded-3">
          <h3>Select Language:</h3>
          <select className="form-select" value={language} onChange={handleLanguageChange}>
            <option value="English">English</option>
            <option value="Hindi">Hindi</option>
          </select>
        </div>
      ) : (
        <div className="p-5 text-center bg-body-tertiary rounded-3">
          <h1 className="text-body-emphasis my-4">Write Your Query</h1>
          <div className="form-floating mt-4">
            <input
              type="text"
              className="form-control"
              id="prompt"
              placeholder="Type here"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              required
            />
            <label htmlFor="prompt">Type here</label>
          </div>
          <button type='button' onClick={handleClickSpeak} className='btn btn-dark lg px-4 mx-4 my-4'>Submit</button>
          <p className="lead">
            Want to speak instead? <button className='btn' onClick={() => setSpeak(true)}>Click me.</button>
          </p>
        </div>
      )}
    </div>
  );
}

export default Hero2;
