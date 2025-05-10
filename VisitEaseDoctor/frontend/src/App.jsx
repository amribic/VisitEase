import { useState } from 'react'
import './App.css'
import Login from './Login'
import PatientList from './PatientList'

function App() {
  const [user, setUser] = useState(null)

  if (!user) {
    return <Login onLogin={setUser} />
  }

  return <PatientList />
}

export default App
