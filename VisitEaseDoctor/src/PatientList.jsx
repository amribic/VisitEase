function PatientList() {
  // Mocked patient data
  const patients = [
    { id: 1, name: 'John Doe', age: 34 },
    { id: 2, name: 'Jane Smith', age: 28 },
    { id: 3, name: 'Alice Johnson', age: 45 },
  ];

  return (
    <div className="card">
      <h2>Patient List</h2>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {patients.map((patient) => (
          <li key={patient.id} style={{ margin: '1em 0' }}>
            <strong>{patient.name}</strong> (Age: {patient.age})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PatientList; 