import React from 'react'
import { Container, Nav, Navbar } from 'react-bootstrap'
import logo from '../assets/skull.svg'


const NavBar:React.FC = () => {

  return (
    <>
    <Navbar className="bg-body-tertiary" expand="lg" data-bs-theme="dark">
        <Container>
          <Navbar.Brand href="/" className='metamorphous-font'>
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
          <Nav className="ms-auto gap-4">
            <Nav.Link href="/">Welcome</Nav.Link>
            <Nav.Link href="/viewcharacterdb">View Character DB</Nav.Link>
            <Nav.Link href="/viewencounterchars">View Encounter Characters</Nav.Link>
            <Nav.Link href="/findcharschat">Find Characters Chat</Nav.Link>
            <Nav.Link href="/makecharschat">Make Characters Chat</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </>
  )
}

export default NavBar