import React from 'react';
import './App.css';
import Welcome from './components/Candidate/candidatewelcome/Welcom';
import Headers from './components/Candidate/candidateheader/Header';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';  
import AllJobs from './components/Candidate/alljobs/AllJobs';
import AppliedJobs from './components/Candidate/appliedjobs/AppliedJobs';
import Form from './components/Candidate/form/Form';

//Home page
import Home from './components/Home/Home/HomePage/Home';
import Aboutus from './components/Home/Home/About/AboutUs';
import Careers from './components/Home/Home/Careers/Careers';
import Product from './components/Home/Home/Product/Product';
import ContactUs from './components/Home/Home/Contact/contact';
import LandingPage from './components/Home/Home/Login/LandingPage';
import { Login } from '@mui/icons-material';
import LoginPage from './components/Home/Home/Login/LoginPage';
import ForgotPassword from './components/Home/Home/Login/ForgotPassword';
import ClientSignup from './components/Home/Home/Login/Client/ClientSignup';
// import ClientHome from './components/Client/Welcom/ClientHome';
// import Login from './components/Home/Home/Login';
// import Signup from './components/Home/Signup/Signup';

function App() {
  return (
    <>
  
    <div className="App">
      <Router>
        
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<Aboutus />} />
          <Route path="/product" element={<Product />} />
          <Route path="/careers" element={<Careers/>} />
          <Route path="/contact" element={<ContactUs/>} />
          <Route path="/landingpage" element={<LandingPage/>} />
          <Route path="/login/:userType" element={<LoginPage />} />
          <Route path="/form" element={<Form />} />
          <Route path="/forgotpassword/:userType" element={<ForgotPassword />} />
          <Route path="/client-signup" element={<ClientSignup />} />
          {/* <Route path="/client-dashboard" element={<ClientHome />} />  */}
          {/* <Route path="/login" element={<Login/>} /> */}
          {/* <Route path="/signup" element={<Signup />} />  */}
          {/* <Route path="/home" element={<Welcome />} /> */}
          {/* <Route path="/alljobs" element={<AllJobs />} /> */}
          {/* <Route path="/relatedjob" element={<AllJobs />} /> */}
          {/* <Route path="/appliedjobs" element={<AppliedJobs />} /> */}
        </Routes>
      </Router>
    </div>
    </>
    
  );
}

export default App;
