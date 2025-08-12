import React from "react";
import { Navbar, Nav, NavDropdown, Container } from "react-bootstrap";
import 'bootstrap/dist/css/bootstrap.min.css';
import { NavLink,Link} from "react-router-dom";

const Header = () => {
    return(
        <>
        <Navbar expand="lg" className="bg-body-tertiary">
        <Container>
        <Navbar.Brand href="#home">React-Bootstrap</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <NavLink className="home" to="/">Home</NavLink>
            <NavDropdown className="jobs" title="Jobs" id="basic-nav-dropdown">
              <NavDropdown.Item className="relatedjobs" as={Link} to="/relatedjob">Related Jobs</NavDropdown.Item>
              <NavDropdown.Item className="alljobs" as={Link} to="/alljobs">
                 All Jobs
              </NavDropdown.Item>
            </NavDropdown>
            <NavLink className="appliedjobs" to="/appliedjobs">Applied Jobs</NavLink>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
        </>
    )    
}
export default Header;