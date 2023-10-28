import './App.css';
import Header from './components/Header';
import Feedback from './components/Feedback'
import { BrowserRouter, Routes, Route } from "react-router-dom";



import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';

function App() {
  return (
    <BrowserRouter>
      <Header />
      <br></br>
      <Routes>
      <Route path="/" element={<Home />} />      
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/feedback" element={<Feedback />} />

      <Route path="/about" element={<Feedback />} />
      <Route path="/contact" element={<Feedback />} />

        {/* <Route path="/" element={<Home />} /> */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
