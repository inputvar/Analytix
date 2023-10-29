import React from 'react'
import lawyer from "../lawyer.jpg"
import { Link } from 'react-router-dom'

export default function Hero1() {
  return (
    <div className="container col-xxl-8 px-4 py-5 pb-0">
    <div className="row flex-lg-row-reverse align-items-center g-5 py-5">
      <div className="col-10 col-sm-8 col-lg-6">
        <img src={lawyer} className="d-block mx-lg-auto img-fluid" alt="Lawyer" width="700" height="500" loading="lazy"/>
      </div>
      <div className="col-lg-6">
        <h1 className="display-5 fw-bold text-body-emphasis lh-1 mb-3">Find Your Right Attorney Now.</h1>
        <p className="lead fw-normal">Connect with the right attorney for your unique legal concerns. Our platform provides efficient and user-friendly legal support, making legal expertise accessible to everyone. <span className='fw-bold'>Submit Your Queries Now!</span> </p>
        <div className="d-grid gap-2 d-md-flex justify-content-md-start">
          <Link to="/login" type="button" className="btn btn-outline-dark btn-lg px-4 me-md-2">Login</Link>
          <Link to="/signup" type="button" className="btn btn-outline-dark btn-lg px-4">Sign up</Link>
        </div>
      </div>
    </div>
  </div>
  )
}
