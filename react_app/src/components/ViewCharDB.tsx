import axios from 'axios'
import {useState , useEffect } from 'react'
import { Container, Table } from 'react-bootstrap'


const ViewCharDB = () => {
  const [characters, setCharacters] = useState([])

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
    <Container>
      <Table striped>

        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Dexterity Init Mod +</th>
            <th>Other Init Mod +</th>
            <th>Roll =</th>
            <th>Total Initiative</th>
          </tr>
        </thead>

        <tbody>
          {characters.map((char, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{char.name}</td>
              <td>{char.dex_init_mod}</td>
              <td>{char.other_init_mod}</td>
              <td>{char.init_roll}</td>
              <td>{char.initiative}</td>
            </tr>
          ))}
        </tbody>

      </Table>
    </Container>
  )
}

export default ViewCharDB