import './App.css';
import Header from './components/Header';
import Feedback from './components/Feedback';
import {useState} from 'react'
import { BrowserRouter, Routes, Route } from "react-router-dom";



import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Admin from './pages/Admin';

import About from './components/About';
import Contact from './components/Contact';


function App() {


  return (
    <BrowserRouter>
    <Header/>
      <br></br>
      <Routes>
      <Route path="/admin" element={<Admin />}/> 
      <Route path="/" element={<Home />} />      
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/feedback" element={<Feedback />} />

      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />

        {/* <Route path="/" element={<Home />} /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
