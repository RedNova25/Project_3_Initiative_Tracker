import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'
import { Container, Table } from 'react-bootstrap'

const InitiativeView = () => {
  const [encounterChars, setEncounterChars] = useState([])
  const navigate = useNavigate()

  const fetchEncounterChars = async () => {
  //   curl -X 'GET' \
  // 'http://127.0.0.1:8000/encounter/' \
  // -H 'accept: application/json'
    const request = await axios.get('http://127.0.0.1:8000/encounter/')
    setEncounterChars(request.data)
    // for each character add a roll to the character object with a random number between 1 and 20
    // setEncounterChars(request.data.map(char => ({...char, init_roll: Math.floor(Math.random() * 20) + 1})))
    // sort by initiative order (dex_score + other_init_mod + init_roll)
    setEncounterChars(request.data.map(char => ({...char, init_roll: Math.floor(Math.random() * 20) + 1})).sort((a, b) => (b.dex_score + b.other_init_mod + b.init_roll) - (a.dex_score + a.other_init_mod + a.init_roll))) 
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
            <th>#</th>
            <th>Name</th>
            <th>Class</th>
            <th>Dexterity Init Mod +</th>
            <th>Other Init Mod +</th>
            <th>Roll =</th>
            <th>Total Initiative</th>
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
              <td>{char.init_roll}</td>
              <td>{char.dex_score + char.other_init_mod + char.init_roll}</td>
            </tr>
          ))}
        </tbody>

      </Table>
    </Container>
  )
}

export default InitiativeView