import React, { useContext } from 'react';
import { UserContext } from '../App';
import Header from '../components/Header';
import Hero1 from '../components/Hero1';
import Hero2 from '../components/Hero2';
import About from '../components/About';
import Contact from '../components/Contact';
import { useState } from 'react';

function Home() {

  // const [isLogged, setIsLogged] = useState(false)
  const { logged } = useContext(UserContext);

  return (

    <div>
        <Header logged={logged}/>
        {logged?<Hero2/> : <Hero1/>}
        <About/>
        <Contact/>
    </div>
  )
}

export default Home