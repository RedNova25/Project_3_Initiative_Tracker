import axios from 'axios'
import {useState , useEffect } from 'react'
import { Container, Table } from 'react-bootstrap'


const ViewCharDB:React.FC = () => {
  const [characters, setCharacters] = useState([])

  const fetchCharacters = async () => {
    const request = await axios.get('http://127.0.0.1:8000/combatants/data')
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
            <th>Class</th>
            <th>Dexterity</th>
            <th>Other Initiative Modifier</th>
          </tr>
        </thead>

        <tbody>
          {characters.map((char, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{char.name}</td>
              <td>{char.char_class}</td>
              <td>{char.dex_score}</td>
              <td>{char.other_init_mod}</td>
            </tr>
          ))}
        </tbody>

      </Table>
    </Container>
  )
}

export default ViewCharDB