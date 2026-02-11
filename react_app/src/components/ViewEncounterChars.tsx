import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { Container, Row, Col, Button, Table } from 'react-bootstrap'
import { useNavigate } from 'react-router'

const ViewEncounterChars:React.FC = () => {
  const [encounterChars, setEncounterChars] = useState([])
  const navigate = useNavigate()

  // const fetchCharacters = async () => {
  //   //http://127.0.0.1:8000/combatants/
  //   const request = await axios.get('http://127.0.0.1:8000/combatants/data')
  //   console.log(request.data)
  //   // sort by character name alphabetically
  //   setCharacters(request.data.sort((a, b) => a.name.localeCompare(b.name)))
  // }

  const fetchEncounterChars = async () => {
  //   curl -X 'GET' \
  // 'http://127.0.0.1:8000/encounter/data/' \
  // -H 'accept: application/json'
    const request = await axios.get('http://127.0.0.1:8000/encounter')
    setEncounterChars(request.data)
    console.log(request.data)
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
    fetchEncounterChars()
  }, [])



  return (
    // <Container>
    //   <Row>

    //     <Col> 
    //       <h1>All Characters</h1>
    //       <ul>
    //         {characters.map((char, index) => (
    //           <li key={index}>{char.name}
    //           <Button variant="primary" onClick={() => addToEncounter(char)}>Add to Encounter</Button>
    //           </li>
    //         ))}
    //       </ul>
    //     </Col>

    //     <Col> 
    //       <h1>Encounter Characters<Button variant="secondary" onClick={clearEncounter}>Clear Encounter</Button></h1>
    //       <ul>
    //         {encounterChars.map((char, index) => (
    //           <li key={index}>{char.name}<Button variant="danger" onClick={() => removeFromEncounter(char)}>Remove</Button></li>
    //         ))}
    //       </ul>
    //       <Button onClick={() => navigate('/initiativeview')}>Roll Initiative</Button>
    //     </Col>

    //   </Row>
    // </Container>
    <Container>
      <Row className="align-items-center">
        <Col className="text-center"> 
          <h1>Encounter Characters</h1>
        </Col>
        <Col className="text-center">
          <Button className='my-button' variant="secondary" onClick={clearEncounter}>Clear Encounter</Button>
        </Col>
        <Col className="text-center">
          <Button  className='my-button' onClick={() => navigate('/initiativeview')}>Roll Initiative</Button>
        </Col>
      </Row>
      <hr className='border-3'/>
      <Table striped>
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Class</th>
            <th>Dexterity</th>
            <th>Other Initiative Modifier</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          {encounterChars.map((char, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{char.name}</td>
              <td>{char.char_class}</td>
              <td>{char.dex_score}</td>
              <td>{char.other_init_mod}</td>
              <td><Button variant="danger" className='my-button' onClick={() => removeFromEncounter(char)}>Remove From Encounter</Button></td>
            </tr>
          ))}
        </tbody>

      </Table>
    </Container>
  )
}

export default ViewEncounterChars