import axios from 'axios'
import React, { useState } from 'react'
import { Button, Card, Container, Form, Table } from 'react-bootstrap'

const FindCharsChat: React.FC = () => {
    //Creating state to capture LLM input, 
    //output, and making a dynamic "please wait" button to signal users 
    //the chat is currently working and fetching their response
    const [input, setInput] = useState<string>("")
    const [output, setOutput] = useState<string>("")
    const [loading, setLoading] = useState<boolean>(false)
    
    //Function that sends user input for character and captures response
    const chatFunction = async () => {
        setLoading(true)
        const response = await axios.post("http://127.0.0.1:8000/chat/find_char_chat", {query: input})
        console.log(response)
        setOutput(response.data)

        setInput("")
        setLoading(false)
    }
    //Function allows the button to add to encounter functionality to work
    const addToEncounter = async (name) => {
      const request = await axios.put(`http://127.0.0.1:8000/encounter/${name}`)
      console.log(request.data)
    }
  return (
    <Card className="p-4 shadow-sm">
      <Card.Title as="h2" className="mb-4 text-center">Find Characters</Card.Title>
      <Form.Control
        type="text"
        placeholder="Tell me what characters or classes you are looking for."
        value={input}
        onChange={(event) => setInput(event.target.value)}
        className="mb-4 shadow-sm"
        style={{ maxWidth: "400px", margin: "0 auto" }}
      />
      <div className="d-flex justify-content-center mb-4">
      <Button onClick={chatFunction} size="lg" disabled={loading} className="shadow-sm" style={{ minWidth: "220px" }}>
        {loading ? "Fetching character" : "Find character"}
      </Button>
      </div>
      <Container>
        {output && output.trim().length > 0 && (
        <Table striped>
          <thead>
            <tr>
              <th>Name</th>
              <th>Class</th>
              <th>Dexterity</th>
              <th>Other Initiative Modifier</th>
            </tr>
          </thead>

          <tbody>
            {output
            .trim()
            .split("\n\n")
            .map((block, index) => {
        const lines = block.split("\n");

        const name = lines[0]?.replace(/^Name:\s*/i, "");
        const charClassLine = lines.find(l =>/^Class:|^Char Class:|^Char_class:/i.test(l));
        const charClass = charClassLine?.split(":")[1]?.trim();
        const dexLine = lines.find(l => /^Dexterity:|^Dexterity Score:/i.test(l));
        const dex = dexLine?.split(":")[1]?.trim();
        const init = lines.find(l => l.startsWith("Other Initiative Modifier:"))?.split(": ")[1];

        return (
          <tr key={index}>
            <td>{name}</td>
            <td>{charClass}</td>
            <td>{dex}</td>
            <td>{init}</td>
            <td><Button variant="success" onClick={() => addToEncounter(name)}>Add To Encounter</Button></td>
          </tr>
        );
      })}
          </tbody>
        </Table>
    )}
      </Container>
    </Card>
  );
}

export default FindCharsChat