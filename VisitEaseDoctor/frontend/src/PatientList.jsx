import { useState, useEffect } from 'react';
import './PatientList.css';
import PatientDetail from './PatientDetail';

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

function getInitials(name) {
  return name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase();
}

function PatientList() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [debugInfo, setDebugInfo] = useState({
    userIds: [],
    failedUsers: [],
    processingTime: null,
    lastError: null
  });

  useEffect(() => {
    const fetchPatients = async () => {
      console.log('Starting to fetch patients...');
      const startTime = Date.now();
      const failedUsers = [];

      try {
        // Fetch user IDs
        console.log('Fetching user IDs from /get-user-ids...');
        const response = await fetch('http://localhost:8080/get-user-ids');
        if (!response.ok) {
          const errorText = await response.text();
          console.error('Failed to fetch user IDs:', {
            status: response.status,
            statusText: response.statusText,
            error: errorText
          });
          throw new Error(`Failed to fetch patients: ${response.status} ${response.statusText}`);
        }
        
        const userIds = await response.json();
        console.log('Received user IDs:', userIds);
        setDebugInfo(prev => ({ ...prev, userIds }));
        
        // Fetch structured data for each user
        console.log('Starting to fetch structured data for each user...');
        const patientPromises = userIds.map(async (userId) => {
          try {
            // Try to fetch structured data first
            const dataResponse = await fetch(`http://localhost:8080/get-structured-data?user_id=${userId}`);
            let userData = null;
            let insuranceCard = {};
            let doctorLetter = {};
            let name = '';
            let age = 'N/A';
            let gender = 'N/A';
            let lastVisit = 'N/A';
            let appointmentTime = 'N/A';
            let incomplete = false;
            let email = '';
            let createdAt = '';

            if (dataResponse.ok) {
              userData = await dataResponse.json();
              insuranceCard = userData.insuranceCard || {};
              doctorLetter = userData.doctorLetter || {};
              if (insuranceCard.name && insuranceCard.name.trim() !== '') {
                name = insuranceCard.name;
              }
              age = calculateAge(insuranceCard.birthDate) || 'N/A';
              gender = insuranceCard.gender || 'N/A';
              lastVisit = formatDate(doctorLetter.created_at) || 'N/A';
            }

            // If no insurance name, fetch registration info
            if (!name || name.trim() === '') {
              const profileResponse = await fetch(`http://localhost:8080/get-user-basic-profile?user_id=${userId}`);
              if (profileResponse.ok) {
                const profile = await profileResponse.json();
                if (profile.full_name && profile.full_name.trim() !== '') {
                  name = profile.full_name;
                  age = calculateAge(profile.date_of_birth) || 'N/A';
                  email = profile.email || '';
                  createdAt = profile.created_at || '';
                  incomplete = true;
                }
              }
            }

            // If still no name, fallback
            if (!name || name.trim() === '') name = 'Unknown Patient';

            return {
              id: userId,
              name,
              age,
              gender,
              lastVisit,
              appointmentTime,
              email,
              createdAt,
              data: userData,
              incomplete
            };
          } catch (err) {
            // If both fetches fail, return a placeholder patient
            console.error(`Error processing user ${userId}:`, err);
            failedUsers.push({ id: userId, error: err.message });
            return {
              id: userId,
              name: 'Unknown Patient',
              age: 'N/A',
              gender: 'N/A',
              lastVisit: 'N/A',
              appointmentTime: 'N/A',
              email: '',
              createdAt: '',
              data: null,
              incomplete: true
            };
          }
        });

        const patientsData = (await Promise.all(patientPromises)).filter(Boolean);
        console.log('Final processed patients data:', patientsData);
        
        setPatients(patientsData);
        setDebugInfo(prev => ({
          ...prev,
          failedUsers,
          processingTime: Date.now() - startTime,
          lastError: null
        }));
      } catch (err) {
        console.error('Error in fetchPatients:', err);
        setError(err.message);
        setDebugInfo(prev => ({
          ...prev,
          lastError: err.message,
          processingTime: Date.now() - startTime
        }));
      } finally {
        setLoading(false);
      }
    };

    fetchPatients();
  }, []);

  const calculateAge = (birthDate) => {
    if (!birthDate) {
      console.log('No birth date provided for age calculation');
      return null;
    }
    try {
      const birth = new Date(birthDate);
      const today = new Date();
      let age = today.getFullYear() - birth.getFullYear();
      const monthDiff = today.getMonth() - birth.getMonth();
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
        age--;
      }
      console.log(`Calculated age ${age} from birth date ${birthDate}`);
      return age;
    } catch (err) {
      console.error('Error calculating age:', err);
      return null;
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) {
      console.log('No date string provided for formatting');
      return null;
    }
    try {
      const date = new Date(dateString);
      const formatted = date.toLocaleDateString('de-DE');
      console.log(`Formatted date ${dateString} to ${formatted}`);
      return formatted;
    } catch (err) {
      console.error('Error formatting date:', err);
      return null;
    }
  };

  const filteredPatients = patients.filter(patient =>
    patient.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Debug information display
  const renderDebugInfo = () => {
    if (process.env.NODE_ENV === 'development') {
      return (
        <div style={{ 
          position: 'fixed', 
          bottom: 0, 
          right: 0, 
          background: 'rgba(0,0,0,0.8)', 
          color: 'white', 
          padding: '10px',
          fontSize: '12px',
          maxHeight: '200px',
          overflow: 'auto',
          zIndex: 1000
        }}>
          <h4>Debug Info:</h4>
          <div>Total Users: {debugInfo.userIds.length}</div>
          <div>Failed Users: {debugInfo.failedUsers.length}</div>
          <div>Processing Time: {debugInfo.processingTime}ms</div>
          {debugInfo.lastError && <div>Last Error: {debugInfo.lastError}</div>}
          {debugInfo.failedUsers.length > 0 && (
            <div>
              Failed Users Details:
              {debugInfo.failedUsers.map((user, idx) => (
                <div key={idx}>User {user.id}: {user.error}</div>
              ))}
            </div>
          )}
        </div>
      );
    }
    return null;
  };

  if (loading) {
    return (
      <div className="patient-app-bg">
        <div>Loading...</div>
        {renderDebugInfo()}
      </div>
    );
  }

  if (error) {
    return (
      <div className="patient-app-bg">
        <div>Error: {error}</div>
        {renderDebugInfo()}
      </div>
    );
  }

  if (selectedPatient) {
    return <PatientDetail patient={selectedPatient} onBack={() => setSelectedPatient(null)} />;
  }

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
                <th>Appointment Time</th>
              </tr>
            </thead>
            <tbody>
              {filteredPatients.map((patient, idx) => (
                <tr key={patient.id} style={{ cursor: 'pointer' }} onClick={() => setSelectedPatient(patient)}>
                  <td>
                    <span className="patient-avatar-table" style={{ background: avatarColors[idx % avatarColors.length] }}>
                      {getInitials(patient.name)}
                    </span>
                    <span className="patient-fullname">{patient.name}</span>
                  </td>
                  <td>{patient.age}</td>
                  <td>{patient.gender}</td>
                  <td>{patient.lastVisit}</td>
                  <td>{patient.appointmentTime}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      {renderDebugInfo()}
    </div>
  );
}

export default PatientList; 
