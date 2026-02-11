import NavBar from './components/NavBar'
import { Route, Routes } from 'react-router-dom'
// components
import InitiativeView from './components/InitiativeView'
import ViewEncounterChars from './components/ViewEncounterChars'
import Home from './components/Home'
import ViewCharDB from './components/ViewCharDB'
// css
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'
import FindCharsChat from './components/FindCharsChat'
import MakeCharsChat from './components/MakeCharsChat'


function App() {


  return (
    <>
    
      <NavBar />
      
      <Routes>
        <Route path="/" element={<Home />}  />
        <Route path="/viewcharacterdb" element={<ViewCharDB />}  />
        <Route path="/initiativeview" element={<InitiativeView />} />
        <Route path="/viewencounterchars" element={<ViewEncounterChars/>}  />
        <Route path="/findcharschat" element={<FindCharsChat/>}/>
        <Route path="/makecharschat" element={<MakeCharsChat/>}/>
      </Routes>

    </>
  )
}

export default App
