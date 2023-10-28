import React, { useState } from 'react'
import { Link } from "react-router-dom";

function Header() {

    const [logged, setLogged] = useState(false)

  return (
    <div>
        <header className="p-3 bg-dark text-white">
    <div className="container">
      <div className="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">

        <Link to="/" className=" navtit d-flex align-items-center mb-2 mb-lg-0 text-white text-decoration-none fw-900">
            LawYantra
          </Link>

        <ul className="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          
        </ul>
        {/* nav-link px-2 text-white */}
        {/* <form className="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3">
          <input type="search" className="form-control form-control-dark" placeholder="Search..." aria-label="Search" />
        </form> */}
        <Link to="/about" className="nav-link px-2 text-white">About</Link>
        <Link to="/contact" className="nav-link px-2 text-white">Contact</Link>


        {logged? <Link to="./feedback" className='nav-link px-2 text-white '>Feedback</Link>  : <div className="text-end">
          <Link to="/login" type="button" className="btn btn-outline-light me-2">Login</Link>
          <Link to="/signup" type="button" className="btn btn-outline-info">Sign-up</Link>
        </div>
}
      </div>
    </div>
  </header>
    </div>
  )
}

export default Header