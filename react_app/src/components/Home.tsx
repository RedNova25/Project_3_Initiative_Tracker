import React from 'react'

const Home:React.FC = () => {
  return (
    <>
        <h1 className='text-center mt-5'>Welcome to the Initiative Tracker!</h1>
        <p className='text-center mt-3'>This app is designed to help DMs and players keep track of initiative during combat encounters in Dungeons & Dragons 5th Edition. You can create and manage your character database, view encounter characters, and track initiative order with ease.</p>
        <h2 className='text-center mt-5'>Components</h2>
        <ul className='list-unstyled text-center mt-3'>
            <li><strong>Character Database:</strong> View and manage your characters, including their stats, abilities, and other relevant information.</li>
            <li><strong>Encounter Characters:</strong> Add characters to the encounter.</li>
            <li><strong>Initiative View:</strong> Roll for initiative for all characters in the encounter.</li>
        </ul>
    </>
    
  )
}

export default Home