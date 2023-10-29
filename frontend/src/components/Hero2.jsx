import React from 'react'
import { useState } from 'react'

function Hero2() {


    const [speak, setSpeak] = useState(false)
    const [language, setLanguage] = useState('English')

    const handleClickSpeak = (event) => { 
        setSpeak(true)
     }

     const handleLanguageChange = (event) => {
        const selectedLanguage = event.target.value;
        setLanguage(selectedLanguage); // Update the language state when the dropdown value changes
      };

  return (
    <div class="container container-input my-5">

    {speak ? <div class="p-5 text-center bg-body-tertiary rounded-3">
    <form>
    <div className="form-floating mt-4">
    <h3>Select Language:</h3>
      <select className="form-select" value={language} onChange={handleLanguageChange}>
        <option value="English">English</option>
        <option value="Hindi">Hindi</option>
      </select></div>
      
      </form>
  </div>: <div class="p-5 text-center bg-body-tertiary rounded-3">
    <h1 class="text-body-emphasis my-4">Write Your Query</h1>
    <form>
    <div className="form-floating mt-4">
    <input type="text" className="form-control" id="prompt" placeholder="name@example.com" required/>
      <label for="prompt">Type here</label></div>
      <button type='submit' className='btn btn-dark lg px-4 mx-4 my-4'> Submit</button>
      </form>
      <p class="lead">
      Want to speak instead? <button  className='btn' onClick={handleClickSpeak}>Click me.</button>
    </p>
  </div>}

</div>

  )
}

export default Hero2