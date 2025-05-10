import { useState } from 'react';

function PatientList() {
  // Mocked patient data
  const patients = [
    { id: 1, name: 'John Doe', age: 34 },
    { id: 2, name: 'Jane Smith', age: 28 },
    { id: 3, name: 'Alice Johnson', age: 45 },
    { id: 4, name: 'Bob Brown', age: 52 },
    { id: 5, name: 'Charlie Davis', age: 30 },
    { id: 6, name: 'Diana Evans', age: 39 },
    { id: 7, name: 'Eve Foster', age: 25 },
    { id: 8, name: 'Frank Green', age: 47 },
    { id: 9, name: 'Grace Hall', age: 33 },
    { id: 10, name: 'Henry Irving', age: 41 },
  ];

  const [searchTerm, setSearchTerm] = useState('');

  const filteredPatients = patients.filter(patient =>
    patient.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', width: '100%', backgroundColor: '#f5f5f5' }}>
      <div style={{ backgroundColor: 'white', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
        <h2>Patient List</h2>
        <input
          type="text"
          placeholder="Search patients..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{ width: '100%', padding: '0.5rem', marginBottom: '1rem', border: '1px solid #ddd', borderRadius: '4px' }}
        />
      </div>
      <div style={{ flex: 1, overflowY: 'auto'}}>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {filteredPatients.map((patient) => (
            <li key={patient.id} style={{ margin: '0.5em 0', padding: '1rem', backgroundColor: 'white', borderRadius: '4px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
              <strong>{patient.name}</strong> (Age: {patient.age})
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default PatientList; 