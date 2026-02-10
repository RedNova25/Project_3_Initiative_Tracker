import React, { useState } from 'react'
import { Container, Nav, Navbar } from 'react-bootstrap'
import logo from '../assets/logo.svg'


const NavBar:React.FC = () => {
    const [counter, setCounter] = useState(0)

  return (
    <>
    <Navbar className="bg-body-tertiary" expand="lg" data-bs-theme="dark">
        <Container>
          <Navbar.Brand href="/">
            <img
              alt=""
              src={logo}
              width="30"
              height="30"
              className="d-inline-block align-top"
            />{' '}
            Initiative Tracker
          </Navbar.Brand>
          {/* right justify the nav links */}
          <Nav className="ms-auto">
            <Nav.Link href="/viewcharacterdb">+View Character DB</Nav.Link>
            <Nav.Link href="/viewencounterchars">+View Encounter Characters</Nav.Link>
            <Nav.Link href="/initiativeview">+Initiative View</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </>
  )
}

export default NavBar