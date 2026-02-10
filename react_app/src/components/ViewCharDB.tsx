import axios from 'axios'
import React, { use, useEffect } from 'react'


const ViewCharDB = () => {
  const [characters, setCharacters] = React.useState([])

  const fetchCharacters = async () => {
    //http://127.0.0.1:8000/combatants/
    const request = await axios.get('http://127.0.0.1:8000/combatants/')
    setCharacters(request.data)
    console.log(request.data)
  }



    
  useEffect(() => {
    fetchCharacters()


  }, [])


  return (
    <div>ViewCharDB</div>
  )
}

export default ViewCharDB