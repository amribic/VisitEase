import { useState } from 'react';
import './PatientList.css';

const avatarColors = [
  '#F9D97A', // yellow
  '#B6E2D3', // green
  '#BFD7F3', // blue
  '#F7B7A3', // orange
  '#E2C2F9', // purple
  '#F9E2AE', // light yellow
  '#A3D8F7', // light blue
  '#F7C6C7', // pink
  '#C2F9E2', // mint
  '#F9B7E2', // magenta
];

const patients = [
  { name: 'Maria Schmidt', age: 45, gender: 'Female', lastVisit: '15.03.2024' },
  { name: 'Hans Müller', age: 62, gender: 'Male', lastVisit: '10.03.2024' },
  { name: 'Klaus Weber', age: 70, gender: 'Male', lastVisit: '05.03.2024' },
  { name: 'Friedrich Becker', age: 89, gender: 'Male', lastVisit: '01.03.2024' },
  { name: 'Sophie Fischer', age: 31, gender: 'Female', lastVisit: '20.02.2024' },
  { name: 'Wilhelm Hoffmann', age: 90, gender: 'Male', lastVisit: '15.02.2024' },
  { name: 'Anna Wagner', age: 84, gender: 'Female', lastVisit: '10.02.2024' },
  { name: 'Heinrich Schulz', age: 95, gender: 'Male', lastVisit: '05.02.2024' },
  { name: 'Elisabeth Bauer', age: 84, gender: 'Female', lastVisit: '01.02.2024' },
];

function getInitials(name) {
  return name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase();
}

function PatientList() {
  const [searchTerm, setSearchTerm] = useState('');
  const filteredPatients = patients.filter(patient =>
    patient.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="patient-app-bg">
      <div className="patient-navbar">
        <h1 className="patient-list-title">Patient list</h1>
      </div>
      <div className="patient-list-layout">
        <div className="patient-filter-bar">
          <input
            type="text"
            placeholder="Search patient..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="patient-search-input"
          />
          {/* Add more filter fields here as needed */}
          <button className="filter-reset-btn">Reset filter</button>
          <button className="more-filter-btn">More</button>
        </div>
        <div className="patient-table-wrapper">
          <table className="patient-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Age</th>
                <th>Gender</th>
                <th>Last Visit</th>
              </tr>
            </thead>
            <tbody>
              {filteredPatients.map((patient, idx) => (
                <tr key={patient.name}>
                  <td>
                    <span className="patient-avatar-table" style={{ background: avatarColors[idx % avatarColors.length] }}>
                      {getInitials(patient.name)}
                    </span>
                    <span className="patient-fullname">{patient.name}</span>
                  </td>
                  <td>{patient.age}</td>
                  <td>{patient.gender}</td>
                  <td>{patient.lastVisit}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default PatientList; 