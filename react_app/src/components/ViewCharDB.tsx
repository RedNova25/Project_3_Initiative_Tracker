import axios from 'axios'
import {useState , useEffect } from 'react'
import { Button, Container, Table } from 'react-bootstrap'


const ViewCharDB:React.FC = () => {
  const [characters, setCharacters] = useState([])

  const fetchCharacters = async () => {
    const request = await axios.get('http://127.0.0.1:8000/combatants/data')
    console.log(request.data)
    // sort by character name alphabetically
    setCharacters(request.data.sort((a, b) => a.name.localeCompare(b.name)))
  }

  const addToEncounter = async (char) => {
      const request = await axios.put(`http://127.0.0.1:8000/encounter/${char.name}`)
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
            <th>Name</th>
            <th>Class</th>
            <th>Dexterity</th>
            <th>Other Initiative Modifier</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          {characters.map((char, index) => (
            <tr key={index}>
              <td>{char.name}</td>
              <td>{char.char_class}</td>
              <td>{char.dex_score}</td>
              <td>{char.other_init_mod}</td>
              <td><Button variant="success" className='my-button' onClick={() => addToEncounter(char)}>Add To Encounter</Button></td>
            </tr>
          ))}
        </tbody>

      </Table>
    </Container>
  )
}

export default ViewCharDB