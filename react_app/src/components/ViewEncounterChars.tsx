import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { Container, Row, Col, Button } from 'react-bootstrap'
import { useNavigate } from 'react-router'

const ViewEncounterChars:React.FC = () => {
  const [encounterChars, setEncounterChars] = useState([])
  const [characters, setCharacters] = useState([])
  const navigate = useNavigate()

  const fetchCharacters = async () => {
    //http://127.0.0.1:8000/combatants/
    const request = await axios.get('http://127.0.0.1:8000/combatants/data')
    setCharacters(request.data)
    // sort by character name alphabetically
    setCharacters(request.data.sort((a, b) => a.name.localeCompare(b.name)))
    console.log(request.data)
  }

  const fetchEncounterChars = async () => {
  //   curl -X 'GET' \
  // 'http://127.0.0.1:8000/encounter/data/' \
  // -H 'accept: application/json'
    const request = await axios.get('http://127.0.0.1:8000/encounter')
    setEncounterChars(request.data)
    console.log(request.data)
  }

  const addToEncounter = async (char) => {
  //   curl -X 'PUT' \
  // 'http://127.0.0.1:8000/encounter/?name=Anders' \
  // -H 'accept: application/json'
    const request = await axios.put(`http://127.0.0.1:8000/encounter/${char.name}`)
    console.log(request.data)
    setEncounterChars(request.data.encounter)
  }
  
  const clearEncounter = async () => {
  //   curl -X 'DELETE' \
  // 'http://127.0.0.1:8000/encounter/' \
  // -H 'accept: application/json'
  const request = await axios.delete('http://127.0.0.1:8000/encounter')
  console.log(request.data) 
  alert(request.data.message)
  setEncounterChars([])
  }

  const removeFromEncounter = async (char) => {
  //   curl -X 'DELETE' \
  // 'http://127.0.0.1:8000/encounter/Anders' \
  // -H 'accept: application/json'
    const request = await axios.delete(`http://127.0.0.1:8000/encounter/${char.name}`)
    console.log(request.data)
    setEncounterChars(request.data.encounter)

  }

  
  useEffect(() => {
    fetchCharacters()
    fetchEncounterChars()
  }, [])


  return (
    <Container>
      <Row>

        <Col> 
          <h1>All Characters</h1>
          <ul>
            {characters.map((char, index) => (
              <li key={index}>{char.name}
              <Button variant="primary" onClick={() => addToEncounter(char)}>Add to Encounter</Button>
              </li>
            ))}
          </ul>
        </Col>

        <Col> 
          <h1>Encounter Characters<Button variant="secondary" onClick={clearEncounter}>Clear Encounter</Button></h1>
          <ul>
            {encounterChars.map((char, index) => (
              <li key={index}>{char.name}<Button variant="danger" onClick={() => removeFromEncounter(char)}>Remove</Button></li>
            ))}
          </ul>
          <Button onClick={() => navigate('/initiativeview')}>Roll Initiative</Button>
        </Col>

      </Row>
    </Container>
  )
}

export default ViewEncounterChars