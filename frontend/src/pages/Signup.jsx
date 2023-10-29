import React from 'react'
import GoogleButton from 'react-google-button';
import Header from '../components/Header';


function Signup() {
  return (
    <div>
    <Header/>
        <br></br>

    <main className="form-signin w-100 m-auto mt-5">
  <form>
    <h1 className="h3 mb-3 fw-normal">Please Sign Up</h1>

    <div className="form-floating mt-4">
      <input type="text" className="form-control" id="floatingInput" placeholder="name@example.com" required/>
      <label for="floatingInput">Username</label>
    </div>                                                                                                                                                    

    <div className="form-floating mt-4">
      <input type="email" className="form-control" id="floatingInput" placeholder="name@example.com" required/>
      <label for="floatingInput">Email address</label>
    </div>
    <div className="form-floating mt-4">
      <input type="password" className="form-control" id="floatingPassword" placeholder="Password" required/>
      <label for="floatingPassword">Password</label>
    </div>

    {/* <div className="form-check text-start my-3">
      <input className="form-check-input" type="checkbox" value="remember-me" id="flexCheckDefault"/>
      <label className="form-check-label" for="flexCheckDefault">
        Remember me
      </label>
    </div> */}
    <button className="btn btn-dark w-100 py-2 mt-5" type="submit">Sign up</button>
    <GoogleButton type="dark" className='mt-3 w-100' style={{"border-radius" : "3px"}}/>

  </form>
</main>
</div>
  )
}

export default Signup