import React from 'react'
import { Container } from 'react-bootstrap'

const Home:React.FC = () => {
  return (
    <>
      <Container>
        <div className='home-container'>
          <h1 className='text-center mt-5 metamorphous-font'>Welcome to the Initiative Tracker!</h1>
          <p className='text-center mt-3'>This app is designed to help DMs and players keep track of initiative during combat encounters in Dungeons & Dragons 5th Edition. You can create and manage your character database, view encounter characters, and track initiative order with ease.</p>
          <h2 className='text-center mt-5 metamorphous-font'>Components</h2>
          <ul className='list-unstyled text-center mt-3'>
              <li><strong>View Character DB:</strong> View and add characters to your encounter.</li>
              <li><strong>View Encounter Characters:</strong> Remove characters from your encounter and Roll Initiative.</li>
              <li><strong>Find Characters Chat:</strong> Use AI to find a character.</li>
              <li><strong>Make Characters Chat:</strong> Use AI to make a character.</li>
          </ul>
        </div>
      </Container>
    </>
    
  )
}

export default Home