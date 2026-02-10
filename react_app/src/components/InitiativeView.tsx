import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { Container, Table } from 'react-bootstrap'

const InitiativeView:React.FC = () => {
  const [encounterChars, setEncounterChars] = useState([])

  const fetchEncounterChars = async () => {
  //   curl -X 'GET' \
  // 'http://127.0.0.1:8000/encounter/' \
  // -H 'accept: application/json'
    const request = await axios.get('http://127.0.0.1:8000/encounter/rolls')
    setEncounterChars(request.data)
    console.log(request.data)
  }

  
  useEffect(() => {
    fetchEncounterChars()
  }, [])

  return (
    <Container>
      <Table striped>

        <thead>
          <tr>
            <th>Initiative</th>
            <th>Name</th>
            <th>Dexterity Modifier</th>
            <th>Other Modifier</th>
            <th>Roll</th>
          </tr>
        </thead>

        <tbody>
          {encounterChars.map((char, index) => (
            <tr key={index}>
              <td>{char.initiative}</td>
              <td>{char.name}</td>
              <td>{char.dex_init_mod}</td>
              <td>{char.other_init_mod}</td>
              <td>{char.init_roll}</td>
            </tr>
          ))}
        </tbody>

      </Table>
    </Container>
  )
}

export default InitiativeView