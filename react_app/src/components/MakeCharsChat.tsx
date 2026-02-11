import axios from 'axios'
import React, { useState } from 'react'
import { Button, Card, Form} from 'react-bootstrap'

const MakeCharsChat: React.FC = () => {
    //Creating state to capture LLM input, 
    //output, and making a dynamic "please wait" button to signal users 
    //the chat is currently working and fetching their response
    const [inputJSON, setInputJSON] = useState<string>("")
    const [outputJSON, setOutputJson] = useState<string>("")
    const [input, setInput] = useState<string>("")
    const [output, setOutput] = useState<string>("")
    const [loadingJSON, setLoadingJSON] = useState<boolean>(false)
    const [loading, setLoading] = useState<boolean>(false)
    const [chat, setChat] = useState<string>("");
    const [successMessage, setSuccessMessage] = useState<string>("");
    //Function that sends user input to create character with inputted specification to the chat bot, and receive json
    const chatFunction = async () => {
        setLoadingJSON(true)
        const response = await axios.post("http://127.0.0.1:8000/chat/make_chars_chat", {input: inputJSON})
        console.log(response)
        setChat(response.data)
        const match = response.data.match(/```json\s*([\s\S]*?)\s*```/)
        if (match && match[1]) {
            // Parse once to remove escape characters
            const parsed = JSON.parse(match[1]);

            // Convert back to formatted JSON string
            const prettyJson = JSON.stringify(parsed, null, 2);

            // Wrap in triple backticks
            const finalString = `\`\`\`json${prettyJson}\`\`\``;
            setOutputJson(finalString);
        }

        //const match = response.data.match(/```json\s*([\s\S]*?)\s*```/)
        //const parse = match[1]
        //const parse = match[0].replace(/\n/g, '').replace(/\\/g, '').trim()
        //setOutputJson(parse)
        //setOutputJson(response.data)
        setInputJSON("")
        setLoadingJSON(false)
    }

    //Function that sends JSON data to ingest and make the character
    const ingestFunction = async () => {
      setLoading(true)
        const response = await axios.post("http://127.0.0.1:8000/chat/ingest_chars_from_chat/raw", {input: input})
        console.log(response)
        setOutput(response.data)
        setInput("")
        setLoading(false)
        if (response.status === 200) {
            setSuccessMessage("Character has been successfully created!");
        }
        else {
            setSuccessMessage("Failed to create character.");
        }
    }
  return (
    <Card className="p-4 shadow-sm">
      <Card.Title as="h2" className="mb-4 text-center">
        Make Characters
      </Card.Title>
      <Form.Control
        type="text"
        placeholder="Tell me what character you would like to make."
        value={inputJSON}
        onChange={(event) => setInputJSON(event.target.value)}
        className="mb-4 shadow-sm"
        style={{ maxWidth: "400px", margin: "0 auto" }}
      />
      <div className="d-flex justify-content-center mb-4">
        <Button
          onClick={chatFunction}
          size="lg"
          disabled={loading}
          className="shadow-sm my-button"
          style={{ minWidth: "220px" }}
        >
          {loadingJSON ? "Creating JSON of character" : "JSON character"}
        </Button>
      </div>
      {outputJSON && (
        <>
          {/* <pre>{JSON.stringify(outputJSON, null, 2)}</pre> */}
          <pre>{chat}</pre>
          <div className="text-center mt-2">
            <Button onClick={() => setInput(outputJSON)}>
              Paste into Create Character text box
            </Button>
          </div>
        </>
      )}
      <Form.Control
        type="text"
        placeholder="Paste a characters JSON."
        value={input}
        onChange={(event) => setInput(event.target.value)}
        className="mb-4 shadow-sm"
        style={{ maxWidth: "400px", margin: "0 auto" }}
      />
      <div className="d-flex justify-content-center mb-4">
        <Button
          onClick={ingestFunction}
          size="lg"
          disabled={loading}
          className="shadow-sm my-button"
          style={{ minWidth: "220px" }}
        >
          {loading ? "Ingesting character JSON" : "Create character"}
        </Button>
      </div>
      {successMessage && (
        <div className="text-center text-success mb-3">{successMessage}</div>
      )}
    </Card>
  );
}

export default MakeCharsChat